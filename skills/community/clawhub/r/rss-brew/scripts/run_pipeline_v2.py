#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


SCRIPT_DIR = Path(__file__).resolve().parent
APP_SRC_DIR = SCRIPT_DIR.parent / "app" / "src"
if str(APP_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(APP_SRC_DIR))

from rss_brew.state.manifests import list_committed_manifests, read_json, update_manifest, write_json
from rss_brew.state.publish import write_current_pointers
from rss_brew.state.winner import select_winner

ARTICLE_CATEGORIES = [
    "ai-frontier-tech",
    "vc-investment",
    "startup-strategy",
    "business-insights",
    "china-tech-market",
    "product-design",
    "learning-career",
    "productivity-tools",
    "strategy-analysis",
    "other",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_cmd(cmd: list[str]) -> int:
    print("[orchestrator] $", " ".join(cmd))
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"[orchestrator] ERROR: command failed with code {res.returncode}", file=sys.stderr)
    return res.returncode


def copy_if_exists(src: Path, dst: Path) -> None:
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copytree_replace(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_dir():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_digest_artifacts_to_versioned(publish_dir: Path, *artifacts: Path) -> None:
    for artifact in artifacts:
        if artifact.exists() and artifact.is_file():
            copy_if_exists(artifact, publish_dir / artifact.name)


def pick_latest(pub: Path, pattern: str) -> Path | None:
    candidates = sorted(pub.glob(pattern))
    return candidates[-1] if candidates else None


def promote_digest_artifacts(pub: Path, digest_path: Path) -> None:
    digest_dir = digest_path.parent
    digest_dir.mkdir(parents=True, exist_ok=True)

    src_md = (pub / digest_path.name) if (pub / digest_path.name).exists() else pick_latest(pub, "daily-digest-*.md")
    if src_md:
        copy_if_exists(src_md, digest_path)

    src_html = (pub / digest_path.with_suffix('.html').name) if (pub / digest_path.with_suffix('.html').name).exists() else pick_latest(pub, "rss-brew-digest-*.html")
    if src_html:
        copy_if_exists(src_html, digest_path.with_suffix('.html'))

    src_pdf = (pub / digest_path.with_suffix('.pdf').name) if (pub / digest_path.with_suffix('.pdf').name).exists() else pick_latest(pub, "rss-brew-digest-*.pdf")
    if src_pdf:
        copy_if_exists(src_pdf, digest_path.with_suffix('.pdf'))


def publish_staging_to_versioned(staging_dir: Path, publish_dir: Path, *digest_artifacts: Path) -> None:
    publish_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        "new-articles.json",
        "rule-filtered-articles.json",
        "model-scored-articles.json",
        "ranked-articles.json",
        "distribution.json",
        "scored-articles.json",
        "scored-articles.enriched.json",
        "deep-set.json",
        "deep-set.enriched.json",
        "other-set.json",
        "processed-index.json",
        "metadata.json",
    ]:
        copy_if_exists(staging_dir / name, publish_dir / name)

    copy_digest_artifacts_to_versioned(publish_dir, *digest_artifacts)

    if (staging_dir / "run-stats").exists():
        copytree_replace(staging_dir / "run-stats", publish_dir / "run-stats")

    for category in ARTICLE_CATEGORIES:
        src = staging_dir / category
        if src.exists() and src.is_dir():
            copytree_replace(src, publish_dir / category)


def resolve_winner_publish_dir(winner: Dict[str, Any], data_root: Path, day: str) -> Path | None:
    published_path = winner.get("published_path")
    if isinstance(published_path, str) and published_path:
        pub = Path(published_path)
        if pub.exists():
            return pub

    winner_run_id = str(winner.get("run_id") or "").strip()
    if winner_run_id:
        fallback = data_root / "daily" / day / winner_run_id
        if fallback.exists():
            return fallback

    return None


def promote_winner_outputs(
    winner_publish_dir: Path,
    data_root: Path,
    new_articles: Path,
    scored: Path,
    deep_set: Path,
    digest_path: Path,
    dedup: Path,
    metadata: Path,
) -> bool:
    pub = winner_publish_dir
    if not pub.exists():
        return False

    copy_if_exists(pub / "new-articles.json", new_articles)
    copy_if_exists(pub / "scored-articles.json", scored)
    copy_if_exists(pub / "deep-set.json", deep_set)
    copy_if_exists(pub / "other-set.json", data_root / "other-set.json")
    copy_if_exists(pub / "ranked-articles.json", data_root / "ranked-articles.json")
    copy_if_exists(pub / "distribution.json", data_root / "distribution.json")
    copy_if_exists(pub / "rule-filtered-articles.json", data_root / "rule-filtered-articles.json")
    copy_if_exists(pub / "model-scored-articles.json", data_root / "model-scored-articles.json")
    copy_if_exists(pub / "processed-index.json", dedup)
    copy_if_exists(pub / "metadata.json", metadata)

    promote_digest_artifacts(pub, digest_path)

    if (pub / "run-stats").exists():
        copytree_replace(pub / "run-stats", data_root / "run-stats")

    for category in ARTICLE_CATEGORIES:
        src = pub / category
        if src.exists() and src.is_dir():
            copytree_replace(src, data_root / category)

    return True


def main() -> None:
    ap = argparse.ArgumentParser(description="RSS-Brew token-saving pipeline v2 orchestrator")
    ap.add_argument("--python", default=sys.executable, help="Python interpreter for sub-steps")
    ap.add_argument("--data-root", default="/root/workplace/2 Areas/rss-brew-data")
    ap.add_argument("--sources", default=None)
    ap.add_argument("--dedup", default=None)
    ap.add_argument("--metadata", default=None)
    ap.add_argument("--new-articles", default=None)
    ap.add_argument("--scored", default=None)
    ap.add_argument("--deep-set", default=None)
    ap.add_argument("--digest", default=None)
    ap.add_argument("--run-stats-dir", default=None)
    ap.add_argument("--skip-core", action="store_true")
    ap.add_argument("--mock", action="store_true", help="Mock model calls for dry-run")
    ap.add_argument("--debug", action="store_true", help="Enable debug-only behaviors (e.g. env limits)")
    # compatibility no-op: v2 is now the only path
    ap.add_argument("--scoring-v2", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--enable-enrichment", action="store_true")
    args = ap.parse_args()

    data_root = Path(args.data_root)
    sources = Path(args.sources or data_root / "sources.yaml")
    dedup = Path(args.dedup or data_root / "processed-index.json")
    metadata = Path(args.metadata or data_root / "metadata.json")
    new_articles = Path(args.new_articles or data_root / "new-articles.json")
    scored = Path(args.scored or data_root / "scored-articles.json")
    deep_set = Path(args.deep_set or data_root / "deep-set.json")
    run_stats_dir = Path(args.run_stats_dir or data_root / "run-stats")

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{os.getpid()}"
    run_records_day = data_root / "run-records" / day
    prior_manifests = list_committed_manifests(run_records_day)
    attempt = len(prior_manifests) + 1

    digest_path = Path(args.digest) if args.digest else (data_root / "digests" / f"daily-digest-{day}.md")
    manifest_path = run_records_day / f"{run_id}.json"

    staging_dir = data_root / ".staging" / run_id
    staging_digest_dir = staging_dir / "digests"
    staging_run_stats_dir = staging_dir / "run-stats"

    staged_new = staging_dir / "new-articles.json"
    staged_rule_filtered = staging_dir / "rule-filtered-articles.json"
    staged_model_scored = staging_dir / "model-scored-articles.json"
    staged_ranked = staging_dir / "ranked-articles.json"
    staged_distribution = staging_dir / "distribution.json"
    staged_scored = staging_dir / "scored-articles.json"
    staged_deep = staging_dir / "deep-set.json"
    staged_deep_enriched = staging_dir / "deep-set.enriched.json"
    staged_other = staging_dir / "other-set.json"
    staged_dedup = staging_dir / "processed-index.json"
    staged_metadata = staging_dir / "metadata.json"
    staged_digest = staging_digest_dir / f"daily-digest-{day}.md"
    staged_html = staging_digest_dir / f"rss-brew-digest-{day}.html"
    staged_pdf = staging_digest_dir / f"rss-brew-digest-{day}.pdf"

    daily_dir = data_root / "daily" / day
    publish_dir = daily_dir / run_id
    finalize_lock_path = daily_dir / ".finalize.lock"

    manifest: Dict[str, Any] = {
        "day": day,
        "run_id": run_id,
        "attempt": attempt,
        "started_at": now_iso(),
        "finished_at": None,
        "status": "running",
        "new_articles": 0,
        "deep_set_count": 0,
        "failure_reason": None,
        "delivery_status": "pending",
        "staging_path": str(staging_dir),
        "published_path": None,
        "finalize_started_at": None,
        "finalize_finished_at": None,
        "commit_token": None,
        "supersedes_run_id": None,
        # historical-compat field; v2 is always-on now
        "scoring_v2": True,
    }
    write_json(manifest_path, manifest)

    try:
        staging_dir.mkdir(parents=True, exist_ok=True)
        # Seed candidate dedup/metadata snapshots from current committed state.
        if dedup.exists():
            copy_if_exists(dedup, staged_dedup)
        else:
            write_json(staged_dedup, {})
        if metadata.exists():
            copy_if_exists(metadata, staged_metadata)
        else:
            write_json(staged_metadata, {})

        if not args.skip_core:
            code = run_cmd(
                [
                    args.python,
                    str(SCRIPT_DIR / "core_pipeline.py"),
                    "--sources",
                    str(sources),
                    "--dedup",
                    str(staged_dedup),
                    "--metadata",
                    str(staged_metadata),
                    "--output",
                    str(staged_new),
                    "--run-stats-dir",
                    str(staging_run_stats_dir),
                ]
            )
            if code != 0:
                raise RuntimeError(f"core_pipeline_failed:{code}")
        else:
            # Dry-run / testing mode: allow caller to supply new-articles input directly.
            # We still keep all staged artifacts inside the staging dir.
            if new_articles.exists():
                copy_if_exists(new_articles, staged_new)
            elif not staged_new.exists():
                write_json(staged_new, {"generated_at": now_iso(), "article_count": 0, "articles": []})

        new_payload = read_json(staged_new, {})
        new_count = int(new_payload.get("article_count", 0) or 0)
        manifest = update_manifest(manifest_path, {"new_articles": new_count})

        existing_winner = select_winner(prior_manifests)
        existing_winner_new = int((existing_winner or {}).get("new_articles", 0) or 0)
        should_skip_generation = bool(existing_winner and existing_winner_new > 0 and new_count == 0)

        if not should_skip_generation:
            rule_cmd = [
                args.python,
                str(SCRIPT_DIR / "phase_rule_filter_score.py"),
                "--input",
                str(staged_new),
                "--output",
                str(staged_rule_filtered),
            ]
            code = run_cmd(rule_cmd)
            if code != 0:
                raise RuntimeError(f"phase_rule_filter_failed:{code}")

            phase_a_cmd = [
                args.python,
                str(SCRIPT_DIR / "phase_model_score.py"),
                "--input",
                str(staged_rule_filtered),
                "--output",
                str(staged_model_scored),
                "--model",
                "CHEAP",
            ]
            limit = os.environ.get("RSS_BREW_PHASE_A_LIMIT", "").strip()
            env_mode = os.environ.get("RSS_BREW_ENV", "").strip().lower()
            if (args.debug or env_mode == "dev") and limit.isdigit() and int(limit) > 0:
                phase_a_cmd += ["--limit", limit]
            if args.mock:
                phase_a_cmd.append("--mock")
            code = run_cmd(phase_a_cmd)
            if code != 0:
                raise RuntimeError(f"phase_a_failed:{code}")

            rank_cmd = [
                args.python,
                str(SCRIPT_DIR / "phase_rank_distribute.py"),
                "--input",
                str(staged_model_scored),
                "--ranked-output",
                str(staged_ranked),
                "--distribution-output",
                str(staged_distribution),
                "--deep-output",
                str(staged_deep),
                "--other-output",
                str(staged_other),
                "--compat-scored-output",
                str(staged_scored),
                "--sources",
                str(sources),
            ]
            code = run_cmd(rank_cmd)
            if code != 0:
                raise RuntimeError(f"phase_rank_distribute_failed:{code}")

            phase_b_input = staged_deep
            if args.enable_enrichment or os.getenv("RSS_BREW_ENABLE_ENRICHMENT") == "1":
                enrich_cmd = [
                    args.python,
                    str(SCRIPT_DIR / "phase_enrich_context.py"),
                    "--input",
                    str(staged_deep),
                    "--output",
                    str(staged_deep_enriched),
                ]
                if args.mock:
                    enrich_cmd.append("--mock")
                code = run_cmd(enrich_cmd)
                if code == 0 and staged_deep_enriched.exists():
                    phase_b_input = staged_deep_enriched

            phase_b_cmd = [
                args.python,
                str(SCRIPT_DIR / "phase_b_analyze.py"),
                "--input",
                str(phase_b_input),
                "--output",
                str(staged_deep),
                "--data-root",
                str(staging_dir),
                "--model",
                "VERTEX_PRO",
                "--preselected",
            ]
            if args.mock:
                phase_b_cmd.append("--mock")
            code = run_cmd(phase_b_cmd)
            if code != 0:
                raise RuntimeError(f"phase_b_failed:{code}")

            digest_cmd = [
                args.python,
                str(SCRIPT_DIR / "digest_writer.py"),
                "--scored",
                str(staged_scored),
                "--deep-set",
                str(staged_deep),
                "--other-set",
                str(staged_other),
                "--run-stats-dir",
                str(staging_run_stats_dir),
                "--output",
                str(staged_digest),
            ]
            code = run_cmd(digest_cmd)
            if code != 0:
                raise RuntimeError(f"digest_failed:{code}")

            render_cmd = [
                args.python,
                str(SCRIPT_DIR / "render_digest_pdf_nextdraft.py"),
                "--input",
                str(staged_digest),
                "--html-output",
                str(staged_html),
                "--pdf-output",
                str(staged_pdf),
            ]
            code = run_cmd(render_cmd)
            if code != 0:
                raise RuntimeError(f"render_digest_pdf_failed:{code}")

            deep_payload = read_json(staged_deep, {})
            manifest = update_manifest(manifest_path, {"deep_set_count": int(deep_payload.get("article_count", 0) or 0)})
        else:
            manifest = update_manifest(
                manifest_path,
                {
                    "failure_reason": "guardrail_nonzero_committed_winner_preserved",
                    "deep_set_count": int((existing_winner or {}).get("deep_set_count", 0) or 0),
                },
            )

        manifest = update_manifest(manifest_path, {"status": "staged", "finished_at": now_iso()})

        daily_dir.mkdir(parents=True, exist_ok=True)
        with open(finalize_lock_path, "a+", encoding="utf-8") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)

            manifest = update_manifest(
                manifest_path,
                {
                    "status": "finalize_in_progress",
                    "finalize_started_at": now_iso(),
                    "published_path": str(publish_dir),
                },
            )

            publish_staging_to_versioned(staging_dir, publish_dir, staged_digest, staged_html, staged_pdf)

            commit_token = f"{run_id}:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
            manifest = update_manifest(
                manifest_path,
                {
                    "status": "committed",
                    "finalize_finished_at": now_iso(),
                    "finished_at": now_iso(),
                    "commit_token": commit_token,
                },
            )

            committed = list_committed_manifests(run_records_day)
            winner = select_winner(committed)
            if winner:
                winner_run_id = str(winner.get("run_id") or "")
                manifest = update_manifest(manifest_path, {"supersedes_run_id": winner_run_id if winner_run_id != run_id else None})

                write_current_pointers(
                    run_records_day=run_records_day,
                    daily_dir=daily_dir,
                    day=day,
                    winner_run_id=winner_run_id,
                    selected_at=now_iso(),
                )

                # Promotion is required when the winner is the current run (it must publish & promote).
                # But if the winner is a legacy committed run from before Phase 2, it may not have
                # published_path populated. In that case, top-level outputs are already that winner,
                # so we skip promotion rather than failing the pipeline.
                promoted = True
                winner_publish_dir = resolve_winner_publish_dir(winner, data_root, day)
                if winner_run_id == run_id:
                    promoted = bool(winner_publish_dir) and promote_winner_outputs(winner_publish_dir, data_root, new_articles, scored, deep_set, digest_path, dedup, metadata)
                else:
                    if winner_publish_dir:
                        promoted = promote_winner_outputs(winner_publish_dir, data_root, new_articles, scored, deep_set, digest_path, dedup, metadata)

                if not promoted:
                    raise RuntimeError("winner_promotion_failed")

        write_json(
            data_root / "run-records" / "latest-run.json",
            {
                "day": day,
                "run_id": run_id,
                "manifest": str(manifest_path),
                "status": "committed",
            },
        )

        print("[orchestrator] DONE")

    except Exception as exc:
        manifest = update_manifest(
            manifest_path,
            {
                "status": "failed",
                "finished_at": now_iso(),
                "failure_reason": str(exc),
            },
        )
        write_json(
            data_root / "run-records" / "latest-run.json",
            {
                "day": day,
                "run_id": run_id,
                "manifest": str(manifest_path),
                "status": manifest.get("status"),
            },
        )
        print(f"[orchestrator] FAILED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
