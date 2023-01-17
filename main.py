from flask import Flask, request, render_template, redirect, url_for, flash,session
from flask_session import Session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration settings
app.config['MYSQL_USER'] = 'ng169'
app.config['MYSQL_PASSWORD'] = 'test123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'magazinesite'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL()
mysql.init_app(app)

app.config['SECRET_KEY'] = 'secretkey'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/')
def home():
    cur = mysql.connection.cursor()
    id = session.get("id")
    data = None
    type = session.get("type")
    if id and type == "user":
        cur.execute(f"Select * from user where id = {id}")
        data = cur.fetchone()
    elif id and type == "author":
        cur.execute(f"Select * from author where id = {id}")
        data = cur.fetchone()
    return render_template("index.html",data = data,type=type)


# ---------------------------AUTHENTICATION ---------------------------
@app.route('/login/user', methods=["GET", "POST"])
def login_user():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cur.execute(f"select * from login where email_id = '{email}'")
        user = cur.fetchone()
        if user and user["password"] == password:
            cur.execute(f"select id from user where email = '{email}'")
            user_id = cur.fetchone()
            session["id"] = user_id["id"] 
            session["type"] = "user"
            return redirect(url_for("home"))
        else:
            flash("Wrong password")
    return render_template("auth/loginUser.html")

@app.route('/login/author', methods=["GET", "POST"])
def login_author():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cur.execute(f"select * from login where email_id = '{email}'")
        author = cur.fetchone()
        if author and author["password"] == password:
            cur.execute(f"select id from author where email = '{email}'")
            author_id = cur.fetchone()
            session["id"] = author_id["id"] 
            session["type"] = "author"
            return redirect(url_for("home"))
        else:
            flash("Wrong password")
    return render_template("auth/loginAuthor.html")


@app.route('/register/user', methods=["GET", "POST"])
def register_user():
    cur = mysql.connection.cursor()
    if request.method=="POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        address = request.form.get("address")
        password = request.form.get("password")
        type = "user"
        cur.execute("INSERT INTO login VALUES (%s, %s,%s)", (email, password,type))
        cur.execute("INSERT INTO user (name, phone,address,email) VALUES (%s, %s,%s,%s)", (name, phnum,address,email))
        mysql.connection.commit()
        return redirect(url_for("login_user"))
    return render_template("auth/registerUser.html")

@app.route('/register/author', methods=["GET", "POST"])
def register_author():
    cur = mysql.connection.cursor()
    if request.method=="POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        address = request.form.get("address")
        password = request.form.get("password")
        type = "author"
        cur.execute("INSERT INTO login VALUES (%s, %s,%s)", (email, password,type))
        cur.execute("INSERT INTO author (name, phone,address,email) VALUES (%s, %s,%s,%s)", (name, phnum,address,email))
        mysql.connection.commit()
        return redirect(url_for("login_author"))
    return render_template("auth/registerAuthor.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session["id"]=None
    session["type"]=None
    return redirect(url_for("home"))

#---------------------------magazine ---------------------------
@app.route('/magazine/add',methods = ["GET","POST"])
def add_magazine():
    cur = mysql.connection.cursor()
    if session.get("type") != "author":
        return redirect(url_for("login_author"))
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("editor1")
        author_id = session.get("id")
        cur.execute("insert into magazine(title,description,content,author_id) values(%s,%s,%s,%s)",(title,description,content,author_id))
        mysql.connection.commit()
        return redirect(url_for("home"))
    return render_template("magazine/add.html")

@app.route('/magazine/view/<int:id>',methods = ["GET"])
def view_magazine(id):
    cur = mysql.connection.cursor()
    cur.execute(f"select * from magazine where id = {id}")
    mag_data = cur.fetchone()
    ismagAuthor = False
    if session.get("type")=="author" and mag_data["author_id"]==session.get("id"):
        ismagAuthor=True
    return render_template("magazine/view.html",mag=mag_data,ismagAuthor=ismagAuthor)
    
@app.route('/magazine/edit/<int:id>',methods = ["GET","POST"])
def edit_magazine(id):
    cur = mysql.connection.cursor()
    cur.execute(f"select * from magazine where id = {id}")
    mag_data = cur.fetchone()
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("editor1")
        cur.execute("update magazine set title =%s ,description=%s ,content=%s where id = %s",(title,description,content,id))
        mysql.connection.commit()
        return redirect(url_for("view_magazine",id = id))
    return render_template("magazine/edit.html",mag = mag_data)

@app.route('/magazine/delete/<int:id>',methods = ["GET"])
def delete_magazine(id):
    cur = mysql.connection.cursor()
    cur.execute(f"delete from magazine where id = {id} ")
    mysql.connection.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)