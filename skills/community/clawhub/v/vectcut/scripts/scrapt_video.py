#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

import requests

BASE_URL = "https://open.vectcut.com"
PLATFORM_CONFIG = {
    "xiaohongshu": {
        "path": "/scrapt/xiaohongshu/parse",
        "doc_url": "https://docs.vectcut.com/433862658e0",
    },
    "douyin": {
        "path": "/scrapt/douyin/parse",
        "doc_url": "https://docs.vectcut.com/433861888e0",
    },
    "kuaishou": {
        "path": "/scrapt/kuaishou/parse",
        "doc_url": "https://docs.vectcut.com/433861890e0",
    },
    "bilibili": {
        "path": "/scrapt/bilibili/parse",
        "doc_url": "https://docs.vectcut.com/433861891e0",
    },
    "tiktok": {
        "path": "/scrapt/tiktok/parse",
        "doc_url": "https://docs.vectcut.com/433861892e0",
    },
    "youtube": {
        "path": "/scrapt/youtube/parse",
        "doc_url": "https://docs.vectcut.com/433861893e0",
    },
}


def _ensure_token():
    token = os.environ.get("VECTCUT_API_KEY")
    if not token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first."
        )
    return token


def _auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _parse_json_response(resp):
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _detect_platform(text):
    lowered = (text or "").lower()
    if re.search(r"(xiaohongshu\.com|xhslink\.com|小红书)", lowered):
        return "xiaohongshu"
    if re.search(r"(douyin\.com|iesdouyin\.com|抖音)", lowered):
        return "douyin"
    if re.search(r"(kuaishou\.com|快手)", lowered):
        return "kuaishou"
    if re.search(r"(bilibili\.com|b23\.tv|哔哩|b站)", lowered):
        return "bilibili"
    if re.search(r"(tiktok\.com|tik tok|tiktok)", lowered):
        return "tiktok"
    if re.search(r"(youtube\.com|youtu\.be|youtube)", lowered):
        return "youtube"
    return ""


def parse_social_link(token, platform, source_text):
    config = PLATFORM_CONFIG.get(platform)
    if not config:
        raise RuntimeError(f"Unsupported platform: {platform}")
    resp = requests.post(
        f"{BASE_URL}{config['path']}",
        headers=_auth_headers(token),
        json={"url": source_text},
        timeout=90,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    if not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    return body


def _extract_video_url(parse_result):
    data = parse_result.get("data") or {}
    video = data.get("video") or {}
    candidate = str(video.get("url") or "").strip()
    if candidate.startswith(("http://", "https://")):
        return candidate
    return ""


def _load_describe_video_module():
    current_script = Path(__file__).resolve()
    describe_path = (
        current_script.parents[2] / "describe-video" / "scripts" / "describe_video.py"
    )
    if not describe_path.exists():
        raise RuntimeError(f"describe-video script not found: {describe_path}")
    spec = importlib.util.spec_from_file_location("describe_video_module", describe_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_markdown(result, describe_markdown):
    meta = result["meta"]
    parse_result = result["parse_result"]
    data = parse_result.get("data") or {}
    lines = []
    lines.append("# 社媒链接深度解析报告（scrapt-video）")
    lines.append("")
    lines.append("## 解析概览")
    lines.append(f"- 平台：{meta['platform']}")
    lines.append(f"- 解析接口：`{meta['parse_endpoint']}`")
    lines.append(f"- 接口文档：{meta['doc_url']}")
    lines.append(f"- 原始链接/文案：{meta['source_text']}")
    lines.append(f"- 解析出的视频直链：{meta['resolved_video_url'] or '(空)'}")
    lines.append("")
    lines.append("## 平台素材信息")
    lines.append(f"- 标题：{data.get('title') or '(空)'}")
    lines.append(f"- 描述：{data.get('desc') or '(空)'}")
    lines.append(f"- 作者：{((data.get('author') or {}).get('nickname')) or '(空)'}")
    lines.append(f"- 内容类型：{data.get('type') or '(空)'}")
    lines.append(f"- 原始链接：{data.get('original_url') or '(空)'}")
    lines.append("")
    lines.append("## Describe Video 分析")
    lines.append("")
    lines.append(describe_markdown.strip() if describe_markdown else "(无)")
    lines.append("")
    return "\n".join(lines)


def run(source_text, platform="", analysis_prompt="", poll_interval=2.0, timeout=600.0):
    token = _ensure_token()
    chosen_platform = platform.strip().lower() if platform else _detect_platform(source_text)
    if not chosen_platform:
        supported = ", ".join(sorted(PLATFORM_CONFIG.keys()))
        raise RuntimeError(
            f"Cannot detect platform from input. Please pass --platform explicitly. "
            f"Supported: {supported}"
        )
    if chosen_platform not in PLATFORM_CONFIG:
        raise RuntimeError(f"Unsupported platform: {chosen_platform}")

    parse_result = parse_social_link(token, chosen_platform, source_text)
    video_url = _extract_video_url(parse_result)
    if not video_url:
        raise RuntimeError(
            "No video url returned by scrapt API. "
            "The source may be unsupported, region-limited, or non-video content."
        )

    describe_module = _load_describe_video_module()
    describe_report = describe_module.run(
        urls=[video_url],
        analysis_prompt=analysis_prompt,
        poll_interval=poll_interval,
        timeout=timeout,
    )
    describe_markdown = describe_module.render_markdown(describe_report)

    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "platform": chosen_platform,
            "doc_url": PLATFORM_CONFIG[chosen_platform]["doc_url"],
            "parse_endpoint": PLATFORM_CONFIG[chosen_platform]["path"],
            "source_text": source_text,
            "resolved_video_url": video_url,
            "analysis_prompt": analysis_prompt.strip(),
        },
        "parse_result": parse_result,
        "describe_video_report": describe_report,
        "describe_video_markdown": describe_markdown,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse social link with platform scrapt API then run describe-video."
    )
    parser.add_argument("source_text", help="原始链接或分享文案")
    parser.add_argument(
        "--platform",
        default="",
        choices=sorted(PLATFORM_CONFIG.keys()),
        help="可选，手动指定平台；不传则自动识别",
    )
    parser.add_argument("--analysis-prompt", default="")
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--json-output", default="scrapt_video_report.json")
    parser.add_argument("--md-output", default="scrapt_video_report.md")
    args = parser.parse_args()

    try:
        result = run(
            source_text=args.source_text,
            platform=args.platform,
            analysis_prompt=args.analysis_prompt,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        markdown = render_markdown(result, result.get("describe_video_markdown", ""))
        with open(args.md_output, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(
            json.dumps(
                {
                    "platform": result["meta"]["platform"],
                    "parse_endpoint": result["meta"]["parse_endpoint"],
                    "resolved_video_url": result["meta"]["resolved_video_url"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        print(f"结构化 JSON 已输出到: {args.json_output}", file=sys.stderr)
        print(f"可读 Markdown 已输出到: {args.md_output}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
