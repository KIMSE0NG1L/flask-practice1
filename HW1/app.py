from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/profile")
def profile():
    hobbies = ["개발", "주식", "운동"]
    return render_template("profile.html", hobbies=hobbies)


@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)
