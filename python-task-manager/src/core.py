class TaskManagerBase:
    def __init__(self, filename="tasks.txt"):
        self._filename = filename
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