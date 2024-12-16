import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # For Progressbar
import shutil
import os
import tempfile

# Global variable to store the selected file path and output video path
selected_file = None
output_video = None

def place_mp4_file():
    global selected_file
    file_path = filedialog.askopenfilename(
        title="Select an MP4 file",
        filetypes=(("MP4 Files", "*.mp4"), ("All Files", "*.*"), ("Mov Files", "*.mov"))
    )
    if file_path:
        file_label.config(text=f"Selected File: {file_path}")
        selected_file = file_path  # Store the file path globally
        add_overlay()  # Add overlay as soon as a file is selected
    else:
        file_label.config(text="No file selected")


def add_overlay():
    global output_video
    try:
        # Create a temporary file for the output video (do not save it in the same folder)
        temp_dir = tempfile.mkdtemp()  # Temporary directory
        output_video = os.path.join(temp_dir, 'EDITED.mp4')

        # FFmpeg command to apply the overlay
        cmd = [
            'ffmpeg',
            '-i', selected_file,
            '-i', 'redCircle.png',
            '-filter_complex',
            '[1:v]scale=100:-1[overlay];[0:v][overlay]overlay=W-w-1000:H-h-10',
            # Resize the overlay image to 100px width and apply it
            '-codec:a', 'copy',  # Keep the audio as is
            output_video  # Save output to the temporary file
        ]

        # Run the FFmpeg command
        subprocess.run(cmd, check=True)
        print(f"Overlay added successfully! Output saved temporarily as {output_video}")

        # Ensure the output video file exists
        if os.path.exists(output_video):
            print(f"Output video file exists: {output_video}")
        else:
            print(f"Error: Output video not found at {output_video}")

        # Enable the "Download" button after processing is done
        download_button.config(state=tk.NORMAL)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        status_label.config(text=f"Error occurred during overlay processing.")


# Function to download (move) the processed video to the Desktop
def download_file():
    global output_video
    if output_video and os.path.exists(output_video):
        # Get the Downloads folder path (Desktop in this case)
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Ensure that the directory exists
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)

        # Get the base file name of the output video
        file_name = os.path.basename(output_video)

        # Create the full destination path on the Desktop
        destination = os.path.join(desktop_path, file_name)

        try:
            # Move the output video to the Desktop
            shutil.move(output_video, destination)
            # Update the status label with the location of the downloaded file
            status_label.config(text=f"File successfully downloaded to: {destination}")
            print(f"File moved to: {destination}")
        except Exception as e:
            status_label.config(text=f"Error: {e}")
            print(f"Error moving file: {e}")
    else:
        status_label.config(text="No processed video to download.")


# Create the main window
root = tk.Tk()
root.title("MP4 File Selector and Downloader")
root.geometry("700x300")

# Add a button to select the MP4 file
select_button = tk.Button(root, text="Place MP4 File", command=place_mp4_file)
select_button.pack(pady=20)

# Label to display the selected file path
file_label = tk.Label(root, text="No file selected", wraplength=300)
file_label.pack(pady=20)

# Add a button to download the processed video (initially disabled)
download_button = tk.Button(root, text="Download", command=download_file, state=tk.DISABLED)
download_button.pack(pady=20)

# Status label to show result or errors
status_label = tk.Label(root, text="")
status_label.pack(pady=20)

# Start the main loop to run the GUI
root.mainloop()
