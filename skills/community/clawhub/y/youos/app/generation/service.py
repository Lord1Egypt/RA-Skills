from __future__ import annotations

import json
import logging
import os
import re
import shutil
import signal
import sqlite3
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from app.core.config import (
    get_account_for_sender,
    get_base_model,
    get_model_fallback,
    get_persona_style_anchor,
    get_user_name,
    get_user_names,
)
from app.core.sender import classify_sender, extract_domain, first_name_from_display_name
from app.core.settings import get_adapter_path
from app.core.text_utils import strip_quoted_text
from app.db.bootstrap import connect as _connect
from app.db.bootstrap import resolve_sqlite_path
from app.retrieval.service import (
    RetrievalMatch,
    RetrievalRequest,
    RetrievalResponse,
    retrieve_context,
)

logger = logging.getLogger(__name__)

_EXEMPLAR_CACHE_TTL_SECONDS = 30 * 60
_exemplar_cache: dict[tuple[str, str], dict[str, Any]] = {}


def clear_exemplar_cache(*, database_url: str | None = None) -> None:
    _exemplar_cache.clear()
    if database_url:
        try:
            db_path = resolve_sqlite_path(database_url)
            conn = _connect(db_path)
            try:
                conn.execute("DELETE FROM exemplar_cache")
                conn.commit()
            finally:
                conn.close()
        except Exception:
            logger.warning("Failed to clear persistent exemplar cache", exc_info=True)


def _cache_key(intent_hint: str | None, sender_type: str | None) -> tuple[str, str]:
    return ((intent_hint or "general").strip().lower(), (sender_type or "unknown").strip().lower())


def _get_cached_exemplar_ids(intent_hint: str | None, sender_type: str | None, *, database_url: str | None = None) -> tuple[list[str], bool, str]:
    key = _cache_key(intent_hint, sender_type)
    key_str = f"{key[0]}::{key[1]}"

    # 1) In-memory fast path
    entry = _exemplar_cache.get(key)
    if entry:
        if time.time() - float(entry.get("ts", 0.0)) <= _EXEMPLAR_CACHE_TTL_SECONDS:
            ids = [str(x) for x in entry.get("ids", []) if x]
            logger.info("Exemplar cache HIT(mem) key=%s size=%d", key_str, len(ids))
            return ids, True, key_str
        _exemplar_cache.pop(key, None)

    # 2) Persistent fallback
    if database_url:
        try:
            db_path = resolve_sqlite_path(database_url)
            conn = _connect(db_path)
            try:
                row = conn.execute(
                    "SELECT source_ids_json, strftime('%s', updated_at) FROM exemplar_cache WHERE cache_key = ?",
                    (key_str,),
                ).fetchone()
                if row:
                    source_ids_json, updated_epoch = row
                    updated_epoch = int(updated_epoch or 0)
                    if updated_epoch and (time.time() - updated_epoch) <= _EXEMPLAR_CACHE_TTL_SECONDS:
                        ids = [str(x) for x in json.loads(source_ids_json or "[]") if x]
                        _exemplar_cache[key] = {"ts": time.time(), "ids": ids[:10]}
                        logger.info("Exemplar cache HIT(db) key=%s size=%d", key_str, len(ids))
                        return ids, True, key_str
                    conn.execute("DELETE FROM exemplar_cache WHERE cache_key = ?", (key_str,))
                    conn.commit()
            finally:
                conn.close()
        except Exception:
            logger.warning("Exemplar cache DB read failed for key=%s", key_str, exc_info=True)

    logger.info("Exemplar cache MISS key=%s", key_str)
    return [], False, key_str


def _update_exemplar_cache(intent_hint: str | None, sender_type: str | None, source_ids: list[str], *, database_url: str | None = None) -> None:
    key = _cache_key(intent_hint, sender_type)
    key_str = f"{key[0]}::{key[1]}"
    ids = [sid for sid in source_ids[:10] if sid]
    _exemplar_cache[key] = {"ts": time.time(), "ids": ids}

    if database_url:
        try:
            db_path = resolve_sqlite_path(database_url)
            conn = _connect(db_path)
            try:
                conn.execute(
                    """
                    INSERT INTO exemplar_cache(cache_key, source_ids_json, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(cache_key) DO UPDATE SET
                        source_ids_json=excluded.source_ids_json,
                        updated_at=CURRENT_TIMESTAMP
                    """,
                    (key_str, json.dumps(ids)),
                )
                conn.commit()
            finally:
                conn.close()
        except Exception:
            logger.warning("Exemplar cache DB write failed for key=%s", key_str, exc_info=True)


def _apply_cached_order(reply_pairs: list[RetrievalMatch], cached_ids: list[str]) -> list[RetrievalMatch]:
    if not cached_ids or not reply_pairs:
        return reply_pairs
    rank = {sid: i for i, sid in enumerate(cached_ids)}
    cached = [rp for rp in reply_pairs if rp.source_id in rank]
    uncached = [rp for rp in reply_pairs if rp.source_id not in rank]
    cached.sort(key=lambda rp: rank.get(rp.source_id, 9999))
    return cached + uncached


def _top_exemplar_source_ids(reply_pairs: list[RetrievalMatch], limit: int = 5) -> list[str]:
    # Prefer feedback-derived quality (metadata["quality_score"]) first, then
    # relevance score. Retrieval surfaces quality_score into metadata so this
    # primary key is live in production, not just in tests.
    ranked = sorted(
        [rp for rp in reply_pairs if rp.source_id],
        key=lambda rp: ((rp.metadata or {}).get("quality_score", 1.0), rp.score),
        reverse=True,
    )
    return [rp.source_id for rp in ranked[:limit]]


@dataclass(slots=True)
class DraftRequest:
    inbound_message: str
    mode: str | None = None
    audience_hint: str | None = None
    top_k_reply_pairs: int = 5
    top_k_chunks: int = 3
    account_email: str | None = None
    use_local_model: bool = True
    tone_hint: str | None = None
    sender: str | None = None
    intent_hint: str | None = None
    thread_id: str | None = None
    use_adapter: bool = True
    subject: str | None = None
    user_prompt: str | None = None
    # Pin the generation backend regardless of config/use_local_model. Used by
    # the cross-model comparison (app/evaluation/model_compare.py) to draft the
    # same case under each engine. One of "mlx" | "ollama" | "claude" | "none";
    # None (default) = normal selection. Pinning "mlx" still requires the local
    # model to be available — otherwise it falls through the usual chain.
    backend_override: str | None = None


@dataclass(slots=True)
class DraftResponse:
    draft: str
    detected_mode: str
    precedent_used: list[dict[str, Any]]
    retrieval_method: str
    confidence: str
    confidence_reason: str
    model_used: str
    sender_profile: dict[str, Any] | None = None
    suggested_subject: str | None = None
    token_estimate: int | None = None
    empty_output_retried: bool = False
    exemplar_cache_hit: bool = False
    exemplar_cache_key: str | None = None
    # Post-generation repair (see _repair_draft). length_flag is always
    # computed ("ok"/"long"/"short"/None); repairs lists any mutations applied
    # (only when the opt-in repair flags are enabled).
    length_flag: str | None = None
    repairs: list[str] = field(default_factory=list)
    # Ranked alternatives when multi-candidate generation is enabled (else []).
    candidates: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _load_prompts(configs_dir: Path) -> dict[str, str]:
    path = configs_dir / "prompts.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_persona(configs_dir: Path) -> dict[str, Any]:
    path = configs_dir / "persona.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _build_signature_patterns() -> list[re.Pattern[str]]:
    """Build signature-stripping patterns dynamically from config user names."""
    patterns: list[re.Pattern[str]] = []
    for name in get_user_names():
        if name.strip():
            patterns.append(re.compile(rf"^{re.escape(name)}", re.MULTILINE))
    # Standard signature delimiters
    patterns.extend(
        [
            re.compile(r"^-- $", re.MULTILINE),
            re.compile(r"^--$", re.MULTILINE),
            re.compile(r"^Best,\s*$", re.MULTILINE),
            re.compile(r"^Cheers,\s*$", re.MULTILINE),
            re.compile(r"^Regards,\s*$", re.MULTILINE),
            re.compile(r"^Kind regards,\s*$", re.MULTILINE),
            re.compile(r"^Thanks,\s*$", re.MULTILINE),
            re.compile(r"^Sent from my iPhone", re.MULTILINE),
        ]
    )
    return patterns


# Lazily built on first use so config is loaded at call time, not import time.
_signature_patterns: list[re.Pattern[str]] | None = None


def _get_signature_patterns() -> list[re.Pattern[str]]:
    global _signature_patterns
    if _signature_patterns is None:
        _signature_patterns = _build_signature_patterns()
    return _signature_patterns


def strip_signature(text: str) -> str:
    """Strip signature from reply text for use as exemplar."""
    earliest_pos = len(text)
    found = False
    for pattern in _get_signature_patterns():
        match = pattern.search(text)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()
            found = True
    if found:
        return text[:earliest_pos].rstrip()
    return text


def _score_confidence(
    reply_pairs: list[RetrievalMatch],
    score_stats: dict[str, float] | None = None,
) -> tuple[str, str]:
    if not reply_pairs:
        return "low", "no strong matches in retrieved precedent"

    top_score = max(rp.score for rp in reply_pairs)

    # Use relative thresholds when score stats are available
    if score_stats and score_stats.get("mean") is not None and score_stats.get("stddev") is not None:
        mean = score_stats["mean"]
        stddev = score_stats["stddev"]
        if top_score > mean + stddev:
            return "high", f"top score {top_score:.1f} exceeds mean+1σ ({mean:.1f}+{stddev:.1f})"
        if top_score > mean:
            return "medium", f"top score {top_score:.1f} above mean ({mean:.1f})"
        return "low", f"top score {top_score:.1f} below mean ({mean:.1f})"

    # Fallback to absolute thresholds (empty corpus or no stats)
    high_count = sum(1 for rp in reply_pairs if rp.score > 8.0)
    medium_count = sum(1 for rp in reply_pairs if rp.score > 6.0)
    if high_count >= 3:
        return "high", f"{high_count} strong reply pair matches found"
    if medium_count >= 1:
        return "medium", f"{medium_count} moderate reply pair matches found"
    return "low", "no strong matches in retrieved precedent"


def _has_thread_context(text: str) -> bool:
    """Return True if inbound_text contains multiple 'From:' blocks (multi-message thread)."""
    return text.count("From:") >= 2


def _extract_thread_parts(text: str) -> tuple[str, list[dict[str, str]]]:
    """Extract the most recent message and thread history from a multi-message thread.

    Returns (active_inbound, history) where history is a list of
    {"sender": ..., "text": ...} dicts for prior exchanges.
    """
    # Split on "From:" blocks
    parts = re.split(r"(?=^From:\s)", text, flags=re.MULTILINE)
    if len(parts) < 2:
        return text, []

    active_inbound = parts[0].strip()
    if not active_inbound and len(parts) > 1:
        active_inbound = parts[1].strip()
        parts = parts[2:]
    else:
        parts = parts[1:]

    history: list[dict[str, str]] = []
    for part in parts[:4]:  # Last 4 messages max, will take 2 exchanges
        lines = part.strip().split("\n", 1)
        sender_line = lines[0] if lines else ""
        body = lines[1].strip() if len(lines) > 1 else ""
        sender = sender_line.replace("From:", "").strip()[:80]
        history.append({"sender": sender, "text": body[:200]})

    return active_inbound, history


def _format_thread_context(active_inbound: str, history: list[dict[str, str]]) -> str:
    """Format thread history into a prompt section."""
    if not history:
        return active_inbound

    parts = ["[THREAD HISTORY — last 2 exchanges]"]
    for entry in history[:4]:
        parts.append(f"Previous: {entry['sender']} wrote: {entry['text']}")
    parts.append("---")
    parts.append("[CURRENT MESSAGE]")
    parts.append(active_inbound)
    return "\n".join(parts)


def _lookup_prior_reply_to_sender(sender: str, database_url: str, conn: sqlite3.Connection | None = None) -> str | None:
    """Find the most recent prior reply the user sent to this exact sender."""
    _own_conn = conn is None
    if _own_conn:
        db_path = resolve_sqlite_path(database_url)
        conn = _connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT reply_text FROM reply_pairs
            WHERE inbound_author LIKE ?
            ORDER BY paired_at DESC LIMIT 1
            """,
            (f"%{sender}%",),
        ).fetchone()
        if row and row[0]:
            return row[0][:PRIOR_REPLY_CHARS]
        return None
    except Exception:
        logger.warning("Failed to look up prior reply for sender %s", sender, exc_info=True)
        return None
    finally:
        if _own_conn:
            conn.close()


def _confidence_label(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def _deduplicate_by_thread(reply_pairs: list[RetrievalMatch]) -> list[RetrievalMatch]:
    """Keep only the highest-score pair per thread_id. None thread_ids are treated as unique."""
    seen_threads: dict[str, RetrievalMatch] = {}
    result: list[RetrievalMatch] = []
    for rp in reply_pairs:
        if rp.thread_id is None:
            result.append(rp)
        elif rp.thread_id not in seen_threads:
            seen_threads[rp.thread_id] = rp
            result.append(rp)
        elif rp.score > seen_threads[rp.thread_id].score:
            # Replace with higher score
            result = [r for r in result if r is not seen_threads[rp.thread_id]]
            seen_threads[rp.thread_id] = rp
            result.append(rp)
    return result


def _format_exemplars(
    reply_pairs: list[RetrievalMatch],
    *,
    max_exemplars: int = 5,
    score_stats: dict[str, float] | None = None,
) -> str:
    if not reply_pairs:
        return "(no exemplars found)"
    # Deduplicate by thread_id
    reply_pairs = _deduplicate_by_thread(reply_pairs)
    # Sort by score descending
    sorted_pairs = sorted(reply_pairs, key=lambda rp: rp.score, reverse=True)
    # Drop exemplars with score below MIN_SCORE_FILTER
    from app.retrieval.service import MIN_SCORE_FILTER
    sorted_pairs = [rp for rp in sorted_pairs if rp.score >= MIN_SCORE_FILTER]
    if not sorted_pairs:
        return "(no exemplars found)"

    # D1: Use relative thresholds (mean±σ) when stats available
    if score_stats and score_stats.get("mean") is not None and score_stats.get("stddev") is not None:
        mean = score_stats["mean"]
        stddev = score_stats["stddev"]
        def _relative_conf(score: float) -> str:
            if score > mean + stddev:
                return "high"
            if score > mean:
                return "medium"
            return "low"
        conf_fn = _relative_conf
    else:
        def _abs_conf(score: float) -> str:
            norm = min(score / 10.0, 1.0) if score > 0 else 0.0
            return _confidence_label(norm)
        conf_fn = _abs_conf

    parts: list[str] = ["The following are examples of how you have replied to similar emails:"]
    for i, rp in enumerate(sorted_pairs[:max_exemplars], 1):
        inbound = (rp.inbound_text or "")[:EXEMPLAR_INBOUND_CHARS]
        reply = strip_signature(rp.reply_text or "")[:EXEMPLAR_REPLY_CHARS]
        conf = conf_fn(rp.score)
        parts.append(f"[EXAMPLE {i} — confidence: {conf}]\nInbound: {inbound}\nYour reply: {reply}\n---")
    return "\n\n".join(parts)


def _precedent_summary(match: RetrievalMatch) -> dict[str, Any]:
    return {
        "source_id": match.source_id,
        "title": match.title,
        "snippet": match.snippet,
        "score": match.score,
        "reply_pair_id": match.reply_pair_id,
    }


_TONE_INSTRUCTIONS: dict[str, str] = {
    "shorter": "Be more concise. Aim for half the word count.",
    "more_formal": "Use a more formal, professional tone.",
    "more_detail": "Add more detail and context to your reply.",
    "warmer": "Use a warmer, friendlier, more personal tone.",
    "casual": "Use a casual, conversational tone — as you would with a close colleague.",
    "urgent": "Convey urgency clearly. Lead with the action needed and timeline.",
    "concise": "Be extremely concise. One to three sentences maximum.",
    "detailed": "Provide thorough, detailed explanations. Break down complex points.",
    "professional": "Maintain a polished, professional business tone throughout.",
}


_MEMORY_STOPWORDS = frozenset({
    "this", "that", "with", "from", "have", "been", "will", "your", "some",
    "they", "their", "what", "when", "where", "just", "like", "also", "into",
    "more", "here", "there", "about", "which", "would", "could", "should",
    "please", "thank", "regards", "hello", "dear", "hope", "doing", "well",
    "email", "reply", "send", "sent", "write", "writing",
})


def _extract_content_words(text: str) -> list[str]:
    """Extract significant words from text for project/topic matching."""
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    return [w for w in words if w not in _MEMORY_STOPWORDS]


def lookup_facts(
    *,
    sender: str | None,
    inbound_text: str,
    database_url: str,
    conn: sqlite3.Connection | None = None,
) -> list[dict[str, Any]]:
    """Query memory table for facts relevant to this draft.

    Returns facts in three categories:
    - user_pref: always included (sign-off style, meeting times, etc.)
    - contact: facts about the sender (matched by email)
    - project: facts matched by key/tag appearing in the inbound text
    """
    _own_conn = conn is None
    if _own_conn:
        db_path = resolve_sqlite_path(database_url)
        conn = _connect(db_path)
        conn.row_factory = sqlite3.Row
    facts: list[dict[str, Any]] = []
    try:
        # 1. User preferences — always include
        rows = conn.execute(
            "SELECT type, key, fact FROM memory WHERE type = 'user_pref' ORDER BY updated_at DESC"
        ).fetchall()
        facts.extend({"type": r["type"], "key": r["key"], "fact": r["fact"]} for r in rows)

        # 2. Contact facts for sender email
        if sender:
            m = re.search(r"[\w.+-]+@[\w.-]+\.\w+", sender.lower())
            email = m.group(0) if m else sender.lower().strip()
            rows = conn.execute(
                "SELECT type, key, fact FROM memory WHERE type = 'contact' AND lower(key) = ?",
                (email,),
            ).fetchall()
            facts.extend({"type": r["type"], "key": r["key"], "fact": r["fact"]} for r in rows)

        # 3. Project facts matching keywords in inbound text
        project_rows = conn.execute(
            "SELECT type, key, fact, tags FROM memory WHERE type = 'project'"
        ).fetchall()
        if project_rows:
            inbound_lower = inbound_text.lower()
            for row in project_rows:
                key_lower = row["key"].lower()
                tags = json.loads(row["tags"]) if row["tags"] else []
                if key_lower in inbound_lower or any(t.lower() in inbound_lower for t in tags):
                    facts.append({"type": row["type"], "key": row["key"], "fact": row["fact"]})

    except Exception:
        logger.exception("lookup_facts failed for sender %r", sender)
    finally:
        if _own_conn:
            conn.close()
    return facts


def _format_facts_context(facts: list[dict[str, Any]]) -> str:
    """Format facts into a prompt block."""
    if not facts:
        return ""
    lines = ["[FACTS CONTEXT — facts about this sender and your preferences]"]
    for f in facts:
        t = f["type"]
        k = f["key"]
        v = f["fact"]
        if t == "user_pref":
            lines.append(f"- Your preference ({k}): {v}")
        elif t == "contact":
            lines.append(f"- About {k}: {v}")
        elif t == "project":
            lines.append(f"- Project ({k}): {v}")
    return "\n".join(lines)


def lookup_sender_profile(email: str, database_url: str, conn: sqlite3.Connection | None = None) -> dict[str, Any] | None:
    """Look up a sender profile from the database."""
    _own_conn = conn is None
    if _own_conn:
        db_path = resolve_sqlite_path(database_url)
        conn = _connect(db_path)
        conn.row_factory = sqlite3.Row
    try:
        # Check if sender_profiles table exists
        exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='sender_profiles'").fetchone()
        if not exists:
            return None
        row = conn.execute("SELECT * FROM sender_profiles WHERE email = ?", (email.lower(),)).fetchone()
        if not row:
            return None
        profile_dict = {
            "email": row["email"],
            "display_name": row["display_name"],
            "domain": row["domain"],
            "company": row["company"],
            "sender_type": row["sender_type"],
            "relationship_note": row["relationship_note"],
            "reply_count": row["reply_count"],
            "avg_reply_words": row["avg_reply_words"],
            "first_seen": row["first_seen"],
            "last_seen": row["last_seen"],
            "topics": json.loads(row["topics_json"]) if row["topics_json"] else [],
        }
        # Include avg_response_hours if available
        try:
            profile_dict["avg_response_hours"] = row["avg_response_hours"]
        except (IndexError, KeyError):
            pass
        return profile_dict
    finally:
        if _own_conn:
            conn.close()


_GREETING_WORDS = frozenset({
    "hi", "hello", "hey", "dear", "good", "morning", "afternoon", "evening",
    "hope", "greetings", "howdy", "salutations",
})

# Lines that are pure social filler — skip entirely for subject extraction
_FILLER_PATTERNS = re.compile(
    r"^(hi|hello|hey|dear|good morning|good afternoon|good evening|"
    r"i hope (you are|you're|this finds you|all is)|"
    r"hope you (are|'re)|"
    r"thank you (for|in advance)|"
    r"thanks for|"
    r"warm regards|"
    r"kind regards|"
    r"best regards|"
    r"i am writing|"
    r"i'm writing)",
    re.IGNORECASE,
)

# Action/topic keywords that signal a meaningful sentence
_TOPIC_KEYWORDS = re.compile(
    r"\b(payment|invoice|outstanding|follow.?up|meeting|schedule|proposal|"
    r"update|confirm|approve|review|request|issue|problem|question|"
    r"deadline|project|contract|agreement|feedback|report|delivery|"
    r"order|account|subscription|renewal|support|urgent|asap|required|"
    r"please|kindly|need|want|would like)\b",
    re.IGNORECASE,
)


def _subject_fallback(inbound_text: str) -> str | None:
    """Rule-based subject line fallback.

    1. If inbound has 'Subject:' header: strip 'Re:' prefixes, return 'Re: <subject>'
    2. Find first substantive sentence (contains a topic keyword, not a filler line)
    3. Truncate to ~60 chars, capitalize cleanly
    4. If nothing found: return None (let caller decide)
    """
    # 1. Check for Subject: header in first 5 lines
    for line in inbound_text.split("\n")[:5]:
        stripped = line.strip()
        if stripped.lower().startswith("subject:"):
            subj = stripped[len("subject:"):].strip()
            while subj.lower().startswith("re:"):
                subj = subj[3:].strip()
            if subj and len(subj) >= 3:
                return f"Re: {subj}"

    # 2. Find first substantive sentence — prefer topic keywords, strip "I am/I'm" openers
    lines = [line.strip() for line in inbound_text.split("\n") if line.strip()]

    def _clean_subject(text: str) -> str | None:
        # Strip leading "I am/I'm/We are/We're" to get to the point
        text = re.sub(r"^(I am|I'm|We are|We're|I would like to|I'd like to)\s+", "", text, flags=re.IGNORECASE)
        sentence = re.split(r"[.!?]", text)[0].strip()[:65].rstrip(" ,;:")
        if len(sentence) >= 8:
            return sentence[0].upper() + sentence[1:]
        return None

    # First pass: lines with topic keywords
    for line in lines:
        if _FILLER_PATTERNS.match(line) or len(line) < 15:
            continue
        if _TOPIC_KEYWORDS.search(line):
            result = _clean_subject(line)
            if result:
                return result

    # Second pass: any non-filler line
    for line in lines:
        if _FILLER_PATTERNS.match(line) or len(line) < 15:
            continue
        result = _clean_subject(line)
        if result:
            return result

    return None


def generate_subject(inbound_text: str, draft: str, database_url: str, configs_dir: Path) -> str | None:
    """Generate a subject line for the draft reply."""
    # Try rule-based fallback first
    fallback = _subject_fallback(inbound_text)
    if fallback is not None:
        return fallback

    # Only call Claude CLI if fallback returned None and model fallback != 'none'
    model_fallback = get_model_fallback()
    if model_fallback == "none":
        return None

    try:
        prompt = (
            "Generate a concise email subject line (under 60 chars) for this reply.\n\n"
            f"Inbound:\n{inbound_text[:500]}\n\nDraft reply:\n{draft[:500]}\n\n"
            "Output ONLY the subject line, nothing else."
        )
        # Prefer the local model so subject generation doesn't depend on the
        # Claude CLI (which was the silent failure source in the nightly job
        # and stalled draft generation by 120s on every benchmark case).
        if _local_model_available():
            result = _call_local_model(prompt, max_tokens=30, use_adapter=False)
        else:
            result = _call_claude_cli(prompt)
        # Clean up: remove quotes, "Subject:" prefix
        result = result.strip().strip('"').strip("'")
        if result.lower().startswith("subject:"):
            result = result[len("subject:") :].strip()
        return result[:80] if result else None
    except Exception:
        logger.warning("Subject generation failed", exc_info=True)
        return None


def _format_sender_context(profile: dict[str, Any]) -> str:
    """Format sender profile into a prompt context block."""
    user_name = get_user_name()
    topics = ", ".join(profile.get("topics", [])) or "none recorded"
    result = (
        f"[SENDER CONTEXT]\n"
        f"Sender: {profile.get('display_name') or 'Unknown'} <{profile['email']}>\n"
        f"Company: {profile.get('company') or 'Unknown'}\n"
        f"Type: {profile.get('sender_type') or 'unknown'}\n"
        f"Relationship: {profile.get('relationship_note') or 'no note'}\n"
        f"History: {user_name} has replied {profile.get('reply_count', 0)} times to this sender. "
        f"Avg reply length: {profile.get('avg_reply_words') or 'N/A'} words.\n"
        f"Topics discussed: {topics}"
    )
    avg_response_hours = profile.get("avg_response_hours")
    if avg_response_hours is not None:
        result += f"\nTypical reply time to this sender: ~{int(avg_response_hours)}h"
    return result


def _resolve_greeting(persona: dict[str, Any], sender_type: str | None, first_name: str | None = None) -> str:
    """Resolve greeting from persona config: mode greeting > greeting_patterns > default."""
    greeting = ""
    modes = persona.get("modes", {})
    greeting_patterns = persona.get("greeting_patterns", {})
    if sender_type and sender_type in modes and "greeting" in modes[sender_type]:
        greeting = modes[sender_type]["greeting"]
    elif sender_type and sender_type in greeting_patterns:
        greeting = greeting_patterns[sender_type]
    elif "default" in greeting_patterns:
        greeting = greeting_patterns["default"]
    if greeting and "{name}" in greeting:
        if first_name:
            greeting = greeting.replace("{name}", first_name).replace("  ", " ")
        else:
            # No first name available — collapse "Hi {name}," into "Hi," rather
            # than rendering the embarrassing "Hi ," with a leading space. The
            # leading-space form of the placeholder is consumed first so the
            # punctuation around it doesn't leave a dangling " ,".
            greeting = greeting.replace(" {name}", "").replace("{name}", "")
    return greeting


def _resolve_closing(persona: dict[str, Any], sender_type: str | None) -> str:
    """Resolve closing from persona config: mode closing > closing_patterns > default."""
    closing = ""
    modes = persona.get("modes", {})
    closing_patterns = persona.get("closing_patterns", {})
    if sender_type and sender_type in modes and "closing" in modes[sender_type]:
        closing = modes[sender_type]["closing"]
    elif sender_type and sender_type in closing_patterns:
        closing = closing_patterns[sender_type]
    elif "default" in closing_patterns:
        closing = closing_patterns["default"]
    return closing


# --- Post-generation repair -------------------------------------------------
# The model output is returned with only an emptiness check today. This pass
# optionally repairs the draft and always annotates its length. Mutations are
# OFF by default (behavior-preserving) — flip them on per instance once their
# effect has been verified against real drafts.

_GREETING_TOKENS = ("hi ", "hi,", "hey", "hello", "dear", "good morning", "good afternoon", "good evening")
_CLOSING_TOKENS = (
    "best", "cheers", "regards", "kind regards", "thanks", "thank you",
    "sincerely", "talk soon", "warmly", "all the best", "speak soon",
)


def _get_repair_config() -> dict[str, bool]:
    """Read ``generation.repair`` flags (all default False / behavior-preserving)."""
    from app.core.config import load_config

    cfg = load_config() or {}
    gen = cfg.get("generation", {}) if isinstance(cfg, dict) else {}
    rep = gen.get("repair", {}) if isinstance(gen, dict) else {}
    rep = rep if isinstance(rep, dict) else {}
    return {
        "enforce_greeting_closing": bool(rep.get("enforce_greeting_closing", False)),
        "strip_trailing_signature": bool(rep.get("strip_trailing_signature", False)),
    }


def _draft_has_greeting(text: str, greeting: str) -> bool:
    first = text.lstrip().split("\n", 1)[0].strip().lower()
    if not first:
        return False
    g = greeting.strip().lower().rstrip(",")
    if g and first.startswith(g.split()[0]):
        return True
    return any(first.startswith(tok) for tok in _GREETING_TOKENS)


def _draft_has_closing(text: str, closing: str) -> bool:
    tail = "\n".join(text.rstrip().splitlines()[-3:]).lower()
    if not tail:
        return False
    c_first = closing.strip().lower().split("\n", 1)[0].split(",", 1)[0].strip()
    if c_first and c_first in tail:
        return True
    return any(tok in tail for tok in _CLOSING_TOKENS)


def _length_flag(text: str, target_words: int | None) -> str | None:
    """Non-mutating length annotation relative to the persona's target words."""
    if not target_words or target_words <= 0:
        return None
    n = len(text.split())
    if n == 0:
        return None
    if n > target_words * 2:
        return "long"
    if n < max(1, target_words // 2):
        return "short"
    return "ok"


def _repair_draft(
    draft: str,
    *,
    greeting: str,
    closing: str,
    target_words: int | None,
    config: dict[str, bool],
) -> tuple[str, list[str], str | None]:
    """Optionally repair a draft; always return its length flag.

    Returns ``(text, repairs_applied, length_flag)``. Placeholder/error drafts
    (``[...]``) are left untouched.
    """
    repairs: list[str] = []
    text = draft
    stripped_all = text.strip()
    if stripped_all.startswith("[") and stripped_all.endswith("]"):
        return text, repairs, None

    if config.get("strip_trailing_signature"):
        stripped = strip_signature(text).rstrip()
        if stripped and stripped != text.rstrip():
            text = stripped
            repairs.append("stripped_trailing_signature")

    if config.get("enforce_greeting_closing"):
        if greeting and not _draft_has_greeting(text, greeting):
            text = f"{greeting}\n\n{text.lstrip()}"
            repairs.append("added_greeting")
        if closing and not _draft_has_closing(text, closing):
            text = f"{text.rstrip()}\n\n{closing}"
            repairs.append("added_closing")

    return text, repairs, _length_flag(text, target_words)


def _draft_logging_enabled() -> bool:
    """``generation.log_drafts`` — default True (append-only local signal log)."""
    try:
        from app.core.config import load_config

        cfg = load_config() or {}
        gen = cfg.get("generation", {}) if isinstance(cfg, dict) else {}
        if isinstance(gen, dict):
            return gen.get("log_drafts", True) is not False
    except Exception:
        logger.debug("Could not read generation.log_drafts", exc_info=True)
    return True


def _log_draft_event(
    database_url: str,
    *,
    inbound_text: str,
    draft: str,
    account_email: str | None,
    sender: str | None,
    sender_type: str | None,
    detected_mode: str | None,
    intent: str | None,
    confidence: str | None,
    confidence_reason: str | None,
    model_used: str | None,
    retrieval_method: str | None,
    exemplar_ids: list[str],
    length_flag: str | None,
) -> bool:
    """Append one row to ``draft_events``. Never raises — logging a draft must
    not break drafting. Returns True if a row was written.

    Self-heals the table (``CREATE TABLE IF NOT EXISTS``) so it works on an
    instance whose DB predates this table without requiring a bootstrap.
    """
    if not _draft_logging_enabled():
        return False
    try:
        db_path = resolve_sqlite_path(database_url)
        conn = _connect(db_path)
        try:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS draft_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inbound_text TEXT NOT NULL, generated_draft TEXT NOT NULL,
                    account_email TEXT, sender TEXT, sender_type TEXT,
                    detected_mode TEXT, intent TEXT, confidence TEXT,
                    confidence_reason TEXT, model_used TEXT, retrieval_method TEXT,
                    exemplar_ids TEXT NOT NULL DEFAULT '[]', length_flag TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            conn.execute(
                """INSERT INTO draft_events
                   (inbound_text, generated_draft, account_email, sender, sender_type,
                    detected_mode, intent, confidence, confidence_reason, model_used,
                    retrieval_method, exemplar_ids, length_flag)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    inbound_text, draft, account_email, sender, sender_type, detected_mode,
                    intent, confidence, confidence_reason, model_used, retrieval_method,
                    json.dumps([str(i) for i in (exemplar_ids or [])]), length_flag,
                ),
            )
            conn.commit()
            return True
        finally:
            conn.close()
    except Exception:
        logger.warning("Failed to log draft event", exc_info=True)
        return False


def assemble_prompt(
    *,
    inbound_message: str,
    reply_pairs: list[RetrievalMatch],
    persona: dict[str, Any],
    prompts: dict[str, str],
    detected_mode: str | None = None,
    audience_hint: str | None = None,
    tone_hint: str | None = None,
    sender_context: str | None = None,
    language_hint: str | None = None,
    intent_hint: str | None = None,
    sender_type: str | None = None,
    first_name: str | None = None,
    memory_facts: list[dict[str, Any]] | None = None,
    score_stats: dict[str, float] | None = None,
    subject: str | None = None,
    user_prompt: str | None = None,
) -> str:
    style = persona.get("style", {})
    voice = style.get("voice", "direct, clear, pragmatic")
    avg_words = style.get("avg_reply_words")
    constraints = style.get("constraints", [])
    # Prefer intent-specific avg_words if available
    if intent_hint and intent_hint != "general":
        intent_avg = style.get("intent_avg_words", {})
        if isinstance(intent_avg, dict) and intent_hint in intent_avg:
            avg_words = intent_avg[intent_hint]
    system = prompts.get(
        "system_prompt",
        "You are YouOS, a local-first email copilot.",
    )

    exemplars_text = _format_exemplars(reply_pairs, score_stats=score_stats)
    n = len(reply_pairs)

    # Build persona constraints block
    persona_lines: list[str] = [f"Persona: {voice}."]
    if avg_words:
        persona_lines.append(f"Target reply length: ~{avg_words} words.")
    for c in constraints:
        persona_lines.append(f"- {c}")

    # Style-driven constraints from persona analysis
    bullet_pct = style.get("bullet_point_pct")
    if bullet_pct is not None and bullet_pct > 0.4:
        persona_lines.append("- prefer bullet points for multi-item responses")
    directness = style.get("directness_score")
    if directness is not None and directness > 0.8:
        persona_lines.append("- be direct, avoid hedging")
    avg_para = style.get("avg_paragraphs")
    if avg_para is not None and avg_para > 2:
        persona_lines.append("- use clear paragraph breaks")

    persona_block = "\n".join(persona_lines)

    style_anchor_block = ""
    if sender_type:
        style_anchor = get_persona_style_anchor(sender_type)
        if style_anchor:
            style_anchor_block = f"\n[STYLE ANCHOR — {sender_type}]\n{style_anchor.strip()}\n"

    # Build optional context lines
    context_lines: list[str] = []
    if detected_mode:
        context_lines.append(f"Detected mode: {detected_mode}")
    if audience_hint:
        context_lines.append(f"Audience: {audience_hint}")
    if intent_hint and intent_hint != "general":
        context_lines.append(f"Email intent: {intent_hint}")
    if _has_thread_context(inbound_message):
        context_lines.append("Note: This inbound message contains a multi-message thread. Consider the full conversation context when drafting your reply.")
    context_block = ""
    if context_lines:
        context_block = "\n" + "\n".join(context_lines) + "\n"

    # Build tone instruction — known keys map to instructions, free-text injected directly
    tone_instruction = ""
    if tone_hint:
        if tone_hint in _TONE_INSTRUCTIONS:
            tone_instruction = f"\n{_TONE_INSTRUCTIONS[tone_hint]}\n"
        else:
            tone_instruction = f"\nTone guidance: {tone_hint}\n"

    custom_instruction = ""
    if user_prompt and user_prompt.strip():
        custom_instruction = f"\nAdditional user instruction: {user_prompt.strip()}\n"

    sender_block = ""
    if sender_context:
        sender_block = f"\n{sender_context}\n"

    facts_block = ""
    if memory_facts:
        facts_block = f"\n{_format_facts_context(memory_facts)}\n"

    language_block = ""
    if language_hint and language_hint != "en":
        language_block = f"\n[LANGUAGE: {language_hint}] Reply in the same language as the inbound message.\n"

    result = (
        f"[SYSTEM]\n"
        f"{system.strip()}\n"
        f"{persona_block}\n"
        f"{context_block}"
        f"{style_anchor_block}"
        f"{sender_block}"
        f"{facts_block}"
        f"{language_block}"
        f"\n"
        f"[EXEMPLARS — {n} similar past replies]\n"
        f"{exemplars_text}\n"
        f"\n"
        f"[TASK]\n"
        f"Draft a reply to the following inbound message in your style.\n"
        f"Use the exemplars above as style and tone guidance.\n"
        f"Do not copy them verbatim — use them as reference only.\n"
        f"Output the draft reply text only. No preamble, no explanation.\n"
        f"{tone_instruction}"
        f"{custom_instruction}"
    )

    # Append length guidance if avg_reply_words is set
    if avg_words:
        p25 = style.get("avg_reply_words_p25")
        p75 = style.get("avg_reply_words_p75")
        if p25 is not None and p75 is not None:
            result += f"\nTarget length: ~{avg_words} words (typical range: {p25}\u2013{p75}). Be concise.\n"
        else:
            result += f"\nTarget length: ~{avg_words} words. Be concise.\n"

    # Greeting/closing injection
    greeting = _resolve_greeting(persona, sender_type, first_name)
    closing = _resolve_closing(persona, sender_type)
    if greeting and closing:
        result += f"\nBegin your reply with: {greeting}\nEnd your reply with: {closing}\n"

    inbound_section = inbound_message
    if subject:
        inbound_section = f"Subject: {subject}\n\n{inbound_message}"
    result += f"\n[INBOUND MESSAGE]\n{inbound_section}"
    return result


PROMPT_TOKEN_BUDGET: int = 2000
EXEMPLAR_REPLY_CHARS: int = 600
EXEMPLAR_INBOUND_CHARS: int = 400
PRIOR_REPLY_CHARS: int = 200
SUBPROCESS_TIMEOUT: int = 120


def _estimate_tokens(text: str) -> int:
    """Estimate token count using a simple word-count * 1.4 approximation."""
    return int(len(text.split()) * 1.4)


def _resolve_decoding(intent: str | None, confidence: str | None) -> tuple[float | None, float | None]:
    """Resolve ``(temperature, top_p)`` from ``generation.decoding`` config.

    Returns ``(None, None)`` when nothing is configured — preserving each
    backend's current default (MLX: no ``--temp``/``--top-p``; Ollama: 0.7).
    Surfacing these (like the retrieval weights) is the precondition for the
    autoresearch loop to A/B-tune fidelity vs. variety. Supports a per-intent
    temperature override (``intent_temperature``) and a per-confidence delta
    (``high_confidence_temperature_delta`` / ``low_confidence_temperature_delta``),
    e.g. lower temperature when retrieval is high-confidence.
    """
    try:
        from app.core.config import load_config

        cfg = load_config() or {}
        gen = cfg.get("generation", {}) if isinstance(cfg, dict) else {}
        dec = gen.get("decoding", {}) if isinstance(gen, dict) else {}
        if not isinstance(dec, dict) or not dec:
            return None, None

        temp = dec.get("temperature")
        intent_temps = dec.get("intent_temperature", {})
        if intent and isinstance(intent_temps, dict) and intent in intent_temps:
            temp = intent_temps[intent]

        if temp is not None and confidence:
            delta_key = {
                "high": "high_confidence_temperature_delta",
                "low": "low_confidence_temperature_delta",
            }.get(confidence)
            if delta_key and delta_key in dec:
                try:
                    temp = max(0.0, float(temp) + float(dec[delta_key]))
                except (TypeError, ValueError):
                    pass

        top_p = dec.get("top_p")
        temp_f = float(temp) if temp is not None else None
        top_p_f = float(top_p) if top_p is not None else None
        return temp_f, top_p_f
    except Exception:
        logger.debug("Could not resolve generation.decoding", exc_info=True)
        return None, None


# --- Multi-candidate generation + ranking -----------------------------------
# Optionally generate several drafts (a temperature spread) and return the
# best by a deterministic scorer. Off by default — it multiplies model calls.


def _multi_candidate_config() -> dict[str, Any]:
    """Read ``generation.multi_candidate`` (default disabled)."""
    try:
        from app.core.config import load_config

        cfg = load_config() or {}
        gen = cfg.get("generation", {}) if isinstance(cfg, dict) else {}
        mc = gen.get("multi_candidate", {}) if isinstance(gen, dict) else {}
        mc = mc if isinstance(mc, dict) else {}
        temps = mc.get("temperatures")
        if not isinstance(temps, list) or not temps:
            temps = [0.3, 0.7, 1.0]
        return {"enabled": bool(mc.get("enabled", False)), "temperatures": [float(t) for t in temps]}
    except Exception:
        logger.debug("Could not read generation.multi_candidate", exc_info=True)
        return {"enabled": False, "temperatures": [0.3, 0.7, 1.0]}


def _is_usable_draft(text: str) -> bool:
    """Mirror the empty/signature-only check used by the fallback path."""
    non_ws = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    if non_ws < 10:
        return False
    stripped_all = text.strip()
    if stripped_all.startswith("[") and stripped_all.endswith("]"):
        return False
    stripped = strip_signature(text).strip()
    return not (len(stripped) < 15 and non_ws > 0)


def _score_candidate(text: str, *, target_words: int | None, greeting: str, closing: str) -> float:
    """Deterministic candidate score (higher is better).

    Unusable (empty/placeholder/signature-only) drafts are disqualified.
    Otherwise: length-fit (peaks at the persona target) plus credit for
    honoring the persona greeting/closing when those are configured.
    """
    if not _is_usable_draft(text):
        return float("-inf")
    score = 0.0
    if target_words and target_words > 0:
        ratio = len(text.split()) / target_words
        score += max(0.0, 1.0 - abs(ratio - 1.0))  # 1.0 at exact match, →0 as it drifts
        if _length_flag(text, target_words) == "ok":
            score += 0.5
    if greeting:
        score += 0.5 if _draft_has_greeting(text, greeting) else 0.0
    if closing:
        score += 0.5 if _draft_has_closing(text, closing) else 0.0
    return score


def _rank_candidates(
    raw: list[tuple[str, str, float | None]],
    *,
    target_words: int | None,
    greeting: str,
    closing: str,
) -> list[dict[str, Any]]:
    """Score and sort candidates best-first.

    ``raw`` is a list of ``(draft, model_used, temperature)``. Returns dicts
    with the draft, model_used, temperature and score, sorted descending.
    """
    scored = [
        {
            "draft": draft,
            "model_used": model_used,
            "temperature": temperature,
            "score": _score_candidate(draft, target_words=target_words, greeting=greeting, closing=closing),
        }
        for draft, model_used, temperature in raw
    ]
    scored.sort(key=lambda c: c["score"], reverse=True)
    return scored


ADAPTER_PATH = get_adapter_path()


def _get_base_model_id() -> str:
    return get_base_model()


def _adapter_available() -> bool:
    return (ADAPTER_PATH / "adapters.safetensors").exists()


def _local_model_available() -> bool:
    """Local MLX generation is usable when the `mlx_lm` CLI is on PATH.

    Distinct from `_adapter_available()`: the LoRA adapter is optional —
    when absent, generation falls back to the base model rather than
    failing over to a cloud model. The review_queue's "auto" mode keeps
    its stricter "must have adapter" gate via `_adapter_available()`.
    """
    return shutil.which("mlx_lm") is not None


def _persona_adapter_available(sender_type: str | None) -> Path | None:
    """Return the path to a per-persona adapter, or None when not available.

    Phase 3 of per-persona adapters. The routing decision in
    `generate_draft` calls this with the inbound's `sender_type_hint`; a
    non-None return means the per-persona adapter is on disk and routing
    can use it instead of the global. NULL/unknown/empty sender_type
    returns None — we don't have a persona adapter for "unknown" and
    routing should fall through to the global in that case.
    """
    if not sender_type or sender_type == "unknown":
        return None
    from app.core.settings import get_persona_adapter_path

    path = get_persona_adapter_path(sender_type)
    if (path / "adapters.safetensors").exists():
        return path
    return None


def _persona_routing_enabled() -> bool:
    """True when ``personas.routing_enabled: true`` is set in the config.

    Default-off so existing installs upgrade through Phases 1+2 without
    any generation behavior change — the user opts in once Phase 2 has
    accumulated per-persona adapters they want to use.
    """
    try:
        from app.core.config import load_config

        raw = load_config() or {}
        if not isinstance(raw, dict):
            return False
        personas_cfg = raw.get("personas") or {}
        if not isinstance(personas_cfg, dict):
            return False
        return bool(personas_cfg.get("routing_enabled", False))
    except Exception:
        return False


def _compute_max_tokens(avg_reply_words: int | None, *, persona: dict[str, Any] | None = None, intent: str | None = None) -> int:
    """Compute max_tokens as a rough upper bound from avg_reply_words.

    Priority: mode-specific > intent-specific > global > default 300.
    """
    effective_words = avg_reply_words
    if persona:
        # 1. Mode-specific avg_reply_words (highest priority)
        mode_words = persona.get("_active_mode_config", {}).get("avg_reply_words")
        if mode_words is not None:
            effective_words = mode_words
        # 2. Intent-specific (only if mode didn't override)
        elif intent and intent != "general":
            intent_avg = persona.get("style", {}).get("intent_avg_words", {})
            if isinstance(intent_avg, dict) and intent in intent_avg:
                effective_words = intent_avg[intent]
        # 3. Global fallback
        if effective_words is None:
            effective_words = persona.get("style", {}).get("avg_reply_words")
    if effective_words is None:
        return 300
    return max(100, min(500, effective_words * 5))


def _strip_mlx_output(raw: str) -> str:
    """Extract just the generated text from mlx_lm generate output.

    mlx_lm wraps output like:
        ==========
        <generated text>
        ==========
        Prompt: N tokens, X tokens-per-sec
        Generation: N tokens, X tokens-per-sec
        Peak memory: X GB
    """
    # Split on the separator lines
    parts = re.split(r"={5,}", raw)
    # The generated text is the second segment (index 1) if separators exist
    if len(parts) >= 2:
        return parts[1].strip()
    # No separators — strip stats lines from the end as fallback
    lines = raw.strip().splitlines()
    clean = [
        line for line in lines
        if not re.match(r"^(Prompt:|Generation:|Peak memory:|Fetching)", line)
    ]
    return "\n".join(clean).strip()


def _call_local_model(
    prompt: str,
    *,
    max_tokens: int = 300,
    use_adapter: bool = True,
    adapter_path: Path | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
) -> str:
    """Run mlx_lm against the base model, optionally with a LoRA adapter.

    `adapter_path` overrides the global ADAPTER_PATH — used by Phase-3
    persona routing to point at `<models>/adapters/personas/<sender_type>/`
    instead of the global `<models>/adapters/latest/`. Falls back to
    ADAPTER_PATH when `use_adapter=True` and `adapter_path` is None
    (preserves the historical behavior).
    """
    # Prefer the warm server (no per-draft model reload) for the common case: the
    # global adapter (or base). It serves a single adapter loaded at startup, so a
    # per-persona adapter_path, or an explicit base request (use_adapter=False
    # while an adapter is loaded), must use the per-request subprocess below.
    if adapter_path is None and use_adapter:
        from app.core import model_server

        if model_server.is_enabled() and model_server.ensure_running():
            try:
                return model_server.complete(prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p)
            except Exception:
                logger.warning("warm model server call failed; falling back to subprocess", exc_info=True)

    cmd = [
        "mlx_lm",
        "generate",
        "--model",
        _get_base_model_id(),
    ]
    chosen_adapter = adapter_path if adapter_path is not None else (ADAPTER_PATH if use_adapter else None)
    if chosen_adapter is not None:
        cmd.extend(["--adapter-path", str(chosen_adapter)])
    cmd.extend(
        [
            "--prompt",
            prompt,
            "--max-tokens",
            str(max_tokens),
        ]
    )
    # Only pass sampling flags when configured — omitting them preserves
    # mlx_lm's own defaults (the historical behavior).
    if temperature is not None:
        cmd.extend(["--temp", str(temperature)])
    if top_p is not None:
        cmd.extend(["--top-p", str(top_p)])
    result = _run_subprocess(cmd, timeout=SUBPROCESS_TIMEOUT)
    if result.returncode != 0:
        raise RuntimeError(f"mlx_lm generate failed (exit {result.returncode}): {result.stderr.strip()}")
    return _strip_mlx_output(result.stdout)


def _local_draft_once(
    prompt: str,
    *,
    max_tokens: int,
    temperature: float | None,
    top_p: float | None,
    request: "DraftRequest",
    sender_type_hint: str | None,
) -> tuple[str, str]:
    """Produce one local-model draft, honoring the Phase-3 adapter precedence.

    Returns ``(draft, model_used)``. Factored out so both the single-draft
    path and multi-candidate generation share the exact same adapter routing.
    """
    persona_adapter_path: Path | None = None
    if request.use_adapter and _persona_routing_enabled():
        persona_adapter_path = _persona_adapter_available(sender_type_hint)
    if persona_adapter_path is not None:
        draft = _call_local_model(
            prompt, max_tokens=max_tokens, adapter_path=persona_adapter_path,
            temperature=temperature, top_p=top_p,
        )
        return draft, f"qwen2.5-1.5b-lora-{sender_type_hint}"
    with_adapter = request.use_adapter and _adapter_available()
    draft = _call_local_model(
        prompt, max_tokens=max_tokens, use_adapter=with_adapter,
        temperature=temperature, top_p=top_p,
    )
    return draft, ("qwen2.5-1.5b-lora" if with_adapter else "qwen2.5-1.5b-base")


def _generate_via_ollama(
    prompt: str,
    model: str = "mistral",
    base_url: str = "http://localhost:11434",
    *,
    num_predict: int = 400,
    temperature: float | None = None,
    top_p: float | None = None,
) -> str:
    """Generate via Ollama HTTP API."""
    import urllib.request

    # Preserve the historical 0.7 default when temperature isn't configured.
    options: dict[str, Any] = {"temperature": 0.7 if temperature is None else temperature, "num_predict": num_predict}
    if top_p is not None:
        options["top_p"] = top_p
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": options}).encode()
    req = urllib.request.Request(f"{base_url}/api/generate", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("response", "").strip()
    except Exception as exc:
        raise RuntimeError(f"Ollama generation failed: {exc}") from exc


def _run_subprocess(cmd: list[str], *, timeout: int = SUBPROCESS_TIMEOUT) -> subprocess.CompletedProcess[str]:
    """Run a subprocess with a hard timeout that kills the whole process group.

    `subprocess.run(timeout=...)` only SIGKILLs the direct child; if that child
    (e.g. the `claude` Node CLI or `mlx_lm`) spawned its own subprocesses that
    inherited the stdout/stderr pipes, the parent's read blocks waiting for EOF
    until *those* exit — so a single stalled generation can hang far past the
    timeout (observed: an 8-minute stall on a 120s timeout). Running in a new
    session and killing the process group on timeout releases the pipes.
    """
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            proc.kill()
        proc.communicate()
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def _call_claude_cli(prompt: str, *, max_tokens: int = 300) -> str:  # noqa: ARG001
    # Note: claude CLI --print does not support --max-tokens; use -p to pass prompt
    cmd = ["claude", "--print", "-p", prompt]
    result = _run_subprocess(cmd, timeout=SUBPROCESS_TIMEOUT)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(f"claude CLI failed (exit {result.returncode}): {stderr}")
    return result.stdout.strip()


def generate_draft(
    request: DraftRequest,
    *,
    database_url: str,
    configs_dir: Path,
) -> DraftResponse:
    # Strip quoted text from inbound before processing
    clean_inbound = strip_quoted_text(request.inbound_message)

    from app.core.text_utils import detect_language

    detected_lang = detect_language(clean_inbound)

    # Handle thread context for ongoing threads
    inbound_for_prompt = clean_inbound
    if _has_thread_context(clean_inbound):
        active_inbound, history = _extract_thread_parts(clean_inbound)
        inbound_for_prompt = _format_thread_context(active_inbound, history)

    # Open one shared DB connection for all metadata lookups (P1)
    db_path = resolve_sqlite_path(database_url)
    shared_conn = _connect(db_path)
    shared_conn.row_factory = sqlite3.Row
    try:

        # Look up prior reply to this sender for additional context (works for standalone emails too)
        user_name = get_user_name()
        if request.sender:
            prior_reply = _lookup_prior_reply_to_sender(request.sender, database_url, conn=shared_conn)
            if prior_reply:
                inbound_for_prompt += f"\n\n[PRIOR REPLY TO THIS SENDER]\n{user_name} previously wrote: {prior_reply}"

        # Infer account email from sender if not explicitly provided
        if request.account_email:
            account_emails = (request.account_email,)
        elif request.sender:
            inferred = get_account_for_sender(request.sender)
            account_emails = (inferred,) if inferred else ()
        else:
            account_emails = ()
        sender_type_hint = None
        sender_domain_hint = None
        if request.sender:
            sender_type_hint = classify_sender(request.sender)
            sender_domain_hint = extract_domain(request.sender)

        # Classify intent (multi-intent support)
        from app.core.intent import classify_intents_multi

        if request.intent_hint:
            detected_intent = request.intent_hint
            intent_hint_2 = None
        else:
            intents = classify_intents_multi(clean_inbound)
            detected_intent = intents[0]
            intent_hint_2 = intents[1] if len(intents) > 1 else None

        # E20: for very short inbound (<50 chars), fall back to sender-profile-based retrieval
        retrieval_query = clean_inbound
        if len(clean_inbound.strip()) < 50 and request.sender:
            # Augment query with sender email so retrieval finds past replies to this person
            retrieval_query = f"{clean_inbound} {request.sender}".strip()

        retrieval_response: RetrievalResponse = retrieve_context(
            RetrievalRequest(
                query=retrieval_query,
                scope="all",
                account_emails=account_emails,
                top_k_reply_pairs=request.top_k_reply_pairs,
                top_k_chunks=request.top_k_chunks,
                sender_type_hint=sender_type_hint,
                sender_domain_hint=sender_domain_hint,
                language_hint=detected_lang,
                intent_hint=detected_intent,
                intent_hint_2=intent_hint_2,
                thread_id=request.thread_id,
            ),
            database_url=database_url,
            configs_dir=configs_dir,
        )

        detected_mode = request.mode or retrieval_response.detected_mode
        reply_pairs = retrieval_response.reply_pairs

        cached_ids, exemplar_cache_hit, exemplar_cache_key = _get_cached_exemplar_ids(detected_intent, sender_type_hint, database_url=database_url)
        reply_pairs = _apply_cached_order(reply_pairs, cached_ids)

        selected_ids = _top_exemplar_source_ids(reply_pairs)
        # Only persist on a cache miss or when the selection actually changed —
        # otherwise every hit triggered a redundant DB write of the same row.
        if not exemplar_cache_hit or selected_ids != cached_ids[: len(selected_ids)]:
            _update_exemplar_cache(detected_intent, sender_type_hint, selected_ids, database_url=database_url)

        # Build score stats dict from retrieval response
        score_stats = None
        if retrieval_response.mean_score is not None:
            score_stats = {
                "max": retrieval_response.max_score,
                "mean": retrieval_response.mean_score,
                "stddev": retrieval_response.score_stddev,
            }
        confidence, confidence_reason = _score_confidence(reply_pairs, score_stats=score_stats)

        prompts = _load_prompts(configs_dir)
        persona = _load_persona(configs_dir)

        # Per-sender-type persona mode override
        _sender_type = sender_type_hint
        modes = persona.get("modes", {})
        if _sender_type and _sender_type in modes:
            mode_config = modes[_sender_type]
            persona["_active_mode_config"] = mode_config
            # Merge mode values into persona style, but never override custom_constraints
            style = persona.setdefault("style", {})
            for key in ("voice", "avg_reply_words", "greeting", "closing"):
                if key in mode_config:
                    style[key] = mode_config[key]
        else:
            persona["_active_mode_config"] = {}

        # Look up sender profile if sender provided
        sender_profile = None
        sender_context = None
        first_name = None
        if request.sender:
            sender_profile = lookup_sender_profile(request.sender, database_url, conn=shared_conn)
            if sender_profile:
                sender_context = _format_sender_context(sender_profile)
                first_name = first_name_from_display_name(sender_profile.get("display_name"))

        # Look up facts (user prefs, contact facts, project context)
        memory_facts = lookup_facts(
            sender=request.sender,
            inbound_text=clean_inbound,
            database_url=database_url,
            conn=shared_conn,
        )
    finally:
        shared_conn.close()

    prompt = assemble_prompt(
        inbound_message=inbound_for_prompt,
        reply_pairs=reply_pairs,
        persona=persona,
        prompts=prompts,
        detected_mode=detected_mode,
        audience_hint=request.audience_hint,
        tone_hint=request.tone_hint,
        sender_context=sender_context,
        language_hint=detected_lang,
        intent_hint=detected_intent,
        sender_type=sender_type_hint,
        first_name=first_name,
        memory_facts=memory_facts,
        score_stats=score_stats,
        subject=request.subject,
        user_prompt=request.user_prompt,
    )

    # Token budget check — greedy knapsack: calculate each exemplar cost once (P5)
    token_estimate = _estimate_tokens(prompt)
    if token_estimate > PROMPT_TOKEN_BUDGET and reply_pairs:
        # Build base prompt without any exemplars to get baseline cost
        base_prompt = assemble_prompt(
            inbound_message=inbound_for_prompt,
            reply_pairs=[],
            persona=persona,
            prompts=prompts,
            detected_mode=detected_mode,
            audience_hint=request.audience_hint,
            tone_hint=request.tone_hint,
            sender_context=sender_context,
            language_hint=detected_lang,
            intent_hint=detected_intent,
            sender_type=sender_type_hint,
            first_name=first_name,
            memory_facts=memory_facts,
            score_stats=score_stats,
            subject=request.subject,
            user_prompt=request.user_prompt,
        )
        budget = PROMPT_TOKEN_BUDGET - _estimate_tokens(base_prompt)
        used = 0
        trimmed_pairs = []
        # Trim by score (highest-relevance first) so the token budget keeps the
        # best exemplars. reply_pairs may have been reordered cache-first by
        # _apply_cached_order, which must not demote a high-score pair out of the
        # budget — the cache is for consistency, not selection.
        for rp in sorted(reply_pairs, key=lambda r: r.score, reverse=True):
            inbound_ex = (rp.inbound_text or "")[:EXEMPLAR_INBOUND_CHARS]
            reply_ex = strip_signature(rp.reply_text or "")[:EXEMPLAR_REPLY_CHARS]
            cost = _estimate_tokens(f"[EXAMPLE]\nInbound: {inbound_ex}\nYour reply: {reply_ex}\n---")
            if used + cost <= budget:
                trimmed_pairs.append(rp)
                used += cost
        removed = len(reply_pairs) - len(trimmed_pairs)
        if removed:
            logger.info("Prompt truncated: removed %d exemplars to fit token budget", removed)
            reply_pairs = trimmed_pairs
            prompt = assemble_prompt(
                inbound_message=inbound_for_prompt,
                reply_pairs=trimmed_pairs,
                persona=persona,
                prompts=prompts,
                detected_mode=detected_mode,
                audience_hint=request.audience_hint,
                tone_hint=request.tone_hint,
                sender_context=sender_context,
                language_hint=detected_lang,
                intent_hint=detected_intent,
                sender_type=sender_type_hint,
                first_name=first_name,
                memory_facts=memory_facts,
                score_stats=score_stats,
                subject=request.subject,
                user_prompt=request.user_prompt,
            )
        token_estimate = _estimate_tokens(prompt)

    precedent_used = [_precedent_summary(rp) for rp in reply_pairs]

    # Compute length-aware max_tokens (intent-specific if available)
    avg_reply_words = persona.get("style", {}).get("avg_reply_words")
    # Use intent-specific avg if available
    intent_avg = persona.get("style", {}).get("intent_avg_words", {})
    if isinstance(intent_avg, dict) and detected_intent in intent_avg:
        avg_reply_words = intent_avg[detected_intent]
    max_tokens = _compute_max_tokens(avg_reply_words, persona=persona, intent=detected_intent)
    # Decoding params (default None -> each backend keeps its current default).
    temperature, top_p = _resolve_decoding(detected_intent, confidence)

    # Greeting/closing resolved once — reused by candidate ranking and the
    # post-generation repair pass below.
    repair_greeting = _resolve_greeting(persona, sender_type_hint, first_name)
    repair_closing = _resolve_closing(persona, sender_type_hint)

    fallback_model = get_model_fallback()
    # An explicit backend_override pins the engine for this draft (used by the
    # cross-model comparison). "mlx" routes to the local path; anything else
    # forces that fallback model and disables the local path.
    use_local = request.use_local_model
    if request.backend_override:
        use_local = request.backend_override == "mlx"
        if request.backend_override != "mlx":
            fallback_model = request.backend_override
    candidates: list[dict[str, Any]] = []
    try:
        if use_local and _local_model_available():
            # Phase 3 routing precedence is encapsulated in _local_draft_once:
            #   1. per-persona adapter (routing on + caller wants it + trained)
            #   2. global "latest" adapter when one is trained
            #   3. base model otherwise
            # `model_used` is honest about which adapter actually ran.
            mc = _multi_candidate_config()
            if mc["enabled"]:
                # Generate a temperature spread, then keep the best-scoring draft.
                raw: list[tuple[str, str, float | None]] = []
                for t in mc["temperatures"]:
                    try:
                        d, mu = _local_draft_once(
                            prompt, max_tokens=max_tokens, temperature=t, top_p=top_p,
                            request=request, sender_type_hint=sender_type_hint,
                        )
                        raw.append((d, mu, t))
                    except Exception:
                        logger.warning("multi-candidate: one candidate failed", exc_info=True)
                if not raw:
                    raise RuntimeError("all draft candidates failed")
                candidates = _rank_candidates(
                    raw, target_words=avg_reply_words, greeting=repair_greeting, closing=repair_closing,
                )
                draft = candidates[0]["draft"]
                model_used = candidates[0]["model_used"]
            else:
                draft, model_used = _local_draft_once(
                    prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p,
                    request=request, sender_type_hint=sender_type_hint,
                )
        elif fallback_model == "ollama":
            from app.core.config import get_ollama_config

            ollama_cfg = get_ollama_config()
            ollama_model = ollama_cfg.get("model", "mistral")
            ollama_url = ollama_cfg.get("base_url", "http://localhost:11434")
            draft = _generate_via_ollama(
                prompt, model=ollama_model, base_url=ollama_url, num_predict=max_tokens,
                temperature=temperature, top_p=top_p,
            )
            model_used = f"ollama:{ollama_model}"
        elif fallback_model == "claude":
            draft = _call_claude_cli(prompt, max_tokens=max_tokens)
            model_used = "claude"
        elif fallback_model == "none":
            # Fallback explicitly disabled: no local model and no cloud call.
            draft = "[no model available: local model unavailable and fallback disabled]"
            model_used = "none"
        else:
            draft = _call_claude_cli(prompt, max_tokens=max_tokens)
            model_used = fallback_model
    except Exception as exc:
        draft = f"[draft generation failed: {exc}]"
        model_used = "error"

    # Retry on empty or signature-only local model output
    empty_output_retried = False
    _draft_stripped = strip_signature(draft).strip()
    non_ws = len(draft.replace(" ", "").replace("\n", "").replace("\t", ""))
    _looks_like_only_signature = len(_draft_stripped) < 15 and non_ws > 0
    if (non_ws < 10 or _looks_like_only_signature) and model_used not in ("error", "claude"):
        logger.warning("Local model returned empty output, falling back to Claude")
        if fallback_model != "none":
            try:
                draft = _call_claude_cli(prompt, max_tokens=max_tokens)
                model_used = "claude"
                empty_output_retried = True
            except Exception as fallback_exc:
                raise ValueError("Draft generation returned empty output") from fallback_exc
        else:
            raise ValueError("Draft generation returned empty output")

        # Increment counter in pipeline log
        try:
            log_path = Path(__file__).resolve().parents[1] / "var" / "pipeline_last_run.json"
            if log_path.exists():
                log_data = json.loads(log_path.read_text(encoding="utf-8"))
                log_data["local_model_empty_retries"] = log_data.get("local_model_empty_retries", 0) + 1
                log_path.write_text(json.dumps(log_data, indent=2))
        except Exception:
            logger.warning("Failed to update pipeline log", exc_info=True)

    # Post-generation repair: always annotate length; optionally enforce the
    # persona greeting/closing and strip a trailing duplicate signature (both
    # default-off — see _get_repair_config).
    draft, repairs, length_flag = _repair_draft(
        draft,
        greeting=repair_greeting,
        closing=repair_closing,
        target_words=avg_reply_words,
        config=_get_repair_config(),
    )

    # Generate subject line
    suggested_subject = generate_subject(request.inbound_message, draft, database_url, configs_dir)

    # Capture the draft event (exemplars/intent/sender_type/confidence the
    # draft was produced with) for the nightly's training signal. Fault-
    # isolated: never affects the returned draft. Skipped for forced-backend
    # (benchmark/comparison) drafts — they're not real user drafts and would
    # pollute both the training signal and the "drafting with" status derived
    # from draft_events.model_used.
    if request.backend_override is None:
        _log_draft_event(
            database_url,
            inbound_text=request.inbound_message,
            draft=draft,
            account_email=request.account_email,
            sender=request.sender,
            sender_type=sender_type_hint,
            detected_mode=detected_mode,
            intent=detected_intent,
            confidence=confidence,
            confidence_reason=confidence_reason,
            model_used=model_used,
            retrieval_method=retrieval_response.retrieval_method,
            exemplar_ids=selected_ids,
            length_flag=length_flag,
        )

    return DraftResponse(
        draft=draft,
        detected_mode=detected_mode,
        precedent_used=precedent_used,
        retrieval_method=retrieval_response.retrieval_method,
        confidence=confidence,
        confidence_reason=confidence_reason,
        model_used=model_used,
        sender_profile=sender_profile,
        suggested_subject=suggested_subject,
        token_estimate=token_estimate,
        empty_output_retried=empty_output_retried,
        exemplar_cache_hit=exemplar_cache_hit,
        exemplar_cache_key=exemplar_cache_key,
        length_flag=length_flag,
        repairs=repairs,
        candidates=candidates,
    )
