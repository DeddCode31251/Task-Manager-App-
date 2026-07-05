import json
import os
from tkinter import *
from tkinter import ttk, messagebox

# ---------------- File Handling ----------------
filename = "tasks.json"
Tasks = {}

def load_tasks():
    global Tasks
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                Tasks = json.load(f)
            except json.JSONDecodeError:
                Tasks = {}
    else:
        Tasks = {}

def save_tasks():
    with open(filename, "w") as f:
        json.dump(Tasks, f, indent=4)
    messagebox.showinfo("Saved", "Tasks saved successfully!")

# ---------------- Task Operations ----------------
def add_task():
    name = task_name.get().strip().lower()
    desc = task_desc.get().strip()
    if not name or not desc:
        messagebox.showerror("Error", "Task name and description cannot be empty!")
        return
    Tasks[name] = {
        "Content": desc,
        "Done": done_var.get(),
        "In_Progress": progress_var.get()
    }
    update_listbox()
    clear_inputs()

def remove_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No task selected.")
        return
    task_name_selected = task_listbox.get(selected[0]).split(" | ")[0]
    Tasks.pop(task_name_selected, None)
    update_listbox()
    detail_text.set("")

def update_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No task selected.")
        return
    task_name_selected = task_listbox.get(selected[0]).split(" | ")[0]
    if task_name_selected in Tasks:
        Tasks[task_name_selected]["Content"] = task_desc.get().strip()
        Tasks[task_name_selected]["Done"] = done_var.get()
        Tasks[task_name_selected]["In_Progress"] = progress_var.get()
        update_listbox()
        clear_inputs()

def update_listbox():
    task_listbox.delete(0, END)
    for name, details in Tasks.items():
        task_listbox.insert(
            END,
            f"{name} | Desc: {details['Content']} | Done: {details['Done']} | In Progress: {details['In_Progress']}"
        )

def show_details(event):
    selected = task_listbox.curselection()
    if not selected:
        return
    task_name_selected = task_listbox.get(selected[0]).split(" | ")[0]
    details = Tasks.get(task_name_selected, {})
    if details:
        detail_text.set(
            f"Task: {task_name_selected}\n"
            f"Description: {details['Content']}\n"
            f"Done: {details['Done']}\n"
            f"In Progress: {details['In_Progress']}"
        )

def clear_inputs():
    task_name.set("")
    task_desc.set("")
    done_var.set(False)
    progress_var.set(False)

# ---------------- Tkinter UI ----------------
root = Tk()
root.title("Task Tracker")

# Input Frame
input_frame = ttk.LabelFrame(root, text="Task Details", padding=10)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

task_name = StringVar()
task_desc = StringVar()
done_var = BooleanVar()
progress_var = BooleanVar()

ttk.Label(input_frame, text="Task Name:").grid(row=0, column=0, sticky="w")
ttk.Entry(input_frame, textvariable=task_name, width=30).grid(row=0, column=1)

ttk.Label(input_frame, text="Description:").grid(row=1, column=0, sticky="w")
ttk.Entry(input_frame, textvariable=task_desc, width=30).grid(row=1, column=1)

ttk.Checkbutton(input_frame, text="Done", variable=done_var).grid(row=2, column=0, sticky="w")
ttk.Checkbutton(input_frame, text="In Progress", variable=progress_var).grid(row=2, column=1, sticky="w")

# Buttons
btn_frame = ttk.Frame(root, padding=10)
btn_frame.grid(row=1, column=0, sticky="ew")

ttk.Button(btn_frame, text="Add Task", command=add_task).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Update Task", command=update_task).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Remove Task", command=remove_task).grid(row=0, column=2, padx=5)
ttk.Button(btn_frame, text="Save Tasks", command=save_tasks).grid(row=0, column=3, padx=5)

# Task List
list_frame = ttk.LabelFrame(root, text="Tasks", padding=10)
list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

task_listbox = Listbox(list_frame, width=80, height=10)
task_listbox.pack(side=LEFT, fill=BOTH)
scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=task_listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
task_listbox.config(yscrollcommand=scrollbar.set)

# Bind selection event
task_listbox.bind("<<ListboxSelect>>", show_details)

# Details Panel
detail_frame = ttk.LabelFrame(root, text="Selected Task Details", padding=10)
detail_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

detail_text = StringVar()
ttk.Label(detail_frame, textvariable=detail_text, justify=LEFT).pack(anchor="w")

# Load tasks initially
load_tasks()
update_listbox()

root.mainloop()
