"""Rule-based fact extractor for notes.

Parses note text for patterns like 'prefers X', 'always CC x@y.z',
'hates X', 'uses X timezone', 'meeting on X days', 'sign off with X', etc.

Returns a list of candidate facts with type (contact/project/user_pref),
key, fact text, and confidence score. Deduplication against the DB is
handled separately; similar existing facts are merged on save.
"""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path

# ── Rule definition ──────────────────────────────────────────────────────────

@dataclass
class _Rule:
    pattern: re.Pattern
    fact_type: str
    template: str
    confidence: float
    claims_span: bool = False   # marks span so skip_claimed rules won't also fire here
    skip_claimed: bool = False  # skip if span overlaps a claimed span
    check_negation: bool = True  # apply negation detection before accepting match


# ── Negation detection ───────────────────────────────────────────────────────

_NEGATION_RE = re.compile(
    r"\b(?:not|don'?t|doesn'?t|didn'?t|never|no\s+longer|won'?t|cannot|can'?t)"
    r"\s*(?:\w+\s*){0,2}$",
    re.I,
)


def _is_negated(text: str, match_start: int) -> bool:
    """Return True if the match position is preceded by a negation word."""
    lookbehind = text[max(0, match_start - 60) : match_start]
    return bool(_NEGATION_RE.search(lookbehind))


# ── Project key extraction ───────────────────────────────────────────────────

_PROJECT_RE = re.compile(
    # "project Alpha" → group 1, or "Alpha project" → group 2 (uppercase required to avoid "for project")
    r"\bproject\s+([A-Za-z0-9_-]{2,30})\b"
    r"|\b([A-Z][A-Za-z0-9_-]{1,29})\s+project\b",
)


def _extract_project_key(note: str, project_name: str | None) -> str:
    if project_name:
        return project_name.lower().strip()
    m = _PROJECT_RE.search(note)
    if m:
        return (m.group(1) or m.group(2)).lower()
    return "default"


# ── Rules ────────────────────────────────────────────────────────────────────
# Order matters: specific patterns before generic ones.
# claims_span=True  → this rule "owns" the match span for subsequent skip_claimed rules.
# skip_claimed=True → skip if the match span overlaps any claimed span.

_RULES: list[_Rule] = [
    # Specific "prefers short/brief replies" — claims span to suppress generic match
    _Rule(
        re.compile(r"\bprefers?\s+(?:short|brief|concise)\s+(?:replies?|emails?|responses?|messages?)", re.I),
        "contact", "Prefers short replies", 0.8, claims_span=True,
    ),
    # Prefers bullet points
    _Rule(
        re.compile(r"\bprefers?\s+(?:bullet[\s-]?points?|numbered\s+lists?)", re.I),
        "contact", "Prefers bullet points", 0.8, claims_span=True,
    ),
    # Prefers formal/informal/casual tone
    _Rule(
        re.compile(r"\bprefers?\s+(formal|informal|casual)\s+(?:tone|style|communication|language)", re.I),
        "contact", "Prefers {0} communication style", 0.8, claims_span=True,
    ),
    # Hates / dislikes — inherently negative, skip negation check
    _Rule(
        re.compile(r"\b(?:hates?|dislikes?)\s+([^.,;!?\n]{3,60})", re.I),
        "contact", "Dislikes {0}", 0.6, check_negation=False,
    ),
    # Don't / avoid — inherently negative
    _Rule(
        re.compile(r"\bdon'?t\s+(?:like|use|send|include)\s+([^.,;!?\n]{3,60})", re.I),
        "contact", "Avoid: {0}", 0.6, check_negation=False,
    ),
    # Always CC email@domain
    _Rule(
        re.compile(r"\balways\s+cc\s+([\w.+%-]+@[\w.-]+\.[a-z]{2,})", re.I),
        "contact", "Always CC {0}", 0.9,
    ),
    # CC his/her/their assistant [name]
    _Rule(
        re.compile(
            r"\bcc\s+(?:his|her|their|the)\s+assistant\s+([A-Za-z][a-zA-Z'-]+(?:\s+[A-Za-z][a-zA-Z'-]+)?)",
            re.I,
        ),
        "contact", "CC assistant: {0}", 0.8,
    ),
    # Timezone abbreviations: UTC+5, GMT-8, EST, PST, etc.
    _Rule(
        re.compile(
            r"\b(UTC[+-]\d+(?::\d+)?|GMT[+-]\d+(?::\d+)?|EST|EDT|CST|CDT|MST|MDT|PST|PDT|CET|CEST|IST|JST|AEST|AEDT|NZST)\b"
        ),
        "contact", "Uses {0} timezone", 0.9,
    ),
    # "uses X timezone" / "in X timezone" (IANA-style: Region/City)
    _Rule(
        re.compile(r"\b(?:uses?\s+)?([A-Z][a-z]+/[A-Z][A-Za-z_]+)\s+(?:time\s*zone|timezone|tz)\b", re.I),
        "contact", "Uses {0} timezone", 0.9,
    ),
    # Meetings on weekdays
    _Rule(
        re.compile(
            r"\bmeetings?\s+(?:on|every)\s+((?:(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*)"
            r"(?:(?:,\s*|\s+and\s+)(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*)*)",
            re.I,
        ),
        "contact", "Meetings on {0}", 0.8,
    ),
    # Available on weekdays
    _Rule(
        re.compile(
            r"\bavailable\s+(?:on|every)\s+((?:(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*)"
            r"(?:(?:,\s*|\s+and\s+)(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*)*)",
            re.I,
        ),
        "contact", "Available on {0}", 0.8,
    ),
    # Signs off with / signs off as
    _Rule(
        re.compile(r"\bsigns?\s+off\s+(?:with|as)\s+[\"']?([^\"'.,;!?\n]{2,40})[\"']?", re.I),
        "user_pref", "Sign off: {0}", 0.9,
    ),
    # Signature: X
    _Rule(
        re.compile(r"\bsignature[:\s]+[\"']?([^\"'.,;!?\n]{2,40})[\"']?", re.I),
        "user_pref", "Sign off: {0}", 0.9,
    ),
    # Use "X" as sign-off / sign off
    _Rule(
        re.compile(r'\buse\s+["\']([^"\']{2,40})["\']?\s+(?:as\s+(?:the\s+)?)?sign[\s-]off', re.I),
        "user_pref", "Sign off: {0}", 0.9,
    ),
    # Responds within N hours/days
    _Rule(
        re.compile(r"\bresponds?\s+(?:within|in)\s+(\d+\s+(?:hours?|days?|minutes?|business\s+days?))", re.I),
        "contact", "Responds within {0}", 0.8,
    ),
    # Writes in <language>
    _Rule(
        re.compile(
            r"\bwrites?\s+(?:only\s+)?in\s+(English|Spanish|French|German|Chinese|Japanese"
            r"|Portuguese|Italian|Dutch|Russian|Arabic|Hindi|Korean|Polish|Swedish|Norwegian)\b",
            re.I,
        ),
        "contact", "Writes in {0}", 0.8,
    ),
    # Speaks <language>
    _Rule(
        re.compile(
            r"\bspeaks?\s+(English|Spanish|French|German|Chinese|Japanese"
            r"|Portuguese|Italian|Dutch|Russian|Arabic|Hindi|Korean|Polish|Swedish|Norwegian)\b",
            re.I,
        ),
        "contact", "Speaks {0}", 0.8,
    ),
    # Always wants / always needs
    _Rule(
        re.compile(r"\balways\s+(?:wants?|needs?|requires?)\s+([^.,;!?\n]{3,60})", re.I),
        "contact", "Always wants {0}", 0.8,
    ),
    # Never CC / never include / never send — inherently negative
    _Rule(
        re.compile(r"\bnever\s+(?:cc|bcc|include|send|reply\s+to)\s+([^.,;!?\n]{3,60})", re.I),
        "contact", "Never {0}", 0.8, check_negation=False,
    ),
    # Deadline: <date/description>
    _Rule(
        re.compile(r"\bdeadline[:\s]+([^.,;!?\n]{3,50})", re.I),
        "project", "Deadline: {0}", 0.9,
    ),
    # Budget: $X
    _Rule(
        re.compile(r"\bbudget[:\s]+(\$?[\d,]+(?:\s*[kKmMbB])?)", re.I),
        "project", "Budget: {0}", 0.9,
    ),

    # ── New patterns ─────────────────────────────────────────────────────────

    # Reports to [name/email]
    _Rule(
        re.compile(r"\breports\s+to\s+([^.,;!?\n]{2,50})", re.I),
        "contact", "Reports to {0}", 0.9,
    ),
    # Title/role: X
    _Rule(
        re.compile(r"\b(?:title|role)[:\s]+([^.,;!?\n]{2,50})", re.I),
        "contact", "Title: {0}", 0.8,
    ),
    # Works at / company: X
    _Rule(
        re.compile(r"\b(?:works?\s+at|company[:\s]+)\s*([^.,;!?\n]{2,40})", re.I),
        "contact", "Company: {0}", 0.8,
    ),
    # Phone: +43... / mobile / cell / tel
    _Rule(
        re.compile(r"\b(?:phone|tel|mobile|cell)[:\s]+([+\d\s()\-]{7,20})", re.I),
        "contact", "Phone: {0}", 0.9,
    ),
    # Based in / located in / location: X
    _Rule(
        re.compile(r"\b(?:based\s+in|located\s+in|location[:\s]+)\s*([^.,;!?\n]{2,40})", re.I),
        "contact", "Location: {0}", 0.8,
    ),
    # Preferred name: X / goes by X / call them/him/her X
    _Rule(
        re.compile(
            r"\b(?:preferred\s+name[:\s]+|goes\s+by\s+|call\s+(?:them|him|her)\s+)"
            r"([^.,;!?\n]{2,30})",
            re.I,
        ),
        "contact", "Preferred name: {0}", 0.9,
    ),
    # Don't email after Xpm / OOO on X / unavailable on X — inherently negative
    _Rule(
        re.compile(
            r"\b(?:don'?t\s+email\s+after|ooo\s+on|unavailable\s+on|out\s+of\s+office\s+on)\s+"
            r"([^.,;!?\n]{2,40})",
            re.I,
        ),
        "contact", "Unavailable: {0}", 0.8, check_negation=False,
    ),
    # Decision maker / gatekeeper — pattern handles "not the decision maker" inline
    _Rule(
        re.compile(r"\b((?:not\s+(?:the\s+)?)?decision\s+maker|gatekeeper|key\s+contact)\b", re.I),
        "contact", "Role: {0}", 0.8, check_negation=False,
    ),
    # Referred by / introduced by
    _Rule(
        re.compile(r"\b(?:referred\s+by|introduced\s+by|referral\s+from)\s+([^.,;!?\n]{2,40})", re.I),
        "contact", "Referred by {0}", 0.9,
    ),
    # Account manager / key account / VIP
    _Rule(
        re.compile(r"\b(account\s+manager|key\s+account|vip\s+(?:client|contact)|high[\s-]value)\b", re.I),
        "contact", "Tag: {0}", 0.8,
    ),
    # Billing email: X / invoice to X
    _Rule(
        re.compile(r"\b(?:billing\s+email[:\s]+|invoice\s+to\s+)([\w.+%-]+@[\w.-]+\.[a-z]{2,})", re.I),
        "contact", "Billing email: {0}", 0.9,
    ),
    # Renewal date: X / contract expires X
    _Rule(
        re.compile(r"\b(?:renewal\s+date[:\s]+|contract\s+expires?\s+)([^.,;!?\n]{3,40})", re.I),
        "project", "Renewal date: {0}", 0.9,
    ),
    # Stakeholder: X / involved: X
    _Rule(
        re.compile(r"\b(?:stakeholders?[:\s]+|involved[:\s]+)([^.,;!?\n]{2,50})", re.I),
        "project", "Stakeholder: {0}", 0.8,
    ),

    # Generic prefers X — MUST be last; skip if span already claimed by specific prefers
    _Rule(
        re.compile(r"\bprefers?\s+([^.,;!?\n]{3,60})", re.I),
        "contact", "Prefers {0}", 0.6, skip_claimed=True,
    ),
]


# ── Core extraction ──────────────────────────────────────────────────────────

def extract_facts(
    note: str,
    sender_email: str | None = None,
    project_name: str | None = None,
) -> list[dict]:
    """Extract structured facts from a note string.

    Args:
        note: The note text to parse.
        sender_email: Optional email used as the key for contact-type facts.
        project_name: Optional project name override for project-type facts.

    Returns:
        List of dicts with keys: type, key, fact, confidence.
    """
    if not note or not note.strip():
        return []

    proj_key = _extract_project_key(note, project_name)
    results: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    claimed_spans: list[tuple[int, int]] = []

    for rule in _RULES:
        for m in rule.pattern.finditer(note):
            # Negation check
            if rule.check_negation and _is_negated(note, m.start()):
                continue

            # Skip if this span overlaps any span claimed by a higher-priority rule
            if rule.skip_claimed and any(
                m.start() < e and m.end() > s for s, e in claimed_spans
            ):
                continue

            # Claim this span so lower-priority generic rules skip it
            if rule.claims_span:
                claimed_spans.append((m.start(), m.end()))

            # Build fact text
            if "{0}" in rule.template and m.lastindex:
                captured = m.group(1).strip().rstrip(".,;!")
                fact_text = rule.template.replace("{0}", captured)
                # Downgrade confidence for very long captures (likely noisy)
                confidence = rule.confidence if len(captured) <= 40 else 0.4
            else:
                fact_text = rule.template
                confidence = rule.confidence

            # Determine key
            if rule.fact_type == "contact":
                key = sender_email.lower().strip() if sender_email else "unknown"
            elif rule.fact_type == "project":
                key = proj_key
            else:
                key = "default"

            dedup = (rule.fact_type, key, fact_text.lower())
            if dedup in seen:
                continue
            seen.add(dedup)

            results.append({
                "type": rule.fact_type,
                "key": key,
                "fact": fact_text,
                "confidence": confidence,
            })

    return results


# ── LLM fallback ─────────────────────────────────────────────────────────────

def extract_facts_llm(note: str, sender_email: str | None = None) -> list[dict]:
    """Call Claude CLI to extract facts from unstructured notes.

    Only intended as a fallback when rule-based extraction returns nothing.
    Returns a list of fact dicts (type, key, fact, confidence).
    """
    prompt = (
        "Extract structured facts from the note below about a contact or project.\n"
        "Return ONLY a JSON array of objects, each with keys:\n"
        '  "type"  → one of: contact, project, user_pref\n'
        '  "key"   → email address for contact facts, project name for project facts, '
        '"default" for user_pref\n'
        '  "fact"  → short descriptive string (e.g. "Prefers short replies")\n\n'
        f"Sender email: {sender_email or 'unknown'}\n"
        f"Note: {note}\n\n"
        "JSON array:"
    )
    try:
        result = subprocess.run(
            ["claude", "--print", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return []
        text = result.stdout.strip()
        json_match = re.search(r"\[.*\]", text, re.DOTALL)
        if not json_match:
            return []
        items = json.loads(json_match.group())
        facts: list[dict] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            f_type = str(item.get("type", "contact"))
            f_key = str(item.get("key") or sender_email or "unknown")
            f_fact = str(item.get("fact", "")).strip()
            if f_type not in ("contact", "project", "user_pref") or not f_fact:
                continue
            facts.append({"type": f_type, "key": f_key, "fact": f_fact, "confidence": 0.5})
        return facts
    except Exception:
        return []


# ── DB helpers ───────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _keyword_overlap(a: str, b: str) -> float:
    """Jaccard similarity on lowercase word tokens."""
    wa = set(re.findall(r"\w+", a.lower()))
    wb = set(re.findall(r"\w+", b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def filter_new_facts(candidates: list[dict], db_path: Path) -> list[dict]:
    """Drop candidates whose normalized fact text already exists for the same type+key."""
    if not candidates:
        return []
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT type, key, fact FROM memory").fetchall()
    finally:
        conn.close()

    existing = {(r[0], r[1], _normalize(r[2])) for r in rows}
    return [c for c in candidates if (c["type"], c["key"], _normalize(c["fact"])) not in existing]


def save_facts(facts: list[dict], db_path: Path) -> list[dict]:
    """Upsert facts into the memory table; return saved rows (with id).

    If a fact of the same type+key with sufficiently similar text already
    exists (keyword overlap ≥ 0.5), the existing row is updated in place
    rather than creating a duplicate entry.
    """
    if not facts:
        return []

    saved: list[dict] = []
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        for f in facts:
            try:
                confidence = f.get("confidence", 0.8)

                # Look for a similar (but not identical) existing fact to merge into
                existing_rows = conn.execute(
                    "SELECT id, fact FROM memory WHERE type = ? AND key = ?",
                    (f["type"], f["key"]),
                ).fetchall()

                similar_id: int | None = None
                for row in existing_rows:
                    if (
                        _normalize(f["fact"]) != _normalize(row["fact"])
                        and _keyword_overlap(f["fact"], row["fact"]) >= 0.5
                    ):
                        similar_id = row["id"]
                        break

                if similar_id is not None:
                    conn.execute(
                        """
                        UPDATE memory
                        SET fact = ?, confidence = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (f["fact"], confidence, similar_id),
                    )
                    conn.commit()
                    row = conn.execute(
                        "SELECT id, type, key, fact, confidence FROM memory WHERE id = ?",
                        (similar_id,),
                    ).fetchone()
                else:
                    conn.execute(
                        """
                        INSERT INTO memory (type, key, fact, confidence, tags, updated_at)
                        VALUES (?, ?, ?, ?, '[]', CURRENT_TIMESTAMP)
                        ON CONFLICT(type, key, fact) DO UPDATE SET
                            confidence = excluded.confidence,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (f["type"], f["key"], f["fact"], confidence),
                    )
                    conn.commit()
                    row = conn.execute(
                        "SELECT id, type, key, fact, confidence FROM memory "
                        "WHERE type = ? AND key = ? AND fact = ?",
                        (f["type"], f["key"], f["fact"]),
                    ).fetchone()

                if row:
                    saved.append({
                        "id": row["id"],
                        "type": row["type"],
                        "key": row["key"],
                        "fact": row["fact"],
                        "confidence": row["confidence"],
                    })
            except Exception:
                pass
    finally:
        conn.close()

    return saved


def extract_and_save(
    note: str,
    db_path: Path,
    sender_email: str | None = None,
    project_name: str | None = None,
    use_llm: bool = False,
) -> list[dict]:
    """Convenience wrapper: extract → deduplicate → save → return saved facts.

    Args:
        note: The note text to parse.
        db_path: Path to the SQLite database.
        sender_email: Optional email key for contact facts.
        project_name: Optional project name key for project facts.
        use_llm: If True and rule extraction finds nothing, fall back to LLM extraction.
    """
    candidates = extract_facts(note, sender_email=sender_email, project_name=project_name)

    if use_llm and len(candidates) == 0 and len(note.strip()) > 30:
        candidates = extract_facts_llm(note, sender_email=sender_email)

    new_facts = filter_new_facts(candidates, db_path)
    return save_facts(new_facts, db_path)
