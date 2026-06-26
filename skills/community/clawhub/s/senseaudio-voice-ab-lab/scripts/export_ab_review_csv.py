#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a human-review CSV from AB manifest and TTS results.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--tts-results", required=True)
    parser.add_argument("--out-csv", required=True)
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    tts_results = json.loads(Path(args.tts_results).read_text(encoding="utf-8"))
    result_map = {item["variant_id"]: item for item in tts_results["results"]}

    rows = []
    for item in manifest["variants"]:
        audio = result_map.get(item["variant_id"], {})
        extra = audio.get("extra_info") or {}
        rows.append(
            {
                "campaign_name": manifest.get("campaign_name", ""),
                "variant_id": item["variant_id"],
                "tone": item["tone"],
                "regional_style": item["regional_style"],
                "voice_id": audio.get("voice_id", ""),
                "estimated_points": item.get("estimated_points", ""),
                "audio_length_ms": extra.get("audio_length", ""),
                "usage_characters": extra.get("usage_characters", ""),
                "audio_path": audio.get("out_path", ""),
                "hook_score_1_5": "",
                "clarity_score_1_5": "",
                "conversion_score_1_5": "",
                "regional_fit_score_1_5": "",
                "review_notes": "",
                "text": item["text"],
            }
        )

    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
