create schema magazinesite;
use magazinesite;

CREATE TABLE `magazinesite`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `magazinesite`.`author` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  `email` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

ALTER TABLE `magazinesite`.`author` 
ADD COLUMN `magazine_count` INT NULL DEFAULT 0 AFTER `address`;


CREATE TABLE `magazinesite`.`login` (
  `email_id` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NULL,
  PRIMARY KEY (`email_id`));

ALTER TABLE `magazinesite`.`author` 
ADD INDEX `fk_loginAuthor_idx` (`email` ASC) VISIBLE;
;
ALTER TABLE `magazinesite`.`author` 
ADD CONSTRAINT `fk_loginAuthor`
  FOREIGN KEY (`email`)
  REFERENCES `magazinesite`.`login` (`email_id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE `magazinesite`.`user` 
ADD INDEX `fk_loginUser_idx` (`email` ASC) VISIBLE;
;
ALTER TABLE `magazinesite`.`user` 
ADD CONSTRAINT `fk_loginUser`
  FOREIGN KEY (`email`)
  REFERENCES `magazinesite`.`login` (`email_id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;


CREATE TABLE `magazinesite`.`magazine` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NULL,
  `description` VARCHAR(400) NULL,
  `published_date` DATETIME NULL,
  `number_of_reads` INT NULL DEFAULT 0,
  `number_of_likes` INT NULL DEFAULT 0,
  `author_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_magazine_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_magazine`
    FOREIGN KEY (`author_id`)
    REFERENCES `magazinesite`.`author` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

ALTER TABLE `magazinesite`.`magazine` 
ADD COLUMN `content` VARCHAR(1000) NULL AFTER `author_id`;


CREATE TABLE `magazinesite`.`category` (
  `id` INT NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));


CREATE TABLE `magazinesite`.`comment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `content` VARCHAR(200) NULL,
  `date_added` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comment_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_comment`
    FOREIGN KEY (`user_id`)
    REFERENCES `magazinesite`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


DROP TRIGGER IF EXISTS `magazinesite`.`magazine_BEFORE_INSERT`;

DELIMITER $$
USE `magazinesite`$$
CREATE DEFINER = CURRENT_USER TRIGGER `magazinesite`.`magazine_BEFORE_INSERT` BEFORE INSERT ON `magazine` FOR EACH ROW
BEGIN
SET NEW.published_date = NOW();
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS `magazinesite`.`comment_BEFORE_INSERT`;

DELIMITER $$
USE `magazinesite`$$
CREATE DEFINER = CURRENT_USER TRIGGER `magazinesite`.`comment_BEFORE_INSERT` BEFORE INSERT ON `comment` FOR EACH ROW
BEGIN
SET NEW.date_added = NOW();
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS `magazinesite`.`magazine_AFTER_INSERT`;

DELIMITER $$
USE `magazinesite`$$
CREATE DEFINER = CURRENT_USER TRIGGER `magazinesite`.`magazine_AFTER_INSERT` AFTER INSERT ON `magazine` FOR EACH ROW
BEGIN
UPDATE `author`
SET magazine_count = magazine_count + 1
WHERE `author`.id = NEW.id;
END$$
DELIMITER ;
