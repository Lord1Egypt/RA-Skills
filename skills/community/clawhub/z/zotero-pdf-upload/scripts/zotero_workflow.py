#!/usr/bin/env python3
"""CLI workflow helpers for standalone Zotero operations.

Design principles:
- Parse and inspect without writing by default.
- Require explicit flags before creating collections/items.
- Keep output machine-readable JSON for agent chaining.
"""


import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from zotero_client import ConfigError, ZoteroClient, parse_zotero_library_url, resolve_library_settings


def _load_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _render_collection(col: Dict[str, Any]) -> Dict[str, Any]:
    data = col.get("data", {}) if isinstance(col, dict) else {}
    key = col.get("key") or data.get("key")
    return {
        "key": key,
        "name": data.get("name") or col.get("name") or "",
        "parentCollection": data.get("parentCollection"),
        "version": col.get("version") or data.get("version"),
    }


def cmd_parse_url(args: argparse.Namespace) -> int:
    parsed = parse_zotero_library_url(args.url)
    print(json.dumps({"ok": True, "parsed": parsed}, ensure_ascii=False, indent=2))
    return 0


def _client_from_config(config_path: str) -> ZoteroClient:
    cfg = _load_json(config_path)
    settings = resolve_library_settings(cfg, require_api_key=True)
    return ZoteroClient(
        api_key=settings.api_key,
        library_id=settings.library_id,
        library_type=settings.library_type,
        timeout=int(cfg.get("zotero", {}).get("timeoutSec", 30)),
    )


def cmd_list_collections(args: argparse.Namespace) -> int:
    cfg = _load_json(args.config)
    settings = resolve_library_settings(cfg, require_api_key=True)
    client = ZoteroClient(
        api_key=settings.api_key,
        library_id=settings.library_id,
        library_type=settings.library_type,
        timeout=int(cfg.get("zotero", {}).get("timeoutSec", 30)),
    )

    collections = client.list_collections_paged(max_items=args.max_items, page_size=args.page_size)
    rendered = [_render_collection(c) for c in collections]

    item_for_match: Dict[str, Any] = {
        "title": args.title or "",
        "abstractNote": args.abstract or "",
        "tags": args.tags or [],
    }

    match = None
    if any(item_for_match.values()) or args.collection_name_hint:
        best, score, reason = client.find_best_matching_collection(
            item=item_for_match,
            collections=collections,
            collection_name_hint=args.collection_name_hint or "",
        )
        if best is not None:
            match = {
                "collection": _render_collection(best),
                "score": score,
                "reason": reason,
            }
        else:
            match = {
                "collection": None,
                "score": score,
                "reason": reason,
                "suggestedCollectionName": client.suggest_collection_name(item_for_match),
            }

    print(
        json.dumps(
            {
                "ok": True,
                "library": {
                    "type": settings.library_type,
                    "id": settings.library_id,
                    "apiKeySource": settings.api_key_source,
                },
                "collections": rendered,
                "match": match,
                "note": "No write performed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_choose_collection(args: argparse.Namespace) -> int:
    payload = _load_json(args.item_json)

    if args.collections_json:
        collections = json.loads(Path(args.collections_json).read_text(encoding="utf-8"))
        collections = collections if isinstance(collections, list) else []
        client = None
    else:
        cfg = _load_json(args.config)
        settings = resolve_library_settings(cfg, require_api_key=True)
        client = ZoteroClient(
            api_key=settings.api_key,
            library_id=settings.library_id,
            library_type=settings.library_type,
            timeout=int(cfg.get("zotero", {}).get("timeoutSec", 30)),
        )
        collections = client.list_collections_paged(max_items=args.max_items, page_size=args.page_size)

    worker = client or ZoteroClient(api_key="dummy", library_id="0", library_type="user")
    best, score, reason = worker.find_best_matching_collection(
        item=payload,
        collections=collections,
        collection_name_hint=args.collection_name_hint or "",
    )

    if best is None:
        result = {
            "status": "pending-new-collection-approval",
            "matchedCollection": None,
            "matchScore": score,
            "reason": reason,
            "suggestedCollectionName": worker.suggest_collection_name(payload),
            "approvalRequired": True,
            "nextAction": "Run create-collection explicitly after human approval",
        }
    else:
        result = {
            "status": "matched-existing-collection",
            "matchedCollection": _render_collection(best),
            "matchScore": score,
            "reason": reason,
            "approvalRequired": False,
        }

    print(json.dumps({"ok": True, "result": result}, ensure_ascii=False, indent=2))
    return 0


def cmd_create_collection(args: argparse.Namespace) -> int:
    if not args.approve_create:
        raise ConfigError("Refusing to create collection without --approve-create")

    client = _client_from_config(args.config)
    resp = client.create_collection(name=args.name, parent_collection_key=args.parent_key)

    print(
        json.dumps(
            {
                "ok": True,
                "action": "create-collection",
                "response": resp,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _extract_created_item_key(resp: Dict[str, Any]) -> Optional[str]:
    successful = resp.get("successful") if isinstance(resp, dict) else None
    if not isinstance(successful, dict):
        return None
    first = next(iter(successful.values()), None)
    if isinstance(first, dict):
        return first.get("key")
    return None


def _normalize_tags(raw_tags: Any) -> List[str]:
    if not isinstance(raw_tags, list):
        return []
    out = []
    for tag in raw_tags:
        if isinstance(tag, dict):
            value = str(tag.get("tag") or "").strip()
        else:
            value = str(tag).strip()
        if value:
            out.append(value)
    return out


def cmd_create_item(args: argparse.Namespace) -> int:
    if not args.approve_write:
        raise ConfigError("Refusing to create item without --approve-write")

    cfg = _load_json(args.config)
    client = _client_from_config(args.config)

    item_input = _load_json(args.item_json)
    normalized_item = {
        "itemType": item_input.get("itemType", "journalArticle"),
        "title": item_input.get("title", ""),
        "creators": item_input.get("creators", []),
        "abstractNote": item_input.get("abstractNote", item_input.get("summary", "")),
        "date": item_input.get("date", ""),
        "url": item_input.get("url", item_input.get("entry_url", "")),
        "DOI": item_input.get("DOI", ""),
        "archive": item_input.get("archive", ""),
        "archiveLocation": item_input.get("archiveLocation", item_input.get("id", "")),
        "extra": item_input.get("extra", ""),
        "tags": _normalize_tags(item_input.get("tags", [])),
    }

    collection_key = args.collection_key or ""

    if not collection_key and args.auto_match_collection:
        collections = client.list_collections_paged(max_items=args.max_items, page_size=args.page_size)
        best, score, reason = client.find_best_matching_collection(
            item=normalized_item,
            collections=collections,
            collection_name_hint=args.collection_name_hint or "",
        )
        if best is None:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "status": "pending-new-collection-approval",
                        "reason": reason,
                        "matchScore": score,
                        "suggestedCollectionName": client.suggest_collection_name(normalized_item),
                        "note": "No item write performed",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 2
        rendered_best = _render_collection(best)
        collection_key = str(rendered_best.get("key") or "")

    payload = client.build_item_payload(normalized_item, collection_key=collection_key or None)
    resp = client.create_item(payload)
    item_key = _extract_created_item_key(resp)

    attachment = None
    if args.attach_pdf and item_key:
        allow_attach = bool(cfg.get("zotero", {}).get("allowPdfUpload", True))
        if not allow_attach:
            attachment = {
                "status": "skipped",
                "reason": "zotero.allowPdfUpload=false in config",
            }
        else:
            attachment = client.upload_pdf_attachment(
                parent_item_key=item_key,
                pdf_path=args.attach_pdf,
                title=args.attachment_title or "",
            )

    print(
        json.dumps(
            {
                "ok": True,
                "action": "create-item",
                "collectionKey": collection_key or None,
                "response": resp,
                "itemKey": item_key,
                "attachment": attachment,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Standalone Zotero workflow CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_parse = sub.add_parser("parse-url", help="Parse Zotero group/user URL")
    p_parse.add_argument("--url", required=True)
    p_parse.set_defaults(func=cmd_parse_url)

    p_list = sub.add_parser("list-collections", help="List collections and optional heuristic match")
    p_list.add_argument("--config", required=True)
    p_list.add_argument("--max-items", type=int, default=300)
    p_list.add_argument("--page-size", type=int, default=100)
    p_list.add_argument("--title", default="")
    p_list.add_argument("--abstract", default="")
    p_list.add_argument("--tags", nargs="*", default=[])
    p_list.add_argument("--collection-name-hint", default="")
    p_list.set_defaults(func=cmd_list_collections)

    p_choose = sub.add_parser("choose-collection", help="Choose best existing collection; never auto-create")
    p_choose.add_argument("--config", help="Runtime config JSON (required unless --collections-json is used)")
    p_choose.add_argument("--collections-json", help="Optional local collection list JSON for offline tests")
    p_choose.add_argument("--item-json", required=True, help="Item metadata JSON")
    p_choose.add_argument("--collection-name-hint", default="")
    p_choose.add_argument("--max-items", type=int, default=300)
    p_choose.add_argument("--page-size", type=int, default=100)
    p_choose.set_defaults(func=cmd_choose_collection)

    p_create_col = sub.add_parser("create-collection", help="Explicitly create a collection")
    p_create_col.add_argument("--config", required=True)
    p_create_col.add_argument("--name", required=True)
    p_create_col.add_argument("--parent-key", default="")
    p_create_col.add_argument("--approve-create", action="store_true", help="Required safety flag")
    p_create_col.set_defaults(func=cmd_create_collection)

    p_create_item = sub.add_parser("create-item", help="Create item metadata and optionally attach PDF")
    p_create_item.add_argument("--config", required=True)
    p_create_item.add_argument("--item-json", required=True)
    p_create_item.add_argument("--collection-key", default="")
    p_create_item.add_argument("--collection-name-hint", default="")
    p_create_item.add_argument("--auto-match-collection", action="store_true")
    p_create_item.add_argument("--attach-pdf", default="")
    p_create_item.add_argument("--attachment-title", default="")
    p_create_item.add_argument("--max-items", type=int, default=300)
    p_create_item.add_argument("--page-size", type=int, default=100)
    p_create_item.add_argument("--approve-write", action="store_true", help="Required safety flag")
    p_create_item.set_defaults(func=cmd_create_item)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if not getattr(args, "cmd", None):
            parser.print_help()
            return 2

        if args.cmd == "choose-collection" and not args.collections_json and not args.config:
            raise ConfigError("choose-collection requires --config or --collections-json")

        return int(args.func(args))
    except ConfigError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
