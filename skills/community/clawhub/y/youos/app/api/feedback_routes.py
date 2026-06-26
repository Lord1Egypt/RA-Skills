from __future__ import annotations

import json
import logging
import re
import sqlite3
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.core.diff import similarity_ratio
from app.core.facts_extractor import extract_and_save
from app.core.rate_limit import RATE_LIMIT_RESPONSE, draft_limiter
from app.db.bootstrap import resolve_sqlite_path
from app.generation.service import DraftRequest, clear_exemplar_cache, generate_draft

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])


def _analyze_edit_categories(generated: str, edited: str) -> list[str]:
    """Categorize the types of edits made between generated_draft and edited_reply."""
    categories: list[str] = []
    gen_lines = generated.strip().splitlines()
    edit_lines = edited.strip().splitlines()

    # Greeting change: first non-empty line differs
    gen_first = next((line for line in gen_lines if line.strip()), "")
    edit_first = next((line for line in edit_lines if line.strip()), "")
    if gen_first != edit_first and (
        any(kw in gen_first.lower() for kw in ("hi", "hello", "dear", "hey", "good morning", "good afternoon"))
        or any(kw in edit_first.lower() for kw in ("hi", "hello", "dear", "hey", "good morning", "good afternoon"))
    ):
        categories.append("greeting_change")

    # Closing change: last non-empty line differs
    gen_last = next((line for line in reversed(gen_lines) if line.strip()), "")
    edit_last = next((line for line in reversed(edit_lines) if line.strip()), "")
    if gen_last != edit_last and (
        any(kw in gen_last.lower() for kw in ("regards", "thanks", "cheers", "sincerely", "best", "warm"))
        or any(kw in edit_last.lower() for kw in ("regards", "thanks", "cheers", "sincerely", "best", "warm"))
    ):
        categories.append("closing_change")

    # Length change
    gen_words = len(generated.split())
    edit_words = len(edited.split())
    if gen_words > 0 and edit_words > 0:
        ratio = edit_words / gen_words
        if ratio < 0.7:
            categories.append("length_change_shorter")
        elif ratio > 1.4:
            categories.append("length_change_longer")

    # Tone change: detect formality shift
    formal_words = re.compile(r"\b(please|kindly|hereby|accordingly|aforementioned|subsequently)\b", re.IGNORECASE)
    casual_words = re.compile(r"\b(hey|yeah|nope|gonna|wanna|cool|awesome|sure thing)\b", re.IGNORECASE)
    gen_formal = len(formal_words.findall(generated))
    edit_formal = len(formal_words.findall(edited))
    gen_casual = len(casual_words.findall(generated))
    edit_casual = len(casual_words.findall(edited))
    if abs(edit_formal - gen_formal) >= 2 or abs(edit_casual - gen_casual) >= 2:
        categories.append("tone_change")

    # Content addition/removal
    gen_sentences = len(re.split(r"[.!?]+", generated))
    edit_sentences = len(re.split(r"[.!?]+", edited))
    if edit_sentences > gen_sentences + 2:
        categories.append("content_addition")
    elif edit_sentences < gen_sentences - 2:
        categories.append("content_removal")

    return categories

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"
TEMPLATE_PATH = TEMPLATE_DIR / "feedback.html"


def _get_db_path(request: Request) -> Path:
    return resolve_sqlite_path(request.app.state.settings.database_url)


@router.get("", response_class=HTMLResponse)
def feedback_page() -> HTMLResponse:
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


# Bookmarklet install page — mounted outside /feedback prefix via app-level include
_BOOKMARKLET_ROUTER = APIRouter(tags=["bookmarklet"])
BOOKMARKLET_TEMPLATE = TEMPLATE_DIR / "bookmarklet.html"
POPUP_TEMPLATE = TEMPLATE_DIR / "draft_popup.html"

ABOUT_TEMPLATE = TEMPLATE_DIR / "about.html"


@_BOOKMARKLET_ROUTER.get("/about", response_class=HTMLResponse)
def about_page() -> HTMLResponse:
    html = ABOUT_TEMPLATE.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@_BOOKMARKLET_ROUTER.get("/bookmarklet", response_class=HTMLResponse)
def bookmarklet_page(request: Request) -> HTMLResponse:
    base_url = str(request.base_url).rstrip("/")
    extension_dir = str((TEMPLATE_DIR.parent / "extension").resolve())
    html = BOOKMARKLET_TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("http://localhost:8765/feedback", f"{base_url}/feedback")
    html = html.replace("http://localhost:8765/draft-popup", f"{base_url}/draft-popup")
    html = html.replace("YOUOS_BASE_URL", base_url)
    # The exact folder to pick in chrome://extensions → "Load unpacked".
    html = html.replace("YOUOS_EXTENSION_PATH", extension_dir)
    return HTMLResponse(content=html)


@_BOOKMARKLET_ROUTER.get("/draft-popup", response_class=HTMLResponse)
def draft_popup_page() -> HTMLResponse:
    """Minimal popup-optimised draft UI, embedded as iframe in Gmail."""
    html = POPUP_TEMPLATE.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@router.post("/scan-corpus-facts")
def scan_corpus_facts(request: Request) -> dict:
    """Scan the top 100 reply pairs (by quality_score) and extract facts from each."""
    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, inbound_text, reply_text, inbound_author
            FROM reply_pairs
            ORDER BY COALESCE(quality_score, 1.0) DESC
            LIMIT 100
            """
        ).fetchall()
    finally:
        conn.close()

    total_extracted = 0
    for row in rows:
        combined = f"{row['inbound_text'] or ''}\n{row['reply_text'] or ''}".strip()
        if not combined:
            continue
        try:
            facts = extract_and_save(combined, db_path, sender_email=row["inbound_author"])
            total_extracted += len(facts)
        except Exception:
            logger.warning("Facts extraction failed for reply pair %s", row["id"], exc_info=True)

    return {"status": "ok", "facts_extracted": total_extracted, "pairs_scanned": len(rows)}


class GenerateBody(BaseModel):
    inbound_text: str = Field(min_length=1)
    tone_hint: Literal["shorter", "more_formal", "more_detail"] | None = None
    sender: str | None = None
    mode: Literal["reply", "compose"] | None = "reply"
    user_prompt: str | None = None


@router.post("/generate")
def feedback_generate(body: GenerateBody, request: Request) -> dict:
    client_ip = request.client.host if request.client else "unknown"
    if not draft_limiter.is_allowed(client_ip):
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=429, content=RATE_LIMIT_RESPONSE)
    settings = request.app.state.settings
    try:
        response = generate_draft(
            DraftRequest(
                inbound_message=body.inbound_text,
                tone_hint=body.tone_hint,
                sender=body.sender,
                mode=body.mode,
                user_prompt=body.user_prompt,
            ),
            database_url=settings.database_url,
            configs_dir=settings.configs_dir,
        )
    except Exception:
        logger.exception("Draft generation failed for sender=%r", body.sender)
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=500,
            content={"error": "Draft generation failed", "detail": "An internal error occurred. Please try again."},
        )

    # Save to draft_history
    try:
        db_path = _get_db_path(request)
        conn = sqlite3.connect(db_path)
        try:
            conn.execute(
                """INSERT INTO draft_history
                   (inbound_text, sender, generated_draft, confidence, model_used, retrieval_method)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    body.inbound_text,
                    body.sender,
                    response.draft,
                    response.confidence,
                    response.model_used,
                    (
                        f"{response.retrieval_method}"
                        f"|cache_hit={int(response.exemplar_cache_hit)}"
                        f"|cache_key={response.exemplar_cache_key or ''}"
                    ),
                ),
            )
            conn.commit()
        finally:
            conn.close()
    except Exception:
        logger.warning("Failed to save draft history for sender=%r", body.sender, exc_info=True)

    # Store a draft trace so the UI's "How was this generated?" explain link
    # works (it fetches /draft/explain?draft_id=...). Without this the link was
    # never rendered because draft_id was always absent from the response.
    try:
        from app.api.routes import _store_trace

        draft_id = _store_trace(
            inbound_text=body.inbound_text,
            sender=body.sender,
            response=response,
            detected_mode=response.detected_mode,
        )
    except Exception:
        draft_id = None

    return {
        "draft": response.draft,
        "precedent_used": response.precedent_used,
        "confidence": response.confidence,
        "confidence_reason": response.confidence_reason,
        "confidence_warning": response.confidence == "low",
        "suggested_subject": response.suggested_subject,
        "exemplar_cache_hit": response.exemplar_cache_hit,
        "exemplar_cache_key": response.exemplar_cache_key,
        "model_used": response.model_used,
        "draft_id": draft_id,
    }


class SubmitBody(BaseModel):
    inbound_text: str = Field(min_length=1)
    generated_draft: str = Field(min_length=1)
    edited_reply: str = Field(min_length=1)
    feedback_note: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    sender: str | None = None
    precedents_used: list[dict] | None = None


@router.post("/submit")
def feedback_submit(body: SubmitBody, request: Request) -> dict:
    db_path = _get_db_path(request)
    edit_distance_pct = round(1.0 - similarity_ratio(body.generated_draft, body.edited_reply), 4)
    edit_categories = _analyze_edit_categories(body.generated_draft, body.edited_reply)
    edit_categories_json = json.dumps(edit_categories) if edit_categories else None
    precedents_json = json.dumps(body.precedents_used) if body.precedents_used else None
    # Persona-routing cohort (Phase 1 of per-persona adapters): the per-
    # sender_type adapter selected at generation time in Phase 3 will be
    # trained from feedback pairs filtered on this column, so classify now
    # while we have body.sender. Defaults to NULL when no sender provided
    # — the backfill / future generation paths treat NULL as "unknown".
    from app.core.sender import classify_sender

    sender_type = classify_sender(body.sender) if body.sender else None
    conn = sqlite3.connect(db_path)
    try:
        # Ensure columns exist (in case bootstrap hasn't run yet)
        cols = {row[1] for row in conn.execute("PRAGMA table_info(feedback_pairs)").fetchall()}
        if "edit_categories" not in cols:
            conn.execute("ALTER TABLE feedback_pairs ADD COLUMN edit_categories TEXT")
        if "precedents_used" not in cols:
            conn.execute("ALTER TABLE feedback_pairs ADD COLUMN precedents_used TEXT")
        if "sender_type" not in cols:
            conn.execute("ALTER TABLE feedback_pairs ADD COLUMN sender_type TEXT")
        conn.execute(
            """
            INSERT INTO feedback_pairs
                (inbound_text, generated_draft, edited_reply, feedback_note, rating,
                 edit_distance_pct, edit_categories, precedents_used, sender_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                body.inbound_text,
                body.generated_draft,
                body.edited_reply,
                body.feedback_note,
                body.rating,
                edit_distance_pct,
                edit_categories_json,
                precedents_json,
                sender_type,
            ),
        )
        conn.commit()

        # Update quality_score on linked reply_pair if reply_pair_id exists
        try:
            last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            row = conn.execute("SELECT reply_pair_id, rating, edit_distance_pct FROM feedback_pairs WHERE id = ?", (last_id,)).fetchone()
            if row and row[0] is not None and row[1] is not None:
                rp_id = row[0]
                rating = row[1]
                edp = row[2] or 0.0
                quality_score = (rating / 5.0) * (1.0 - edp) + 0.3
                quality_score = max(0.3, min(1.3, quality_score))
                conn.execute("UPDATE reply_pairs SET quality_score = ? WHERE id = ?", (round(quality_score, 4), rp_id))
                conn.commit()
                # Invalidate exemplar cache on successful quality update
                clear_exemplar_cache(database_url=request.app.state.settings.database_url)
        except Exception:
            logger.warning("Failed to update quality_score for reply pair or clear cache", exc_info=True)

        clear_exemplar_cache(database_url=request.app.state.settings.database_url)
        total = conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]
    finally:
        conn.close()

    # Extract and auto-save facts from the feedback note
    extracted_facts: list[dict] = []
    if body.feedback_note:
        try:
            extracted_facts = extract_and_save(body.feedback_note, db_path, sender_email=body.sender)
        except Exception:
            logger.warning("Facts extraction failed for feedback note", exc_info=True)

    return {
        "status": "saved",
        "total_pairs": total,
        "edit_distance_pct": edit_distance_pct,
        "edit_categories": edit_categories,
        "extracted_facts": extracted_facts,
    }
