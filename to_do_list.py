from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

USER_DATA_FILE = "user_data.txt"
TASK_DATA_FILE = "tasks.txt"

# 사용자 정보를 파일에서 읽어오기
def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, "r") as file:
        lines = file.readlines()
        return [line.strip().split(",") for line in lines]

# 작업 데이터를 파일에서 읽어오기
def load_task_data():
    if not os.path.exists(TASK_DATA_FILE):
        return []
    with open(TASK_DATA_FILE, "r") as file:
        lines = file.readlines()
        return [line.strip().split(",") for line in lines]

# 작업 데이터를 파일에 저장
def save_task_data(task_data):
    with open(TASK_DATA_FILE, "a") as file:
        file.write(",".join(task_data) + "\n")

# 작업 데이터를 파일에 덮어쓰기
def overwrite_task_data(tasks):
    with open(TASK_DATA_FILE, "w") as file:
        for task in tasks:
            file.write(",".join(task) + "\n")

# 홈 페이지
@app.route("/")
def home():
    return render_template("index.html")

# 회원가입 페이지
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        birthday = request.form["birthday"]

        # 비밀번호 확인
        if password != confirm_password:
            flash("비밀번호가 일치하지 않습니다!")
            return redirect(url_for("signup"))

        # 중복 아이디 확인
        users = load_user_data()
        for user in users:
            if user[0] == user_id:
                flash("이미 존재하는 아이디입니다!")
                return redirect(url_for("signup"))

        # 사용자 정보 저장
        with open(USER_DATA_FILE, "a") as file:
            file.write(",".join([user_id, password, name, age, gender, birthday]) + "\n")
        flash("회원가입이 완료되었습니다. 로그인 해주세요.")
        return redirect(url_for("login"))
    return render_template("signup.html")

# 로그인 페이지
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        users = load_user_data()
        for user in users:
            if user[0] == user_id and user[1] == password:
                return redirect(url_for("dashboard", user_id=user_id))
        flash("로그인 실패! 아이디 또는 비밀번호를 확인하세요.")
    return render_template("login.html")

# 대시보드
@app.route("/dashboard/<user_id>")
def dashboard(user_id):
    tasks = [task for task in load_task_data() if task[0] == user_id]
    return render_template("dashboard.html", user_id=user_id, tasks=tasks)

# 작업 추가
@app.route("/add_task/<user_id>", methods=["GET", "POST"])
def add_task(user_id):
    if request.method == "POST":
        task_name = request.form["task_name"]
        task_description = request.form["task_description"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        save_task_data([user_id, task_name, task_description, start_date, end_date, "해야 할 일"])
        flash("작업이 추가되었습니다.")
        return redirect(url_for("dashboard", user_id=user_id))
    return render_template("add_task.html", user_id=user_id)

# 작업 수정
@app.route("/edit_task/<user_id>/<task_name>", methods=["GET", "POST"])
def edit_task(user_id, task_name):
    tasks = load_task_data()
    task_to_edit = None

    for task in tasks:
        if task[0] == user_id and task[1] == task_name:
            task_to_edit = task
            break

    if not task_to_edit:
        flash("수정할 작업을 찾을 수 없습니다.")
        return redirect(url_for("dashboard", user_id=user_id))

    if request.method == "POST":
        task_to_edit[2] = request.form["task_description"]
        task_to_edit[5] = request.form["status"]
        overwrite_task_data(tasks)
        flash("작업이 수정되었습니다.")
        return redirect(url_for("dashboard", user_id=user_id))

    return render_template("edit_task.html", user_id=user_id, task=task_to_edit)

# 상태별 작업 보기
@app.route("/view_tasks/<user_id>/<status>")
def view_tasks(user_id, status):
    tasks = [task for task in load_task_data() if task[0] == user_id and task[5] == status]
    return render_template("view_tasks.html", user_id=user_id, tasks=tasks, status=status)

@app.route("/edit_task/<user_id>/<task_name>", methods=["GET", "POST"])
def edit_task(user_id, task_name):
    # 모든 작업 데이터 로드
    tasks = load_task_data()
    task_to_edit = None

    # 수정할 작업 찾기
    for task in tasks:
        if task[0] == user_id and task[1] == task_name:
            task_to_edit = task
            break

    if not task_to_edit:
        flash("수정할 작업을 찾을 수 없습니다.")
        return redirect(url_for("dashboard", user_id=user_id))

    if request.method == "POST":
        # 작업 설명과 상태 업데이트
        task_to_edit[2] = request.form["task_description"]  # 설명 업데이트
        task_to_edit[5] = request.form["status"]  # 상태 업데이트
        overwrite_task_data(tasks)  # 수정된 데이터를 파일에 저장
        flash("작업이 수정되었습니다.")
        return redirect(url_for("dashboard", user_id=user_id))

    return render_template("edit_task.html", user_id=user_id, task=task_to_edit)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5500)