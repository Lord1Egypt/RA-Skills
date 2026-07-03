#!/usr/bin/env python3
"""
Activity analyzer for local markdown logs.
Usage:
  python3 activity-analyzer.py summary [date]
  python3 activity-analyzer.py search "<query>"
"""

import os
import sys
import json
import glob
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "..", "config.json")


def load_config():
    config = {"output_dir": os.path.expanduser("~/screen-activity")}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                user_cfg = json.load(f)
            config["output_dir"] = os.path.expanduser(user_cfg.get("output_dir", config["output_dir"]))
        except (json.JSONDecodeError, IOError):
            pass
    return config


def load_logs(output_dir, date_str=None):
    """Load all markdown log entries for a given date, or today if not specified."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    md_path = os.path.join(output_dir, f"{date_str}.md")
    if not os.path.exists(md_path):
        return []

    entries = []
    with open(md_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("- **") and "** " in line:
                # Format: - **HH:MM** description
                try:
                    time_part = line.split("** ")[0].replace("- **", "")
                    desc = line.split("** ", 1)[1] if "** " in line else ""
                    entries.append({"time": time_part, "description": desc})
                except (IndexError, ValueError):
                    pass

    return entries


def summary(output_dir, date_str=None):
    """Print a daily activity summary."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    entries = load_logs(output_dir, date_str)

    if not entries:
        print(f"📭 {date_str} 没有记录")
        return

    print(f"\n📊 {date_str} 屏幕活动总结\n")
    print(f"共 {len(entries)} 条记录\n")

    # Count apps
    app_count = {}
    for e in entries:
        desc = e["description"]
        # Try to extract app name from [AppName] format
        if desc.startswith("[") and "]" in desc:
            app = desc[1:desc.index("]")]
        else:
            app = "其他"
        app_count[app] = app_count.get(app, 0) + 1

    print("📱 应用使用统计:")
    for app, count in sorted(app_count.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * min(count, 20)
        print(f"  {app:12s} {bar} {count}")

    print(f"\n📝 时间线:")
    for e in entries:
        desc = e["description"][:100]
        print(f"  {e['time']}  {desc}")


def search(output_dir, query):
    """Search all log files for a keyword."""
    files = sorted(glob.glob(os.path.join(output_dir, "*.md")), reverse=True)
    results = []

    for fpath in files:
        date_str = os.path.splitext(os.path.basename(fpath))[0]
        try:
            with open(fpath) as f:
                content = f.read()
        except (IOError, UnicodeDecodeError):
            continue

        for line in content.split("\n"):
            if query.lower() in line.lower() and line.startswith("- **"):
                results.append((date_str, line.strip()))

    if not results:
        print(f"🔍 未找到包含「{query}」的记录")
        return

    print(f"\n🔍 找到 {len(results)} 条包含「{query}」的记录:\n")
    for date_str, line in results[:30]:
        print(f"  [{date_str}] {line}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 activity-analyzer.py summary [date]")
        print("  python3 activity-analyzer.py search <query>")
        sys.exit(1)

    config = load_config()
    output_dir = config["output_dir"]

    cmd = sys.argv[1]

    if cmd == "summary":
        date_str = sys.argv[2] if len(sys.argv) > 2 else None
        summary(output_dir, date_str)

    elif cmd == "search":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not query:
            print("请提供搜索关键词")
            sys.exit(1)
        search(output_dir, query)

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
