#!/usr/bin/env python3
"""
Auto Publisher - WordPress/CMS Publishing Script
Publishes articles with featured images to WordPress via REST API.
Supports custom platforms via configurable endpoints.
"""

import argparse
import base64
import json
import os
import sys
import logging
import mimetypes
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin

# Setup logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "publisher.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("auto-publisher")


class WordPressPublisher:
    """Publish articles to WordPress via REST API v2."""

    def __init__(self, config: dict):
        self.site_url = config["platform"]["url"].rstrip("/")
        self.username = config["platform"]["username"]

        # Auto-detect REST API base URL format
        # Some WordPress sites use /wp-json/wp/v2, others use ?rest_route=/wp/v2
        self.api_style = config["platform"].get("api_style", "auto")
        self._detect_api_base()

        # Load password from environment variable
        password_env = config["platform"].get("app_password_env", "WP_APP_PASSWORD")
        self.password = os.environ.get(password_env)
        if not self.password:
            raise ValueError(
                f"Environment variable '{password_env}' is not set. "
                f"Please set it with your WordPress Application Password.\n"
                f"  export {password_env}='xxxx xxxx xxxx xxxx'\n"
                f"Or configure it in OpenClaw settings."
            )

        self.auth_header = self._make_auth_header()
        self.publishing_config = config.get("publishing", {})

    def _detect_api_base(self):
        """Auto-detect whether to use /wp-json/ or ?rest_route= format."""
        if self.api_style == "rest_route":
            self.use_rest_route = True
            self.api_base = f"{self.site_url}/?rest_route=/wp/v2"
            return
        elif self.api_style == "wp_json":
            self.use_rest_route = False
            self.api_base = f"{self.site_url}/wp-json/wp/v2"
            return

        # Auto-detect: try /wp-json/ first, fall back to ?rest_route=
        try:
            req = Request(
                f"{self.site_url}/wp-json/wp/v2/posts?per_page=1",
                headers={"User-Agent": "OpenClaw-AutoPublisher/1.0"}
            )
            with urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    self.use_rest_route = False
                    self.api_base = f"{self.site_url}/wp-json/wp/v2"
                    logger.info("Detected API style: /wp-json/")
                    return
        except Exception:
            pass

        # Try ?rest_route=
        try:
            req = Request(
                f"{self.site_url}/?rest_route=/wp/v2/posts&per_page=1",
                headers={"User-Agent": "OpenClaw-AutoPublisher/1.0"}
            )
            with urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    self.use_rest_route = True
                    self.api_base = f"{self.site_url}/?rest_route=/wp/v2"
                    logger.info("Detected API style: ?rest_route=")
                    return
        except Exception:
            pass

        # Default to ?rest_route= as more widely supported
        self.use_rest_route = True
        self.api_base = f"{self.site_url}/?rest_route=/wp/v2"
        logger.warning("Could not detect API style, defaulting to ?rest_route=")

    def _make_auth_header(self) -> str:
        """Create Basic Auth header."""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def _build_url(self, endpoint: str) -> str:
        """Build the correct API URL based on detected style."""
        if self.use_rest_route:
            # ?rest_route= style: split endpoint from query params
            # e.g. "tags?search=foo" -> rest_route=/wp/v2/tags&search=foo
            if "?" in endpoint:
                path, params = endpoint.split("?", 1)
                return f"{self.site_url}/?rest_route=/wp/v2/{path}&{params}"
            else:
                return f"{self.site_url}/?rest_route=/wp/v2/{endpoint}"
        else:
            return f"{self.api_base}/{endpoint}"

    def _api_request(self, endpoint: str, method: str = "GET",
                     data: dict = None, files: dict = None) -> dict:
        """Make an API request to WordPress REST API."""
        url = self._build_url(endpoint)

        if files:
            # File upload - multipart handling
            return self._upload_file(url, files)

        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw-AutoPublisher/1.0",
        }

        body = json.dumps(data).encode("utf-8") if data else None
        req = Request(url, data=body, headers=headers, method=method)

        try:
            with urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            logger.error(f"API Error {e.code}: {error_body}")
            raise
        except URLError as e:
            logger.error(f"Connection Error: {e.reason}")
            raise

    def _upload_file(self, url: str, files: dict) -> dict:
        """Upload a file to WordPress media library."""
        file_path = files.get("file")
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = os.path.basename(file_path)
        content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        with open(file_path, "rb") as f:
            file_data = f.read()

        headers = {
            "Authorization": self.auth_header,
            "Content-Type": content_type,
            "Content-Disposition": f'attachment; filename="{filename}"',
            "User-Agent": "OpenClaw-AutoPublisher/1.0",
        }

        req = Request(url, data=file_data, headers=headers, method="POST")

        try:
            with urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            logger.error(f"Upload Error {e.code}: {error_body}")
            raise

    def upload_image(self, image_path: str, alt_text: str = "") -> dict:
        """Upload an image and return media object."""
        logger.info(f"Uploading image: {image_path}")
        media = self._upload_file(
            self._build_url("media"),
            {"file": image_path}
        )

        # Update alt text if provided
        if alt_text and media.get("id"):
            self._api_request(
                f"media/{media['id']}",
                method="POST",
                data={"alt_text": alt_text}
            )

        logger.info(f"Image uploaded successfully. Media ID: {media.get('id')}")
        return media

    def get_or_create_category(self, name: str) -> int:
        """Get category ID by name, create if not exists."""
        from urllib.parse import quote
        # Search existing categories
        try:
            search_endpoint = f"categories"
            # For ?rest_route= style, params need to be handled differently
            if self.use_rest_route:
                url = f"{self.site_url}/?rest_route=/wp/v2/categories&search={quote(name)}&per_page=100"
                headers = {
                    "Authorization": self.auth_header,
                    "User-Agent": "OpenClaw-AutoPublisher/1.0",
                }
                req = Request(url, headers=headers)
                with urlopen(req, timeout=15) as response:
                    cats = json.loads(response.read().decode("utf-8"))
            else:
                cats = self._api_request(f"categories?search={name}&per_page=100")

            for cat in cats:
                if cat["name"].lower() == name.lower():
                    return cat["id"]
        except Exception:
            pass

        # Create new category
        try:
            cat = self._api_request("categories", method="POST", data={"name": name})
            return cat["id"]
        except HTTPError as e:
            if e.code == 400:  # Already exists (slug conflict)
                try:
                    if self.use_rest_route:
                        url = f"{self.site_url}/?rest_route=/wp/v2/categories&search={quote(name)}"
                        headers = {"Authorization": self.auth_header, "User-Agent": "OpenClaw-AutoPublisher/1.0"}
                        req = Request(url, headers=headers)
                        with urlopen(req, timeout=15) as response:
                            cats = json.loads(response.read().decode("utf-8"))
                    else:
                        cats = self._api_request(f"categories?search={name}")
                    if cats:
                        return cats[0]["id"]
                except Exception:
                    pass
            raise

    def get_or_create_tags(self, tag_names: list) -> list:
        """Get or create tags, return list of tag IDs."""
        import time
        from urllib.parse import quote
        tag_ids = []
        for name in tag_names:
            for attempt in range(3):
                try:
                    encoded_name = quote(name, safe='')
                    tags = self._api_request(f"tags?search={encoded_name}&per_page=10")
                    found = False
                    for tag in tags:
                        if tag["name"].lower() == name.lower():
                            tag_ids.append(tag["id"])
                            found = True
                            break
                    if not found:
                        tag = self._api_request("tags", method="POST", data={"name": name})
                        tag_ids.append(tag["id"])
                    break  # Success, exit retry loop
                except Exception as e:
                    if attempt < 2:
                        logger.info(f"Retrying tag '{name}' (attempt {attempt + 2}/3)...")
                        time.sleep(2)
                    else:
                        logger.warning(f"Could not create tag '{name}' after 3 attempts: {e}")
        return tag_ids

    def publish_article(self, article: dict) -> dict:
        """
        Publish an article to WordPress.

        article schema:
        {
            "title": "Article Title",
            "content": "<p>HTML content...</p>",
            "excerpt": "Short description",
            "categories": ["News", "World"],
            "tags": ["breaking", "politics"],
            "featured_image_path": "/path/to/image.jpg",
            "featured_image_alt": "Image description",
            "status": "publish",  # publish | draft | pending | future
            "date": "2026-03-27T10:00:00",  # optional, for scheduled posts
            "meta_description": "SEO meta description"
        }
        """
        logger.info(f"Publishing article: {article.get('title', 'Untitled')}")

        # Handle featured image
        featured_media_id = 0
        image_path = article.get("featured_image_path")
        if image_path and os.path.exists(image_path):
            try:
                media = self.upload_image(
                    image_path,
                    alt_text=article.get("featured_image_alt", article.get("title", ""))
                )
                featured_media_id = media.get("id", 0)
            except Exception as e:
                logger.warning(f"Failed to upload featured image: {e}")

        # Resolve categories
        category_ids = []
        for cat_name in article.get("categories", self.publishing_config.get("categories", [])):
            try:
                cat_id = self.get_or_create_category(cat_name)
                category_ids.append(cat_id)
            except Exception as e:
                logger.warning(f"Could not resolve category '{cat_name}': {e}")

        # Resolve tags
        tag_ids = self.get_or_create_tags(article.get("tags", []))

        # Build post data
        post_data = {
            "title": article.get("title", "Untitled"),
            "content": article.get("content", ""),
            "excerpt": article.get("excerpt", ""),
            "status": article.get("status", self.publishing_config.get("status", "draft")),
            "categories": category_ids,
            "tags": tag_ids,
        }

        if featured_media_id:
            post_data["featured_media"] = featured_media_id

        if article.get("date"):
            post_data["date"] = article["date"]

        # Create post
        result = self._api_request("posts", method="POST", data=post_data)

        post_url = result.get("link", "")
        post_id = result.get("id", "")
        logger.info(f"Article published successfully! ID: {post_id}, URL: {post_url}")

        return {
            "success": True,
            "post_id": post_id,
            "post_url": post_url,
            "title": article.get("title"),
            "status": result.get("status"),
        }


class CustomPublisher:
    """Publish articles to custom CMS platforms via REST API."""

    def __init__(self, config: dict):
        self.endpoints = config["platform"]["endpoints"]
        self.auth_header = self._resolve_auth(config)

    def _resolve_auth(self, config: dict) -> str:
        auth_template = self.endpoints.get("auth_header", "")
        if "{TOKEN}" in auth_template:
            token_env = config["platform"].get("token_env", "CMS_API_TOKEN")
            token = os.environ.get(token_env, "")
            return auth_template.replace("{TOKEN}", token)
        return auth_template

    def publish_article(self, article: dict) -> dict:
        """Publish to custom platform."""
        endpoint = self.endpoints.get("publish", "")
        method, url = endpoint.split(" ", 1)

        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
        }

        body = json.dumps(article).encode("utf-8")
        req = Request(url, data=body, headers=headers, method=method)

        try:
            with urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Custom publish failed: {e}")
            return {"success": False, "error": str(e)}


def get_publisher(config: dict):
    """Factory function to create the appropriate publisher."""
    platform_type = config["platform"]["type"].lower()

    if platform_type == "wordpress":
        return WordPressPublisher(config)
    elif platform_type == "custom":
        return CustomPublisher(config)
    else:
        raise ValueError(f"Unsupported platform type: {platform_type}")


def main():
    parser = argparse.ArgumentParser(description="Publish articles to CMS platforms")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--article", required=True, help="Path to article JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Preview without publishing")
    args = parser.parse_args()

    # Load config
    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Load article
    with open(args.article, "r", encoding="utf-8") as f:
        article = json.load(f)

    if args.dry_run:
        logger.info("=== DRY RUN MODE ===")
        logger.info(f"Title: {article.get('title')}")
        logger.info(f"Status: {article.get('status', 'draft')}")
        logger.info(f"Categories: {article.get('categories')}")
        logger.info(f"Tags: {article.get('tags')}")
        logger.info(f"Content length: {len(article.get('content', ''))} chars")
        logger.info(f"Has image: {bool(article.get('featured_image_path'))}")
        print(json.dumps({"success": True, "dry_run": True, "article": article}, ensure_ascii=False, indent=2))
        return

    # Publish
    publisher = get_publisher(config)

    # Support single article or batch
    if isinstance(article, list):
        results = []
        for art in article:
            try:
                result = publisher.publish_article(art)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to publish '{art.get('title')}': {e}")
                results.append({"success": False, "error": str(e), "title": art.get("title")})
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        result = publisher.publish_article(article)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
