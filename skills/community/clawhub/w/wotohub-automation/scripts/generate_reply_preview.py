#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional

import inbox
from common import get_token
from html_email_utils import plain_text_to_html, normalize_html_body, html_to_plain_text
from build_conversation_analysis_input import _extract_records, _extract_dialogue_items, _pick_first


def _truncate(text: str, limit: int = 220) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def _default_reply_subject(latest_mail: dict) -> str:
    subject = _pick_first(latest_mail.get("subject"), default="")
    if not subject:
        return "Re:"
    return subject if subject.lower().startswith("re:") else f"Re: {subject}"


def _infer_reply_language(latest_mail: dict) -> str:
    text = " ".join([str(latest_mail.get("subject") or ""), str(latest_mail.get("cleanContent") or latest_mail.get("content") or "")])
    if any("\u3040" <= ch <= "\u30ff" for ch in text):
        return "ja"
    if any("\uac00" <= ch <= "\ud7af" for ch in text):
        return "ko"
    lowered = text.lower()
    if any(token in lowered for token in ("hola", "gracias", "colabor", "muestra", "detalles", "interesa")):
        return "es"
    return "en"


def _fallback_reply_body(latest_mail: dict) -> str:
    blogger_name = _pick_first(latest_mail.get("bloggerName"), latest_mail.get("bloggerUserName"), "there")
    lang = _infer_reply_language(latest_mail)
    if lang == "es":
        return f"Hola {blogger_name},\n\nGracias por tu respuesta. Con gusto puedo compartirte más detalles para avanzar.\n\nSaludos,\nTeam"
    if lang == "ja":
        return f"{blogger_name}様\n\nご返信ありがとうございます。必要でしたら詳細をお送りします。\n\nよろしくお願いいたします。\nTeam"
    if lang == "ko":
        return f"안녕하세요 {blogger_name}님,\n\n답장 주셔서 감사합니다. 필요하시면 자세한 내용을 공유드리겠습니다.\n\n감사합니다.\nTeam"
    return f"Hi {blogger_name},\n\nThanks for your reply. I'd be happy to share more details so we can move forward.\n\nBest,\nTeam"


def _build_thread_summary(dialogue_items: list[dict], latest_mail: dict) -> dict:
    last_incoming = None
    last_outgoing = None
    for item in dialogue_items:
        if str(item.get("type")) == "1":
            last_incoming = item
        elif str(item.get("type")) == "2":
            last_outgoing = item
    return {
        "latestIncoming": _truncate(_pick_first(latest_mail.get("cleanContent"), latest_mail.get("content"))),
        "lastOutgoing": _truncate(_pick_first((last_outgoing or {}).get("cleanContent"), (last_outgoing or {}).get("content"))),
        "lastIncoming": _truncate(_pick_first((last_incoming or {}).get("cleanContent"), (last_incoming or {}).get("content"))),
        "turns": len(dialogue_items),
    }


def _is_valid_reply_analysis_item(item: dict) -> bool:
    if not isinstance(item, dict):
        return False
    has_identity = bool(item.get("replyId") or item.get("chatId"))
    has_stage = bool(str(item.get("conversationStage") or item.get("stage") or "").strip())
    has_body = bool(str(item.get("replyBody") or item.get("body") or "").strip())
    return has_identity and has_stage and has_body


def _normalize_model_analysis(model_analysis: Optional[dict], mail_id, chat_id: str) -> Optional[dict]:
    if not isinstance(model_analysis, dict):
        return None
    items = model_analysis.get("items")
    if isinstance(items, list):
        for item in items:
            if not _is_valid_reply_analysis_item(item):
                continue
            if str(item.get("replyId", "")) == str(mail_id) or str(item.get("chatId", "")) == str(chat_id):
                return item
    if _is_valid_reply_analysis_item(model_analysis) and (str(model_analysis.get("replyId", "")) == str(mail_id) or str(model_analysis.get("chatId", "")) == str(chat_id)):
        return model_analysis
    return None


def _reply_style_hint(stage: str, tone: str, latest_intent: str) -> str:
    parts = []
    if stage:
        parts.append(f"阶段：{stage}")
    if latest_intent:
        parts.append(f"意图：{latest_intent}")
    if tone:
        parts.append(f"语气：{tone}")
    return " | ".join(parts)


def _build_preview_item(mail: dict, detail: dict, dialogue_items: list[dict], model_analysis: Optional[dict]= None) -> dict:
    blogger_id = _pick_first(mail.get("bloggerId"), detail.get("bloggerId"))
    chat_id = _pick_first(mail.get("chatId"), detail.get("chatId"))
    reply_id = _pick_first(detail.get("id"), mail.get("id"))
    nickname = _pick_first(mail.get("bloggerName"), mail.get("bloggerUserName"), detail.get("bloggerName"), "未知达人")
    original_link = _pick_first((detail.get("bloggerHover") or {}).get("link"), mail.get("link"))

    matched_analysis = _normalize_model_analysis(model_analysis, reply_id, str(chat_id))
    if matched_analysis:
        analysis_obj = matched_analysis.get("analysis") if isinstance(matched_analysis.get("analysis"), dict) else {}
        stage = matched_analysis.get("stage") or matched_analysis.get("conversationStage") or "-"
        latest_intent = matched_analysis.get("latestIntent") or analysis_obj.get("latestIntent") or "-"
        tone = matched_analysis.get("tone") or analysis_obj.get("tone") or "-"
        strategy = matched_analysis.get("recommendedStrategy") or analysis_obj.get("recommendedStrategy") or ""
        context_summary = {
            "latestIncoming": matched_analysis.get("latestIncoming") or _truncate(_pick_first(detail.get("cleanContent"), detail.get("content"), mail.get("cleanContent"), mail.get("content"))),
            "lastOutgoing": matched_analysis.get("lastOutgoing") or "",
            "lastIncoming": matched_analysis.get("lastIncoming") or "",
            "stage": stage,
            "latestIntent": latest_intent,
            "tone": tone,
            "recommendedStrategy": strategy,
            "resolvedPoints": matched_analysis.get("resolvedPoints") or analysis_obj.get("resolvedPoints") or [],
            "openQuestions": matched_analysis.get("openQuestions") or analysis_obj.get("openQuestions") or [],
            "riskFlags": matched_analysis.get("riskFlags") or analysis_obj.get("riskFlags") or [],
            "avoidances": matched_analysis.get("avoidances") or analysis_obj.get("avoidances") or [],
            "turns": matched_analysis.get("turns") or len(dialogue_items),
            "analysis": matched_analysis,
        }
        subject = matched_analysis.get("subject") or _default_reply_subject(detail or mail)
        body = matched_analysis.get("body") or matched_analysis.get("replyBody") or _fallback_reply_body(detail or mail)
        analysis_mode = "model-first"
        analysis_source = "external_model"
        analysis_confidence = "high"
    else:
        context_summary = _build_thread_summary(dialogue_items, detail or mail)
        context_summary["stage"] = "model-analysis-required"
        subject = _default_reply_subject(detail or mail)
        body = _fallback_reply_body(detail or mail)
        analysis_mode = "fallback-light"
        analysis_source = "fallback_light"
        analysis_confidence = "low"

    html_body = normalize_html_body(plain_text_to_html(body))
    plain_text_body = html_to_plain_text(html_body)
    return {
        "replyId": reply_id,
        "chatId": chat_id,
        "bloggerId": blogger_id,
        "nickname": nickname,
        "subject": subject,
        "body": plain_text_body,
        "htmlBody": html_body,
        "plainTextBody": plain_text_body,
        "replyStyleHint": _reply_style_hint(context_summary.get("stage", "-"), context_summary.get("tone", "-"), context_summary.get("latestIntent", "-")),
        "contextSummary": context_summary,
        "latestMail": {
            "subject": _pick_first(detail.get("subject"), mail.get("subject")),
            "content": _pick_first(detail.get("cleanContent"), detail.get("content"), mail.get("cleanContent"), mail.get("content")),
            "cleanContent": _pick_first(detail.get("cleanContent"), detail.get("content"), mail.get("cleanContent"), mail.get("content")),
            "bloggerName": _pick_first(detail.get("bloggerName"), mail.get("bloggerName"), mail.get("bloggerUserName")),
            "bloggerUserName": _pick_first(detail.get("bloggerUserName"), mail.get("bloggerUserName")),
        },
        "fansNum": _pick_first((mail.get("bloggerHover") or {}).get("fansNum"), (detail.get("bloggerHover") or {}).get("fansNum")),
        "originalLink": original_link,
        "analysisMode": analysis_mode,
        "analysisSource": analysis_source,
        "analysisConfidence": analysis_confidence,
        "recommendedAction": "review_then_send" if analysis_mode == "model-first" else "review_required",
    }


def _build_display(previews: list[dict]) -> dict:
    if not previews:
        text = "未扫描到待回复邮件"
        return {"count": 0, "summary": text, "markdownText": text, "plainText": text, "displayText": text}
    lines = [f"共 {len(previews)} 条回复预览"]
    for item in previews[:5]:
        lines.append(f"- @{item.get('nickname') or item.get('bloggerId')} ({item.get('replyId')}) [{item.get('analysisMode')}] {item.get('subject')}")
    text = "\n".join(lines)
    return {"count": len(previews), "summary": text, "markdownText": text, "plainText": text, "displayText": text}


def generate_reply_previews(
    token: str,
    page_size: int = 20,
    only_unread: bool = True,
    only_unreplied: bool = True,
    limit: int = 10,
    model_analysis: Optional[dict]= None,
    lazy_dialogue: bool = True,
    candidate_items: Optional[list[dict]]= None,
) -> dict[str, Any]:
    if candidate_items is None:
        inbox_resp = inbox.list_inbox(
            token,
            current_page=1,
            page_size=page_size,
            is_read=1 if only_unread else 0,
            is_reply=0 if only_unreplied else 0,
            time_range=3,
        )
        records = _extract_records(inbox_resp)
    else:
        records = [x for x in candidate_items if isinstance(x, dict)]

    previews = []
    for mail in records[:limit]:
        mail_id = mail.get("id")
        chat_id = mail.get("chatId")
        if not mail_id or not chat_id:
            continue
        detail_resp = inbox.get_email_detail(token, int(mail_id))
        detail = detail_resp.get("data") if isinstance(detail_resp, dict) and isinstance(detail_resp.get("data"), dict) else mail
        dialogue_items = []
        if not lazy_dialogue:
            dialogue_resp = inbox.get_dialogue(token, str(chat_id))
            dialogue_items = _extract_dialogue_items(dialogue_resp)
        previews.append(_build_preview_item(mail, detail, dialogue_items, model_analysis=model_analysis))

    display = _build_display(previews)
    return {"replyPreviews": previews, **display}


def main():
    ap = argparse.ArgumentParser(description="Generate reply previews from inbox replies")
    ap.add_argument("--token")
    ap.add_argument("--page-size", type=int, default=20)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--include-read", action="store_true")
    ap.add_argument("--include-replied", action="store_true")
    ap.add_argument("--full-dialogue", action="store_true")
    ap.add_argument("--model-analysis-file")
    ap.add_argument("--output")
    args = ap.parse_args()

    token = get_token(args.token, feature="reply_preview")
    model_analysis = None
    if args.model_analysis_file:
        model_analysis = json.loads(Path(args.model_analysis_file).read_text())
    result = generate_reply_previews(
        token=token,
        page_size=args.page_size,
        only_unread=not args.include_read,
        only_unreplied=not args.include_replied,
        limit=args.limit,
        model_analysis=model_analysis,
        lazy_dialogue=not args.full_dialogue,
    )
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
