from __future__ import annotations

import json
import logging
import re
import sqlite3
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.core.config import get_review_batch_size, get_review_draft_model
from app.core.diff import hybrid_similarity, similarity_ratio
from app.core.sender import classify_sender
from app.core.text_utils import decode_html_entities, strip_quoted_text
from app.db.bootstrap import connect, resolve_sqlite_path
from app.generation.service import DraftRequest, _adapter_available, generate_draft

router = APIRouter(prefix="/review-queue", tags=["review-queue"])

_RQ_MAX_WORKERS = 4  # parallel draft generation threads


def _resolve_use_local_model() -> bool:
    """Resolve whether to use the local model for Review Queue drafts based on config.

    review.draft_model:
      'claude' (default) — always use Claude (faster)
      'local'            — always use local Qwen adapter
      'auto'             — use local if adapter is ready, else Claude
    """
    model_pref = get_review_draft_model()
    if model_pref == "local":
        return True
    if model_pref == "auto":
        return _adapter_available()
    return False  # 'claude'


def _generate_draft_for_candidate(
    cand: dict[str, Any],
    *,
    database_url: str,
    configs_dir: Any,
    use_local_model: bool = False,
) -> dict[str, Any] | None:
    """Generate a draft for a single candidate. Returns item dict or None on failure."""
    display_inbound = decode_html_entities(cand["inbound_text"])
    clean_inbound = strip_quoted_text(display_inbound)
    try:
        draft_response = generate_draft(
            DraftRequest(
                inbound_message=clean_inbound,
                sender=cand["inbound_author"],
                use_local_model=use_local_model,
            ),
            database_url=database_url,
            configs_dir=configs_dir,
        )
        return {
            "reply_pair_id": cand["reply_pair_id"],
            "inbound_text": display_inbound,
            "inbound_author": cand["inbound_author"],
            "subject": cand["subject"],
            "generated_draft": draft_response.draft,
            "sender_profile": None,  # filled in after
            "account_email": cand.get("account_email"),
            "paired_at": cand["paired_at"],
            "suggested_subject": getattr(draft_response, "suggested_subject", None),
            "_cand_author": cand["inbound_author"],  # for profile lookup
        }
    except Exception as exc:
        logger.warning("Draft generation failed for rp %s: %s", cand.get("reply_pair_id"), exc)
        return None

# Content patterns that indicate automated/machine-generated emails — not useful for training
_AUTOMATED_CONTENT_PATTERNS = re.compile(
    r"(multifunction printer|xerox scan|attachment file type|"
    r"this is an automated (message|email|notification|response)|"
    r"do not reply to this (email|message)|"
    r"you are receiving this (email|message) because|"
    r"unsubscribe|manage (your )?preferences|"
    r"this message was sent to|"
    r"view (this email|in browser)|"
    r"privacy policy|terms of service|"
    r"invoice #|order #|order confirmation|"
    r"your (order|payment|subscription|account) (has been|is|was)|"
    r"transaction (id|reference|number)|"
    r"receipt for your|"
    r"security (alert|notification|code)|"
    r"verification code|one-time (password|code)|otp:|"
    r"password (reset|change)|reset your password|"
    r"reacted to your message|liked your message|"
    r"assets/reaction/|/reaction/(like|love|laugh|wow|sad|angry)\.png)",
    re.IGNORECASE,
)

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parents[2]

# Track last sender profile rebuild time (epoch seconds)
_last_sender_profile_rebuild: float = 0.0


def _trigger_sender_profile_rebuild() -> None:
    """Launch build_sender_profiles.py in the background."""
    global _last_sender_profile_rebuild
    try:
        subprocess.Popen(
            [sys.executable, str(ROOT_DIR / "scripts" / "build_sender_profiles.py")],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _last_sender_profile_rebuild = time.time()
        logger.info("Triggered background sender profile rebuild")
    except Exception as exc:
        logger.warning("Failed to trigger sender profile rebuild: %s", exc)


def _get_db_path(request: Request) -> Path:
    return resolve_sqlite_path(request.app.state.settings.database_url)


def _get_settings(request: Request):
    return request.app.state.settings


def score_pair_for_review(pair: dict[str, Any], reviewed_sender_types: Counter) -> float:
    """Score a candidate pair for review priority.

    Higher score = more likely to be selected.
    """
    score = 0.0

    # Recency bonus — prefer pairs from last 6 months
    six_months_ago = datetime.now(tz=timezone.utc) - timedelta(days=180)
    paired_at = pair.get("paired_at") or ""
    if paired_at:
        try:
            dt = datetime.fromisoformat(paired_at.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt > six_months_ago:
                score += 0.3
        except (ValueError, TypeError):
            pass

    # Continuous recency score — 1.0 for today, 0.0 for 1yr+
    if paired_at:
        try:
            dt = datetime.fromisoformat(paired_at.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            days_old = (datetime.now(tz=timezone.utc) - dt).days
            recency_score = max(0.0, 1.0 - (days_old / 365))
            score += recency_score * 0.3
        except (ValueError, TypeError):
            pass

    # Sender type diversity bonus
    sender_type = classify_sender(pair.get("inbound_author"))
    if reviewed_sender_types[sender_type] < 2:
        score += 0.4

    # Length filter — prefer medium length (100-500 chars inbound)
    inbound_len = len(pair.get("inbound_text") or "")
    if 100 < inbound_len < 500:
        score += 0.3

    return score


def _recipient_list_contains_email(recipients: Any, email: str) -> bool:
    """Return True if recipient list contains the given email."""
    if not recipients or not email:
        return False
    target = email.strip().lower()
    if not target:
        return False

    if not isinstance(recipients, list):
        recipients = [recipients]

    for item in recipients:
        if isinstance(item, dict):
            value = (item.get("email") or "").strip().lower()
            if value == target:
                return True
        elif isinstance(item, str) and item.strip().lower() == target:
            return True
    return False


def _fetch_candidates(
    db_path: Path,
    batch_size: int,
    exclude_ids: list[int],
) -> tuple[list[dict[str, Any]], int]:
    """Select reply_pairs not yet reviewed, with smart scoring for diversity."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # Count total unreviewed
        total_unreviewed = conn.execute(
            """
            SELECT COUNT(*) FROM reply_pairs rp
            WHERE NOT EXISTS (
                SELECT 1 FROM feedback_pairs fp WHERE fp.reply_pair_id = rp.id
            )
            """
        ).fetchone()[0]

        # Build exclude clause
        placeholders = ""
        params: list[Any] = []
        if exclude_ids:
            placeholders = " AND rp.id NOT IN ({})".format(",".join("?" for _ in exclude_ids))
            params.extend(exclude_ids)

        # Fetch a larger pool for scoring
        query = """
            SELECT rp.id, rp.inbound_text, rp.inbound_author, rp.reply_text,
                   rp.paired_at, rp.metadata_json,
                   d.title as doc_title,
                   d.metadata_json as doc_metadata_json
            FROM reply_pairs rp
            LEFT JOIN documents d ON rp.document_id = d.id
            WHERE NOT EXISTS (
                SELECT 1 FROM feedback_pairs fp WHERE fp.reply_pair_id = rp.id
            )
            AND LENGTH(rp.inbound_text) >= 50
            AND rp.inbound_text NOT LIKE '---------- Forwarded%%'
            {}
            ORDER BY rp.paired_at DESC
            LIMIT ?
        """.format(placeholders)
        params.append(batch_size * 5)  # fetch larger pool for scoring

        rows = conn.execute(query, params).fetchall()

        # First pass: filter out automated senders, short replies, and build candidate list
        pool: list[dict[str, Any]] = []
        for row in rows:
            author = row["inbound_author"] or ""
            author_lower = author.lower()

            # Hard filter: automated sender prefixes
            if any(
                prefix in author_lower
                for prefix in [
                    "no-reply",
                    "noreply",
                    "donotreply",
                    "do-not-reply",
                    "mailer-daemon",
                    "notifications",
                    "notification",
                    "receipt",
                    "invoice",
                    "billing",
                    "payment",
                    "confirm",
                    "automated",
                    "newsletter",
                    "marketing",
                    "support@",
                    "info@",
                    "hello@",
                    "team@",
                    "contact@",
                ]
            ):
                continue

            # Also use classify_sender to catch automated senders not covered by prefixes
            sender_type = classify_sender(author)
            if sender_type == "automated":
                continue

            # Content-based filter: skip emails that look machine-generated
            inbound_text = row["inbound_text"] or ""
            if _AUTOMATED_CONTENT_PATTERNS.search(inbound_text[:500]):
                continue

            # Skip very short replies (< 20 chars) — not useful training signal
            if len(row["reply_text"] or "") < 20:
                continue

            doc_meta = {}
            if row["doc_metadata_json"]:
                try:
                    doc_meta = json.loads(row["doc_metadata_json"])
                except (json.JSONDecodeError, TypeError):
                    pass

            # Exclude threads where account owner is CC'd but not a direct recipient.
            # These are often informational copies and not emails requiring a reply.
            account_email = (doc_meta.get("account_email") or "").strip().lower()
            recipients = doc_meta.get("recipients") or {}
            if account_email and isinstance(recipients, dict):
                is_in_to = _recipient_list_contains_email(recipients.get("to"), account_email)
                is_in_cc = _recipient_list_contains_email(recipients.get("cc"), account_email)
                if is_in_cc and not is_in_to:
                    continue

            pool.append(
                {
                    "reply_pair_id": row["id"],
                    "inbound_text": row["inbound_text"],
                    "inbound_author": row["inbound_author"],
                    "subject": row["doc_title"],
                    "reply_text": row["reply_text"],
                    "paired_at": row["paired_at"],
                    "account_email": doc_meta.get("account_email"),
                }
            )

        # Second pass: score and select with diversity
        reviewed_sender_types: Counter = Counter()
        scored = [(score_pair_for_review(p, reviewed_sender_types), i, p) for i, p in enumerate(pool)]
        scored.sort(key=lambda x: x[0], reverse=True)

        candidates: list[dict[str, Any]] = []
        for _score, _idx, pair in scored:
            if len(candidates) >= batch_size:
                break
            sender_type = classify_sender(pair.get("inbound_author"))
            candidates.append(pair)
            reviewed_sender_types[sender_type] += 1

        return candidates, total_unreviewed
    finally:
        conn.close()


def _lookup_sender_profile_safe(db_path: Path, email: str) -> dict[str, Any] | None:
    """Look up sender profile, returning None if table doesn't exist or no match."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='sender_profiles'").fetchone()
        if not exists:
            return None
        # Extract email address from "Name <email>" format
        import re

        match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", email)
        if not match:
            return None
        clean_email = match.group(0).lower()
        row = conn.execute("SELECT * FROM sender_profiles WHERE email = ?", (clean_email,)).fetchone()
        if not row:
            return None
        return {
            "display_name": row["display_name"],
            "company": row["company"],
            "sender_type": row["sender_type"],
            "reply_count": row["reply_count"],
        }
    except Exception:
        return None
    finally:
        conn.close()


def _count_reviewed_today(db_path: Path) -> int:
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute("SELECT COUNT(*) FROM feedback_pairs WHERE DATE(created_at) = DATE('now')").fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def _get_review_streak(db_path: Path) -> int:
    """Return the number of consecutive days with at least one review, ending today."""
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT DATE(created_at) as review_date, COUNT(*) as cnt
            FROM feedback_pairs
            WHERE created_at IS NOT NULL
            GROUP BY DATE(created_at)
            ORDER BY review_date DESC
            """
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return 0

    from datetime import date, timedelta

    today = date.today()
    streak = 0
    expected = today
    for row in rows:
        try:
            row_date = date.fromisoformat(row[0])
        except (ValueError, TypeError):
            continue
        if row_date == expected:
            streak += 1
            expected = expected - timedelta(days=1)
        elif row_date < expected:
            # Gap — streak broken
            break
    return streak


def _update_streak_table(db_path: Path, count: int) -> None:
    """Upsert today's review count into review_streaks table."""
    conn = sqlite3.connect(db_path)
    try:
        # Ensure table exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS review_streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                review_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute(
            "INSERT INTO review_streaks (date, review_count) VALUES (DATE('now'), ?) "
            "ON CONFLICT(date) DO UPDATE SET review_count = excluded.review_count",
            (count,),
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


@router.get("/next")
def review_queue_next(
    request: Request,
    batch_size: int = Query(default=None, ge=1, le=50),
    exclude_ids: str = Query(default=""),
) -> dict:
    db_path = _get_db_path(request)
    settings = _get_settings(request)

    # Use config batch_size if not explicitly provided
    if batch_size is None:
        batch_size = get_review_batch_size()

    # Parse exclude_ids
    excluded: list[int] = []
    if exclude_ids.strip():
        excluded = [int(x) for x in exclude_ids.split(",") if x.strip().isdigit()]

    candidates, total_unreviewed = _fetch_candidates(db_path, batch_size, excluded)

    # Generate all drafts in parallel (model determined by review.draft_model config)
    use_local = _resolve_use_local_model()
    workers = 1 if use_local else _RQ_MAX_WORKERS  # local model can't run in parallel
    items = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _generate_draft_for_candidate,
                cand,
                database_url=settings.database_url,
                configs_dir=settings.configs_dir,
                use_local_model=use_local,
            ): cand
            for cand in candidates[:batch_size]
        }
        for future in as_completed(futures):
            result = future.result()
            if result is None:
                continue
            author = result.pop("_cand_author", None)
            if author:
                result["sender_profile"] = _lookup_sender_profile_safe(db_path, author)
            items.append(result)
            if len(items) >= batch_size:
                break

    # Trigger sender profile rebuild if last rebuild was > 1 hour ago
    global _last_sender_profile_rebuild
    if items and (time.time() - _last_sender_profile_rebuild) > 3600:
        _trigger_sender_profile_rebuild()

    reviewed_today = _count_reviewed_today(db_path)
    streak = _get_review_streak(db_path)

    return {
        "items": items,
        "total_unreviewed": total_unreviewed,
        "reviewed_today": reviewed_today,
        "streak_days": streak,
    }


class ReviewSubmitBody(BaseModel):
    reply_pair_id: int
    inbound_text: str = Field(min_length=1)
    generated_draft: str = Field(min_length=1)
    edited_reply: str = Field(min_length=1)
    feedback_note: str | None = None
    rating: int = Field(default=4, ge=1, le=5)


@router.get("/next-stream")
def review_queue_next_stream(
    request: Request,
    batch_size: int = Query(default=None, ge=1, le=50),
    exclude_ids: str = Query(default=""),
) -> StreamingResponse:
    """Stream review queue items one by one as SSE, generating drafts progressively."""
    db_path = _get_db_path(request)
    settings = _get_settings(request)

    if batch_size is None:
        batch_size = get_review_batch_size()

    excluded: list[int] = []
    if exclude_ids.strip():
        excluded = [int(x) for x in exclude_ids.split(",") if x.strip().isdigit()]

    candidates, total_unreviewed = _fetch_candidates(db_path, batch_size, excluded)
    reviewed_today = _count_reviewed_today(db_path)
    streak = _get_review_streak(db_path)

    # Pre-enrich candidates with sender profiles (fast DB lookup, no model needed)
    enriched: list[dict[str, Any]] = []
    for cand in candidates[:batch_size]:
        display_inbound = decode_html_entities(cand["inbound_text"])
        clean_inbound = strip_quoted_text(display_inbound)
        sender_profile = _lookup_sender_profile_safe(db_path, cand["inbound_author"]) if cand["inbound_author"] else None
        enriched.append({**cand, "_display_inbound": display_inbound, "_clean_inbound": clean_inbound, "_sender_profile": sender_profile})

    def _generate() -> Any:
        # 1. Send metadata
        meta = {
            "type": "meta",
            "total_unreviewed": total_unreviewed,
            "reviewed_today": reviewed_today,
            "batch_size": len(enriched),
            "streak_days": streak,
        }
        yield f"data: {json.dumps(meta)}\n\n"

        if not enriched:
            yield 'data: {"type": "done"}\n\n'
            return

        # 2. Send all email previews immediately — no waiting for drafts
        for i, cand in enumerate(enriched):
            preview = {
                "type": "item_preview",
                "index": i,
                "reply_pair_id": cand["reply_pair_id"],
                "inbound_text": cand["_display_inbound"],
                "inbound_author": cand["inbound_author"],
                "subject": cand["subject"],
                "sender_profile": cand["_sender_profile"],
                "account_email": cand.get("account_email"),
                "paired_at": cand["paired_at"],
                "generated_draft": None,  # draft pending
            }
            yield f"data: {json.dumps(preview)}\n\n"

        # 3. Generate drafts and stream each one as it completes
        use_local = _resolve_use_local_model()
        workers = 1 if use_local else _RQ_MAX_WORKERS
        item_count = 0

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_idx = {
                executor.submit(
                    _generate_draft_for_candidate,
                    cand,
                    database_url=settings.database_url,
                    configs_dir=settings.configs_dir,
                    use_local_model=use_local,
                ): i
                for i, cand in enumerate(enriched)
            }
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                result = future.result()
                if result is None:
                    yield f"data: {json.dumps({'type': 'item_draft', 'index': idx, 'error': True})}\n\n"
                    continue
                result.pop("_cand_author", None)
                draft_msg = {
                    "type": "item_draft",
                    "index": idx,
                    "generated_draft": result["generated_draft"],
                    "suggested_subject": result.get("suggested_subject"),
                }
                yield f"data: {json.dumps(draft_msg)}\n\n"
                item_count += 1

        yield 'data: {"type": "done"}\n\n'

        global _last_sender_profile_rebuild
        if item_count > 0 and (time.time() - _last_sender_profile_rebuild) > 3600:
            _trigger_sender_profile_rebuild()

    return StreamingResponse(_generate(), media_type="text/event-stream")


@router.post("/submit")
def review_queue_submit(body: ReviewSubmitBody, request: Request) -> dict:
    db_path = _get_db_path(request)
    edit_distance_pct = round(1.0 - similarity_ratio(body.generated_draft, body.edited_reply), 4)

    conn = connect(db_path)
    try:
        # Persona-routing cohort (Phase 1 of per-persona adapters): derive
        # sender_type from the linked reply_pair's inbound_author so this row
        # is correctly cohorted at training time. NULL when the lookup fails
        # (deleted reply_pair, or one with no inbound_author) — treated as
        # "unknown" by downstream consumers.
        sender_type: str | None = None
        try:
            row = conn.execute(
                "SELECT inbound_author FROM reply_pairs WHERE id = ?",
                (body.reply_pair_id,),
            ).fetchone()
            if row and row[0]:
                from app.core.sender import classify_sender

                sender_type = classify_sender(row[0])
        except sqlite3.OperationalError:
            # No reply_pairs table (very fresh install) — leave NULL.
            pass

        # Atomic insert-if-absent. A plain check-then-insert raced: two concurrent
        # submits of the same reply_pair_id could both pass the check and double
        # insert. The WHERE NOT EXISTS runs inside the insert's write transaction,
        # so at most one row is created.
        cur = conn.execute(
            """
            INSERT INTO feedback_pairs
                (inbound_text, generated_draft, edited_reply, feedback_note,
                 rating, edit_distance_pct, reply_pair_id, sender_type)
            SELECT ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM feedback_pairs WHERE reply_pair_id = ?
            )
            """,
            (
                body.inbound_text,
                body.generated_draft,
                body.edited_reply,
                body.feedback_note,
                body.rating,
                edit_distance_pct,
                body.reply_pair_id,
                sender_type,
                body.reply_pair_id,
            ),
        )
        conn.commit()
        if cur.rowcount == 0:
            existing = conn.execute(
                "SELECT id FROM feedback_pairs WHERE reply_pair_id = ?",
                (body.reply_pair_id,),
            ).fetchone()
            return {"status": "already_submitted", "feedback_id": existing[0] if existing else None}
        total = conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]

        # Save to draft_history
        try:
            conn.execute(
                """INSERT INTO draft_history
                   (inbound_text, sender, generated_draft, final_reply, edit_distance_pct)
                   VALUES (?, ?, ?, ?, ?)""",
                (body.inbound_text, None, body.generated_draft, body.edited_reply, edit_distance_pct),
            )
            conn.commit()
        except Exception:
            pass
    finally:
        conn.close()

    # Update streak table and trigger sender profile rebuild every 10 submissions
    reviewed_today = _count_reviewed_today(db_path)
    _update_streak_table(db_path, reviewed_today)
    if total % 10 == 0:
        _trigger_sender_profile_rebuild()

    streak = _get_review_streak(db_path)
    return {"status": "saved", "total_pairs": total, "edit_distance_pct": edit_distance_pct, "streak_days": streak}


@router.post("/trigger-autoresearch")
def trigger_autoresearch() -> dict:
    """Fire off the autoresearch loop in the background after a batch is complete."""
    import subprocess
    import threading

    def _run() -> None:
        try:
            venv_python = Path(__file__).resolve().parents[3] / ".venv" / "bin" / "python3"
            script = Path(__file__).resolve().parents[3] / "scripts" / "nightly_pipeline.py"
            subprocess.run([str(venv_python), str(script), "--autoresearch-only"], timeout=7200)
        except Exception:
            pass

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return {"status": "started", "message": "Autoresearch optimization started in background."}


class CompareBody(BaseModel):
    inbound_text: str = Field(min_length=1)
    sender: str | None = None


@router.post("/compare")
def draft_compare(body: CompareBody, request: Request) -> dict:
    """Compare Qwen+LoRA adapter vs Qwen base (no adapter)."""
    settings = _get_settings(request)
    clean_inbound = strip_quoted_text(body.inbound_text)

    # Adapter draft (with LoRA adapter + exemplars)
    try:
        adapter_response = generate_draft(
            DraftRequest(
                inbound_message=clean_inbound,
                sender=body.sender,
                use_adapter=True,
            ),
            database_url=settings.database_url,
            configs_dir=settings.configs_dir,
        )
        adapter_draft = adapter_response.draft
        adapter_confidence = adapter_response.confidence
        exemplar_count = len(adapter_response.precedent_used)
    except Exception as exc:
        adapter_draft = f"[generation failed: {exc}]"
        adapter_confidence = "error"
        exemplar_count = 0

    # Base draft (no adapter, no exemplars)
    try:
        base_response = generate_draft(
            DraftRequest(
                inbound_message=clean_inbound,
                sender=body.sender,
                use_adapter=False,
                top_k_reply_pairs=0,
                top_k_chunks=0,
            ),
            database_url=settings.database_url,
            configs_dir=settings.configs_dir,
        )
        base_draft = base_response.draft
    except Exception as exc:
        base_draft = f"[generation failed: {exc}]"

    # Compute improvement hint based on similarity
    try:
        sim = hybrid_similarity(adapter_draft, base_draft)
        if sim < 0.7:
            improvement_hint = "Adapter appears to be helping"
        else:
            improvement_hint = "Drafts similar — adapter may need more training"
    except Exception:
        improvement_hint = "Unable to compare drafts"

    return {
        "adapter_draft": adapter_draft,
        "base_draft": base_draft,
        "adapter_confidence": adapter_confidence,
        "exemplar_count": exemplar_count,
        "improvement_hint": improvement_hint,
    }
