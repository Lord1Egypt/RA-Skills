"""
GitHub OpenClaw 动态采集模块
搜索 GitHub 上 OpenClaw 相关的最新动态（issues/PRs/releases/新仓库）
"""

import json
from datetime import datetime, timedelta, timezone

try:
    import requests

    def _get(url, params=None, timeout=15):
        resp = requests.get(url, params=params, timeout=timeout, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "spec-engine-collector/1.0",
        })
        resp.raise_for_status()
        return resp.json()

except ImportError:
    import urllib.request
    import urllib.parse
    import urllib.error

    def _get(url, params=None, timeout=15):
        if params:
            url = url + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "spec-engine-collector/1.0",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))


API_BASE = "https://api.github.com"


def _trunc(text, max_len=200):
    """截断文本到指定长度"""
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\r", " ").strip()
    return text[:max_len] + ("..." if len(text) > max_len else "")


def _parse_issue(item):
    """解析 issue/PR 搜索结果"""
    is_pr = "pull_request" in item
    repo_full = ""
    if item.get("repository_url"):
        repo_full = item["repository_url"].split("repos/")[-1]

    return {
        "title": item.get("title", ""),
        "url": item.get("html_url", ""),
        "author": item.get("user", {}).get("login", "unknown"),
        "type": "pr" if is_pr else "issue",
        "publish_time": item.get("created_at", ""),
        "description": _trunc(item.get("body", "")),
        "repo": repo_full,
    }


def _parse_repo(item):
    """解析仓库搜索结果"""
    return {
        "title": item.get("full_name", ""),
        "url": item.get("html_url", ""),
        "author": item.get("owner", {}).get("login", "unknown"),
        "type": "repo",
        "publish_time": item.get("created_at", ""),
        "description": _trunc(item.get("description", "")),
        "repo": item.get("full_name", ""),
    }


def collect(keyword="openclaw", hours=24):
    """
    搜索 GitHub 上指定关键词的最新动态

    Args:
        keyword: 搜索关键词，默认 "openclaw"
        hours: 回溯小时数，默认 24

    Returns:
        dict: 包含 source, items, total, query_time 的结果字典
    """
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=hours)
    since_str = since.strftime("%Y-%m-%d")
    query_time = now.strftime("%Y-%m-%d %H:%M")

    items = []
    errors = []

    # 1. 搜索 issues + PRs
    try:
        q = f"{keyword} created:>{since_str}"
        data = _get(f"{API_BASE}/search/issues", params={
            "q": q,
            "sort": "created",
            "order": "desc",
            "per_page": 30,
        })
        for item in data.get("items", []):
            items.append(_parse_issue(item))
    except Exception as e:
        errors.append(f"issues/PRs search failed: {e}")

    # 2. 搜索新仓库
    try:
        q = f"{keyword} created:>{since_str}"
        data = _get(f"{API_BASE}/search/repositories", params={
            "q": q,
            "sort": "created",
            "order": "desc",
            "per_page": 30,
        })
        for item in data.get("items", []):
            items.append(_parse_repo(item))
    except Exception as e:
        errors.append(f"repos search failed: {e}")

    # 按发布时间倒序排列
    items.sort(key=lambda x: x.get("publish_time", ""), reverse=True)

    result = {
        "source": "github",
        "items": items,
        "total": len(items),
        "query_time": query_time,
    }
    if errors:
        result["errors"] = errors

    return result


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("正在搜索 GitHub 上 OpenClaw 最近 24 小时的动态...\n")
    result = collect()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n共找到 {result['total']} 条结果")
    if result.get("errors"):
        print("部分请求出错:", result["errors"])
