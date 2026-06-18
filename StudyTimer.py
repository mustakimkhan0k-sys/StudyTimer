# ===============================================================
# StudyTimer — FIXED Launcher (Stable on Python 3.13)
# Self-updating system + schedule editor support
# Launch Timer uses pythonw.exe (no recursive launcher issue)
# ===============================================================

import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import traceback

# ----------------------------------------------------------------
# CONSTANT PATHS
# ----------------------------------------------------------------
APP_FOLDER = os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~'), "StudyTimer")
MAIN_APP_PATH = os.path.join(APP_FOLDER, "main_app.py")
BACKUP_FILE = os.path.join(APP_FOLDER, "main_app.bak")

# ----------------------------------------------------------------
# DEFAULT EMBEDDED main_app.py (FALLBACK)
# ----------------------------------------------------------------
EMBEDDED_DEFAULT = """
print("main_app.py is missing. Please update script using the launcher.")
"""

# ----------------------------------------------------------------
# ENSURE main_app.py EXISTS
# ----------------------------------------------------------------
def ensure_main_script():
    os.makedirs(APP_FOLDER, exist_ok=True)
    if not os.path.exists(MAIN_APP_PATH):
        with open(MAIN_APP_PATH, "w", encoding="utf-8") as f:
            f.write(EMBEDDED_DEFAULT)

# ----------------------------------------------------------------
# READ / WRITE main_app.py
# ----------------------------------------------------------------
def read_main_script():
    if os.path.exists(MAIN_APP_PATH):
        with open(MAIN_APP_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def write_main_script(text):
    if os.path.exists(MAIN_APP_PATH):
        shutil.copy2(MAIN_APP_PATH, BACKUP_FILE)
    with open(MAIN_APP_PATH, "w", encoding="utf-8") as f:
        f.write(text)

# ----------------------------------------------------------------
# FIXED: Launch Timer using pythonw.exe (NO RECURSIVE LAUNCH)
# ----------------------------------------------------------------
def launch_timer():
    script = MAIN_APP_PATH

    # Try pythonw.exe first (no console)
    py_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(py_dir, "pythonw.exe")

    if os.path.exists(pythonw):
        cmd = [pythonw, script]
    else:
        # fallback to python.exe
        cmd = [sys.executable, script]

    try:
        subprocess.Popen(cmd, close_fds=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch timer:\n{e}\n{traceback.format_exc()}")

# ----------------------------------------------------------------
# UPDATE WINDOW
# ----------------------------------------------------------------
def open_update_window(root):
    win = tk.Toplevel(root)
    win.title("Update Script")
    win.geometry("900x600")

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    btns = tk.Frame(frame)
    btns.pack(fill="x")

    editor = scrolledtext.ScrolledText(frame, wrap="none", font=("Consolas", 11))
    editor.pack(fill="both", expand=True, pady=10)

    # Load existing code
    editor.insert("1.0", read_main_script())

    # Buttons
    def load_file():
        f = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if f:
            editor.delete("1.0", "end")
            editor.insert("1.0", open(f, "r", encoding="utf-8").read())

    def save():
        text = editor.get("1.0", "end")
        write_main_script(text)
        messagebox.showinfo("Saved", "Script updated successfully!")

    tk.Button(btns, text="Load File", command=load_file).pack(side="left", padx=5)
    tk.Button(btns, text="Apply Update", command=save).pack(side="left", padx=5)

    tk.Label(btns, text=f"Path: {MAIN_APP_PATH}", fg="#666").pack(side="right")

# ----------------------------------------------------------------
# MAIN UI
# ----------------------------------------------------------------
def launcher_ui():
    ensure_main_script()

    root = tk.Tk()
    root.title("StudyTimer — Launcher")
    root.geometry("430x240")

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="StudyTimer — Launcher",
             font=("Segoe UI", 15, "bold")).pack(anchor="w")

    tk.Label(frame,
             text=f"Script stored at:\n{MAIN_APP_PATH}",
             font=("Segoe UI", 9), fg="#444").pack(anchor="w", pady=(5, 10))

    # Buttons row
    row = tk.Frame(frame)
    row.pack(pady=10)

    tk.Button(row, text="Launch Timer", width=14,
              command=launch_timer).pack(side="left", padx=5)

    tk.Button(row, text="Update Script", width=14,
              command=lambda: open_update_window(root)).pack(side="left", padx=5)

    tk.Button(row, text="Open Script Folder", width=16,
              command=lambda: os.startfile(APP_FOLDER)).pack(side="left", padx=5)

    tk.Label(frame,
             text="Paste updated full script in Update window → Apply Update.",
             font=("Segoe UI", 9), fg="#333").pack(pady=(20, 0))

    root.mainloop()

# ----------------------------------------------------------------
# START
# ----------------------------------------------------------------
if __name__ == "__main__":
    launcher_ui()
