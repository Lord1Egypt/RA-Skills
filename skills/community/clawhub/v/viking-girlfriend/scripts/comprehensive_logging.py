"""
comprehensive_logging.py — Sigrid's High-Detail Session Logger
==============================================================

Adopted from NorseSagaEngine comprehensive_logging.py.
Adapted for the Ørlög Architecture: game-specific TurnLog replaced with
InteractionLog (user_message, session_id, sigrid_location).

Norse framing: This is the saga-scribe of the hall — every word spoken,
every thought of the AI, every error and warning, inscribed in the World Tree.
Nothing is lost. Everything has its verse.
"""

from __future__ import annotations

import json
import logging
import re
import traceback
from dataclasses import asdict, dataclass, field
from datetime import datetime
from functools import wraps
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Dict, List, Optional, Tuple

from scripts.crash_reporting import get_crash_reporter


# ─── Secret masking ───────────────────────────────────────────────────────────

_MASK_PATTERNS: List[Tuple[str, re.Pattern]] = [
    # OpenAI/Anthropic/generic sk- API keys
    ("api_key_sk",    re.compile(r"sk-[A-Za-z0-9_\-]{20,}", re.ASCII)),
    # Bearer tokens in HTTP headers
    ("bearer_token",  re.compile(r"(Bearer\s+)[A-Za-z0-9+/=_\-]{20,}", re.IGNORECASE)),
    # Assignment patterns: SOME_API_KEY=actualvalue  or  SOME_SECRET="value"
    ("env_assign",    re.compile(
        r"(?i)([A-Z_a-z0-9]*(?:API_KEY|SECRET|PASSWORD|TOKEN|AUTH)[A-Z_a-z0-9]*"
        r"\s*=\s*[\"']?)[^\s\"',;\\]{8,}",
    )),
]


def _mask_secrets(text: str) -> str:
    """Replace recognizable secret patterns with [REDACTED].

    Applied to every log record before it reaches any handler.
    Never raises — silently returns original text on any error.
    """
    if text is None:
        return ""
    try:
        for name, pattern in _MASK_PATTERNS:
            if name == "bearer_token":
                # Keep the "Bearer " prefix, mask only the token value
                text = pattern.sub(r"\1[REDACTED]", text)
            elif name == "env_assign":
                # Keep the KEY= prefix, mask only the value
                text = pattern.sub(r"\1[REDACTED]", text)
            else:
                text = pattern.sub("[REDACTED]", text)
    except Exception:  # nosec B110 - calling logger here causes infinite recursion in _mask_secrets
        pass
    return text


class _SecretMaskingFilter(logging.Filter):
    """Logging filter that scrubs secrets from records before they hit disk.

    Attached to every file handler by ComprehensiveLogger._setup_loggers().
    Mutates record.msg and record.args in-place so the formatted output is clean.
    """

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        try:
            if isinstance(record.msg, str):
                record.msg = _mask_secrets(record.msg)
            if record.args:
                if isinstance(record.args, tuple):
                    record.args = tuple(
                        _mask_secrets(a) if isinstance(a, str) else a
                        for a in record.args
                    )
                elif isinstance(record.args, dict):
                    record.args = {
                        k: _mask_secrets(v) if isinstance(v, str) else v
                        for k, v in record.args.items()
                    }
        except Exception:  # nosec B110 - cannot call logger inside SecretsMaskingFilter (infinite recursion)
            pass
        return True  # Always allow the record through after masking


@dataclass
class AICallLog:
    """Record of a single call to any AI model — Conscious, Deep, or Subconscious mind."""

    timestamp: str
    call_id: str
    model_tier: str          # "conscious-mind" | "deep-mind" | "subconscious"
    call_type: str
    prompt_length: int
    prompt_preview: str
    full_prompt: str
    context_keys: List[str]
    response_length: int
    response_preview: str
    full_response: str
    processing_time: float
    success: bool
    error: Optional[str] = None
    data_sources: List[str] = field(default_factory=list)
    data_path: List[str] = field(default_factory=list)


@dataclass
class InteractionLog:
    """Record of a single conversation turn — the thread Verdandi is weaving now."""

    interaction_number: int
    timestamp: str
    user_message: str
    session_id: str
    sigrid_location: str          # from environment_mapper (home, expedition, etc.)
    ai_calls: List[AICallLog] = field(default_factory=list)
    model_tier_visits: Dict[str, int] = field(default_factory=dict)
    sigrid_response: str = ""
    events_detected: List[str] = field(default_factory=list)
    memories_formed: List[Dict[str, Any]] = field(default_factory=list)
    state_changes: Dict[str, Any] = field(default_factory=dict)
    emotional_state: Dict[str, float] = field(default_factory=dict)   # PAD vector snapshot
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class ComprehensiveLogger:
    """High-detail logger with fail-safe writes and per-interaction snapshots.

    The saga-scribe never drops the quill — every write is guarded.
    """

    def __init__(self, logs_dir: str = "logs") -> None:
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.logs_dir / f"session_{self.session_id}"
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self._call_counter = 0
        self._lock = Lock()
        self.current_interaction: Optional[InteractionLog] = None
        self.interaction_logs: List[InteractionLog] = []

        self.crash_reporter = get_crash_reporter(str(self.logs_dir))
        self._setup_loggers()
        self.main_logger.info("Sigrid session started: %s", self.session_id)

    def _setup_loggers(self) -> None:
        """Erect the five pillars of observation — Huginn watches all channels."""
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        _masking_filter = _SecretMaskingFilter()

        def _build_logger(name: str, filename: str, level: int) -> logging.Logger:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.propagate = False
            logger.handlers.clear()
            handler = logging.FileHandler(
                self.session_dir / filename, encoding="utf-8"
            )
            handler.setFormatter(formatter)
            handler.addFilter(_masking_filter)
            logger.addHandler(handler)
            return logger

        self.main_logger = _build_logger(
            f"sigrid.{self.session_id}", "full_log.log", logging.DEBUG
        )
        self.ai_logger = _build_logger(
            f"sigrid.{self.session_id}.ai", "ai_calls.log", logging.DEBUG
        )
        self.path_logger = _build_logger(
            f"sigrid.{self.session_id}.path", "data_paths.log", logging.DEBUG
        )
        self.error_logger = _build_logger(
            f"sigrid.{self.session_id}.error", "errors.log", logging.WARNING
        )
        self.memory_logger = _build_logger(
            f"sigrid.{self.session_id}.memory", "memory_events.log", logging.DEBUG
        )

    def _safe_json_dump(self, path: Path, payload: Any) -> None:
        try:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, default=str, ensure_ascii=False)
        except Exception as exc:
            self.error_logger.error("Failed writing %s: %s", path, exc)

    def _get_call_id(self) -> str:
        with self._lock:
            self._call_counter += 1
            return f"{self.session_id}_{self._call_counter:06d}"

    def start_interaction(
        self,
        interaction_number: int,
        user_message: str,
        session_id: str,
        sigrid_location: str = "home",
    ) -> None:
        """Open a new interaction log — the Norn picks up her thread."""
        self.current_interaction = InteractionLog(
            interaction_number=interaction_number,
            timestamp=datetime.now().isoformat(),
            user_message=user_message,
            session_id=session_id,
            sigrid_location=sigrid_location,
        )
        self.main_logger.info("=== INTERACTION %s START ===", interaction_number)
        self.main_logger.info("Session: %s | Location: %s", session_id, sigrid_location)
        self.crash_reporter.trace_event(
            category="interaction",
            message="interaction_start",
            details={
                "interaction_number": interaction_number,
                "session_id": session_id,
                "location": sigrid_location,
                "message_preview": (user_message or "")[:250],
            },
        )

    def end_interaction(self, sigrid_response: str = "") -> None:
        """Close the interaction log and flush to disk — Urd records what was."""
        if not self.current_interaction:
            return
        self.current_interaction.sigrid_response = sigrid_response
        self.main_logger.info(
            "=== INTERACTION %s END ===", self.current_interaction.interaction_number
        )
        turn_file = (
            self.session_dir
            / f"interaction_{self.current_interaction.interaction_number:04d}.json"
        )
        self._safe_json_dump(turn_file, asdict(self.current_interaction))
        self.interaction_logs.append(self.current_interaction)
        self.current_interaction = None

    def log_ai_call(
        self,
        model_tier: str,
        call_type: str,
        prompt: str,
        response: str,
        context: Optional[Dict[str, Any]] = None,
        processing_time: float = 0.0,
        success: bool = True,
        error: Optional[str] = None,
        data_sources: Optional[List[str]] = None,
        data_path: Optional[List[str]] = None,
    ) -> str:
        """Record an AI model call — every raven's flight is noted."""
        call_id = self._get_call_id()
        call_log = AICallLog(
            timestamp=datetime.now().isoformat(),
            call_id=call_id,
            model_tier=model_tier,
            call_type=call_type,
            prompt_length=len(prompt or ""),
            prompt_preview=(prompt or "")[:500],
            full_prompt=prompt or "",
            context_keys=list((context or {}).keys()),
            response_length=len(response or ""),
            response_preview=(response or "")[:500],
            full_response=response or "",
            processing_time=processing_time,
            success=success,
            error=error,
            data_sources=data_sources or [],
            data_path=data_path or [],
        )

        self.ai_logger.info(
            "[%s] TIER=%s TYPE=%s SUCCESS=%s", call_id, model_tier, call_type, success
        )
        self.ai_logger.debug("[%s] PROMPT: %s", call_id, call_log.full_prompt)
        self.ai_logger.debug("[%s] RESPONSE: %s", call_id, call_log.full_response)
        if error:
            self.ai_logger.error("[%s] ERROR: %s", call_id, error)

        if data_path:
            self.path_logger.info("[%s] PATH: %s", call_id, " -> ".join(data_path))
        if data_sources:
            self.path_logger.info("[%s] SOURCES: %s", call_id, ", ".join(data_sources))

        if self.current_interaction:
            self.current_interaction.ai_calls.append(call_log)
            visits = self.current_interaction.model_tier_visits
            visits[model_tier] = visits.get(model_tier, 0) + 1

        self.crash_reporter.trace_event(
            category="ai_call",
            message=f"{model_tier}:{call_type}",
            severity="error" if not success else "info",
            details={
                "call_id": call_id,
                "model_tier": model_tier,
                "success": success,
                "prompt_length": call_log.prompt_length,
                "response_length": call_log.response_length,
                "processing_time": processing_time,
                "error": error,
            },
        )

        # Append to JSONL for cross-interaction crash recovery (Urðarbrunnr)
        try:
            jsonl_path = self.session_dir / "ai_calls.jsonl"
            with open(jsonl_path, "a", encoding="utf-8") as fh:
                fh.write(
                    json.dumps(asdict(call_log), default=str, ensure_ascii=False) + "\n"
                )
        except Exception as exc:
            self.error_logger.error("Failed appending AI call log: %s", exc)

        return call_id

    def log_memory_formation(
        self,
        memory_type: str,
        content: str,
        importance: int,
        tags: Optional[List[str]] = None,
        memory_payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record a new memory being woven into Sigrid's episodic store."""
        self.memory_logger.info(
            "MEMORY FORMED type=%s importance=%s tags=%s",
            memory_type, importance, tags or [],
        )
        self.memory_logger.debug("Content: %s", (content or "")[:1000])
        if memory_payload is not None:
            self.memory_logger.debug(
                "Payload: %s", json.dumps(memory_payload, default=str)[:2500]
            )
        if self.current_interaction:
            self.current_interaction.memories_formed.append({
                "type": memory_type,
                "content": content,
                "importance": importance,
                "tags": tags or [],
                "payload": memory_payload or {},
            })

    def log_state_change(self, key: str, old_value: Any, new_value: Any) -> None:
        """Record a state machine transition — the Wyrd weaving shifts."""
        self.main_logger.debug("STATE %s: %s -> %s", key, old_value, new_value)
        if self.current_interaction:
            self.current_interaction.state_changes[key] = {
                "from": old_value,
                "to": new_value,
            }

    def log_emotional_state(self, pad_vector: Dict[str, float]) -> None:
        """Snapshot the current PAD emotional coordinate into the interaction log."""
        self.main_logger.debug(
            "EMOTIONAL STATE P=%.3f A=%.3f D=%.3f",
            pad_vector.get("pleasure", 0.0),
            pad_vector.get("arousal", 0.0),
            pad_vector.get("dominance", 0.0),
        )
        if self.current_interaction:
            self.current_interaction.emotional_state = pad_vector

    def log_error(
        self,
        error: Exception,
        context: str = "",
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an error and send it to the crash reporter — no troll hides twice."""
        tb = traceback.format_exc()
        self.error_logger.error("ERROR in %s: %s", context, error)
        self.error_logger.error("TRACEBACK:\n%s", tb)
        if extra:
            self.error_logger.error("EXTRA: %s", json.dumps(extra, default=str))

        telemetry = {
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "interaction_number": getattr(
                self.current_interaction, "interaction_number", None
            ),
            "extra": extra or {},
        }
        self.crash_reporter.trace_event(
            category="error",
            message=f"{context}:{type(error).__name__}",
            severity="error",
            details=telemetry,
        )
        self.crash_reporter.report_exception(
            error, context or "comprehensive_logger", metadata=telemetry, tb_text=tb
        )
        if self.current_interaction:
            self.current_interaction.errors.append(f"{context}: {error}")

    def log_warning(self, message: str, context: str = "") -> None:
        self.error_logger.warning("WARNING in %s: %s", context, message)
        if self.current_interaction:
            self.current_interaction.warnings.append(f"{context}: {message}")


# ─── Decorator for AI-calling functions ───────────────────────────────────────

def log_ai_function(model_tier: str, call_type: str) -> Callable:
    """Decorator: automatically log entry/exit of AI-calling functions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import time
            start = time.time()
            comp_logger: Optional[ComprehensiveLogger] = getattr(
                wrapper, "_comprehensive_logger", None
            )
            try:
                result = func(*args, **kwargs)
                if comp_logger:
                    comp_logger.log_ai_call(
                        model_tier=model_tier,
                        call_type=call_type,
                        prompt=str(kwargs.get("prompt", args[0] if args else "")),
                        response=result if isinstance(result, str) else str(result),
                        processing_time=time.time() - start,
                        success=True,
                    )
                return result
            except Exception as exc:
                if comp_logger:
                    comp_logger.log_error(exc, f"{model_tier}.{func.__name__}")
                    comp_logger.log_ai_call(
                        model_tier=model_tier,
                        call_type=call_type,
                        prompt=str(kwargs.get("prompt", "")),
                        response="",
                        processing_time=time.time() - start,
                        success=False,
                        error=str(exc),
                    )
                raise
        return wrapper
    return decorator


# ─── Singleton accessor ────────────────────────────────────────────────────────

_comprehensive_logger: Optional[ComprehensiveLogger] = None


def get_comprehensive_logger() -> ComprehensiveLogger:
    global _comprehensive_logger
    if _comprehensive_logger is None:
        _comprehensive_logger = ComprehensiveLogger()
    return _comprehensive_logger


def init_comprehensive_logger(logs_dir: str = "logs") -> ComprehensiveLogger:
    global _comprehensive_logger
    _comprehensive_logger = ComprehensiveLogger(logs_dir)
    return _comprehensive_logger
