import sys
import os
import json
import time
import requests
from datetime import datetime, timezone, timedelta

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

CACHE_FILE = "wechat_articles_cache.json"
CACHE_EXPIRE_SECONDS = 3600  # 1 hour


def timestamp_to_local_str(timestamp):
    """Convert Unix timestamp to UTC+8 datetime string."""
    if not timestamp:
        return ""
    dt = datetime.fromtimestamp(timestamp, tz=timezone(timedelta(hours=8)))
    return dt.strftime("%Y-%m-%d %H:%M")

def get_api_key():
    api_key = os.environ.get("WCRSS_API_KEY")
    if not api_key:
        raise ValueError("WCRSS_API_KEY environment variable not set. Please set it first.")
    return api_key

def fetch_articles(recent_days=3, num=10):
    """
    Fetch articles from wcrss.com API and cache locally.
    Returns the cached data (either fresh or from cache).
    """
    api_key = get_api_key()

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cached_data = json.load(f)

        cache_time = cached_data.get("cache_time", 0)
        current_time = time.time()

        if current_time - cache_time < CACHE_EXPIRE_SECONDS:
            print(f"Using cached data (age: {int(current_time - cache_time)}s)")
            return cached_data

    url = f"https://api.wcrss.com/sapi/articles?recentDays={recent_days}&num={num}"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API request failed: {str(e)}")

    cached_data = {
        "cache_time": time.time(),
        "cache_time_readable": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "articles": data.get("articles", []),
        "publishers": data.get("publishers", [])
    }

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cached_data, f, ensure_ascii=False, indent=2)

    print(f"Fetched {len(cached_data['articles'])} articles and cached to {CACHE_FILE}")
    return cached_data

def get_article_by_index(index):
    """
    Get a single article by its index in the list.
    Returns dict with: title, author, content_html, url, publish_time
    Returns None if index is out of range.
    """
    if not os.path.exists(CACHE_FILE):
        raise ValueError(f"Cache file {CACHE_FILE} not found. Please run fetch_articles() first.")

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    articles = data.get("articles", [])
    publishers = data.get("publishers", [])

    if index < 0 or index >= len(articles):
        return None

    article = articles[index]
    mp_id = article.get("mp_id")

    author = "Unknown"
    for pub in publishers:
        if pub.get("mp_id") == mp_id:
            author = pub.get("nickname", "Unknown")
            break

    return {
        "title": article.get("title", ""),
        "author": author,
        "publish_time": timestamp_to_local_str(article.get("publish_time")),
        "url": article.get("url", ""),
        "content_html": article.get("content_html", ""),
        "description": article.get("description", "")
    }

def get_articles_count():
    """Get the total number of cached articles."""
    if not os.path.exists(CACHE_FILE):
        return 0

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return len(data.get("articles", []))

def clear_cache():
    """Clear the local cache file."""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print(f"Cache file {CACHE_FILE} removed")
    else:
        print("No cache file to remove")

if __name__ == "__main__":
    # sys.argv = [__file__, "count", "1", "10"]  # debug FIXME
    if len(sys.argv) < 2:
        print("Usage: python wechat_rss.py <command> [args]")
        print("Commands:")
        print("  fetch [recentDays] [num]  - Fetch and cache articles")
        print("  get <index>                - Get article by index")
        print("  count                      - Get total articles count")
        print("  clear                      - Clear cache")
        sys.exit(1)

    command = sys.argv[1]

    if command == "fetch":
        recent_days = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        num = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = fetch_articles(recent_days, num)
        print(f"Total articles: {len(result['articles'])}")
    elif command == "get":
        index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        article = get_article_by_index(index)
        if article:
            print(json.dumps(article, ensure_ascii=False, indent=2))
        else:
            print(f"Article at index {index} not found")
    elif command == "count":
        print(get_articles_count())
    elif command == "clear":
        clear_cache()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
