#!/usr/bin/env python3
"""
ZeeLin X Creator Briefing runner (no openclaw task dependency).
- Fetches creator profile pages through r.jina.ai mirror
- Extracts recent post-like lines
- Builds markdown briefing
- Drafts English tweet
- Optionally publishes via existing tweet.sh
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict

import requests

WORKSPACE = Path("/Users/youke/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "zeelin-x-creator-briefing"
CONFIG_FILE = SKILL_DIR / "config" / "creators.yaml"
REPORT_DIR = WORKSPACE / "reports"
TWEET_SCRIPT = WORKSPACE / "skills" / "zeelin-twitter-web-autopost" / "scripts" / "tweet.sh"


def parse_creators_from_yaml(path: Path) -> List[Dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"- handle:\s*\"([^\"]+)\"\s*\n\s*name:\s*\"([^\"]+)\"", text)
    out = []
    seen = set()
    for handle, name in blocks:
        h = handle.strip()
        if h.lower() in seen:
            continue
        seen.add(h.lower())
        out.append({"handle": h, "name": name.strip()})
    return out


def fetch_profile_markdown(handle: str, timeout: int = 25) -> str:
    url = f"https://r.jina.ai/http://x.com/{handle}"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text


def extract_signal_lines(md: str, max_lines: int = 8) -> List[str]:
    lines = [ln.strip() for ln in md.splitlines()]
    cleaned = []
    bad_prefixes = (
        "Title:", "URL Source:", "Published Time:", "Markdown Content:",
        "Pinned", "Quote", "[![Image", "![Image"
    )
    for ln in lines:
        if not ln or len(ln) < 40 or len(ln) > 320:
            continue
        if ln.startswith(bad_prefixes):
            continue
        if re.match(r"^@?[A-Za-z0-9_\.-]+$", ln):
            continue
        if "http" in ln and len(ln) < 80:
            continue
        if ln in cleaned:
            continue
        cleaned.append(ln)
        if len(cleaned) >= max_lines:
            break
    return cleaned


def build_briefing(date_str: str, creators: List[Dict[str, str]], days: int) -> Dict[str, str]:
    sections = []
    top_items = []
    unavailable = []
    total_lines = 0

    for c in creators:
        h, name = c["handle"], c["name"]
        try:
            md = fetch_profile_markdown(h)
            lines = extract_signal_lines(md, max_lines=6)
            if not lines:
                unavailable.append((h, name, "页面可读但未提取到有效近况"))
                continue

            total_lines += len(lines)
            bullets = "\n".join([f"- {x}" for x in lines[:4]])
            section = (
                f"### @{h} ({name})\n"
                f"- 近{days}天可见高信号摘录（基于公开页面抓取）：\n"
                f"{bullets}\n"
            )
            sections.append(section)
            top_items.append({"handle": h, "name": name, "line": lines[0]})
        except Exception as e:
            unavailable.append((h, name, f"抓取失败: {e.__class__.__name__}"))

    top_items = top_items[:5]
    top_block = "\n".join(
        [f"{i+1}. @{it['handle']}：{it['line'][:120]}" for i, it in enumerate(top_items)]
    ) or "暂无可提炼高信号主线"

    unavailable_block = "\n".join(
        [f"- @{h} ({n}) - {r}" for h, n, r in unavailable[:12]]
    ) or "- 无"

    md = f"""# X AI Creator Briefing - {date_str}

> ZeeLin AI 推特博主信息简报（自动生成）

## 📊 本期概览
- 监控博主：{len(creators)} 位
- 成功抓取：{len(sections)} 位
- 提取信号：{total_lines} 条
- 抓取窗口：最近 {days} 天（按公开页面可见内容近似）

## 🔥 高信号主线
{top_block}

## 📌 按博主摘录
{os.linesep.join(sections) if sections else '暂无可用摘录'}

## ⚠️ 未抓到内容的博主
{unavailable_block}

## 方法说明
- 当前版本使用 `https://r.jina.ai/http://x.com/<handle>` 抓取公开页面文本镜像。
- 若账号隐私/限流/页面结构变化，可能导致当日无结果。
- 本简报优先“可稳定运行”，后续可接入更完整的数据源。
"""

    tweet = "📊 AI Creator Briefing ({date})\n\nTop updates:\n{items}\n\nFull briefing saved in workspace reports.\n\n#AI #OpenClaw #Agent".format(
        date=date_str,
        items="\n".join([f"{i+1}. @{it['handle']}: {it['line'][:90]}" for i, it in enumerate(top_items[:3])]) or "1. No strong public updates captured today"
    )

    return {"briefing_md": md, "tweet": tweet}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=10)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    date_str = dt.datetime.now().strftime("%Y-%m-%d")
    creators = parse_creators_from_yaml(CONFIG_FILE)
    result = build_briefing(date_str, creators, args.days)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    briefing_path = REPORT_DIR / f"x-creator-briefing-{date_str}.md"
    tweet_path = REPORT_DIR / f"x-creator-tweet-{date_str}.txt"
    run_meta = REPORT_DIR / f"x-creator-run-{date_str}.json"

    briefing_path.write_text(result["briefing_md"], encoding="utf-8")
    tweet_path.write_text(result["tweet"], encoding="utf-8")

    meta = {
        "date": date_str,
        "briefing": str(briefing_path),
        "tweetDraft": str(tweet_path),
        "published": False,
    }

    if args.publish:
        try:
            subprocess.run(["bash", str(TWEET_SCRIPT), result["tweet"], "https://x.com"], check=True)
            meta["published"] = True
        except Exception as e:
            meta["publishError"] = str(e)

    run_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Briefing: {briefing_path}")
    print(f"Tweet draft: {tweet_path}")
    print(f"Meta: {run_meta}")
    print(f"Published: {meta.get('published', False)}")
    if meta.get("publishError"):
        print(f"Publish error: {meta['publishError']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
