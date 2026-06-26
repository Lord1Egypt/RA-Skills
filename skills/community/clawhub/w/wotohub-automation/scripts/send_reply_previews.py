#!/usr/bin/env python3
from __future__ import annotations
from typing import Optional

import argparse
import json
import subprocess
import sys
from pathlib import Path

from campaign_state_store import CampaignStateStore
from common import log_file
from conversation_state import mark_replied
from email_send_guardrails import validate_reply_preview_identity
from reply_safety import classify_reply_risk


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text())


def extract_reply_previews(data: dict) -> list[dict]:
    previews = data.get("replyPreviews") or []
    return [x for x in previews if isinstance(x, dict)]


def build_commands(previews: list[dict], dry_run: bool = False) -> list[dict]:
    commands = []
    for item in previews:
        blogger_id = item.get("bloggerId")
        reply_id = item.get("replyId")
        subject = item.get("subject") or ""
        body = item.get("htmlBody") or item.get("plainTextBody") or item.get("body") or ""
        analysis_mode = str(item.get("analysisMode") or "")
        risk = classify_reply_risk(item.get("latestMail") or item, item.get("classification") if isinstance(item.get("classification"), dict) else None)
        if not blogger_id or not reply_id or not subject or not body:
            continue
        if analysis_mode != "model-first":
            commands.append({
                "nickname": item.get("nickname"),
                "bloggerId": blogger_id,
                "chatId": item.get("chatId"),
                "replyId": reply_id,
                "subject": subject,
                "dry_run": dry_run,
                "risk": risk,
                "status": "blocked",
                "reason": "reply_model_analysis_required",
            })
            continue
        identity_check = validate_reply_preview_identity(item)
        if not identity_check.get("ok"):
            commands.append({
                "nickname": item.get("nickname"),
                "bloggerId": blogger_id,
                "chatId": item.get("chatId"),
                "replyId": reply_id,
                "subject": subject,
                "dry_run": dry_run,
                "risk": risk,
                "status": "blocked",
                "reason": identity_check.get("reason") or "reply_identity_guardrail_blocked",
            })
            continue
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "inbox.py"),
            "reply",
            "--blogger-ids", str(blogger_id),
            "--reply-id", str(reply_id),
            "--subject", subject,
            "--content", body,
        ]
        commands.append({
            "nickname": item.get("nickname"),
            "bloggerId": blogger_id,
            "chatId": item.get("chatId"),
            "replyId": reply_id,
            "subject": subject,
            "cmd": cmd,
            "dry_run": dry_run,
            "risk": risk,
        })
    return commands


def run_commands(commands: list[dict], campaign_id: Optional[str]= None) -> list[dict]:
    results = []
    store = CampaignStateStore(campaign_id) if campaign_id else None
    for item in commands:
        risk = item.get("risk") or {}
        if item.get("status") == "blocked":
            results.append(dict(item))
            if store:
                store.record_reply_action(item["replyId"], {
                    "bloggerId": item.get("bloggerId"),
                    "deliveryMode": "human_review",
                    "status": "blocked",
                    "reviewRequired": True,
                    "riskLevel": risk.get("riskLevel"),
                    "reasons": [(item.get("reason") or "reply_blocked")],
                })
            continue
        if not risk.get("autoSendAllowed"):
            blocked = {**item, "status": "blocked", "reason": "reply_risk_blocked"}
            results.append(blocked)
            if store:
                store.record_reply_action(item["replyId"], {
                    "bloggerId": item.get("bloggerId"),
                    "deliveryMode": "human_review",
                    "status": "blocked",
                    "reviewRequired": True,
                    "riskLevel": risk.get("riskLevel"),
                    "reasons": risk.get("reasons"),
                })
            continue
        if item["dry_run"]:
            results.append({**item, "status": "dry_run"})
            continue
        proc = subprocess.run(item["cmd"], capture_output=True, text=True)
        try:
            resp = json.loads(proc.stdout)
            code = str(resp.get("code", ""))
            success = code in {"0", "200"} or resp.get("success") is True
            status = "success" if success else "failed"
            result = {**item, "status": status, "response": resp}
            results.append(result)
            if success:
                mark_replied(
                    item["replyId"],
                    reply_id=item["replyId"],
                    auto=True,
                    metadata={"nickname": item.get("nickname"), "subject": item.get("subject")},
                    chat_id=item.get("chatId"),
                )
                if store:
                    store.record_reply_action(item["replyId"], {
                        "bloggerId": item.get("bloggerId"),
                        "deliveryMode": "auto_send",
                        "status": "sent",
                        "reviewRequired": False,
                        "riskLevel": risk.get("riskLevel"),
                        "reasons": risk.get("reasons"),
                    })
        except Exception as exc:
            results.append({**item, "status": "error", "error": str(exc), "stdout": proc.stdout[:200]})
    return results


def summarize(results: list[dict]) -> dict:
    ok = [r for r in results if r["status"] == "success"]
    fail = [r for r in results if r["status"] == "failed"]
    dry = [r for r in results if r["status"] == "dry_run"]
    blocked = [r for r in results if r["status"] == "blocked"]
    return {
        "ok": len(ok),
        "failed": len(fail),
        "dryRun": len(dry),
        "blocked": len(blocked),
    }


def main():
    ap = argparse.ArgumentParser(description="Send only low-risk model-first reply previews directly via inbox.py reply")
    ap.add_argument("input", help="generate_reply_preview.py output JSON file")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--campaign-id")
    args = ap.parse_args()

    data = load_json(args.input)
    previews = extract_reply_previews(data)
    commands = build_commands(previews, dry_run=args.dry_run)
    if args.limit > 0:
        commands = commands[:args.limit]
    if not commands:
        print("没有可发送的回复预览（检查 bloggerId / replyId / subject / body）", file=sys.stderr)
        sys.exit(1)

    results = run_commands(commands, campaign_id=args.campaign_id)
    summary = summarize(results)
    log_path = log_file("reply_sent_log.json")
    existing = json.loads(log_path.read_text()) if log_path.exists() else []
    existing.extend(results)
    log_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    print(json.dumps({"results": results, "summary": summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
