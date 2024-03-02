import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
import subprocess
import tkinter.font as tkfont

class CodeEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("SuperPy")
        self.text_widget = tk.Text(self.master, bg='black', fg='white', insertbackground='white', selectbackground='#333', selectforeground='white', undo=True)
        self.text_widget.pack(expand=True, fill='both')
        self.create_menu()
        self.create_toolbar()
        self.libraries = []
        self.work_space = None
        self.current_font = ("Courier", 12)  # Default font

    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Background Color", command=self.change_background_color)
        settings_menu.add_command(label="Libraries", command=self.libraries_setting)
        settings_menu.add_command(label="Work Spaces", command=self.workspaces_setting)

        
        font_options = [
            ("Arial", 10),
            ("Helvetica", 10),
            ("Times", 10),
            ("Courier", 10),
            ("Verdana", 10)
        ]

        font_submenu = tk.Menu(settings_menu, tearoff=0)
        for font_name, font_size in font_options:
            font_submenu.add_command(label=f"{font_name} {font_size}", command=lambda f=(font_name, font_size): self.change_font(f))
        settings_menu.add_cascade(label="Font", menu=font_submenu)

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
                code = file.read()
                self.insert_highlighted_code(code)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_widget.get(1.0, tk.END))
            messagebox.showinfo("Info", "File saved successfully.")
            if self.work_space == "Flask":
                start_flask_server()
            elif self.work_space == "Django":
                start_django_server()

    def run_code(self):
        code = self.text_widget.get(1.0, tk.END)
       

    def change_background_color(self):
        color = colorchooser.askcolor(title="Select Background Color")
        if color:
            self.text_widget.config(bg=color[1])

    def libraries_setting(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Libraries Setting")
        label = tk.Label(settings_window, text="Select a library to install:")
        label.pack()
        listbox = tk.Listbox(settings_window)
        libraries = [
            "numpy", "matplotlib", "pandas", "scipy", "sklearn", "tensorflow", "torch", "requests", "beautifulsoup4", "pygame", "requests", "kivy", "tkinter"
        ]
        for lib in libraries:
            listbox.insert(tk.END, lib)
        listbox.pack()
        save_button = tk.Button(settings_window, text="Save", command=lambda: self.install_selected_library(listbox.get(tk.ACTIVE), settings_window))
        save_button.pack()

    def install_selected_library(self, library, settings_window):
        try:
            import pip
            pip.main(['install', library])
        except Exception as e:
            print(f"An error occurred while installing {library}: {e}")
        settings_window.destroy()

    def workspaces_setting(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Work Spaces Setting")
        label = tk.Label(settings_window, text="Select a workspace:")
        label.pack()
        workspace_var = tk.StringVar()
        flask_radio = tk.Radiobutton(settings_window, text="Flask", variable=workspace_var, value="Flask")
        flask_radio.pack()
        django_radio = tk.Radiobutton(settings_window, text="Django", variable=workspace_var, value="Django")
        django_radio.pack()
        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_workspace(workspace_var.get(), settings_window))
        save_button.pack()

    def save_workspace(self, workspace, settings_window):
        self.work_space = workspace
        settings_window.destroy()

    def insert_highlighted_code(self, code):
        highlighted_code = highlight(code, PythonLexer(), Terminal256Formatter(style='colorful'))
        self.text_widget.insert(tk.END, highlighted_code)

    def change_font(self, font):
        self.current_font = font
        self.text_widget.config(font=font)

def start_django_server():
    try:
        subprocess.Popen(['python', 'manage.py', 'runserver'])
    except Exception as e:
        print(f"An error occurred while starting Django server: {e}")

def start_flask_server():
    try:
        subprocess.Popen(['python', 'app.py'])
    except Exception as e:
        print(f"An error occurred while starting Flask server: {e}")

def main():
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

