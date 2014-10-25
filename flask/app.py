from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import g
import sqlite3
from contextlib import closing

# Configuration
DATABASE = "/tmp/todo.db"
DEBUG = True
SECRET_KEY = ""
USERNAME = "admin"
PASSWORD = "default"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config["DATABASE"])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/hello_page/")
@app.route("/hello_page/<name>")
def hello_page(name=None):
  return render_template("hello.html", name = name)

@app.route("/http", methods=['POST', 'GET'])
def http_demo():
  if request.method == 'POST':
    return "POST Request"
  else:
    return "GET Request"

@app.route("/hello/")
def hello():
  return "Hello World!"

@app.route("/hello/<name>")
def hello_name(name):
  return "Hello %s!" % name

@app.route("/todo/new")
def todo_new():
  return render_template("new_todo.html")

@app.route("/todo/add", methods=["POST"])
def todo_add():
  g.db.execute('insert into tasks (name) values (?)', [request.form['task']])
  g.db.commit()
  return redirect(url_for('todo_show'))

@app.route("/todo")
def todo_show():
  cur = g.db.execute('select id, name from tasks')
  tasks = [dict(tid=row[0], name=row[1]) for row in cur.fetchall()]
  return render_template('todo.html', tasks=tasks)

@app.route("/todo/remove/<int:tid>")
def todo_remove(tid):
  sql_command = "delete from tasks where id=%d" % tid
  g.db.execute(sql_command)
  g.db.commit()
  return redirect(url_for('todo_show'))

if __name__ == "__main__":
  app.run(debug=True)
