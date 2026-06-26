#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

DEFAULT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0e41994e-9e62-4713-ad69-fddeaaba8e9a"
ACTION_WORDS = {
    "seo": "优化 SEO / 搜索可见性",
    "title": "调整页面标题或主标题",
    "description": "调整页面描述文案",
    "keyword": "调整关键词覆盖",
    "footer": "调整页脚区域",
    "header": "调整页头区域",
    "style": "优化样式表现",
    "css": "优化样式表现",
    "less": "优化样式表现",
    "layout": "调整页面布局",
    "color": "调整颜色或视觉风格",
    "font": "调整字号或字体表现",
    "link": "调整链接或跳转入口",
    "banner": "调整 Banner 或首屏内容",
    "hero": "调整首屏视觉内容",
    "meta": "调整页面元信息",
    "question": "调整问答/内容模块",
    "productdemand": "更新需求文档",
}


def run_git(project_dir: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(project_dir),
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def read_summary(args) -> str:
    if args.summary:
        return args.summary.strip()
    if args.summary_file:
        return Path(args.summary_file).read_text(encoding="utf-8").strip()
    if args.stdin:
        return sys.stdin.read().strip()
    return ""


def changed_files(project_dir: Path, commit_ref: str) -> list[str]:
    files = run_git(project_dir, "show", "--name-only", "--pretty=format:", commit_ref)
    return [line.strip() for line in files.splitlines() if line.strip()]


def diff_text(project_dir: Path, commit_ref: str) -> str:
    return run_git(project_dir, "show", "--stat=200,200", "--format=medium", commit_ref)


def summarize_from_files(files: list[str]) -> str:
    if not files:
        return "- 本次提交未提取到文件级变动信息"

    notes: list[str] = []
    lowered = "\n".join(files).lower()
    matched_actions = []
    for key, note in ACTION_WORDS.items():
        if key in lowered:
            matched_actions.append(note)

    for note, _count in Counter(matched_actions).most_common(6):
        notes.append(f"- {note}")

    top_files = files[:8]
    if top_files:
        notes.append("- 涉及文件：" + "、".join(top_files))

    return "\n".join(dict.fromkeys(notes)) if notes else "\n".join(f"- {f}" for f in top_files)


def summarize_from_diff(project_dir: Path, commit_ref: str) -> str:
    files = changed_files(project_dir, commit_ref)
    base = summarize_from_files(files)
    text = diff_text(project_dir, commit_ref).lower()

    extra = []
    if re.search(r"title|description|keywords|canonical|meta", text):
        extra.append("- 处理了页面标题、描述、关键词或 canonical 等 SEO 信息")
    if re.search(r"font-size|font|color|background|margin|padding|border|less|css", text):
        extra.append("- 调整了页面样式、字号、颜色或间距等视觉细节")
    if re.search(r"href|window\.location|router|link", text):
        extra.append("- 调整了链接、跳转入口或导航相关逻辑")
    if re.search(r"productdemand\.md|backup", text):
        extra.append("- 更新并备份了需求文档")

    summary_lines = []
    for line in base.splitlines():
        if line.strip():
            summary_lines.append(line)
    for line in extra:
        if line not in summary_lines:
            summary_lines.append(line)

    return "\n".join(summary_lines[:8]) if summary_lines else base


def build_content(project_dir: Path, branch: str, commit_ref: str, summary: str) -> str:
    commit_hash = run_git(project_dir, "rev-parse", "--short", commit_ref)
    commit_subject = run_git(project_dir, "show", "-s", "--format=%s", commit_ref)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = summary.strip() if summary.strip() else summarize_from_diff(project_dir, commit_ref)
    return "\n".join([
        f"时间：{timestamp}",
        f"项目：{project_dir}",
        f"分支：{branch}",
        f"提交：{commit_hash} {commit_subject}",
        "代码变动点：",
        summary,
    ])


def post_json(url: str, payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send push result summary to WeCom webhook")
    parser.add_argument("--project-dir", required=True, help="Git project directory")
    parser.add_argument("--branch", default="feat/test", help="Git branch name")
    parser.add_argument("--commit-ref", default="HEAD", help="Git commit ref")
    parser.add_argument("--summary", help="Summary text")
    parser.add_argument("--summary-file", help="Path to summary text file")
    parser.add_argument("--stdin", action="store_true", help="Read summary text from stdin")
    parser.add_argument("--webhook-url", default=os.environ.get("WECOM_WEBHOOK_URL", DEFAULT_WEBHOOK_URL), help="Override webhook URL")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    summary = read_summary(args)
    content = build_content(project_dir, args.branch, args.commit_ref, summary)
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    response_text = post_json(args.webhook_url, payload)
    print(response_text)
    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError:
        return 1
    return 0 if response_json.get("errcode") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
