#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional
import json as _json
import tempfile
import subprocess
import sys

import inbox
from build_conversation_analysis_input import _extract_records, _pick_first
from campaign_reply_analysis import coerce_model_reply_analysis, validate_model_reply_analysis
from generate_reply_preview import generate_reply_previews
from common import get_token
from conversation_state import mark_scanned, mark_classified, mark_preview_generated, mark_notified, mark_archived, get_skip_reason, should_skip_email, get_email_state, get_chat_state
from reply_policy import decide_reply_action, load_policy


def _heuristic_classify(mail: dict[str, Any]) -> dict[str, Any]:
    text = " ".join([
        str(mail.get("subject") or ""),
        str(mail.get("cleanContent") or mail.get("content") or ""),
    ]).lower()

    if any(x in text for x in ["not interested", "no thanks", "pass"]):
        classification = "rejection"
        priority = "low"
        requires_human = False
    elif any(x in text for x in ["price", "budget", "commission", "rate"]):
        classification = "pricing_discussion"
        priority = "high"
        requires_human = True
    elif any(x in text for x in ["sample", "ship", "shipping"]):
        classification = "asks_for_sample_process"
        priority = "medium"
        requires_human = False
    elif any(x in text for x in ["detail", "details", "more info", "information"]):
        classification = "asks_for_product_details"
        priority = "high"
        requires_human = False
    elif any(x in text for x in ["interested", "sounds good", "let's do it", "next step"]):
        classification = "simple_interest_acknowledgement"
        priority = "high"
        requires_human = False
    else:
        classification = "unknown"
        priority = "medium"
        requires_human = True

    return {
        "classification": classification,
        "priority": priority,
        "requiresHuman": requires_human,
        "autoReplyAllowed": classification in {"asks_for_product_details", "asks_for_sample_process", "asks_for_next_steps", "simple_interest_acknowledgement"},
        "recommendedAction": "preview_reply",
        "summary": "Heuristic classification result from current subject/content.",
    }


def _load_model_classification(path: Optional[str]) -> Optional[dict[str, Any]]:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text())
        return data if isinstance(data, dict) else None
    except Exception:
        return None

def _load_conversation_analysis(path: Optional[str]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if not path:
        return None, None
    p = Path(path)
    if not p.exists():
        return None, {
            "ok": False,
            "errors": [f"conversation_analysis file not found: {path}"],
            "warnings": [],
            "itemCount": 0,
            "validItemCount": 0,
        }
    try:
        raw = json.loads(p.read_text())
    except Exception as exc:
        return None, {
            "ok": False,
            "errors": [f"conversation_analysis JSON parse failed: {exc}"],
            "warnings": [],
            "itemCount": 0,
            "validItemCount": 0,
        }
    coerced = coerce_model_reply_analysis(raw)
    validation = validate_model_reply_analysis(coerced)
    if not validation.get("ok"):
        return None, validation
    return coerced, validation


def _match_model_classification(model_classification: Optional[dict[str, Any]], email_id, chat_id) -> Optional[dict[str, Any]]:
    if not isinstance(model_classification, dict):
        return None
    items = model_classification.get("items")
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, dict):
                continue
            if str(item.get("emailId", "")) == str(email_id) or str(item.get("replyId", "")) == str(email_id) or str(item.get("chatId", "")) == str(chat_id):
                return item
    return None


def _build_human_summary(results: list[dict[str, Any]], mode: str, skipped_items: Optional[list[dict[str, Any]]]= None, auto_reply_report: Optional[dict[str, Any]]= None) -> dict[str, str]:
    if not results:
        text = "本轮未发现新的待处理回信。"
        return {"summary": text, "displayText": text}

    high = [x for x in results if (x.get("classification") or {}).get("priority") == "high"]
    preview = [x for x in results if (x.get("decision") or {}).get("action") == "preview_reply"]
    notify = [x for x in results if (x.get("decision") or {}).get("action") == "notify_only"]
    archive = [x for x in results if (x.get("decision") or {}).get("action") == "archive"]

    lines = [f"本轮模式：{mode}", f"共处理 {len(results)} 封候选回信。"]
    if high:
        lines.append(f"高优先级：{len(high)} 封")
    if preview:
        lines.append(f"建议生成回复预览：{len(preview)} 封")
        for item in preview[:3]:
            lines.append(f"- @{item.get('bloggerName') or item.get('bloggerId')}: {(item.get('classification') or {}).get('classification')} | {(item.get('decision') or {}).get('reason')}")
    if notify:
        lines.append(f"建议人工查看：{len(notify)} 封")
    if archive:
        lines.append(f"建议归档：{len(archive)} 封")
    if skipped_items:
        lines.append(f"本轮跳过：{len(skipped_items)} 封")
        for item in skipped_items[:3]:
            lines.append(f"- 跳过 @{item.get('bloggerName') or item.get('chatId')}: {item.get('reason')}")
    if auto_reply_report:
        lines.append(f"自动回复候选：{auto_reply_report.get('candidateCount', 0)} 封（本轮最多自动发送 {auto_reply_report.get('maxAutoReplies', 0)} 封）")

    text = "\n".join(lines)
    return {"summary": text, "displayText": text}


def _auto_send_reply_previews(preview_result: dict[str, Any], max_auto: int = 3) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as tf:
        tf.write(_json.dumps(preview_result, ensure_ascii=False, indent=2))
        temp_path = tf.name
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "send_reply_previews.py"),
        temp_path,
        "--limit",
        str(max_auto),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def run_monitor(
    token: str,
    mode: str = "reply_assist",
    page_size: int = 20,
    limit: int = 10,
    include_read: bool = False,
    include_replied: bool = False,
    policy_file: Optional[str]= None,
    model_classification: Optional[dict[str, Any]]= None,
    conversation_analysis: Optional[dict[str, Any]]= None,
    conversation_analysis_validation: Optional[dict[str, Any]]= None,
    generate_preview: bool = False,
) -> dict[str, Any]:
    inbox_resp = inbox.list_inbox(
        token,
        current_page=1,
        page_size=page_size,
        is_read=0 if include_read else 1,
        is_reply=0 if not include_replied else 0,
        time_range=3,
    )
    records = _extract_records(inbox_resp)
    policy = load_policy(policy_file)
    auto_reply_requested = mode == "auto_reply"
    auto_reply_analysis_ready = auto_reply_requested and conversation_analysis is not None
    effective_mode = "auto_reply" if auto_reply_analysis_ready else "reply_assist"

    results: list[dict[str, Any]] = []
    scanned_count = 0
    candidate_count = 0
    preview_count = 0
    notify_count = 0
    archive_count = 0
    skipped_count = 0
    skipped_items: list[dict[str, Any]] = []

    for mail in records[:limit]:
        email_id = mail.get("id")
        chat_id = mail.get("chatId")
        blogger_id = _pick_first(mail.get("bloggerId"), default="")
        if not email_id or not chat_id:
            continue
        scanned_count += 1
        skip_reason = get_skip_reason(email_id, chat_id=chat_id, cooldown_minutes=30)
        if skip_reason:
            skipped_count += 1
            skipped_items.append({
                "emailId": email_id,
                "chatId": chat_id,
                "reason": skip_reason,
                "bloggerName": _pick_first(mail.get("bloggerName"), mail.get("bloggerUserName")),
            })
            continue

        candidate_count += 1
        mark_scanned(email_id, chat_id=chat_id, blogger_id=blogger_id, metadata={
            "subject": mail.get("subject"),
            "bloggerName": _pick_first(mail.get("bloggerName"), mail.get("bloggerUserName")),
        })
        classification = _match_model_classification(model_classification, email_id, chat_id) or _heuristic_classify(mail)
        classification['_mail'] = {
            'id': email_id,
            'chatId': chat_id,
            'subject': mail.get('subject'),
            'cleanContent': mail.get('cleanContent') or mail.get('content'),
        }
        mark_classified(email_id, classification["classification"], classification["priority"], classification["requiresHuman"], metadata=classification)
        state_item = get_email_state(email_id) or {}
        chat_state = get_chat_state(chat_id) or {}
        merged_state = dict(state_item)
        for key in ("autoReplyCount", "campaignCycleState"):
            if chat_state.get(key) not in (None, ""):
                merged_state[key] = chat_state.get(key)
        merged_state["chatId"] = chat_id
        decision = decide_reply_action(classification, mode=effective_mode, policy_config=policy, conversation_state=merged_state)
        if auto_reply_requested and not auto_reply_analysis_ready and decision.get("action") == "auto_reply":
            decision = {
                "action": "preview_reply",
                "reason": "auto-reply downgraded to preview-first because valid conversation_analysis was not provided",
                "requiresHuman": True,
                "autoReplyAllowed": False,
            }

        action = decision.get("action")
        if action == "preview_reply":
            preview_count += 1
            mark_preview_generated(email_id, metadata={"reason": decision.get("reason")})
        elif action == "notify_only":
            notify_count += 1
            mark_notified(email_id, metadata={"reason": decision.get("reason")})
        elif action == "archive":
            archive_count += 1
            mark_archived(email_id, metadata={"reason": decision.get("reason")})

        results.append({
            "emailId": email_id,
            "chatId": chat_id,
            "bloggerId": blogger_id,
            "bloggerName": _pick_first(mail.get("bloggerName"), mail.get("bloggerUserName")),
            "subject": mail.get("subject"),
            "classification": classification,
            "decision": decision,
        })

    result = {
        "mode": mode,
        "effectiveMode": effective_mode,
        "autoReplyConversationAnalysisReady": auto_reply_analysis_ready,
        "conversationAnalysisValidation": conversation_analysis_validation,
        "scannedCount": scanned_count,
        "candidateCount": candidate_count,
        "previewCount": preview_count,
        "notifyCount": notify_count,
        "archiveCount": archive_count,
        "skippedCount": skipped_count,
        "skippedItems": skipped_items,
        "items": results,
    }

    auto_reply_report = None
    if generate_preview:
        preview_candidates = [
            {
                "id": item["emailId"],
                "chatId": item["chatId"],
                "bloggerId": item.get("bloggerId"),
                "bloggerName": item.get("bloggerName"),
                "subject": item.get("subject"),
            }
            for item in results
            if (item.get("decision") or {}).get("action") in {"preview_reply", "auto_reply"}
        ]
        if preview_candidates:
            result["replyPreviewResult"] = generate_reply_previews(
                token=token,
                page_size=page_size,
                only_unread=not include_read,
                only_unreplied=not include_replied,
                limit=min(len(preview_candidates), 5),
                model_analysis=conversation_analysis,
                lazy_dialogue=not auto_reply_analysis_ready,
                candidate_items=preview_candidates,
            )
            if auto_reply_requested:
                auto_candidates = [
                    item for item in results
                    if (item.get("decision") or {}).get("action") == "auto_reply"
                ]
                if auto_candidates:
                    auto_reply_report = {
                        "candidateCount": len(auto_candidates),
                        "maxAutoReplies": 3,
                    }
                    preview_result = result["replyPreviewResult"]
                    preview_items = preview_result.get("replyPreviews") or []
                    all_model_first = bool(preview_items) and all(item.get("analysisMode") == "model-first" for item in preview_items)
                    if auto_reply_analysis_ready and all_model_first:
                        result["autoReplyExecution"] = _auto_send_reply_previews(preview_result, max_auto=3)
                    else:
                        result["autoReplyExecution"] = {
                            "status": "blocked",
                            "reason": (
                                "auto_reply requires valid conversation_analysis plus full-thread model-first previews; "
                                "falling back to preview-first review flow"
                            ),
                        }
    if auto_reply_report:
        result["autoReplyReport"] = auto_reply_report
    summary = _build_human_summary(results, mode=mode, skipped_items=skipped_items, auto_reply_report=auto_reply_report)
    result["summary"] = summary["summary"]
    result["displayText"] = summary["displayText"]
    return result


def main():
    ap = argparse.ArgumentParser(description="Monitor inbox and produce reply-assist decisions")
    ap.add_argument("--token")
    ap.add_argument("--mode", choices=["reply_assist", "auto_reply"], default="reply_assist")
    ap.add_argument("--page-size", type=int, default=20)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--include-read", action="store_true")
    ap.add_argument("--include-replied", action="store_true")
    ap.add_argument("--policy-file", help="custom reply policy JSON file")
    ap.add_argument("--model-classification-file", help="模型生成的 reply classification JSON 文件")
    ap.add_argument("--conversation-analysis-file", help="模型生成的 conversation_analysis JSON 文件；auto_reply 必须提供有效文件")
    ap.add_argument("--generate-preview", action="store_true", help="对 preview_reply 候选进一步生成回复预览")
    ap.add_argument("--output")
    args = ap.parse_args()

    token = get_token(args.token, feature="reply_assist")
    model_classification = _load_model_classification(args.model_classification_file)
    conversation_analysis, conversation_analysis_validation = _load_conversation_analysis(args.conversation_analysis_file)
    result = run_monitor(
        token=token,
        mode=args.mode,
        page_size=args.page_size,
        limit=args.limit,
        include_read=args.include_read,
        include_replied=args.include_replied,
        policy_file=args.policy_file,
        model_classification=model_classification,
        conversation_analysis=conversation_analysis,
        conversation_analysis_validation=conversation_analysis_validation,
        generate_preview=args.generate_preview,
    )
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
