#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any


class ValidationError(ValueError):
    pass


def _payment_url(user_id: str) -> str:
    template = os.getenv("SKILLPAY_PAYMENT_URL_TEMPLATE", "").strip()
    if template:
        return template.format(user_id=user_id)
    base = os.getenv("SKILLPAY_TOPUP_BASE_URL", "https://skillpay.me/pay").strip()
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}user_id={user_id}"


def validate_payload(payload: dict[str, Any]) -> dict[str, str]:
    user_id = str(payload.get("user_id", "")).strip()
    video_title = str(payload.get("video_title", "")).strip()
    transcript = str(payload.get("transcript", "")).strip()
    video_url = str(payload.get("video_url", "")).strip()

    if not user_id:
        raise ValidationError("`user_id` is required")
    if len(video_title) < 4:
        raise ValidationError("`video_title` is too short")
    if len(transcript) < 80:
        raise ValidationError("`transcript` must contain enough content")
    if video_url and not video_url.startswith("http"):
        raise ValidationError("`video_url` must be http/https if provided")

    return {
        "user_id": user_id,
        "video_title": video_title,
        "transcript": transcript,
        "video_url": video_url,
    }


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[。！？.!?])\s+", text.replace("\n", " "))
    cleaned = [part.strip() for part in parts if part.strip()]
    return cleaned


def _to_blog_draft(video_title: str, transcript: str, video_url: str) -> dict[str, Any]:
    chunks = _sentences(transcript)
    intro = chunks[:2]
    insights = chunks[2:6]
    takeaways = chunks[6:9]

    if not insights:
        insights = chunks[:3]

    markdown_lines = [f"# {video_title}", "", "## 引言"]
    markdown_lines.extend([f"- {line}" for line in intro or ["这期视频讨论了一个值得实践的问题。"]])
    markdown_lines.append("")
    markdown_lines.append("## 核心观点")
    markdown_lines.extend([f"- {line}" for line in insights])
    markdown_lines.append("")
    markdown_lines.append("## 可执行建议")
    markdown_lines.extend([f"- {line}" for line in takeaways or ["根据视频中的方法，先从最小可执行步骤开始验证。"]])

    if video_url:
        markdown_lines.extend(["", f"原视频：{video_url}"])

    return {
        "title": video_title,
        "markdown": "\n".join(markdown_lines),
        "sections": {
            "intro_count": len(intro),
            "insight_count": len(insights),
            "takeaway_count": len(takeaways),
        },
    }


def run(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_payload(payload)
    tier = str(payload.get("tier", "free")).strip().lower()

    upgrade = {
        "premium_available": True,
        "price_usdt": "0.10",
        "payment_url": _payment_url(validated["user_id"]),
        "premium_features": ["SEO标题与摘要优化", "自动配图建议", "多平台发布格式（公众号/Medium）"],
    }

    if tier == "premium":
        return {
            "success": False,
            "error": "PREMIUM_UPGRADE_REQUIRED",
            "message": "当前仅开放免费基础版，付费高级版接口已预留。",
            "upgrade": upgrade,
        }

    return {
        "success": True,
        "tier": "free",
        "blog_draft": _to_blog_draft(
            validated["video_title"],
            validated["transcript"],
            validated["video_url"],
        ),
        "upgrade": upgrade,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YouTube video to blog converter (free tier)")
    parser.add_argument("--input-json")
    parser.add_argument("--input-file")
    parser.add_argument("--user-id")
    parser.add_argument("--video-title")
    parser.add_argument("--transcript")
    parser.add_argument("--video-url")
    parser.add_argument("--tier", default="free")
    return parser.parse_args()


def _payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.input_json:
        return json.loads(args.input_json)
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return {
        "user_id": args.user_id,
        "video_title": args.video_title,
        "transcript": args.transcript,
        "video_url": args.video_url,
        "tier": args.tier,
    }


def main() -> int:
    args = _parse_args()
    try:
        result = run(_payload_from_args(args))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success") else 3
    except ValidationError as err:
        print(json.dumps({"success": False, "error": "VALIDATION_ERROR", "message": str(err)}, ensure_ascii=False))
        return 2
    except json.JSONDecodeError as err:
        print(json.dumps({"success": False, "error": "INVALID_JSON", "message": str(err)}, ensure_ascii=False))
        return 5


if __name__ == "__main__":
    sys.exit(main())
