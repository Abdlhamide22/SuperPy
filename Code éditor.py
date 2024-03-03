import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
import subprocess

class CodeEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("SuperPy")
        self.text_widget = tk.Text(self.master, bg='black', fg='white', insertbackground='white', selectbackground='#333', selectforeground='white', undo=True)
        self.text_widget.pack(expand=True, fill='both')
        self.output_frame = tk.Frame(self.master, bg='black')
        self.output_frame.pack(expand=True, fill='both')
        self.output_text = tk.Text(self.output_frame, bg='black', fg='white', insertbackground='white', selectbackground='#333', selectforeground='white')
        self.output_text.pack(expand=True, fill='both')
        self.create_menu()
        self.create_sidebar()
        self.libraries = []
        self.work_space = None

    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Run", command=self.run_code)  # Add Run command here
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Add Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Background Color", command=self.change_background_color)
        settings_menu.add_command(label="Libraries", command=self.libraries_setting)
        settings_menu.add_command(label="Work Spaces", command=self.workspaces_setting)  
        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.master.config(menu=menubar)

    def create_sidebar(self):
        sidebar = tk.Frame(self.master, bg='gray')
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        open_file_button = tk.Button(sidebar, text="Open File", command=self.open_file)
        open_file_button.pack(fill=tk.X)

        create_file_button = tk.Button(sidebar, text="Create File", command=self.create_file)
        create_file_button.pack(fill=tk.X)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_widget.delete(1.0, tk.END)
                code = file.read()
                self.insert_highlighted_code(code)

    def create_file(self):
        self.text_widget.delete(1.0, tk.END)

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
        try:
            # Execute code
            output = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, timeout=5)
            output = output.decode('utf-8')
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            error_output = e.output.decode('utf-8')
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, error_output)
        except subprocess.TimeoutExpired:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Execution timed out.")

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
            "numpy", "matplotlib", "pandas", "scipy", "sklearn", "tensorflow", "torch", "requests", "beautifulsoup4", "pygame", "flask", "django", "requests", "kivy", "tkinter"
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


