import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import subprocess
import discord
from discord.ext import commands

class CodeEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Code Editor")
        self.text_widget = tk.Text(self.master, bg='black', fg='white', insertbackground='white', selectbackground='#333', selectforeground='white', undo=True)
        self.text_widget.pack(expand=True, fill='both')
        self.create_menu()
        self.create_toolbar()
        self.libraries = []
        self.work_space = None

    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Add Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Background Color", command=self.change_background_color)
        settings_menu.add_command(label="Libraries", command=self.libraries_setting)
        settings_menu.add_command(label="Work Spaces", command=self.workspaces_setting)  
        settings_menu.add_command(label="Discord", command=self.update_discord_activity)  
        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.master.config(menu=menubar)

    def create_toolbar(self):
        toolbar = tk.Frame(self.master)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        run_button = tk.Button(toolbar, text="Run", command=self.run_code)
        run_button.pack(side=tk.LEFT)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_widget.get(1.0, tk.END))
            messagebox.showinfo("Info", "File saved successfully.")

    def run_code(self):
        code = self.text_widget.get(1.0, tk.END)
        if self.work_space == "Flask":
            self.setup_flask_environment()
        elif self.work_space == "Django":
            self.setup_django_environment()
        for lib in self.libraries:
            code = f"import {lib}\n" + code
        with open("temp.py", "w") as file:
            file.write(code)
        try:
            result = subprocess.run(["python", "temp.py"], capture_output=True, text=True)
            output = result.stdout
            error = result.stderr
            if error:
                messagebox.showerror("Error", error)
            else:
                output_window = tk.Toplevel(self.master)
                output_window.title("Output")
                output_text = tk.Text(output_window, bg='black', fg='white', insertbackground='white', selectbackground='#333', selectforeground='white', wrap='word')
                output_text.pack(expand=True, fill='both')
                output_text.insert(tk.END, output)
                output_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_background_color(self):
        color = colorchooser.askcolor(title="Select Background Color")
        if color:
            self.text_widget.config(bg=color[1])

    def libraries_setting(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Libraries Setting")
        label = tk.Label(settings_window, text="Select libraries to use:")
        label.pack()
        listbox = tk.Listbox(settings_window, selectmode=tk.MULTIPLE, exportselection=0)
        libraries = [
            "numpy", "matplotlib", "pandas", "scipy", "sklearn", "tensorflow", "torch", "requests", "beautifulsoup4", "pygame"
        ]  
        for lib in libraries:
            listbox.insert(tk.END, lib)
        listbox.pack()
        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_libraries(listbox.curselection(), settings_window))
        save_button.pack()

    def workspaces_setting(self):  
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Work Spaces Setting")
        label = tk.Label(settings_window, text="Select workspace:")
        label.pack()
        workspace_var = tk.StringVar()
        flask_radio = tk.Radiobutton(settings_window, text="Flask", variable=workspace_var, value="Flask")
        flask_radio.pack()
        django_radio = tk.Radiobutton(settings_window, text="Django", variable=workspace_var, value="Django")
        django_radio.pack()
        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_workspace(workspace_var.get(), settings_window))
        save_button.pack()

    def save_libraries(self, selections, settings_window):
        self.libraries = [selections[i] for i in selections]
        settings_window.destroy()

    def save_workspace(self, workspace, settings_window):
        self.work_space = workspace
        settings_window.destroy()

    def update_discord_activity(self):
        bot = commands.Bot(command_prefix='!')
        @bot.event
        async def on_ready():
            print('Bot is ready!')
            await bot.change_presence(activity=discord.Game(name="Editing Code"))  
        bot.run('1202723131198935150')

def main():
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
