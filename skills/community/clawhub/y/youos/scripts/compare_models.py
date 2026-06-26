"""Compare YouOS generation backends on your own mail.

Draws real (inbound → your reply) pairs from the active instance's DB, drafts
each under every available backend (local MLX+LoRA, Ollama, Claude), and scores
each draft against the reply you actually sent. Prints a side-by-side scorecard
ranked by voice-match.

Examples:
    python scripts/compare_models.py --limit 30
    python scripts/compare_models.py --backends mlx,claude --semantic
    python scripts/compare_models.py --limit 50 --json > compare.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.evaluation.model_compare import (
    BACKENDS,
    compare_models,
    detect_available_backends,
    format_comparison,
    sample_reply_pairs,
)

ROOT_DIR = Path(__file__).resolve().parents[1]


def main() -> None:
    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    parser = argparse.ArgumentParser(description="Compare YouOS generation backends on your mail")
    parser.add_argument("--limit", type=int, default=20, help="Number of held-out reply pairs to compare on")
    parser.add_argument("--backends", type=str, default=None,
                        help=f"Comma-separated subset of {','.join(BACKENDS)} (default: auto-detect available)")
    parser.add_argument("--semantic", action="store_true",
                        help="Include the embedding-based semantic score (loads the local model)")
    parser.add_argument("--min-chars", type=int, default=40, help="Skip pairs shorter than this (either side)")
    parser.add_argument("--seed", type=int, default=13, help="Sampling seed (re-runs compare the same messages)")
    parser.add_argument("--db-path", type=Path,
                        default=resolve_sqlite_path(get_settings().database_url), help="Path to SQLite database")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of the scorecard")
    args = parser.parse_args()

    database_url = f"sqlite:///{args.db_path}"
    configs_dir = ROOT_DIR / "configs"

    if args.backends:
        requested = [b.strip() for b in args.backends.split(",") if b.strip()]
        available = detect_available_backends()
        backends = [b for b in requested if b in available]
        missing = [b for b in requested if b not in available]
        if missing and not args.json:
            print(f"Skipping unavailable backend(s): {', '.join(missing)}")
    else:
        backends = detect_available_backends()

    if not backends:
        print("No generation backends available. Install one of: mlx_lm (Apple Silicon), "
              "a running Ollama server, or the `claude` CLI.")
        return

    cases = sample_reply_pairs(database_url, limit=args.limit, min_chars=args.min_chars, seed=args.seed)
    if not cases:
        print(f"No reply pairs found in {args.db_path}. Ingest some mail first "
              "(youos ingest / the /welcome wizard), then re-run.")
        return

    embed_fn = None
    if args.semantic:
        from app.core.embeddings import get_embedding

        embed_fn = get_embedding

    result = compare_models(
        cases,
        backends,
        database_url=database_url,
        configs_dir=configs_dir,
        embed_fn=embed_fn,
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(format_comparison(result))


if __name__ == "__main__":
    main()
