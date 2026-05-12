import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# DB作成
conn = sqlite3.connect("todo.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT
)
""")

conn.commit()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        task = request.form.get("task")

        if task:
            cursor.execute(
                "INSERT INTO tasks (task) VALUES (?)",
                (task,)
            )

            conn.commit()

        return redirect("/")

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)