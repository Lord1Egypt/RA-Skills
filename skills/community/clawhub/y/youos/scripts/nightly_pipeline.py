"""Nightly YouOS pipeline: ingestion → auto-feedback → fine-tune → autoresearch.

Runs all steps sequentially. Each step is best-effort — failures are logged
but don't block subsequent steps.
"""

from __future__ import annotations

import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Make the repo root importable so `from scripts.X import Y` (used below for
# auto-feedback, persona, golden eval helpers) works when this file is invoked
# directly — e.g. `python3 scripts/nightly_pipeline.py` under launchd puts
# `scripts/` on sys.path[0] but not the parent, so `import scripts` fails.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from app.core.config import get_ingestion_accounts, get_last_ingest_at, set_last_ingest_at  # noqa: E402
from app.core.settings import get_settings, get_var_dir  # noqa: E402
from app.db.bootstrap import resolve_sqlite_path  # noqa: E402

ROOT_DIR = Path(__file__).resolve().parents[1]
# Operate on the active instance's DB (YOUOS_DATA_DIR), not the repo's, so the
# autoresearch gate and other DB-dependent steps check the right database.
DEFAULT_DB = resolve_sqlite_path(get_settings().database_url)

ACCOUNTS = get_ingestion_accounts()


def _run_step(name: str, cmd: list[str], timeout: int = 600) -> bool:
    """Run a subprocess step. Returns True on success."""
    print(f"\n{'=' * 60}")
    print(f"STEP: {name}")
    print(f"{'=' * 60}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print(f"  [WARN] {name} exited with code {result.returncode}")
            return False
        print(f"  [OK] {name} completed")
        return True
    except subprocess.TimeoutExpired:
        print(f"  [WARN] {name} timed out after {timeout}s")
        return False
    except Exception as exc:
        print(f"  [WARN] {name} failed: {exc}")
        return False


def _verbose_print(step_num: int, total: int, name: str, count: str | None = None) -> None:
    """Print Rich-style progress when verbose mode is active."""
    from rich import print as rprint

    suffix = f" done ({count})" if count else " done"
    rprint(f"[bold cyan][step {step_num}/{total}][/bold cyan] {name}...{suffix}")


def step_ingest(verbose: bool = False) -> bool:
    """Ingest sent emails incrementally for all accounts."""
    return step_ingest_gmail(verbose=verbose)


def step_ingest_gmail(verbose: bool = False) -> bool:
    """Ingest sent emails incrementally for all accounts."""
    success = True
    for account in ACCOUNTS:
        last_at = get_last_ingest_at(account)
        if last_at:
            # Incremental: use last ingestion timestamp
            date_str = last_at[:10].replace("-", "/")
            query = f"in:sent after:{date_str}"
        else:
            # Initial: use default 48h window
            cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
            date_str = cutoff.strftime("%Y/%m/%d")
            query = f"in:sent after:{date_str}"

        ok = _run_step(
            f"Gmail ingestion ({account})",
            [
                sys.executable,
                str(ROOT_DIR / "scripts" / "ingest_gmail_threads.py"),
                "--live",
                "--account",
                account,
                "--query",
                query,
                "--max-threads",
                "100",
            ],
            timeout=300,
        )
        if ok:
            set_last_ingest_at(account, datetime.now(timezone.utc).isoformat())
        else:
            success = False
    return success


def step_analyze_persona(verbose: bool = False, dry_run: bool = False) -> bool:
    """Run persona analysis and merge results into persona.yaml."""
    # Decide whether to run --full or --recent-days
    last_full_path = get_var_dir() / "persona_last_full_analysis.txt"
    use_full = False
    if last_full_path.exists():
        try:
            last_full_str = last_full_path.read_text(encoding="utf-8").strip()
            last_full_dt = datetime.fromisoformat(last_full_str.replace("Z", "+00:00"))
            if last_full_dt.tzinfo is None:
                last_full_dt = last_full_dt.replace(tzinfo=timezone.utc)
            if (datetime.now(timezone.utc) - last_full_dt).days > 7:
                use_full = True
        except (ValueError, TypeError):
            use_full = True
    else:
        use_full = True

    cmd = [sys.executable, str(ROOT_DIR / "scripts" / "analyze_persona.py")]
    if use_full:
        cmd.append("--full")
    else:
        cmd.extend(["--recent-days", "90"])

    ok = _run_step("Persona analysis", cmd)

    # Track last full analysis
    if ok and use_full:
        last_full_path.parent.mkdir(parents=True, exist_ok=True)
        last_full_path.write_text(datetime.now(timezone.utc).isoformat())
    if not ok:
        return False

    # Merge results into persona.yaml
    try:
        from scripts.analyze_persona_merge import merge_persona_analysis

        merge_persona_analysis(
            analysis_path=ROOT_DIR / "configs" / "persona_analysis.json",
            persona_path=ROOT_DIR / "configs" / "persona.yaml",
            log_path=get_var_dir() / "persona_merge.log",
            dry_run=dry_run,
        )
        print("  [OK] Persona merge completed")
    except Exception as exc:
        print(f"  [WARN] Persona merge failed: {exc}")
        return False
    return True


def step_build_sender_profiles(verbose: bool = False) -> bool:
    """Run sender profile builder."""
    return _run_step(
        "Build sender profiles",
        [sys.executable, str(ROOT_DIR / "scripts" / "build_sender_profiles.py")],
    )


def _pipeline_log_path() -> Path:
    """Path to the active instance's pipeline state file."""
    return get_var_dir() / "pipeline_last_run.json"


def _load_last_auto_feedback_at() -> str | None:
    """Load last_auto_feedback_at from the active instance's pipeline log."""
    import json

    log_path = _pipeline_log_path()
    if not log_path.exists():
        return None
    try:
        data = json.loads(log_path.read_text(encoding="utf-8"))
        return data.get("last_auto_feedback_at")
    except Exception:
        return None


def _save_last_auto_feedback_at() -> None:
    """Write last_auto_feedback_at to the active instance's pipeline log."""
    import json

    log_path = _pipeline_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if log_path.exists():
        try:
            data = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    data["last_auto_feedback_at"] = datetime.now(timezone.utc).isoformat()
    log_path.write_text(json.dumps(data, indent=2))


def step_auto_feedback(verbose: bool = False) -> dict:
    """Extract auto-feedback pairs with dynamic lookback window."""
    import math

    from scripts.extract_auto_feedback import extract_auto_feedback

    print(f"\n{'=' * 60}")
    print("STEP: Auto-feedback extraction")
    print(f"{'=' * 60}")

    # Compute lookback days from last run
    last_at = _load_last_auto_feedback_at()
    if last_at:
        try:
            last_dt = datetime.fromisoformat(last_at.replace("Z", "+00:00"))
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            seconds_since = (datetime.now(timezone.utc) - last_dt).total_seconds()
            days_since = max(1, math.ceil(seconds_since / 86400))
        except (ValueError, TypeError):
            days_since = 2
    else:
        days_since = 2

    print(f"  Lookback: {days_since} day(s)")

    try:
        result = extract_auto_feedback(days=days_since)
        _save_last_auto_feedback_at()
        print("  [OK] Auto-feedback completed")
        return result
    except Exception as exc:
        print(f"  [WARN] Auto-feedback failed: {exc}")
        return {"captured": 0, "total": 0, "skipped": 0, "errors": 0}


def step_export_feedback(verbose: bool = False) -> bool:
    """Export feedback JSONL for fine-tuning."""
    return _run_step(
        "Export feedback JSONL",
        [sys.executable, str(ROOT_DIR / "scripts" / "export_feedback_jsonl.py")],
    )


def step_finetune_lora(verbose: bool = False) -> bool:
    """Run LoRA fine-tuning if enough unused pairs exist."""
    return _run_step(
        "LoRA fine-tuning",
        [sys.executable, str(ROOT_DIR / "scripts" / "finetune_lora.py")],
        timeout=3600,
    )


def step_index_embeddings(verbose: bool = False) -> dict:
    """Run incremental embedding indexer."""
    result = _run_step(
        "Embedding indexer",
        [sys.executable, str(ROOT_DIR / "scripts" / "index_embeddings.py"), "--limit", "500"],
        timeout=1800,
    )
    return {"ok": result}


def _load_min_pairs_per_persona() -> int:
    """Threshold below which a persona cohort is too thin to train.

    Read from ``finetune.min_pairs_per_persona`` in the active instance's
    config; defaults to 30 (matches the existing
    ``finetune-milestone`` threshold for the global adapter, so a user
    who knows that number knows this one).
    """
    try:
        from app.core.config import load_config

        raw = load_config() or {}
        val = (raw.get("finetune", {}) if isinstance(raw, dict) else {}).get("min_pairs_per_persona")
        if isinstance(val, int) and val > 0:
            return val
    except Exception:
        pass
    return 30


def _persona_cohorts_above_threshold(db_path: Path, threshold: int) -> dict[str, int]:
    """Return {sender_type: count} for cohorts that have >= threshold pairs.

    "Unknown" is excluded — we don't train a persona adapter for pairs we
    couldn't classify, since the prompt-side persona modes don't have a
    style anchor for it either.
    """
    if not db_path.exists():
        return {}
    counts: dict[str, int] = {}
    conn = sqlite3.connect(db_path)
    try:
        try:
            rows = conn.execute(
                "SELECT sender_type, COUNT(*) FROM feedback_pairs "
                "WHERE sender_type IS NOT NULL AND sender_type != 'unknown' "
                "GROUP BY sender_type HAVING COUNT(*) >= ?",
                (threshold,),
            ).fetchall()
            counts = {row[0]: int(row[1]) for row in rows}
        except sqlite3.OperationalError:
            # Pre-migration DB — column not present. Caller treats empty
            # dict as "no cohorts to train", which is the right answer.
            pass
    finally:
        conn.close()
    return counts


def step_finetune_personas(verbose: bool = False) -> dict:
    """Train per-persona adapters for any cohort above the threshold.

    Phase 2 of per-persona adapters. Skipped silently when no cohort
    qualifies (the common case until the user accumulates enough
    feedback per sender_type). For each qualifying cohort, runs the
    same export → finetune subprocess pipeline as the global, with
    ``--persona <sender_type>`` set so the adapter lands at
    ``<models>/adapters/personas/<sender_type>/`` and the per-row
    used_in_finetune marking is skipped (the global still needs those
    rows).
    """
    print(f"\n{'=' * 60}")
    print("STEP: Per-persona fine-tuning")
    print(f"{'=' * 60}")

    db_path = resolve_sqlite_path(get_settings().database_url)
    threshold = _load_min_pairs_per_persona()
    eligible = _persona_cohorts_above_threshold(db_path, threshold)

    if not eligible:
        msg = f"[finetune-personas] No cohorts above threshold ({threshold} pairs)"
        print(msg)
        return {"ok": True, "skipped": True, "trained": [], "threshold": threshold}

    trained: list[str] = []
    failed: list[str] = []
    for persona, count in sorted(eligible.items()):
        print(f"  Training persona '{persona}' (cohort size: {count})")
        # Export to a per-persona JSONL so the existing finetune script
        # can pick it up unchanged. Each persona gets its own data dir
        # so concurrent training (future) doesn't clobber.
        persona_data_dir = ROOT_DIR / "data" / "feedback" / f"persona-{persona}"
        export_ok = _run_step(
            f"Export feedback (persona={persona})",
            [
                sys.executable,
                str(ROOT_DIR / "scripts" / "export_feedback_jsonl.py"),
                "--persona", persona,
                "--output", str(persona_data_dir / "train.jsonl"),
            ],
        )
        if not export_ok:
            failed.append(persona)
            continue
        finetune_ok = _run_step(
            f"Finetune (persona={persona})",
            [
                sys.executable,
                str(ROOT_DIR / "scripts" / "finetune_lora.py"),
                "--persona", persona,
                "--data-dir", str(persona_data_dir),
            ],
            timeout=3600,
        )
        if finetune_ok:
            trained.append(persona)
        else:
            failed.append(persona)

    ok = not failed
    return {
        "ok": ok,
        "skipped": False,
        "threshold": threshold,
        "trained": trained,
        "failed": failed,
        "eligible_counts": eligible,
    }


def step_snapshot_daily(verbose: bool = False) -> dict:
    """Take a daily snapshot of the active instance's DB, then prune per policy.

    Skipped silently when the DB doesn't exist yet (fresh instance) so a
    pre-first-ingest nightly doesn't litter the snapshots dir with empty
    DB files. Returns a tiny dict so the pipeline log can record what was
    snapshotted and how many older files were retired by the prune step.
    """
    from app.core.data_safety import create_snapshot, prune_snapshots

    print(f"\n{'=' * 60}")
    print("STEP: Daily snapshot")
    print(f"{'=' * 60}")

    # Resolve lazily — DEFAULT_DB was captured at module import, but tests
    # (and any caller that sets YOUOS_DATA_DIR after the module is first
    # imported) need the path to reflect the *current* settings.
    db_path = resolve_sqlite_path(get_settings().database_url)
    if not db_path.exists():
        print("  [SKIP] daily_snapshot — DB not yet created (pre-first-ingest)")
        return {"ok": True, "skipped": True}

    try:
        snap = create_snapshot(db_path, tier="daily")
        removed = prune_snapshots(db_path)
        total_removed = sum(removed.values())
        print(f"  [OK] snapshot={snap}, pruned={removed} (total={total_removed})")
        return {"ok": True, "skipped": False, "snapshot_path": str(snap), "pruned": removed}
    except Exception as exc:
        print(f"  [WARN] daily_snapshot failed: {exc}")
        return {"ok": False, "skipped": False, "error": str(exc)}


def step_deduplicate(verbose: bool = False) -> bool:
    """Run corpus deduplication (best-effort)."""
    return _run_step(
        "Corpus deduplication",
        [sys.executable, str(ROOT_DIR / "scripts" / "deduplicate_corpus.py")],
        timeout=300,
    )


def _check_benchmark_rotation() -> bool:
    """Check if benchmarks need rotation (> 7 days old). Returns True if rotated."""
    import json

    refresh_path = get_var_dir() / "benchmark_last_refresh.txt"
    needs_refresh = False
    if refresh_path.exists():
        try:
            data = json.loads(refresh_path.read_text(encoding="utf-8"))
            last_dt = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            if (datetime.now(timezone.utc) - last_dt).days > 7:
                needs_refresh = True
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            needs_refresh = True
    else:
        needs_refresh = True

    if needs_refresh:
        now = datetime.now(timezone.utc)
        seed = hash(now.isocalendar()[:2])
        ok = _run_step(
            "Benchmark rotation",
            [sys.executable, str(ROOT_DIR / "scripts" / "generate_benchmarks.py"), "--sample-size", "30"],
        )
        if ok:
            refresh_path.parent.mkdir(parents=True, exist_ok=True)
            refresh_path.write_text(json.dumps({"timestamp": now.isoformat(), "seed": seed}))
        return ok
    return True


def _count_feedback_pairs(db_path: Path) -> int:
    """Count total feedback_pairs."""
    if not db_path.exists():
        return 0
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]
    except Exception:
        return 0
    finally:
        conn.close()


def step_golden_eval(verbose: bool = False) -> bool:
    """Run golden evaluation and return True if composite score >= 0.5."""

    # Skip if DB doesn't exist or < 5 feedback pairs
    if not DEFAULT_DB.exists():
        print("  [SKIP] golden_eval — no database")
        return True
    if _count_feedback_pairs(DEFAULT_DB) < 5:
        print("  [SKIP] golden_eval — fewer than 5 feedback pairs")
        return True

    print(f"\n{'=' * 60}")
    print("STEP: Golden evaluation")
    print(f"{'=' * 60}")

    try:
        from scripts.run_golden_eval import run_golden_eval, save_results

        summary = run_golden_eval()
        save_results(summary)

        total = summary.get("total", 0)
        passed = summary.get("passed", 0)
        composite = passed / total if total > 0 else 0.0
        print(f"  Golden eval: {passed}/{total} passed (composite: {composite:.2f})")
        print("  [OK] Golden evaluation completed")
        return composite >= 0.5
    except Exception as exc:
        print(f"  [WARN] Golden evaluation failed: {exc}")
        return False


def step_autoresearch(verbose: bool = False) -> bool:
    """Run autoresearch optimization loop."""
    # Rotate benchmarks if stale
    _check_benchmark_rotation()
    return _run_step(
        "Autoresearch",
        [sys.executable, str(ROOT_DIR / "scripts" / "run_autoresearch.py"), "--max-iter", "80"],
        timeout=7200,
    )


def _count_unused_feedback(db_path: Path) -> int:
    if not db_path.exists():
        return 0
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT COUNT(*) FROM feedback_pairs WHERE used_in_finetune = 0").fetchone()[0]
    except Exception:
        return 0
    finally:
        conn.close()


def _count_new_feedback_since_last_run(db_path: Path) -> int:
    """Count feedback_pairs created since last pipeline run."""
    import json

    if not db_path.exists():
        return 0
    log_path = _pipeline_log_path()
    last_at = None
    if log_path.exists():
        try:
            data = json.loads(log_path.read_text(encoding="utf-8"))
            last_at = data.get("run_at")
        except Exception:
            pass

    conn = sqlite3.connect(db_path)
    try:
        if last_at:
            return conn.execute(
                "SELECT COUNT(*) FROM feedback_pairs WHERE created_at >= ?",
                (last_at,),
            ).fetchone()[0]
        return conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]
    except Exception:
        return 0
    finally:
        conn.close()


def _count_null_embeddings(db_path: Path) -> int:
    """Count rows still needing an embedding across all embeddable tables.

    The nightly indexer embeds both ``chunks`` and ``reply_pairs``, so the
    skip-gate must look at both. Counting ``chunks`` alone meant an instance
    with a fully-embedded (or empty) ``chunks`` table but a backlog of
    unembedded ``reply_pairs`` would skip indexing every night — silently
    leaving semantic re-ranking off for the primary retrieval table while
    reporting "all documents already indexed".

    Per table: a missing table contributes 0 (pre-ingest); a table that
    exists but has not had the ``embedding`` column migrated yet contributes
    its full row count (so the indexer runs, adds the column, and embeds);
    otherwise the count of rows with ``embedding IS NULL``.
    """
    if not db_path.exists():
        return 0
    conn = sqlite3.connect(db_path)
    try:
        existing = {
            row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        }
        total = 0
        for table in ("chunks", "reply_pairs"):
            if table not in existing:
                continue
            cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
            if "embedding" not in cols:
                # Column not migrated yet — every row needs embedding.
                total += conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            else:
                total += conn.execute(f"SELECT COUNT(*) FROM {table} WHERE embedding IS NULL").fetchone()[0]
        return total
    except Exception:
        return -1
    finally:
        conn.close()


def _count_total_pairs(db_path: Path) -> int:
    """Count total reply_pairs."""
    if not db_path.exists():
        return 0
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
    except Exception:
        return 0
    finally:
        conn.close()


def should_skip_finetune(db_path: Path) -> tuple[bool, str]:
    n = _count_new_feedback_since_last_run(db_path)
    if n < 3:
        return True, f"[finetune] Skipping — only {n} new pairs (need >= 3)"
    return False, ""


def should_skip_autoresearch(db_path: Path) -> tuple[bool, str]:
    n = _count_new_feedback_since_last_run(db_path)
    if n < 5:
        return True, f"[autoresearch] Skipping — only {n} new pairs (need >= 5)"
    return False, ""


def should_skip_embeddings(db_path: Path) -> tuple[bool, str]:
    n = _count_null_embeddings(db_path)
    if n == 0:
        return True, "[embeddings] Skipping — all chunks and reply_pairs already indexed"
    return False, ""


def should_skip_dedup(db_path: Path) -> tuple[bool, str]:
    n = _count_total_pairs(db_path)
    if n < 10:
        return True, f"[dedup] Skipping — corpus too small ({n} pairs)"
    return False, ""


def _write_pipeline_log(run_log: dict) -> None:
    """Write pipeline run log to the active instance's pipeline_last_run.json."""
    import json

    log_path = _pipeline_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(run_log, indent=2))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--autoresearch-only", action="store_true", help="Skip ingestion/finetune, run autoresearch only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print Rich progress for each step")
    args = parser.parse_args()
    verbose = args.verbose

    if args.autoresearch_only:
        print("YouOS Autoresearch (on-demand trigger)")
        step_autoresearch(verbose=verbose)
        return

    start = datetime.now(timezone.utc)
    print(f"YouOS Nightly Pipeline — {start.isoformat()}")
    print(f"{'=' * 60}")

    results: dict[str, str] = {}
    steps: dict[str, bool] = {}
    errors: list[str] = []
    skipped_steps: list[str] = []
    # Wall-clock per step (monotonic, seconds). Without this, a 4-hour nightly
    # tells you nothing about *where* the time went — every step blob just
    # reports OK/WARN. Recorded for the success path, error path, AND the
    # skipped path so a "skipped: xxx" entry is observably ~0s.
    step_durations: dict[str, float] = {}

    def _record_duration(name: str, t0: float) -> None:
        step_durations[name] = round(time.monotonic() - t0, 3)

    # -1. Daily snapshot — first, so the snapshot reflects pre-pipeline state.
    # If the nightly later corrupts something (a bad fine-tune, a bad migration),
    # the user can restore from this morning's snapshot without losing their
    # corpus. Skipped silently on fresh instances (DB doesn't exist yet).
    _t = time.monotonic()
    try:
        snap_result = step_snapshot_daily(verbose=verbose)
        if snap_result.get("skipped"):
            results["daily_snapshot"] = "skipped (pre-first-ingest)"
            steps["daily_snapshot"] = True
            skipped_steps.append("daily_snapshot")
        else:
            ok = snap_result["ok"]
            results["daily_snapshot"] = "OK" if ok else "WARN"
            steps["daily_snapshot"] = ok
            if not ok:
                errors.append(f"Daily snapshot failed: {snap_result.get('error', 'unknown')}")
    except Exception as exc:
        results["daily_snapshot"] = f"error: {exc}"
        steps["daily_snapshot"] = False
        errors.append(f"Daily snapshot error: {exc}")
    _record_duration("daily_snapshot", _t)

    # 0. Corpus deduplication (best-effort, before ingestion) — with skip gate
    _t = time.monotonic()
    skip, skip_msg = should_skip_dedup(DEFAULT_DB)
    if skip:
        print(skip_msg)
        results["dedup"] = f"skipped: {skip_msg}"
        steps["dedup"] = True
        skipped_steps.append("dedup")
    else:
        try:
            ok = step_deduplicate(verbose=verbose)
            results["dedup"] = "OK" if ok else "WARN"
            steps["dedup"] = ok
            if not ok:
                errors.append("Corpus deduplication failed")
        except Exception as exc:
            results["dedup"] = f"error: {exc}"
            steps["dedup"] = False
            errors.append(f"Corpus deduplication error: {exc}")
    _record_duration("dedup", _t)

    # 1. Gmail ingestion
    _t = time.monotonic()
    try:
        ok = step_ingest_gmail(verbose=verbose)
        results["ingestion"] = "OK" if ok else "WARN"
        steps["ingestion"] = ok
        if not ok:
            errors.append("Gmail ingestion failed")
    except Exception as exc:
        results["ingestion"] = f"error: {exc}"
        steps["ingestion"] = False
        errors.append(f"Gmail ingestion error: {exc}")
    _record_duration("ingestion", _t)

    # 1b. Benchmark auto-refresh
    _t = time.monotonic()
    try:
        from app.core.config import _load_raw_config

        cfg = _load_raw_config()
        last_count = cfg.get("benchmarks", {}).get("last_refresh_count", 0)
        if DEFAULT_DB.exists():
            conn = sqlite3.connect(DEFAULT_DB)
            current_count = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
            conn.close()
            if last_count == 0 or current_count > last_count * 1.1:
                ok = _run_step(
                    "Benchmark refresh",
                    [sys.executable, str(ROOT_DIR / "scripts" / "generate_benchmarks.py")],
                )
                results["benchmark_refresh"] = "OK" if ok else "WARN"
                steps["benchmark_refresh"] = ok
                if not ok:
                    errors.append("Benchmark refresh failed")
            else:
                results["benchmark_refresh"] = "skipped (not enough new data)"
                steps["benchmark_refresh"] = True
    except Exception as exc:
        results["benchmark_refresh"] = f"error: {exc}"
        steps["benchmark_refresh"] = False
        errors.append(f"Benchmark refresh error: {exc}")
    _record_duration("benchmark_refresh", _t)

    # 2. Auto-feedback extraction
    _t = time.monotonic()
    try:
        feedback = step_auto_feedback(verbose=verbose)
        results["auto_feedback"] = f"captured {feedback['captured']} pairs"
        steps["auto_feedback"] = True
    except Exception as exc:
        feedback = {"captured": 0, "total": 0, "skipped": 0, "errors": 0}
        results["auto_feedback"] = f"error: {exc}"
        steps["auto_feedback"] = False
        errors.append(f"Auto-feedback error: {exc}")
    _record_duration("auto_feedback", _t)

    # 3. Export + fine-tune (only if enough data)
    unused = _count_unused_feedback(DEFAULT_DB)

    _t = time.monotonic()
    if feedback["captured"] >= 5:
        try:
            ok = step_export_feedback(verbose=verbose)
            results["export"] = "OK" if ok else "WARN"
            steps["export"] = ok
            if not ok:
                errors.append("Feedback export failed")
        except Exception as exc:
            results["export"] = f"error: {exc}"
            steps["export"] = False
            errors.append(f"Feedback export error: {exc}")
    else:
        results["export"] = f"skipped (only {feedback['captured']} new pairs, need 5)"
        steps["export"] = True
    _record_duration("export", _t)

    _t = time.monotonic()
    skip_ft, skip_ft_msg = should_skip_finetune(DEFAULT_DB)
    if skip_ft:
        print(skip_ft_msg)
        results["finetune"] = f"skipped: {skip_ft_msg}"
        steps["finetune"] = True
        skipped_steps.append("finetune")
    elif unused >= 10:
        try:
            ok = step_finetune_lora(verbose=verbose)
            results["finetune"] = "OK" if ok else "WARN"
            steps["finetune"] = ok
            if not ok:
                errors.append("LoRA fine-tuning failed")
        except Exception as exc:
            results["finetune"] = f"error: {exc}"
            steps["finetune"] = False
            errors.append(f"LoRA fine-tuning error: {exc}")
    else:
        results["finetune"] = f"skipped (only {unused} unused pairs, need 10)"
        steps["finetune"] = True
    _record_duration("finetune", _t)

    # 3a-bis. Per-persona fine-tuning (Phase 2). Skipped silently when no
    # cohort exceeds `finetune.min_pairs_per_persona` (default 30). Runs
    # after the global so that any persona's adapter is at least as fresh
    # as the global it falls back to in Phase-3 routed generation.
    _t = time.monotonic()
    try:
        persona_result = step_finetune_personas(verbose=verbose)
        if persona_result.get("skipped"):
            results["finetune_personas"] = (
                f"skipped (no cohort >= {persona_result['threshold']} pairs)"
            )
            steps["finetune_personas"] = True
            skipped_steps.append("finetune_personas")
        else:
            trained = persona_result.get("trained", [])
            failed = persona_result.get("failed", [])
            if persona_result.get("ok"):
                results["finetune_personas"] = f"trained {len(trained)}: {trained}"
                steps["finetune_personas"] = True
            else:
                results["finetune_personas"] = (
                    f"trained {len(trained)}, failed {len(failed)}: {failed}"
                )
                steps["finetune_personas"] = False
                errors.append(f"Persona fine-tune failed for: {failed}")
    except Exception as exc:
        results["finetune_personas"] = f"error: {exc}"
        steps["finetune_personas"] = False
        errors.append(f"Per-persona fine-tune error: {exc}")
    _record_duration("finetune_personas", _t)

    # 3b. Golden evaluation (after fine-tuning, before autoresearch)
    _t = time.monotonic()
    golden_composite = None
    try:
        ok = step_golden_eval(verbose=verbose)
        results["golden_eval"] = "OK" if ok else "WARN"
        steps["golden_eval"] = ok
        # Read composite score from results file
        golden_results_path = get_var_dir() / "golden_results.json"
        if golden_results_path.exists():
            import json as _json2

            golden_data = _json2.loads(golden_results_path.read_text(encoding="utf-8"))
            total_g = golden_data.get("total", 0)
            passed_g = golden_data.get("passed", 0)
            golden_composite = round(passed_g / total_g, 4) if total_g > 0 else 0.0
    except Exception as exc:
        results["golden_eval"] = f"error: {exc}"
        steps["golden_eval"] = False
        errors.append(f"Golden evaluation error: {exc}")
    _record_duration("golden_eval", _t)

    # 4. Embedding indexer (after fine-tuning) — with skip gate
    _t = time.monotonic()
    skip_emb, skip_emb_msg = should_skip_embeddings(DEFAULT_DB)
    if skip_emb:
        print(skip_emb_msg)
        results["embeddings"] = f"skipped: {skip_emb_msg}"
        steps["embeddings"] = True
        skipped_steps.append("embeddings")
    else:
        try:
            embed_result = step_index_embeddings(verbose=verbose)
            ok = embed_result["ok"]
            results["embeddings"] = "OK" if ok else "WARN"
            steps["embeddings"] = ok
            if not ok:
                errors.append("Embedding indexer failed")
        except Exception as exc:
            results["embeddings"] = f"error: {exc}"
            steps["embeddings"] = False
            errors.append(f"Embedding indexer error: {exc}")
    _record_duration("embeddings", _t)

    # 5. Autoresearch — with skip gate
    _t = time.monotonic()
    skip_ar, skip_ar_msg = should_skip_autoresearch(DEFAULT_DB)
    if skip_ar:
        print(skip_ar_msg)
        results["autoresearch"] = f"skipped: {skip_ar_msg}"
        steps["autoresearch"] = True
        skipped_steps.append("autoresearch")
    else:
        try:
            ok = step_autoresearch(verbose=verbose)
            results["autoresearch"] = "OK" if ok else "WARN"
            steps["autoresearch"] = ok
            if not ok:
                errors.append("Autoresearch failed")
        except Exception as exc:
            results["autoresearch"] = f"error: {exc}"
            steps["autoresearch"] = False
            errors.append(f"Autoresearch error: {exc}")
    _record_duration("autoresearch", _t)

    # Include recent git log after autoresearch
    try:
        git_log = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=ROOT_DIR,
        )
        if git_log.returncode == 0 and git_log.stdout.strip():
            results["recent_commits"] = git_log.stdout.strip()
    except Exception:
        pass

    # Determine overall status
    all_ok = all(steps.values())
    any_ok = any(steps.values())
    if all_ok:
        status = "ok"
    elif any_ok:
        status = "partial"
    else:
        status = "failed"

    # Write pipeline log
    # Check if benchmarks were rotated this run
    import json as _json

    benchmark_rotated = False
    refresh_path = get_var_dir() / "benchmark_last_refresh.txt"
    if refresh_path.exists():
        try:
            rd = _json.loads(refresh_path.read_text(encoding="utf-8"))
            ref_dt = datetime.fromisoformat(rd["timestamp"].replace("Z", "+00:00"))
            if ref_dt.tzinfo is None:
                ref_dt = ref_dt.replace(tzinfo=timezone.utc)
            benchmark_rotated = (start - ref_dt).total_seconds() < 3600
        except Exception:
            pass

    elapsed = (datetime.now(timezone.utc) - start).total_seconds()

    # Per-table embedding coverage so the dashboard / a debugging session
    # can answer "is semantic retrieval actually firing on this corpus?"
    # without ad-hoc SQL. Cheap (two COUNT queries) and tolerant of fresh
    # corpora (returns {} when tables aren't present yet).
    try:
        from app.core.stats import get_embedding_coverage

        embedding_coverage = get_embedding_coverage(get_settings().database_url)
    except Exception:
        embedding_coverage = {}

    # Draft-quality-by-condition from the draft_events signal log: which
    # intents/cohorts produce drafts that miss the target length or draw
    # low-confidence retrieval, plus a best-effort edit-distance-by-condition
    # correlation. Surfaces *where* drafting is weak for the self-improvement
    # loop (and a future autoresearch objective). Read-only; tolerant of an
    # absent/empty table (returns a zeroed summary).
    try:
        from app.core.stats import summarize_draft_events

        draft_events_summary = summarize_draft_events(get_settings().database_url)
    except Exception:
        draft_events_summary = {}

    # `schema_version` lets downstream consumers (stats UI, autoresearch
    # convergence dashboard, future history-jsonl trend view) detect a
    # breaking shape change instead of silently mis-parsing a new field.
    # Bump when adding a required field or changing an existing one's
    # semantics; additive optional fields don't need a bump.
    run_log = {
        "schema_version": "v1",
        "run_at": start.isoformat(),
        "duration_seconds": round(elapsed, 2),
        "status": status,
        "steps": steps,
        "step_durations": step_durations,
        "errors": errors,
        "skipped_steps": skipped_steps,
        "benchmark_rotated": benchmark_rotated,
        "golden_composite": golden_composite,
        "embedding_coverage": embedding_coverage,
        "draft_events_summary": draft_events_summary,
    }
    _write_pipeline_log(run_log)

    # Summary
    print(f"\n{'=' * 60}")
    print("NIGHTLY PIPELINE SUMMARY")
    print(f"{'=' * 60}")
    for step, step_status in results.items():
        duration = step_durations.get(step)
        # Skip the duration column for non-step entries like recent_commits.
        if duration is not None:
            print(f"  {step}: {step_status} ({duration:.1f}s)")
        else:
            print(f"  {step}: {step_status}")
    print(f"\nStatus: {status}")
    print(f"Completed in {elapsed:.0f}s")


if __name__ == "__main__":
    main()
