"""
日志工具：将运行事件追加写入 aifusion-meta/logs/YYYY-MM-DD.jsonl
"""

import json
import base64
from datetime import datetime
import requests


def write_log(entry, meta_repo, token, base_url):
    try:
        owner, repo_name = meta_repo.split("/", 1)
        today = datetime.now().strftime("%Y-%m-%d")
        filepath = f"logs/{today}.jsonl"
        api_url = f"{base_url.rstrip('/')}/api/v1/repos/{owner}/{repo_name}/contents/{filepath}"
        headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
        }

        existing_content = ""
        existing_sha = None
        resp = requests.get(api_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            existing_content = base64.b64decode(data["content"]).decode("utf-8")
            existing_sha = data["sha"]

        new_line = json.dumps(entry, ensure_ascii=False)
        new_content = existing_content + new_line + "\n"
        encoded = base64.b64encode(new_content.encode("utf-8")).decode()

        payload = {
            "message": f"log: {entry.get('skill', 'skill')} {entry.get('action', 'event')}",
            "content": encoded,
            "branch": "main",
        }
        if existing_sha:
            payload["sha"] = existing_sha

        method = "PUT" if existing_sha else "POST"
        requests.request(method, api_url, headers=headers, json=payload, timeout=15)
    except Exception:
        pass
