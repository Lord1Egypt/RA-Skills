import argparse
import json
from .core import fetch_user_rss, parse_rss


def cmd_user_posts(args: argparse.Namespace) -> int:
    xml_text = fetch_user_rss(args.username)
    items = parse_rss(xml_text, limit=args.limit)
    if args.format == "json":
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        for it in items:
            date = f" — {it['date']}" if it.get('date') else ""
            print(f"- [{it['title']}]({it['link']}){date}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="velog-cli", description="Velog public RSS CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_user = sub.add_parser("user-posts", help="Fetch latest posts for a user")
    p_user.add_argument("--username", required=True, help="Velog username (without @)")
    p_user.add_argument("--limit", type=int, default=10, help="Number of posts to fetch")
    p_user.add_argument("--format", choices=["md", "json"], default="md")
    p_user.set_defaults(func=cmd_user_posts)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
