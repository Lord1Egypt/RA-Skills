#!/usr/bin/env python3
"""
TingDong Podcast Generator - CLI
调用后端 API v1 将文章/文本转换为播客音频

后端: http://111.229.22.145:8092/api/v1
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

import os

BASE_URL = os.environ.get("TINGDONG_API_URL", "http://111.229.22.145:8092/api/v1").rstrip("/")
API_TOKEN = os.environ.get("TINGDONG_API_TOKEN", "")


def api_post(endpoint: str, payload: dict, timeout: int = 30) -> dict:
    """POST 请求"""
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api_get(endpoint: str, timeout: int = 30) -> dict:
    """GET 请求"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    req = urllib.request.Request(url, method="GET", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def submit(content: str, content_type: str = "url", style: str = "conversational",
           user_id: str = "cli_user") -> dict:
    """提交播客生成任务"""
    return api_post("/podcast/submit", {
        "content": content,
        "content_type": content_type,
        "style": style,
        "user_id": user_id
    })


def poll(task_id: str, max_wait: int = 300, interval: int = 5) -> dict:
    """轮询任务状态直到完成"""
    start = time.time()
    while time.time() - start < max_wait:
        result = api_get(f"/podcast/{task_id}")
        status = result.get("status")
        if status == "completed":
            return result
        elif status == "failed":
            raise RuntimeError(f"Task failed: {result.get('error', 'Unknown')}")
        progress = result.get("progress", status)
        print(f"  [{progress}] waiting...", file=sys.stderr)
        time.sleep(interval)
    raise TimeoutError(f"Task {task_id} timeout after {max_wait}s")


def main():
    parser = argparse.ArgumentParser(description="TingDong Podcast Generator")
    parser.add_argument("content", help="Article URL or text content")
    parser.add_argument("--type", choices=["url", "text"], default="url")
    parser.add_argument("--style", choices=["conversational", "summary", "deep_dive"],
                        default="conversational")
    parser.add_argument("--user-id", default="cli_user")
    parser.add_argument("--no-wait", action="store_true", help="Submit only, don't poll")
    args = parser.parse_args()

    try:
        # Submit
        resp = submit(args.content, args.type, args.style, args.user_id)
        task_id = resp["task_id"]
        print(f"Task submitted: {task_id}", file=sys.stderr)

        if args.no_wait:
            print(json.dumps(resp, ensure_ascii=False, indent=2))
            return

        # Poll
        result = poll(task_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
