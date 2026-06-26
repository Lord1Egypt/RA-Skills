import os
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from app.core.data_safety import (
    create_snapshot,
    list_snapshots,
    restore_snapshot,
    run_startup_safety_checks,
)
from app.core.text_utils import strip_quoted_text
from app.core.version import get_version
from app.db.bootstrap import resolve_sqlite_path
from app.generation.service import DraftRequest, generate_draft
from app.retrieval.service import RetrievalRequest, retrieve_context

router = APIRouter()

# In-memory store for last 20 draft traces
_draft_traces: deque[dict[str, Any]] = deque(maxlen=20)


def _store_trace(
    *,
    inbound_text: str,
    sender: str | None,
    response: Any,
    intent: str | None = None,
    detected_mode: str | None = None,
) -> str:
    """Store a draft trace and return the draft_id."""
    draft_id = os.urandom(4).hex()
    exemplars = []
    for p in response.precedent_used[:5]:
        exemplars.append(
            {
                "source_id": p.get("source_id"),
                "score": p.get("score"),
                "quality_score": p.get("quality_score"),
                "subject": p.get("title"),
                "snippet": (p.get("snippet") or "")[:120],
            }
        )
    _draft_traces.append(
        {
            "draft_id": draft_id,
            "inbound_text": inbound_text[:500],
            "sender": sender,
            "exemplars": exemplars,
            "confidence": response.confidence,
            "model_used": response.model_used,
            "intent": intent,
            "detected_mode": detected_mode or response.detected_mode,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return draft_id


@router.get("/healthz")
def healthz() -> dict[str, str]:
    # Liveness — server is up. Includes the running version so external
    # checks (and the parity test) can confirm /healthz, /readyz, and
    # /api/config agree on the same runtime version.
    return {"status": "ok", "version": get_version()}


@router.get("/readyz")
def readyz(request: Request) -> dict[str, object]:
    # Readiness — server is up *and* its DB path is resolvable. Useful for
    # launchd/health probes and CI smoke checks; pairs with /healthz.
    settings = request.app.state.settings
    db_path = resolve_sqlite_path(settings.database_url)
    return {
        "status": "ok" if db_path.exists() else "starting",
        "version": get_version(),
        "db": str(db_path),
        "db_exists": db_path.exists(),
    }


@router.get("/config-summary")
def config_summary(request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "database_url": settings.database_url,
        "configs_dir": str(settings.configs_dir),
    }


@router.get("/data-safety/report")
def data_safety_report(request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    return run_startup_safety_checks(settings).to_dict()


@router.get("/data-safety/snapshots/list")
def data_safety_snapshots_list(request: Request) -> dict[str, list[str]]:
    settings = request.app.state.settings
    db_path = resolve_sqlite_path(settings.database_url)
    return {"snapshots": [str(p) for p in list_snapshots(db_path)]}


@router.post("/data-safety/snapshots/create")
def data_safety_snapshots_create(request: Request, tier: str = "manual") -> dict[str, str]:
    settings = request.app.state.settings
    db_path = resolve_sqlite_path(settings.database_url)
    try:
        snapshot_path = create_snapshot(db_path, tier=tier)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok", "snapshot_path": str(snapshot_path)}


class SnapshotRestoreBody(BaseModel):
    snapshot_path: str = Field(min_length=1)
    dry_run: bool = False


@router.post("/data-safety/snapshots/restore")
def data_safety_snapshots_restore(body: SnapshotRestoreBody, request: Request) -> dict[str, str]:
    settings = request.app.state.settings
    db_path = resolve_sqlite_path(settings.database_url)
    try:
        backup_path = restore_snapshot(db_path, Path(body.snapshot_path), dry_run=body.dry_run)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "status": "ok",
        "restored_to_db": str(db_path),
        "original_db_backed_up_to": str(backup_path),
    }


class RetrievalLookupBody(BaseModel):
    query: str = Field(min_length=1)
    scope: Literal["all", "documents", "reply_pairs"] = "all"
    source_types: list[str] = Field(default_factory=list)
    account_emails: list[str] = Field(default_factory=list)
    top_k_documents: int | None = Field(default=None, ge=1)
    top_k_chunks: int | None = Field(default=None, ge=1)
    top_k_reply_pairs: int | None = Field(default=None, ge=1)


@router.post("/retrieval/lookup")
def retrieval_lookup(body: RetrievalLookupBody, request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    try:
        response = retrieve_context(
            RetrievalRequest(
                query=body.query,
                scope=body.scope,
                source_types=tuple(body.source_types),
                account_emails=tuple(body.account_emails),
                top_k_documents=body.top_k_documents,
                top_k_chunks=body.top_k_chunks,
                top_k_reply_pairs=body.top_k_reply_pairs,
            ),
            database_url=settings.database_url,
            configs_dir=settings.configs_dir,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return response.to_dict()


class DraftBody(BaseModel):
    inbound_message: str = Field(min_length=1)
    mode: Literal["work", "personal"] | None = None
    audience_hint: str | None = None
    top_k_reply_pairs: int = Field(default=5, ge=1)
    top_k_chunks: int = Field(default=3, ge=1)
    account_email: str | None = None
    tone_hint: Literal["shorter", "more_formal", "more_detail"] | None = None
    sender: str | None = None


@router.post("/draft")
def draft(body: DraftBody, request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    try:
        response = generate_draft(
            DraftRequest(
                inbound_message=body.inbound_message,
                mode=body.mode,
                audience_hint=body.audience_hint,
                top_k_reply_pairs=body.top_k_reply_pairs,
                top_k_chunks=body.top_k_chunks,
                account_email=body.account_email,
                tone_hint=body.tone_hint,
                sender=body.sender,
            ),
            database_url=settings.database_url,
            configs_dir=settings.configs_dir,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    draft_id = _store_trace(
        inbound_text=body.inbound_message,
        sender=body.sender,
        response=response,
    )
    result = response.to_dict()
    result["draft_id"] = draft_id
    return result


@router.get("/draft/explain")
def draft_explain(draft_id: str = Query(..., min_length=1)) -> dict:
    for trace in _draft_traces:
        if trace["draft_id"] == draft_id:
            return trace
    raise HTTPException(status_code=404, detail="Draft trace not found")


class DraftCompareBody(BaseModel):
    inbound_text: str = Field(min_length=1)
    sender: str | None = None


@router.post("/draft/compare")
def draft_compare(body: DraftCompareBody, request: Request) -> dict:
    settings = request.app.state.settings
    clean_inbound = strip_quoted_text(body.inbound_text)

    try:
        retrieval_resp = generate_draft(
            DraftRequest(inbound_message=clean_inbound, sender=body.sender),
            database_url=settings.database_url,
            configs_dir=settings.configs_dir,
        )
        retrieval_draft = retrieval_resp.draft
        retrieval_confidence = retrieval_resp.confidence
        exemplar_count = len(retrieval_resp.precedent_used)
    except Exception as exc:
        retrieval_draft = f"[generation failed: {exc}]"
        retrieval_confidence = "error"
        exemplar_count = 0

    try:
        baseline_resp = generate_draft(
            DraftRequest(
                inbound_message=clean_inbound,
                sender=body.sender,
                top_k_reply_pairs=0,
                top_k_chunks=0,
            ),
            database_url=settings.database_url,
            configs_dir=settings.configs_dir,
        )
        baseline_draft = baseline_resp.draft
    except Exception as exc:
        baseline_draft = f"[generation failed: {exc}]"

    return {
        "retrieval_draft": retrieval_draft,
        "baseline_draft": baseline_draft,
        "retrieval_confidence": retrieval_confidence,
        "exemplar_count": exemplar_count,
    }
