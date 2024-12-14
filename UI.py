import tkinter as tk
from tkinter import filedialog
import shutil
import os

# Global variable to store the selected file path
selected_file = None


# Function to open file dialog and select an MP4 file
def place_mp4_file():
    global selected_file
    file_path = filedialog.askopenfilename(
        title="Select an MP4 file",
        filetypes=(("MP4 Files", "*.mp4"), ("All Files", "*.*"))
    )
    if file_path:
        file_label.config(text=f"Selected File: {file_path}")
        selected_file = file_path  # Store the file path globally
    else:
        file_label.config(text="No file selected")


# Function to download (copy) the selected file to the Downloads folder
def download_file():
    global selected_file
    if selected_file:
        # Get the Downloads folder path (cross-platform)
        download_location = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Ensure that the directory exists
        if not os.path.exists(download_location):
            os.makedirs(download_location)

        # Get the base file name
        file_name = os.path.basename(selected_file)
        # Create the full download path
        destination = os.path.join(download_location, file_name)

        try:
            # Copy the file to the Downloads folder
            shutil.copy(selected_file, destination)
            status_label.config(text=f"File downloaded to: {destination}")
        except Exception as e:
            status_label.config(text=f"Error: {e}")
    else:
        status_label.config(text="No file selected to download.")


# Create the main window
root = tk.Tk()
root.title("MP4 File Selector and Downloader")
root.geometry("400x300")

# Add a button to place MP4 file
select_button = tk.Button(root, text="Place MP4 File", command=place_mp4_file)
select_button.pack(pady=20)

# Label to display the selected file path
file_label = tk.Label(root, text="No file selected", wraplength=300)
file_label.pack(pady=20)

# Add a button to download the selected file
download_button = tk.Button(root, text="Download", command=download_file)
download_button.pack(pady=20)

# Status label to show download result
status_label = tk.Label(root, text="", wraplength=300)
status_label.pack(pady=20)

# Start the main loop to run the GUI
root.mainloop()
