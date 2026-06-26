#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _draft_for_creator(creator: dict, brief: dict, language: str) -> dict:
    blogger_id = creator.get("bloggerId") or creator.get("id") or creator.get("besId") or "unknown-blogger"
    nickname = creator.get("nickname") or creator.get("bloggerName") or creator.get("channelName") or "there"
    product_name = brief.get("productName") or "our product"
    offer_type = brief.get("offerType") or "collaboration"
    subject = f"Collab idea: {product_name} x {nickname}"
    plain = (
        f"Hi {nickname},\n\n"
        f"I came across your content and think {product_name} could be a strong fit for your audience. "
        f"We'd love to explore a {offer_type} collaboration if you're open to it.\n\n"
        f"Happy to share more details.\n"
    )
    html = f"<p>Hi {nickname},</p><p>I came across your content and think <strong>{product_name}</strong> could be a strong fit for your audience. We'd love to explore a <strong>{offer_type}</strong> collaboration if you're open to it.</p><p>Happy to share more details.</p>"
    return {
        "bloggerId": str(blogger_id),
        "nickname": nickname,
        "language": language or "en",
        "style": "creator-friendly-natural",
        "subject": subject,
        "htmlBody": html,
        "plainTextBody": plain,
        "styleReason": "example host draft executor output",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Example host draft executor for WotoHub")
    ap.add_argument("--input", required=True, help="Path to host draft request JSON")
    ap.add_argument("--output", help="Path to write executor output JSON")
    args = ap.parse_args()

    request = json.loads(Path(args.input).read_text(encoding="utf-8"))
    creators = [item for item in (request.get("selectedCreators") or []) if isinstance(item, dict)]
    brief = request.get("brief") or {}
    language = request.get("emailLanguage") or "en"
    drafts = [_draft_for_creator(creator, brief, language) for creator in creators]
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
