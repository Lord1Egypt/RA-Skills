"""CLI runner for YouOS Autoresearch optimizer."""

from __future__ import annotations

import argparse
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.autoresearch.optimizer import format_report, run_autoresearch
from app.core.settings import get_settings, get_var_dir
from app.db.bootstrap import resolve_sqlite_path
from app.generation.service import DraftRequest, generate_draft

ROOT_DIR = Path(__file__).resolve().parents[1]

logger = logging.getLogger(__name__)


def _git_available() -> bool:
    """Check if git is available and we're in a repo."""
    try:
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            timeout=10,
            cwd=ROOT_DIR,
        )
        return result.returncode == 0
    except Exception:
        return False


def _git_commit_hash() -> str | None:
    """Return current HEAD commit hash, or None."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=ROOT_DIR,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def _log_git_hash_to_autoresearch_log() -> None:
    """Append current git commit hash to autoresearch_log.md."""
    commit_hash = _git_commit_hash()
    if not commit_hash:
        logger.warning("Could not get git commit hash for autoresearch log")
        return
    # Match `app.core.stats.AUTORESEARCH_LOG` which already reads from the
    # active instance's var/ — without this, the writer (here) and reader
    # (stats) used different files on a non-default YOUOS_DATA_DIR.
    log_path = get_var_dir() / "autoresearch_log.md"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = f"\n## Run started — {timestamp}\n- Git commit: {commit_hash}\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def _git_commit_kept_change(
    surface_name: str,
    old_value: Any,
    new_value: Any,
    baseline_composite: float,
    candidate_composite: float,
) -> None:
    """Commit config changes for a kept autoresearch improvement."""
    msg = f"autoresearch: keep {surface_name} {old_value} → {new_value} (composite {baseline_composite:.4f} → {candidate_composite:.4f})"
    try:
        subprocess.run(
            ["git", "add", "configs/retrieval/defaults.yaml", "configs/prompts.yaml"],
            capture_output=True,
            timeout=10,
            cwd=ROOT_DIR,
        )
        subprocess.run(
            ["git", "commit", "-m", msg],
            capture_output=True,
            timeout=10,
            cwd=ROOT_DIR,
        )
    except Exception as exc:
        logger.warning("Failed to git commit autoresearch change: %s", exc)


def _git_tag_run(
    baseline_composite: float,
    final_composite: float,
    improvements_kept: int,
) -> None:
    """Tag the end of an autoresearch run with improvements."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tag_name = f"autoresearch-{timestamp}"
    tag_msg = f"composite {baseline_composite:.4f} → {final_composite:.4f}, {improvements_kept} improvements"
    try:
        subprocess.run(
            ["git", "tag", tag_name, "-m", tag_msg],
            capture_output=True,
            timeout=10,
            cwd=ROOT_DIR,
        )
    except Exception as exc:
        logger.warning("Failed to create autoresearch git tag: %s", exc)


def resolve_paths(db_path: Path | None, configs_dir: Path | None) -> tuple[str, Path]:
    """Resolve the DB URL + configs dir for the active instance.

    Defaults come from settings, which derive from ``YOUOS_DATA_DIR``; explicit
    CLI args override. This is what makes autoresearch operate on the instance
    it's meant to tune rather than the repo's default config/DB.
    """
    settings = get_settings()
    resolved_db = db_path or resolve_sqlite_path(settings.database_url)
    resolved_configs = configs_dir or settings.configs_dir
    return f"sqlite:///{resolved_db}", resolved_configs


def _generate_for_eval(
    prompt_text: str,
    *,
    database_url: str,
    configs_dir: Path,
) -> dict[str, Any]:
    """Wrap generate_draft for the eval runner interface."""
    response = generate_draft(
        DraftRequest(inbound_message=prompt_text),
        database_url=database_url,
        configs_dir=configs_dir,
    )
    return {
        "draft": response.draft,
        "detected_mode": response.detected_mode,
        "confidence": response.confidence,
        "precedent_count": len(response.precedent_used),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run YouOS Autoresearch optimizer")
    parser.add_argument(
        "--max-iter",
        type=int,
        default=10,
        help="Maximum number of eval iterations (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show mutation plan without executing",
    )
    parser.add_argument(
        "--surface",
        type=str,
        default=None,
        choices=["retrieval", "prompt_drafting"],
        help="Only tune a specific config surface",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Path to SQLite database (default: the active instance from YOUOS_DATA_DIR)",
    )
    parser.add_argument(
        "--configs-dir",
        type=Path,
        default=None,
        help="Path to configs/ directory (default: the active instance from YOUOS_DATA_DIR)",
    )
    args = parser.parse_args()

    # Resolve the DB and configs from the active instance (YOUOS_DATA_DIR) unless
    # explicitly overridden. These used to be hardcoded to the repo paths, so
    # autoresearch always optimized the repo's default config against the repo
    # DB and never touched the actual instance it was meant to tune.
    database_url, configs_dir = resolve_paths(args.db_path, args.configs_dir)

    has_git = _git_available()
    if not has_git:
        logger.warning("Git not available — skipping git commits/tags for autoresearch")

    # Log git commit hash at start of run
    if has_git:
        _log_git_hash_to_autoresearch_log()

    report = run_autoresearch(
        configs_dir=configs_dir,
        database_url=database_url,
        generate_fn=_generate_for_eval,
        max_iterations=args.max_iter,
        dry_run=args.dry_run,
        surface_filter=args.surface,
    )

    # Git commit each kept improvement and tag the run
    if has_git and not args.dry_run:
        for it in report.iterations:
            if it.kept:
                # Parse old → new from mutation_desc (e.g. "top_k_reply_pairs: 8 → 9")
                parts = it.mutation_desc.split(": ", 1)
                if len(parts) == 2:
                    values = parts[1]
                    val_parts = values.split(" → ")
                    if len(val_parts) == 2:
                        old_val, new_val = val_parts
                    else:
                        old_val, new_val = "?", "?"
                else:
                    old_val, new_val = "?", "?"
                _git_commit_kept_change(
                    it.surface_name,
                    old_val,
                    new_val,
                    it.baseline_composite,
                    it.candidate_composite,
                )

        if report.improvements_kept > 0:
            _git_tag_run(
                report.baseline.composite,
                report.final.composite,
                report.improvements_kept,
            )

    print(format_report(report))


if __name__ == "__main__":
    main()
