import tkinter
import subprocess
import openai

api_key = 'YOUR_API_KEY'


class CLIWindow(tkinter.Tk):
    def __init__(self):
        self.previnp = ""
        self.prevres = ""
        super().__init__()
        self.title("Custom CLI")

        text_font = ("Consolas", 11)  # Consolas is a monospaced font similar to VS Code

        self.dark_bg = "#292D3E"
        self.light_bg = "white"
        self.light_fg = "black"
        self.current_mode = "light"  # Set the initial mode to 'light'
        self.configure(bg=self.light_bg)  # Set the initial background to light mode

        title_bg = self.dark_bg if self.current_mode == "dark" else self.light_bg
        if self.current_mode == "dark":
            title_fg = "#61AFEF"  # Blue color for dark mode
        else:
            title_fg = "#0F9D58"  # Green color for light mode

        title_label = tkinter.Label(
            self,
            text="Custom CLI",
            font=("Arial", 25, "bold"),
            fg=title_fg,
            bg=title_bg,
            anchor="w",
        )
        title_label.pack(padx=20, pady=10, side="top", fill="x")

        self.text_box = tkinter.Text(
            self,
            font=text_font,
            wrap="word",
            bg=self.light_bg,
            fg="black",
            insertbackground="black",
        )  # Set initial text box to light mode
        self.text_box.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.text_box.focus_set()

        self.buttons_frame = tkinter.Frame(self, bg=self.light_bg)
        self.buttons_frame.pack(side="bottom", fill="x")

        self.toggle_text = "Light" if self.current_mode == "dark" else "Dark"
        self.toggle_button = tkinter.Button(
            self.buttons_frame,
            text=self.toggle_text,
            command=self.toggle_mode,
            font=("Arial", 10, "bold"),
            width=10,
            bg="#61AFEF",
            fg="white",
        )
        self.toggle_button.pack(side="left", padx=(10, 0))
        self.toggle_button.config(
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
            font=("Arial", 10),
        )

        self.run_button = tkinter.Button(
            self.buttons_frame,
            text="Run",
            command=self.run_command,
            font=("Arial", 10, "bold"),
            width=10,
            bg="#61AFEF",
            fg="white",
        )
        self.run_button.pack(side="right", padx=(0, 20))

        # self.bind('<Return>', lambda event: self.run_command())  # Bind Enter key to run_command function

    def toggle_mode(self):
        if self.current_mode == "dark":
            self.current_mode = "light"
            self.configure(bg=self.light_bg)

            title_bg = self.light_bg
            title_fg = "#0F9D58"  # Green color for light mode

            self.text_box.configure(
                bg=self.light_bg, fg="black", insertbackground="black"
            )
            self.buttons_frame.configure(bg=self.light_bg)
            self.run_button.config(bg="#61AFEF", fg="white")
        else:
            self.current_mode = "dark"
            self.configure(bg=self.dark_bg)

            title_bg = self.dark_bg
            title_fg = "#61AFEF"  # Blue color for dark mode

            self.text_box.configure(
                bg=self.dark_bg, fg="white", insertbackground="white"
            )
            self.buttons_frame.configure(bg=self.dark_bg)
            self.run_button.config(bg="#61AFEF", fg="white")

        self.update_title(title_bg, title_fg)
        self.toggle_text = "Light" if self.current_mode == "dark" else "Dark"
        self.toggle_button.config(text=self.toggle_text)

    def run_command(self,event=None):
        commands = self.text_box.get("1.0", "end-1c").split("\n")
        command = commands[-1]
        if True:
            if command.strip():
                response = openai.Completion.create(
                engine="text-davinci-003",  # Use the GPT-3.5 engine
                prompt=f"Previous input:\n {self.previnp} \n Previous output:\n {self.prevres} \n Now considering all the previous data,Write a command to execute in windows command prompt to '{command}'\nCommand:",
                max_tokens=30,  # Adjust the maximum number of tokens as needed
                api_key=api_key
                )
                promt=f"Previous input:\n {self.previnp} \n Previous output:\n {self.prevres} \n Now considering all the previous data,Write a command to execute in windows command prompt to '{command}'\nCommand:"
# Extract the generated command from the response
                print(promt)
                generated_command = response.choices[0].text.strip()
                print(generated_command)
                if generated_command in ["cls", "clear"]:
    # Delete the content of the Text widget (clear it)
                    self.text_box.delete("1.0", "end")
                    return

                if generated_command == 'wttr.in':
                    generated_command == 'curl wttr.in'
                process = subprocess.Popen(
                    generated_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                output, error = process.communicate()

                
                self.previnp=command
                self.prevres=generated_command

                if output:
                    self.text_box.insert("end", f"\nOutput:\n{output}\n")
                if error:
                    self.text_box.insert("end", f"\nError:\n{error}\n")

    def update_title(self, bg, fg):
        title_label = self.winfo_children()[
            0
        ]  # Assuming the title is the first child widget
        title_label.configure(fg=fg, bg=bg)

if __name__ == "__main__":
    window = CLIWindow()
    window.geometry("800x600")
    window.text_box.bind("<KeyPress-Return>", window.run_command)
    window.mainloop()
