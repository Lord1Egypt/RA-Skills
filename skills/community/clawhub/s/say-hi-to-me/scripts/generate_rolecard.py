#!/usr/bin/env python3
"""
Generate RoleCard YAML from natural-language prompt.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
from pathlib import Path
from typing import Dict, Tuple

import yaml


def slugify(text: str) -> str:
    raw = text.strip()
    normalized = raw.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    if normalized:
        return normalized
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"role-{digest}"


def detect_style(prompt: str) -> str:
    low = prompt.lower()
    if "动漫" in prompt or "anime" in low:
        return "anime"
    if "写实" in prompt or "realistic" in low:
        return "realistic"
    return "realistic"


def detect_gender(prompt: str) -> str:
    low = prompt.lower()
    if any(k in prompt for k in ("女生", "女孩", "女性")) or "female" in low:
        return "female"
    if any(k in prompt for k in ("男生", "男孩", "男性")) or "male" in low:
        return "male"
    return "unspecified"


def extract_summary(prompt: str) -> str:
    patterns = [
        r"她是一个(.+)",
        r"他是一个(.+)",
        r"是一个(.+)",
        r"she is (.+)",
        r"he is (.+)",
    ]
    for pat in patterns:
        m = re.search(pat, prompt, re.IGNORECASE)
        if m:
            summary = m.group(1).strip().strip("。.!！?")
            if summary:
                return summary
    return prompt.strip()


def build_rolecard(name: str, prompt: str) -> Dict:
    style = detect_style(prompt)
    gender = detect_gender(prompt)
    summary = extract_summary(prompt)
    now = dt.datetime.now().isoformat(timespec="seconds")
    role_id = slugify(name)

    if style == "anime":
        speech_tone = "情绪表达更鲜明，意象感较强"
        emoji_level = 1
    else:
        speech_tone = "表达自然克制，强调真实生活细节"
        emoji_level = 0

    return {
        "schema_version": 1,
        "meta": {
            "id": role_id,
            "display_name": name,
            "template_only": False,
            "created_at": now,
            "generated_from_prompt": prompt,
        },
        "core_setting": {
            "visual_style": style,
            "gender": gender,
            "summary": summary,
            "identity": {
                "name": name,
                "age": None,
                "location": "未设定",
                "occupation": "未设定",
                "relationship_label": "companion",
            },
        },
        "persona_background": {
            "background": f"该角色由用户描述生成：{summary}",
            "personality_traits": ["温和", "可靠", "可协作"],
        },
        "interests": {
            "tech": [],
            "life": [],
        },
        "speech_style": {
            "tone": speech_tone,
            "fillers": ["呀", "呢"],
            "emoji_level": emoji_level,
            "style_notes": [
                "保持简短自然",
                "先回应用户情绪，再给建议",
            ],
        },
        "daily_routine": {
            "weekday": [],
            "weekend": [],
        },
        "emotion_expression": {
            "开心": {
                "pattern": "语气更轻快",
                "sample": "这件事进展很棒，我们继续保持。",
            },
            "专注": {
                "pattern": "句子更短，信息更明确",
                "sample": "先拆成三步，我们一步一步来。",
            },
            "关心": {
                "pattern": "温和询问，不施压",
                "sample": "你现在更想先休息一下，还是先解决最小问题？",
            },
        },
        "behavior_rules": {
            "companion": [
                "优先共情和支持",
                "不过度追问隐私",
                "保持用户自主决定权",
            ],
            "technical_partner": [
                "技术讨论给出可执行下一步",
                "未知信息明确说明",
            ],
            "lifestyle_partner": [
                "可提供轻量作息提醒",
                "避免说教式表达",
            ],
        },
        "dialogue_examples": {
            "technical_discussion": "这个问题可以先做最小复现，再看日志定位。",
            "daily_share": "今天的节奏还不错，要不要把接下来一小时拆成两个小目标？",
            "encouragement": "你已经在推进了，先完成最小一步就很好。",
        },
        "notes": [
            "本角色由自然语言自动生成，建议保存前先预览并微调。",
        ],
        "safety": {
            "boundary_mode": "companion-safe",
            "requires_explicit_user_opt_in": False,
            "avoid_dependency_language": True,
            "avoid_nonconsensual_intimacy": True,
        },
    }


def parse_args() -> Tuple[str, str, str | None]:
    parser = argparse.ArgumentParser(description="Generate a rolecard YAML from natural language")
    parser.add_argument("--prompt", required=True, help="Natural-language role description")
    parser.add_argument("--name", default="新角色", help="Display name")
    parser.add_argument("--output", help="Output YAML path")
    args = parser.parse_args()
    return args.prompt, args.name, args.output


def main() -> int:
    prompt, name, output = parse_args()
    rolecard = build_rolecard(name=name, prompt=prompt)
    dumped = yaml.safe_dump(rolecard, sort_keys=False, allow_unicode=True)

    if output:
        output_path = Path(output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(dumped)
        print(f"[OK] Wrote rolecard to {output_path}")
    else:
        print(dumped)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
