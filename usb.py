import tkinter as tk
from tkinter import messagebox
import subprocess

password = "password" 

def button1_clicked():
    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x200")

    password_label = tk.Label(password_window, text="Enter Password:")
    password_label.pack()

    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()

    def ok_button():
        if password_entry.get() == password:
            subprocess.run([r'block_usb.bat'], text=True)
            password_window.destroy()
            success_label.config(text="USB Ports Disabled Successfully")
        else:
            error_label.config(text="Incorrect password. Please try again.")
            password_entry.delete(0, tk.END)

    ok_button = tk.Button(password_window, text="OK", command=ok_button)
    ok_button.pack()

    error_label = tk.Label(password_window, text="", font=("Arial", 12), bg="#f2f2f2", fg="#ff0000")
    error_label.pack()


def button2_clicked():
    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x200")

    password_label = tk.Label(password_window, text="Enter Password:")
    password_label.pack()

    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()

    def ok_button():
        if password_entry.get() == password:
            # time duration
            duration_window = tk.Toplevel(root)
            duration_window.title("Enter Duration")
            duration_window.geometry("300x200")

            duration_label = tk.Label(duration_window, text="Enter duration in seconds:")
            duration_label.pack()

            duration_entry = tk.Entry(duration_window)
            duration_entry.pack()

            def set_duration():
                duration = duration_entry.get()
                if duration.isdigit():
                    subprocess.run([r'unblock_usb.bat'], text=True)
                    subprocess.run([r'block_usb_with_timer.bat', duration], text=True)
                    password_window.destroy()
                    duration_window.destroy()
                    success_label.config(text="USB Ports Enabled Temporarily")
                else:
                    messagebox.showerror("Error", "Please enter a valid number")

            duration_ok_button = tk.Button(duration_window, text="OK", command=set_duration)
            duration_ok_button.pack()

        else:
            error_label.config(text="Incorrect password. Please try again.")
            password_entry.delete(0, tk.END)

    ok_button = tk.Button(password_window, text="OK", command=ok_button)
    ok_button.pack()

    error_label = tk.Label(password_window, text="", font=("Arial", 12), bg="#f2f2f2", fg="#ff0000")
    error_label.pack()

root = tk.Tk()
root.title("USB Port Security")
root.geometry("400x300")

disable_button = tk.Button(root, text="Disable USB Ports", command=button1_clicked)
disable_button.pack(pady=20)

enable_button = tk.Button(root, text="Enable USB Ports Temporarily", command=button2_clicked)
enable_button.pack(pady=20)

success_label = tk.Label(root, text="", font=("Arial", 12), bg="#f2f2f2", fg="#00ff00")
success_label.pack()

root.mainloop()
