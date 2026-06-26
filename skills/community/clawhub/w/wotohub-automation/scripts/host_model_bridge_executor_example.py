#!/usr/bin/env python3
"""Minimal host-side executor example for hostModelBridgePayload.

This bridge is intentionally production-connectable even though the default generation
mode is mock/example.

What it does:
1. read hostModelBridgePayload JSON
2. build one model-style request per creator
3. generate draft objects (mock/example mode by default)
4. write standard `host_drafts_per_cycle` JSON that run_campaign_cycle.py can consume

This lets upper-layer orchestration wire the full loop today:
payload.json -> executor -> drafts.json -> scheduled_cycle rerun
"""

from __future__ import annotations

from typing import Union

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
for path in (SCRIPT_DIR, SKILL_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from api_campaign_runner import CampaignRunner


def _mock_draft_from_creator(creator: dict, default_language: str = "en") -> dict:
    nickname = creator.get("nickname") or creator.get("bloggerName") or creator.get("channelName") or "there"
    blogger_id = creator.get("bloggerId") or creator.get("id") or ""
    return {
        "bloggerId": blogger_id,
        "nickname": nickname,
        "language": default_language,
        "style": "creator-friendly-natural",
        "subject": f"Collab idea for {nickname}",
        "htmlBody": f"<p>Hi {nickname},</p><p>Would love to explore a collaboration with you.</p>",
        "plainTextBody": f"Hi {nickname},\n\nWould love to explore a collaboration with you.",
        "styleReason": "example_executor_mock_output",
    }


def _write_json(path: Union[str, Path], payload: dict) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Example host bridge executor for hostModelBridgePayload")
    ap.add_argument("--input", required=True, help="Path to hostModelBridgePayload JSON")
    ap.add_argument("--output", help="Path to write generated drafts JSON")
    ap.add_argument("--mode", choices=["mock", "echo"], default="mock", help="mock: generate simple example drafts; echo: only emit message samples, no drafts")
    args = ap.parse_args()

    payload_path = Path(args.input).resolve()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    runner = CampaignRunner()

    executor_example = runner.build_host_model_executor_example(bridge_payload=payload)
    drafts = []
    default_language = ((payload.get("generationPlan") or {}).get("defaultLanguage")) or "en"
    if args.mode == "mock":
        for creator in payload.get("selectedCreators") or []:
            drafts.append(_mock_draft_from_creator(creator, default_language=default_language))

    result = {
        **runner.build_host_drafts_writeback(bridge_payload=payload, drafts=drafts),
        "messageSamples": executor_example.get("messageSamples") or [],
        "mode": args.mode,
        "targetCount": len(payload.get("selectedCreators") or []),
    }
    if args.output:
        _write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
