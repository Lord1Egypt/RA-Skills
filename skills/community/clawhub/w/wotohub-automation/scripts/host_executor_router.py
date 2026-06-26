#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
for path in (SCRIPT_DIR, SKILL_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import host_analysis_executor_example as analysis_example
import host_reply_analysis_executor_example as reply_example
import host_draft_executor_example as draft_example
import host_model_bridge_executor_example as cycle_draft_example


ANALYSIS_MODES = {"host_analysis_request", "host_url_analysis_request"}
REPLY_MODES = {"host_reply_analysis_request", "host_reply_bridge_payload"}
DRAFT_MODES = {"host_draft_request"}
BRIDGE_DRAFT_MODES = {"host_bridge_payload"}


def _load_json(path: str | Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("router input must be a JSON object")
    return payload


def _write_json(path: str | Path | None, payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if path:
        Path(path).write_text(text, encoding="utf-8")
    print(text)


def _normalize_cycle_draft_payload(payload: dict) -> dict:
    drafts = payload.get("host_drafts_per_cycle") or payload.get("hostDrafts") or payload.get("items") or []
    metadata = payload.get("writeBackMetadata") or payload.get("hostDraftsMetadataPerCycle") or payload.get("host_drafts_metadata_per_cycle") or {}
    return {
        "hostDrafts": drafts,
        "writeBackMetadata": metadata,
        "messageSamples": payload.get("messageSamples") or [],
        "mode": payload.get("mode"),
        "targetCount": payload.get("targetCount"),
    }


def _route_mode(request: dict) -> str:
    mode = str(request.get("mode") or "").strip()
    if mode in ANALYSIS_MODES | REPLY_MODES | DRAFT_MODES | BRIDGE_DRAFT_MODES:
        return mode
    write_back_field = str(((request.get("writeBack") or {}).get("field")) or "").strip()
    if write_back_field in {"host_analysis", "hostAnalysis", "productSummary"}:
        return "host_analysis_request"
    if write_back_field in {"reply_model_analysis", "replyModelAnalysis"}:
        return "host_reply_analysis_request"
    if write_back_field in {"host_drafts_per_cycle", "hostDrafts", "drafts"}:
        return "host_bridge_payload"
    raise ValueError(f"Unsupported router mode: {mode or '<empty>'}")


def dispatch(request: dict) -> dict:
    mode = _route_mode(request)
    if mode in ANALYSIS_MODES:
        host_analysis = analysis_example._build_host_analysis(request)
        result = {
            "hostAnalysis": host_analysis,
            "productSummary": analysis_example._summary_from_analysis(
                host_analysis,
                source_url=request.get("rawInput") or ((request.get("input") or {}).get("url")),
            ),
        }
    elif mode in REPLY_MODES:
        items = [reply_example._build_item(item) for item in reply_example._normalize_items(request)]
        result = {"replyModelAnalysis": {"items": items}}
    elif mode in DRAFT_MODES:
        creators = [item for item in (request.get("selectedCreators") or []) if isinstance(item, dict)]
        brief = request.get("brief") or {}
        language = request.get("emailLanguage") or "en"
        drafts = [draft_example._draft_for_creator(creator, brief, language) for creator in creators]
        result = {
            "hostDrafts": drafts,
            "writeBackMetadata": {
                "selectedCreatorCount": len(creators),
                "generatedDraftCount": len(drafts),
                "uniqueBloggerIdCount": len({x.get("bloggerId") for x in drafts}),
                "missingBloggerIds": [],
                "duplicateBloggerIds": [],
                "unexpectedBloggerIds": [],
            },
        }
    elif mode in BRIDGE_DRAFT_MODES:
        bridge_payload = request
        runner = cycle_draft_example.CampaignRunner()
        executor_example = runner.build_host_model_executor_example(bridge_payload=bridge_payload)
        default_language = ((bridge_payload.get("generationPlan") or {}).get("defaultLanguage")) or "en"
        drafts = [
            cycle_draft_example._mock_draft_from_creator(creator, default_language=default_language)
            for creator in (bridge_payload.get("selectedCreators") or [])
            if isinstance(creator, dict)
        ]
        raw = {
            **runner.build_host_drafts_writeback(bridge_payload=bridge_payload, drafts=drafts),
            "messageSamples": executor_example.get("messageSamples") or [],
            "mode": "mock",
            "targetCount": len(bridge_payload.get("selectedCreators") or []),
        }
        result = _normalize_cycle_draft_payload(raw)
    else:
        raise ValueError(f"Unsupported router mode after normalization: {mode}")

    result["executorMeta"] = {
        **(result.get("executorMeta") or {}),
        "routerMode": mode,
        "routerExample": True,
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Unified example host executor router for WotoHub")
    ap.add_argument("--input", required=True, help="Path to request JSON")
    ap.add_argument("--output", help="Path to write router output JSON")
    args = ap.parse_args()

    request = _load_json(args.input)
    result = dispatch(request)
    _write_json(args.output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
