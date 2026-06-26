"""Unified stats query layer for YouOS."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]


def _get_var_path(filename: str) -> Path:
    from app.core.settings import get_var_dir

    return get_var_dir() / filename


def _resolve_adapter_path() -> Path:
    from app.core.settings import get_adapter_path

    return get_adapter_path()


ADAPTER_PATH = _resolve_adapter_path()
AUTORESEARCH_JSONL = _get_var_path("autoresearch_runs.jsonl")
AUTORESEARCH_LOG = _get_var_path("autoresearch_log.md")


def _safe_count(conn: sqlite3.Connection, table: str) -> int:
    try:
        return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]  # noqa: S608
    except sqlite3.OperationalError:
        return 0


def _group_counts(conn: sqlite3.Connection, column: str, *, default: str) -> dict[str, int]:
    """COUNT(*) grouped by a draft_events column (NULLs folded to *default*)."""
    try:
        rows = conn.execute(
            f"SELECT COALESCE({column}, ?) AS k, COUNT(*) AS n FROM draft_events GROUP BY k ORDER BY n DESC",  # noqa: S608
            (default,),
        ).fetchall()
        return {str(r["k"]): int(r["n"]) for r in rows}
    except sqlite3.OperationalError:
        return {}


def summarize_draft_events(database_url: str) -> dict:
    """Aggregate the ``draft_events`` signal log into a draft-quality picture.

    Every generated draft is logged with the *conditions* it was produced
    under (intent, sender_type, confidence, length_flag). This summarizes them
    so the loop can see *where* drafting is weak — e.g. an intent whose drafts
    are frequently off the target length, or a cohort that draws mostly
    low-confidence retrieval. Where a draft can be matched to an edit outcome
    (a best-effort join to ``draft_history`` on inbound+draft text), it also
    reports the average edit distance by condition. The model's own drafts are
    never training targets; this is analysis/observability for the loop.
    """
    from app.db.bootstrap import resolve_sqlite_path

    empty = {
        "total": 0,
        "by_intent": {},
        "by_sender_type": {},
        "by_confidence": {},
        "by_length_flag": {},
        "by_model": {},
        "off_target_pct": None,
        "outcome": {"matched": 0, "avg_edit_distance_by_sender_type": {}, "avg_edit_distance_by_confidence": {}},
    }

    db_path = resolve_sqlite_path(database_url)
    if not db_path.exists():
        return empty

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        total = _safe_count(conn, "draft_events")
        if total == 0:
            return empty

        summary = {
            "total": total,
            "by_intent": _group_counts(conn, "intent", default="unknown"),
            "by_sender_type": _group_counts(conn, "sender_type", default="unknown"),
            "by_confidence": _group_counts(conn, "confidence", default="unknown"),
            "by_length_flag": _group_counts(conn, "length_flag", default="none"),
            # Which model actually produced each draft — the source of truth for
            # whether the LoRA adapter is really in use vs. a silent base/cloud
            # fallback. See get_drafting_model_status().
            "by_model": _group_counts(conn, "model_used", default="unknown"),
            "off_target_pct": None,
            "outcome": {"matched": 0, "avg_edit_distance_by_sender_type": {}, "avg_edit_distance_by_confidence": {}},
        }

        # Fraction of length-annotated drafts that missed the target band.
        try:
            off, flagged = conn.execute(
                """SELECT
                       SUM(CASE WHEN length_flag IN ('long', 'short') THEN 1 ELSE 0 END),
                       SUM(CASE WHEN length_flag IS NOT NULL THEN 1 ELSE 0 END)
                   FROM draft_events"""
            ).fetchone()
            if flagged:
                summary["off_target_pct"] = round(100.0 * (off or 0) / flagged, 1)
        except sqlite3.OperationalError:
            pass

        # Best-effort outcome correlation: join to draft_history on the only
        # available linkage (inbound + draft text). Not unique — same draft can
        # recur — so this is indicative, not exact; `matched` reports coverage.
        for key, col in (("avg_edit_distance_by_sender_type", "sender_type"), ("avg_edit_distance_by_confidence", "confidence")):
            try:
                rows = conn.execute(
                    f"""SELECT COALESCE(de.{col}, 'unknown') AS k,
                               ROUND(AVG(dh.edit_distance_pct), 3) AS avg_ed,
                               COUNT(*) AS n
                        FROM draft_events de
                        JOIN draft_history dh
                          ON de.inbound_text = dh.inbound_text
                         AND de.generated_draft = dh.generated_draft
                        WHERE dh.edit_distance_pct IS NOT NULL
                        GROUP BY k""",  # noqa: S608
                ).fetchall()
                summary["outcome"][key] = {str(r["k"]): {"avg_edit_distance": r["avg_ed"], "n": int(r["n"])} for r in rows}
            except sqlite3.OperationalError:
                pass

        try:
            matched = conn.execute(
                """SELECT COUNT(*) FROM draft_events de
                   JOIN draft_history dh
                     ON de.inbound_text = dh.inbound_text AND de.generated_draft = dh.generated_draft
                   WHERE dh.edit_distance_pct IS NOT NULL"""
            ).fetchone()[0]
            summary["outcome"]["matched"] = int(matched)
        except sqlite3.OperationalError:
            pass

        return summary
    finally:
        conn.close()


def get_latest_ingest_status(database_url: str) -> dict:
    """Latest ingestion run's status, for the wizard's live progress poll.

    Maps the run-log's ``started`` to ``running``; returns ``idle`` when there's
    no run (or no table yet).
    """
    from app.db.bootstrap import resolve_sqlite_path

    db_path = resolve_sqlite_path(database_url)
    if not db_path.exists():
        return {"status": "idle"}
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            """SELECT status, started_at, completed_at, discovered_count, fetched_count,
                      stored_reply_pair_count, error_summary
               FROM ingest_runs ORDER BY id DESC LIMIT 1"""
        ).fetchone()
    except sqlite3.OperationalError:
        return {"status": "idle"}
    finally:
        conn.close()
    if not row:
        return {"status": "idle"}
    return {
        "status": "running" if row["status"] == "started" else row["status"],
        "started_at": row["started_at"],
        "completed_at": row["completed_at"],
        "discovered": row["discovered_count"],
        "fetched": row["fetched_count"],
        "reply_pairs": row["stored_reply_pair_count"],
        "error": row["error_summary"],
    }


def get_corpus_stats(database_url: str) -> dict:
    """Get corpus health statistics."""
    from app.db.bootstrap import resolve_sqlite_path

    db_path = resolve_sqlite_path(database_url)
    if not db_path.exists():
        return {
            "total_documents": 0,
            "total_reply_pairs": 0,
            "total_feedback_pairs": 0,
            "reviewed_today": 0,
            "reviewed_this_week": 0,
            "avg_edit_distance": None,
            "embedding_pct": None,
            "outcome_metrics": {
                "accept_unchanged_pct": None,
                "low_edit_pct": None,
                "high_rating_pct": None,
                "median_edit_distance": None,
            },
        }

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        total_docs = _safe_count(conn, "documents")
        total_pairs = _safe_count(conn, "reply_pairs")
        total_feedback = _safe_count(conn, "feedback_pairs")

        reviewed_today = 0
        reviewed_week = 0
        avg_edit_dist = None
        try:
            reviewed_today = conn.execute("SELECT COUNT(*) FROM feedback_pairs WHERE DATE(created_at) = DATE('now')").fetchone()[0]
            reviewed_week = conn.execute("SELECT COUNT(*) FROM feedback_pairs WHERE created_at >= DATE('now', '-7 days')").fetchone()[0]
            row = conn.execute(
                "SELECT AVG(edit_distance_pct) FROM "
                "(SELECT edit_distance_pct FROM feedback_pairs "
                "WHERE edit_distance_pct IS NOT NULL ORDER BY id DESC LIMIT 50)"
            ).fetchone()
            if row and row[0] is not None:
                avg_edit_dist = round(row[0], 4)
        except sqlite3.OperationalError:
            pass

        embedding_pct = None
        try:
            if total_pairs > 0:
                with_emb = conn.execute("SELECT COUNT(*) FROM reply_pairs WHERE embedding IS NOT NULL").fetchone()[0]
                embedding_pct = round((with_emb / total_pairs) * 100, 1)
        except sqlite3.OperationalError:
            pass

        # Outcome metrics (proxy for real-world draft quality)
        outcome_metrics = {
            "accept_unchanged_pct": None,
            "low_edit_pct": None,
            "high_rating_pct": None,
            "median_edit_distance": None,
        }
        try:
            row = conn.execute(
                """
                SELECT
                    ROUND(100.0 * AVG(CASE WHEN edit_distance_pct <= 0.01 THEN 1.0 ELSE 0.0 END), 1) AS accept_unchanged_pct,
                    ROUND(100.0 * AVG(CASE WHEN edit_distance_pct <= 0.15 THEN 1.0 ELSE 0.0 END), 1) AS low_edit_pct,
                    ROUND(100.0 * AVG(CASE WHEN rating >= 4 THEN 1.0 ELSE 0.0 END), 1) AS high_rating_pct
                FROM feedback_pairs
                WHERE edit_distance_pct IS NOT NULL
                """
            ).fetchone()
            if row:
                outcome_metrics["accept_unchanged_pct"] = row[0]
                outcome_metrics["low_edit_pct"] = row[1]
                outcome_metrics["high_rating_pct"] = row[2]

            # Median edit distance from last 100 feedback rows
            med_row = conn.execute(
                """
                SELECT edit_distance_pct
                FROM feedback_pairs
                WHERE edit_distance_pct IS NOT NULL
                ORDER BY id DESC
                LIMIT 100
                """
            ).fetchall()
            if med_row:
                vals = sorted(float(r[0]) for r in med_row)
                n = len(vals)
                if n % 2 == 1:
                    median_val = vals[n // 2]
                else:
                    median_val = (vals[(n // 2) - 1] + vals[n // 2]) / 2
                outcome_metrics["median_edit_distance"] = round(median_val, 4)
        except sqlite3.OperationalError:
            pass

        return {
            "total_documents": total_docs,
            "total_reply_pairs": total_pairs,
            "total_feedback_pairs": total_feedback,
            "reviewed_today": reviewed_today,
            "reviewed_this_week": reviewed_week,
            "avg_edit_distance": avg_edit_dist,
            "embedding_pct": embedding_pct,
            "outcome_metrics": outcome_metrics,
        }
    finally:
        conn.close()


def get_model_status(configs_dir: Path) -> dict:
    """Get model and adapter status."""
    adapter_exists = (ADAPTER_PATH / "adapters.safetensors").exists()
    lora_trained_at = None
    if adapter_exists:
        try:
            from datetime import datetime, timezone

            mtime = os.path.getmtime(ADAPTER_PATH / "adapters.safetensors")
            lora_trained_at = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
        except Exception:
            pass

    # Capability-aware (not just "does the adapter file exist"): without mlx_lm
    # the local model can't run at all, so drafting falls to the cloud — claiming
    # "lora" there is the false-confidence we're trying to avoid.
    import shutil

    local_available = shutil.which("mlx_lm") is not None
    if not local_available:
        gen_model = "claude"
    elif adapter_exists:
        gen_model = "qwen2.5-1.5b-lora"
    else:
        gen_model = "qwen2.5-1.5b-base"

    # Benchmark trend
    benchmark_trend: list[dict] = []
    if AUTORESEARCH_JSONL.exists():
        try:
            lines = AUTORESEARCH_JSONL.read_text(encoding="utf-8").strip().splitlines()
            for line in lines[-5:]:
                entry = json.loads(line)
                benchmark_trend.append(
                    {
                        "date": entry.get("run_at", ""),
                        "composite_score": entry.get("composite_score"),
                        "improvements_kept": entry.get("config_snapshot", {}).get("improvements_kept"),
                    }
                )
        except Exception:
            benchmark_trend = []
    if not benchmark_trend and AUTORESEARCH_LOG.exists():
        try:
            import re

            log_text = AUTORESEARCH_LOG.read_text(encoding="utf-8")
            entries = re.findall(r"## Run (\d{4}-\d{2}-\d{2}[^\n]*)\n(.*?)(?=\n## Run |\Z)", log_text, re.DOTALL)
            for date_str, body in entries[-5:]:
                score_match = re.search(r"composite[_\s]?score[:\s]*([\d.]+)", body, re.IGNORECASE)
                kept_match = re.search(r"improvements?\s*kept[:\s]*(\d+)", body, re.IGNORECASE)
                benchmark_trend.append(
                    {
                        "date": date_str.strip(),
                        "composite_score": score_match.group(1) if score_match else None,
                        "improvements_kept": int(kept_match.group(1)) if kept_match else None,
                    }
                )
        except Exception:
            pass

    return {
        "generation_model": gen_model,
        "local_available": local_available,
        "lora_adapter_exists": adapter_exists,
        "lora_trained_at": lora_trained_at,
        "last_finetune_run": lora_trained_at,
        "benchmark_trend": benchmark_trend,
    }


def _recent_model_counts(conn: sqlite3.Connection, limit: int = 50) -> dict[str, int]:
    """``{model_used: count}`` over the most recent *limit* drafts.

    Recent-only because an adapter trained today shouldn't be judged by drafts
    produced weeks ago on the base model.
    """
    try:
        rows = conn.execute(
            "SELECT COALESCE(model_used, 'unknown') AS k, COUNT(*) AS n FROM "
            "(SELECT model_used FROM draft_events ORDER BY id DESC LIMIT ?) GROUP BY k",
            (limit,),
        ).fetchall()
        return {str(r["k"]): int(r["n"]) for r in rows}
    except sqlite3.OperationalError:
        return {}


def _classify_model_used(model_used: str) -> str:
    """Bucket a raw ``model_used`` label into lora | base | cloud | other."""
    m = (model_used or "").lower()
    if "lora" in m:  # qwen2.5-1.5b-lora and per-persona qwen2.5-1.5b-lora-<type>
        return "lora"
    if m.endswith("-base"):
        return "base"
    if m == "claude" or m.startswith("ollama"):
        return "cloud"
    return "other"


def _classify_drafting(by_model: dict[str, int], adapter_trained: bool, local_available: bool) -> tuple[str, str, str, bool]:
    """Decide what's *actually* drafting → (state, label, detail, healthy).

    Prefers reality (what recent drafts used); falls back to capability (adapter
    on disk + mlx_lm) when there are no drafts yet. ``healthy`` is False whenever
    the LoRA isn't the thing drafting — that's the signal a surface should warn on.
    """
    totals = {"lora": 0, "base": 0, "cloud": 0, "other": 0}
    for model, n in by_model.items():
        totals[_classify_model_used(model)] += n
    n = sum(totals.values())

    if n:
        lora, base, cloud = totals["lora"], totals["base"], totals["cloud"]
        if lora and not base and not cloud:
            return ("personalized", "Your fine-tuned model (LoRA)",
                    f"All of the last {n} drafts used your trained LoRA adapter.", True)
        if lora and (base or cloud):
            return ("mixed", "Mostly your LoRA — some fell back",
                    f"{base} base-model and {cloud} cloud-fallback draft(s) in the last {n}. "
                    "Check that mlx_lm is installed and the adapter is trained.", False)
        if base and not lora:
            return ("base", "Base model — your LoRA is NOT in use",
                    "Recent drafts ran on the base model. Train an adapter with `youos finetune` "
                    "(or via the wizard) so drafts sound like you.", False)
        if cloud and not lora:
            return ("cloud", "Cloud fallback — not your local LoRA",
                    "Recent drafts used the cloud/Ollama fallback, not your local model. "
                    "Is mlx_lm installed and an adapter trained?", False)
        return ("unknown", "Unknown", f"The last {n} drafts have no recognizable model label.", False)

    # No drafts yet — infer from capability.
    if not local_available:
        return ("cloud", "Cloud fallback (local model unavailable)",
                'mlx_lm is not installed, so the local model can\'t run — drafts will use the cloud '
                'fallback. Install it: pip install -e ".[mlx]".', False)
    if adapter_trained:
        return ("personalized", "Your fine-tuned model (LoRA) — ready",
                "Adapter trained and the local model is available; drafts will use your LoRA. No drafts yet.", True)
    return ("base", "Base model — no LoRA trained yet",
            "No adapter trained yet — drafts will use the base model (not personalized) until you fine-tune.", False)


_READINESS_MESSAGES = {
    "not_started": "Your voice model hasn't been trained yet — drafts use the base model and won't sound like you. "
                   "Start fine-tuning from the setup wizard or Settings.",
    "training": "Training your voice model on your sent mail… drafts use the base model until it's ready.",
    "benchmarking": "Benchmarking your newly trained voice model… almost there.",
    "benchmark_pending": "Your voice model is trained but not yet benchmarked — it'll be validated by tonight's run "
                         "(or run `youos eval --golden`). Drafts may not reflect the validated model yet.",
    "ready": "Your voice model is trained and benchmarked — drafts now sound like you.",
}


def get_model_readiness(database_url: str, *, finetune_running: bool = False) -> dict:
    """Is the personalized model ready to rely on — i.e. trained AND benchmarked?

    Used to ask a user to wait before drafting on a half-baked model. Phases:
    ``not_started`` → ``training`` → ``benchmarking`` → ``benchmark_pending`` →
    ``ready``. "Benchmarked" means a golden eval ran at or after the adapter was
    trained (the wizard's fine-tune now chains the eval, so this is reachable
    without waiting for the nightly). ``finetune_running`` is supplied by the
    route layer since the in-progress handle lives there.
    """
    adapter_file = _resolve_adapter_path() / "adapters.safetensors"
    adapter_trained = adapter_file.exists()

    benchmarked = False
    if adapter_trained:
        golden = _get_var_path("golden_results.json")
        try:
            benchmarked = golden.exists() and golden.stat().st_mtime >= adapter_file.stat().st_mtime
        except OSError:
            benchmarked = False

    if finetune_running:
        phase = "benchmarking" if adapter_trained else "training"
    elif not adapter_trained:
        phase = "not_started"
    elif not benchmarked:
        phase = "benchmark_pending"
    else:
        phase = "ready"

    return {
        "phase": phase,
        "ready": phase == "ready",
        "message": _READINESS_MESSAGES[phase],
        "adapter_trained": adapter_trained,
        "benchmarked": benchmarked,
        "running": finetune_running,
    }


def get_drafting_model_status(database_url: str) -> dict:
    """What model is *actually* drafting — to prevent the silent-failure where a
    user believes drafts are personalized while they run on the base model or
    fall back to the cloud.

    Reality first (recent ``draft_events.model_used``), capability as the fallback
    (adapter on disk + ``mlx_lm`` available).
    """
    import shutil

    from app.db.bootstrap import resolve_sqlite_path

    adapter_trained = (_resolve_adapter_path() / "adapters.safetensors").exists()
    local_available = shutil.which("mlx_lm") is not None

    by_model: dict[str, int] = {}
    db_path = resolve_sqlite_path(database_url)
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            by_model = _recent_model_counts(conn)
        finally:
            conn.close()

    state, label, detail, healthy = _classify_drafting(by_model, adapter_trained, local_available)
    return {
        "state": state,
        "label": label,
        "detail": detail,
        "healthy": healthy,
        "adapter_trained": adapter_trained,
        "local_available": local_available,
        "recent_by_model": by_model,
    }


def get_pipeline_status(project_root: Path) -> dict | None:
    """Read var/pipeline_last_run.json if it exists."""
    log_path = project_root / "var" / "pipeline_last_run.json"
    if not log_path.exists():
        return None
    try:
        return json.loads(log_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def get_persona_adapter_status() -> dict[str, dict]:
    """Return ``{persona: {trained: bool, mtime: iso|None, pairs_used: int|None}}``.

    One entry per sender_type cohort (internal / external_client / personal /
    automated) — "unknown" excluded since Phase 2 doesn't train an adapter
    for it. Used by the stats endpoint and the doctor check so the user
    can see which personas have a trained adapter without poking the
    filesystem.

    ``mtime`` and ``pairs_used`` come from the adapter's `meta.json`
    (written by `scripts/finetune_lora.py`) when present; otherwise mtime
    falls back to the safetensors file's mtime and pairs_used is None.
    """
    from app.core.settings import get_persona_adapter_path

    out: dict[str, dict] = {}
    for persona in ("internal", "external_client", "personal", "automated"):
        adapter_dir = get_persona_adapter_path(persona)
        sfile = adapter_dir / "adapters.safetensors"
        meta_path = adapter_dir / "meta.json"
        entry: dict = {"trained": sfile.exists(), "mtime": None, "pairs_used": None}
        if not sfile.exists():
            out[persona] = entry
            continue
        # Prefer the train metadata json; fall back to fs mtime.
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                entry["mtime"] = meta.get("trained_at")
                entry["pairs_used"] = meta.get("pairs_used")
            except Exception:
                pass
        if entry["mtime"] is None:
            try:
                from datetime import datetime, timezone

                entry["mtime"] = datetime.fromtimestamp(
                    sfile.stat().st_mtime, tz=timezone.utc
                ).isoformat()
            except Exception:
                pass
        out[persona] = entry
    return out


def get_embedding_coverage(database_url: str) -> dict[str, float]:
    """Fraction of rows with non-empty embeddings, per indexed table.

    Returns ``{"chunks": 0.42, "reply_pairs": 0.31}`` when both tables exist
    and have rows. Missing / empty tables are silently omitted — so a fresh
    instance returns ``{}`` rather than zeros that would imply "indexed,
    but every row failed".

    Used to answer "is semantic retrieval actually firing on this corpus?"
    from the stats endpoint and the nightly pipeline log — without this,
    the only way to tell was to add ad-hoc logging inside the retrieval
    reranker. Mirrors ``app.retrieval.service._embedding_coverage`` which
    is per-table and connection-scoped; this is the public, multi-table,
    db-path-scoped version intended for stats callers.
    """
    from app.db.bootstrap import resolve_sqlite_path

    db_path = resolve_sqlite_path(database_url)
    if not db_path.exists():
        return {}

    coverage: dict[str, float] = {}
    conn = sqlite3.connect(db_path)
    try:
        existing_tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        for table in ("chunks", "reply_pairs"):
            if table not in existing_tables:
                continue
            cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
            if "embedding" not in cols:
                continue
            total = _safe_count(conn, table)
            if total == 0:
                continue
            row = conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE embedding IS NOT NULL AND LENGTH(embedding) > 0"  # noqa: S608
            ).fetchone()
            embedded = row[0] if row else 0
            coverage[table] = round(embedded / total, 4)
    except sqlite3.OperationalError:
        return coverage
    finally:
        conn.close()
    return coverage
