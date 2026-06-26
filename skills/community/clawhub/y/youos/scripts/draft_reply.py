import argparse
import json
import sys
from pathlib import Path

from app.core.settings import get_settings
from app.generation.service import DraftRequest, generate_draft


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Draft a reply in your style using retrieved precedent from the YouOS corpus.")
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="The inbound message to draft a reply to.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read the inbound message from stdin.",
    )
    parser.add_argument(
        "--mode",
        choices=("work", "personal"),
        default=None,
        help="Override mode detection (work or personal).",
    )
    parser.add_argument(
        "--audience",
        default=None,
        help='Audience hint, e.g. "client", "colleague", "friend".',
    )
    parser.add_argument(
        "--account",
        default=None,
        help="Filter retrieval to a specific account email.",
    )
    parser.add_argument(
        "--top-k-reply-pairs",
        type=int,
        default=5,
        help="Number of reply-pair exemplars to retrieve.",
    )
    parser.add_argument(
        "--top-k-chunks",
        type=int,
        default=3,
        help="Number of document chunks to retrieve.",
    )
    parser.add_argument(
        "--sender",
        default=None,
        help="Sender email address for sender-aware retrieval boosting.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Optional SQLite database path override.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.stdin:
        inbound_message = sys.stdin.read().strip()
    elif args.message:
        inbound_message = args.message
    else:
        build_parser().print_help()
        sys.exit(1)

    if not inbound_message:
        print("Error: empty inbound message.", file=sys.stderr)
        sys.exit(1)

    settings = get_settings()
    database_url = settings.database_url
    if args.db_path is not None:
        database_url = f"sqlite:///{args.db_path}"

    request = DraftRequest(
        inbound_message=inbound_message,
        mode=args.mode,
        audience_hint=args.audience,
        top_k_reply_pairs=args.top_k_reply_pairs,
        top_k_chunks=args.top_k_chunks,
        account_email=args.account,
        sender=args.sender,
    )

    response = generate_draft(
        request,
        database_url=database_url,
        configs_dir=settings.configs_dir,
    )

    print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
