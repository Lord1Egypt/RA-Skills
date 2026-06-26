#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def read_text(path):
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text()


def bullets_under(text, heading):
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    lines = text.splitlines()
    out = []
    capture = False
    for line in lines:
        if re.match(pattern, line.strip()):
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.strip().startswith("-"):
            out.append(line.strip()[1:].strip())
    return out


def extract_name(user_md):
    m = re.search(r"\*\*Name:\*\*\s*(.+)", user_md)
    return m.group(1).strip() if m else None


def extract_timezone(user_md):
    m = re.search(r"\*\*Timezone:\*\*\s*(.+)", user_md)
    return m.group(1).strip() if m else None


def infer_company(memory_md):
    m = re.search(r"AI 视频剪辑产品 \*\*(.+?)\*\*", memory_md)
    if m:
        return m.group(1).strip()
    return None


def infer_platforms(memory_md, user_md):
    platforms = []
    if "YouTube" in memory_md:
        platforms.append("YouTube")
    if "小红书" in memory_md:
        platforms.append("Xiaohongshu")
    if "Telegram" in user_md:
        platforms.append("Telegram")
    seen = []
    for p in platforms:
        if p not in seen:
            seen.append(p)
    return seen


def infer_content_pattern(memory_md):
    patterns = []
    if "养虾日记" in memory_md or "Shrimp Diaries" in memory_md:
        patterns.append("Build-in-public / real process diary")
    if "AI + Humanity" in memory_md:
        patterns.append("AI + Humanity thesis content")
    if "Sparki" in memory_md:
        patterns.append("Founder / AI product building")
    return " + ".join(patterns) if patterns else "Founder/operator content"


def infer_current_problem(memory_md):
    if "个人品牌" in memory_md or "内容账号" in memory_md:
        return "Turn strategic thinking and real product-building process into a repeatable content system."
    return "Content operating system still needs clearer focus."


def main():
    parser = argparse.ArgumentParser(description="Extract creator context from OpenClaw memory files")
    parser.add_argument("--workspace", default="/Users/fischer/.openclaw/workspace")
    parser.add_argument("--output")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    memory_md = read_text(workspace / "MEMORY.md")
    user_md = read_text(workspace / "USER.md")

    result = {
        "creator": {
            "name": extract_name(user_md),
            "role": "Founder / builder",
            "company": infer_company(memory_md),
            "platforms": infer_platforms(memory_md, user_md),
            "content_pattern": infer_content_pattern(memory_md),
            "current_problem": infer_current_problem(memory_md),
            "timezone": extract_timezone(user_md),
        },
        "memory_summary": {
            "mission": bullets_under(memory_md, "Fischer 的使命"),
            "business": bullets_under(memory_md, "Fischer 的业务"),
            "background_advantages": bullets_under(memory_md, "Fischer 的背景优势"),
        }
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text)
    print(text)


if __name__ == "__main__":
    main()
