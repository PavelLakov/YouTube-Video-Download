import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os
import subprocess
import platform

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("520x400")
        self.root.resizable(False, False)

        self.link_file = None
        self.output_folder = None

        # URL entry
        ttk.Label(root, text="Paste a YouTube Link (optional):").pack(pady=(10, 0))
        self.url_entry = ttk.Entry(root, width=60)
        self.url_entry.pack(pady=5)

        # File input
        self.file_btn = ttk.Button(root, text="Or Select a File with Links (.txt)", command=self.select_file)
        self.file_btn.pack(pady=5)

        # Folder selection
        self.folder_btn = ttk.Button(root, text="Choose Download Folder", command=self.select_folder)
        self.folder_btn.pack(pady=(10, 5))

        # Button row
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        self.download_btn = ttk.Button(btn_frame, text="Download", command=self.start_download_thread)
        self.download_btn.grid(row=0, column=0, padx=10)

        self.open_folder_btn = ttk.Button(btn_frame, text="Open Folder", command=self.open_folder)
        self.open_folder_btn.grid(row=0, column=1, padx=10)

        self.exit_btn = ttk.Button(btn_frame, text="Exit", command=root.quit)
        self.exit_btn.grid(row=0, column=2, padx=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=450)
        self.progress.pack(pady=(10, 5))

        # Status
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack()

    def select_file(self):
        self.link_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.link_file:
            self.status_label.config(text=f"✅ File selected: {os.path.basename(self.link_file)}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.status_label.config(text=f"📁 Folder selected: {folder}")

    def open_folder(self):
        if self.output_folder and os.path.isdir(self.output_folder):
            system = platform.system()
            try:
                if system == "Windows":
                    os.startfile(self.output_folder)
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", self.output_folder])
                else:  # Linux and others
                    subprocess.run(["xdg-open", self.output_folder])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder: {e}")
        else:
            messagebox.showwarning("No Folder", "Please choose a download folder first.")

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
                messagebox.showerror("Missing Input", "Paste a link or select a file.")
                return

            if not self.output_folder:
                messagebox.showerror("Missing Output Folder", "Please choose a download folder.")
                return

            def hook(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
                    downloaded = d.get('downloaded_bytes', 0)
                    percent = downloaded / total * 100
                    self.progress['value'] = percent
                    self.status_label.config(text=f"⬇ Downloading: {percent:.1f}%")
                    self.root.update_idletasks()
                elif d['status'] == 'finished':
                    self.progress['value'] = 100
                    self.status_label.config(text="✅ Download finished")
                    self.root.update_idletasks()

            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
                'progress_hooks': [hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for url in urls:
                    self.progress['value'] = 0
                    self.status_label.config(text="Starting download...")
                    ydl.download([url])

            messagebox.showinfo("Download Complete", "✅ All videos downloaded.")
            self.status_label.config(text="✅ All downloads complete.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="❌ Download failed.")

# Start app
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()