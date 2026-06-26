#!/usr/bin/env python3
"""
Fetch tweets from all followed accounts within the last N hours and save
structured facts to JSON.

Primary mode:
    python fetch_digest.py --hours 24 --output digest.json --json-only

Notion sync mode:
    python fetch_digest.py --sync-only --notion-markdown-input digest.md

Requires: twitter-cli installed and authenticated.
Optional: Notion sync via Notion API key in ~/.config/notion/api_key

Primary responsibility: objective data collection and Notion sync.
Subjective ranking, topic grouping, and final Chinese editing belong to the
agent/model that reads the JSON output.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib import error, request
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_NOTION_PARENT_PAGE_ID = "323dfb80-f233-811a-b597-f30cb2013145"
DEFAULT_NOTION_PARENT_PAGE_URL = "https://www.notion.so/323dfb80f233811ab597f30cb2013145"
DEFAULT_NOTION_KEY_PATH = Path.home() / ".config/notion/api_key"
NOTION_VERSION = "2025-09-03"


TWITTER_BIN: Optional[str] = None


def find_twitter_binary() -> str:
    """Locate the twitter CLI binary, checking env var, PATH, and common install locations."""
    global TWITTER_BIN
    if TWITTER_BIN is not None:
        return TWITTER_BIN

    env_bin = os.environ.get("TWITTER_BIN")
    if env_bin and Path(env_bin).is_file():
        TWITTER_BIN = env_bin
        return TWITTER_BIN

    found = shutil.which("twitter")
    if found:
        TWITTER_BIN = found
        return TWITTER_BIN

    fallback_paths = [
        Path.home() / ".local/bin/twitter",
        Path("/opt/homebrew/bin/twitter"),
        Path("/usr/local/bin/twitter"),
    ]
    for p in fallback_paths:
        if p.is_file():
            TWITTER_BIN = str(p)
            return TWITTER_BIN

    print(
        "Error: twitter CLI not found.\n"
        "  Checked: $TWITTER_BIN env var, $PATH, ~/.local/bin/twitter, /opt/homebrew/bin/twitter\n"
        "  Install: uv tool install twitter-cli\n"
        "  Or set:  export TWITTER_BIN=/path/to/twitter",
        file=sys.stderr,
    )
    sys.exit(1)


def run_twitter_cmd(args: List[str], timeout: int = 60) -> Tuple[Optional[Dict], Optional[str]]:
    twitter_bin = find_twitter_binary()
    cmd = [twitter_bin] + args + ["--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            print(f"  [warn] command failed: {twitter_bin} {' '.join(args)}", file=sys.stderr)
            if stderr:
                print(f"         {stderr}", file=sys.stderr)
            return None, stderr or f"exit code {result.returncode}"
        return json.loads(result.stdout), None
    except FileNotFoundError:
        message = (
            f"twitter binary not found at: {twitter_bin}. "
            f"Install with `uv tool install twitter-cli` or set TWITTER_BIN."
        )
        print(
            f"  [error] twitter binary not found at: {twitter_bin}\n"
            f"          Install: uv tool install twitter-cli\n"
            f"          Or set:  export TWITTER_BIN=/path/to/twitter",
            file=sys.stderr,
        )
        return None, message
    except subprocess.TimeoutExpired as e:
        print(f"  [warn] command timed out: {twitter_bin} {' '.join(args)} ({e})", file=sys.stderr)
        return None, f"timeout: {e}"
    except json.JSONDecodeError as e:
        print(f"  [warn] invalid json from: {twitter_bin} {' '.join(args)} ({e})", file=sys.stderr)
        return None, f"invalid json: {e}"


def notion_key() -> Optional[str]:
    if not DEFAULT_NOTION_KEY_PATH.exists():
        return None
    key = DEFAULT_NOTION_KEY_PATH.read_text(encoding="utf-8").strip()
    return key or None


def notion_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def notion_request(method: str, url: str, api_key: str, payload: Optional[Dict] = None) -> Dict:
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(url, data=data, method=method)
    for k, v in notion_headers(api_key).items():
        req.add_header(k, v)
    try:
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        raise RuntimeError(f"Notion API {e.code}: {body}")
    except error.URLError as e:
        raise RuntimeError(f"Notion API unreachable: {e}")


def notion_rich_text(
    text: str,
    *,
    bold: bool = False,
    italic: bool = False,
    code: bool = False,
    href: Optional[str] = None,
) -> Dict:
    item: Dict = {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "strikethrough": False,
            "underline": False,
            "code": code,
            "color": "default",
        },
    }
    if href:
        item["text"]["link"] = {"url": href}
    return item


INLINE_TOKEN_RE = re.compile(r"(\[[^\]]+\]\([^)]+\)|\*\*.+?\*\*|`[^`]+`|https?://[^\s]+)")
HORIZONTAL_RULE_RE = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")


def parse_inline_markdown(text: str) -> List[Dict]:
    parts: List[Dict] = []
    last_end = 0
    for match in INLINE_TOKEN_RE.finditer(text):
        if match.start() > last_end:
            parts.append(notion_rich_text(text[last_end:match.start()]))

        token = match.group(0)
        if token.startswith("**") and token.endswith("**") and len(token) >= 4:
            parts.append(notion_rich_text(token[2:-2], bold=True))
        elif token.startswith("`") and token.endswith("`") and len(token) >= 2:
            parts.append(notion_rich_text(token[1:-1], code=True))
        elif token.startswith("["):
            mid = token.find("](")
            label = token[1:mid]
            href = token[mid + 2:-1]
            if label:
                parts.append(notion_rich_text(label, href=href))
        else:
            parts.append(notion_rich_text(token, href=token))
        last_end = match.end()

    if last_end < len(text):
        parts.append(notion_rich_text(text[last_end:]))

    return parts or [notion_rich_text("")]


def make_notion_block(block_type: str, rich_text: List[Dict], children: Optional[List[Dict]] = None) -> Dict:
    block = {
        "object": "block",
        "type": block_type,
        block_type: {"rich_text": rich_text},
    }
    if children:
        block[block_type]["children"] = children
    return block


def make_divider_block() -> Dict:
    return {
        "object": "block",
        "type": "divider",
        "divider": {},
    }


def make_callout_block(
    rich_text: List[Dict],
    *,
    emoji: str = "💡",
    color: str = "gray_background",
    children: Optional[List[Dict]] = None,
) -> Dict:
    block = {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": rich_text,
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }
    if children:
        block["callout"]["children"] = children
    return block


def make_toggle_block(rich_text: List[Dict], children: Optional[List[Dict]] = None) -> Dict:
    block = {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": rich_text,
            "color": "default",
        },
    }
    if children:
        block["toggle"]["children"] = children
    return block


def rich_text_plain_text(rich_text: List[Dict]) -> str:
    parts: List[str] = []
    for item in rich_text:
        text = ((item.get("text") or {}).get("content")) or ""
        parts.append(text)
    return "".join(parts)


def prepend_rich_text(prefix: str, rich_text: List[Dict]) -> List[Dict]:
    return [notion_rich_text(prefix)] + rich_text


def is_horizontal_rule(text: str) -> bool:
    return bool(HORIZONTAL_RULE_RE.fullmatch(text))


def count_leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def is_numbered_item(text: str) -> bool:
    numbered = text.split(". ", 1)
    return len(numbered) == 2 and numbered[0].isdigit()


def is_structured_block(text: str) -> bool:
    return (
        text.startswith("# ")
        or text.startswith("#### ")
        or text.startswith("### ")
        or text.startswith("## ")
        or text.startswith("- ")
        or text.startswith("> ")
        or is_numbered_item(text)
        or is_horizontal_rule(text)
    )


def normalize_section_title(text: str) -> str:
    title = text.strip().strip(":：")
    title = re.sub(r"[（(][^)）]*[)）]", "", title)
    title = re.sub(r"^[一二三四五六七八九十0-9]+[、.．)）]\s*", "", title)
    title = re.sub(r"^[^\w\u4e00-\u9fff]+", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def is_top_picks_title(text: str) -> bool:
    title = normalize_section_title(text)
    keywords = (
        "最值得看",
        "最重要的 3 条",
        "最重要的3条",
        "今天最值得看的 3 条",
        "今天最值得看的3条",
        "今天最值得看的几条",
        "先看这 3 条",
        "先看这3条",
        "热门推文",
    )
    return any(keyword in title for keyword in keywords)


def is_skip_section_title(text: str) -> bool:
    title = normalize_section_title(text)
    keywords = (
        "可跳过",
        "低优先级",
        "高热度但未必最有料",
        "可低配关注",
        "风险与噪音提醒",
        "噪音提醒",
    )
    return any(keyword in title for keyword in keywords)


def parse_paragraph(lines: List[str], start_idx: int, base_indent: int) -> Tuple[List[Dict], int]:
    chunks: List[str] = []
    i = start_idx
    while i < len(lines):
        raw = lines[i].rstrip()
        if not raw.strip():
            break
        indent = count_leading_spaces(raw)
        stripped = raw[indent:]
        if indent < base_indent:
            break
        if i != start_idx and indent == base_indent and is_structured_block(stripped):
            break
        if i != start_idx and indent > base_indent and is_structured_block(stripped):
            break
        chunks.append(stripped)
        i += 1
    paragraph = " ".join(chunk.strip() for chunk in chunks if chunk.strip())
    return [make_notion_block("paragraph", parse_inline_markdown(paragraph))], i


def parse_markdown_blocks(lines: List[str], start_idx: int = 0, base_indent: int = 0) -> Tuple[List[Dict], int]:
    blocks: List[Dict] = []
    i = start_idx

    while i < len(lines):
        raw = lines[i].rstrip()
        if not raw.strip():
            i += 1
            continue

        indent = count_leading_spaces(raw)
        if indent < base_indent:
            break

        stripped = raw[indent:]

        if is_horizontal_rule(stripped):
            blocks.append(make_divider_block())
            i += 1
            continue
        if stripped.startswith("# "):
            blocks.append(make_notion_block("heading_1", parse_inline_markdown(stripped[2:])))
            i += 1
            continue
        if stripped.startswith("#### "):
            blocks.append(make_notion_block("heading_3", parse_inline_markdown(stripped[5:])))
            i += 1
            continue
        if stripped.startswith("### "):
            blocks.append(make_notion_block("heading_2", parse_inline_markdown(stripped[4:])))
            i += 1
            continue
        if stripped.startswith("## "):
            blocks.append(make_notion_block("heading_1", parse_inline_markdown(stripped[3:])))
            i += 1
            continue
        if stripped.startswith("> "):
            blocks.append(make_notion_block("quote", parse_inline_markdown(stripped[2:])))
            i += 1
            continue
        if stripped.startswith("- "):
            children, next_idx = parse_markdown_blocks(lines, i + 1, indent + 1)
            blocks.append(
                make_notion_block(
                    "bulleted_list_item",
                    parse_inline_markdown(stripped[2:]),
                    children or None,
                )
            )
            i = next_idx
            continue
        if is_numbered_item(stripped):
            content = stripped.split(". ", 1)[1]
            children, next_idx = parse_markdown_blocks(lines, i + 1, indent + 1)
            blocks.append(
                make_notion_block(
                    "numbered_list_item",
                    parse_inline_markdown(content),
                    children or None,
                )
            )
            i = next_idx
            continue

        paragraph_blocks, next_idx = parse_paragraph(lines, i, base_indent)
        blocks.extend(paragraph_blocks)
        i = next_idx

    return blocks, i


def markdown_to_notion_blocks(markdown: str) -> List[Dict]:
    blocks, _ = parse_markdown_blocks(markdown.splitlines())
    styled = stylize_notion_blocks(blocks)
    return styled or [make_notion_block("paragraph", [notion_rich_text("无内容")])]


def stylize_notion_blocks(blocks: List[Dict]) -> List[Dict]:
    if not blocks:
        return blocks

    styled: List[Dict] = []
    current_section = ""
    top_item_index = 0

    for block in blocks:
        block_type = block["type"]

        if block_type in {"heading_1", "heading_2", "heading_3"}:
            heading = block[block_type]
            heading_text = rich_text_plain_text(heading["rich_text"]).strip()
            if block_type == "heading_2" and styled and styled[-1]["type"] != "divider":
                styled.append(make_divider_block())
            current_section = heading_text
            if "3 行" in heading_text and "结论" in heading_text:
                current_section = "3 行结论"
            elif is_top_picks_title(heading_text):
                current_section = "最值得看"
            elif is_skip_section_title(heading_text):
                current_section = "可跳过"
            top_item_index = 0
            styled.append(block)
            continue

        if block_type == "paragraph":
            paragraph = block["paragraph"]
            paragraph_text = rich_text_plain_text(paragraph["rich_text"]).strip()
            if is_top_picks_title(paragraph_text):
                current_section = "最值得看"
                top_item_index = 0
                styled.append(make_notion_block("heading_2", paragraph["rich_text"]))
                continue
            if paragraph_text.startswith("结论：") or paragraph_text.startswith("结论:"):
                styled.append(
                    make_callout_block(
                        paragraph["rich_text"],
                        emoji="💡",
                        color="blue_background",
                    )
                )
                continue

        if current_section == "3 行结论" and block_type in {"bulleted_list_item", "numbered_list_item"}:
            item = block[block_type]
            styled.append(
                make_callout_block(
                    item["rich_text"],
                    emoji="💡",
                    color="blue_background",
                    children=item.get("children"),
                )
            )
            continue

        if current_section == "最值得看" and block_type == "numbered_list_item":
            top_item_index += 1
            item = block["numbered_list_item"]
            styled.append(
                make_toggle_block(
                    prepend_rich_text(f"{top_item_index}. ", item["rich_text"]),
                    item.get("children"),
                )
            )
            continue

        if current_section == "可跳过" and block_type == "bulleted_list_item":
            item = block["bulleted_list_item"]
            styled.append(
                make_callout_block(
                    item["rich_text"],
                    emoji="⏭️",
                    color="gray_background",
                    children=item.get("children"),
                )
            )
            continue

        styled.append(block)

    return styled


def create_notion_page(api_key: str, title: str, parent_page_id: str, children: List[Dict]) -> Dict:
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title,
                        }
                    }
                ]
            }
        },
        "icon": {"type": "emoji", "emoji": "📰"},
        "children": children,
    }
    return notion_request("POST", "https://api.notion.com/v1/pages", api_key, payload)


NOTION_MAX_CHILDREN = 100
NOTION_SAFE_CHILDREN = 90


def notion_block_count(markdown: str) -> int:
    stripped = markdown.strip()
    if not stripped:
        return 0
    return len(markdown_to_notion_blocks(stripped + "\n"))


def split_markdown_for_notion(markdown: str) -> List[Tuple[str, str]]:
    lines = markdown.splitlines()
    sections: List[Tuple[str, List[str]]] = []
    current_title = "总览"
    current_lines: List[str] = []

    for line in lines:
        if (line.startswith("## ") or line.startswith("### ")) and current_lines:
            sections.append((current_title, current_lines))
            current_title = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_title, current_lines))

    pages: List[Tuple[str, str]] = []
    page_index = 1
    current_page_title = "总览"
    current_page_lines: List[str] = []
    current_block_budget = 0

    for section_title, section_lines in sections:
        section_md = "\n".join(section_lines).strip() + "\n"
        section_block_count = notion_block_count(section_md)

        tentative_page_md = "\n".join(current_page_lines + section_lines).strip() + "\n"
        tentative_page_blocks = notion_block_count(tentative_page_md)
        if current_page_lines and tentative_page_blocks > NOTION_SAFE_CHILDREN:
            pages.append((current_page_title or f"第{page_index}部分", "\n".join(current_page_lines).strip() + "\n"))
            page_index += 1
            current_page_lines = []
            current_block_budget = 0
            current_page_title = section_title

        if section_block_count > NOTION_SAFE_CHILDREN:
            chunk_lines: List[str] = []
            chunk_budget = 0
            chunk_no = 1
            for line in section_lines:
                tentative_chunk_md = "\n".join(chunk_lines + [line]).strip() + "\n"
                tentative_chunk_blocks = notion_block_count(tentative_chunk_md)
                if chunk_lines and tentative_chunk_blocks > NOTION_SAFE_CHILDREN:
                    pages.append((f"{section_title}（{chunk_no}）", "\n".join(chunk_lines).strip() + "\n"))
                    chunk_no += 1
                    chunk_lines = []
                    chunk_budget = 0
                chunk_lines.append(line)
                chunk_budget = notion_block_count("\n".join(chunk_lines).strip() + "\n")
            if chunk_lines:
                pages.append((f"{section_title}（{chunk_no}）", "\n".join(chunk_lines).strip() + "\n"))
            current_page_lines = []
            current_block_budget = 0
            current_page_title = ""
            continue

        current_page_lines.extend(section_lines)
        current_block_budget = notion_block_count("\n".join(current_page_lines).strip() + "\n")
        if not current_page_title:
            current_page_title = section_title

    if current_page_lines:
        pages.append((current_page_title or f"第{page_index}部分", "\n".join(current_page_lines).strip() + "\n"))

    return pages or [("总览", markdown)]


def sync_to_notion(markdown: str, title: str, parent_page_id: str) -> str:
    api_key = notion_key()
    if not api_key:
        raise RuntimeError(f"Notion API key not found at {DEFAULT_NOTION_KEY_PATH}")

    blocks = markdown_to_notion_blocks(markdown)
    if len(blocks) <= NOTION_MAX_CHILDREN:
        response = create_notion_page(api_key, title, parent_page_id, blocks)
        return response.get("url") or DEFAULT_NOTION_PARENT_PAGE_URL

    parts = split_markdown_for_notion(markdown)
    created_pages = []
    for idx, (part_title, part_md) in enumerate(parts, 1):
        part_blocks = markdown_to_notion_blocks(part_md)
        response = create_notion_page(api_key, f"{title}（{idx}/{len(parts)} {part_title}）", parent_page_id, part_blocks)
        created_pages.append((response.get("url") or DEFAULT_NOTION_PARENT_PAGE_URL, part_title))

    directory_lines = [f"## {title}", "", "本页为自动拆分页目录。", ""]
    for idx, (url, part_title) in enumerate(created_pages, 1):
        directory_lines.append(f"- [{title}（{idx}/{len(created_pages)} {part_title}）]({url})")
    directory_blocks = markdown_to_notion_blocks("\n".join(directory_lines) + "\n")
    directory = create_notion_page(api_key, title, parent_page_id, directory_blocks)
    return directory.get("url") or (created_pages[0][0] if created_pages else DEFAULT_NOTION_PARENT_PAGE_URL)


def get_username() -> Tuple[Optional[str], Optional[str]]:
    data, error_message = run_twitter_cmd(["whoami"])
    if error_message:
        return None, error_message
    if data and data.get("ok"):
        return data["data"]["user"]["screenName"], None
    return None, "unexpected response from twitter whoami"


def get_following(username: str) -> Tuple[List[Dict], Optional[str]]:
    data, error_message = run_twitter_cmd(["following", username, "--max", "200"], timeout=120)
    if error_message:
        return [], error_message
    if data and data.get("ok"):
        return data["data"], None
    return [], "unexpected response from twitter following"


def get_user_posts(screen_name: str, max_count: int = 10) -> Tuple[List[Dict], Optional[str]]:
    data, error_message = run_twitter_cmd(
        ["user-posts", screen_name, "--max", str(max_count), "--full-text"],
        timeout=60,
    )
    if error_message:
        return [], error_message
    if data and data.get("ok"):
        return data["data"], None
    return [], "unexpected response from twitter user-posts"


def parse_twitter_time(time_str: str) -> Optional[datetime]:
    try:
        return datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y")
    except (ValueError, TypeError):
        return None


def to_local_string(dt: Optional[datetime]) -> str:
    if not dt:
        return "未知时间"
    return dt.astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M")


def local_day_string(dt: datetime) -> str:
    return dt.astimezone(LOCAL_TZ).strftime("%Y-%m-%d")


def filter_recent(tweets: List[Dict], cutoff: datetime) -> List[Dict]:
    recent = []
    for t in tweets:
        created = parse_twitter_time(t.get("createdAt", ""))
        if created and created >= cutoff:
            t = dict(t)
            t["createdAtLocal"] = to_local_string(created)
            t["createdAtTs"] = created.timestamp()
            t["url"] = tweet_url(t)
            recent.append(t)
    return recent


def tweet_url(tweet: Dict) -> str:
    author = tweet.get("author", {}) or {}
    screen_name = author.get("screenName", "unknown")
    tweet_id = tweet.get("id", "")
    return f"https://x.com/{screen_name}/status/{tweet_id}"


def collect_accounts_from_following(following: List[Dict]) -> List[Dict]:
    accounts = []
    for user in following:
        accounts.append(
            {
                "name": user.get("name", ""),
                "screenName": user.get("screenName", ""),
                "description": user.get("description", ""),
            }
        )
    accounts.sort(key=lambda x: (x.get("screenName") or "").lower())
    return accounts


def summarize_accounts_with_tweets(tweets: List[Dict]) -> List[Dict]:
    by_author: Dict[str, Dict] = {}
    for tweet in tweets:
        author = tweet.get("author", {}) or {}
        sn = author.get("screenName")
        if not sn:
            continue
        item = by_author.setdefault(
            sn,
            {
                "screenName": sn,
                "name": author.get("name", ""),
                "tweetCount": 0,
                "latestTweetAtTs": 0,
                "latestTweetAtLocal": "未知时间",
                "latestTweetUrl": "",
            },
        )
        item["tweetCount"] += 1
        created_ts = tweet.get("createdAtTs", 0) or 0
        if created_ts >= item["latestTweetAtTs"]:
            item["latestTweetAtTs"] = created_ts
            item["latestTweetAtLocal"] = tweet.get("createdAtLocal", "未知时间")
            item["latestTweetUrl"] = tweet.get("url", "")
    return sorted(by_author.values(), key=lambda x: (-x["tweetCount"], -x["latestTweetAtTs"], x["screenName"].lower()))


def load_markdown_override(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Fetch Twitter facts to JSON or sync an existing Markdown file to Notion")
    parser.add_argument("--hours", type=int, default=24, help="Look back N hours (default: 24)")
    parser.add_argument("--max-per-user", type=int, default=10, help="Max tweets to fetch per user (default: 10)")
    parser.add_argument("--output", "-o", type=str, default="", help="Save JSON to file")
    parser.add_argument("--notion-parent-page-id", type=str, default=DEFAULT_NOTION_PARENT_PAGE_ID, help="Notion parent page id")
    parser.add_argument("--notion-markdown-input", type=str, default="", help="Use this Markdown file as the Notion content source (for translated/edited output)")
    parser.add_argument("--notion-title", type=str, default="", help="Override Notion page title")
    parser.add_argument("--users", type=str, default="", help="Comma-separated usernames (skip auto-detect)")
    parser.add_argument("--sample-size", type=int, default=0, help="Only use the first N accounts from the detected/provided list (for testing)")
    parser.add_argument("--twitter-bin", type=str, default="", help="Path to the twitter CLI binary (default: auto-detect)")
    parser.add_argument("--json-only", action="store_true", help="Explicitly request facts-only JSON output (same behavior as the default fetch mode)")
    parser.add_argument("--sync-only", action="store_true", help="Only sync an existing Markdown file to Notion; skip Twitter fetching")
    args = parser.parse_args()

    if args.twitter_bin:
        global TWITTER_BIN
        TWITTER_BIN = args.twitter_bin

    if args.json_only and args.sync_only:
        print("Error: --json-only and --sync-only cannot be used together.", file=sys.stderr)
        sys.exit(1)

    if args.notion_markdown_input and not args.sync_only:
        print(
            "Error: --notion-markdown-input is only supported together with --sync-only.",
            file=sys.stderr,
        )
        sys.exit(1)

    now = datetime.now(timezone.utc)

    if args.sync_only:
        if not args.notion_markdown_input:
            print("Error: --sync-only requires --notion-markdown-input <file>.", file=sys.stderr)
            sys.exit(1)
        notion_title = args.notion_title or local_day_string(now)
        notion_url = sync_to_notion(
            markdown=load_markdown_override(args.notion_markdown_input),
            title=notion_title,
            parent_page_id=args.notion_parent_page_id,
        )
        print(f"Synced to Notion: {notion_url}", file=sys.stderr)
        return

    cutoff = now - timedelta(hours=args.hours)

    if args.users:
        screen_names = [u.strip().lstrip("@") for u in args.users.split(",") if u.strip()]
        following = [{"screenName": sn, "name": sn, "description": ""} for sn in screen_names]
        print(f"Using provided user list: {len(screen_names)} accounts", file=sys.stderr)
    else:
        print("Detecting current user...", file=sys.stderr)
        username, username_error = get_username()
        if not username:
            detail = username_error or "Is twitter-cli authenticated?"
            print(f"Error: could not detect Twitter username. {detail}", file=sys.stderr)
            sys.exit(1)
        print(f"Logged in as @{username}", file=sys.stderr)

        print("Fetching following list...", file=sys.stderr)
        following, following_error = get_following(username)
        if following_error:
            print(f"Error: could not fetch following list. {following_error}", file=sys.stderr)
            sys.exit(1)
        screen_names = [u["screenName"] for u in following if u.get("screenName")]
        print(f"Following {len(screen_names)} accounts", file=sys.stderr)

    if args.sample_size and args.sample_size > 0:
        screen_names = screen_names[: args.sample_size]
        following = [u for u in following if u.get("screenName") in set(screen_names)]
        print(f"Sampling first {len(screen_names)} accounts for this run", file=sys.stderr)

    accounts = collect_accounts_from_following(following)
    all_tweets = []
    failed_accounts = []
    for i, sn in enumerate(screen_names, 1):
        print(f"  [{i}/{len(screen_names)}] Fetching @{sn}...", file=sys.stderr)
        posts, post_error = get_user_posts(sn, args.max_per_user)
        if post_error:
            failed_accounts.append({"screenName": sn, "error": post_error})
            print(f"    -> failed: {post_error}", file=sys.stderr)
            continue
        recent = filter_recent(posts, cutoff)
        if recent:
            print(f"    -> {len(recent)} tweets in last {args.hours}h", file=sys.stderr)
        all_tweets.extend(recent)

    all_tweets.sort(key=lambda t: t.get("createdAtTs", 0), reverse=True)

    accounts_with_tweets = summarize_accounts_with_tweets(all_tweets)
    result = {
        "ok": True,
        "generated_at": now.isoformat(),
        "generated_at_local": to_local_string(now),
        "hours": args.hours,
        "total_accounts": len(accounts),
        "active_accounts": len(accounts_with_tweets),
        "total_tweets": len(all_tweets),
        "requested_accounts": screen_names,
        "failed_accounts": failed_accounts,
        "accounts": accounts,
        "accounts_with_recent_tweets": accounts_with_tweets,
        "tweets": all_tweets,
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_json, encoding="utf-8")
        print(f"\nSaved {len(all_tweets)} tweets to {output_path}", file=sys.stderr)
    else:
        print(output_json)

    print(
        f"\nDone: {len(all_tweets)} tweets from {len(screen_names)} accounts in the last {args.hours}h",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
