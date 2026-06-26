import argparse
import json
from pathlib import Path

from app.core.settings import get_settings
from app.retrieval.service import RetrievalRequest, retrieve_context


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Look up similar past replies and relevant document evidence from the YouOS corpus. "
            "This uses lexical and metadata-aware ranking only; embeddings are not implemented yet."
        )
    )
    parser.add_argument("query", help="Natural-language lookup query.")
    parser.add_argument(
        "--scope",
        choices=("all", "documents", "reply_pairs"),
        default="all",
        help="Restrict retrieval to document evidence, reply pairs, or both.",
    )
    parser.add_argument(
        "--source-type",
        action="append",
        default=[],
        help="Filter by source type. Repeat for multiple values, for example gmail_thread or google_doc.",
    )
    parser.add_argument(
        "--account",
        action="append",
        default=[],
        help="Filter by source account email. Repeat for multiple values.",
    )
    parser.add_argument(
        "--top-k-documents",
        type=int,
        default=None,
        help="Override the number of document matches returned.",
    )
    parser.add_argument(
        "--top-k-chunks",
        type=int,
        default=None,
        help="Override the number of chunk matches returned.",
    )
    parser.add_argument(
        "--top-k-reply-pairs",
        type=int,
        default=None,
        help="Override the number of reply-pair matches returned.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Optional SQLite database path override. Defaults to YOUOS_DATABASE_URL.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = get_settings()
    database_url = settings.database_url
    if args.db_path is not None:
        database_url = f"sqlite:///{args.db_path}"

    response = retrieve_context(
        RetrievalRequest(
            query=args.query,
            scope=args.scope,
            source_types=tuple(args.source_type),
            account_emails=tuple(args.account),
            top_k_documents=args.top_k_documents,
            top_k_chunks=args.top_k_chunks,
            top_k_reply_pairs=args.top_k_reply_pairs,
        ),
        database_url=database_url,
        configs_dir=settings.configs_dir,
    )
    print(json.dumps(response.to_dict(), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
