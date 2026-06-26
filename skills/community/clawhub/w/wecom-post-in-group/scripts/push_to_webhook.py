#!/usr/bin/env python3
"""
Push content to a WeChat Work (企业微信) webhook.

Usage:
    python3 push_to_webhook.py --webhook <URL_OR_KEY> --format <markdown|text> --message <CONTENT>
    python3 push_to_webhook.py --webhook <URL_OR_KEY> --format markdown --file <FILE_PATH>

Options:
    --webhook   Webhook URL or key (required)
    --format    Message format: 'markdown' or 'text' (default: markdown)
    --message   Message content as string
    --file      Read message content from file
    --mention   Mention users (comma-separated user IDs, or '@all')
    --split     Auto-split long messages (for markdown: 4096 bytes limit)

Examples:
    python3 push_to_webhook.py --webhook "adeee643-..." --format markdown --message "# Hello\\nWorld"
    python3 push_to_webhook.py --webhook "adeee643-..." --format text --message "Hello" --mention "@all"
    python3 push_to_webhook.py --webhook "adeee643-..." --format markdown --file report.md
"""

import sys
import re
import json
import argparse
import urllib.request
import urllib.error

WEBHOOK_BASE = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)
URL_PATTERN = re.compile(
    r'^https://qyapi\.weixin\.qq\.com/cgi-bin/webhook/send\?key=([0-9a-f-]+)$',
    re.IGNORECASE
)

# WeChat Work limits
MARKDOWN_MAX_BYTES = 4096
TEXT_MAX_BYTES = 2048


def resolve_webhook_url(input_str: str) -> str:
    """Resolve webhook input to full URL."""
    input_str = input_str.strip()
    if URL_PATTERN.match(input_str):
        return input_str
    if UUID_PATTERN.match(input_str):
        return f"{WEBHOOK_BASE}{input_str}"
    raise ValueError(f"Invalid webhook: {input_str}")


def split_content(content: str, max_bytes: int) -> list[str]:
    """Split content into chunks that fit within byte limit."""
    chunks = []
    current = ""

    for line in content.split('\n'):
        test = current + ('\n' if current else '') + line
        if len(test.encode('utf-8')) > max_bytes:
            if current:
                chunks.append(current)
            current = line
        else:
            current = test

    if current:
        chunks.append(current)

    return chunks if chunks else [content]


def send_message(url: str, payload: dict) -> dict:
    """Send a message to the webhook."""
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"errcode": e.code, "errmsg": f"HTTP Error: {e.reason}"}
    except urllib.error.URLError as e:
        return {"errcode": -1, "errmsg": f"Connection Error: {e.reason}"}
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}


def push_markdown(url: str, content: str, auto_split: bool = False) -> list[dict]:
    """Push markdown content, optionally splitting if too long."""
    results = []

    if auto_split and len(content.encode('utf-8')) > MARKDOWN_MAX_BYTES:
        chunks = split_content(content, MARKDOWN_MAX_BYTES)
        for i, chunk in enumerate(chunks):
            payload = {"msgtype": "markdown", "markdown": {"content": chunk}}
            result = send_message(url, payload)
            result["chunk"] = f"{i+1}/{len(chunks)}"
            results.append(result)
    else:
        payload = {"msgtype": "markdown", "markdown": {"content": content}}
        results.append(send_message(url, payload))

    return results


def push_text(url: str, content: str, mentions: list[str] = None, auto_split: bool = False) -> list[dict]:
    """Push text content with optional mentions."""
    results = []
    text_body = {"content": content}

    if mentions:
        if "@all" in mentions:
            text_body["mentioned_list"] = ["@all"]
        else:
            text_body["mentioned_list"] = mentions

    if auto_split and len(content.encode('utf-8')) > TEXT_MAX_BYTES:
        chunks = split_content(content, TEXT_MAX_BYTES)
        for i, chunk in enumerate(chunks):
            body = {"content": chunk}
            if mentions and i == 0:  # Only mention in first chunk
                body.update({k: v for k, v in text_body.items() if k != "content"})
            payload = {"msgtype": "text", "text": body}
            result = send_message(url, payload)
            result["chunk"] = f"{i+1}/{len(chunks)}"
            results.append(result)
    else:
        payload = {"msgtype": "text", "text": text_body}
        results.append(send_message(url, payload))

    return results


def main():
    parser = argparse.ArgumentParser(description="Push content to WeChat Work webhook")
    parser.add_argument("--webhook", required=True, help="Webhook URL or key")
    parser.add_argument("--format", choices=["markdown", "text"], default="markdown",
                        help="Message format (default: markdown)")
    parser.add_argument("--message", help="Message content")
    parser.add_argument("--file", help="Read message from file")
    parser.add_argument("--mention", help="Mention users (comma-separated, or @all)")
    parser.add_argument("--split", action="store_true", help="Auto-split long messages")

    args = parser.parse_args()

    # Resolve webhook
    try:
        url = resolve_webhook_url(args.webhook)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # Get content
    content = None
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
    elif args.message:
        content = args.message
    else:
        # Read from stdin
        content = sys.stdin.read()

    if not content or not content.strip():
        print("❌ No content provided. Use --message, --file, or pipe via stdin.")
        sys.exit(1)

    # Parse mentions
    mentions = None
    if args.mention:
        mentions = [m.strip() for m in args.mention.split(",")]

    # Send
    content_bytes = len(content.encode('utf-8'))
    print(f"📤 Pushing {args.format} message ({content_bytes} bytes)...")

    if args.format == "markdown":
        results = push_markdown(url, content, auto_split=args.split)
    else:
        results = push_text(url, content, mentions=mentions, auto_split=args.split)

    # Report results
    all_ok = True
    for r in results:
        chunk_info = f" [chunk {r.get('chunk', '1/1')}]" if r.get("chunk") else ""
        if r.get("errcode") == 0:
            print(f"✅ Sent successfully{chunk_info}")
        else:
            print(f"❌ Failed{chunk_info}: {json.dumps(r, ensure_ascii=False)}")
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
