# Setup — Social Video Downloader

## Requirements

Install yt-dlp and ffmpeg:

```bash
# Debian/Ubuntu/Kali
sudo apt install ffmpeg
pip install --break-system-packages yt-dlp

# macOS
brew install yt-dlp ffmpeg
```

## Verify Installation

```bash
yt-dlp --version
ffmpeg -version
```

Both commands should return version numbers.

## Notes

- No API keys or login required
- Only public posts can be downloaded
- Private/restricted content will fail
- ffmpeg is optional but recommended for best format support
