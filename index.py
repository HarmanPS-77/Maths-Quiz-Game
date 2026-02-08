import tkinter as tk
import random
import time

OPERATORS = ["+", "-", "*", "/"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 7

class MathQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("450x400")
        self.root.configure(bg="#f8f9fa")  # Base background
        self.username = ""
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Enter your name:", font=("Times New Roman", 14, "bold"),
                              bg="#f8f9fa", fg="#2C3E50")
        self.label.pack(pady=10)

        self.entry_name = tk.Entry(self.root, font=("Times New Roman", 12, "bold"),
                                   bg="#EAF2F8", fg="#1B2631", insertbackground="#1B2631")
        self.entry_name.pack(pady=5)
        self.entry_name.bind("<Return>", self.start_game)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game,
                                      font=("Times New Roman", 12, "bold"), bg="#566573", fg="#FDFEFE")
        self.start_button.pack(pady=10)

    def start_game(self, event=None):
        name = self.entry_name.get().strip()
        if not name:
            return
        self.username = name
        self.clear_screen()
        self.current = 0
        self.wrong = 0
        self.start_time = time.time()
        self.timer_running = True

        self.greet_label = tk.Label(self.root, text=f"Hello {self.username}! Let's begin.",
                                    font=("Times New Roman", 14, "bold"), fg="#1A5276", bg="#f8f9fa")
        self.greet_label.pack(pady=5)

        self.question_count_label = tk.Label(self.root, text="", font=("Times New Roman", 12, "bold"),
                                             bg="#f8f9fa", fg="#154360")
        self.question_count_label.pack()

        self.difficulty_label = tk.Label(self.root, text="", font=("Times New Roman", 12, "bold"),
                                         bg="#f8f9fa", fg="#7D3C98")
        self.difficulty_label.pack()

        self.problem_label = tk.Label(self.root, text="", font=("Times New Roman", 16, "bold"),
                                      bg="#f8f9fa", fg="#4A235A")
        self.problem_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Times New Roman", 14, "bold"),
                              bg="#FCF3CF", fg="#1C2833", insertbackground="#1C2833")
        self.entry.pack()
        self.entry.bind("<Return>", self.check_answer)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answer,
                                       font=("Times New Roman", 12, "bold"), bg="#2E4053", fg="#FBFCFC")
        self.submit_button.pack(pady=10)

        self.feedback_label = tk.Label(self.root, text="", font=("Times New Roman", 12, "bold"),
                                       bg="#f8f9fa", fg="#922B21")
        self.feedback_label.pack()

        self.status_label = tk.Label(self.root, text="", font=("Times New Roman", 12, "bold"),
                                     bg="#f8f9fa", fg="#1B2631")
        self.status_label.pack()

        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Times New Roman", 12, "bold"),
                                    bg="#f8f9fa", fg="#1F618D")
        self.timer_label.pack()

        # Minimalistic matching buttons
        btn_bg = "#404040"     # Soft dark gray
        btn_fg = "#ffffff"     # Bright text

        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again,
                                           font=("Times New Roman", 12, "bold"), bg=btn_bg, fg=btn_fg,
                                           state=tk.DISABLED)
        self.play_again_button.pack(side=tk.LEFT, padx=30, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy,
                                     font=("Times New Roman", 12, "bold"), bg=btn_bg, fg=btn_fg,
                                     state=tk.DISABLED)
        self.exit_button.pack(side=tk.RIGHT, padx=30, pady=10)

        self.next_problem()
        self.update_timer()

    def next_problem(self):
        if self.current >= TOTAL_PROBLEMS:
            self.end_game()
            return
        self.current += 1
        self.question_count_label.config(text=f"Question {self.current} of {TOTAL_PROBLEMS}")

        if self.current >= 6:
            expr, answer, level = self.generate_higher_problem()
        elif self.current >= 3:
            expr, answer, level = self.generate_medium_problem()
        else:
            expr, answer, level = self.generate_problem()

        self.current_expr = expr
        self.current_answer = answer
        self.current_difficulty = level

        self.difficulty_label.config(text=f"Difficulty: {level}")
        self.problem_label.config(text=f"Problem #{self.current}: {expr}")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def generate_problem(self):
        while True:
            a = random.randint(MIN_OPERAND, MAX_OPERAND)
            b = random.randint(MIN_OPERAND, MAX_OPERAND)
            op = random.choice(OPERATORS)
            if op == "/" and (b == 0 or a % b != 0):
                continue
            expr = f"{a} {op} {b}"
            try:
                answer = int(eval(expr))
                return expr, answer, "Easy"
            except:
                continue

    def generate_medium_problem(self):
        while True:
            a = random.randint(MIN_OPERAND, MAX_OPERAND)
            b = random.randint(MIN_OPERAND, MAX_OPERAND)
            c = random.randint(1, 6)
            op1 = random.choice(["+", "-"])
            op2 = random.choice(["*", "/"])
            expr = f"{a} {op1} {b} {op2} {c}"
            try:
                answer = eval(expr)
                if "/" in expr and not float(answer).is_integer():
                    continue
                return expr, int(answer), "Medium"
            except:
                continue

    def generate_higher_problem(self):
        while True:
            a = random.randint(MIN_OPERAND, MAX_OPERAND)
            b = random.randint(MIN_OPERAND, MAX_OPERAND)
            c = random.randint(MIN_OPERAND, MAX_OPERAND)
            op1 = random.choice(OPERATORS)
            op2 = random.choice(OPERATORS)
            expr = f"{a} {op1} {b} {op2} {c}"
            try:
                answer = eval(expr)
                if "/" in expr and not float(answer).is_integer():
                    continue
                return expr, int(answer), "Hard"
            except:
                continue

    def check_answer(self, event=None):
        guess = self.entry.get().strip()
        if not guess:
            return
        try:
            if int(guess) == self.current_answer:
                self.feedback_label.config(text="✅ Nice!", fg="green")
                self.root.after(800, self.next_problem)
            else:
                self.wrong += 1
                if self.current_difficulty == "Hard":
                    self.status_label.config(text="Too tough! Game over.", fg="#C0392B")
                    self.end_game(force=True)
                elif self.current_difficulty == "Medium":
                    self.feedback_label.config(text="⚠️ Incorrect. Think carefully!", fg="#E67E22")
                else:
                    self.feedback_label.config(text="❌ Oops! Try again.", fg="red")
        except:
            self.feedback_label.config(text="❗ Invalid input.", fg="orange")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def end_game(self, force=False):
        self.timer_running = False
        self.submit_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)
        total_time = round(time.time() - self.start_time)
        self.feedback_label.config(text="")

        if force:
            self.status_label.config(
                text=f"Game Over, {self.username}! Wrong answer on a hard question.\nTime: {total_time}s")
        else:
            self.status_label.config(
                text=f"Well done, {self.username}! You've completed {TOTAL_PROBLEMS} questions.\nTime: {total_time}s\nWrong Attempts: {self.wrong}")

        self.timer_label.config(text=f"Time: {total_time}s")
        self.play_again_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)
        self.root.after(4000, self.show_farewell_screen)

    def show_farewell_screen(self):
        self.clear_screen()
        farewell = tk.Label(self.root, text=f"🎉 Great job, {self.username}!",
                            font=("Times New Roman", 16, "bold"), fg="#4a0072", bg="#f8f9fa")
        farewell.pack(pady=20)

        message = tk.Label(self.root, text="Thanks for playing the Math Quiz!\nKeep learning and stay sharp! 🔢",
                           font=("Times New Roman", 14, "bold"), fg="#333", bg="#f8f9fa")
        message.pack(pady=10)

        exit_button = tk.Button(self.root, text="Exit", font=("Times New Roman", 12, "bold"),
                                command=self.root.destroy, bg="#404040", fg="#ffffff")
        exit_button.pack(pady=10)

    def play_again(self):
        self.clear_screen()
        self.create_widgets()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizGUI(root)
    root.mainloop()


