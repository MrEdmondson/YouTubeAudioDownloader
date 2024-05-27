from pytube import YouTube
from pytube import Playlist
import os
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import re

def SanitizeFilename(filename):
    # Remove special characters (except alphanumeric, hyphen, and underscore)
    sanitized = re.sub(r'[^\w-]', '', filename)
    return sanitized

def IsValidYoutubePlaylist(url):
    regex = r'^(?:https?://)?(?:www\.)?(?:youtube\.com/playlist\?list=|youtu\.be/)([a-zA-Z0-9_-]+)'
    return re.match(regex, url) is not None

# Locate named file in folder location
def FindFiles(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def DownloadPlaylist(link, path):    
    # Playlist object
    pl = Playlist(link)

    # Intial value for variable to count item # being downloaded
    n = 1
    # Initial value for counting items not downloaded
    skipped = 0

    # Get all video urls in playlist
    for url in pl.video_urls:
        # Get video stream info from url
        yt = YouTube(url)
        # Locate file by name
        result = FindFiles(yt.title + ".mp4", path)
        # If file found continue
        if result:
            # Update progress
            percentage = round(n*100/pl.length)
            pb['value'] = percentage
            percentage_label.config(text=f"{percentage}%")
            root.update()

            # Track progress and items skipped
            n += 1
            skipped += 1
            # Let user know an item has already been downloaded
            items_skipped_label.config(text=f"{skipped}/{pl.length} Items Already Downloaded")
            continue
        else:
            # Collect audio only
            yd = yt.streams.get_audio_only()
            # Download the audio file and name it as the video title
            yd.download(path, filename = SanitizeFilename(yt.title) + ".mp4")

            # Update progress
            percentage = round(n*100/pl.length)
            pb['value'] = percentage
            percentage_label.config(text=f"{percentage}%")
            root.update()

            # Track progress
            n += 1

# Download YouTube platlist when Download button is clicked
def DownloadClicked():
    # Clear labels
    finished_label.config(text = "")
    items_skipped_label.config(text = "")
    invalid_playlist_label.config(text= "")

    # Checks if playlist is valid before continuing
    if not IsValidYoutubePlaylist(e.get()):
        invalid_playlist_label.config(text = "Invalid Playlist")
        return    

    # Let's user choose the download folder location
    path = filedialog.askdirectory(title = "Select a Folder")
    # Do nothing if cancel is selected
    if not path:
        return

    DownloadPlaylist(e.get(), path)
    
    # Tell user that the download is finished
    finished_label.config(text = "Download Finished")

# UI name and size
root = Tk()
root.title("YouTube Playlist Downloader")
root.geometry("600x200")

# Labels that get cleared
invalid_playlist_label = Label(root, text="")
invalid_playlist_label.grid(row=0, column=2, padx=5)
finished_label = Label(root, pady=5, text = "")
finished_label.grid(row=3, column=1)
items_skipped_label = Label(root, text = "")
items_skipped_label.grid(row=4, column=1)

# User link input widget
e = Entry(root, width = 72, borderwidth = 5)
e.grid(row=0, column=1)
e.insert(0, "YouTube Playlist Link")

# Progress bar widget
pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=430)
pb.grid(row=2, column=1, columnspan=2, padx=5, sticky = W)

# Progress percentage widget
percentage_label = Label(root, text="0%")
percentage_label.grid(row=2, column=0, padx=10, pady=5, sticky=E)

# Download button widget
download_button = Button(root, text = "Download", command = DownloadClicked, bg = "#74B72E", padx = 24, pady = 16)
download_button.grid(row=1, column=1, pady=10)

# Run application
root.mainloop()

# Addition stuff to use below
"""
# Get video and not just audio
yt = YouTube(link_here)
yd = yt.streams.get_highest_quality()
"""