#!/usr/bin/env python3
"""Helpers for staged video suggestion and prompt building."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy


VIDEO_TYPES = [
    {
        "id": "cinematic-story",
        "number": 1,
        "name": "电影感剧情短片",
        "summary": "适合情绪推进、悬疑感、广告式叙事和镜头表达。",
        "template_lead": "Cinematic tone, story-first framing, layered lighting, deliberate camera movement.",
        "defaults": {
            "duration": 10,
            "ratio": "16:9",
            "motion": "medium",
            "style": "cinematic",
            "brightness": "normal",
            "subtitle": "off",
            "dream_filter": "off",
        },
        "keywords": {
            "剧情": 5,
            "故事": 5,
            "电影": 5,
            "悬疑": 4,
            "情感": 4,
            "预告片": 4,
            "叙事": 4,
            "广告": 3,
            "cinematic": 5,
            "story": 5,
            "drama": 4,
            "film": 4,
            "trailer": 4,
            "emotional": 4,
        },
    },
    {
        "id": "vertical-social",
        "number": 2,
        "name": "竖屏短视频爆款",
        "summary": "适合短视频平台、强节奏开头和竖屏传播场景。",
        "template_lead": "Vertical video, immediate hook in the first second, punchy rhythm, mobile-native framing.",
        "defaults": {
            "duration": 6,
            "ratio": "9:16",
            "motion": "strong",
            "style": "original",
            "brightness": "bright",
            "subtitle": "off",
            "dream_filter": "off",
        },
        "keywords": {
            "竖屏": 6,
            "短视频": 6,
            "抖音": 7,
            "小红书": 7,
            "快手": 7,
            "爆款": 5,
            "吸睛": 4,
            "开头": 3,
            "hook": 5,
            "viral": 5,
            "vertical": 6,
            "social": 4,
            "reel": 5,
            "short-form": 5,
        },
    },
    {
        "id": "landscape-atmosphere",
        "number": 3,
        "name": "唯美风景/氛围片",
        "summary": "适合风景、治愈、旅行、星空和氛围类内容。",
        "template_lead": "Atmospheric beauty, soft light, immersive scenery, slow cinematic drift.",
        "defaults": {
            "duration": 12,
            "ratio": "16:9",
            "motion": "light",
            "style": "cinematic",
            "brightness": "bright",
            "subtitle": "off",
            "dream_filter": "on",
        },
        "keywords": {
            "风景": 6,
            "治愈": 6,
            "旅行": 5,
            "星空": 6,
            "海边": 5,
            "森林": 5,
            "草地": 5,
            "雨": 3,
            "日落": 6,
            "雪山": 6,
            "氛围": 5,
            "landscape": 6,
            "atmosphere": 5,
            "nature": 5,
            "travel": 5,
            "sky": 4,
            "sunset": 6,
            "rain": 3,
        },
    },
    {
        "id": "commercial-product",
        "number": 4,
        "name": "动态产品展示/商业",
        "summary": "适合电商、品牌宣传、3C 产品和商业展示。",
        "template_lead": "Premium commercial look, product-focused composition, polished reflections, smooth transitions.",
        "defaults": {
            "duration": 8,
            "ratio": "16:9",
            "motion": "medium",
            "style": "realistic",
            "brightness": "bright",
            "subtitle": "off",
            "dream_filter": "off",
        },
        "keywords": {
            "产品": 7,
            "手机": 8,
            "耳机": 7,
            "口红": 7,
            "汽车": 7,
            "品牌": 6,
            "电商": 6,
            "展示": 5,
            "商业": 6,
            "宣传": 5,
            "product": 7,
            "commercial": 6,
            "brand": 6,
            "showcase": 5,
            "device": 6,
            "promo": 5,
        },
    },
    {
        "id": "abstract-experimental",
        "number": 5,
        "name": "抽象艺术/实验风",
        "summary": "适合 MV、赛博朋克、超现实和强风格实验画面。",
        "template_lead": "Bold experimental visuals, surreal motion, graphic forms, high style intensity.",
        "defaults": {
            "duration": 10,
            "ratio": "16:9",
            "motion": "strong",
            "style": "original",
            "brightness": "normal",
            "subtitle": "off",
            "dream_filter": "off",
        },
        "keywords": {
            "抽象": 7,
            "艺术": 6,
            "实验": 6,
            "赛博朋克": 7,
            "蒸汽波": 7,
            "超现实": 7,
            "几何": 5,
            "mv": 5,
            "abstract": 7,
            "experimental": 6,
            "surreal": 7,
            "cyberpunk": 7,
            "vaporwave": 7,
            "music video": 5,
        },
    },
]


STYLE_TEXT = {
    "realistic": "realistic texture, believable lighting, grounded physical detail",
    "anime": "anime-inspired shapes, crisp outlines, stylized color design",
    "cinematic": "cinematic lighting, depth, lens language, polished grading",
    "original": "preserve the user's original tone without over-stylizing",
}

MOTION_TEXT = {
    "light": "gentle drifting movement",
    "medium": "clear but controlled camera motion",
    "strong": "dynamic camera motion with fast visual energy",
}

BRIGHTNESS_TEXT = {
    "moody": "moody contrast and darker atmosphere",
    "normal": "balanced exposure and natural contrast",
    "bright": "bright and airy presentation",
}

SUBTITLE_TEXT = {
    "off": "no on-screen subtitle",
    "on": "include concise on-screen subtitle guidance if the model supports it",
}

DREAM_FILTER_TEXT = {
    "off": "no dreamy diffusion effect",
    "on": "enabled for a soft poetic glow",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Video intent suggestion and prompt builder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    suggest = subparsers.add_parser("suggest", help="Rank fixed video types for a user idea")
    suggest.add_argument("--input", required=True, help="Raw user idea")
    suggest.add_argument("--limit", type=int, default=4, help="How many ranked options to return (3-5 recommended)")
    suggest.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")

    build = subparsers.add_parser("build", help="Build a prompt preview for a chosen video type")
    build.add_argument("--input", required=True, help="Raw user idea")
    build.add_argument("--type", required=True, dest="type_id", help="Video type id")
    build.add_argument("--duration", type=int, choices=(5, 8, 10, 12), help="Target duration in seconds")
    build.add_argument("--ratio", choices=("9:16", "16:9", "1:1", "4:3"), help="Aspect ratio")
    build.add_argument("--motion", choices=("light", "medium", "strong"), help="Motion intensity")
    build.add_argument("--style", choices=("realistic", "anime", "cinematic", "original"), help="Style preference")
    build.add_argument("--brightness", choices=("moody", "normal", "bright"), help="Brightness preference")
    build.add_argument("--subtitle", choices=("off", "on"), help="Subtitle toggle")
    build.add_argument("--dream-filter", choices=("off", "on"), dest="dream_filter", help="Dream filter toggle")
    build.add_argument("--notes", action="append", default=[], help="Additional user notes")
    build.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")

    return parser.parse_args()


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def score_video_type(user_input: str, video_type: dict) -> tuple[int, list[str]]:
    text = normalize(user_input)
    score = 0
    hits = []
    for keyword, weight in video_type["keywords"].items():
        if keyword in text:
            score += weight
            hits.append(keyword)
    return score, hits


def build_reason(score: int, hits: list[str]) -> str:
    if hits:
        preview = ", ".join(hits[:4])
        return f"Matched keywords: {preview}"
    if score <= 0:
        return "No strong keyword hit, kept as a stable fallback option"
    return "Matched general intent"


def rank_video_types(user_input: str, limit: int) -> list[dict]:
    ranked = []
    for video_type in VIDEO_TYPES:
        score, hits = score_video_type(user_input, video_type)
        ranked.append((score, video_type["number"], video_type, hits))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    safe_limit = min(max(limit, 3), 5)

    results = []
    for rank, item in enumerate(ranked[:safe_limit], start=1):
        score, _number, video_type, hits = item
        results.append(
            {
                "rank": rank,
                "id": video_type["id"],
                "number": video_type["number"],
                "name": video_type["name"],
                "summary": video_type["summary"],
                "reason": build_reason(score, hits),
                "match_score": score,
                "defaults": deepcopy(video_type["defaults"]),
                "template_lead": video_type["template_lead"],
            }
        )
    return results


def get_video_type(type_id: str) -> dict:
    for video_type in VIDEO_TYPES:
        if video_type["id"] == type_id:
            return deepcopy(video_type)
    raise SystemExit(f"Unknown video type: {type_id}")


def merge_params(video_type: dict, args: argparse.Namespace) -> dict:
    params = deepcopy(video_type["defaults"])
    for key in ("duration", "ratio", "motion", "style", "brightness", "subtitle", "dream_filter"):
        value = getattr(args, key, None)
        if value is not None:
            params[key] = value
    return params


def build_prompt(user_input: str, video_type: dict, params: dict, notes: list[str]) -> str:
    sections = [
        video_type["template_lead"],
        f"Core idea: {user_input.strip()}.",
        f"Duration: {params['duration']}s.",
        f"Aspect ratio: {params['ratio']}.",
        f"Camera motion: {MOTION_TEXT[params['motion']]}.",
        f"Style: {STYLE_TEXT[params['style']]}.",
        f"Brightness: {BRIGHTNESS_TEXT[params['brightness']]}.",
        f"Dream filter: {DREAM_FILTER_TEXT[params['dream_filter']]}.",
        f"Subtitle: {SUBTITLE_TEXT[params['subtitle']]}.",
    ]
    for note in notes:
        cleaned = note.strip()
        if cleaned:
            sections.append(f"Additional user note: {cleaned}.")
    return " ".join(sections)


def make_state(user_input: str, stage: str, selected_type: str | None, params: dict, final_prompt: str) -> dict:
    return {
        "user_input": user_input,
        "selected_type": selected_type,
        "params": deepcopy(params),
        "final_prompt": final_prompt,
        "stage": stage,
    }


def format_markdown_suggestions(user_input: str, suggestions: list[dict]) -> str:
    lines = [f"Input idea: {user_input}", "", "Ranked video types:"]
    for item in suggestions:
        defaults = item["defaults"]
        lines.append(
            f"{item['rank']}. {item['name']} (`{item['id']}`) - {item['summary']} "
            f"Default: {defaults['duration']}s, {defaults['ratio']}. {item['reason']}."
        )
    return "\n".join(lines)


def format_markdown_build(video_type: dict, params: dict, prompt: str, notes: list[str]) -> str:
    lines = [
        f"Selected type: {video_type['name']} (`{video_type['id']}`)",
        "",
        "Current parameters:",
        f"- duration: {params['duration']}s",
        f"- ratio: {params['ratio']}",
        f"- motion: {params['motion']}",
        f"- style: {params['style']}",
        f"- brightness: {params['brightness']}",
        f"- subtitle: {params['subtitle']}",
        f"- dream_filter: {params['dream_filter']}",
    ]
    if notes:
        lines.append(f"- notes: {', '.join(note for note in notes if note.strip())}")
    lines.extend(["", "Prompt preview:", prompt])
    return "\n".join(lines)


def main() -> None:
    args = parse_args()

    if args.command == "suggest":
        suggestions = rank_video_types(args.input, args.limit)
        payload = {
            "user_input": args.input,
            "options": suggestions,
            "state": make_state(
                user_input=args.input,
                stage="choose_type",
                selected_type=None,
                params={},
                final_prompt="",
            ),
        }
        if args.format == "markdown":
            print(format_markdown_suggestions(args.input, suggestions))
            return
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "build":
        video_type = get_video_type(args.type_id)
        params = merge_params(video_type, args)
        prompt = build_prompt(args.input, video_type, params, args.notes)
        payload = {
            "user_input": args.input,
            "selected_type": {
                "id": video_type["id"],
                "number": video_type["number"],
                "name": video_type["name"],
                "summary": video_type["summary"],
            },
            "params": params,
            "notes": [note for note in args.notes if note.strip()],
            "prompt": prompt,
            "state": make_state(
                user_input=args.input,
                stage="confirm",
                selected_type=video_type["id"],
                params=params,
                final_prompt=prompt,
            ),
        }
        if args.format == "markdown":
            print(format_markdown_build(video_type, params, prompt, args.notes))
            return
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
