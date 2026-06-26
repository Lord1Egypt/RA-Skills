---
name: twitter-video-download
description: Download videos from Twitter/X posts. Just give it a tweet URL and it will download the video to your specified location.
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["python","pip"],"packages":["yt-dlp"],"env":["PROXY_URL"]}}}
---

# Twitter Video Download

Download videos from Twitter/X posts using yt-dlp.

## Setup

```bash
# Install yt-dlp
pip install yt-dlp

# Configure proxy (required for China users)
# Twitter/X is overseas, proxy is needed to access
# Please replace with your proxy address
setx PROXY_URL "http://your-proxy-address:port"
```

## Usage in OpenClaw

Just tell me:
> "Download this Twitter video: https://x.com/xxx/status/xxx"

Or specify a save location:
> "Download video to D:\Videos: https://x.com/xxx/status/xxx"

I will automatically call this skill to execute the download.

## Command Line Usage

```bash
# Enter skill directory
cd [skill_directory]\scripts

# Set proxy environment variable (replace with your proxy)
set PROXY_URL=http://your-proxy-address:port

# Download video
node download.mjs "https://twitter.com/username/status/123456789"

# Specify output directory
node download.mjs "https://twitter.com/username/status/123456789" --output "D:\Downloads"

# Specify filename
node download.mjs "https://twitter.com/username/status/123456789" --filename "my_video"
```

## Options

- `-o, --output <path>`: Output directory (default: current directory)
- `-f, --filename <name>`: Custom filename (without extension)
- `-q, --quality <quality>`: Video quality (best/bestvideo/worst)

## Examples

```
node download.mjs "https://x.com/username/status/123456789" --output "D:\Downloads"
```

## Security Notes

- **No shell execution**: Uses spawn with `shell: false` for security
- **URL validation**: Only accepts twitter.com and x.com URLs
- **Filename sanitization**: Prevents path traversal attacks
- **Proxy validation**: Validates proxy URL format before use
- **yt-dlp**: Uses the well-known, trusted yt-dlp library

## Notes

- Supports twitter.com and x.com links
- Supports GIF download (converted to MP4)
- Proxy is required for China users, otherwise SSL connection error will occur
- Videos are saved in MP4 format

---

💖 If this skill is useful for you, please give it a star on ClawHub to show your support! It helps others discover this skill too.
