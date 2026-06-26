import argparse
from pathlib import Path

from app.core.config import get_ingestion_accounts
from app.ingestion.google_docs import (
    DEFAULT_DRIVE_QUERY,
    SUPPORTED_IMPORT_FORMAT,
    GogDocsLiveOptions,
    ingest_google_docs,
)


def main() -> None:
    default_accounts = get_ingestion_accounts()
    parser = argparse.ArgumentParser(description=("Import Google Docs into the YouOS SQLite database from live gog access or YouOS cached JSON snapshots."))
    parser.add_argument(
        "export_path",
        nargs="?",
        type=Path,
        default=Path("data/google_docs"),
        help="Cached Docs snapshot file or directory. Ignored when --live is used.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Optional override for the target SQLite database path.",
    )
    parser.add_argument(
        "--show-format",
        action="store_true",
        help="Print the supported import contract and exit.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live Google Docs via gog instead of reading local cached snapshots.",
    )
    parser.add_argument(
        "--account",
        action="append",
        default=[],
        help=(f"Google account to ingest via gog. Repeat for multiple accounts. Defaults to {', '.join(default_accounts)} when --live is used."),
    )
    parser.add_argument(
        "--doc-id",
        action="append",
        default=[],
        help=("Explicit Google Doc id to ingest. Repeat for multiple docs. When set, discovery via gog drive search is skipped."),
    )
    parser.add_argument(
        "--query",
        default=DEFAULT_DRIVE_QUERY,
        help=("Drive search query for live gog ingestion. Defaults to a raw Drive query for non-trashed Google Docs."),
    )
    parser.add_argument(
        "--full-text-query",
        action="store_true",
        help="Treat --query as gog drive search full-text input instead of Drive raw-query syntax.",
    )
    parser.add_argument(
        "--max-docs",
        type=int,
        default=20,
        help="Maximum docs per account for live gog discovery.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Optional directory to save raw live gog Docs snapshots as local JSON files.",
    )
    parser.add_argument(
        "--all-tabs",
        action="store_true",
        help="Read all Doc tabs via gog docs cat --all-tabs instead of default tab behavior.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=0,
        help="Pass through to gog docs cat --max-bytes. Use 0 for unlimited content.",
    )
    args = parser.parse_args()

    if args.show_format:
        print(SUPPORTED_IMPORT_FORMAT)
        return

    if args.max_docs <= 0:
        parser.error("--max-docs must be greater than 0.")

    live_options = None
    if args.live:
        live_options = GogDocsLiveOptions(
            accounts=tuple(args.account or default_accounts),
            query=args.query,
            max_docs=args.max_docs,
            cache_dir=args.cache_dir,
            raw_query=not args.full_text_query,
            all_tabs=args.all_tabs,
            max_bytes=args.max_bytes,
            doc_ids=tuple(args.doc_id),
        )

    result = ingest_google_docs(
        None if args.live else args.export_path,
        db_path=args.db_path,
        live=live_options,
    )
    if result.run_id:
        print(f"[{result.status}] run_id={result.run_id}")
    print(result.detail)
    if result.status == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
