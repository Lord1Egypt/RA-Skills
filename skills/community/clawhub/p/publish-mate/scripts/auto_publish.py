#!/usr/bin/env python3
"""
Auto Publisher - One-Click Publishing Pipeline
Combines: fetch news → find images → compose article → upload & publish

Usage:
    python3 auto_publish.py --config ../config.json
    python3 auto_publish.py --config ../config.json --max 3 --dry-run
    python3 auto_publish.py --config ../config.json --image-source rss
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import ssl
import logging
import mimetypes
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote

# Setup
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = DATA_DIR / "images"
HISTORY_FILE = DATA_DIR / "published_history.json"

for d in [LOG_DIR, DATA_DIR, IMAGE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Import full-article fetcher from fetch_news module
sys.path.insert(0, str(SCRIPT_DIR))
from fetch_news import fetch_full_article

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "auto_publish.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("auto-publish")


# ============================================================
# Utility Functions
# ============================================================

def fetch_url(url: str, timeout: int = 15) -> bytes:
    """Fetch content from URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OpenClaw-AutoPublisher/1.0)",
        "Accept": "*/*",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        # Retry with SSL context
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
            with urlopen(req, timeout=timeout, context=ctx) as resp:
                return resp.read()
        except ImportError:
            raise


def strip_html(text: str) -> str:
    """Remove HTML tags."""
    clean = re.sub(r"<[^>]+>", "", text)
    return unescape(clean).strip()


def article_hash(title: str, url: str) -> str:
    return hashlib.md5(f"{title}|{url}".encode()).hexdigest()


def load_history() -> set:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_history(history: set):
    with open(HISTORY_FILE, "w") as f:
        json.dump(list(history), f)


# ============================================================
# News Fetching
# ============================================================

def fetch_rss(source: dict) -> list:
    """Fetch articles from RSS feed."""
    url = source["url"]
    name = source.get("name", url)
    max_items = source.get("max_items", 5)
    logger.info(f"Fetching RSS: {name}")

    try:
        content = fetch_url(url)
        root = ET.fromstring(content)
        items = []

        for item in root.findall(".//item"):
            if len(items) >= max_items:
                break
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            desc = strip_html(item.findtext("description", ""))
            pub_date = item.findtext("pubDate", "")

            # Extract image from media:content or enclosure
            image_url = ""
            media = item.find("{http://search.yahoo.com/mrss/}content")
            if media is not None:
                image_url = media.get("url", "")

            if not image_url:
                media_thumb = item.find("{http://search.yahoo.com/mrss/}thumbnail")
                if media_thumb is not None:
                    image_url = media_thumb.get("url", "")

            if not image_url:
                enclosure = item.find("enclosure")
                if enclosure is not None and "image" in enclosure.get("type", ""):
                    image_url = enclosure.get("url", "")

            if not image_url:
                # Try to extract from content
                content_encoded = item.findtext(
                    "{http://purl.org/rss/1.0/modules/content/}encoded", ""
                )
                img_match = re.search(
                    r'<img[^>]+src=["\']([^"\']+)', content_encoded or ""
                )
                if img_match:
                    image_url = img_match.group(1)

            tags = [cat.text for cat in item.findall("category") if cat.text]

            # Fetch full article content if description is short
            content = desc
            if len(desc) < 500 and link:
                logger.info(f"Fetching full article: {title[:50]}...")
                full_content = fetch_full_article(link)
                if full_content and len(full_content) > len(desc):
                    content = full_content

            items.append({
                "title": title,
                "summary": desc[:500],
                "content": content,
                "source_url": link,
                "source_name": name,
                "published_date": pub_date,
                "image_url": image_url,
                "tags": tags[:10],
            })

        logger.info(f"Fetched {len(items)} articles from {name}")
        return items
    except Exception as e:
        logger.error(f"Failed to fetch RSS '{name}': {e}")
        return []


def fetch_newsapi(source: dict) -> list:
    """Fetch from NewsAPI.org."""
    api_key = os.environ.get(source.get("api_key_env", "NEWS_API_KEY"), "")
    if not api_key:
        logger.warning("NEWS_API_KEY not set, skipping")
        return []

    category = source.get("category", "general")
    country = source.get("country", "us")
    max_items = source.get("max_items", 5)

    try:
        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"country={country}&category={category}"
            f"&pageSize={max_items}&apiKey={api_key}"
        )
        data = json.loads(fetch_url(url))
        items = []
        for a in data.get("articles", []):
            items.append({
                "title": a.get("title", ""),
                "summary": (a.get("description") or "")[:500],
                "content": a.get("content") or a.get("description") or "",
                "source_url": a.get("url", ""),
                "source_name": a.get("source", {}).get("name", "NewsAPI"),
                "published_date": a.get("publishedAt", ""),
                "image_url": a.get("urlToImage", ""),
                "tags": [],
            })
        logger.info(f"Fetched {len(items)} articles from NewsAPI")
        return items
    except Exception as e:
        logger.error(f"NewsAPI failed: {e}")
        return []


def fetch_all_news(config: dict) -> list:
    """Fetch from all configured sources."""
    sources = config.get("news_sources", [])
    all_articles = []
    for source in sources:
        if source.get("_disabled"):
            continue
        src_type = source.get("type", "rss")
        if src_type == "rss":
            all_articles.extend(fetch_rss(source))
        elif src_type == "newsapi":
            all_articles.extend(fetch_newsapi(source))
    return all_articles


# ============================================================
# Image Fetching
# ============================================================

def search_pixabay(query: str, api_key: str) -> str:
    """Search Pixabay for a free image, return download URL."""
    url = (
        f"https://pixabay.com/api/?key={api_key}"
        f"&q={quote(query)}&per_page=3&image_type=photo&orientation=horizontal"
        f"&safesearch=true&min_width=800"
    )
    try:
        data = json.loads(fetch_url(url))
        hits = data.get("hits", [])
        if hits:
            return hits[0].get("largeImageURL", "")
    except Exception as e:
        logger.warning(f"Pixabay search failed: {e}")
    return ""


def search_unsplash(query: str, api_key: str) -> str:
    """Search Unsplash for an image, return download URL."""
    url = f"https://api.unsplash.com/search/photos?query={quote(query)}&per_page=1&orientation=landscape"
    headers = {
        "Authorization": f"Client-ID {api_key}",
        "Accept": "application/json",
        "User-Agent": "OpenClaw-AutoPublisher/1.0",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            results = data.get("results", [])
            if results:
                return results[0]["urls"]["regular"]
    except Exception as e:
        logger.warning(f"Unsplash search failed: {e}")
    return ""


def search_pexels(query: str, api_key: str) -> str:
    """Search Pexels for an image, return download URL."""
    url = f"https://api.pexels.com/v1/search?query={quote(query)}&per_page=1&orientation=landscape"
    headers = {
        "Authorization": api_key,
        "User-Agent": "OpenClaw-AutoPublisher/1.0",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            photos = data.get("photos", [])
            if photos:
                return photos[0]["src"]["large"]
    except Exception as e:
        logger.warning(f"Pexels search failed: {e}")
    return ""


def get_image_for_article(article: dict, config: dict) -> str:
    """
    Get an image for the article. Returns local file path or empty string.

    Strategy:
    1. Use image_url from RSS feed if available
    2. Search image API (Unsplash/Pexels/Pixabay) based on article title
    3. Use picsum.photos as last resort (random image)
    """
    images_config = config.get("images", {})

    # Strategy 1: Use RSS image URL
    rss_image = article.get("image_url", "")
    if rss_image and images_config.get("fallback_from_rss", True):
        logger.info(f"Using RSS image: {rss_image[:80]}...")
        local_path = download_image(rss_image, article["title"])
        if local_path:
            return local_path

    # Strategy 2: Search image API
    source = images_config.get("source", "").lower()
    keywords = extract_keywords(article["title"])

    if source == "unsplash":
        api_key = os.environ.get(images_config.get("api_key_env", "UNSPLASH_API_KEY"), "")
        if api_key:
            img_url = search_unsplash(keywords, api_key)
            if img_url:
                return download_image(img_url, article["title"])

    elif source == "pexels":
        api_key = os.environ.get(images_config.get("api_key_env", "PEXELS_API_KEY"), "")
        if api_key:
            img_url = search_pexels(keywords, api_key)
            if img_url:
                return download_image(img_url, article["title"])

    elif source == "pixabay":
        api_key = os.environ.get(images_config.get("api_key_env", "PIXABAY_API_KEY"), "")
        if api_key:
            img_url = search_pixabay(keywords, api_key)
            if img_url:
                return download_image(img_url, article["title"])

    # Strategy 3: Fallback to picsum.photos (random but always works)
    logger.info("Using picsum.photos fallback for image")
    fallback_url = "https://picsum.photos/800/450"
    return download_image(fallback_url, article["title"])


def extract_keywords(title: str) -> str:
    """Extract English keywords from title for image search."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "has", "have", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "in", "on", "at", "to",
        "for", "of", "with", "by", "from", "as", "into", "about",
        "after", "before", "between", "and", "or", "but", "not",
        "this", "that", "these", "those", "it", "its", "they",
        "says", "said", "over", "new", "how", "why", "what",
    }
    words = re.findall(r"\b[a-zA-Z]{3,}\b", title.lower())
    keywords = [w for w in words if w not in stop_words]
    return " ".join(keywords[:5]) if keywords else "news world"


def download_image(url: str, title: str = "") -> str:
    """Download image to local directory, return path."""
    slug = re.sub(r"[^a-z0-9]", "-", title.lower()[:40]).strip("-") or "image"
    filename = f"{slug}-{hashlib.md5(url.encode()).hexdigest()[:8]}.jpg"
    local_path = IMAGE_DIR / filename

    # Skip if already downloaded
    if local_path.exists() and local_path.stat().st_size > 1000:
        logger.info(f"Image already cached: {local_path}")
        return str(local_path)

    try:
        img_data = fetch_url(url, timeout=20)
        if len(img_data) < 1000:
            logger.warning(f"Downloaded image too small ({len(img_data)} bytes), skipping")
            return ""
        with open(local_path, "wb") as f:
            f.write(img_data)
        logger.info(f"Image downloaded: {local_path} ({len(img_data)} bytes)")
        return str(local_path)
    except Exception as e:
        logger.warning(f"Failed to download image from {url[:80]}: {e}")
        return ""


# ============================================================
# WordPress Publisher
# ============================================================

class WordPressPublisher:
    """Publish articles with images to WordPress."""

    def __init__(self, config: dict):
        self.site_url = config["platform"]["url"].rstrip("/")
        self.username = config["platform"]["username"]

        password_env = config["platform"].get("app_password_env", "WP_APP_PASSWORD")
        self.password = os.environ.get(password_env)
        if not self.password:
            raise ValueError(f"Environment variable '{password_env}' not set!")

        cred = f"{self.username}:{self.password}"
        self.auth_header = f"Basic {base64.b64encode(cred.encode()).decode()}"

        # Detect API style
        self.use_rest_route = True  # Default
        self._detect_api()
        self.pub_config = config.get("publishing", {})

    def _detect_api(self):
        """Auto-detect REST API URL format."""
        # Try /wp-json/ first (with auth)
        try:
            req = Request(
                f"{self.site_url}/wp-json/wp/v2/posts?per_page=1",
                headers={
                    "User-Agent": "OpenClaw/1.0",
                    "Authorization": self.auth_header,
                }
            )
            with urlopen(req, timeout=8) as resp:
                if resp.status == 200:
                    self.use_rest_route = False
                    logger.info("API: /wp-json/ style")
                    return
        except Exception:
            pass
        
        logger.info("API: /wp-json/ style (default)")
        self.use_rest_route = False

    def _url(self, endpoint: str) -> str:
        """Build API URL."""
        if self.use_rest_route:
            if "?" in endpoint:
                path, params = endpoint.split("?", 1)
                return f"{self.site_url}/?rest_route=/wp/v2/{path}&{params}"
            return f"{self.site_url}/?rest_route=/wp/v2/{endpoint}"
        return f"{self.site_url}/wp-json/wp/v2/{endpoint}"

    def _request(self, endpoint: str, method: str = "GET",
                 data: dict = None, retries: int = 2) -> dict:
        """Make API request with retry on connection failures."""
        url = self._url(endpoint)
        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw-AutoPublisher/1.0)",
        }
        body = json.dumps(data).encode("utf-8") if data else None

        for attempt in range(retries + 1):
            try:
                req = Request(url, data=body, headers=headers, method=method)
                with urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except (URLError, ConnectionError, OSError) as e:
                if attempt < retries:
                    wait = 3 * (attempt + 1)
                    logger.info(f"Request retry {attempt+1}/{retries} for {endpoint}: {e}")
                    time.sleep(wait)
                else:
                    raise

    def upload_image(self, file_path: str, alt_text: str = "") -> int:
        """Upload image to media library using http.client for reliable SSL handling.

        Some servers (behind Nginx/CDN) accept the upload (201) but return an empty body.
        In that case, we query the media library to find the recently uploaded image.
        """
        import http.client as httplib
        from urllib.parse import urlparse

        logger.info(f"Uploading image: {Path(file_path).name}")

        filename = os.path.basename(file_path)
        content_type = mimetypes.guess_type(file_path)[0] or "image/jpeg"

        with open(file_path, "rb") as f:
            file_data = f.read()

        parsed = urlparse(self.site_url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        use_ssl = parsed.scheme == "https"

        headers = {
            "Authorization": self.auth_header,
            "Content-Type": content_type,
            "Content-Disposition": f'attachment; filename="{filename}"',
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw-AutoPublisher/1.0)",
            "Connection": "close",
            "Content-Length": str(len(file_data)),
        }

        if self.use_rest_route:
            path = "/?rest_route=/wp/v2/media"
        else:
            path = "/wp-json/wp/v2/media"

        for attempt in range(3):
            try:
                if use_ssl:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    conn = httplib.HTTPSConnection(host, port, timeout=60, context=ctx)
                else:
                    conn = httplib.HTTPConnection(host, port, timeout=60)

                conn.request("POST", path, body=file_data, headers=headers)
                resp = conn.getresponse()
                status = resp.status
                body = resp.read().decode("utf-8", errors="replace")
                conn.close()

                if status in (200, 201):
                    # Try to parse response body
                    if body.strip():
                        try:
                            media = json.loads(body)
                            media_id = media.get("id", 0)
                            if media_id:
                                logger.info(f"Image uploaded! Media ID: {media_id}")
                                time.sleep(3)
                                return media_id
                        except json.JSONDecodeError:
                            pass

                    # Server returned 201 but empty/invalid body
                    # Query recent media to find our upload
                    logger.info("Upload accepted (201) but empty response. Querying media library...")
                    time.sleep(5)
                    media_id = self._find_recent_media(filename)
                    if media_id:
                        logger.info(f"Found uploaded image! Media ID: {media_id}")
                        return media_id
                    else:
                        logger.warning("Could not find uploaded media in library")
                else:
                    logger.warning(f"Image upload attempt {attempt+1}: HTTP {status}")
                    if body:
                        logger.warning(f"Response: {body[:200]}")

            except Exception as e:
                if attempt < 2:
                    logger.warning(f"Image upload attempt {attempt+1} failed: {e}, retrying in 5s...")
                    time.sleep(5)
                else:
                    logger.error(f"Image upload failed after 3 attempts: {e}")
                    return 0
        return 0

    def _find_recent_media(self, filename_hint: str = "") -> int:
        """Find the most recently uploaded media item."""
        try:
            media_list = self._request("media?per_page=1&orderby=date&order=desc")
            if media_list and isinstance(media_list, list):
                return media_list[0].get("id", 0)
        except Exception as e:
            logger.warning(f"Could not query media library: {e}")
        return 0

    def get_or_create_category(self, name: str) -> int:
        """Get or create a category."""
        # Search existing
        try:
            cats = self._request(f"categories?search={quote(name, safe='')}&per_page=50")
            for cat in cats:
                if cat["name"].lower() == name.lower():
                    return cat["id"]
        except Exception:
            pass

        # Try to create
        try:
            cat = self._request("categories", method="POST", data={"name": name})
            return cat["id"]
        except HTTPError as e:
            # 400 = term_exists (already exists with different slug)
            if e.code == 400:
                try:
                    error_data = json.loads(e.read().decode("utf-8"))
                    if error_data.get("code") == "term_exists":
                        term_id = error_data.get("data", {}).get("term_id")
                        if term_id:
                            return term_id
                except Exception:
                    pass
                # Fallback: search again more broadly
                try:
                    cats = self._request(f"categories?per_page=100")
                    for cat in cats:
                        if cat["name"].lower() == name.lower():
                            return cat["id"]
                except Exception:
                    pass
            logger.warning(f"Category '{name}' failed: {e}")
            return 0
        except Exception as e:
            logger.warning(f"Category '{name}' failed: {e}")
            return 0

    def get_or_create_tag(self, name: str) -> int:
        """Get or create a tag with retry."""
        for attempt in range(3):
            try:
                tags = self._request(f"tags?search={quote(name, safe='')}&per_page=10")
                for tag in tags:
                    if tag["name"].lower() == name.lower():
                        return tag["id"]
                tag = self._request("tags", method="POST", data={"name": name})
                return tag["id"]
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    logger.warning(f"Tag '{name}' failed: {e}")
        return 0

    def publish(self, title: str, content: str, excerpt: str = "",
                categories: list = None, tags: list = None,
                featured_image_path: str = "", status: str = "publish") -> dict:
        """
        Full publish pipeline: upload image → create categories/tags → create post.
        """
        # Upload featured image
        featured_media = 0
        if featured_image_path and os.path.exists(featured_image_path):
            featured_media = self.upload_image(featured_image_path, alt_text=title)

        # Resolve categories
        cat_ids = []
        for name in (categories or self.pub_config.get("categories", [])):
            cid = self.get_or_create_category(name)
            if cid:
                cat_ids.append(cid)

        # Resolve tags
        tag_ids = []
        for name in (tags or []):
            tid = self.get_or_create_tag(name)
            if tid:
                tag_ids.append(tid)

        # Create post
        post_data = {
            "title": title,
            "content": content,
            "excerpt": excerpt,
            "status": status or self.pub_config.get("status", "draft"),
            "categories": cat_ids,
            "tags": tag_ids,
        }
        if featured_media:
            post_data["featured_media"] = featured_media

        logger.info(f"Creating post: {title[:60]}...")
        result = self._request("posts", method="POST", data=post_data)

        return {
            "success": True,
            "post_id": result.get("id"),
            "post_url": result.get("link"),
            "title": title,
            "status": result.get("status"),
            "featured_media": featured_media,
        }


# ============================================================
# Main Pipeline
# ============================================================

def run_pipeline(config: dict, max_articles: int = 0, dry_run: bool = False):
    """
    Full pipeline: Fetch news → Get images → Compose → Publish
    """
    logger.info("=" * 60)
    logger.info("Auto Publisher Pipeline Started")
    logger.info("=" * 60)

    # 1. Fetch news
    logger.info("\n📰 Step 1: Fetching news...")
    all_articles = fetch_all_news(config)
    logger.info(f"Total articles fetched: {len(all_articles)}")

    if not all_articles:
        logger.warning("No articles found. Check your news sources.")
        return []

    # 2. Dedup
    history = load_history()
    unique = []
    for art in all_articles:
        h = article_hash(art["title"], art["source_url"])
        if h not in history:
            unique.append(art)
            history.add(h)

    limit = max_articles or config.get("publishing", {}).get("posts_per_day", 5)
    unique = unique[:limit]
    logger.info(f"Unique new articles: {len(unique)}")

    if not unique:
        logger.info("No new articles to publish (all already published).")
        return []

    # 3. Process each article
    results = []
    publisher = None if dry_run else WordPressPublisher(config)
    content_rules = config.get("content_rules", {})
    language = config.get("publishing", {}).get("language", "en")

    for i, article in enumerate(unique):
        logger.info(f"\n{'='*40}")
        logger.info(f"📝 Article {i+1}/{len(unique)}: {article['title'][:60]}")

        # 3a. Get image
        logger.info("🖼️  Finding image...")
        image_path = get_image_for_article(article, config)
        logger.info(f"Image: {image_path or 'None'}")

        # 3b. Compose HTML content
        source_link = f'<a href="{article["source_url"]}">{article["source_name"]}</a>'
        html_content = f"""<p>{article['content']}</p>
<hr />
<p><em>Source: {source_link}</em></p>
<p><small>Auto-published by OpenClaw Auto Publisher</small></p>"""

        if dry_run:
            logger.info(f"[DRY RUN] Would publish: {article['title']}")
            logger.info(f"  Image: {image_path or 'None'}")
            logger.info(f"  Content length: {len(html_content)} chars")
            results.append({
                "success": True,
                "dry_run": True,
                "title": article["title"],
                "image": image_path,
            })
            continue

        # 3c. Publish
        try:
            default_tags = config.get("publishing", {}).get("default_tags", [])
            all_tags = list(set(article.get("tags", []) + default_tags))

            result = publisher.publish(
                title=article["title"],
                content=html_content,
                excerpt=article["summary"][:200],
                categories=None,  # Use config defaults
                tags=all_tags[:10],
                featured_image_path=image_path,
                status=config.get("publishing", {}).get("status", "publish"),
            )
            results.append(result)
            logger.info(f"✅ Published: {result.get('post_url', 'N/A')}")

        except Exception as e:
            logger.error(f"❌ Failed to publish '{article['title']}': {e}")
            results.append({
                "success": False,
                "title": article["title"],
                "error": str(e),
            })

        # Small delay between posts
        if i < len(unique) - 1:
            time.sleep(3)

    # Save history
    save_history(history)

    # Summary
    success = sum(1 for r in results if r.get("success"))
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 Pipeline Complete: {success}/{len(results)} articles published")
    for r in results:
        status = "✅" if r.get("success") else "❌"
        url = r.get("post_url", r.get("error", "N/A"))
        logger.info(f"  {status} {r.get('title', 'Unknown')[:50]}")
        if r.get("post_url"):
            logger.info(f"     → {r['post_url']}")
    logger.info("=" * 60)

    return results


def main():
    parser = argparse.ArgumentParser(description="Auto Publisher - Full Pipeline")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--max", type=int, default=0, help="Max articles to publish")
    parser.add_argument("--dry-run", action="store_true", help="Preview without publishing")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = BASE_DIR / args.config

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    results = run_pipeline(config, max_articles=args.max, dry_run=args.dry_run)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
