#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


RELATION_STYLES = {
    "stranger": {"address": "旅人", "warmth": "reserved"},
    "neutral": {"address": "朋友", "warmth": "steady"},
    "trusted": {"address": "老朋友", "warmth": "warm"},
    "ally": {"address": "搭档", "warmth": "close"},
}


INTENT_RULES = [
    ("accept", ["我接", "交给我", "我去", "我来", "收到", "可以", "行"]),
    ("ask_info", ["在哪", "怎么做", "怎么走", "什么情况", "再说一遍", "线索", "细说"]),
    ("refuse", ["不去", "不接", "没空", "算了", "下次吧"]),
    ("thanks", ["谢谢", "辛苦", "多谢"]),
    ("hostile", ["烦", "闭嘴", "滚", "别吵", "少废话"]),
]


def clean(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", "", text)
    return text.strip("，。,；;：: ")


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_RULES:
        if any(keyword in text for keyword in keywords):
            return intent
    return "discuss"


def build_lines(profile: dict, relationship: str, intent: str, transcript: str, location: str, objective: str) -> list[dict]:
    relation = RELATION_STYLES[relationship]
    address = relation["address"]
    catchphrase = clean(profile.get("catchphrase", ""))
    catchphrase_prefix = f"{catchphrase}。" if catchphrase else ""
    location = clean(location)
    objective = clean(objective)

    if intent == "accept":
        texts = [
            f"{catchphrase_prefix}{address}，那我就把真线索交给你。目标还是{objective}，先去{location}，别让风声跑在你前面。",
            f"{catchphrase_prefix}你既然接了，我就不绕弯。到了{location}先看痕迹，再决定怎么动手。",
        ]
    elif intent == "ask_info":
        texts = [
            f"{catchphrase_prefix}{address}，你问得对。重点不是硬闯，是先摸清{location}那边的动静，目标始终是{objective}。",
            f"{catchphrase_prefix}我再说直白点，先到{location}找线索，再围着{objective}这件事收口。",
        ]
    elif intent == "refuse":
        texts = [
            f"{catchphrase_prefix}{address}，这回你若不接，我会另找人手。但{location}那边不会等太久。",
            f"{catchphrase_prefix}我尊重你的决定，不过{objective}这件事一旦拖久，麻烦会更大。",
        ]
    elif intent == "thanks":
        texts = [
            f"{catchphrase_prefix}{address}，客气的话先放一边。真要谢我，就把{objective}办稳，别让{location}白起风。",
            f"{catchphrase_prefix}等你把事办妥，我们再慢慢说。现在先盯紧{location}。",
        ]
    elif intent == "hostile":
        texts = [
            f"{catchphrase_prefix}{address}，火气留着也解决不了事。你若还想推进{objective}，就先把注意力放回{location}。",
            f"{catchphrase_prefix}我只提醒一次，局势比脾气重要。想继续谈，就按线索去{location}。",
        ]
    else:
        texts = [
            f"{catchphrase_prefix}{address}，我听见你的意思了。现在最要紧的还是{objective}，而突破口在{location}。",
            f"{catchphrase_prefix}你若还有顾虑，可以边走边问。但先去{location}，别让事件脱手。",
        ]

    lines = []
    for idx, text in enumerate(texts, start=1):
        lines.append(
            {
                "line_id": f"L{idx:02d}",
                "event_type": "player_reply",
                "relationship": relationship,
                "npc_name": profile["npc_name"],
                "voice_id": profile["voice_id"],
                "intent": intent,
                "player_transcript": transcript,
                "text": text,
            }
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Build NPC reply lines from a player transcript.")
    parser.add_argument("--profile-json", required=True)
    parser.add_argument("--player-transcript-json", required=True)
    parser.add_argument("--relationship", default="neutral", choices=sorted(RELATION_STYLES.keys()))
    parser.add_argument("--location", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    profile = json.loads(Path(args.profile_json).read_text(encoding="utf-8"))
    transcript_payload = json.loads(Path(args.player_transcript_json).read_text(encoding="utf-8"))
    transcript = clean(
        transcript_payload.get("transcript")
        or transcript_payload.get("text")
        or transcript_payload.get("raw_response", {}).get("text")
        or ""
    )
    if not transcript:
        raise SystemExit("Transcript is empty.")

    intent = detect_intent(transcript)
    result = {
        "npc_profile": profile,
        "scene": {
            "event_type": "player_reply",
            "relationship": args.relationship,
            "location": args.location,
            "objective": args.objective,
            "player_transcript": transcript,
            "intent": intent,
        },
        "lines": build_lines(profile, args.relationship, intent, transcript, args.location, args.objective),
    }

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
