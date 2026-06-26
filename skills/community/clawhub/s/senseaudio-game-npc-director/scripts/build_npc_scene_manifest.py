#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


RELATION_STYLES = {
    "stranger": {
        "address": "旅人",
        "warmth": "reserved",
        "trust_line": "规矩先听清楚，再往前走。",
    },
    "neutral": {
        "address": "朋友",
        "warmth": "steady",
        "trust_line": "照流程做，事情就会顺很多。",
    },
    "trusted": {
        "address": "老朋友",
        "warmth": "warm",
        "trust_line": "你来得正好，这次我就直说重点。",
    },
    "ally": {
        "address": "搭档",
        "warmth": "close",
        "trust_line": "有你在，这件事我就放心多了。",
    },
}


EVENT_TEMPLATES = {
    "quest_offer": [
        "{catchphrase}{address}，{location}那边出了点状况。{objective}，你若愿意接手，我现在就把线索交给你。",
        "{catchphrase}{trust_line}{objective}，办成之后，{reward}。",
    ],
    "quest_update": [
        "{catchphrase}{address}，{objective}这件事有新动静了。{event_detail}",
        "{catchphrase}先别松劲，{next_step}",
    ],
    "world_event": [
        "{catchphrase}{location}全域注意。{event_detail}",
        "{catchphrase}{address}，若你还在外面活动，{next_step}",
    ],
    "ambient_broadcast": [
        "{catchphrase}这里是{location}的例行播报。{event_detail}",
        "{catchphrase}{address}，今天的风向不太对，{next_step}",
    ],
}


def clean(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[。.!?！？]+$", "", text)
    return text


def join_sentence(text: str) -> str:
    text = clean(text)
    return f"{text}。" if text else ""


def render(template: str, data: dict) -> str:
    text = template.format(**data)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"。+", "。", text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an NPC scene manifest.")
    parser.add_argument("--profile-json", required=True)
    parser.add_argument("--event-type", required=True, choices=sorted(EVENT_TEMPLATES.keys()))
    parser.add_argument("--relationship", default="neutral", choices=sorted(RELATION_STYLES.keys()))
    parser.add_argument("--objective", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--event-detail", default="")
    parser.add_argument("--next-step", default="先去高处观察，再决定下一步")
    parser.add_argument("--reward", default="报酬我会照规矩给足")
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    profile = json.loads(Path(args.profile_json).read_text(encoding="utf-8"))
    relation = RELATION_STYLES[args.relationship]
    data = {
        "npc_name": profile["npc_name"],
        "role": profile["role"],
        "world": profile["world"],
        "voice_id": profile["voice_id"],
        "catchphrase": join_sentence(profile.get("catchphrase", "")),
        "address": relation["address"],
        "trust_line": relation["trust_line"],
        "location": clean(args.location),
        "objective": clean(args.objective),
        "event_detail": join_sentence(args.event_detail),
        "next_step": join_sentence(args.next_step),
        "reward": clean(args.reward),
    }

    lines = []
    for idx, template in enumerate(EVENT_TEMPLATES[args.event_type], start=1):
        lines.append(
            {
                "line_id": f"L{idx:02d}",
                "event_type": args.event_type,
                "relationship": args.relationship,
                "npc_name": profile["npc_name"],
                "voice_id": profile["voice_id"],
                "text": render(template, data),
            }
        )

    result = {
        "npc_profile": profile,
        "scene": {
            "event_type": args.event_type,
            "relationship": args.relationship,
            "location": args.location,
            "objective": args.objective,
            "event_detail": args.event_detail,
            "next_step": args.next_step,
        },
        "lines": lines,
    }

    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
