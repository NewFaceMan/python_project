import tkinter as tk
from tkinter import messagebox

def show_login():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="ID:").grid(row=0, column=0)
    tk.Entry(root).grid(row=0, column=1)
    tk.Label(root, text="Pw:").grid(row=1, column=0)
    tk.Entry(root, show="*").grid(row=1, column=1)
    tk.Button(root, text="로그인", command=login).grid(row=2, columnspan=2)

def show_signup():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="ID:").grid(row=0, column=0)
    id_entry = tk.Entry(root)
    id_entry.grid(row=0, column=1)
    
    tk.Label(root, text="PW:").grid(row=1, column=0)
    pw_entry = tk.Entry(root, show="*")
    pw_entry.grid(row=1, column=1)
    
    tk.Label(root, text="이름:").grid(row=2, column=0)
    name_entry = tk.Entry(root)
    name_entry.grid(row=2, column=1)
    
    tk.Label(root, text="나이:").grid(row=3, column=0)
    age_entry = tk.Entry(root)
    age_entry.grid(row=3, column=1)
    
    tk.Label(root, text="성별:").grid(row=4, column=0)
    gender_entry = tk.Entry(root)
    gender_entry.grid(row=4, column=1)
    
    tk.Label(root, text="생일:").grid(row=5, column=0)
    birthday_entry = tk.Entry(root)
    birthday_entry.grid(row=5, column=1)
    
    tk.Button(root, text="회원가입", command=lambda: signup(id_entry.get(), pw_entry.get(), name_entry.get(), age_entry.get(), gender_entry.get(), birthday_entry.get())).grid(row=6, columnspan=2)

def login():
    messagebox.showinfo("로그인", "로그인 기능은 아직 구현되지 않았습니다.")

def signup(id, pw, name, age, gender, birthday):
    with open("users.txt", "a") as file:
        file.write(f"{id},{pw},{name},{age},{gender},{birthday}\n")
    messagebox.showinfo("회원가입", "회원가입이 완료되었습니다.")
    show_main_menu()

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Button(root, text="로그인 하기", command=show_login).grid(row=0, column=0)
    tk.Button(root, text="회원가입 하기", command=show_signup).grid(row=0, column=1)

root = tk.Tk()
root.title("로그인 및 회원가입")
show_main_menu()
root.mainloop()
