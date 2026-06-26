#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Optional

from send_generated_emails import build_batch_payload, build_send_summary, send_batch


def normalize_send_policy(*, mode: str, send_policy: Optional[str]= None, review_required: Optional[bool]= None) -> dict[str, Any]:
    requested = (send_policy or "").strip().lower()
    if requested not in {"", "prepare_only", "manual_send", "scheduled_send"}:
        requested = ""
    # 默认口径：manual 仍保守只准备，scheduled_cycle 默认自动发送。
    if not requested:
        requested = "scheduled_send" if mode == "scheduled_cycle" else "prepare_only"
    execute_send = requested in {"manual_send", "scheduled_send"}
    if review_required is None:
        requires_review = requested == "manual_send"
        if mode == "scheduled_cycle" and requested == "scheduled_send":
            requires_review = False
    else:
        requires_review = bool(review_required) or requested == "manual_send"
    return {
        "requested": requested,
        "executeSend": execute_send and not requires_review,
        "reviewRequired": requires_review,
        "summary": (
            "prepare-only" if requested == "prepare_only" else
            "human-confirmed send" if requested == "manual_send" else
            "scheduled guarded send"
        ),
    }


def normalize_reply_policy(*, mode: str, reply_send_policy: Optional[str]= None, review_required: Optional[bool]= None) -> dict[str, Any]:
    requested = (reply_send_policy or "").strip().lower()
    if requested not in {"", "prepare_only", "safe_auto_send", "human_only"}:
        requested = ""
    if not requested:
        requested = "safe_auto_send" if mode == "scheduled_cycle" else "human_only"
    execute_send = requested == "safe_auto_send"
    if review_required is None:
        requires_review = requested == "human_only"
    else:
        requires_review = bool(review_required) or requested == "human_only"
    return {
        "requested": requested,
        "executeSend": execute_send and not requires_review,
        "reviewRequired": requires_review,
        "summary": (
            "prepare-only" if requested == "prepare_only" else
            "safe auto-send" if requested == "safe_auto_send" else
            "human-only"
        ),
    }


def execute_outreach_send(*, emails: list[dict[str, Any]], send_policy_info: dict[str, Any], token: Optional[str], brief: dict[str, Any], timing: str = "", creator_profiles_by_id: Optional[dict[str, dict[str, Any]]] = None, draft_generation: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    summary = {
        "preparedCount": len(emails),
        "autoSendExecuted": False,
        "sendPolicy": send_policy_info.get("requested"),
        "reviewRequired": send_policy_info.get("reviewRequired", True),
        "timing": timing or None,
        "status": "prepared",
        "notes": "Campaign engine prepares outreach candidates but does not silently send them.",
    }
    draft_generation = draft_generation or {}
    draft_status = str(draft_generation.get("status") or "").strip()
    draft_validation = draft_generation.get("validation") or {}
    if draft_status == "host_drafts_identity_conflict":
        summary.update({
            "status": "blocked",
            "notes": "Host draft write-back failed identity validation before send execution.",
            "draftGenerationStatus": draft_status,
            "draftValidation": draft_validation,
        })
        return summary
    if not emails:
        summary["notes"] = "No outreach emails prepared in this cycle."
        return summary
    if not token:
        summary["status"] = "blocked"
        summary["notes"] = "Missing token; outreach send execution blocked."
        return summary
    if send_policy_info.get("reviewRequired"):
        summary["status"] = "review_required"
        summary["notes"] = "Send policy requires human review before execution."
        return summary
    if not send_policy_info.get("executeSend"):
        return summary
    expected_language = str(brief.get("language") or "en").strip() or "en"
    allow_fallback_send = bool(brief.get("allow_fallback_send", False))
    batch_payload = build_batch_payload(
        {"emails": emails},
        expected_language=expected_language,
        allow_fallback_send=allow_fallback_send,
        creator_profiles_by_id=creator_profiles_by_id,
    )
    send_summary = build_send_summary(batch_payload, dry_run=False, timing=timing)
    if batch_payload.get("blocked"):
        summary.update({
            "status": "review_required",
            "notes": "Some outreach emails were blocked by send-time validation or fallback-send policy.",
            "batchSummary": send_summary,
            "blocked": batch_payload.get("blocked"),
            "auditResults": batch_payload.get("auditResults") or [],
            "draftGenerationStatus": draft_status or None,
            "draftValidation": draft_validation or None,
        })
        return summary
    batch_result = send_batch(batch_payload, dry_run=False, timing=timing)
    summary.update({
        "status": batch_result.get("status") or "unknown",
        "autoSendExecuted": batch_result.get("status") == "sent",
        "notes": "Outreach batch executed by campaign engine.",
        "batchSummary": send_summary,
        "apiResult": batch_result.get("response"),
        "auditResults": batch_payload.get("auditResults") or [],
        "draftGenerationStatus": draft_status or None,
        "draftValidation": draft_validation or None,
    })
    return summary
