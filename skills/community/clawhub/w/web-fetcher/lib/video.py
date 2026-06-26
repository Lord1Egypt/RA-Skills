"""Video download module using yt-dlp."""
import os
import re
import subprocess

from lib.router import check_dependency


def fetch_video(url, output_dir, quality="1080", audio_only=False, cookies_browser=None):
    """Download video using yt-dlp. Returns path to downloaded file."""
    if not check_dependency("yt-dlp"):
        return None

    os.makedirs(output_dir, exist_ok=True)

    cmd = ["yt-dlp"]

    if audio_only:
        cmd += ["-x", "--audio-format", "mp3"]
    else:
        cmd += [
            "-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
            "--merge-output-format", "mp4",
        ]

    cmd += ["-o", os.path.join(output_dir, "%(title)s.%(ext)s")]

    if cookies_browser:
        cmd += ["--cookies-from-browser", cookies_browser]

    cmd.append(url)

    print(f"[*] Downloading: {url}")
    print(f"[*] Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[!] yt-dlp error:\n{result.stderr}")
        return None

    # Parse output to find downloaded file path
    output = result.stdout + result.stderr
    match = re.search(r'\[Merger\] Merging formats into "(.+?)"', output)
    if not match:
        match = re.search(r'\[download\] Destination: (.+)', output)
    if not match:
        match = re.search(r'\[download\] (.+?) has already been downloaded', output)
    if not match:
        # ExtractAudio post-processor
        match = re.search(r'\[ExtractAudio\] Destination: (.+)', output)

    filepath = match.group(1) if match else None
    if filepath:
        print(f"[+] Downloaded: {filepath}")
    else:
        print(f"[+] Download completed (check {output_dir})")

    return filepath
