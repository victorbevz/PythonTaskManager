import tkinter as tk
from tkinter import ttk, messagebox, END
from core import TaskManagerBase
import os

class TaskManagerApp(TaskManagerBase):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Advanced To-Do List (OOP)")
        self.root.geometry("550x400")
        self.root.resizable(False, False)

        # REMOVE these lines:
        # self.root.tk.call("source", os.path.join(os.path.dirname(__file__), "azure.tcl"))
        # self.root.tk.call("set_theme", "dark")

        # Set dark theme for ttk (optional, but safe)
        style = ttk.Style()
        style.theme_use('azure-dark')

        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill='both', expand=True)

        entry_frame = ttk.LabelFrame(main_frame, text="Add New Task", padding="10 10 10 10")
        entry_frame.pack(fill='x', pady=10)

        self.entry = ttk.Entry(entry_frame, width=25)
        self.entry.grid(row=0, column=0, padx=5, pady=5)

        self.due_date_entry = ttk.Entry(entry_frame, width=15)
        self.due_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Due Date (DD-MM-YYYY):").grid(row=1, column=1, sticky='w', padx=5)

        self.priority_label = ttk.Label(entry_frame, text="Priority:")
        self.priority_label.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(entry_frame, textvariable=self.priority_var, values=["Low", "Medium", "High"], width=8, state="readonly")
        self.priority_combo.current(1)
        self.priority_combo.grid(row=0, column=3, padx=5, pady=5)

        entry_frame.columnconfigure(0, weight=2)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.columnconfigure(2, weight=0)
        entry_frame.columnconfigure(3, weight=0)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=5)

        button_texts = [
            ("Add Task", self.add_task),
            ("Remove Task", self.remove_task),
            ("Clear All", self.clear_tasks),
            ("Save Tasks", self.save_tasks_gui),
            ("Load Tasks", self.load_tasks_gui)
        ]

        self.buttons = []
        for i, (text, cmd) in enumerate(button_texts):
            btn = ttk.Button(button_frame, text=text, command=cmd)
            btn.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            self.buttons.append(btn)
            button_frame.columnconfigure(i, weight=1)

        listbox_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="10 10 10 10")
        listbox_frame.pack(fill='both', expand=True, pady=10)

        # --- Replace Listbox with Treeview ---
        self.tree = ttk.Treeview(listbox_frame, columns=("Task", "Due", "Priority"), show="headings", selectmode="browse")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Due", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.column("Task", width=220)
        self.tree.column("Due", width=100)
        self.tree.column("Priority", width=80)
        self.tree.pack(fill='both', expand=True)

        self.load_tasks_gui()

    def add_task(self):
        task = self.entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_var.get()
        if task and due_date:
            self.tree.insert("", "end", values=(task, due_date, priority))
            self.entry.delete(0, END)
            self.due_date_entry.delete(0, END)
        else:
            messagebox.showwarning("Warning", "You must enter a task and due date!")

    def remove_task(self):
        selected = self.tree.selection()
        if selected:
            self.tree.delete(selected[0])

    def clear_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def save_tasks_gui(self):
        tasks = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            tasks.append(f"{values[0]} (Due: {values[1]}, Priority: {values[2]})")
        self.save_tasks(tasks)

    def load_tasks_gui(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_tasks()
        for task in self.tasks:
            # Try to parse the saved string, fallback to putting it in the Task column
            try:
                name, rest = task.split(" (Due: ")
                due, priority = rest[:-1].split(", Priority: ")
                self.tree.insert("", "end", values=(name, due, priority))
            except Exception:
                self.tree.insert("", "end", values=(task, "", ""))