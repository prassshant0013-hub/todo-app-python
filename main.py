import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"

# -----------------------------
# Data Handling
# -----------------------------
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# -----------------------------
# Functions
# -----------------------------
def add_task():
    text = entry.get().strip()
    priority = priority_var.get()

    if text == "":
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return

    tasks.append({
        "text": text,
        "done": False,
        "priority": priority
    })

    entry.delete(0, tk.END)
    update_list()
    save_tasks()

def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        update_list()
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task first!")

def toggle_task():
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = not tasks[index]["done"]
        update_list()
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task first!")

def filter_tasks(mode):
    update_list(mode)

def update_list(mode="all"):
    listbox.delete(0, tk.END)

    for task in tasks:
        # Handle old data safely
        priority = task.get("priority", "Medium")

        if mode == "done" and not task["done"]:
            continue
        if mode == "pending" and task["done"]:
            continue

        text = f"[{priority}] {task['text']}"
        if task["done"]:
            text = "✔ " + text

        listbox.insert(tk.END, text)

# -----------------------------
# UI Setup
# -----------------------------
root = tk.Tk()
root.title("Pro To-Do App")
root.geometry("450x550")
root.config(bg="#121212")
root.resizable(False, False)

tasks = load_tasks()

# Title
tk.Label(root, text="📝 To-Do Manager",
         font=("Segoe UI", 18, "bold"),
         bg="#121212", fg="white").pack(pady=10)

# Entry
entry = tk.Entry(root,
                 font=("Segoe UI", 14),
                 bg="#1e1e1e",
                 fg="white",
                 insertbackground="white")
entry.pack(padx=10, pady=10, fill="x")

# Priority Dropdown
priority_var = tk.StringVar(value="Medium")
tk.OptionMenu(root, priority_var, "Low", "Medium", "High").pack()

# Button Frame
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add", width=10,
          bg="#28a745", fg="white",
          command=add_task).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Delete", width=10,
          bg="#dc3545", fg="white",
          command=delete_task).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Done", width=10,
          bg="#ffc107", fg="black",
          command=toggle_task).grid(row=0, column=2, padx=5)

# Filter Frame
filter_frame = tk.Frame(root, bg="#121212")
filter_frame.pack(pady=5)

tk.Button(filter_frame, text="All", width=10,
          bg="#444", fg="white",
          command=lambda: filter_tasks("all")).grid(row=0, column=0, padx=5)

tk.Button(filter_frame, text="Done", width=10,
          bg="#444", fg="white",
          command=lambda: filter_tasks("done")).grid(row=0, column=1, padx=5)

tk.Button(filter_frame, text="Pending", width=10,
          bg="#444", fg="white",
          command=lambda: filter_tasks("pending")).grid(row=0, column=2, padx=5)

# Listbox
listbox = tk.Listbox(root,
                     font=("Segoe UI", 13),
                     bg="#1e1e1e",
                     fg="white",
                     selectbackground="#444",
                     height=15)
listbox.pack(padx=10, pady=15, fill="both", expand=True)

# Scrollbar
scroll = tk.Scrollbar(listbox)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)

# Keyboard shortcuts
def key_event(event):
    if event.keysym == "Return":
        add_task()
    elif event.keysym == "Delete":
        delete_task()
    elif event.keysym == "space":
        toggle_task()

root.bind("<Return>", key_event)
root.bind("<Delete>", key_event)
root.bind("<space>", key_event)

update_list()

# Run
root.mainloop()