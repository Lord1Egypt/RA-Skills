"""
Downloads audio from a YouTube URL for the TextOps transcription skill.

Usage:
  python download_audio.py <youtube_url>

Extracts audio-only (mp3) to the current working directory.
Installs / updates yt-dlp automatically if needed.
Exits 0 on success, 1 on failure.

Output tags (mirrors transcribe.py style):
  [YTDLP] Installing...
  [YTDLP] Ready (version X.Y.Z)
  [AUDIO] Fetching audio...
  [AUDIO] Updating yt-dlp and retrying...
  [FILE] /absolute/path/to/Title.mp3
  ERROR: <message>
"""

import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def log(msg):
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode("utf-8", errors="replace").decode("utf-8"), flush=True)


def _yt_dlp_version():
    """Return yt-dlp version string, or None if not available."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def _install_yt_dlp(upgrade=False):
    """Install or upgrade yt-dlp via pip. Returns True on success."""
    cmd = [sys.executable, "-m", "pip", "install",
           "--break-system-packages", "-q",
           *(["--upgrade"] if upgrade else []),
           "yt-dlp"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def ensure_yt_dlp():
    """Make sure yt-dlp is available. Returns version string or exits."""
    version = _yt_dlp_version()
    if version:
        log(f"[YTDLP] Ready (version {version})")
        return version

    log("[YTDLP] Installing...")
    if not _install_yt_dlp():
        log("ERROR: Could not install yt-dlp via pip. Install it manually: pip install yt-dlp")
        sys.exit(1)

    version = _yt_dlp_version()
    if not version:
        log("ERROR: yt-dlp installed but still not found on PATH. Try restarting your terminal.")
        sys.exit(1)

    log(f"[YTDLP] Ready (version {version})")
    return version


def _parse_destination(output):
    """Extract the output file path from yt-dlp stdout."""
    # yt-dlp prints: [ExtractAudio] Destination: /path/to/file.mp3
    # or on some versions: [download] Destination: /path/to/file.mp3
    for line in output.splitlines():
        m = re.search(r"Destination:\s+(.+)$", line)
        if m:
            return m.group(1).strip()
    return None


def _run_download(url):
    """Run yt-dlp and return (success, output, file_path)."""
    cmd = [
        "yt-dlp",
        "-x",
        "--format", "bestaudio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--no-playlist",
        "-o", "%(title)s.%(ext)s",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    combined = result.stdout + result.stderr

    if result.returncode != 0:
        return False, combined, None

    path = _parse_destination(combined)
    if path and not os.path.isabs(path):
        path = os.path.abspath(path)

    return True, combined, path


def download(url):
    log("[AUDIO] Fetching audio...")
    ok, output, path = _run_download(url)

    if not ok:
        log("[AUDIO] Updating yt-dlp and retrying...")
        _install_yt_dlp(upgrade=True)
        ok, output, path = _run_download(url)

    if not ok:
        # Print last few lines of yt-dlp output to help diagnose
        last_lines = "\n".join(output.strip().splitlines()[-5:])
        log(f"ERROR: Download failed.\n{last_lines}")
        sys.exit(1)

    if not path or not os.path.isfile(path):
        # yt-dlp succeeded but we couldn't parse the path — search cwd for newest mp3
        mp3s = [f for f in os.listdir(".") if f.endswith(".mp3")]
        if mp3s:
            path = os.path.abspath(sorted(mp3s, key=os.path.getmtime)[-1])
        else:
            log("ERROR: Download reported success but output file not found.")
            sys.exit(1)

    log(f"[FILE] {path}")
    return path


def main():
    if len(sys.argv) < 2:
        log("Usage: python download_audio.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    ensure_yt_dlp()
    download(url)


if __name__ == "__main__":
    main()
