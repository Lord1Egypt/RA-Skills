#!/usr/bin/env python3
"""创建或更新微信公众号草稿"""
import argparse
import json
import sys

from wechat_client import WeChatSkillError, add_draft, get_draft, update_draft, upload_permanent_material
from normalize_article import normalize_article_payload


def resolve_thumb(payload: dict) -> tuple[str, str | None]:
    if payload.get("thumb_media_id"):
        return payload["thumb_media_id"], None
    path = payload.get("thumb_image_path")
    if not path:
        raise WeChatSkillError("Missing cover: provide thumb_media_id or thumb_image_path")
    result = upload_permanent_material(path, payload.get("thumb_upload_type", "thumb"))
    mid = result.get("media_id")
    if not mid:
        raise WeChatSkillError("Material upload ok but media_id missing")
    return mid, path


def fetch_preview_urls(media_id: str) -> list[str]:
    try:
        detail = get_draft(media_id)
        return [item["url"] for item in detail.get("news_item", []) if item.get("url")]
    except Exception:
        return []


def build_article(payload: dict, thumb_media_id: str) -> dict:
    for key in ["title", "author", "digest", "content"]:
        if not payload.get(key):
            raise WeChatSkillError(f"Missing: {key}")
    return {
        "title": payload["title"], "author": payload["author"], "digest": payload["digest"],
        "content": payload["content"], "thumb_media_id": thumb_media_id,
        "content_source_url": payload.get("content_source_url", ""),
        "need_open_comment": int(payload.get("need_open_comment", 0)),
        "only_fans_can_comment": int(payload.get("only_fans_can_comment", 0)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--index", type=int, default=0)
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    try:
        payload, normalization = normalize_article_payload(payload)
        thumb_media_id, uploaded_from = resolve_thumb(payload)
        article = build_article(payload, thumb_media_id)

        if args.update:
            media_id = payload.get("draft_media_id") or payload.get("media_id")
            if not media_id:
                raise WeChatSkillError("Update requires draft_media_id")
            result = update_draft(media_id, article, index=args.index)
            preview_urls = fetch_preview_urls(media_id)
            output = {"ok": True, "step": "upsert_draft", "mode": "update", "media_id": media_id,
                       "preview_urls": preview_urls, "thumb_media_id": thumb_media_id,
                       "uploaded_thumb_from": uploaded_from, "content_normalization": normalization, "result": result}
        else:
            result = add_draft(article)
            draft_id = result.get("media_id")
            preview_urls = fetch_preview_urls(draft_id) if draft_id else []
            output = {"ok": True, "step": "upsert_draft", "mode": "create", "media_id": draft_id,
                       "preview_urls": preview_urls, "thumb_media_id": thumb_media_id,
                       "uploaded_thumb_from": uploaded_from, "content_normalization": normalization, "result": result}

        json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except Exception as e:
        json.dump({"ok": False, "step": "upsert_draft", "message": str(e)}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
