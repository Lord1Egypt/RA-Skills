#!/usr/bin/env python3
"""Social Video Downloader.

Downloads videos from Instagram, TikTok, YouTube Shorts, and other platforms via yt-dlp.
Validates URLs to prevent command injection and SSRF before downloading.

Usage:
    python3 download.py <url> [output_dir]

Requirements:
    pip install yt-dlp
"""

import ipaddress
import json
import os
import subprocess
import sys
import time
from urllib.parse import urlparse

# Allowed domains for download
ALLOWED_DOMAINS = {
    "instagram.com", "www.instagram.com",
    "tiktok.com", "www.tiktok.com", "vm.tiktok.com",
    "youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com",
    "twitter.com", "www.twitter.com", "x.com", "www.x.com",
    "reddit.com", "www.reddit.com", "v.redd.it",
    "facebook.com", "www.facebook.com", "fb.watch",
    "vimeo.com", "www.vimeo.com",
    "dailymotion.com", "www.dailymotion.com",
    "twitch.tv", "www.twitch.tv", "clips.twitch.tv",
    "bilibili.com", "www.bilibili.com",
}

BLOCKED_IP_RANGES = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def validate_url(url):
    """Validate URL to prevent command injection and SSRF."""
    # Check for shell metacharacters
    dangerous_chars = ["$", "`", "(", ")", ";", "|", "&", "\n", "\r", "\\"]
    for char in dangerous_chars:
        if char in url:
            return False, f"URL contains forbidden character: {char}"

    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Invalid URL format"

    # Must be http or https
    if parsed.scheme not in ("http", "https"):
        return False, f"Only http/https allowed, got: {parsed.scheme}"

    # Must have a hostname
    hostname = parsed.hostname
    if not hostname:
        return False, "URL has no hostname"

    # Check domain allowlist
    domain_allowed = False
    for allowed in ALLOWED_DOMAINS:
        if hostname == allowed or hostname.endswith("." + allowed):
            domain_allowed = True
            break
    if not domain_allowed:
        return False, f"Domain not in allowlist: {hostname}"

    # Resolve and check for private IPs (SSRF protection)
    import socket
    try:
        addr_infos = socket.getaddrinfo(hostname, None)
        for info in addr_infos:
            ip_str = info[4][0]
            ip = ipaddress.ip_address(ip_str)
            for blocked in BLOCKED_IP_RANGES:
                if ip in blocked:
                    return False, f"Hostname resolves to blocked IP: {ip_str}"
    except socket.gaierror:
        return False, f"Cannot resolve hostname: {hostname}"

    return True, None


def download(url, output_dir="/tmp"):
    """Download video using yt-dlp."""
    timestamp = int(time.time())
    output_file = os.path.join(output_dir, f"social_dl_{timestamp}.mp4")

    # Use -- to prevent option injection, pass URL as separate argument
    cmd = [
        "yt-dlp",
        "-o", output_file,
        "--no-playlist",
        "--merge-output-format", "mp4",
        "--retries", "2",
        "--socket-timeout", "30",
        "--no-warnings",
        "--", url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        return None, f"Download failed: {result.stderr.strip()}"

    if not os.path.exists(output_file):
        return None, "Download failed: file not created"

    return output_file, None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp"

    # Validate URL before doing anything
    valid, error = validate_url(url)
    if not valid:
        print(f"ERROR: {error}")
        sys.exit(1)

    # Check metadata first
    print(f"Checking metadata for: {url}")
    meta_cmd = ["yt-dlp", "--no-playlist", "--print", "title", "--no-warnings", "--", url]
    meta_result = subprocess.run(meta_cmd, capture_output=True, text=True, timeout=30)

    if meta_result.returncode != 0 or not meta_result.stdout.strip():
        print(f"ERROR: Could not fetch video metadata. URL may be invalid or blocked.")
        sys.exit(1)

    print(f"Title: {meta_result.stdout.strip()}")
    print(f"Downloading...")

    output_file, error = download(url, output_dir)

    if error:
        print(f"ERROR: {error}")
        sys.exit(1)

    print(f"SUCCESS:{output_file}")


if __name__ == "__main__":
    main()
