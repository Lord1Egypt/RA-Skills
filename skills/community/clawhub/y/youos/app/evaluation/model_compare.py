"""Cross-model comparison — how the backends stack up on *your* mail.

YouOS can draft with a local Qwen fine-tuned on your sent mail, an Ollama model,
or Claude. The honest way to compare them isn't vibes: draft the *same* messages
under each backend and score every draft against the reply you actually sent
(voice-match, see ``voice_match.py``), plus length and latency.

The key subtlety: a frontier cloud model usually writes a *better email*, but the
question that decides whether the privacy/cost trade is worth it is whether it
sounds **more like you** than your own fine-tuned local model. This module
answers that with numbers.

Honesty guards:
  * Cases are real ``reply_pairs`` (inbound → the reply you actually wrote), so the
    reference is ground truth, not a curated ideal.
  * Each backend is *pinned* via ``DraftRequest.backend_override`` so we know which
    engine ran — and we flag any case where generation silently fell back to
    another backend (e.g. an empty local draft retried on Claude), so a fallback
    can't masquerade as the pinned model's score.
"""

from __future__ import annotations

import shutil
import socket
import sqlite3
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from app.evaluation.voice_match import voice_match_score

BACKENDS = ("mlx", "ollama", "claude")


@dataclass
class BackendScore:
    backend: str
    n: int
    voice_match: float
    semantic_similarity: float | None
    lexical_overlap: float
    style_similarity: float
    length_ratio: float
    avg_words: float
    fallback_count: int
    error_count: int
    avg_latency_s: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ComparisonResult:
    backends: list[str]
    n_cases: int
    scores: list[BackendScore]
    cases: list[dict[str, Any]]
    semantic: bool
    run_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "backends": self.backends,
            "n_cases": self.n_cases,
            "semantic": self.semantic,
            "run_at": self.run_at,
            "scores": [s.to_dict() for s in self.scores],
            "cases": self.cases,
        }


# -- Backend availability ─────────────────────────────────────────────


def _ollama_reachable() -> bool:
    """True if an Ollama server is listening at the configured base_url."""
    try:
        from app.core.config import get_ollama_config

        base_url = get_ollama_config().get("base_url", "http://localhost:11434")
        parsed = urlparse(base_url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 11434
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except Exception:
        return False


def detect_available_backends() -> list[str]:
    """Which backends can actually run here (so we don't score a dead engine)."""
    available: list[str] = []
    if shutil.which("mlx_lm") is not None:
        available.append("mlx")
    if _ollama_reachable():
        available.append("ollama")
    if shutil.which("claude") is not None:
        available.append("claude")
    return available


# -- Held-out cases from real reply pairs ──────────────────────────────


def sample_reply_pairs(
    database_url: str,
    *,
    limit: int = 20,
    min_chars: int = 40,
    seed: int = 13,
) -> list[dict[str, Any]]:
    """Sample real (inbound → your reply) pairs to use as comparison cases.

    Deterministic for a given ``seed`` so re-runs compare the same messages.
    Filters out trivially short pairs where voice-match would be noise.
    """
    import random

    from app.db.bootstrap import connect, resolve_sqlite_path

    db_path = resolve_sqlite_path(database_url)
    conn = connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """SELECT id, inbound_text, reply_text FROM reply_pairs
               WHERE length(trim(reply_text)) >= ? AND length(trim(inbound_text)) >= ?""",
            (min_chars, min_chars),
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()

    rng = random.Random(seed)
    if len(rows) > limit:
        rows = rng.sample(rows, limit)
    return [
        {
            "case_key": f"pair-{r['id']}",
            "prompt_text": r["inbound_text"],
            "reference_reply": r["reply_text"],
        }
        for r in rows
    ]


# -- Generation (one backend, one case) ────────────────────────────────


def _default_generate(
    prompt: str,
    *,
    backend: str,
    database_url: str,
    configs_dir: Path,
) -> dict[str, Any]:
    """Draft ``prompt`` with a specific backend pinned. Mirrors run_eval's wrapper."""
    from app.generation.service import DraftRequest, generate_draft

    resp = generate_draft(
        DraftRequest(
            inbound_message=prompt,
            use_local_model=(backend == "mlx"),
            backend_override=backend,
        ),
        database_url=database_url,
        configs_dir=configs_dir,
    )
    return {
        "draft": resp.draft,
        "model_used": resp.model_used,
        "detected_mode": resp.detected_mode,
        "confidence": resp.confidence,
    }


def _fell_back(requested: str, model_used: str) -> bool:
    """True if the engine that actually ran isn't the one we pinned.

    Generation retries empty/failed local drafts on Claude (see generate_draft);
    without this guard that Claude draft would be scored as the local model's.
    """
    mu = (model_used or "").lower()
    if requested == "claude":
        return mu != "claude"
    if requested == "ollama":
        return not mu.startswith("ollama")
    if requested == "mlx":
        return mu in ("claude", "none", "error", "") or mu.startswith("ollama")
    return False


# -- Comparison ────────────────────────────────────────────────────────


def compare_models(
    cases: list[dict[str, Any]],
    backends: Sequence[str],
    *,
    database_url: str,
    configs_dir: Path,
    generate_fn: Callable[..., dict[str, Any]] | None = None,
    embed_fn: Callable[[str], Sequence[float]] | None = None,
) -> ComparisonResult:
    """Draft every case under every backend and score voice-match.

    ``generate_fn(prompt, *, backend, database_url, configs_dir)`` is injectable so
    the comparison is testable without a model; defaults to the real backend-pinned
    generator. ``embed_fn`` enables the semantic component of voice-match.
    """
    gen = generate_fn or _default_generate
    scores: list[BackendScore] = []
    per_case: dict[str, dict[str, Any]] = {
        c["case_key"]: {"case_key": c["case_key"], "backends": {}} for c in cases
    }

    for backend in backends:
        n = fell = errors = 0
        v = lex = sty = length = words = 0.0
        sem_sum = 0.0
        sem_n = 0
        latencies: list[float] = []

        for case in cases:
            t0 = time.monotonic()
            try:
                out = gen(
                    case["prompt_text"],
                    backend=backend,
                    database_url=database_url,
                    configs_dir=configs_dir,
                )
            except Exception as exc:
                errors += 1
                per_case[case["case_key"]]["backends"][backend] = {"error": str(exc)}
                continue
            latencies.append(time.monotonic() - t0)

            draft = out.get("draft", "")
            model_used = out.get("model_used", "")
            vm = voice_match_score(draft, case["reference_reply"], embed_fn=embed_fn)
            fb = _fell_back(backend, model_used)

            n += 1
            v += vm["voice_match"]
            lex += vm["lexical_overlap"]
            sty += vm["style_similarity"]
            length += vm["length_ratio"]
            words += len(draft.split())
            if vm["semantic_similarity"] is not None:
                sem_sum += vm["semantic_similarity"]
                sem_n += 1
            if fb:
                fell += 1

            per_case[case["case_key"]]["backends"][backend] = {
                "model_used": model_used,
                "voice_match": vm["voice_match"],
                "semantic": vm["semantic_similarity"],
                "words": len(draft.split()),
                "fell_back": fb,
            }

        scores.append(
            BackendScore(
                backend=backend,
                n=n,
                voice_match=round(v / n, 3) if n else 0.0,
                semantic_similarity=round(sem_sum / sem_n, 3) if sem_n else None,
                lexical_overlap=round(lex / n, 3) if n else 0.0,
                style_similarity=round(sty / n, 3) if n else 0.0,
                length_ratio=round(length / n, 3) if n else 0.0,
                avg_words=round(words / n, 1) if n else 0.0,
                fallback_count=fell,
                error_count=errors,
                avg_latency_s=round(sum(latencies) / len(latencies), 2) if latencies else 0.0,
            )
        )

    return ComparisonResult(
        backends=list(backends),
        n_cases=len(cases),
        scores=scores,
        cases=list(per_case.values()),
        semantic=embed_fn is not None,
        run_at=datetime.now(timezone.utc).isoformat(),
    )


# -- Reporting ─────────────────────────────────────────────────────────


def format_comparison(result: ComparisonResult) -> str:
    """A side-by-side scorecard, ranked by voice-match (the deciding metric)."""
    lines: list[str] = []
    lines.append(f"Cross-model comparison — {result.n_cases} of your real replies"
                 f"{' (semantic on)' if result.semantic else ''} | {result.run_at}")
    lines.append("=" * 86)
    sem_h = "semantic" if result.semantic else "  sem   "
    lines.append(f" {'backend':<10} {'n':>3} | {'voice':>6} {sem_h:>8} {'lexical':>7} {'style':>6} {'lenfit':>6} | {'words':>5} {'fellbk':>6} {'lat(s)':>6}")
    lines.append("-" * 86)

    # Rank by voice-match — the metric that decides the privacy/cost trade.
    ranked = sorted(result.scores, key=lambda s: s.voice_match, reverse=True)
    for s in ranked:
        sem = f"{s.semantic_similarity:.3f}" if s.semantic_similarity is not None else "   -  "
        lines.append(
            f" {s.backend:<10} {s.n:>3} | {s.voice_match:>6.3f} {sem:>8} "
            f"{s.lexical_overlap:>7.3f} {s.style_similarity:>6.3f} {s.length_ratio:>6.3f} | "
            f"{s.avg_words:>5.1f} {s.fallback_count:>6} {s.avg_latency_s:>6.2f}"
        )

    lines.append("=" * 86)
    if ranked and ranked[0].n:
        top = ranked[0]
        lines.append(f" Best voice-match: {top.backend} ({top.voice_match:.3f})")
        if any(s.fallback_count for s in ranked):
            lines.append(" Note: 'fellbk' counts cases where generation silently fell back to another"
                         " engine — those drafts are NOT this backend's own output.")
    else:
        lines.append(" No cases scored — is there reply-pair data in this instance's DB?")
    return "\n".join(lines)


__all__ = [
    "BACKENDS",
    "BackendScore",
    "ComparisonResult",
    "compare_models",
    "detect_available_backends",
    "format_comparison",
    "sample_reply_pairs",
]
