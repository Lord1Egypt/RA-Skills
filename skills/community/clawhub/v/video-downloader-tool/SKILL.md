---
name: video-downloader
description: Universal video downloader supporting multiple platforms (Douyin, Bilibili, YouTube, TikTok, etc.). Can download videos by URL or search by keyword (Douyin supported). Use when users need to download videos from video platforms.
---

# Universal Video Downloader

A versatile video downloading tool that supports multiple video platforms with intelligent platform detection and multiple download methods.

## Supported Platforms

- **Douyin** (抖音) - Chinese TikTok
- **Bilibili** (B站) - Chinese video platform
- **YouTube** - Global video platform
- **TikTok** - International short video
- **Xigua** (西瓜视频) - Chinese video platform
- **Kuaishou** (快手) - Chinese short video
- **Generic** - Any other video site (using browser mode)

## Features

- **Automatic Platform Detection** - Identifies platform from URL
- **Smart Download Method** - Uses yt-dlp for most sites, DrissionPage for anti-crawl sites
- **Search & Download** - Search Douyin by keyword and download results
- **Batch Download** - Download multiple videos at once
- **Metadata Extraction** - Saves title, author, platform info

## Prerequisites

```bash
# Required dependencies
pip install yt-dlp requests DrissionPage

# For DrissionPage browser automation
# Chrome browser will be auto-downloaded on first use
```

## Usage

### Download Single Video

```bash
# Douyin
python scripts/video_downloader.py "https://www.douyin.com/video/xxx"

# Bilibili
python scripts/video_downloader.py "https://www.bilibili.com/video/xxx"

# YouTube
python scripts/video_downloader.py "https://www.youtube.com/watch?v=xxx"

# Any other platform
python scripts/video_downloader.py "https://example.com/video"
```

### Batch Download

```bash
python scripts/video_downloader.py \
  -u "https://www.douyin.com/video/xxx" \
  -u "https://www.bilibili.com/video/yyy" \
  -u "https://www.youtube.com/watch?v=zzz"
```

### Search and Download (Douyin)

```bash
# Search "美女" and download 5 videos
python scripts/video_downloader.py 美女 --search --count 5

# Search with custom count
python scripts/video_downloader.py 美女 --search --count 10
```

### Force Browser Mode

For sites with strong anti-crawl protection:

```bash
python scripts/video_downloader.py "https://example.com/video" --browser
```

### Specify Output Directory

```bash
python scripts/video_downloader.py "URL" --output "D:\\MyVideos"
```

## Parameters

- `url_or_keyword` - Video URL or search keyword
- `--url, -u` - Video URL(s), can be used multiple times
- `--search, -s` - Enable search mode (for Douyin)
- `--platform, -p` - Platform for search (default: douyin)
- `--count, -n` - Number of videos to download (default: 5)
- `--output, -o` - Output directory (default: D:\video_downloads)
- `--browser, -b` - Force use browser mode for downloading

## Output Structure

```
video_downloads/
├── single_20240312_121029/
│   ├── 001_video_title.mp4
│   └── 001_video_title.json
├── batch_20240312_121102/
│   ├── 001_video1.mp4
│   ├── 001_video1.json
│   ├── 002_video2.mp4
│   ├── 002_video2.json
│   └── _summary.json
└── douyin_keyword_20240312_121205/
    ├── 001_video1.mp4
    ├── 001_video1.json
    ├── 002_video2.mp4
    ├── 002_video2.json
    └── _summary.json
```

### Metadata Format

```json
{
  "index": 1,
  "title": "Video Title",
  "author": "Uploader Name",
  "platform": "douyin",
  "url": "https://www.douyin.com/video/xxx",
  "video_filename": "001_video_title.mp4",
  "file_size_mb": 16.84,
  "download_time": "2024-03-12T12:20:30"
}
```

## How It Works

### Platform Detection

The tool automatically detects the platform from the URL:
- `douyin.com` → Douyin
- `bilibili.com` / `b23.tv` → Bilibili
- `youtube.com` / `youtu.be` → YouTube
- `tiktok.com` → TikTok
- etc.

### Download Methods

1. **yt-dlp** (default for most platforms)
   - Fast and reliable
   - Supports 1000+ sites
   - Best for YouTube, Bilibili, etc.

2. **DrissionPage** (for anti-crawl sites)
   - Real browser automation
   - Bypasses most anti-crawl protections
   - Used automatically for Douyin
   - Can be forced with `--browser` flag

### Search Functionality

For Douyin search:
1. Opens browser and navigates to search page
2. Extracts video links from search results
3. Downloads each video using browser session

## Troubleshooting

### "yt-dlp not installed"

```bash
pip install yt-dlp
```

### "DrissionPage not installed"

```bash
pip install DrissionPage
```

### Download fails for specific site

Try forcing browser mode:
```bash
python video_downloader.py "URL" --browser
```

### Chrome not found (DrissionPage)

DrissionPage will auto-download Chrome on first use. If it fails:
1. Install Chrome manually
2. Or set Chrome path in DrissionPage config

### Connection errors

Some sites may block automated access. Try:
- Using a VPN
- Waiting a few minutes between requests
- Using `--browser` mode

## Notes

- **Respect Copyright** - Only download videos you have permission to use
- **Rate Limiting** - The tool includes delays to avoid overwhelming servers
- **Cookie Support** - DrissionPage mode uses browser cookies for authenticated access
- **File Naming** - Special characters in titles are sanitized for filesystem compatibility

## Dependencies

- Python 3.8+
- yt-dlp
- DrissionPage
- requests
- BeautifulSoup4 (optional, for parsing)

## License

This tool is for educational and personal use only. Respect the terms of service of video platforms.
