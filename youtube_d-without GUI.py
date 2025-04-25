import yt_dlp

def download_video(url):
    try:
        ydl_opts = {
            'format': 'best',  # or 'bestvideo+bestaudio'
            'outtmpl': '%(title)s.%(ext)s',  # Save with video title
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Download completed.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    link = input("Enter a YouTube link to download: ")
    download_video(link)