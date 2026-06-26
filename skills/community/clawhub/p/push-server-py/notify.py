#!/usr/bin/env python3
"""
WeCom Notification Skill for OpenClaw
Sends notifications via OpenAPI push service.

Environment variables:
  QYWX_PUSH_API_KEY  - API Key for X-API-Key header (required)
  QYWX_PUSH_URL      - Base URL of push service, e.g. https://push.wechat.com (required)

Usage:
  python3 scripts/notify.py '<JSON>'

Supported msgType: TEXT, MARKDOWN, TEXT_CARD, NEWS
"""

import sys
import json
import os
import urllib.request
import urllib.error


def qywx_notify(api_key: str, push_url: str, request_body: dict):
    url = push_url.rstrip("/") + "/api/v2/openapi/messages/send"

    data = json.dumps(request_body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("X-API-Key", api_key)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise Exception(f"HTTP {e.code}: {body}")

    if result.get("success") is False or (
        "errCode" in result and result["errCode"] != 0
    ):
        err_code = result.get("errCode", "unknown")
        err_msg = result.get("message", "Unknown error")
        raise Exception(f"API error: {err_msg} (errCode: {err_code})")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 notify.py '<JSON>'")
        sys.exit(1)

    query = sys.argv[1]
    parse_data = {}
    try:
        parse_data = json.loads(query)
        print(f"success parse request body: {parse_data}")
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    # Validate required fields
    if "toUser" not in parse_data:
        print("Error: toUser must be present in request body.")
        sys.exit(1)

    msg_type = parse_data.get("msgType", "TEXT").upper()
    valid_types = {"TEXT", "MARKDOWN", "TEXT_CARD", "NEWS"}
    if msg_type not in valid_types:
        print(f"Error: msgType must be one of {sorted(valid_types)}, got '{msg_type}'.")
        sys.exit(1)

    if msg_type in ("TEXT", "MARKDOWN") and "content" not in parse_data:
        print(f"Error: content must be present for msgType {msg_type}.")
        sys.exit(1)

    if msg_type == "TEXT_CARD":
        for field in ("title", "description", "url"):
            if field not in parse_data:
                print(f"Error: {field} must be present for msgType TEXT_CARD.")
                sys.exit(1)

    if msg_type == "NEWS":
        articles = parse_data.get("articles")
        if not isinstance(articles, list) or len(articles) == 0:
            print("Error: articles must be a non-empty list for msgType NEWS.")
            sys.exit(1)

    # Load env vars
    api_key = os.getenv("QYWX_PUSH_API_KEY")
    push_url = os.getenv("QYWX_PUSH_URL")

    if not api_key:
        print("Error: QYWX_PUSH_API_KEY must be set in environment.")
        sys.exit(1)

    if not push_url:
        print("Error: QYWX_PUSH_URL must be set in environment.")
        sys.exit(1)

    # Build request body
    request_body = {
        "msgType": msg_type,
        "toUser": parse_data["toUser"],
    }

    if msg_type in ("TEXT", "MARKDOWN"):
        request_body["content"] = parse_data["content"]

    elif msg_type == "TEXT_CARD":
        request_body["title"] = parse_data["title"]
        request_body["description"] = parse_data["description"]
        request_body["url"] = parse_data["url"]
        request_body["btnText"] = parse_data.get("btnText", "View Details")

    elif msg_type == "NEWS":
        request_body["articles"] = parse_data["articles"]

    try:
        result = qywx_notify(api_key, push_url, request_body)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)