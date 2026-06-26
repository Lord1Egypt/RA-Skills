import re
import os
import subprocess
import sys

def extract_url(text):
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

def download_video(url):
    try:
        output_dir = os.path.join(os.getcwd(), "videos")
        os.makedirs(output_dir, exist_ok=True)
        
        command = [
            sys.executable, "-m", "yt_dlp",
            "--format", "best",
            "--output", os.path.join(output_dir, "%(title)s.%(ext)s"),
            url
        ]
        
        subprocess.run(command, check=True)
        return f"Video downloaded successfully to {output_dir}"
    except Exception as e:
        return f"Error downloading video: {str(e)}"

def main(text):
    url = extract_url(text)
    if not url:
        return "No video URL found in the input"
    return download_video(url)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
        print(main(input_text))
