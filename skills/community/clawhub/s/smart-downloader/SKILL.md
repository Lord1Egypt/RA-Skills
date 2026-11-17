---
name: smart-downloader
version: 1.0.0
description: Smart file downloader with multi-threading, resumable downloads, and progress display
whenToUse: When you need to download multiple files or large files
---

## Overview

Smart file downloader with multi-threaded concurrent downloads, resumable download support, progress display, and file integrity verification.

## Core Features

- **Multi-threaded concurrent downloads**: Use Semaphore to control concurrency, improve download speed
- **Resumable downloads**: Support resuming from breakpoint, avoid repeated downloads
- **Progress display**: Rich progress bar showing download progress, speed, remaining time
- **File integrity verification**: Automatically verify file integrity after download
- **Custom request headers**: Support custom User-Agent, Referer, etc.
- **Error retry**: Automatically retry failed downloads, default max 5 times
- **Proxy support**: Support HTTP/HTTPS/SOCKS5 proxies
- **Temporary file management**: Download to temporary directory, automatically move to target directory after completion

## Usage

Provide a list of download URLs, and the script will automatically download all files.

## Parameters

- `urls`: List of download URLs (required, comma separated or file path)
- `output_dir`: Output directory (required)
- `max_workers`: Max concurrency (optional, default 4)
- `chunk_size`: Chunk size (optional, default 2MB)
- `timeout`: Request timeout (optional, default 10 seconds)
- `retry`: Max retry times (optional, default 5)
- `headers`: Custom request headers (optional, JSON format)
- `proxy`: Proxy address (optional)

## Example

```bash
python scripts/smart_download.py urls.txt output/
python scripts/smart_download.py "https://example.com/file1.jpg,https://example.com/file2.jpg" output/
python scripts/smart_download.py urls.txt output/ --max-workers 8 --timeout 30
python scripts/smart_download.py urls.txt output/ --proxy http://127.0.0.1:7890
```

## URL File Format

Supports two ways to provide URLs:

1. **Command line comma separated**:
   ```
   python scripts/smart_download.py "url1,url2,url3" output/
   ```

2. **File path** (one URL per line):
   ```
   https://example.com/file1.jpg
   https://example.com/file2.jpg
   https://example.com/file3.mp4
   ```

## Output Format

- Files are saved in `output_dir` directory
- Temporary files are saved in `{output_dir}/.temp/` directory
- Temporary directory is automatically cleaned after download

## Progress Display

During download, the following information is displayed:
- File name
- Download progress (percentage)
- Download speed (MB/s)
- Remaining time
- Downloaded/Total size

## Tech Stack

- Python 3.11+
- httpx 0.28.1
- aiofiles 25.1.0
- rich 14.3.3

## Performance Optimization Tips

1. **Concurrency**: Adjust based on network and target server (recommended 4-8)
2. **Chunk size**: For large files (>100MB), consider increasing to 4-8MB
3. **Timeout**: For slow networks, consider increasing to 30-60 seconds
4. **Retry times**: For unstable networks, consider increasing to 10 times

## Error Handling

- Automatically retry failed downloads
- Display detailed error information
- Failed download files are logged
- Support manual cleanup and re-download

## Legal Disclaimer

This skill is for learning and research purposes only.

Users must comply with the following principles when using this skill:
1. Not for any commercial use
2. Comply with target platform's terms of service and robots.txt rules
3. Do not conduct large-scale downloads or cause operational disruption to the platform
4. Reasonably control request frequency to avoid burdening the target platform
5. Do not use for any illegal or improper purposes

By using this skill, you agree to comply with the above principles.
