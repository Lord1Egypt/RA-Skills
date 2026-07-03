#!/usr/bin/env python3
"""
Activity analyzer: daily summary + search past logs.
Works with both local backend and SiYuan backend.
"""

import json
import os
import sys
import re
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.json")
LOCAL_DIR = os.path.expanduser("~/screen-activity")


def load_config():
    config = {"backend": "local", "local": {"output_dir": "~/screen-activity"}}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                user = json.load(f)
            for k, v in user.items():
                if k in config and isinstance(config[k], dict) and isinstance(v, dict):
                    config[k].update(v)
                else:
                    config[k] = v
        except (json.JSONDecodeError, IOError):
            pass
    return config


def get_local_dir(config=None):
    if config is None:
        config = load_config()
    return os.path.expanduser(config.get("local", {}).get("output_dir", "~/screen-activity"))


# ==================== Daily Summary ====================

def daily_summary(date_str=None, config=None):
    """Generate a summary of today's (or given date's) activity."""
    if config is None:
        config = load_config()
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    backend = config.get("backend", "local")

    if backend == "siyuan":
        return _summary_siyuan(date_str, config)
    else:
        return _summary_local(date_str, config)


def _summary_local(date_str, config):
    local_dir = get_local_dir(config)
    md_path = os.path.join(local_dir, f"{date_str}.md")
    if not os.path.exists(md_path):
        return f"{date_str} 暂无活动记录。"

    with open(md_path) as f:
        content = f.read()

    # Parse entries
    entries = re.findall(r"-\s+\*\*(.+?)\*\*\s+(.+?)(?:\n|$)", content)
    if not entries:
        return f"{date_str} 暂无有效活动记录。"

    # Count by app/category
    app_count = {}
    total_entries = len(entries)

    for time_str, desc in entries:
        # Extract app name from [app] description
        app_match = re.match(r"\[(.+?)\]", desc)
        app = app_match.group(1) if app_match else desc[:20]
        app_count[app] = app_count.get(app, 0) + 1

    # Build summary
    lines = [
        f"## {date_str} 活动总结",
        f"",
        f"- 总记录数: {total_entries} 条",
        f"- 活跃应用: {len(app_count)} 个",
        f"",
        f"### 应用分布",
    ]
    for app, cnt in sorted(app_count.items(), key=lambda x: -x[1]):
        pct = int(cnt / total_entries * 100)
        bar = "#" * min(pct // 5, 20)
        lines.append(f"- {app}: {cnt} 次 ({pct}%) {bar}")

    return "\n".join(lines)


def _summary_siyuan(date_str, config):
    """Fetch today's SiYuan doc and summarize."""
    siyuan = config.get("siyuan", {})
    # This would need to query SiYuan API to get the daily doc content
    # For now, return a note that SiYuan summary requires API call
    return f"SiYuan backend summary: please query SiYuan doc for {date_str} 操作记录 directly."


# ==================== Search ====================

def search_logs(query, days=7, config=None):
    """Search past activity logs for a query string."""
    if config is None:
        config = load_config()
    backend = config.get("backend", "local")

    if backend == "siyuan":
        return _search_siyuan(query, days, config)
    else:
        return _search_local(query, days, config)


def _search_local(query, days, config):
    local_dir = get_local_dir(config)
    results = []
    now = datetime.now()

    for i in range(days):
        d = now - timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        md_path = os.path.join(local_dir, f"{date_str}.md")
        if not os.path.exists(md_path):
            continue

        with open(md_path) as f:
            content = f.read()

        # Find matching lines
        for line in content.split("\n"):
            if re.search(query, line, re.IGNORECASE) and line.strip().startswith("-"):
                results.append((date_str, line.strip()))

    if not results:
        return f"未找到匹配 '{query}' 的记录（最近 {days} 天）。"

    lines = [f"## 搜索结果: '{query}' ({len(results)} 条)\n"]
    current_date = None
    for date_str, line in results:
        if date_str != current_date:
            lines.append(f"\n**{date_str}**")
            current_date = date_str
        lines.append(f"  {line}")
    return "\n".join(lines)


def _search_siyuan(query, days, config):
    return f"SiYuan search: use SiYuan's built-in search for '{query}'."


# ==================== Analyze Screenshot ====================

def analyze_screenshot(screenshot_path, config=None):
    """Analyze a single screenshot with the VL model."""
    if config is None:
        config = load_config()

    mlx_url = config.get("mlx_url", "")
    mode = config.get("analysis_mode", "simple")
    custom_prompt = config.get("analysis_prompt", "")

    prompts = {
        "simple": '用一句简短中文描述这张屏幕截图中用户正在做什么，格式: [应用名] 简短描述。只输出描述。',
        "category": '判断用户当前状态，从：工作 / 娱乐 / 学习 / 休息 中选一个，格式：[分类] 简短描述。只输出结果。',
        "productivity": '评估当前活动的生产力得分(1-10分)，格式：[得分] 简短描述。只输出结果。',
        "custom": custom_prompt,
    }
    prompt = prompts.get(mode, prompts["simple"])

    if not os.path.exists(screenshot_path):
        return "Screenshot file not found."

    try:
        import base64, urllib.request
        with open(screenshot_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        payload = {
            "model": "Qwen3.5-9B-MLX-4bit",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    {"type": "text", "text": prompt},
                ]
            }],
            "max_tokens": 80,
            "temperature": 0.3,
        }

        req = urllib.request.Request(
            f"{mlx_url}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Authorization": "Bearer placeholder"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Analysis failed: {e}"


# ==================== CLI ====================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage:")
        print(f"  {sys.argv[0]} summary [date]        # Daily summary")
        print(f"  {sys.argv[0]} search <query> [days]  # Search logs")
        print(f"  {sys.argv[0]} analyze <screenshot>  # Analyze one screenshot")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "summary":
        date_str = sys.argv[2] if len(sys.argv) > 2 else None
        print(daily_summary(date_str))
    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        print(search_logs(query, days))
    elif cmd == "analyze":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        print(analyze_screenshot(path))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
