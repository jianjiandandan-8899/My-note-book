from flask import Flask, render_template, request,redirect, url_for
import sqlite3
from db import init_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

app = Flask(__name__)

app.secret_key = "dev-secret-key"


init_db()


@app.route("/")
def home():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, content FROM notes")
    rows = cursor.fetchall()

    conn.close()

    notes = [
        {
            "id": r[0],
            "title": r[1],
            "content": r[2]
        }
        for r in rows
    ]
    return render_template("notes.html", notes = notes)



@app.route("/add", methods=["GET","POST"])
def add_note():
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))

        conn.commit()
        conn.close()


        return redirect(url_for("home"))

    return render_template("add.html")



@app.route("/search", methods=["GET","POST"])
def search_note():
    if request.method == "POST":
        keyword = request.form["keyword"]
        if keyword == "":
            return render_template("search.html", notes=[])

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        

        cursor.execute("SELECT id, title, content FROM notes WHERE title LIKE ?", (f"%{keyword}%",))
        rows = cursor.fetchall()

        notes = [
        {
            "id": r[0],
            "title": r[1],
            "content": r[2]
        }
        for r in rows
        ]
        return render_template("search.html", notes = notes)
    
    return render_template("search.html")

@app.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return render_template("register.html", response="Username and password required")
        

        hashword = generate_password_hash(password)
        
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()


        

        try:
            cursor.execute("insert into users (username, password) VALUES (?, ?)",(username, hashword))
            
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", response="Username already taken")
        
        conn.close()
        return redirect(url_for("login"))
    
    return render_template("register.html" )


@app.route("/login", methods =["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]



        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()

        cursor.execute("select password from users where username =  ? ",(username, ))
        row = cursor.fetchone()

        if row is None:
            response = "Invalid credentials"
            return render_template("login.html", response = response)
        
        stored_hash = row[0]
        
        if check_password_hash(stored_hash, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", response = "Invalid credentials!")
    
    return render_template("login.html")
    

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
    