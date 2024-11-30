import os

# 사용자 정보 파일 경로
USER_DATA_FILE = "user_data.txt"

# 사용자 정보를 파일에 저장
def save_user_data(user_data):
    with open(USER_DATA_FILE, "a") as file:
        file.write(",".join(user_data) + "\n")

# 사용자 정보를 파일에서 읽어오기
def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, "r") as file:
        lines = file.readlines()
        return [line.strip().split(",") for line in lines]

# 회원가입
def sign_up():
    print("회원가입")
    user_id = input("아이디: ")
    password = input("패스워드: ")
    name = input("이름: ")
    age = input("나이: ")
    gender = input("성별: ")
    birthday = input("생일 (YYYY-MM-DD): ")
    save_user_data([user_id, password, name, age, gender, birthday])
    print("회원가입이 완료되었습니다!")

# 로그인
def log_in():
    print("로그인")
    user_id = input("아이디: ")
    password = input("패스워드: ")
    users = load_user_data()
    for user in users:
        if user[0] == user_id and user[1] == password:
            print(f"로그인 성공! 환영합니다, {user[2]}님.")
            return
    print("로그인 실패! 아이디 또는 패스워드를 확인하세요.")

# 메인 프로그램
def main():
    # 기존 사용자 데이터를 로드
    if not os.path.exists(USER_DATA_FILE):
        print("사용자 데이터 파일이 없습니다. 새로 생성합니다.")
        open(USER_DATA_FILE, "w").close()

    while True:
        print("\n1. 회원가입")
        print("2. 로그인")
        print("3. 종료")
        choice = input("선택: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            log_in()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()