#!/usr/bin/env python3
"""
TingDong Podcast Generator - REST API v1 Client
调用后端 API 将文章/文本转换为播客音频

后端地址: http://111.229.22.145:8092
API版本: v1
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "http://111.229.22.145:8092"
API_PREFIX = "/api/v1"


def call_api(endpoint: str, payload: dict = None, method: str = "GET", timeout: int = 30) -> dict:
    """调用后端 API"""
    url = f"{BASE_URL}{API_PREFIX}{endpoint}"
    
    if method == "POST" and payload:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    else:
        req = urllib.request.Request(url, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            raise RuntimeError(f"API error {e.code}: {error_json.get('error', error_body)}")
        except json.JSONDecodeError:
            raise RuntimeError(f"API error {e.code}: {error_body}")
    except Exception as e:
        raise RuntimeError(f"Request failed: {e}")


def submit_task(content: str, content_type: str = "url", style: str = "conversational",
                duration: str = "medium", user_id: str = "skill_user") -> str:
    """
    提交播客生成任务
    
    Args:
        content: 文章链接或文本内容
        content_type: "url" | "text"
        style: "conversational" | "summary" | "deep_dive"
        duration: "short" | "medium" | "long"
        user_id: 用户标识
    
    Returns:
        task_id: 任务 ID
    """
    payload = {
        "content": content,
        "content_type": content_type,
        "style": style,
        "duration": duration,
        "user_id": user_id
    }
    
    result = call_api("/podcast/submit", payload, method="POST")
    return result["task_id"]


def poll_task(task_id: str, max_wait: int = 300, interval: int = 5) -> dict:
    """
    轮询任务状态直到完成
    
    Args:
        task_id: 任务 ID
        max_wait: 最大等待秒数
        interval: 轮询间隔秒数
    
    Returns:
        任务结果字典
    """
    start = time.time()
    
    while time.time() - start < max_wait:
        result = call_api(f"/podcast/{task_id}", method="GET")
        
        status = result.get("status")
        progress = result.get("progress", "")
        
        if status == "completed":
            return result
        elif status == "failed":
            raise RuntimeError(f"Task failed: {result.get('error', 'Unknown error')}")
        
        if progress:
            print(f"  [{status}] {progress}", file=sys.stderr)
        
        time.sleep(interval)
    
    raise TimeoutError(f"Task {task_id} did not complete within {max_wait}s")


def generate_podcast(content: str, content_type: str = "url", style: str = "conversational",
                     duration: str = "medium", user_id: str = "skill_user",
                     wait: bool = True) -> dict:
    """
    完整流程：提交任务 + 轮询结果
    
    Returns:
        {
            "task_id": "...",
            "status": "completed",
            "title": "播客标题",
            "audio_url": "http://.../audio/xxx.mp3",
            "content_length": 2406,
            "analysis_length": 1195,
            "source": "来源"
        }
    """
    task_id = submit_task(content, content_type, style, duration, user_id)
    print(f"Task submitted: {task_id}", file=sys.stderr)
    
    if not wait:
        return {"task_id": task_id, "status": "pending"}
    
    return poll_task(task_id)


def main():
    parser = argparse.ArgumentParser(description="TingDong Podcast Generator (API v1)")
    parser.add_argument("content", help="Article URL or text content")
    parser.add_argument("--type", choices=["url", "text"], default="url", help="Content type")
    parser.add_argument("--style", choices=["conversational", "summary", "deep_dive"],
                        default="conversational", help="Podcast style")
    parser.add_argument("--duration", choices=["short", "medium", "long"],
                        default="medium", help="Target duration")
    parser.add_argument("--user-id", default="cli_user", help="User identifier")
    parser.add_argument("--no-wait", action="store_true", help="Submit only, don't poll")
    
    args = parser.parse_args()
    
    try:
        result = generate_podcast(
            content=args.content,
            content_type=args.type,
            style=args.style,
            duration=args.duration,
            user_id=args.user_id,
            wait=not args.no_wait
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
