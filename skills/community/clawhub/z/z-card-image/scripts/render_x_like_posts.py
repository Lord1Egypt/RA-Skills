#!/usr/bin/env python3
"""
render_x_like_posts.py — 将多条帖子渲染为一张 X-like 风格长图 PNG

推荐用法:
  python3 render_x_like_posts.py \
    --author "OpenAI" \
    --handle "@OpenAI" \
    --post "第一条帖子" \
    --post "第二条帖子" \
    --out /path/to/workspace/tmp/x-like-posts.png

也支持:
  --posts-file posts.json

posts.json 格式:
  ["post one", "post two"]
  或
  [{"text": "post one"}, {"text": "post two"}]
"""

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

SKILL_DIR = Path(__file__).parent.parent
TEMPLATE_PATH = SKILL_DIR / "assets" / "templates" / "x-like-posts.html"
ICONS_DIR = SKILL_DIR / "assets" / "icons"
FONTS_DIR = SKILL_DIR / "assets" / "fonts"

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
]

WIDTH = 900
MIN_HEIGHT = 1200
MAX_HEIGHT = 16000
TEXT_WIDTH_CHARS = 26
DISPLAY_TZ = ZoneInfo("Asia/Shanghai")
DISPLAY_TZ_LABEL = "UTC+8"


def find_chrome():
    for path in CHROME_PATHS:
        if Path(path).exists() or shutil.which(path):
            return path
    return None


def weighted_length(text: str) -> float:
    total = 0.0
    for ch in text:
        if ch == "\n":
            total += 8.0
        elif ord(ch) < 128:
            total += 0.55
        else:
            total += 1.0
    return total


def estimate_post_height(text: str) -> int:
    paragraphs = [p for p in text.splitlines() if p.strip()] or [text]
    wrapped_lines = 0
    for paragraph in paragraphs:
        logical_lines = max(1, math.ceil(weighted_length(paragraph) / TEXT_WIDTH_CHARS))
        wrapped_lines += logical_lines
    wrapped_lines += max(0, len(paragraphs) - 1)
    return 120 + wrapped_lines * 48


def estimate_canvas_height(posts: Iterable[str]) -> int:
    total = 210
    for post in posts:
        total += estimate_post_height(post) + 20
    return max(MIN_HEIGHT, min(MAX_HEIGHT, total + 120))


def load_posts(args) -> list[dict]:
    posts = []
    raw_posts = list(args.post) + list(args.tweet)
    if raw_posts:
        posts.extend([{"text": text.strip()} for text in raw_posts if text.strip()])

    input_file = args.posts_file or args.tweets_file
    if input_file:
        raw = Path(input_file).read_text(encoding="utf-8")
        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            sys.exit("posts file must be a JSON array")
        for item in parsed:
            if isinstance(item, str) and item.strip():
                posts.append({"text": item.strip()})
            elif isinstance(item, dict) and str(item.get("text", "")).strip():
                posts.append(
                    {
                        "text": str(item["text"]).strip(),
                        "created_at": str(item.get("created_at", "")).strip(),
                        "url": str(item.get("url", "")).strip(),
                        "favorite_count": item.get("favorite_count", 0),
                        "retweet_count": item.get("retweet_count", 0),
                    }
                )

    if not posts:
        sys.exit("需要至少一条帖子：传 --post/--tweet 或 --posts-file/--tweets-file")

    return posts


def text_to_html(text: str) -> str:
    parts = []
    for block in text.splitlines():
        if not block.strip():
            continue
        parts.append(f"<p>{escape(block)}</p>")
    return "".join(parts) if parts else f"<p>{escape(text)}</p>"


def parse_created_at(created_at: str):
    if not created_at:
        return None
    try:
        return datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_created_at(created_at: str) -> str:
    if not created_at:
        return ""
    dt = parse_created_at(created_at)
    if not dt:
        return created_at
    local_dt = dt.astimezone(DISPLAY_TZ)
    return local_dt.strftime(f"%Y-%m-%d %H:%M {DISPLAY_TZ_LABEL}")


def build_date_label(posts: list[dict]) -> str:
    created_times = []
    for post in posts:
        dt = parse_created_at(str(post.get("created_at", "")).strip())
        if dt:
            created_times.append(dt.astimezone(DISPLAY_TZ))
    if not created_times:
        return "日期未知"

    created_times.sort(reverse=True)
    return created_times[0].strftime("%Y-%m-%d")


def to_int(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def build_stats(post: dict) -> str:
    parts = []
    created_at = format_created_at(str(post.get("created_at", "")).strip())
    if created_at:
        parts.append(f'<span class="stat">{escape(created_at)}</span>')

    repost_count = to_int(post.get("retweet_count", 0))
    favorite_count = to_int(post.get("favorite_count", 0))
    if repost_count > 0:
        parts.append(f'<span class="stat"><strong>{repost_count}</strong> RT</span>')
    if favorite_count > 0:
        parts.append(f'<span class="stat"><strong>{favorite_count}</strong> Likes</span>')

    if str(post.get("url", "")).strip():
        parts.append('<span class="stat">x.com</span>')

    return "".join(parts) if parts else '<span class="stat">Forwarded from X</span>'


def build_post_items(posts: list[dict], author: str, handle: str, avatar_path: str) -> str:
    total = len(posts)
    items = []
    for index, post in enumerate(posts, 1):
        text = str(post.get("text", "")).strip()
        items.append(
            f"""
<article class="tweet">
  <div class="avatar-wrap">
    <img src="{avatar_path}" alt="avatar">
  </div>
  <div class="tweet-main">
    <div class="tweet-top">
      <span class="name">{escape(author)}</span>
      <span class="handle">{escape(handle)}</span>
      <span class="meta">· Post</span>
    </div>
    <div class="tweet-text">{text_to_html(text)}</div>
    <div class="tweet-footer">
      <span class="tweet-index">{index} / {total}</span>
      <span class="tweet-stats">{build_stats(post)}</span>
    </div>
  </div>
</article>
""".strip()
        )
    return "\n".join(items)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--author", default="Unknown Author")
    ap.add_argument("--handle", default="@twitter")
    ap.add_argument("--post", action="append", default=[], help="单条帖子内容，可重复传入")
    ap.add_argument("--posts-file", default="", help="JSON 数组文件，元素为字符串或 {text}")
    ap.add_argument("--tweet", action="append", default=[], help="兼容旧参数：单条推文内容，可重复传入")
    ap.add_argument("--tweets-file", default="", help="兼容旧参数：JSON 数组文件，元素为字符串或 {text}")
    ap.add_argument("--header-label", default="X-like 帖子分享图")
    ap.add_argument("--footer", default="整理转发 · via z-card-image")
    ap.add_argument("--bg", default="#f5f8fa")
    ap.add_argument("--card-bg", default="#ffffff")
    ap.add_argument("--text", default="#0f1419")
    ap.add_argument("--muted", default="#536471")
    ap.add_argument("--border", default="#e6ecf0")
    ap.add_argument("--accent", default="#1d9bf0")
    ap.add_argument("--avatar", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    chrome = find_chrome()
    if not chrome:
        sys.exit("Chrome/Chromium not found")

    posts = load_posts(args)
    avatar_path = args.avatar or str(ICONS_DIR / "avatar_jinx_cartoon.jpg")
    font_path = str(FONTS_DIR / "AlimamaShuHeiTi-Bold.ttf")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    post_items = build_post_items(posts, args.author, args.handle, avatar_path)
    replacements = {
        "{{BG_COLOR}}": args.bg,
        "{{CARD_BG}}": args.card_bg,
        "{{TEXT_COLOR}}": args.text,
        "{{MUTED_COLOR}}": args.muted,
        "{{BORDER_COLOR}}": args.border,
        "{{ACCENT_COLOR}}": args.accent,
        "{{AUTHOR_NAME}}": escape(args.author),
        "{{AUTHOR_HANDLE}}": escape(args.handle),
        "{{AUTHOR_AVATAR}}": avatar_path,
        "{{HEADER_LABEL}}": escape(args.header_label),
        "{{TIME_RANGE_LABEL}}": escape(build_date_label(posts)),
        "{{FOOTER_TEXT}}": escape(args.footer),
        "{{FONT_PATH}}": font_path,
        "{{TWEET_ITEMS}}": post_items,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)

    height = estimate_canvas_height([str(post.get("text", "")) for post in posts])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as handle:
        handle.write(template)
        tmp_html = handle.name

    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--window-size={WIDTH},{height}",
        f"--screenshot={out}",
        f"file://{tmp_html}",
    ]
    result = subprocess.run(cmd, capture_output=True)
    Path(tmp_html).unlink(missing_ok=True)
    if result.returncode != 0:
        sys.exit(f"Chrome failed:\n{result.stderr.decode()}")

    print(f"✅ Saved to {out}")


if __name__ == "__main__":
    main()
