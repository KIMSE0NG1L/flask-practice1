import os

from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_restx import Api, Resource, fields, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Flask-SQLAlchemy 는 SQLAlchemy(app) 호출 시점의 URI로 엔진을 한 번만 만든다.
# test_api.py 가 import 전에 이 환경변수를 바꿔서 메모리 DB로 띄운다 (74쪽 setUp 참고).
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TODO_DATABASE_URI", "sqlite:///todo.db")
app.config["ERROR_404_HELP"] = False  # 404 메시지에 "did you mean" 안내문이 붙지 않게 한다
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200), default="")
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Todo {self.id} {self.text}>"


# ----- 화면 (브라우저용) -----

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        todo = Todo(text=request.form["todo"], note=request.form.get("note", ""))
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("index"))

    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/toggle/<int:id>")
def toggle(id):
    todo = db.get_or_404(Todo, id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete(id):
    todo = db.get_or_404(Todo, id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = db.get_or_404(Todo, id)
    if request.method == "POST":
        todo.text = request.form["todo"]
        todo.note = request.form.get("note", "")
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo)


# ----- API (/api) -----

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp, doc="/docs", title="Todo API", version="1.0",
          description="HW4 에서 만든 todo 앱의 API")
ns = api.namespace("todos", description="할 일 CRUD")

todo_model = api.model("Todo", {
    "id": fields.Integer(readonly=True, description="할 일의 줄 번호"),
    "text": fields.String(required=True, description="할 일", example="우유 사기"),
    "done": fields.Boolean(description="완료 여부", example=False),
    "note": fields.String(description="설명", example="2리터짜리로"),
})

todo_input = api.model("TodoInput", {
    "text": fields.String(required=True, description="할 일", example="우유 사기"),
    "done": fields.Boolean(description="완료 여부", example=False),
    "note": fields.String(description="설명", example="2리터짜리로"),
})


def get_or_abort(id):
    todo = db.session.get(Todo, id)
    if todo is None:
        abort(404, message=f"{id} 번 할 일이 없습니다")
    return todo


@ns.route("/")
class TodoList(Resource):
    @ns.doc("목록 보기")
    @ns.param("done", "true 면 완료만, false 면 아직 안 한 것만")
    @ns.marshal_list_with(todo_model)
    def get(self):
        """할 일을 돌려준다. done 을 주면 걸러서 돌려준다"""
        q = Todo.query
        done = request.args.get("done")
        if done is not None:
            q = q.filter_by(done=(done.lower() == "true"))
        return q.all()

    @ns.doc("할 일 만들기")
    @ns.expect(todo_input)
    @ns.marshal_with(todo_model, code=201)
    def post(self):
        """할 일을 하나 만든다"""
        todo = Todo(
            text=api.payload["text"],
            done=api.payload.get("done", False),
            note=api.payload.get("note", ""),
        )
        db.session.add(todo)
        db.session.commit()
        return todo, 201


@ns.route("/<int:id>")
@ns.param("id", "할 일의 줄 번호")
@ns.response(404, "그 번호의 할 일이 없습니다")
class TodoItem(Resource):
    @ns.doc("할 일 하나 보기")
    @ns.marshal_with(todo_model)
    def get(self, id):
        """할 일 하나를 돌려준다"""
        return get_or_abort(id)

    @ns.doc("할 일 일부 바꾸기")
    @ns.expect(todo_input)
    @ns.marshal_with(todo_model)
    def patch(self, id):
        """보낸 칸만 바꾼다"""
        todo = get_or_abort(id)
        payload = api.payload or {}
        if "text" in payload:
            todo.text = payload["text"]
        if "done" in payload:
            todo.done = payload["done"]
        if "note" in payload:
            todo.note = payload["note"]
        db.session.commit()
        return todo

    @ns.doc("할 일 지우기")
    def delete(self, id):
        """할 일 하나를 지운다"""
        todo = get_or_abort(id)
        db.session.delete(todo)
        db.session.commit()
        return "", 204


app.register_blueprint(api_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
