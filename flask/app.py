from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
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

if __name__ == "__main__":
  app.run(debug=True)
