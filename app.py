import tkinter as tk
from tkinter import messagebox
import time
import os
import platform

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x400")
        self.root.configure(bg="#282c34")  # Dark background

        # Timer Label
        self.timer_label = tk.Label(root, text="Timer", font=("Helvetica", 28, "bold"), bg="#282c34", fg="#61dafb")
        self.timer_label.pack(pady=20)

        # Time Display
        self.time_display = tk.Label(root, text="25:00", font=("Helvetica", 56, "bold"), bg="#282c34", fg="#98c379")
        self.time_display.pack(pady=20)

        # Duration Inputs
        self.work_duration_label = tk.Label(root, text="Work Duration (min):", bg="#282c34", fg="#abb2bf", font=("Helvetica", 12))
        self.work_duration_label.pack()
        self.work_duration_input = tk.Entry(root, width=5, font=("Helvetica", 12), bg="#3e4451", fg="#dcdfe4", insertbackground="#dcdfe4")
        self.work_duration_input.insert(0, "25")
        self.work_duration_input.pack()

        self.break_duration_label = tk.Label(root, text="Break Duration (min):", bg="#282c34", fg="#abb2bf", font=("Helvetica", 12))
        self.break_duration_label.pack()
        self.break_duration_input = tk.Entry(root, width=5, font=("Helvetica", 12), bg="#3e4451", fg="#dcdfe4", insertbackground="#dcdfe4")
        self.break_duration_input.insert(0, "5")
        self.break_duration_input.pack()

        # Buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_timer, bg="#61dafb", fg="#282c34", font=("Helvetica", 14, "bold"), relief="flat")
        self.start_button.pack(side="left", padx=20, pady=20)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, bg="#e06c75", fg="#282c34", font=("Helvetica", 14, "bold"), relief="flat")
        self.reset_button.pack(side="right", padx=20, pady=20)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer, bg="#c678dd", fg="#282c34", font=("Helvetica", 14, "bold"), relief="flat")
        self.pause_button.pack(side="left", padx=20, pady=20)

        self.resume_button = tk.Button(root, text="Resume", command=self.resume_timer, bg="#56b6c2", fg="#282c34", font=("Helvetica", 14, "bold"), relief="flat")
        self.resume_button.pack(side="right", padx=20, pady=20)

        self.timer_running = False
        self.remaining_time = 0

    def start_timer(self):
        try:
            work_duration = int(self.work_duration_input.get())
            self.remaining_time = work_duration * 60
            self.timer_running = True
            self.countdown(self.remaining_time)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for durations.")

    def countdown(self, count):
        if self.timer_running:
            minutes = count // 60
            seconds = count % 60
            self.time_display.config(text=f"{minutes:02}:{seconds:02}")
            if count > 0:
                self.remaining_time = count - 1
                self.root.after(1000, self.countdown, self.remaining_time)
            else:
                self.play_sound()
                messagebox.showinfo("Time's up!", "Take a break or start a new session.")

    def play_sound(self):
        if platform.system() == "Darwin":  # macOS
            os.system("afplay /System/Library/Sounds/Glass.aiff")
        elif platform.system() == "Windows":
            import winsound
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        else:  # Linux
            os.system("aplay /usr/share/sounds/alsa/Front_Center.wav")

    def reset_timer(self):
        self.time_display.config(text="25:00")
        self.timer_running = False
        self.remaining_time = 0

    def pause_timer(self):
        self.timer_running = False

    def resume_timer(self):
        if not self.timer_running and self.remaining_time > 0:
            self.timer_running = True
            self.countdown(self.remaining_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()