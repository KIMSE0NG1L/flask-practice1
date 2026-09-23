# app.py
from flask import Flask, render_template
app = Flask(__name__)
@app.route("/hi/<name>")
def hi_template_render(name):
    return render_template("hi.html", name=name)

@app.route("/")
def home():
    return "<h1>메인 페이지</h1>"

@app.route("/about")
def about():
    return "<h1>소개 페이지</h1>"

@app.route("/test/<text>")
def route_sample(text):
    return f"<h1>{text}</h1>"

@app.route("/age/<num>") # 타입 없음
def age_any(num):
    return f"<h1>{num} 살 — 타입은 {type(num).__name__}</h1>"

@app.route("/age2/<int:num>") # 정수만
def age_int(num):
    return f"<h1>{num} 살 — 타입은 {type(num).__name__}</h1>"

# app.py 맨 아래에 추가
if __name__ == "__main__":
    app.run(debug=True)
