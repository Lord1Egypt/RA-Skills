#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _normalize_items(request: dict) -> list[dict]:
    semantic_context = request.get("semanticContext") or {}
    resolved = semantic_context.get("resolvedArtifacts") or {}
    incoming = resolved.get("selectedReplyItems") or resolved.get("replyCandidates") or []
    if isinstance(incoming, list) and incoming:
        return [item for item in incoming if isinstance(item, dict)]
    campaign_id = request.get("campaignId") or ((semantic_context.get("meta") or {}).get("campaignId"))
    return [{
        "replyId": request.get("replyId") or 1,
        "chatId": request.get("chatId") or f"chat-{campaign_id or 'demo'}",
        "subject": "Re: Collaboration Opportunity",
        "latestIncoming": request.get("rawInput") or "Creator asked for more details.",
    }]


def _build_item(item: dict) -> dict:
    latest_incoming = item.get("latestIncoming") or item.get("replyBody") or "Creator asked for more details."
    return {
        "replyId": item.get("replyId"),
        "chatId": item.get("chatId"),
        "subject": item.get("subject") or "Re: Collaboration Opportunity",
        "latestIncoming": latest_incoming,
        "lastOutgoing": item.get("lastOutgoing") or "We introduced the collaboration idea and asked about fit.",
        "conversationStage": item.get("conversationStage") or "follow_up",
        "analysis": {
            "latestIntent": item.get("latestIntent") or "asking_product_details",
            "resolvedPoints": item.get("resolvedPoints") or [],
            "openQuestions": item.get("openQuestions") or ["product details", "next collaboration step"],
            "recommendedStrategy": item.get("recommendedStrategy") or "Answer clearly, keep tone warm-professional, and move to the next concrete step.",
            "tone": item.get("tone") or "warm-professional",
        },
        "replyBody": item.get("replyBody") or "Hi there, thanks for your reply. Happy to share more details and align on the next step.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Example reply analysis executor for WotoHub")
    ap.add_argument("--input", required=True, help="Path to host reply analysis request JSON")
    ap.add_argument("--output", help="Path to write executor output JSON")
    args = ap.parse_args()

    request = json.loads(Path(args.input).read_text(encoding="utf-8"))
    items = [_build_item(item) for item in _normalize_items(request)]
    result = {
        "replyModelAnalysis": {"items": items},
        "executorMeta": {
            "example": True,
            "mode": request.get("mode"),
        },
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
