import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image, ImageTk
import subprocess
import threading
import time

# Constants - Replace with your own email and password
SENDER_EMAIL = 'sravanikasoju2004@gmail.com'  # Replace with your Gmail address
SENDER_PASSWORD = 'fwld nsgy hgdo cpeb'  # Replace with your Gmail app-specific password
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin'

def send_email_otp(receiver_email, otp):
    """Send OTP to the provided email address."""
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = receiver_email
    message['Subject'] = 'Your OTP Code'

    body = f"Your OTP is {otp}."
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    finally:
        server.quit()

def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def verify_admin_credentials(action):
    entered_email = entry_email.get().strip()
    entered_password = entry_password.get().strip()
    
    if entered_email == ADMIN_EMAIL and entered_password == ADMIN_PASSWORD:
        otp = generate_otp()
        if send_email_otp(entered_email, otp):
            prompt_otp_verification(otp, action)
        else:
            messagebox.showerror("Error", "Failed to send OTP. Please try again.")
    else:
        messagebox.showerror("Error", "Invalid email or password. Please try again.")

def prompt_otp_verification(otp, action):
    otp_window = Toplevel(root)
    otp_window.title("OTP Verification")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.45)
    window_height = int(screen_height * 0.45)
    x_position = int((screen_width - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)
    otp_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    otp_window.configure(bg="#f0f0f0")  # Background color

    label_otp = Label(otp_window, text="Enter the OTP sent to your email:", bg="#f0f0f0", font=("Arial", 12))
    label_otp.pack(pady=(20, 5))

    entry_otp = Entry(otp_window, width=30, font=("Arial", 12))
    entry_otp.pack(pady=5)

    def check_otp():
        entered_otp = entry_otp.get().strip()
        if entered_otp == otp:
            otp_window.destroy()
            if action == "enable":
                open_duration_window()
            elif action == "disable":
                disable_usb_ports()
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")

    btn_verify_otp = Button(otp_window, text="Verify OTP", command=check_otp, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    btn_verify_otp.pack(pady=10)

def open_otp_window(action):
    global otp_window, entry_email, entry_password
    otp_window = Toplevel(root)
    otp_window.title("Admin Verification")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.45)
    window_height = int(screen_height * 0.45)
    x_position = int((screen_width - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)
    otp_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    otp_window.configure(bg="#f0f0f0")  # Background color

    label_email = Label(otp_window, text="Enter your email address:", bg="#f0f0f0", font=("Arial", 12))
    label_email.pack(pady=(20, 5))

    entry_email = Entry(otp_window, width=30, font=("Arial", 12))
    entry_email.pack(pady=5)

    label_password = Label(otp_window, text="Enter your password:", bg="#f0f0f0", font=("Arial", 12))
    label_password.pack(pady=(20, 5))

    entry_password = Entry(otp_window, width=30, font=("Arial", 12), show='*')
    entry_password.pack(pady=5)

    btn_verify = Button(otp_window, text="Send OTP", command=lambda: verify_admin_credentials(action), font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    btn_verify.pack(pady=10)

def open_duration_window():
    duration_window = Toplevel(root)
    duration_window.title("Enter Duration")
    duration_window.geometry("300x200")

    duration_label = Label(duration_window, text="Enter duration in seconds:")
    duration_label.pack()

    duration_entry = Entry(duration_window)
    duration_entry.pack()

    def set_duration():
        duration = duration_entry.get()
        if duration.isdigit():
            subprocess.run([r'unblock_usb.bat'], text=True)
            subprocess.run([r'block_usb_with_timer.bat', duration], text=True)
            duration_window.destroy()
            success_label.config(text="USB Ports Enabled Temporarily")
        else:
            messagebox.showerror("Error", "Please enter a valid number")

    duration_ok_button = Button(duration_window, text="OK", command=set_duration)
    duration_ok_button.pack()

def disable_usb_ports():
    """Disable USB ports."""
    try:
        subprocess.run([r'block_usb.bat'], text=True)
        success_label.config(text="USB Ports Disabled Successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disable USB ports: {e}")

def request_access(action):
    open_otp_window(action)

root = tk.Tk()
root.title("USB Port Security")
root.geometry("600x500")  # Adjust size as needed

# Load the background image
bg_image_path = r"D:\USB Physical Security_Project\bg2.jpg"  # Update with your image path
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((600, 500), Image.LANCZOS)  # Adjust size as needed
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=600, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Add the label
label = Label(root, text="USB Security", font=("Arial", 24), bg="#fff", fg="#000")
label.place(relx=0.5, rely=0.1, anchor="center")

# Add success label
success_label = Label(root, text="", font=("Arial", 14), bg="#fff", fg="#4CAF50")
success_label.place(relx=0.5, rely=0.9, anchor="center")

# Add the buttons
disable_button = Button(root, text="Disable USB Ports", command=lambda: request_access("disable"), font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5)
disable_button.place(relx=0.5, rely=0.4, anchor="center")

enable_button = Button(root, text="Enable USB Ports Temporarily", command=lambda: request_access("enable"), font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5)
enable_button.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
