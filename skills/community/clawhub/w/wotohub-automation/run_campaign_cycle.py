#!/usr/bin/env python3
"""Cron-friendly WotoHub campaign cycle entrypoint.

Production bridge behavior for scheduled host-model draft generation:
- first run the deterministic engine
- if it pauses at waiting_for_host_drafts, optionally emit a host bridge payload
- if caller already provided generated drafts file, inject drafts and rerun automatically

This keeps the production entrypoint usable by cron / upper-layer orchestrators without
forcing them to reconstruct the request contract themselves.
"""
from __future__ import annotations

from typing import Union

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from campaign_engine import run_engine_from_brief  # type: ignore
from api_campaign_runner import CampaignRunner  # type: ignore


def _load_json(path: Union[str, Path]) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_json_or_text(value: str | None):
    if not value:
        return None
    candidate = Path(value)
    if candidate.exists():
        text = candidate.read_text(encoding="utf-8")
    else:
        text = value
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return text


def _load_host_drafts_artifact(path: Union[str, Path]) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"drafts": data, "metadata": {}}
    if isinstance(data, dict):
        metadata = data.get("writeBackMetadata") or data.get("hostDraftsMetadataPerCycle") or data.get("host_drafts_metadata_per_cycle") or {}
        if not isinstance(metadata, dict):
            metadata = {}
        for key in ("items", "host_drafts_per_cycle", "hostDraftsPerCycle", "hostDrafts", "emailModelDrafts"):
            items = data.get(key)
            if isinstance(items, list):
                return {"drafts": items, "metadata": metadata}
    return {"drafts": [], "metadata": {}}


def _write_json(path: Union[str, Path], payload: dict) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _decide_exit_code(result: dict) -> int:
    summary = result.get("summary") or {}
    search_summary = summary.get("search") or {}
    status_values = {
        str(result.get("status") or "").strip(),
        str((result.get("draftGeneration") or {}).get("status") or "").strip(),
        str((result.get("send") or {}).get("status") or "").strip(),
        str((result.get("replyActions") or {}).get("execution", {}).get("status") or "").strip(),
        str((result.get("replyStrictMode") or {}).get("status") or "").strip(),
    }
    status_values = {x for x in status_values if x}

    if result.get("error"):
        return 1
    if search_summary.get("success") is False:
        return 1
    if any(x in {"failed", "error"} for x in status_values):
        return 1
    if any(x in {"needs_user_input", "waiting_for_host_analysis", "waiting_for_external_host_analysis", "waiting_for_host_drafts", "waiting_for_host_reply_analysis", "review_required"} for x in status_values):
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Run one WotoHub campaign cycle")
    ap.add_argument("--campaign-id", required=True)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--token")
    ap.add_argument("--target-count", type=int, default=30)
    ap.add_argument("--page-size", type=int, default=10, help="Search page size per cycle (default: 10 for stable scheduled runs; increase to 20-30 when you need more recall)")
    ap.add_argument("--mode", choices=["single_cycle", "scheduled_cycle"], default="single_cycle")
    ap.add_argument("--send-policy", choices=["prepare_only", "manual_send", "scheduled_send"], default=None, help="Outreach send policy (default: scheduled_send for scheduled_cycle, prepare_only otherwise)")
    ap.add_argument("--reply-send-policy", choices=["prepare_only", "safe_auto_send", "human_only"], default=None, help="Reply send policy (default: safe_auto_send for scheduled cycles with low-risk-only auto replies, human_only for manual cycles)")
    review_group = ap.add_mutually_exclusive_group()
    review_group.add_argument("--review-required", dest="review_required", action="store_true", default=None, help="Force human review before send execution")
    review_group.add_argument("--no-review-required", dest="review_required", action="store_false", help="Allow execution without human review if policy permits")
    ap.add_argument("--timing", default="", help="Optional scheduled send time, format yyyy-MM-dd HH:mm:ss")
    ap.add_argument("--host-analysis-bridge-payload", help="When waiting_for_host_analysis, write hostAnalysis bridge payload JSON to this path")
    ap.add_argument("--host-analysis-bridge-request", help="When waiting_for_host_analysis, also write raw hostAnalysisRequest JSON to this path")
    ap.add_argument("--host-analysis-bridge-executor", help="Auto-run a bridge executor when waiting_for_host_analysis. Accepts either a command string with {input}/{output}/{skill_root} placeholders, or a JSON file / JSON object with command|args|timeoutSeconds|cwd|env.")
    ap.add_argument("--host-bridge-payload", help="When waiting_for_host_drafts, write hostModelBridgePayload JSON to this path")
    ap.add_argument("--host-bridge-drafts", help="JSON file containing generated drafts (array or {items:[...]}); when provided, inject into host_drafts_per_cycle and rerun automatically")
    ap.add_argument("--host-bridge-request", help="When waiting_for_host_drafts, also write raw hostDraftGenerationRequest JSON to this path")
    ap.add_argument("--host-bridge-executor", help="Auto-run a bridge executor when waiting_for_host_drafts. Accepts either a command string with {input}/{output}/{skill_root} placeholders, or a JSON file / JSON object with command|args|timeoutSeconds|cwd|env.")
    ap.add_argument("--output")
    args = ap.parse_args()

    runner = CampaignRunner()
    brief = _load_json(args.brief)
    host_drafts_artifact = _load_host_drafts_artifact(args.host_bridge_drafts) if args.host_bridge_drafts else {"drafts": [], "metadata": {}}

    result = runner.run_cycle(
        args.campaign_id,
        brief,
        {
            "token": args.token,
            "targetCount": args.target_count,
            "mode": args.mode,
            "pageSize": args.page_size,
            "sendPolicy": args.send_policy,
            "replySendPolicy": args.reply_send_policy,
            "reviewRequired": args.review_required,
            "timing": args.timing,
            **({"hostAnalysisExecutor": _load_json_or_text(args.host_analysis_bridge_executor)} if args.host_analysis_bridge_executor else {}),
            **({"host_drafts_per_cycle": host_drafts_artifact.get("drafts") or []} if args.host_bridge_drafts else {}),
            **({"host_drafts_metadata_per_cycle": host_drafts_artifact.get("metadata") or {}} if args.host_bridge_drafts and host_drafts_artifact.get("metadata") else {}),
            **({"hostBridgeExecutor": _load_json_or_text(args.host_bridge_executor)} if args.host_bridge_executor else {}),
        },
    )

    host_analysis_request = result.get("hostAnalysisRequest")
    if host_analysis_request and args.host_analysis_bridge_request:
        _write_json(args.host_analysis_bridge_request, host_analysis_request)

    if host_analysis_request and args.host_analysis_bridge_payload:
        bridge_payload = runner.build_host_analysis_bridge_payload(request=host_analysis_request, skill_root=Path(__file__).resolve().parent)
        _write_json(args.host_analysis_bridge_payload, bridge_payload)

    host_request = result.get("hostDraftGenerationRequest")
    if host_request and args.host_bridge_request:
        _write_json(args.host_bridge_request, host_request)

    if host_request and args.host_bridge_payload:
        bridge_payload = runner.build_host_model_bridge_payload(request=host_request, skill_root=Path(__file__).resolve().parent)
        _write_json(args.host_bridge_payload, bridge_payload)

    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return _decide_exit_code(result)


def legacy_main() -> int:
    ap = argparse.ArgumentParser(description="Run one WotoHub campaign cycle")
    ap.add_argument("--campaign-id", required=True)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--token")
    ap.add_argument("--target-count", type=int, default=30)
    ap.add_argument("--page-size", type=int, default=10, help="Search page size per cycle (default: 10 for stable scheduled runs; increase to 20-30 when you need more recall)")
    ap.add_argument("--mode", choices=["single_cycle", "scheduled_cycle"], default="single_cycle")
    ap.add_argument("--send-policy", choices=["prepare_only", "manual_send", "scheduled_send"], default=None, help="Outreach send policy (default: scheduled_send for scheduled_cycle, prepare_only otherwise)")
    ap.add_argument("--reply-send-policy", choices=["prepare_only", "safe_auto_send", "human_only"], default=None, help="Reply send policy (default: safe_auto_send for scheduled cycles with low-risk-only auto replies, human_only for manual cycles)")
    review_group = ap.add_mutually_exclusive_group()
    review_group.add_argument("--review-required", dest="review_required", action="store_true", default=None, help="Force human review before send execution")
    review_group.add_argument("--no-review-required", dest="review_required", action="store_false", help="Allow execution without human review if policy permits")
    ap.add_argument("--timing", default="", help="Optional scheduled send time, format yyyy-MM-dd HH:mm:ss")
    ap.add_argument("--output")
    args = ap.parse_args()

    result = run_engine_from_brief(
        campaign_id=args.campaign_id,
        brief_path=args.brief,
        token=args.token,
        target_count=args.target_count,
        mode=args.mode,
        page_size=args.page_size,
        send_policy=args.send_policy,
        reply_send_policy=args.reply_send_policy,
        review_required=args.review_required,
        timing=args.timing,
    )
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return _decide_exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
