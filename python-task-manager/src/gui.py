import tkinter as tk
from tkinter import Tk, messagebox, StringVar, END
from tkinter import ttk
from core import TaskManagerBase

class TaskManagerApp(TaskManagerBase):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Advanced To-Do List (OOP)")
        self.root.geometry("500x400")  # Increased width
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')  # Try 'clam', 'alt', 'default', or 'vista'

        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill='both', expand=True)

        entry_frame = ttk.LabelFrame(main_frame, text="Add New Task", padding="10 10 10 10")
        entry_frame.pack(fill='x', pady=10)

        self.entry = ttk.Entry(entry_frame, width=30)
        self.entry.grid(row=0, column=0, padx=5, pady=5)
        self.due_date_entry = ttk.Entry(entry_frame, width=15)
        self.due_date_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(entry_frame, text="Due Date (DD-MM-YYYY):").grid(row=1, column=1, sticky='w', padx=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Task", command=self.add_task, width=12)
        self.add_button.pack(side='left', padx=3)
        self.remove_button = ttk.Button(button_frame, text="Remove Task", command=self.remove_task, width=12)
        self.remove_button.pack(side='left', padx=3)
        self.clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_tasks, width=12)
        self.clear_button.pack(side='left', padx=3)
        self.save_button = ttk.Button(button_frame, text="Save Tasks", command=self.save_tasks_gui, width=12)
        self.save_button.pack(side='left', padx=3)
        self.load_button = ttk.Button(button_frame, text="Load Tasks", command=self.load_tasks_gui, width=12)
        self.load_button.pack(side='left', padx=3)

        listbox_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="10 10 10 10")
        listbox_frame.pack(fill='both', expand=True, pady=10)

        self.listbox = tk.Listbox(listbox_frame, width=50, height=10, font=('Segoe UI', 10))
        self.listbox.pack(fill='both', expand=True)

        self.load_tasks_gui()

    def add_task(self):
        task = self.entry.get()
        due_date = self.due_date_entry.get()
        if task and due_date:
            task_with_due_date = f"{task} (Due: {due_date})"
            self.listbox.insert(END, task_with_due_date)
            self.entry.delete(0, END)
            self.due_date_entry.delete(0, END)
        else:
            messagebox.showwarning("Warning", "You must enter a task and due date!")

    def remove_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_task_index)
        except IndexError:
            pass

    def clear_tasks(self):
        self.listbox.delete(0, END)

    def save_tasks_gui(self):
        tasks = self.listbox.get(0, END)
        self.save_tasks(tasks)

    def load_tasks_gui(self):
        self.listbox.delete(0, END)
        self.load_tasks()
        for task in self.tasks:
            self.listbox.insert(END, task)