from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pytube import YouTube

def select_path():
    download_path = filedialog.askdirectory()
    path_var.set(download_path)

def download_video():
    try:
        url = YouTube(link.get())
        selected_stream = select_best_stream(url)
        download_path = path_var.get()
        selected_stream.download(download_path)
        status_label.config(text='Download Complete')
    except Exception as e:
        status_label.config(text=f'Error: {str(e)}')

def select_best_stream(yt):
    streams = yt.streams.filter(progressive=True)
    best_stream = None
    best_resolution = -1
    best_filesize = float('inf')

    for stream in streams:
        resolution = get_resolution(stream)
        filesize = get_filesize(stream)

        if resolution > best_resolution or (resolution == best_resolution and filesize < best_filesize):
            best_stream = stream
            best_resolution = resolution
            best_filesize = filesize

    return best_stream

def get_resolution(stream):
    resolution_str = stream.resolution
    if resolution_str:
        return int(resolution_str[:-1])
    else:
        return -1

def get_filesize(stream):
    filesize_str = stream.filesize
    if filesize_str:
        return int(filesize_str)
    else:
        return float('inf')

root = Tk()
root.geometry('600x350')
root.title("YouTube Video Downloader")

# Adding a background image
bg_image = PhotoImage(file="background.png")
bg_label = Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

Label(root, text='YouTube Video Downloader', font='arial 20 bold', bg='white').pack(pady=10)

link_label = Label(root, text='Enter YouTube Link:', font='arial 12', bg='white')
link_label.pack()
link = StringVar()
Entry(root, width=60, textvariable=link).pack()

path_var = StringVar()
path_var.set("Select Download Path")
download_path_entry = Entry(root, width=60, textvariable=path_var, state='readonly')
download_path_entry.pack()

select_path_button = Button(root, text='Select Path', font='arial 12', bg='pale turquoise', command=select_path)
select_path_button.pack(pady=5)

download_button = Button(root, text='Download', font='arial 15 bold', bg='pale green', command=download_video)
download_button.pack(pady=10)

status_label = Label(root, text='', font='arial 12', bg='white')
status_label.pack()

root.mainloop()
