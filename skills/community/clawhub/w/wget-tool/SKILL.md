---
name: wget-tool
description: Download files from the web via HTTP/HTTPS/FTP with resume support, recursive mirroring, rate limiting, and progress feedback.
---

# WGet Tool — Web File Downloader

Download files from HTTP/HTTPS/FTP servers with resume support, recursive downloading, bandwidth limiting, and robust error handling. Ideal for batch downloads, website mirroring, and automated data acquisition.

## Quick Start

```bash
# Download a single file
wget-tool https://example.com/file.zip

# Download with a different filename
wget-tool https://example.com/file.zip -O output.zip
```

## Usage

```bash
wget-tool URL [OPTIONS]

Options:
  -O, --output FILE    Save to specific filename
  -c, --continue       Resume partial download
  -q, --quiet          Suppress progress output
  --limit-rate RATE    Limit download speed (e.g., 100k, 1M)
  -r, --recursive      Download recursively
  -l, --level N        Maximum recursion depth
  --timeout SEC        Connection timeout in seconds
  --retries N          Number of retries on failure (default: 3)
  --header HEADER      Add custom HTTP header
  --user-agent UA      Custom User-Agent string
  -P, --directory-prefix DIR   Save files under directory
  --json               Output as JSON with download metadata
```

## Examples

```bash
# Resume an interrupted download
wget-tool https://example.com/large-file.iso -c

# Download with speed limit
wget-tool https://example.com/video.mp4 --limit-rate 500k

# Recursively download a website (depth 2)
wget-tool -r -l 2 https://docs.example.com/

# Custom headers and user-agent
wget-tool https://api.example.com/data.json \
  --header "Authorization: Bearer token123" \
  --user-agent "MyScript/1.0"

# Download with retries and timeout
wget-tool https://unreliable-server.com/file.dat --timeout 10 --retries 5

# Machine-readable output
wget-tool https://example.com/file.zip --json
```

## Features

- **HTTP/HTTPS/FTP** — supports major protocols
- **Resume support** — continue interrupted downloads with -c
- **Recursive mirroring** — download entire site trees
- **Bandwidth limiting** — avoid saturating connections
- **Retry logic** — configurable retries and timeouts
- **Custom headers** — authentication, API tokens, referrers
- **JSON output** — metadata for pipeline integration
- **Progress feedback** — speed, ETA, and percentage
