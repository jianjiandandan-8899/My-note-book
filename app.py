from flask import Flask, render_template, request,redirect, url_for

app = Flask(__name__)

notes = [
    {
        "title":"first note",
        "content":"this is my first note"
    },
    {
        "title":"second note",
        "content":"this is my second note" 
    }
]


@app.route("/")
def home():

    return render_template("notes.html", notes = notes)

@app.route("/add", methods=["GET","POST"])
def add_note():
    if request.method == "GET":
        return render_template("add.html")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        note={
            "title": title,
            "content": content
        }

        notes.append(note)
        return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(debug=True)
    