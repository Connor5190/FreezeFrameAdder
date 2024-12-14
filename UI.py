import tkinter as tk
from tkinter import filedialog
import shutil
import subprocess
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


def add_overlay(output_video):
    try:
        # FFmpeg command to overlay the PNG on the video
        cmd = [
            'ffmpeg',
            '-i', selected_file,  # Input video file
            '-i', redCircle.png,  # Overlay PNG file
            '-filter_complex', 'overlay=W-w-10:H-h-10',  # Position overlay at the bottom-right corner
            '-codec:a', 'copy',  # Keep the audio track as is
            output_video  # Output video file
        ]

        # Run the command using subprocess
        subprocess.run(cmd, check=True)
        print(f"Overlay added successfully! Output saved as {output_video}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

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
        status_label.config(text="No file selected to down