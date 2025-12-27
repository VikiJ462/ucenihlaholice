import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# ======================
# DATA LEKCÍ
# ======================

LESSONS = {
    1: [("Ⰰ", "Az", "a"), ("Ⰱ", "Buky", "b"), ("Ⰲ", "Vědě", "v"), ("Ⰳ", "Glagoli", "g")],
    2: [("Ⰴ", "Dobro", "d"), ("Ⰵ", "Jest", "e"), ("Ⰶ", "Živěte", "ž"), ("Ⰷ", "Dzělo", "dz")],
    3: [("Ⰸ", "Zemlja", "z"), ("Ⰹ", "Izhe", "i"), ("Ⰺ", "Initial Izhe", "ji"), ("Ⰻ", "Djerv", "ď")],
}

# ======================
# DATABASE
# ======================

db = sqlite3.connect("userprogress.sql")
cur = db.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS progress (
    xp INTEGER,
    unlocked INTEGER
)
""")
cur.execute("SELECT COUNT(*) FROM progress")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO progress VALUES (0, 1)")
db.commit()

def load_progress():
    cur.execute("SELECT xp, unlocked FROM progress")
    return cur.fetchone()

def save_progress(xp, unlocked):
    cur.execute("UPDATE progress SET xp=?, unlocked=?", (xp, unlocked))
    db.commit()

xp, unlocked = load_progress()

# ======================
# GUI
# ======================

root = tk.Tk()
root.title("Hlaholice Trainer")
root.geometry("420x360")

mode = "menu"
current = []
index = 0
correct = 0

# ======================
# FUNCTIONS
# ======================

def header_text():
    level = xp // 100 + 1
    return f"XP: {xp} | Level: {level} | Odemčeno: {unlocked}"

def show_menu():
    clear()
    header.config(text=header_text())
    tk.Label(root, text="Vyber lekci").pack()
    for i in range(1, unlocked + 1):
        tk.Button(root, text=f"Lekce {i} – učit se",
                  command=lambda i=i: start_learn(i)).pack(pady=2)
        tk.Button(root, text=f"Lekce {i} – test",
                  command=lambda i=i: start_test(i)).pack(pady=2)

def start_learn(lesson):
    global current, index, mode
    mode = "learn"
    current = LESSONS[lesson]
    index = 0
    clear()
    next_learn()

def next_learn():
    if index >= len(current):
        messagebox.showinfo("Hotovo", "Lekce projeta 👍\nTeď můžeš jít na test.")
        show_menu()
        return

    char, name, sound = current[index]
    clear()
    tk.Label(root, text=char, font=("Arial", 48)).pack()
    tk.Label(root, text=f"Název: {name}", font=("Arial", 14)).pack()
    tk.Label(root, text=f"Výslovnost: {sound}", font=("Arial", 14)).pack()
    tk.Button(root, text="Další", command=next_learn_step).pack(pady=10)

def next_learn_step():
    global index
    index += 1
    next_learn()

def start_test(lesson):
    global current, index, correct, mode
    mode = "test"
    current = LESSONS[lesson][:]
    random.shuffle(current)
    index = 0
    correct = 0
    clear()
    next_test()

def next_test():
    if index >= len(current):
        finish_test()
        return

    char, name, _ = current[index]
    clear()
    tk.Label(root, text=char, font=("Arial", 48)).pack()
    entry.delete(0, tk.END)
    entry.pack()
    tk.Button(root, text="OK", command=check_answer).pack(pady=5)

def check_answer():
    global xp, unlocked, index, correct
    char, name, _ = current[index]
    if entry.get().strip().lower() == name.lower():
        correct += 1
        xp += 10
        messagebox.showinfo("Správně", "✅ dobře")
    else:
        messagebox.showerror("Špatně", f"❌ správně: {name}")

    index += 1
    next_test()

def finish_test():
    global unlocked
    percent = correct / len(current)
    if percent >= 0.7:
        messagebox.showinfo("Test OK", "Lekce splněna 🎉")
        if unlocked < len(LESSONS):
            unlocked += 1
    else:
        messagebox.showwarning("Fail", "Zkus to znovu 😬")

    save_progress(xp, unlocked)
    show_menu()

def clear():
    for w in root.winfo_children():
        w.pack_forget()
    header.pack(pady=5)

# ======================
# UI ELEMENTS
# ======================

header = tk.Label(root, font=("Arial", 12))
entry = tk.Entry(root, font=("Arial", 14))

show_menu()
root.mainloop()
