#!/usr/bin/env python3
"""
Auto Publisher - Image Fetching Script
Fetches relevant images from Unsplash, Pexels, or Pixabay for articles.
Downloads images to local temp directory for WordPress upload.
"""

import argparse
import json
import os
import re
import sys
import logging
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import quote

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "image_fetcher.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("image-fetcher")

IMAGE_DIR = Path(__file__).parent.parent / "data" / "images"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


class UnsplashFetcher:
    """Fetch images from Unsplash API."""

    BASE_URL = "https://api.unsplash.com"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str, count: int = 1) -> list:
        """Search for images on Unsplash."""
        url = f"{self.BASE_URL}/search/photos?query={quote(query)}&per_page={count}&orientation=landscape"
        headers = {
            "Authorization": f"Client-ID {self.api_key}",
            "Accept": "application/json",
        }
        req = Request(url, headers=headers)

        try:
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read())
                results = []
                for photo in data.get("results", []):
                    results.append({
                        "url": photo["urls"]["regular"],
                        "download_url": photo["urls"]["regular"],
                        "alt": photo.get("alt_description", query),
                        "credit": f"Photo by {photo['user']['name']} on Unsplash",
                        "source": "unsplash",
                    })
                return results
        except Exception as e:
            logger.error(f"Unsplash search failed: {e}")
            return []


class PexelsFetcher:
    """Fetch images from Pexels API."""

    BASE_URL = "https://api.pexels.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str, count: int = 1) -> list:
        """Search for images on Pexels."""
        url = f"{self.BASE_URL}/search?query={quote(query)}&per_page={count}&orientation=landscape"
        headers = {
            "Authorization": self.api_key,
            "Accept": "application/json",
        }
        req = Request(url, headers=headers)

        try:
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read())
                results = []
                for photo in data.get("photos", []):
                    results.append({
                        "url": photo["src"]["large"],
                        "download_url": photo["src"]["large"],
                        "alt": photo.get("alt", query),
                        "credit": f"Photo by {photo['photographer']} on Pexels",
                        "source": "pexels",
                    })
                return results
        except Exception as e:
            logger.error(f"Pexels search failed: {e}")
            return []


class PixabayFetcher:
    """Fetch images from Pixabay API."""

    BASE_URL = "https://pixabay.com/api"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str, count: int = 1) -> list:
        """Search for images on Pixabay."""
        url = f"{self.BASE_URL}/?key={self.api_key}&q={quote(query)}&per_page={count}&image_type=photo&orientation=horizontal"

        try:
            with urlopen(url, timeout=15) as response:
                data = json.loads(response.read())
                results = []
                for photo in data.get("hits", []):
                    results.append({
                        "url": photo["largeImageURL"],
                        "download_url": photo["largeImageURL"],
                        "alt": photo.get("tags", query),
                        "credit": f"Image from Pixabay by {photo.get('user', 'unknown')}",
                        "source": "pixabay",
                    })
                return results
        except Exception as e:
            logger.error(f"Pixabay search failed: {e}")
            return []


def download_image(url: str, filename: str = None) -> str:
    """Download image to local directory, return local path."""
    if not filename:
        # Generate filename from URL
        ext = ".jpg"
        if ".png" in url.lower():
            ext = ".png"
        elif ".webp" in url.lower():
            ext = ".webp"
        filename = f"img_{hash(url) % 100000:05d}{ext}"

    local_path = IMAGE_DIR / filename

    try:
        headers = {"User-Agent": "OpenClaw-AutoPublisher/1.0"}
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as response:
            with open(local_path, "wb") as f:
                f.write(response.read())
        logger.info(f"Downloaded image: {local_path}")
        return str(local_path)
    except Exception as e:
        logger.error(f"Failed to download image from {url}: {e}")
        return ""


def extract_keywords(title: str) -> str:
    """Extract search keywords from article title."""
    # Remove common stop words
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "has", "have", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "in", "on", "at", "to",
        "for", "of", "with", "by", "from", "as", "into", "about",
        "after", "before", "between", "and", "or", "but", "not",
        "this", "that", "these", "those", "it", "its", "they",
    }
    words = re.findall(r"\b[a-zA-Z]{3,}\b", title.lower())
    keywords = [w for w in words if w not in stop_words]
    return " ".join(keywords[:5])


def get_image_fetcher(config: dict):
    """Create appropriate image fetcher from config."""
    images_config = config.get("images", {})
    source = images_config.get("source", "unsplash").lower()

    if source == "unsplash":
        api_key = os.environ.get(images_config.get("api_key_env", "UNSPLASH_API_KEY"), "")
        if not api_key:
            logger.warning("UNSPLASH_API_KEY not set")
            return None
        return UnsplashFetcher(api_key)
    elif source == "pexels":
        api_key = os.environ.get(images_config.get("api_key_env", "PEXELS_API_KEY"), "")
        if not api_key:
            logger.warning("PEXELS_API_KEY not set")
            return None
        return PexelsFetcher(api_key)
    elif source == "pixabay":
        api_key = os.environ.get(images_config.get("api_key_env", "PIXABAY_API_KEY"), "")
        if not api_key:
            logger.warning("PIXABAY_API_KEY not set")
            return None
        return PixabayFetcher(api_key)
    else:
        logger.warning(f"Unknown image source: {source}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Fetch images for articles")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--query", help="Search query for image")
    parser.add_argument("--title", help="Article title (auto-extract keywords)")
    parser.add_argument("--url", help="Direct image URL to download")
    parser.add_argument("--count", type=int, default=1, help="Number of images")
    args = parser.parse_args()

    # Direct URL download
    if args.url:
        path = download_image(args.url)
        print(json.dumps({"success": bool(path), "path": path}))
        return

    # Load config
    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    fetcher = get_image_fetcher(config)
    if not fetcher:
        print(json.dumps({"success": False, "error": "No image fetcher available"}))
        return

    # Determine query
    query = args.query or (extract_keywords(args.title) if args.title else "news")

    # Search and download
    results = fetcher.search(query, args.count)
    downloaded = []
    for result in results:
        path = download_image(result["download_url"])
        if path:
            downloaded.append({
                "path": path,
                "alt": result["alt"],
                "credit": result["credit"],
                "source": result["source"],
            })

    print(json.dumps({
        "success": len(downloaded) > 0,
        "images": downloaded,
        "query": query,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
