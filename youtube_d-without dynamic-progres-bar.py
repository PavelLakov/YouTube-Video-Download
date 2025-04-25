import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("520x380")
        self.root.resizable(False, False)

        self.link_file = None
        self.output_folder = None

        # Paste URL input
        ttk.Label(root, text="Paste a YouTube Link (optional):").pack(pady=(10, 0))
        self.url_entry = ttk.Entry(root, width=60)
        self.url_entry.pack(pady=5)

        # File selection
        self.file_btn = ttk.Button(root, text="Or Select a File with Links (.txt)", command=self.select_file)
        self.file_btn.pack(pady=5)

        # Folder selection
        self.folder_btn = ttk.Button(root, text="Choose Download Folder", command=self.select_folder)
        self.folder_btn.pack(pady=10)

        # Buttons: Download + Exit
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=15)

        self.download_btn = ttk.Button(btn_frame, text="Download", command=self.start_download_thread)
        self.download_btn.grid(row=0, column=0, padx=10)

        self.exit_btn = ttk.Button(btn_frame, text="Exit", command=root.quit)
        self.exit_btn.grid(row=0, column=1, padx=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=450)
        self.progress.pack(pady=20)

        # Status label
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack()

    def select_file(self):
        self.link_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.link_file:
            self.status_label.config(text=f"✅ Selected file: {os.path.basename(self.link_file)}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.status_label.config(text=f"📁 Output folder: {folder}")

    def start_download_thread(self):
        thread = threading.Thread(target=self.download_videos)
        thread.start()

    def download_videos(self):
        try:
            pasted_url = self.url_entry.get().strip()
            urls = []

            if pasted_url:
                urls = [pasted_url]
            elif self.link_file:
                with open(self.link_file, 'r') as file:
                    urls = [line.strip() for line in file if line.strip()]
            else:
                messagebox.showerror("Missing Input", "Please paste a URL or select a file.")
                return

            if not self.output_folder:
                messagebox.showerror("Missing Output Folder", "Please choose a folder to save the videos.")
                return

            total = len(urls)
            self.progress['maximum'] = total
            self.progress['value'] = 0

            def hook(d):
                if d['status'] == 'downloading':
                    percent = float(d.get('downloaded_bytes', 0)) / float(d.get('total_bytes', 1)) * 100
                    self.progress['value'] = percent
                    self.status_label.config(text=f"⬇ Downloading: {percent:.1f}%")
                    self.root.update_idletasks()

                elif d['status'] == 'finished':
                    self.progress['value'] = 100
                    self.status_label.config(text="✅ Finished downloading.")
                    self.root.update_idletasks()

            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
                'progress_hooks': [hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(urls)

            messagebox.showinfo("Download Complete", "✅ All videos downloaded.")
            self.status_label.config(text="✅ Download complete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="❌ Download failed.")

# Start app
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()