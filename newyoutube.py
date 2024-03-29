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
root.attributes('-fullscreen', False)  # Open in fullscreen mode
root.title("YouTube Video Downloader")

bg_image = PhotoImage(file="background.png")
bg_label = Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

Label(root, text='YouTube Video Downloader', font='arial 30 bold', bg='white').pack(pady=40)

link_label = Label(root, text='Enter YouTube Link:', font='arial 20', bg='white')
link_label.pack()
link = StringVar()
Entry(root, width=80, font='arial 18', textvariable=link).pack(pady=20)

quality_label = Label(root, text='Select Quality:', font='arial 20', bg='white')
quality_label.pack(pady=10)
qualities = ['1080p', '720p', '480p', '360p']
quality_var = StringVar()
quality_dropdown = ttk.Combobox(root, font='arial 18', textvariable=quality_var, values=qualities)
quality_dropdown.pack(pady=20)

format_label = Label(root, text='Select Format:', font='arial 20', bg='white')
format_label.pack(pady=10)
formats = ['Video']
format_var = StringVar()
format_dropdown = ttk.Combobox(root, font='arial 18', textvariable=format_var, values=formats)
format_dropdown.pack(pady=10)

path_var = StringVar()
path_var.set("Select Download Path")
download_path_entry = Entry(root, width=80, font='arial 18', textvariable=path_var, state='readonly')
download_path_entry.pack(pady=10)

select_path_button = Button(root, text='Select Path', font='arial 20', bg='pale turquoise', command=select_path)
select_path_button.pack(pady=10)

download_button = Button(root, text='Download', font='arial 30 bold', bg='pale green', command=download_video)
download_button.pack(pady=10)

exit_button = Button(root, text='exit', font='arial 30 bold', bg='pale green', command=root.destroy)
exit_button.place(x=900,y=620)

status_label = Label(root, text='', font='arial 20', bg='white')
status_label.pack(pady=10)

root.mainloop()
