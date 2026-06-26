#!/usr/bin/env python3
"""
Setup script for Tech Weekly Briefing - Adds all media sources to blogwatcher.
"""

import subprocess
import sys

MEDIA_SOURCES = {
    "techcrunch": "https://techcrunch.com/feed/",
    "the-verge": "https://www.theverge.com/rss/index.xml",
    "wired": "https://www.wired.com/feed/rss",
    "ars-technica": "https://arstechnica.com/feed/",
    "mit-technology-review": "https://www.technologyreview.com/feed/",
    "bloomberg-tech": "https://www.bloomberg.com/feeds/markets/news.rss",
    "wsj-tech": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
    "reuters-tech": "https://www.reutersagency.com/feed/?best-topics=tech",
    "ft-tech": "https://www.ft.com/?format=rss",
    "axios": "https://www.axios.com/feeds/feed.rss"
}

def add_blog(name: str, url: str):
    """Add a blog to blogwatcher."""
    try:
        result = subprocess.run(
            ["blogwatcher", "add", name, url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if "Added" in result.stdout or "already" in result.stderr.lower():
            print(f"✓ {name}")
            return True
        else:
            print(f"✗ {name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {name}: {e}")
        return False

def main():
    print("Setting up Tech Weekly Briefing media sources...")
    print("=" * 50)
    
    success_count = 0
    for name, url in MEDIA_SOURCES.items():
        if add_blog(name, url):
            success_count += 1
    
    print("=" * 50)
    print(f"Setup complete: {success_count}/{len(MEDIA_SOURCES)} sources added")
    
    # List current blogs
    print("\nCurrent blog list:")
    subprocess.run(["blogwatcher", "blogs"])
    
    return 0 if success_count > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
