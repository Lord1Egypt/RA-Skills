#!/usr/bin/env python3
"""查询微信素材、草稿、已发布文章"""
import argparse, json, sys
from wechat_client import count_drafts, get_draft, get_material_count, get_published_article, list_drafts, list_materials, list_published

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("materials-count")
    p = sub.add_parser("materials-list"); p.add_argument("--type", required=True, choices=["image","video","voice","news"]); p.add_argument("--offset", type=int, default=0); p.add_argument("--count", type=int, default=20)
    sub.add_parser("drafts-count")
    p = sub.add_parser("drafts-list"); p.add_argument("--offset", type=int, default=0); p.add_argument("--count", type=int, default=20); p.add_argument("--no-content", action="store_true")
    p = sub.add_parser("drafts-get"); p.add_argument("--media-id", required=True)
    p = sub.add_parser("published-list"); p.add_argument("--offset", type=int, default=0); p.add_argument("--count", type=int, default=20); p.add_argument("--no-content", action="store_true")
    p = sub.add_parser("published-get"); p.add_argument("--article-id", required=True)

    args = parser.parse_args()
    handlers = {
        "materials-count": lambda: get_material_count(),
        "materials-list": lambda: list_materials(args.type, args.offset, args.count),
        "drafts-count": lambda: count_drafts(),
        "drafts-list": lambda: list_drafts(args.offset, args.count, args.no_content),
        "drafts-get": lambda: get_draft(args.media_id),
        "published-list": lambda: list_published(args.offset, args.count, args.no_content),
        "published-get": lambda: get_published_article(args.article_id),
    }
    try:
        result = handlers[args.command]()
        json.dump({"ok": True, "step": args.command, "result": result}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except Exception as e:
        json.dump({"ok": False, "step": args.command, "message": str(e)}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
