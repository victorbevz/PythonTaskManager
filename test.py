import tkinter as tk
from tkinter import messagebox
import datetime

class TaskManagerBase:
    def __init__(self, filename="tasks.txt"):
        self._filename = filename  # encapsulated attribute
        self._tasks = []

    def load_tasks(self):
        try:
            with open(self._filename, "r") as file:
                self._tasks = [task.strip() for task in file.readlines()]
        except FileNotFoundError:
            self._tasks = []

    def save_tasks(self, tasks):
        with open(self._filename, "w") as file:
            for task in tasks:
                file.write(task + "\n")

    @property
    def tasks(self):
        return self._tasks

class TaskManagerApp(TaskManagerBase):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Advanced To-Do List (OOP)")

        self.entry = tk.Entry(root, width=30)
        self.due_date_label = tk.Label(root, text="Due Date (DD-MM-YYYY):")
        self.due_date_entry = tk.Entry(root, width=15)
        self.entry.pack(pady=10)
        self.due_date_label.pack()
        self.due_date_entry.pack()

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.remove_button = tk.Button(root, text="Remove Task", command=self.remove_task)
        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_tasks)
        self.save_button = tk.Button(root, text="Save Tasks", command=self.save_tasks_gui)
        self.load_button = tk.Button(root, text="Load Tasks", command=self.load_tasks_gui)

        self.add_button.pack()
        self.remove_button.pack()
        self.clear_button.pack()
        self.save_button.pack()
        self.load_button.pack()

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        self.load_tasks_gui()

    def add_task(self):
        task = self.entry.get()
        due_date = self.due_date_entry.get()
        if task and due_date:
            task_with_due_date = f"{task} (Due: {due_date})"
            self.listbox.insert(tk.END, task_with_due_date)
            self.entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task and due date!")

    def remove_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_task_index)
        except IndexError:
            pass

    def clear_tasks(self):
        self.listbox.delete(0, tk.END)

    def save_tasks_gui(self):
        tasks = self.listbox.get(0, tk.END)
        self.save_tasks(tasks)

    def load_tasks_gui(self):
        self.listbox.delete(0, tk.END)
        self.load_tasks()
        for task in self.tasks:
            self.listbox.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()