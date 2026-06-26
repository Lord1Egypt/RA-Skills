from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.config import load_config
from app.core.settings import get_adapter_path, get_var_dir
from app.core.stats import (
    get_corpus_stats,
    get_drafting_model_status,
    get_latest_ingest_status,
    get_model_readiness,
    get_model_status,
    get_pipeline_status,
    summarize_draft_events,
)
from app.core.version import get_version
from app.db.bootstrap import resolve_sqlite_path

router = APIRouter(tags=["stats"])

ROOT_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT_DIR / "templates" / "stats.html"


@router.get("/api/config")
def get_api_config(request: Request) -> dict[str, Any]:
    config = load_config()
    user_name = config.get("user", {}).get("name", "")
    display_name = config.get("user", {}).get("display_name", "") or "YouOS"

    db_path = resolve_sqlite_path(request.app.state.settings.database_url)
    corpus_ready = False
    model_ready = False
    feedback_pair_count = 0
    adapter_ready = (get_adapter_path() / "adapters.safetensors").exists()
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        try:
            count = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
            corpus_ready = count > 0
            model_ready = adapter_ready
            feedback_pair_count = conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]
        except sqlite3.OperationalError:
            pass
        finally:
            conn.close()

    return {
        "display_name": display_name,
        "user_name": user_name,
        "version": get_version(),
        "corpus_ready": corpus_ready,
        "model_ready": model_ready,
        "feedback_pair_count": feedback_pair_count,
        "adapter_ready": adapter_ready,
    }


class ConfigSetRequest(BaseModel):
    key: str
    value: Any


class IdentityRequest(BaseModel):
    name: str | None = None
    emails: list[str] | None = None
    display_name: str | None = None  # explicit override; otherwise derived as <First>OS


# Lookback → Gmail `newer_than:` filter. Whitelisted so nothing the user types
# reaches the ingest command; "all" omits the date filter.
INGEST_LOOKBACKS: dict[str, str] = {
    "6m": "newer_than:6m",
    "1y": "newer_than:1y",
    "2y": "newer_than:2y",
    "3y": "newer_than:3y",
    "4y": "newer_than:4y",
    "all": "",
}


class IngestRequest(BaseModel):
    lookback: str = "1y"


@router.get("/api/config/flags")
def get_config_flags() -> dict:
    """List the whitelisted feature flags + their current values (for the
    settings page / onboarding wizard to render toggles)."""
    from app.core.feature_flags import list_flags

    return {"flags": list_flags()}


@router.post("/api/config/set")
def set_config_flag(body: ConfigSetRequest) -> dict:
    """Set one whitelisted feature flag. Restricted to the feature-flag
    whitelist, so this can't write arbitrary config keys."""
    from app.core.feature_flags import set_flag

    try:
        value = set_flag(body.key, body.value)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown flag: {body.key}") from None
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid value for {body.key}: {exc}") from None
    return {"ok": True, "key": body.key, "value": value}


@router.post("/api/config/identity")
def set_config_identity(body: IdentityRequest) -> dict:
    """Set the user's name / email addresses (onboarding + settings)."""
    from app.core.feature_flags import set_identity

    try:
        result = set_identity(body.name, body.emails, display_name=body.display_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None
    return {"ok": True, **result}


@router.post("/api/ingest")
def trigger_ingest(body: IngestRequest, request: Request) -> dict:
    """Kick off Gmail ingestion in the background, bounded by a lookback window.

    The lookback is whitelisted and the command is an arg list (no shell), so
    nothing user-supplied is interpolated into a command. Returns immediately;
    the wizard polls /api/ingest/status for progress.
    """
    if body.lookback not in INGEST_LOOKBACKS:
        raise HTTPException(status_code=400, detail=f"lookback must be one of {sorted(INGEST_LOOKBACKS)}")

    database_url = request.app.state.settings.database_url
    if get_latest_ingest_status(database_url).get("status") == "running":
        raise HTTPException(status_code=409, detail="An ingestion is already running.")

    date_filter = INGEST_LOOKBACKS[body.lookback]
    query = f"in:anywhere {date_filter}".strip()
    script = ROOT_DIR / "scripts" / "ingest_gmail_threads.py"
    # Detached background process: fetch all threads within the date window.
    subprocess.Popen(  # noqa: S603
        [sys.executable, str(script), "--live", "--query", query, "--max-threads", "0"],
        cwd=str(ROOT_DIR),
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return {"started": True, "lookback": body.lookback, "query": query}


@router.get("/api/ingest/status")
def ingest_status(request: Request) -> dict:
    return get_latest_ingest_status(request.app.state.settings.database_url)


# Tracks an in-progress wizard-launched fine-tune (single-worker dev server).
_finetune_proc: Any = None


@router.post("/api/finetune")
def trigger_finetune() -> dict:
    """Run export -> LoRA fine-tune -> golden benchmark in the background.

    Chaining the golden eval means the adapter is *validated* before we call the
    model "ready" — so the wizard's readiness gate can actually clear without
    waiting for the nightly. Same single detached process (one running handle).
    """
    global _finetune_proc
    if _finetune_proc is not None and _finetune_proc.poll() is None:
        raise HTTPException(status_code=409, detail="Fine-tuning is already running.")
    scripts = ROOT_DIR / "scripts"
    # Sequential export -> finetune -> benchmark in one detached process; paths
    # are constants (no user input), invoked as an arg list (no shell).
    code = (
        "import subprocess,sys;"
        f"subprocess.run([sys.executable, {str(scripts / 'export_feedback_jsonl.py')!r}], check=False);"
        f"subprocess.run([sys.executable, {str(scripts / 'finetune_lora.py')!r}], check=False);"
        f"subprocess.run([sys.executable, {str(scripts / 'run_golden_eval.py')!r}], check=False)"
    )
    _finetune_proc = subprocess.Popen(  # noqa: S603
        [sys.executable, "-c", code],
        cwd=str(ROOT_DIR),
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return {"started": True}


@router.get("/api/finetune/status")
def finetune_status() -> dict:
    running = _finetune_proc is not None and _finetune_proc.poll() is None
    adapter_ready = (get_adapter_path() / "adapters.safetensors").exists()
    return {"status": "running" if running else ("done" if adapter_ready else "idle"), "adapter_ready": adapter_ready}


_benchmark_proc: Any = None


@router.post("/api/benchmark")
def trigger_benchmark() -> dict:
    """Run the golden benchmark on the *current* adapter in the background.

    Lets the readiness gate clear (trained → benchmarked → ready) without
    retraining or waiting for the nightly — the action behind the banner's
    "Run benchmark now".
    """
    global _benchmark_proc
    if _benchmark_proc is not None and _benchmark_proc.poll() is None:
        raise HTTPException(status_code=409, detail="A benchmark is already running.")
    if _finetune_proc is not None and _finetune_proc.poll() is None:
        raise HTTPException(status_code=409, detail="Fine-tuning (which includes the benchmark) is already running.")
    _benchmark_proc = subprocess.Popen(  # noqa: S603
        [sys.executable, str(ROOT_DIR / "scripts" / "run_golden_eval.py")],
        cwd=str(ROOT_DIR),
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return {"started": True}


def _model_work_running() -> bool:
    """True while a fine-tune or a benchmark is in progress."""
    return (_finetune_proc is not None and _finetune_proc.poll() is None) or (
        _benchmark_proc is not None and _benchmark_proc.poll() is None
    )


@router.get("/api/model/readiness")
def model_readiness(request: Request) -> dict:
    """Is the personalized model trained AND benchmarked — i.e. safe to rely on?

    Drives the soft "please wait" gate on the drafting page and onboarding.
    """
    return get_model_readiness(request.app.state.settings.database_url, finetune_running=_model_work_running())


@router.post("/api/token")
def create_token() -> dict:
    """Create an API token for the browser extension (shown once)."""
    from app.core.auth import add_api_token

    return {"token": add_api_token()}


@router.post("/api/service/install")
def service_install() -> dict:
    """Install + start the launchd background service (run at login, auto-restart)."""
    from app.core import service

    ok, message = service.install()
    if not ok:
        raise HTTPException(status_code=500, detail=message)
    return {"ok": True, "message": message}


@router.get("/api/service/status")
def service_status() -> dict:
    from app.core import service

    return {"status": service.status()}


@router.get("/stats", response_class=HTMLResponse)
def stats_page() -> HTMLResponse:
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@router.get("/settings", response_class=HTMLResponse)
def settings_page() -> HTMLResponse:
    html = (ROOT_DIR / "templates" / "settings.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@router.get("/welcome", response_class=HTMLResponse)
def onboarding_page() -> HTMLResponse:
    html = (ROOT_DIR / "templates" / "onboarding.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@router.get("/api/stats")
def api_stats() -> dict[str, Any]:
    """Return API-level stats including embedding cache."""
    from app.core.embeddings import get_embedding_cache_info

    return {"embedding_cache": get_embedding_cache_info()}


@router.get("/stats/data")
def stats_data(request: Request) -> dict[str, Any]:
    settings = request.app.state.settings
    corpus = get_corpus_stats(settings.database_url)
    model = get_model_status(Path(settings.configs_dir))
    # The real "what's drafting" signal (from recent draft_events), so the UI can
    # warn when the LoRA silently isn't in use. Merged into the model payload.
    model["drafting"] = get_drafting_model_status(settings.database_url)
    pipeline_last_run = get_pipeline_status(get_var_dir().parent)
    draft_events = summarize_draft_events(settings.database_url)

    # Extract benchmark_trend from model status (kept together for source consistency)
    benchmark_trend = model.pop("benchmark_trend", [])

    # Sender profiles + cost (still needs direct DB access for row-level data)
    db_path = resolve_sqlite_path(settings.database_url)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        lora_pairs_used = 0
        try:
            row = conn.execute("SELECT COUNT(*) FROM feedback_pairs WHERE used_in_finetune = 1").fetchone()
            lora_pairs_used = row[0] if row else 0
        except sqlite3.OperationalError:
            pass

        # Per-persona feedback pair counts. Phase 1 of per-persona adapters
        # surfaces "how many pairs per cohort" so the user can see when each
        # cohort crosses the (Phase 2) training threshold without needing
        # ad-hoc SQL. NULL bucketed as "unknown" so existing pre-backfill
        # rows are visible rather than invisible.
        feedback_by_persona: dict[str, int] = {}
        try:
            rows = conn.execute(
                "SELECT COALESCE(sender_type, 'unknown') AS persona, COUNT(*) AS n "
                "FROM feedback_pairs GROUP BY persona"
            ).fetchall()
            feedback_by_persona = {str(r["persona"]): int(r["n"]) for r in rows}
        except sqlite3.OperationalError:
            # Pre-migration DB — column doesn't exist yet. Surface as empty
            # dict so a downstream UI can render "no data yet" rather than
            # crashing on the missing key.
            pass

        total_profiles = 0
        top_senders: list[dict[str, Any]] = []
        try:
            total_profiles = conn.execute("SELECT COUNT(*) FROM sender_profiles").fetchone()[0]
            rows = conn.execute(
                "SELECT email, display_name, company, sender_type, reply_count FROM sender_profiles ORDER BY reply_count DESC LIMIT 5"
            ).fetchall()
            for r in rows:
                top_senders.append(
                    {
                        "email": r["email"],
                        "display_name": r["display_name"],
                        "company": r["company"],
                        "sender_type": r["sender_type"],
                        "reply_count": r["reply_count"],
                    }
                )
        except sqlite3.OperationalError:
            pass
    finally:
        conn.close()

    total_feedback = corpus["total_feedback_pairs"]

    # Style drift detection
    drift_info: dict[str, Any] = {"status": "stable", "message": "Stable"}
    drift_path = get_var_dir() / "persona_drift.jsonl"
    if drift_path.exists():
        lines = drift_path.read_text(encoding="utf-8").strip().split("\n")
        lines = [ln for ln in lines if ln.strip()]
        if len(lines) >= 2:
            try:
                prev = json.loads(lines[-2])
                curr = json.loads(lines[-1])
                word_delta = curr.get("avg_reply_words", 0) - prev.get("avg_reply_words", 0)
                directness_delta = curr.get("directness_score", 0) - prev.get("directness_score", 0)
                if abs(word_delta) > 8 or abs(directness_delta) > 0.15:
                    drift_info["status"] = "drifting"
                    parts = []
                    if abs(word_delta) > 8:
                        direction = "shorter" if word_delta < 0 else "longer"
                        parts.append(f"replies getting {direction} ({word_delta:+.0f} words)")
                    if abs(directness_delta) > 0.15:
                        direction = "more direct" if directness_delta > 0 else "less direct"
                        parts.append(f"tone {direction}")
                    drift_info["message"] = "Drifting: " + ", ".join(parts)
            except (json.JSONDecodeError, IndexError):
                pass

    # E17: draft quality trend — weekly avg edit_distance_pct for last 8 weeks
    quality_trend: list[dict[str, Any]] = []
    # Outcome deltas: last 7d vs previous 7d
    outcome_deltas: dict[str, Any] = {}
    # E18: per-sender-type accuracy breakdown
    sender_accuracy: list[dict[str, Any]] = []
    # E19: system health card
    system_health: dict[str, Any] = {}
    conn2 = sqlite3.connect(db_path)
    conn2.row_factory = sqlite3.Row
    try:
        # E17: weekly quality trend
        try:
            trend_rows = conn2.execute(
                """
                SELECT
                    strftime('%Y-W%W', created_at) AS week,
                    ROUND(AVG(edit_distance_pct), 4) AS avg_edit_pct,
                    COUNT(*) AS pair_count
                FROM feedback_pairs
                WHERE edit_distance_pct IS NOT NULL
                  AND created_at >= date('now', '-56 days')
                GROUP BY week
                ORDER BY week ASC
                """
            ).fetchall()
            quality_trend = [{"week": r["week"], "avg_edit_pct": r["avg_edit_pct"], "count": r["pair_count"]} for r in trend_rows]
        except sqlite3.OperationalError:
            pass

        # Outcome deltas: recent 7d vs prior 7d
        try:
            row = conn2.execute(
                """
                SELECT
                    ROUND(
                        AVG(CASE WHEN created_at >= date('now', '-7 days') THEN edit_distance_pct END),
                        4
                    ) AS recent_edit,
                    ROUND(
                        AVG(
                            CASE
                                WHEN created_at < date('now', '-7 days')
                                 AND created_at >= date('now', '-14 days')
                                THEN edit_distance_pct
                            END
                        ),
                        4
                    ) AS prev_edit,
                    ROUND(
                        AVG(
                            CASE
                                WHEN created_at >= date('now', '-7 days')
                                THEN CASE WHEN rating >= 4 THEN 1.0 ELSE 0.0 END
                            END
                        ),
                        4
                    ) AS recent_high_rating,
                    ROUND(
                        AVG(
                            CASE
                                WHEN created_at < date('now', '-7 days')
                                 AND created_at >= date('now', '-14 days')
                                THEN CASE WHEN rating >= 4 THEN 1.0 ELSE 0.0 END
                            END
                        ),
                        4
                    ) AS prev_high_rating
                FROM feedback_pairs
                WHERE edit_distance_pct IS NOT NULL
                """
            ).fetchone()
            if row:
                recent_edit = row["recent_edit"]
                prev_edit = row["prev_edit"]
                recent_hr = row["recent_high_rating"]
                prev_hr = row["prev_high_rating"]
                outcome_deltas = {
                    "edit_distance_delta": round(recent_edit - prev_edit, 4) if recent_edit is not None and prev_edit is not None else None,
                    "high_rating_delta": round(recent_hr - prev_hr, 4) if recent_hr is not None and prev_hr is not None else None,
                    "recent_window_count": conn2.execute("SELECT COUNT(*) FROM feedback_pairs WHERE created_at >= date('now', '-7 days')").fetchone()[0],
                    "previous_window_count": conn2.execute(
                        "SELECT COUNT(*) FROM feedback_pairs WHERE created_at < date('now', '-7 days') AND created_at >= date('now', '-14 days')"
                    ).fetchone()[0],
                }
        except sqlite3.OperationalError:
            pass

        # E18: per-sender-type accuracy
        try:
            acc_rows = conn2.execute(
                """
                SELECT
                    sp.sender_type,
                    COUNT(fp.id) AS reviews,
                    ROUND(AVG(fp.edit_distance_pct), 4) AS avg_edit_pct,
                    ROUND(AVG(CAST(fp.rating AS REAL)), 2) AS avg_rating
                FROM feedback_pairs fp
                JOIN reply_pairs rp ON fp.reply_pair_id = rp.id
                JOIN sender_profiles sp ON lower(rp.inbound_author) LIKE '%' || lower(sp.email) || '%'
                WHERE fp.edit_distance_pct IS NOT NULL
                GROUP BY sp.sender_type
                ORDER BY reviews DESC
                """
            ).fetchall()
            sender_accuracy = [
                {"sender_type": r["sender_type"], "reviews": r["reviews"], "avg_edit_pct": r["avg_edit_pct"], "avg_rating": r["avg_rating"]}
                for r in acc_rows
            ]
        except sqlite3.OperationalError:
            pass

        # E19: system health
        try:
            corpus_size = conn2.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
            last_ingestion = conn2.execute("SELECT MAX(paired_at) FROM reply_pairs").fetchone()[0]
            # Previous query (`metadata_json LIKE '%embedding%'`) didn't look at
            # the actual `embedding` BLOB column at all — it just matched the
            # literal string "embedding" inside the metadata JSON, so it was
            # producing a meaningless coverage value. Route through the
            # canonical helper that checks the BLOB column. `system_health`
            # keeps its single-float shape (chunks-only) for stats.html back-
            # compat; the per-table structured view is added below as a
            # top-level `embedding_coverage` field.
            from app.core.stats import get_embedding_coverage

            coverage_by_table = get_embedding_coverage(settings.database_url)
            system_health = {
                "corpus_size": corpus_size,
                "last_ingestion": last_ingestion,
                "embedding_coverage": coverage_by_table.get("chunks", 0.0),
                "adapter_ready": (get_adapter_path() / "adapters.safetensors").exists(),
            }
        except sqlite3.OperationalError:
            pass
    finally:
        conn2.close()

    # Structured per-table view, additive to system_health.embedding_coverage.
    # Lets the dashboard render coverage for chunks AND reply_pairs separately
    # without re-querying — and matches the shape emitted by the nightly
    # pipeline log so a chart can render both signals from one source of truth.
    from app.core.stats import get_embedding_coverage, get_persona_adapter_status

    embedding_coverage_by_table = get_embedding_coverage(settings.database_url)
    # Per-persona adapter readiness: {persona: {trained, mtime, pairs_used}}.
    # Surfaces Phase 2's training state so the user can see which personas
    # are ready for Phase 3 routed generation without poking the filesystem.
    persona_adapters = get_persona_adapter_status()

    return {
        "pipeline_last_run": pipeline_last_run,
        "corpus": corpus,
        "model": {
            **model,
            "lora_pairs_used": lora_pairs_used,
        },
        "benchmark_trend": benchmark_trend,
        "senders": {
            "total_profiles": total_profiles,
            "top_senders": top_senders,
        },
        "cost": {
            "total_drafts": total_feedback,
            "local_drafts": 0,
            "claude_drafts": total_feedback,
        },
        "style_drift": drift_info,
        "quality_trend": quality_trend,
        "outcome_deltas": outcome_deltas,
        "sender_accuracy": sender_accuracy,
        "system_health": system_health,
        "embedding_coverage": embedding_coverage_by_table,
        "feedback_by_persona": feedback_by_persona,
        "persona_adapters": persona_adapters,
        "draft_events": draft_events,
    }
