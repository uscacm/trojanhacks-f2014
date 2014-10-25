from flask import Flask
from flask import render_template
from flask import url_for
app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/hello_page/")
@app.route("/hello_page/<name>")
def hello_page(name=None):
  return render_template("hello.html", name = name);

@app.route("/hello/")
def hello():
  return "Hello World!"

@app.route("/hello/<name>")
def hello_name(name):
  return "Hello %s!" % name

if __name__ == "__main__":
  app.run(debug=True)
