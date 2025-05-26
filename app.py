import customtkinter as ctk
import platform
import os

ctk.set_appearance_mode("light")  # "dark" also available
ctk.set_default_color_theme("green")


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("600x700")  # Enlarged window
        self.root.configure(bg="#C4DCDF")

        self.font_family = "Poppins"
        self.timer_running = False
        self.remaining_time = 0

        # Title
        self.timer_label = ctk.CTkLabel(root, text="Pomodoro Timer",
                                        font=(self.font_family, 32, "bold"),
                                        text_color="#C14364")
        self.timer_label.pack(pady=30)

        # Timer Display
        self.time_display = ctk.CTkLabel(root, text="25:00",
                                         font=(self.font_family, 72, "bold"),
                                         text_color="#2CA18C")
        self.time_display.pack(pady=20)

        # Duration Inputs
        self._add_duration_inputs()

        # Common button style
        btn_opts = {
            "width": 260,
            "height": 50,
            "corner_radius": 25,
            "font": (self.font_family, 16, "bold"),
            "fg_color": "#FF916B",
            "text_color": "white",
            "hover_color": "#C14364"
        }

        # Buttons (well-spaced, not in a cluster)
        self.start_button = ctk.CTkButton(root, text="Start", command=self.start_timer, **btn_opts)
        self.start_button.pack(pady=12)

        self.pause_button = ctk.CTkButton(root, text="Pause", command=self.pause_timer, **btn_opts)
        self.pause_button.pack(pady=12)

        self.resume_button = ctk.CTkButton(root, text="Resume", command=self.resume_timer, **btn_opts)
        self.resume_button.pack(pady=12)

        self.reset_button = ctk.CTkButton(root, text="Reset", command=self.reset_timer, **btn_opts)
        self.reset_button.pack(pady=12)

    def _add_duration_inputs(self):
        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(pady=30)

        label_opts = {
            "font": (self.font_family, 16),
            "text_color": "#1F5869"
        }
        entry_opts = {
            "width": 80,
            "height": 40,
            "font": (self.font_family, 16),
            "fg_color": "#EEE2D1",
            "text_color": "#444444",
            "corner_radius": 10,
            "justify": "center"
        }

        # Work Duration
        work_label = ctk.CTkLabel(frame, text="Work Duration (min):", **label_opts)
        work_label.grid(row=0, column=0, padx=10, pady=10)

        self.work_duration_input = ctk.CTkEntry(frame, **entry_opts)
        self.work_duration_input.insert(0, "25")
        self.work_duration_input.grid(row=0, column=1, padx=10, pady=10)

        # Break Duration
        break_label = ctk.CTkLabel(frame, text="Break Duration (min):", **label_opts)
        break_label.grid(row=1, column=0, padx=10, pady=10)

        self.break_duration_input = ctk.CTkEntry(frame, **entry_opts)
        self.break_duration_input.insert(0, "5")
        self.break_duration_input.grid(row=1, column=1, padx=10, pady=10)

    def start_timer(self):
        try:
            work_duration = int(self.work_duration_input.get())
            self.remaining_time = work_duration * 60
            self.timer_running = True
            self.countdown(self.remaining_time)
        except ValueError:
            ctk.CTkMessageBox(title="Invalid Input", message="Please enter valid numbers.")

    def countdown(self, count):
        if self.timer_running:
            minutes = count // 60
            seconds = count % 60
            self.time_display.configure(text=f"{minutes:02}:{seconds:02}")
            if count > 0:
                self.remaining_time = count - 1
                self.root.after(1000, self.countdown, self.remaining_time)
            else:
                self.play_sound()
                ctk.CTkMessageBox(title="Time's Up", message="Break time or start a new session!")

    def play_sound(self):
        if platform.system() == "Darwin":
            os.system("afplay /System/Library/Sounds/Glass.aiff")
        elif platform.system() == "Windows":
            import winsound
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        else:
            os.system("aplay /usr/share/sounds/alsa/Front_Center.wav")

    def reset_timer(self):
        self.time_display.configure(text="25:00")
        self.timer_running = False
        self.remaining_time = 0

    def pause_timer(self):
        self.timer_running = False

    def resume_timer(self):
        if not self.timer_running and self.remaining_time > 0:
            self.timer_running = True
            self.countdown(self.remaining_time)


if __name__ == "__main__":
    root = ctk.CTk()
    app = PomodoroApp(root)
    root.mainloop()
