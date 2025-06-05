from tkinter import Tk
from gui import TaskManagerApp
import os

if __name__ == "__main__":
    root = Tk()
    # Load Azure theme (ensure forward slashes for Tcl)
    root.tk.call("source", os.path.join(os.path.dirname(__file__), "azure.tcl").replace("\\", "/"))
    root.tk.call("set_theme", "dark")  # Set dark theme
    app = TaskManagerApp(root)
    root.mainloop()