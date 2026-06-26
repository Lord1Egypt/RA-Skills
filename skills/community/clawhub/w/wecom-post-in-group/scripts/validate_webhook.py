#!/usr/bin/env python3
"""
Validate a WeChat Work (企业微信) webhook URL or key.

Usage:
    python3 validate_webhook.py <webhook_url_or_key>

Examples:
    python3 validate_webhook.py "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=adeee643-bc8e-4ad1-bb52-83001cd5986e"
    python3 validate_webhook.py "adeee643-bc8e-4ad1-bb52-83001cd5986e"

Exit codes:
    0 - Valid webhook (test message sent successfully)
    1 - Invalid webhook or connection error
"""

import sys
import re
import json
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


def parse_webhook(input_str: str) -> tuple[str, str]:
    """
    Parse webhook input into (full_url, key).
    Raises ValueError if format is invalid.
    """
    input_str = input_str.strip()

    # Try full URL
    match = URL_PATTERN.match(input_str)
    if match:
        key = match.group(1)
        if UUID_PATTERN.match(key):
            return input_str, key
        raise ValueError(f"Invalid key format in URL: {key}")

    # Try key only
    if UUID_PATTERN.match(input_str):
        return f"{WEBHOOK_BASE}{input_str}", input_str

    raise ValueError(
        f"Invalid webhook format: {input_str}\n"
        f"Expected a UUID key or full webhook URL."
    )


def validate_webhook(url: str) -> dict:
    """
    Send a validation request to the webhook.
    Returns the API response as a dict.
    """
    payload = json.dumps({
        "msgtype": "text",
        "text": {
            "content": "✅ Webhook 验证成功 — 来自 scheduled-webhook-push skill 的测试消息"
        }
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"errcode": e.code, "errmsg": f"HTTP Error: {e.reason}"}
    except urllib.error.URLError as e:
        return {"errcode": -1, "errmsg": f"Connection Error: {e.reason}"}
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}


def mask_key(key: str) -> str:
    """Mask webhook key for display: show first 8 and last 4 chars."""
    if len(key) > 12:
        return f"{key[:8]}...{key[-4:]}"
    return key


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_webhook.py <webhook_url_or_key>")
        sys.exit(1)

    input_str = sys.argv[1]

    try:
        url, key = parse_webhook(input_str)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    masked = mask_key(key)
    print(f"🔑 Webhook Key: {masked}")
    print(f"🌐 URL: {WEBHOOK_BASE}{masked}")
    print(f"📡 Sending test message...")

    result = validate_webhook(url)

    if result.get("errcode") == 0:
        print(f"✅ Webhook is valid! Response: {json.dumps(result)}")
        # Output the full URL for downstream use
        print(f"\nWEBHOOK_URL={url}")
        sys.exit(0)
    else:
        print(f"❌ Webhook validation failed: {json.dumps(result, ensure_ascii=False)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
