#!/usr/bin/env python3
"""
WordPress SEO Article Publisher via REST API
Supports RankMath Free meta fields (title, description, focus_keyword)

Usage:
    python3 publish_wp_article.py '<json_data>'

Environment Variables Required:
    WP_SITE_URL       - WordPress site URL (e.g. https://example.com)
    WP_USERNAME       - WordPress username
    WP_APP_PASSWORD   - WordPress Application Password
    WP_CATEGORY_ID    - Default category ID for articles
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime


def make_api_request(url, auth_b64, method="GET", data=None):
    """Make an authenticated WordPress REST API request."""
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Basic {auth_b64}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "OpenClaw-WP-Publisher/1.0")

    if data is not None:
        req.data = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection failed: {e.reason}")


def get_or_create_tag(site_url, auth_b64, tag_name):
    """Get existing tag ID or create a new one. Returns tag ID or None."""
    # Search for existing tag
    search_url = f"{site_url}/wp-json/wp/v2/tags?search={urllib.parse.quote(tag_name)}&per_page=20"
    try:
        tags = make_api_request(search_url, auth_b64)
        for tag in tags:
            if tag["name"].lower().strip() == tag_name.lower().strip():
                return tag["id"]
    except Exception as e:
        print(f"  WARNING: Failed to search for tag '{tag_name}': {e}")

    # Create new tag
    create_url = f"{site_url}/wp-json/wp/v2/tags"
    try:
        tag = make_api_request(create_url, auth_b64, method="POST", data={"name": tag_name})
        print(f"  Created tag: {tag_name} (ID: {tag['id']})")
        return tag["id"]
    except Exception as e:
        print(f"  WARNING: Failed to create tag '{tag_name}': {e}")
        return None


def resolve_tags(site_url, auth_b64, tag_names):
    """Resolve a list of tag names to tag IDs."""
    if not tag_names:
        return []

    tag_ids = []
    for name in tag_names:
        name = name.strip()
        if not name:
            continue
        tag_id = get_or_create_tag(site_url, auth_b64, name)
        if tag_id:
            tag_ids.append(tag_id)
    return tag_ids


def publish_article(article_data):
    """
    Publish an article to WordPress via REST API with RankMath SEO meta.

    Args:
        article_data: dict with the following keys:
            title           (required) - Article title
            content         (required) - HTML content
            excerpt         (optional) - Short summary / meta description
            slug            (optional) - URL slug
            focus_keyword   (optional) - RankMath focus keyword
            seo_title       (optional) - Custom SEO title (defaults to title)
            seo_description (optional) - Custom meta description (defaults to excerpt)
            tags            (optional) - List of tag name strings
            category_id     (optional) - WordPress category ID (overrides env default)
            status          (optional) - "publish" or "draft" (default: "draft")

    Returns:
        dict with post ID, URL, and status
    """
    # Load credentials from environment
    site_url = os.environ.get("WP_SITE_URL", "").rstrip("/")
    username = os.environ.get("WP_USERNAME", "")
    app_password = os.environ.get("WP_APP_PASSWORD", "")
    default_category = os.environ.get("WP_CATEGORY_ID", "")

    if not site_url:
        print("ERROR: WP_SITE_URL environment variable is not set")
        sys.exit(1)
    if not username:
        print("ERROR: WP_USERNAME environment variable is not set")
        sys.exit(1)
    if not app_password:
        print("ERROR: WP_APP_PASSWORD environment variable is not set")
        sys.exit(1)

    # Build auth header
    credentials = f"{username}:{app_password}"
    auth_b64 = base64.b64encode(credentials.encode()).decode()

    # Extract fields
    title = article_data["title"]
    content = article_data["content"]
    excerpt = article_data.get("excerpt", "")
    slug = article_data.get("slug", "")
    focus_keyword = article_data.get("focus_keyword", "")
    seo_title = article_data.get("seo_title", "") or title
    seo_description = article_data.get("seo_description", "") or excerpt
    tags = article_data.get("tags", [])
    category_id = article_data.get("category_id", "") or default_category
    status = article_data.get("status", "draft")

    print(f"Publishing article: {title}")
    print(f"  Slug:          {slug}")
    print(f"  Status:        {status}")
    print(f"  Focus Keyword: {focus_keyword}")
    print(f"  Category ID:   {category_id}")

    # Resolve tag names → IDs
    tag_ids = resolve_tags(site_url, auth_b64, tags)
    if tags:
        print(f"  Tags:          {tags} → IDs: {tag_ids}")

    # Build post payload with RankMath meta fields
    post_data = {
        "title": title,
        "content": content,
        "excerpt": excerpt,
        "slug": slug,
        "status": status,
        "meta": {
            # RankMath Free SEO fields
            "rank_math_title": seo_title,
            "rank_math_description": seo_description,
            "rank_math_focus_keyword": focus_keyword,
        }
    }

    # Add category if provided
    if category_id:
        try:
            post_data["categories"] = [int(category_id)]
        except ValueError:
            print(f"  WARNING: Invalid category ID '{category_id}', skipping")

    # Add tags if any
    if tag_ids:
        post_data["tags"] = tag_ids

    # Publish via REST API
    api_url = f"{site_url}/wp-json/wp/v2/posts"

    try:
        result = make_api_request(api_url, auth_b64, method="POST", data=post_data)
    except RuntimeError as e:
        print(f"ERROR: Failed to publish article")
        print(f"  {e}")
        sys.exit(1)

    # Success output
    post_id = result["id"]
    post_url = result["link"]
    post_status = result["status"]

    print()
    print("=" * 60)
    print(f"✅ Article published successfully!")
    print(f"  Post ID:        {post_id}")
    print(f"  URL:            {post_url}")
    print(f"  Status:         {post_status}")
    print(f"  Focus Keyword:  {focus_keyword}")
    print("=" * 60)

    # Structured output for agent parsing
    output = {
        "success": True,
        "post_id": post_id,
        "url": post_url,
        "status": post_status,
        "title": title,
        "slug": slug,
        "focus_keyword": focus_keyword,
        "seo_title": seo_title,
        "seo_description": seo_description,
        "tags": tags,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    print(f"\n__RESULT_JSON__:{json.dumps(output)}")

    return output


def print_usage():
    """Print usage instructions."""
    print("WordPress SEO Article Publisher (RankMath Compatible)")
    print()
    print("Usage:")
    print("  python3 publish_wp_article.py '<json_data>'")
    print()
    print("Required environment variables:")
    print("  WP_SITE_URL       WordPress site URL")
    print("  WP_USERNAME       WordPress username")
    print("  WP_APP_PASSWORD   WordPress Application Password")
    print("  WP_CATEGORY_ID    Default category ID (optional)")
    print()
    print("JSON fields:")
    print("  title           (required) Article title")
    print("  content         (required) HTML content body")
    print("  excerpt         (optional) Short summary for meta description")
    print("  slug            (optional) SEO-friendly URL slug")
    print("  focus_keyword   (optional) RankMath focus keyword")
    print("  seo_title       (optional) Custom SEO title")
    print("  seo_description (optional) Custom meta description")
    print("  tags            (optional) List of tag names")
    print("  category_id     (optional) Override default category")
    print("  status          (optional) 'publish' or 'draft' (default: draft)")
    print()
    print("Example:")
    print("""  python3 publish_wp_article.py '{
    "title": "Benefits of Robot Rental",
    "content": "<h2>Why Rent?</h2><p>Content here...</p>",
    "excerpt": "Discover the benefits of robot rental for events.",
    "slug": "benefits-robot-rental",
    "focus_keyword": "robot rental",
    "tags": ["robot", "rental", "events"],
    "status": "draft"
  }'""")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_usage()
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    try:
        article = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}")
        sys.exit(1)

    # Validate required fields
    required = ["title", "content"]
    missing = [f for f in required if not article.get(f)]
    if missing:
        print(f"ERROR: Missing required fields: {', '.join(missing)}")
        sys.exit(1)

    publish_article(article)
