#!/usr/bin/env python3
from typing import Optional
"""
send_generated_emails.py
~~~~~~~~~~~~~~~~~~~~~~~~

Bridge: 将 generate_outreach_emails.py 的输出直接发给 inbox.py send。

用法：
    python3 scripts/send_generated_emails.py generated_emails.json
    python3 scripts/send_generated_emails.py generated_emails.json --dry-run
"""
import argparse
import json
import sys

import inbox
from common import get_token, log_file
from draft_consistency_audit import audit_email_against_creator_profile


def load_emails(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def build_batch_payload(
    emails_data: dict,
    expected_language: str = "en",
    allow_fallback_send: bool = False,
    creator_profiles_by_id: Optional[dict[str, dict]] = None,
) -> dict:
    """Build batch payload.

    Default policy: only host-model drafts are sendable for real outreach.
    Fallback drafts require explicit allow_fallback_send=True.
    """
    from execution_layer import normalize_email_once

    generated = emails_data.get("emails", [])
    emails_payload = []
    blogger_infos = []
    skipped = []
    blocked = []
    audit_results = []
    seen_blogger_ids = set()

    for email in generated:
        blogger_id = email.get("bloggerId")
        nickname = email.get("nickname")
        if not blogger_id:
            skipped.append({"nickname": nickname, "reason": "no bloggerId"})
            continue
        blogger_id = str(blogger_id).strip()
        if blogger_id in seen_blogger_ids:
            blocked.append({"nickname": nickname, "bloggerId": blogger_id, "reason": "duplicate_bloggerId_in_send_batch"})
            continue
        seen_blogger_ids.add(blogger_id)
        draft_source = str(email.get("draftSource") or email.get("source") or "").strip().lower()
        style = str(email.get("style") or "").strip().lower()
        is_host_model = draft_source in {"host-model", "model-first", "host_model"} or style == "model-first"
        is_fallback = draft_source in {"fallback-script", "fallback", "script-fallback"} or style == "fallback-light"
        if is_fallback and not allow_fallback_send:
            blocked.append({"nickname": nickname, "bloggerId": blogger_id, "reason": "fallback_send_not_allowed"})
            continue
        if not is_host_model and not (is_fallback and allow_fallback_send):
            blocked.append({"nickname": nickname, "bloggerId": blogger_id, "reason": "unknown_draft_source"})
            continue

        # Do not gate sending on emailAvailable here.
        # WotoHub send API can resolve the recipient internally from bloggerId.
        # Only require bloggerId + valid normalized email artifact.
        email = normalize_email_once(email)
        creator_profile = dict((creator_profiles_by_id or {}).get(str(blogger_id), {}) or {})
        for key in (
            "bloggerId", "nickname", "bloggerName", "channelName", "platform", "country", "language", "category", "contentStyle", "tagList", "recentTopics", "followers", "fansNum",
        ):
            if email.get(key) not in (None, "", []):
                creator_profile.setdefault(key, email.get(key))
        audit = audit_email_against_creator_profile(
            email,
            expected_language=expected_language,
            creator_profile=creator_profile,
        )
        audit_results.append({
            "bloggerId": blogger_id,
            "nickname": nickname,
            "ok": audit.get("ok", False),
            "errors": audit.get("errors") or [],
            "warnings": audit.get("warnings") or [],
            "checks": audit.get("checks") or [],
            "profileSnapshot": audit.get("profileSnapshot") or {},
        })
        if not audit.get("ok"):
            blocked.append({
                "nickname": nickname,
                "bloggerId": blogger_id,
                "reason": "pre_send_consistency_audit_failed",
                "auditErrors": audit.get("errors") or [],
                "auditWarnings": audit.get("warnings") or [],
            })
            continue

        emails_payload.append({
            "subject": email.get("subject", ""),
            "content": email.get("htmlBody") or email.get("content") or "",
            "bloggerIds": [blogger_id],
        })
        blogger_infos.append({
            "bloggerId": blogger_id,
            "chooseSource": 0,
            "popularizePlanId": -1,
        })

    return {
        "emails": emails_payload,
        "bloggerInfos": blogger_infos,
        "skipped": skipped,
        "blocked": blocked,
        "normalizationSummary": {
            "inputCount": len(generated),
            "sendableCount": len(emails_payload),
            "skippedCount": len(skipped),
            "blockedCount": len(blocked),
            "auditFailedCount": len([x for x in audit_results if not x.get("ok")]),
            "auditWarningCount": len([x for x in audit_results if x.get("warnings")]),
        },
        "auditResults": audit_results,
    }


def send_batch(batch_payload: dict, dry_run: bool = False, timing: str = "") -> dict:
    emails_payload = batch_payload.get("emails", [])
    blogger_infos = batch_payload.get("bloggerInfos", [])
    if dry_run:
        return {
            "status": "dry_run",
            "mailType": 2 if timing else 1,
            "emails": emails_payload,
            "bloggerInfos": blogger_infos,
            "count": len(emails_payload),
        }

    token = get_token(feature="send_email")
    response = inbox.send_email(
        token,
        emails=emails_payload,
        blogger_infos=blogger_infos,
        mail_type=2 if timing else 1,
        timing=timing or "",
    )
    code = str(response.get("code", ""))
    success = code in {"0", "200"} or bool(response.get("success"))
    status = "sent" if success else "failed"
    return {
        "status": status,
        "count": len(emails_payload),
        "response": response,
        "emails": emails_payload,
        "bloggerInfos": blogger_infos,
        "mailType": 2 if timing else 1,
    }


def build_send_summary(batch_payload: dict, dry_run: bool = False, timing: str = "") -> dict:
    emails_payload = batch_payload.get("emails", [])
    subjects = [str(x.get("subject") or "").strip() for x in emails_payload if str(x.get("subject") or "").strip()]
    unique_subjects = list(dict.fromkeys(subjects))
    return {
        "count": len(emails_payload),
        "mailType": "timed" if timing else ("dry_run" if dry_run else "send"),
        "timing": timing or None,
        "subjectPreview": unique_subjects[:3],
        "uniqueSubjectCount": len(unique_subjects),
        "skippedCount": len(batch_payload.get("skipped", [])),
        "blockedCount": len(batch_payload.get("blocked", [])),
        "normalizationSummary": batch_payload.get("normalizationSummary") or {},
        "auditFailedCount": ((batch_payload.get("normalizationSummary") or {}).get("auditFailedCount") or 0),
        "auditWarningCount": ((batch_payload.get("normalizationSummary") or {}).get("auditWarningCount") or 0),
    }


def summarize(result: dict, skipped: list[dict], blocked: Optional[list[dict]]= None, send_summary: Optional[dict]= None):
    print(f"\n{'='*50}")
    if send_summary:
        print("发送摘要：")
        print(f"- 待发送数量：{send_summary.get('count', 0)}")
        print(f"- 发送模式：{send_summary.get('mailType')}")
        if send_summary.get('timing'):
            print(f"- 定时时间：{send_summary.get('timing')}")
        previews = send_summary.get('subjectPreview') or []
        if previews:
            print(f"- 主题预览：{'; '.join(previews)}")
        print(f"- 跳过数量：{send_summary.get('skippedCount', 0)}")
        print(f"- 拦截数量：{send_summary.get('blockedCount', 0)}")
        print(f"- audit 拦截：{send_summary.get('auditFailedCount', 0)}")
        print(f"- audit 警告：{send_summary.get('auditWarningCount', 0)}")

    if result["status"] == "sent":
        print(f"📤 批量发送完成：✅ 1 批 | 共 {result.get('count', 0)} 封")
    elif result["status"] == "dry_run":
        print(f"📤 批量发送演练：🅳 1 批 | 共 {result.get('count', 0)} 封")
    else:
        msg = (result.get("response") or {}).get("message", "")
        print(f"📤 批量发送失败：❌ 1 批 | 共 {result.get('count', 0)} 封 | {msg}")
    if skipped:
        print("\n跳过列表：")
        for item in skipped:
            print(f"  - @{item.get('nickname') or '-'} ({item.get('bloggerId') or '-'}) — {item.get('reason')}")
    if blocked:
        print("\n拦截列表：")
        for item in blocked:
            print(f"  - @{item.get('nickname') or '-'} ({item.get('bloggerId') or '-'}) — {item.get('reason')}")


DEFAULT_SEND_LIMIT = 200


def main():
    ap = argparse.ArgumentParser(description="将生成好的邮件批量发送")
    ap.add_argument("emails_json", help="generate_outreach_emails.py 输出的 JSON 文件路径")
    ap.add_argument("--dry-run", action="store_true", help="仅展示批量 payload，不实际发送")
    ap.add_argument("--limit", type=int, default=DEFAULT_SEND_LIMIT, help=f"最多发送 N 封（默认 {DEFAULT_SEND_LIMIT}，0=不限）")
    ap.add_argument("--timing", default="", help="定时发送时间，格式 yyyy-MM-dd HH:mm:ss")
    ap.add_argument("--expected-language", default="en", help="发送前标题校验语言，默认 en")
    ap.add_argument("--allow-fallback-send", action="store_true", help="允许发送 fallback-script 草稿；默认关闭")
    args = ap.parse_args()

    data = load_emails(args.emails_json)
    if args.limit > 0:
        data = dict(data)
        data["emails"] = (data.get("emails") or [])[:args.limit]

    batch_payload = build_batch_payload(data, expected_language=args.expected_language, allow_fallback_send=args.allow_fallback_send)
    if not batch_payload["emails"]:
        print("没有可发送的邮件：所有候选邮件都被跳过或拦截（检查标题语言、正文内容、bloggerId、draftSource 或 fallback send 权限）", file=sys.stderr)
        sys.exit(1)

    print(f"共 {len(batch_payload['emails'])} 封邮件待批量发送")
    send_summary = build_send_summary(batch_payload, dry_run=args.dry_run, timing=args.timing)
    result = send_batch(batch_payload, dry_run=args.dry_run, timing=args.timing)
    summarize(result, batch_payload.get("skipped", []), batch_payload.get("blocked", []), send_summary)

    log_path = log_file("sent_log.json")
    existing = []
    if log_path.exists():
        existing = json.loads(log_path.read_text())
    existing.append({
        "mode": "batch",
        "status": result.get("status"),
        "count": result.get("count", 0),
        "timing": args.timing or None,
        "summary": send_summary,
        "skipped": batch_payload.get("skipped", []),
        "response": result.get("response"),
        "emails": result.get("emails", []),
        "bloggerInfos": result.get("bloggerInfos", []),
    })
    log_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    print(f"\n📝 批量发送记录已保存到 {log_path}")


if __name__ == "__main__":
    main()
