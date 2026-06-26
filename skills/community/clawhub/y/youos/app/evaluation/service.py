"""Evaluation service — rule-based scoring for YouOS benchmark cases."""

from __future__ import annotations

import json
import logging
import sqlite3
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class EvalRequest:
    case_key: str | None = None  # run specific case; None = run all
    config_tag: str = "default"  # label for this run set


@dataclass
class CaseResult:
    case_key: str
    category: str
    prompt_text: str
    draft: str
    detected_mode: str
    confidence: str
    precedent_count: int
    scores: dict[str, Any]
    pass_fail: str  # "pass" | "fail" | "warn"
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvalSuiteResult:
    config_tag: str
    total_cases: int
    passed: int
    warned: int
    failed: int
    case_results: list[CaseResult]
    run_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            **{k: v for k, v in asdict(self).items() if k != "case_results"},
            "case_results": [cr.to_dict() for cr in self.case_results],
        }


# -- Scoring helpers (deterministic, rule-based) ──────────────────────


def score_keyword_hit_rate(draft: str, keywords: list[str]) -> float:
    if not keywords:
        return 1.0
    draft_lower = draft.lower()
    hits = sum(1 for kw in keywords if kw.lower() in draft_lower)
    return hits / len(keywords)


def score_brevity(word_count: int, max_words: int | None) -> str:
    if max_words is None:
        return "pass"
    if word_count <= max_words:
        return "pass"
    if word_count <= max_words * 1.1:
        return "warn"
    if word_count <= max_words * 1.5:
        return "warn"
    return "fail"


def score_mode_match(detected_mode: str, expected_mode: str) -> bool:
    return detected_mode.lower() == expected_mode.lower()


def confidence_to_score(confidence: str) -> float:
    return {"high": 1.0, "medium": 0.5, "low": 0.0}.get(confidence.lower(), 0.0)


def compute_pass_fail(
    keyword_hit_rate: float,
    brevity_fit: str,
    mode_match: bool,
) -> str:
    if brevity_fit == "fail":
        return "fail"
    if not mode_match:
        return "fail"
    if keyword_hit_rate < 0.5:
        return "fail"
    if brevity_fit == "warn" or keyword_hit_rate < 0.8:
        return "warn"
    return "pass"


# -- Case evaluation ──────────────────────────────────────────────────


def evaluate_case(
    case: dict[str, Any],
    draft: str,
    detected_mode: str,
    confidence: str,
    precedent_count: int,
    *,
    reference_reply: str | None = None,
    embed_fn: Any = None,
) -> CaseResult:
    expected = case.get("expected_properties", {})
    if isinstance(expected, str):
        expected = json.loads(expected)

    keywords = expected.get("should_contain_keywords", [])
    max_words = expected.get("max_words")
    expected_mode = expected.get("mode", "")

    word_count = len(draft.split())
    kw_rate = score_keyword_hit_rate(draft, keywords)
    brevity = score_brevity(word_count, max_words)
    mode_ok = score_mode_match(detected_mode, expected_mode)
    conf_score = confidence_to_score(confidence)

    pf = compute_pass_fail(kw_rate, brevity, mode_ok)

    scores = {
        "keyword_hit_rate": round(kw_rate, 2),
        "brevity_fit": brevity,
        "mode_match": mode_ok,
        "confidence_score": conf_score,
        "word_count": word_count,
        "max_words": max_words,
    }

    # Voice-match (additive, never affects pass/fail): only when the case carries
    # the user's real reply as a reference. This is what makes a cross-model
    # comparison meaningful — see app/evaluation/voice_match.py.
    if reference_reply:
        from app.evaluation.voice_match import voice_match_score

        scores["voice_match"] = voice_match_score(draft, reference_reply, embed_fn=embed_fn)

    return CaseResult(
        case_key=case["case_key"],
        category=case["category"],
        prompt_text=case["prompt_text"],
        draft=draft,
        detected_mode=detected_mode,
        confidence=confidence,
        precedent_count=precedent_count,
        scores=scores,
        pass_fail=pf,
        notes=case.get("notes", ""),
    )


# -- Persistence ──────────────────────────────────────────────────────


def persist_case_result(
    conn: sqlite3.Connection,
    case_result: CaseResult,
    config_tag: str,
    benchmark_case_id: int | None,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    run_key = f"{config_tag}_{case_result.case_key}_{uuid.uuid4().hex[:8]}"
    conn.execute(
        """
        INSERT INTO eval_runs
            (run_key, benchmark_case_id, config_snapshot_json,
             retrieval_summary_json, generation_output, score_json,
             status, started_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_key,
            benchmark_case_id,
            json.dumps({"config_tag": config_tag}),
            json.dumps({"precedent_count": case_result.precedent_count}),
            case_result.draft,
            json.dumps(case_result.scores),
            case_result.pass_fail,
            now,
            now,
        ),
    )


# -- Suite runner ─────────────────────────────────────────────────────


def _golden_path() -> Path:
    return Path(__file__).resolve().parents[2] / "configs" / "benchmarks" / "golden.yaml"


def seed_benchmark_cases_from_golden(conn: sqlite3.Connection, golden_path: Path | None = None) -> int:
    """Create + seed the benchmark_cases table from configs/benchmarks/golden.yaml.

    Returns the number of cases inserted. Idempotent (INSERT OR IGNORE on the
    unique case_key). This lets eval + autoresearch run on a fresh instance that
    was never explicitly seeded, instead of crashing on a missing/empty table.
    """
    import yaml

    path = golden_path or _golden_path()
    if not path.exists():
        return 0
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    cases = data.get("cases", [])

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS benchmark_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_key TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            prompt_text TEXT NOT NULL,
            expected_properties_json TEXT NOT NULL DEFAULT '{}',
            reference_reply TEXT,
            notes TEXT,
            created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    inserted = 0
    for case in cases:
        key = case.get("id")
        prompt = case.get("inbound")
        if not key or not prompt:
            continue
        # Map golden.yaml fields to the expected_properties shape evaluate_case reads.
        expected = {
            "should_contain_keywords": case.get("expected_keywords", []),
            "max_words": case.get("max_words"),
            "mode": case.get("expected_mode", ""),
        }
        # A golden case may carry the user's real reply (or a curated ideal one)
        # as a voice-match reference; `reference_reply` and `expected_reply` are
        # both accepted. Absent → NULL, and voice-match is simply skipped.
        reference_reply = case.get("reference_reply") or case.get("expected_reply")
        cur = conn.execute(
            """INSERT OR IGNORE INTO benchmark_cases
               (case_key, category, prompt_text, expected_properties_json, reference_reply, notes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                key,
                case.get("expected_mode") or "general",
                prompt,
                json.dumps(expected),
                reference_reply,
                case.get("notes", ""),
            ),
        )
        inserted += cur.rowcount
    conn.commit()
    return inserted


def load_benchmark_cases(conn: sqlite3.Connection, case_key: str | None = None) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    # Auto-seed from golden.yaml on a fresh/empty instance so eval and the
    # autoresearch loop don't crash on a missing or unseeded benchmark_cases table.
    try:
        count = conn.execute("SELECT COUNT(*) FROM benchmark_cases").fetchone()[0]
    except sqlite3.OperationalError:
        count = 0
    if count == 0:
        seed_benchmark_cases_from_golden(conn)
    if case_key:
        rows = conn.execute("SELECT * FROM benchmark_cases WHERE case_key = ?", (case_key,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM benchmark_cases").fetchall()
    return [dict(r) for r in rows]


def run_eval_suite(
    request: EvalRequest,
    *,
    generate_fn: Any,
    database_url: str,
    configs_dir: Path,
    persist: bool = True,
    embed_fn: Any = None,
) -> EvalSuiteResult:
    from app.db.bootstrap import connect, resolve_sqlite_path

    db_path = resolve_sqlite_path(database_url)
    conn = connect(db_path)
    try:
        cases = load_benchmark_cases(conn, request.case_key)
        case_results: list[CaseResult] = []

        for case in cases:
            expected = case.get("expected_properties_json", "{}")
            if isinstance(expected, str):
                expected_props = json.loads(expected)
            else:
                expected_props = expected

            # Build a dict with parsed expected_properties for scoring
            eval_case = {
                "case_key": case["case_key"],
                "category": case["category"],
                "prompt_text": case["prompt_text"],
                "expected_properties": expected_props,
                "notes": case.get("notes", ""),
            }

            # Call generation. Tolerate per-case failures (e.g. a generation
            # timeout) so one bad case scores as a fail instead of aborting the
            # whole suite — important for the long autoresearch loop.
            try:
                draft_response = generate_fn(
                    case["prompt_text"],
                    database_url=database_url,
                    configs_dir=configs_dir,
                )
            except Exception as exc:
                logger.warning("Eval generation failed for case %s: %s", case.get("case_key"), exc)
                draft_response = {
                    "draft": "",
                    "detected_mode": "",
                    "confidence": "low",
                    "precedent_count": 0,
                }

            cr = evaluate_case(
                case=eval_case,
                draft=draft_response["draft"],
                detected_mode=draft_response["detected_mode"],
                confidence=draft_response["confidence"],
                precedent_count=draft_response["precedent_count"],
                reference_reply=case.get("reference_reply"),
                embed_fn=embed_fn,
            )
            case_results.append(cr)

            if persist:
                persist_case_result(
                    conn,
                    cr,
                    request.config_tag,
                    case.get("id"),
                )
                # Commit each case so we don't hold the WAL write lock across the
                # whole suite. A single uncommitted transaction spanning every
                # case kept the write lock the entire time, so each per-draft
                # exemplar-cache write blocked for the busy_timeout and then
                # failed with 'database is locked' — and no results were visible
                # until the suite ended.
                conn.commit()
    finally:
        conn.close()

    passed = sum(1 for cr in case_results if cr.pass_fail == "pass")
    warned = sum(1 for cr in case_results if cr.pass_fail == "warn")
    failed = sum(1 for cr in case_results if cr.pass_fail == "fail")

    return EvalSuiteResult(
        config_tag=request.config_tag,
        total_cases=len(case_results),
        passed=passed,
        warned=warned,
        failed=failed,
        case_results=case_results,
        run_at=datetime.now(timezone.utc).isoformat(),
    )
