from flask import Flask, render_template, request,redirect, url_for
import sqlite3
from db import init_db



app = Flask(__name__)


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

        sql = f"INSERT INTO notes (title, content) VALUES ('{title}', '{content}')"
        cursor.execute(sql)

        conn.commit()
        conn.close()


        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/search", methods=["GET","POST"])
def search_note():
    if request.method == "POST":
        keyword = request.form["keyword"]

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        
        sql = f"SELECT id, title, content FROM notes WHERE title LIKE '%{keyword}%'"
        cursor.execute(sql)
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




    
if __name__ == "__main__":
    app.run(debug=True)
    