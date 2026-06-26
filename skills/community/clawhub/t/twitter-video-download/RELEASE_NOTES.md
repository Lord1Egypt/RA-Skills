# Twitter Video Download Skill - Release Notes

---

## Latest Version: 1.0.2 (2026-03-14)

### Security Improvements
- ✅ Changed `shell: true` to `shell: false` - prevents shell injection attacks
- ✅ Added URL validation - only accepts twitter.com/x.com URLs
- ✅ Added filename sanitization - prevents path traversal
- ✅ Added proxy URL format validation
- ✅ Improved error handling and messages

---

## Version 1.0.1 (2026-03-13)

- Initial release with basic functionality

---

## Version 1.0.0 (2026-03-11)

- Initial creation

---

## Basic Information

**Skill Name:** Twitter Video Download
**Slug:** twitter-video-download
**Category:** Utility > Media Download
**Tags:** twitter, x, video, download, media, social-media
**License:** MIT

---

## Description

**One-line Description:**
One-click download Twitter/X videos and GIFs to local storage

**Detailed Introduction:**
A simple and easy-to-use OpenClaw Skill, implemented based on yt-dlp. Supports downloading videos and GIFs from Twitter/X posts, automatically saved as MP4 format. Simply send a video link, and the AI assistant can help you complete the download.

---

## Features

- ✅ Supports twitter.com and x.com links
- ✅ Supports video and GIF downloads (GIF converted to MP4)
- ✅ High-quality video download
- ✅ Custom save path and filename
- ✅ Supports proxy configuration
- ✅ Security: No shell injection, URL validation, filename sanitization
- ✅ Automatic cleanup of temporary files

---

## Environment Requirements

**Required:**
- Python 3.8+
- yt-dlp (`pip install yt-dlp`)

**Optional:**
- Proxy (for accessing Twitter/X from China)

---

## Usage

**Method 1: Tell the AI**
> "Download this video: https://x.com/username/status/123456789"

**Method 2: Command Line**
```bash
node download.mjs "https://x.com/user/status/123456789" --output "D:\Videos"
```

---

## Security

This skill has been improved for security:

1. **No Shell Execution**: Uses `shell: false` in Node.js spawn to prevent command injection
2. **URL Validation**: Only accepts valid Twitter/X URLs
3. **Filename Sanitization**: Prevents path traversal attacks
4. **Proxy Validation**: Validates proxy URL format

---

## Configuration

```bash
# Set proxy (if needed)
setx PROXY_URL "http://your-proxy:port"
```

---

## Author

- Author: Lemonpek66 / Jack
- GitHub: https://github.com/Lemonpek66/twitter-video-download

---

*This skill is safe to use. Please download from ClawHub or GitHub.*
