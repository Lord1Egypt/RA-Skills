import argparse
from pathlib import Path

from app.core.config import get_ingestion_accounts
from app.ingestion.gmail_threads import (
    SUPPORTED_IMPORT_FORMAT,
    GogLiveOptions,
    ingest_gmail_threads,
)


def build_parser() -> argparse.ArgumentParser:
    default_accounts = get_ingestion_accounts()
    parser = argparse.ArgumentParser(description="Import Gmail threads into the YouOS SQLite database from live gog access or local JSON dumps.")
    parser.add_argument(
        "export_path",
        nargs="?",
        default="data/gmail",
        help="JSON file or directory of Gmail thread dumps. Ignored when --live is used.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path. Defaults to YOUOS_DATABASE_URL.",
    )
    parser.add_argument(
        "--user-email",
        action="append",
        default=[],
        help="User-owned email address. Repeat the flag for multiple addresses.",
    )
    parser.add_argument(
        "--user-name",
        action="append",
        default=[],
        help="User-owned display name. Repeat the flag for multiple names.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live Gmail threads via gog instead of reading local JSON.",
    )
    parser.add_argument(
        "--account",
        action="append",
        default=[],
        help=(f"Gmail account to ingest via gog. Repeat for multiple accounts. Defaults to {', '.join(default_accounts)} when --live is used."),
    )
    parser.add_argument(
        "--query",
        default="in:anywhere",
        help="Gmail search query for live gog ingestion.",
    )
    parser.add_argument(
        "--max-threads",
        type=int,
        default=50,
        help="Maximum threads per account for live gog ingestion. Use 0 to fetch all matched threads.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Optional directory to save raw live gog thread payloads as local JSON snapshots.",
    )
    parser.add_argument(
        "--show-format",
        action="store_true",
        help="Print the supported local import format and exit.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.show_format:
        print(SUPPORTED_IMPORT_FORMAT)
        return

    default_accounts = get_ingestion_accounts()

    live_options = None
    if args.live:
        live_options = GogLiveOptions(
            accounts=tuple(args.account or default_accounts),
            query=args.query,
            max_threads=None if args.max_threads == 0 else args.max_threads,
            cache_dir=args.cache_dir,
        )

    result = ingest_gmail_threads(
        None if args.live else Path(args.export_path),
        db_path=args.db_path,
        user_emails=tuple(args.user_email),
        user_names=tuple(args.user_name),
        live=live_options,
    )
    if result.run_id:
        print(f"[{result.status}] run_id={result.run_id}")
    print(result.detail)
    if result.status == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
