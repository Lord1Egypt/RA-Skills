"""
cove_pipeline.py — Chain-of-Verification (CoVe) Pipeline
=========================================================

Named after the ancient practice of verification — a skald does not simply
speak words; they test them against memory, against truth, against the wisdom
of those who came before. CoVe is that process made systematic.

The four-step refinement loop that transforms a raw model draft into a
verified, grounded response:

  Step 1: DRAFT     — generate an initial response against the Ground Truth
  Step 2: QUESTION  — plan verification questions about the draft
  Step 3: ANSWER    — execute questions against MimirWell + MimirWell rerank
  Step 4: REVISE    — revise the draft in light of the Q&A verification

Each step has its own fallback chain. The pipeline is checkpointed after
every step — if the session crashes mid-pipeline, it can resume from the
last completed step on restart.

Bypass logic:
  - Low complexity queries (short, factual, identity questions) skip Steps 2-4
    and return the draft directly — full CoVe is wasteful for simple answers.
  - If the pipeline circuit breaker opens (3 consecutive failures), CoVe is
    bypassed entirely and a direct model call serves the draft.

Norse framing: The raven Huginn already retrieved the truth from the Well.
CoVe is Odin reading that truth, questioning it, and then speaking with
the authority of someone who actually checked their words.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from scripts.mimir_well import (
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    MimirVordurError,
    MimirWell,
    RetryConfig,
    _MimirCircuitBreaker,
    _RetryEngine,
)
from scripts.huginn import RetrievalResult
from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

_DEFAULT_CHECKPOINT_DIR = Path("session/cove_checkpoints")
_DEFAULT_N_QUESTIONS: int = 3
_DEFAULT_STEP_TIMEOUT_S: float = 15.0
_DEFAULT_MIN_COMPLEXITY: str = "medium"

# Complexity levels
_COMPLEXITY_LOW = "low"
_COMPLEXITY_MEDIUM = "medium"
_COMPLEXITY_HIGH = "high"


# ─── Error Taxonomy ───────────────────────────────────────────────────────────


class CovePipelineError(MimirVordurError):
    """Base class for CovePipeline errors."""


class CoveStepFailedError(CovePipelineError):
    """A specific CoVe step failed with no recovery."""

    def __init__(self, step: int, reason: str) -> None:
        self.step = step
        self.reason = reason
        super().__init__(f"CoVe Step {step} failed: {reason}")


class CoveAllFallbacksExhaustedError(CovePipelineError):
    """All fallback paths exhausted — pipeline cannot continue."""


# ─── Template Verification Questions ─────────────────────────────────────────

TEMPLATE_QUESTIONS: Dict[str, List[str]] = {
    "norse_spirituality": [
        "Does this response accurately represent Norse spiritual practices?",
        "Are the rune names and meanings correct?",
        "Does this align with authentic Heathen traditions?",
    ],
    "norse_mythology": [
        "Are the names of gods and entities accurate?",
        "Does the cosmological description match the Eddas?",
        "Are the relationships between mythological figures correct?",
    ],
    "norse_culture": [
        "Is the historical context for this period accurate?",
        "Does this accurately represent Norse social structures?",
        "Are the cultural practices described authentic?",
    ],
    "coding": [
        "Is the code or technical explanation syntactically correct?",
        "Does the algorithm description match standard implementations?",
        "Are the library/API references accurate?",
    ],
    "character": [
        "Is this response consistent with Sigrid's values and worldview?",
        "Does the emotional expression match Sigrid's personality?",
        "Is this consistent with her Norse Pagan spiritual framework?",
    ],
    "roleplay": [
        "Does this response stay true to the established scene context?",
        "Is the character voice consistent with Norse culture?",
        "Does this respect the established narrative continuity?",
    ],
    "default": [
        "Is this factually consistent with the source material?",
        "Does this response contradict any retrieved Ground Truth?",
        "Are there any unsupported claims in this response?",
    ],
}


# ─── Data Structures ──────────────────────────────────────────────────────────


@dataclass
class CoveCheckpoint:
    """Persisted to disk between CoVe steps.

    Enables crash-safe pipeline resumption — if the session dies after Step 2,
    the next session reads this file and skips Steps 1-2 on restart.
    """

    checkpoint_id: str
    query: str
    context: str
    domain: Optional[str]
    draft: Optional[str] = None                              # available after Step 1
    questions: Optional[List[str]] = None                    # available after Step 2
    qa_pairs: Optional[List[Tuple[str, str]]] = None         # available after Step 3
    step_reached: int = 0                                     # 0=start, 1–3 = step N done
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CoveCheckpoint":
        qa = d.get("qa_pairs")
        if qa is not None:
            qa = [tuple(pair) for pair in qa]
        return cls(
            checkpoint_id=d["checkpoint_id"],
            query=d["query"],
            context=d["context"],
            domain=d.get("domain"),
            draft=d.get("draft"),
            questions=d.get("questions"),
            qa_pairs=qa,
            step_reached=int(d.get("step_reached", 0)),
            created_at=d.get("created_at", ""),
        )


@dataclass
class CoveResult:
    """Typed API response from CovePipeline.run()."""

    draft: str                                # Step 1 output
    verification_questions: List[str]         # Step 2 output
    qa_pairs: List[Tuple[str, str]]           # Step 3 output
    final_response: str                       # Step 4 output (may equal draft)
    used_cove: bool                           # False if bypassed
    steps_completed: int                      # 0–4
    fallback_chain: List[str]                 # which fallbacks engaged
    checkpoint_id: Optional[str]
    faithfulness_score: Optional[Any] = None  # FaithfulnessScore — set by caller
    error_context: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "used_cove": self.used_cove,
            "steps_completed": self.steps_completed,
            "fallback_chain": self.fallback_chain,
            "checkpoint_id": self.checkpoint_id,
            "draft_chars": len(self.draft),
            "final_chars": len(self.final_response),
            "n_questions": len(self.verification_questions),
            "n_qa_pairs": len(self.qa_pairs),
            "error_context": self.error_context,
        }


@dataclass
class CoveState:
    """State snapshot published to StateBus."""

    enabled: bool
    total_runs: int
    total_skipped_low_complexity: int
    total_bypassed_circuit_breaker: int
    total_step_failures: Dict[str, int]
    avg_steps_completed: float
    circuit_breaker_pipeline: str
    last_run_at: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── CovePipeline ─────────────────────────────────────────────────────────────


class CovePipeline:
    """Chain-of-Verification — four-step response refinement.

    Sits between HuginnRetriever (retrieval) and VordurChecker (verification).
    Takes a query + retrieval result, generates a draft, plans verification
    questions, answers them against MimirWell, then revises the draft.

    Never raises to the caller — all failure paths produce a valid CoveResult.
    Singleton: use init_cove_from_config() + get_cove().
    """

    def __init__(
        self,
        mimir_well: MimirWell,
        router: Any,                            # ModelRouterClient — Any to avoid circular import
        vordur: Any,                            # VordurChecker — Any to avoid circular import
        min_complexity: str = _DEFAULT_MIN_COMPLEXITY,
        n_verification_questions: int = _DEFAULT_N_QUESTIONS,
        checkpoint_dir: Optional[Path] = None,
        step_timeout_s: float = _DEFAULT_STEP_TIMEOUT_S,
    ) -> None:
        self._well = mimir_well
        self._router = router
        self._vordur = vordur
        self._min_complexity = min_complexity
        self._n_questions = n_verification_questions
        self._checkpoint_dir = checkpoint_dir or _DEFAULT_CHECKPOINT_DIR
        self._step_timeout_s = step_timeout_s

        # Ensure checkpoint dir exists
        try:
            self._checkpoint_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.warning("CovePipeline: could not create checkpoint dir: %s", exc)

        # Circuit breakers — one per step + one for the whole pipeline
        self._cb_pipeline = _MimirCircuitBreaker(
            "cove_pipeline", CircuitBreakerConfig(failure_threshold=3, cooldown_s=30.0)
        )
        self._cb_step2 = _MimirCircuitBreaker(
            "cove_step2", CircuitBreakerConfig(failure_threshold=3, cooldown_s=30.0)
        )
        self._cb_step3 = _MimirCircuitBreaker(
            "cove_step3", CircuitBreakerConfig(failure_threshold=3, cooldown_s=30.0)
        )
        self._cb_step4 = _MimirCircuitBreaker(
            "cove_step4", CircuitBreakerConfig(failure_threshold=3, cooldown_s=30.0)
        )

        # Retry engine for model calls
        self._retry = _RetryEngine(
            RetryConfig(max_attempts=2, base_delay_s=0.5, backoff_factor=2.0, max_delay_s=4.0)
        )

        # Telemetry
        self._total_runs: int = 0
        self._total_skipped_low: int = 0
        self._total_bypassed_cb: int = 0
        self._step_failures: Dict[str, int] = {"step1": 0, "step2": 0, "step3": 0, "step4": 0}
        self._steps_completed_history: List[int] = []
        self._last_run_at: Optional[str] = None

    # ─── Public API ───────────────────────────────────────────────────────────

    def run(
        self,
        query: str,
        context: str,
        retrieval: RetrievalResult,
        complexity: str,
        resume_checkpoint: Optional[CoveCheckpoint] = None,
    ) -> CoveResult:
        """Full CoVe pipeline with per-step circuit breakers and checkpointing.

        Low complexity → returns draft (Step 1 only).
        Pipeline CB open → returns direct model call as draft, used_cove=False.
        All steps have fallback chains — never raises.
        """
        self._total_runs += 1
        self._last_run_at = datetime.now(timezone.utc).isoformat()
        fallback_chain: List[str] = []
        domain = retrieval.domain

        # ── Pipeline circuit breaker check ────────────────────────────────────
        try:
            self._cb_pipeline.before_call()
        except CircuitBreakerOpenError as exc:
            logger.info(
                "CovePipeline: circuit breaker OPEN (%.1fs) — direct draft only",
                exc.cooldown_remaining_s,
            )
            self._total_bypassed_cb += 1
            fallback_chain.append("pipeline_cb_bypass")
            draft = self._direct_draft(query, context)
            result = CoveResult(
                draft=draft,
                verification_questions=[],
                qa_pairs=[],
                final_response=draft,
                used_cove=False,
                steps_completed=1,
                fallback_chain=fallback_chain,
                checkpoint_id=None,
                error_context="Pipeline circuit breaker open",
            )
            self._record_run(1)
            return result

        # ── Low complexity: skip verification ─────────────────────────────────
        if not self._should_use_cove(complexity):
            self._total_skipped_low += 1
            fallback_chain.append("low_complexity_skip")
            draft = self._direct_draft(query, context)
            self._cb_pipeline.on_success()
            result = CoveResult(
                draft=draft,
                verification_questions=[],
                qa_pairs=[],
                final_response=draft,
                used_cove=False,
                steps_completed=1,
                fallback_chain=fallback_chain,
                checkpoint_id=None,
            )
            self._record_run(1)
            return result

        # ── Full CoVe pipeline ─────────────────────────────────────────────────
        checkpoint_id = (
            resume_checkpoint.checkpoint_id if resume_checkpoint
            else str(uuid.uuid4())[:8]
        )
        checkpoint = resume_checkpoint or CoveCheckpoint(
            checkpoint_id=checkpoint_id,
            query=query,
            context=context,
            domain=domain,
        )

        draft: str = checkpoint.draft or ""
        questions: List[str] = checkpoint.questions or []
        qa_pairs: List[Tuple[str, str]] = checkpoint.qa_pairs or []
        steps_completed = checkpoint.step_reached

        try:
            # ── STEP 1: Draft ──────────────────────────────────────────────────
            if steps_completed < 1:
                try:
                    draft = self._step1_draft(query, context, checkpoint)
                    steps_completed = 1
                    self._save_checkpoint(checkpoint)
                except Exception as exc:
                    # Step 1 failure is non-recoverable — abort CoVe
                    self._step_failures["step1"] += 1
                    self._cb_pipeline.on_failure(exc)
                    logger.error("CovePipeline: Step 1 FAILED (%s) — returning empty draft", exc)
                    empty = CoveResult(
                        draft="",
                        verification_questions=[],
                        qa_pairs=[],
                        final_response="",
                        used_cove=False,
                        steps_completed=0,
                        fallback_chain=["step1_failed"],
                        checkpoint_id=checkpoint_id,
                        error_context=f"Step 1 failed: {exc}",
                    )
                    self._record_run(0)
                    return empty

            # ── STEP 2: Plan questions ─────────────────────────────────────────
            if steps_completed < 2:
                questions, step2_fallback = self._step2_plan_questions(
                    draft, context, domain, checkpoint
                )
                if step2_fallback:
                    fallback_chain.append(step2_fallback)
                steps_completed = 2
                self._save_checkpoint(checkpoint)

            # ── STEP 3: Execute questions ──────────────────────────────────────
            if steps_completed < 3:
                qa_pairs, step3_fallback = self._step3_execute_questions(
                    questions, context, checkpoint
                )
                if step3_fallback:
                    fallback_chain.append(step3_fallback)
                steps_completed = 3
                self._save_checkpoint(checkpoint)

            # ── STEP 4: Revise ─────────────────────────────────────────────────
            final_response, step4_fallback = self._step4_revise(
                draft, questions, qa_pairs, context, checkpoint
            )
            if step4_fallback:
                fallback_chain.append(step4_fallback)
            steps_completed = 4

            # Success — delete checkpoint
            self._delete_checkpoint(checkpoint)
            self._cb_pipeline.on_success()

            result = CoveResult(
                draft=draft,
                verification_questions=questions,
                qa_pairs=qa_pairs,
                final_response=final_response,
                used_cove=True,
                steps_completed=steps_completed,
                fallback_chain=fallback_chain,
                checkpoint_id=checkpoint_id,
            )
            self._record_run(steps_completed)
            return result

        except Exception as exc:
            # Unexpected failure — record, open CB
            self._cb_pipeline.on_failure(exc)
            logger.error("CovePipeline: unexpected pipeline failure (%s)", exc)
            fallback_chain.append("unexpected_pipeline_error")
            result = CoveResult(
                draft=draft or "",
                verification_questions=questions,
                qa_pairs=qa_pairs,
                final_response=draft or "",
                used_cove=steps_completed > 0,
                steps_completed=steps_completed,
                fallback_chain=fallback_chain,
                checkpoint_id=checkpoint_id,
                error_context=str(exc),
            )
            self._record_run(steps_completed)
            return result

    # ─── Step Implementations ─────────────────────────────────────────────────

    def _step1_draft(
        self,
        query: str,
        context: str,
        checkpoint: CoveCheckpoint,
    ) -> str:
        """Generate initial draft against Ground Truth context.

        Uses the model router's chosen tier. Raises on failure — Step 1
        failure is non-recoverable.
        """
        from scripts.model_router_client import Message, TIER_CONSCIOUS

        system_prompt = (
            "You are Sigrid, a 21-year-old Norse-Pagan völva. "
            "Use the Ground Truth below to answer accurately.\n\n"
            f"{context}"
        )
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=query),
        ]

        response = self._retry.run(
            self._router.complete,
            messages=messages,
            tier=TIER_CONSCIOUS,
            timeout_s=self._step_timeout_s,
        )
        draft = response.content if hasattr(response, "content") else str(response)

        # Update checkpoint in-place
        checkpoint.draft = draft
        logger.debug("CovePipeline: Step 1 draft produced (%d chars)", len(draft))
        return draft

    def _step2_plan_questions(
        self,
        draft: str,
        context: str,
        domain: Optional[str],
        checkpoint: CoveCheckpoint,
    ) -> Tuple[List[str], Optional[str]]:
        """Plan verification questions about the draft.

        Primary: subconscious tier (Ollama).
        Fallback A: domain-aware template questions.
        Fallback B: generic default questions.
        Returns (questions, fallback_used_or_None).
        """
        fallback_used: Optional[str] = None

        # PRIMARY: model call
        try:
            self._cb_step2.before_call()
            questions = self._retry.run(
                self._call_plan_questions,
                draft=draft,
                context=context,
            )
            if questions:
                self._cb_step2.on_success()
                checkpoint.questions = questions
                logger.debug("CovePipeline: Step 2 planned %d questions", len(questions))
                return questions, None
            # Empty response — fall through
            self._cb_step2.on_success()
        except CircuitBreakerOpenError as exc:
            logger.debug("CovePipeline: Step 2 CB open (%.1fs) — template fallback", exc.cooldown_remaining_s)
            fallback_used = "step2_cb_open"
        except Exception as exc:
            self._step_failures["step2"] += 1
            self._cb_step2.on_failure(exc)
            logger.warning("CovePipeline: Step 2 model call failed (%s) — template fallback", exc)
            fallback_used = "step2_model_failed"

        # FALLBACK A: domain-specific templates
        template_key = domain if domain in TEMPLATE_QUESTIONS else "default"
        questions = TEMPLATE_QUESTIONS[template_key][: self._n_questions]
        fallback_used = fallback_used or "step2_template_fallback"
        logger.info("CovePipeline: Step 2 using template questions (domain=%s)", template_key)
        checkpoint.questions = questions
        return questions, fallback_used

    def _step3_execute_questions(
        self,
        questions: List[str],
        context: str,
        checkpoint: CoveCheckpoint,
    ) -> Tuple[List[Tuple[str, str]], Optional[str]]:
        """Answer verification questions against MimirWell.

        Primary: subconscious tier for each question.
        Fallback: skip (return empty qa_pairs — still counts as step 3 done).
        Returns (qa_pairs, fallback_used_or_None).
        """
        if not questions:
            checkpoint.qa_pairs = []
            return [], None

        qa_pairs: List[Tuple[str, str]] = []
        fallback_used: Optional[str] = None

        try:
            self._cb_step3.before_call()

            for question in questions:
                try:
                    answer = self._retry.run(
                        self._call_answer_question,
                        question=question,
                        context=context,
                    )
                    qa_pairs.append((question, answer))
                except Exception as exc:
                    logger.debug("CovePipeline: Step 3 question failed (%s) — skipping", exc)
                    qa_pairs.append((question, "[answer unavailable]"))

            self._cb_step3.on_success()
            checkpoint.qa_pairs = qa_pairs
            logger.debug("CovePipeline: Step 3 answered %d/%d questions", len(qa_pairs), len(questions))
            return qa_pairs, None

        except CircuitBreakerOpenError as exc:
            logger.debug(
                "CovePipeline: Step 3 CB open (%.1fs) — skipping Q&A", exc.cooldown_remaining_s
            )
            fallback_used = "step3_cb_open"
        except Exception as exc:
            self._step_failures["step3"] += 1
            self._cb_step3.on_failure(exc)
            logger.warning("CovePipeline: Step 3 failed (%s) — skipping Q&A", exc)
            fallback_used = "step3_failed_skip"

        # Fallback: empty pairs (not fatal)
        checkpoint.qa_pairs = []
        return [], fallback_used

    def _step4_revise(
        self,
        draft: str,
        questions: List[str],
        qa_pairs: List[Tuple[str, str]],
        context: str,
        checkpoint: CoveCheckpoint,
    ) -> Tuple[str, Optional[str]]:
        """Revise draft based on Q&A verification results.

        Primary: chosen tier via router.
        Fallback A: conscious tier.
        Fallback B: return Step 1 draft unchanged.
        Returns (revised_response, fallback_used_or_None).
        """
        # If no qa_pairs, revision adds no value — return draft
        if not qa_pairs:
            logger.debug("CovePipeline: Step 4 skipped (no qa_pairs) — returning draft")
            return draft, "step4_no_qa_pairs"

        fallback_used: Optional[str] = None

        try:
            self._cb_step4.before_call()
            revised = self._retry.run(
                self._call_revise,
                draft=draft,
                qa_pairs=qa_pairs,
                context=context,
            )
            if revised and revised.strip():
                self._cb_step4.on_success()
                logger.debug("CovePipeline: Step 4 revision produced (%d chars)", len(revised))
                return revised, None
            # Empty response — fall through
            self._cb_step4.on_success()

        except CircuitBreakerOpenError as exc:
            logger.debug(
                "CovePipeline: Step 4 CB open (%.1fs) — returning draft", exc.cooldown_remaining_s
            )
            fallback_used = "step4_cb_open"
        except Exception as exc:
            self._step_failures["step4"] += 1
            self._cb_step4.on_failure(exc)
            logger.warning("CovePipeline: Step 4 failed (%s) — returning draft unchanged", exc)
            fallback_used = "step4_failed_return_draft"

        return draft, fallback_used or "step4_empty_response"

    # ─── Model Call Helpers ───────────────────────────────────────────────────

    def _direct_draft(self, query: str, context: str) -> str:
        """Generate a draft without CoVe — used for low complexity or CB bypass."""
        try:
            from scripts.model_router_client import Message, TIER_CONSCIOUS

            system_prompt = (
                "You are Sigrid, a 21-year-old Norse-Pagan völva.\n\n"
                f"{context}" if context else "You are Sigrid, a 21-year-old Norse-Pagan völva."
            )
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=query),
            ]
            response = self._router.complete(
                messages=messages,
                tier=TIER_CONSCIOUS,
                timeout_s=self._step_timeout_s,
            )
            return response.content if hasattr(response, "content") else str(response)
        except Exception as exc:
            logger.warning("CovePipeline._direct_draft: failed (%s)", exc)
            return ""

    def _call_plan_questions(self, draft: str, context: str) -> List[str]:
        """Ask the subconscious tier to generate verification questions."""
        from scripts.model_router_client import Message, TIER_SUBCONSCIOUS

        prompt = (
            f"You are checking this response for factual accuracy:\n\n"
            f"RESPONSE:\n{draft}\n\n"
            f"SOURCE CONTEXT:\n{context[:3000]}\n\n"
            f"Write exactly {self._n_questions} yes/no verification questions "
            f"to check if the response is factually consistent with the source. "
            f"Output ONLY numbered questions, one per line, no preamble."
        )
        messages = [Message(role="user", content=prompt)]
        response = self._router.complete(
            messages=messages,
            tier=TIER_SUBCONSCIOUS,
            timeout_s=self._step_timeout_s,
        )
        raw = response.content if hasattr(response, "content") else str(response)
        return self._parse_questions(raw)

    def _call_answer_question(self, question: str, context: str) -> str:
        """Answer a single verification question against the source context."""
        from scripts.model_router_client import Message, TIER_SUBCONSCIOUS

        prompt = (
            f"Answer this question based ONLY on the source context below.\n\n"
            f"QUESTION: {question}\n\n"
            f"SOURCE:\n{context[:3000]}\n\n"
            f"Answer concisely in 1-2 sentences."
        )
        messages = [Message(role="user", content=prompt)]
        response = self._router.complete(
            messages=messages,
            tier=TIER_SUBCONSCIOUS,
            timeout_s=self._step_timeout_s,
        )
        return response.content if hasattr(response, "content") else str(response)

    def _call_revise(
        self,
        draft: str,
        qa_pairs: List[Tuple[str, str]],
        context: str,
    ) -> str:
        """Revise the draft based on Q&A verification results."""
        from scripts.model_router_client import Message, TIER_CONSCIOUS

        qa_text = "\n".join(
            f"Q: {q}\nA: {a}" for q, a in qa_pairs
        )
        prompt = (
            f"You are revising a response based on factual verification.\n\n"
            f"ORIGINAL RESPONSE:\n{draft}\n\n"
            f"VERIFICATION Q&A:\n{qa_text}\n\n"
            f"GROUND TRUTH SOURCE:\n{context[:3000]}\n\n"
            f"Revise the original response to correct any factual errors identified "
            f"in the verification. Maintain the same tone and character voice. "
            f"If the original is already accurate, return it unchanged."
        )
        messages = [Message(role="user", content=prompt)]
        response = self._router.complete(
            messages=messages,
            tier=TIER_CONSCIOUS,
            timeout_s=self._step_timeout_s,
        )
        return response.content if hasattr(response, "content") else str(response)

    # ─── Parsing Helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _parse_questions(raw: str) -> List[str]:
        """Extract numbered questions from model output."""
        if not raw or not raw.strip():
            return []
        lines = raw.strip().split("\n")
        questions: List[str] = []
        for line in lines:
            line = line.strip()
            # Strip leading numbers/bullets: "1. ", "1) ", "- ", "• "
            cleaned = re.sub(r"^[\d]+[.)]\s*|^[-•*]\s*", "", line).strip()
            if cleaned and len(cleaned) > 10:  # minimum viable question length
                questions.append(cleaned)
        return questions

    # ─── Checkpoint Management ────────────────────────────────────────────────

    def _checkpoint_path(self, checkpoint_id: str) -> Path:
        return self._checkpoint_dir / f"cove_{checkpoint_id}.json"

    def _save_checkpoint(self, checkpoint: CoveCheckpoint) -> None:
        """Persist checkpoint to disk. Non-fatal if fails."""
        try:
            path = self._checkpoint_path(checkpoint.checkpoint_id)
            path.write_text(
                json.dumps(checkpoint.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            logger.debug(
                "CovePipeline: checkpoint saved step=%d id=%s",
                checkpoint.step_reached,
                checkpoint.checkpoint_id,
            )
        except Exception as exc:
            logger.debug("CovePipeline: could not save checkpoint: %s", exc)

    def _delete_checkpoint(self, checkpoint: CoveCheckpoint) -> None:
        """Delete completed checkpoint. Non-fatal if fails."""
        try:
            path = self._checkpoint_path(checkpoint.checkpoint_id)
            if path.exists():
                path.unlink()
                logger.debug("CovePipeline: checkpoint deleted id=%s", checkpoint.checkpoint_id)
        except Exception as exc:
            logger.debug("CovePipeline: could not delete checkpoint: %s", exc)

    def load_checkpoint(self, checkpoint_id: str) -> Optional[CoveCheckpoint]:
        """Load a previously saved checkpoint. Returns None if not found."""
        try:
            path = self._checkpoint_path(checkpoint_id)
            if not path.exists():
                return None
            data = json.loads(path.read_text(encoding="utf-8"))
            return CoveCheckpoint.from_dict(data)
        except Exception as exc:
            logger.warning("CovePipeline: could not load checkpoint %s: %s", checkpoint_id, exc)
            return None

    def list_checkpoints(self) -> List[str]:
        """List all checkpoint IDs (incomplete pipelines from previous sessions)."""
        try:
            return [
                p.stem.removeprefix("cove_")
                for p in self._checkpoint_dir.glob("cove_*.json")
            ]
        except Exception:
            return []

    # ─── Utility ──────────────────────────────────────────────────────────────

    def _should_use_cove(self, complexity: str) -> bool:
        """Return True if the pipeline should run the full CoVe loop."""
        order = {_COMPLEXITY_LOW: 0, _COMPLEXITY_MEDIUM: 1, _COMPLEXITY_HIGH: 2}
        min_order = order.get(self._min_complexity, 1)
        query_order = order.get(complexity, 1)
        return query_order >= min_order

    def _record_run(self, steps_completed: int) -> None:
        self._steps_completed_history.append(steps_completed)
        if len(self._steps_completed_history) > 100:
            self._steps_completed_history.pop(0)

    # ─── State & Bus ──────────────────────────────────────────────────────────

    def get_state(self) -> CoveState:
        avg = (
            sum(self._steps_completed_history) / len(self._steps_completed_history)
            if self._steps_completed_history else 0.0
        )
        return CoveState(
            enabled=True,
            total_runs=self._total_runs,
            total_skipped_low_complexity=self._total_skipped_low,
            total_bypassed_circuit_breaker=self._total_bypassed_cb,
            total_step_failures=dict(self._step_failures),
            avg_steps_completed=round(avg, 2),
            circuit_breaker_pipeline=self._cb_pipeline.get_state_label(),
            last_run_at=self._last_run_at,
        )

    def publish(self, bus: StateBus) -> None:
        """Publish current state to the StateBus."""
        try:
            event = StateEvent(
                source_module="cove_pipeline",
                event_type="cove_state",
                payload=self.get_state().to_dict(),
            )
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(bus.publish_state(event, nowait=True))
                else:
                    loop.run_until_complete(bus.publish_state(event, nowait=True))
            except RuntimeError:
                asyncio.run(bus.publish_state(event, nowait=True))
        except Exception as exc:
            logger.debug("CovePipeline.publish: failed (%s)", exc)


# ─── Singleton ────────────────────────────────────────────────────────────────

_COVE: Optional[CovePipeline] = None


def get_cove() -> CovePipeline:
    """Return the global CovePipeline. Raises if not yet initialised."""
    if _COVE is None:
        raise RuntimeError(
            "CovePipeline not initialised — call init_cove_from_config() first."
        )
    return _COVE


def init_cove_from_config(
    config: Any,
    mimir_well: MimirWell,
    router: Any,
    vordur: Any,
) -> CovePipeline:
    """Create and register the global CovePipeline from the skill config dict.

    config      — dict loaded by ConfigLoader.
    mimir_well  — MimirWell singleton.
    router      — ModelRouterClient singleton.
    vordur      — VordurChecker singleton.

    Config keys read (all optional):
        cove.min_complexity              ("medium")
        cove.n_verification_questions    (3)
        cove.checkpoint_dir              ("session/cove_checkpoints")
        cove.step_timeout_s              (15.0)
    """
    global _COVE

    cove_cfg: Dict[str, Any] = {}
    if isinstance(config, dict):
        cove_cfg = config.get("cove", {}) or {}
    elif hasattr(config, "get"):
        cove_cfg = config.get("cove", {}) or {}

    checkpoint_dir_str: str = cove_cfg.get("checkpoint_dir", str(_DEFAULT_CHECKPOINT_DIR))

    _COVE = CovePipeline(
        mimir_well=mimir_well,
        router=router,
        vordur=vordur,
        min_complexity=cove_cfg.get("min_complexity", _DEFAULT_MIN_COMPLEXITY),
        n_verification_questions=int(cove_cfg.get("n_verification_questions", _DEFAULT_N_QUESTIONS)),
        checkpoint_dir=Path(checkpoint_dir_str),
        step_timeout_s=float(cove_cfg.get("step_timeout_s", _DEFAULT_STEP_TIMEOUT_S)),
    )

    logger.info(
        "CovePipeline singleton registered "
        "(min_complexity=%s, n_questions=%d, checkpoint_dir=%s).",
        _COVE._min_complexity,
        _COVE._n_questions,
        _COVE._checkpoint_dir,
    )
    return _COVE
