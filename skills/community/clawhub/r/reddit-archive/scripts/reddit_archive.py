#!/usr/bin/env python3
"""
Reddit Archive - Download images, GIFs, and videos from Reddit users or subreddits.
Usage: python3 reddit_archive.py -u username | -s subreddit [options]
"""

import argparse
import html as html_module
import json
import os
import re
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

# === CONFIG ===
# Reddit's JSON API stopped serving anonymous requests in mid-2026 — 403
# + anti-bot HTML page regardless of UA. The "descriptive bot UA" path
# that their docs used to recommend is the one currently getting blocked
# the hardest, so we present as Safari and scrape old.reddit.com's
# server-rendered listing HTML instead. Schema (the `<div class="thing"
# data-*>` attributes) has been stable since ~2010.
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
ACCEPT_HEADER = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
API_DELAY = 0.8  # seconds between listing-page fetches

# === ARGS ===
def parse_args():
    p = argparse.ArgumentParser(description="Archive Reddit posts (images, GIFs, videos)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("-u", "--user", help="Reddit username")
    g.add_argument("-s", "--subreddit", help="Subreddit name (without r/)")
    p.add_argument("-o", "--output", default=None, help="Output directory")
    p.add_argument("--sort", default="hot", choices=["hot", "new", "rising", "top", "controversial"])
    p.add_argument("--time", default=None, choices=["hour", "day", "week", "month", "year", "all"])
    p.add_argument("--after", default=None, help="Start date (YYYY-MM-DD)")
    p.add_argument("--before", default=None, help="End date (YYYY-MM-DD)")
    p.add_argument("--limit", type=int, default=0, help="Max posts (0=unlimited)")
    p.add_argument("--images", action="store_true", default=True, help="Download images (jpg,png,webp)")
    p.add_argument("--gifs", action="store_true", default=True, help="Download GIFs/videos")
    p.add_argument("--skip-existing", action="store_true", default=True, help="Skip existing files")
    p.add_argument("--workers", type=int, default=4, help="Parallel workers")
    return p.parse_args()

# === HELPERS ===
def get_output_dir(args):
    if args.output:
        return Path(args.output)
    target = args.user or f"r_{args.subreddit}"
    return Path.home() / "temp" / f".reddit_{target}"

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)
    return path

def date_to_utc(date_str):
    """Convert YYYY-MM-DD to Reddit API after parameter."""
    if not date_str:
        return None
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return str(int(dt.timestamp()))
    except:
        return None

def _attr(attrs, name):
    m = re.search(rf'\bdata-{re.escape(name)}="([^"]*)"', attrs)
    return m.group(1) if m else None

def _attr_bool(attrs, name):
    return _attr(attrs, name) == "true"

def _attr_int(attrs, name):
    v = _attr(attrs, name)
    try:
        return int(v) if v is not None else None
    except ValueError:
        return None

def _extract_gallery_metadata(chunk):
    """For gallery posts, old.reddit embeds preview.redd.it URLs in the
    listing chunk. Each unique image is also available unsigned at
    i.redd.it under the same filename (full resolution, no expiry).
    Returns a dict shaped like Reddit's JSON `media_metadata` so the
    downstream get_image_url function doesn't need to change."""
    seen = set()
    metadata = {}
    pattern = re.compile(r"https?://preview\.redd\.it/([a-z0-9]+\.(?:jpg|jpeg|png|webp|gif))", re.I)
    for m in pattern.finditer(chunk):
        filename = m.group(1).lower()
        if filename in seen:
            continue
        seen.add(filename)
        key = f"img_{len(metadata)}"
        metadata[key] = {
            "status": "ready",
            "s": {"u": f"https://i.redd.it/{filename}"}
        }
    return metadata or None

def parse_reddit_html(html):
    """Parse an old.reddit.com listing page into post dicts shaped like
    the (now-dead) JSON API output, so the rest of the script doesn't
    care about the source change. Only the fields downstream code reads
    are populated: id, url, subreddit, created_utc, is_gallery,
    media_metadata, plus a few useful extras."""
    posts = []
    thing_re = re.compile(r'<div\s+([^>]*\bclass="[^"]*\bthing\b[^"]*"[^>]*)>')
    matches = list(thing_re.finditer(html))
    for i, m in enumerate(matches):
        attrs = m.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        chunk = html[m.start():end]

        fullname = _attr(attrs, "fullname")
        if not fullname or not fullname.startswith("t3_"):
            continue
        if _attr_bool(attrs, "promoted"):
            continue  # skip ads

        url = _attr(attrs, "url") or ""
        if url:
            url = html_module.unescape(url)
            if url.startswith("/"):
                url = "https://www.reddit.com" + url

        timestamp_ms = _attr_int(attrs, "timestamp")
        created_utc = timestamp_ms / 1000 if timestamp_ms is not None else None
        is_gallery = _attr_bool(attrs, "is-gallery")
        domain = _attr(attrs, "domain") or ""

        post = {
            "id": fullname[3:],
            "name": fullname,
            "url": url,
            "permalink": _attr(attrs, "permalink"),
            "author": _attr(attrs, "author"),
            "subreddit": _attr(attrs, "subreddit"),
            "domain": domain,
            "score": _attr_int(attrs, "score"),
            "num_comments": _attr_int(attrs, "comments-count"),
            "created_utc": created_utc,
            "is_gallery": is_gallery,
            "over_18": _attr_bool(attrs, "nsfw"),
            "spoiler": _attr_bool(attrs, "spoiler"),
            "is_self": domain.startswith("self."),
            "media_metadata": _extract_gallery_metadata(chunk) if is_gallery else None,
            # `media` / `secure_media` intentionally absent: v.redd.it
            # videos have no DASH manifest URL exposed in listing HTML,
            # so get_video_url routes them through yt-dlp like redgifs.
        }
        posts.append(post)
    return posts

def parse_next_cursor(html):
    """Extract the 'after=t3_<id>' pagination cursor from a listing
    page's 'next ›' link. Returns None when the page has no next link
    (we've hit the end of the listing)."""
    m = re.search(r'class="next-button">\s*<a[^>]+\bhref="[^"]*?after=(t3_[a-z0-9]+)', html)
    return m.group(1) if m else None

def _build_listing_url(args):
    if args.user:
        base = f"https://old.reddit.com/user/{args.user}/submitted/?limit=100&sort={args.sort}"
    else:
        sort_path = "" if args.sort == "hot" else f"{args.sort}/"
        base = f"https://old.reddit.com/r/{args.subreddit}/{sort_path}?limit=100"
    if args.time and args.sort in ("top", "controversial"):
        base += f"&t={args.time}"
    return base

def get_posts(args):
    """Fetch posts from old.reddit.com via HTML scraping."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": ACCEPT_HEADER,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    })
    # NSFW subreddits return an over-18 interstitial without this cookie.
    session.cookies.set("over18", "1")

    base = _build_listing_url(args)
    all_posts = []
    after = None
    count = 0

    while True:
        url = base
        if after:
            url += f"&count={count}&after={after}"

        print(f"Fetching: {url}")
        try:
            r = session.get(url, timeout=30)
        except requests.RequestException as e:
            print(f"Network error: {e}")
            break
        if r.status_code != 200:
            print(f"Error: HTTP {r.status_code}")
            break

        page_posts = parse_reddit_html(r.text)
        if not page_posts:
            print("No posts parsed on this page; stopping.")
            break

        all_posts.extend(page_posts)
        count += len(page_posts)

        if args.limit and len(all_posts) >= args.limit:
            break

        after = parse_next_cursor(r.text)
        if not after:
            break

        time.sleep(API_DELAY)

    # Filter by date (uses created_utc which we populated from data-timestamp)
    if args.after or args.before:
        from datetime import datetime
        filtered = []
        for post in all_posts:
            created = post.get("created_utc") or 0
            post_date = datetime.utcfromtimestamp(created)
            if args.after:
                after_dt = datetime.strptime(args.after, "%Y-%m-%d")
                if post_date < after_dt:
                    continue
            if args.before:
                before_dt = datetime.strptime(args.before, "%Y-%m-%d")
                if post_date > before_dt:
                    continue
            filtered.append(post)
        all_posts = filtered

    if args.limit:
        all_posts = all_posts[:args.limit]

    print(f"Fetched {len(all_posts)} posts")
    return all_posts

def get_image_url(post):
    """Extract direct image URL from post."""
    url = post.get("url", "")
    
    # Direct images
    if url.startswith("https://i.redd.it/"):
        return url, "image", url.split("/")[-1]
    
    # Imgur
    if "imgur.com" in url and not url.endswith(".gifv"):
        img_id = url.split("/")[-1].split(".")[0]
        ext = "jpg"
        if url.endswith(".png"):
            ext = "png"
        elif url.endswith(".gif"):
            ext = "gif"
        elif url.endswith(".gifv"):
            ext = "gif"
            return f"https://i.imgur.com/{img_id}.gif", "gif", f"{img_id}.gif"
        return f"https://i.imgur.com/{img_id}.{ext}", "image", f"{img_id}.{ext}"
    
    # Gallery
    if post.get("is_gallery"):
        metadata = post.get("media_metadata", {})
        images = []
        for item in metadata.values():
            if item.get("status") == "ready":
                img_url = item.get("s", {}).get("u", "").replace("&amp;", "&")
                if img_url:
                    images.append(img_url)
        return images, "gallery", None
    
    return None, None, None

def get_video_url(post):
    """Extract video/GIF URL from post. The returned URL is what gets
    downloaded; the caller decides whether to use yt-dlp or a direct
    HTTP GET based on URL shape."""
    url = post.get("url", "")

    # v.redd.it — HTML scraping doesn't give us the DASH manifest URL,
    # so we hand the watch URL to yt-dlp the same way we do for redgifs.
    if "v.redd.it" in url:
        return url, "video"

    # redgifs
    if "redgifs.com" in url:
        return url, "video"

    # gfycat
    if "gfycat.com" in url:
        return url, "gif"

    # imgur gifv
    if "imgur.com" in url and url.endswith(".gifv"):
        img_id = url.split("/")[-1].replace(".gifv", "")
        return f"https://i.imgur.com/{img_id}.gif", "gif"

    # Direct mp4/gif
    if url.endswith(".mp4") or url.endswith(".gif"):
        return url, "video" if url.endswith(".mp4") else "gif"

    return None, None

def is_image_ext(url):
    return any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"])

def is_video_ext(url):
    return any(url.lower().endswith(ext) for ext in [".mp4", ".gif", ".webm"])

def download_file(url, path, session):
    """Download a single file."""
    try:
        r = session.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def _ytdlp_command(url, path):
    """Builds the yt-dlp argv. v.redd.it URLs redirect to a Reddit
    comments page that requires logged-in cookies to load the video's
    DASH manifest — yt-dlp's --cookies-from-browser pulls them straight
    from a browser keychain. Default is safari (Mac default); override
    with REDDIT_COOKIES_BROWSER=chrome|firefox|brave|edge|vivaldi.
    Browsers without an existing Reddit login session won't help.
    Cookies are domain-scoped so we can safely pass them for all URLs
    — redgifs/gfycat etc. won't receive Reddit cookies."""
    ytdlp = os.environ.get("YTDLP_PATH", "yt-dlp")
    argv = [ytdlp, "-o", str(path), "--no-warnings"]
    browser = os.environ.get("REDDIT_COOKIES_BROWSER", "safari")
    if browser and browser.lower() != "none":
        argv += ["--cookies-from-browser", browser]
    argv.append(url)
    return argv

def download_with_ytdlp(url, path):
    """Download video using yt-dlp. Surfaces yt-dlp's stderr on failure
    instead of swallowing it — Reddit auth errors and extractor breakage
    are the two most common failure modes and the message tells you
    which it is."""
    import subprocess
    try:
        subprocess.run(
            _ytdlp_command(url, path),
            capture_output=True, text=True, timeout=120, check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        err = (e.stderr or "").strip() or (e.stdout or "").strip() or f"exit {e.returncode}"
        if len(err) > 600:
            err = err[:600] + "..."
        print(f"yt-dlp error for {url}:\n  {err}")
    except subprocess.TimeoutExpired:
        print(f"yt-dlp timeout (>120s) for {url}")
    except FileNotFoundError:
        print(f"yt-dlp not found on PATH (set YTDLP_PATH to override)")
    except Exception as e:
        print(f"yt-dlp error for {url}: {e}")
    return False

def process_post(post, dirs, args):
    """Process a single post - returns list of downloaded files."""
    post_id = post.get("id", "unknown")
    subreddit = post.get("subreddit", "unknown")
    target = args.user or subreddit
    downloaded = []
    
    urls_to_download = []
    
    # Images
    if args.images:
        img_urls, img_type, _ = get_image_url(post)
        if img_type == "gallery" and isinstance(img_urls, list):
            for i, img_url in enumerate(img_urls):
                ext = Path(img_url).suffix or ".jpg"
                filename = f"{target}_{post_id}_gallery_{i}{ext}"
                urls_to_download.append((img_url, dirs["pictures"] / filename, False))
        elif img_urls:
            ext = Path(img_urls).suffix or ".jpg"
            filename = f"{target}_{post_id}{ext}"
            urls_to_download.append((img_urls, dirs["pictures"] / filename, False))
    
    # Videos/GIFs
    if args.gifs:
        video_url, video_type = get_video_url(post)
        if video_url:
            if any(h in video_url for h in ("redgifs.com", "gfycat.com", "v.redd.it")):
                # Use yt-dlp for these — watch-page URLs that need
                # extractor logic to resolve to a streamable file.
                filename = f"{target}_{post_id}.mp4"
                urls_to_download.append((video_url, dirs["videos"] / filename, True))
            elif is_video_ext(video_url):
                ext = Path(video_url).suffix or ".mp4"
                filename = f"{target}_{post_id}{ext}"
                urls_to_download.append((video_url, dirs["videos"] / filename, True))
    
    # Download
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    
    for url, path, use_ytdlp in urls_to_download:
        if args.skip_existing and path.exists():
            print(f"Skipping existing: {path.name}")
            continue
        
        print(f"  Downloading: {url[:60]}...")
        
        success = False
        if use_ytdlp:
            success = download_with_ytdlp(url, path)
        else:
            success = download_file(url, path, session)
        
        if success:
            downloaded.append(str(path))
    
    return downloaded

def main():
    args = parse_args()
    
    output_dir = get_output_dir(args)
    ensure_dir(output_dir)
    ensure_dir(output_dir / "Pictures")
    ensure_dir(output_dir / "Videos")
    
    dirs = {
        "pictures": output_dir / "Pictures",
        "videos": output_dir / "Videos"
    }
    
    print(f"Output: {output_dir}")
    print(f"Fetching posts...")
    
    posts = get_posts(args)
    print(f"Processing {len(posts)} posts...")
    
    all_downloaded = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_post, post, dirs, args): post for post in posts}
        for future in as_completed(futures):
            try:
                downloaded = future.result()
                all_downloaded.extend(downloaded)
            except Exception as e:
                print(f"Error processing post: {e}")
    
    print(f"\nDone! Downloaded {len(all_downloaded)} files to {output_dir}")

if __name__ == "__main__":
    main()
