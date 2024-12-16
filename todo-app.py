import tkinter as tk
import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

# Veritabanı ve tablo oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                completed BOOLEAN,
                category TEXT)''')
conn.commit()

# Tkinter penceresi oluşturuluyor
root = tk.Tk()
root.title("Todo List")

# Görev ekleme fonksiyonu
def add_task():
    task = task_entry.get()
    category = category_entry.get()

    if task and category:
        c.execute("INSERT INTO tasks (task, completed, category) VALUES (?, ?, ?)", (task, False, category))
        conn.commit()
        show_tasks()
        task_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)

# Görevleri gösterme fonksiyonu
def show_tasks():
    for widget in tasks_frame.winfo_children():
        widget.destroy()  # Önceki görevleri temizle

    c.execute("SELECT id, task, completed, category FROM tasks")
    tasks = c.fetchall()

    for task in tasks:
        task_id, task_text, completed, category = task

        task_frame = tk.Frame(tasks_frame)
        task_frame.pack(fill="x", pady=5)

        task_label = tk.Label(task_frame, text=f"Task: {task_text}", anchor="w")
        task_label.grid(row=0, column=0, padx=10)

        category_label = tk.Label(task_frame, text=f"Category: {category}", anchor="w")
        category_label.grid(row=0, column=1, padx=10)

        completed_var = tk.BooleanVar(value=completed)  # BooleanVar'ı burada tanımlıyoruz

        # Checkbutton oluşturuluyor ve tamamlanma durumu güncelleniyor
        completed_check = tk.Checkbutton(task_frame, text="Completed", variable=completed_var, command=lambda id=task_id, var=completed_var: toggle_completed(id, var))
        completed_check.grid(row=0, column=2, padx=10)

        delete_button = tk.Button(task_frame, text="Delete", command=lambda id=task_id: delete_task(id))
        delete_button.grid(row=0, column=3, padx=10)

# Tamamlanan durumu değiştirme
def toggle_completed(task_id, var):
    new_completed = var.get()  # Checkbox'ın güncel durumunu alıyoruz
    c.execute("UPDATE tasks SET completed=? WHERE id=?", (new_completed, task_id))
    conn.commit()
    show_tasks()

# Görevi silme
def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    show_tasks()

# Arayüz bileşenleri
task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=5)

category_entry = tk.Entry(root, width=30)
category_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=10)

tasks_frame = tk.Frame(root)
tasks_frame.pack(pady=10)

# Görevleri göster
show_tasks()

root.mainloop()