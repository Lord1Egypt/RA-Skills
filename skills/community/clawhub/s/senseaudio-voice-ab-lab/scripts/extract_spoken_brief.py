#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


FIELD_PATTERNS = {
    "campaign_name": [r"(?:活动名|项目名|campaign)[：: ]+([^。；;\n]+)"],
    "product": [r"(?:产品|商品|品类)(?:是|为)?[：:，,｜| ]+([^。；;\n]+)"],
    "audience": [r"(?:人群|受众|客户|目标用户)(?:是|为)?[：:，, ]+([^。；;\n]+)"],
    "key_message": [r"(?:卖点|核心卖点|重点|主打)(?:是|为)?[：:，, ]+([^。；;\n]+)"],
    "offer": [r"(?:优惠|福利|价格|活动)(?:是|为)?[：:，, ]+([^。；;\n]+)"],
    "cta": [r"(?:行动|行动指令|cta|引导)(?:是|为)?[：:，, ]+([^。；;\n]+)"],
    "proof": [r"(?:证明|背书|信任点|数据)(?:是|为)?[：:，, ]+([^。；;\n]+)"],
}


def clean(value: str) -> str:
    value = re.sub(r"\s+", "", value)
    return value.strip("，。,；;：: ")


def extract_field(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return clean(match.group(1))
    return ""


def postprocess_brief(brief: dict, transcript: str) -> dict:
    if "产品" in brief.get("campaign_name", "") and not brief.get("product"):
        merged = re.search(r"活动名[：: ]+(.+?)(?:产品[：:｜| ]+)(.+)", brief["campaign_name"])
        if merged:
            brief["campaign_name"] = clean(merged.group(1))
            brief["product"] = clean(merged.group(2))
    if "产品" in brief.get("campaign_name", "") and brief.get("product"):
        merged = re.search(r"(.+?)(?:产品[：:｜| ]+)(.+)", brief["campaign_name"])
        if merged:
            brief["campaign_name"] = clean(merged.group(1))

    if brief.get("offer", "").endswith("行动"):
        brief["offer"] = clean(re.sub(r"行动$", "", brief["offer"]))

    if not brief.get("cta"):
        lines = [clean(line) for line in transcript.splitlines() if clean(line)]
        for index, line in enumerate(lines):
            if line.endswith("行动") and index + 1 < len(lines):
                brief["cta"] = clean(lines[index + 1])
                break

    if not brief.get("key_message"):
        key_line = re.search(r"卖点[：: ]+(.+)", transcript)
        if key_line:
            brief["key_message"] = clean(key_line.group(1))

    return brief


def fallback_campaign_name(product: str, audience: str) -> str:
    if product and audience:
        return f"{product}-{audience}-语音测款"
    if product:
        return f"{product}-语音测款"
    return "spoken-brief-campaign"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a structured campaign brief from an ASR transcript.")
    parser.add_argument("--transcript-json", required=True)
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.transcript_json).read_text(encoding="utf-8"))
    transcript = payload.get("transcript") or payload.get("text") or payload.get("raw_response", {}).get("text") or ""
    transcript = transcript.strip()
    if not transcript:
        raise SystemExit("Transcript is empty.")

    brief = {field: extract_field(transcript, patterns) for field, patterns in FIELD_PATTERNS.items()}
    brief = postprocess_brief(brief, transcript)
    if not brief["campaign_name"]:
        brief["campaign_name"] = fallback_campaign_name(brief["product"], brief["audience"])

    required = ["product", "audience", "key_message", "cta"]
    missing = [field for field in required if not brief[field]]
    result = {
        **brief,
        "source": "spoken_transcript",
        "source_transcript": transcript,
        "missing_fields": missing,
        "parse_ready": not missing,
    }

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
