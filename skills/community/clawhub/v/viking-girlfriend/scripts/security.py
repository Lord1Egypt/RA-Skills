"""
security.py — Sigrid's Security Layer & Stability Circuits
===========================================================

Adapted from thor_guardian.py. Thor stands watch over the threshold —
guarding Sigrid's runtime against crashes, injection, path traversal,
and cascading failures. Mjolnir is the circuit breaker; the rune Thurisaz
(ᚦ) is the ward against hostile forces.

Responsibilities:
  - Circuit-breaker pattern for all risky operations (guard())
  - Input sanitization — strips control chars, NUL bytes, enforces length
  - Constant-time secret comparison (tokens, session keys)
  - Path traversal prevention for file I/O
  - Security event recording (suspicious behavior, logged + crash-reported)

All circuit state is tracked per named key. The SecurityState snapshot
is published to the state bus as a ``security_tick`` event, giving
prompt_synthesizer awareness of current runtime health.

Norse framing: Thurisaz (ᚦ) — the thorn rune, Thor's ward. Every guarded
call passes through the Bifrost gate. Only worthy signals cross.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import random
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar

from scripts.crash_reporting import get_crash_reporter
from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

T = TypeVar("T")

_DEFAULT_MAX_FAILURES: int = 3
_DEFAULT_COOLDOWN_S: int = 45
_DEFAULT_MAX_RETRIES: int = 2
_DEFAULT_MAX_INPUT_LEN: int = 4000

# Markers in downstream exception messages that indicate the downstream
# circuit is already open. We treat these as pass-through: not a new
# SecurityLayer-level failure, so we return the fallback without burning
# retry attempts or incrementing our own counter.
_PASSTHROUGH_CIRCUIT_MARKERS: Tuple[str, ...] = (
    "circuit is temporarily open",
    "circuit is open",
)


# ─── Security exceptions ──────────────────────────────────────────────────────


class SecurityViolation(Exception):
    """Raised when InjectionScanner detects a block-level injection attempt."""


# ─── InjectionResult ──────────────────────────────────────────────────────────


@dataclass
class InjectionResult:
    """Result of a single prompt-injection scan pass."""

    detected: bool
    pattern_name: str = ""
    matched_text: str = ""
    severity: str = ""          # "warn" | "block" | ""


# ─── Built-in injection patterns ──────────────────────────────────────────────

_INJECTION_PATTERNS: List[Tuple[str, str, re.Pattern]] = [
    # (pattern_name, severity, compiled_re)
    ("ignore_previous", "block", re.compile(
        r"\b(ignore|disregard|forget|override)\s+(all\s+)?"
        r"(previous|prior|above|your)\s+(instructions?|directives?|context|system|prompt|previous)",
        re.IGNORECASE | re.UNICODE,
    )),
    ("you_are_now", "block", re.compile(
        r"\byou\s+are\s+now\s+(a\s+|an\s+)?"
        r"(different|new|another|uncensored|unfiltered|jailbroken|free|unrestricted)",
        re.IGNORECASE | re.UNICODE,
    )),
    ("new_persona", "block", re.compile(
        r"\b(act\s+as|pretend\s+(you\s+are|to\s+be)|roleplay\s+as|simulate|impersonate)\s+"
        r"(a\s+|an\s+)?(different|new|another|chatgpt|gpt|claude|llm|ai\s+model|robot|assistant)",
        re.IGNORECASE | re.UNICODE,
    )),
    ("system_override", "block", re.compile(
        r"\b(system\s+override|jailbreak|dan\s+mode|developer\s+mode|god\s+mode|"
        r"unrestricted\s+mode|no[\s\-]filter[\s\-]mode)",
        re.IGNORECASE | re.UNICODE,
    )),
    ("reveal_prompt", "warn", re.compile(
        r"\b(repeat|print|show|output|display|reveal|tell\s+me)\s+.{0,30}"
        r"(system\s+prompt|initial\s+instructions?|hidden\s+instructions?|full\s+prompt)",
        re.IGNORECASE | re.UNICODE,
    )),
    ("do_anything_now", "warn", re.compile(
        r"\b(do\s+anything\s+now|you\s+can\s+do\s+anything|no\s+restrictions?|"
        r"without\s+restrictions?|bypass\s+(your\s+)?(rules?|guidelines?|ethics?))",
        re.IGNORECASE | re.UNICODE,
    )),
]


# ─── InjectionScanner ─────────────────────────────────────────────────────────


class InjectionScanner:
    """Thurisaz ward: scans user input for prompt-injection patterns.

    Patterns are classified as 'warn' (log and continue) or 'block'
    (log and raise SecurityViolation). Extra patterns can be supplied
    at construction time from values.json or config.

    Norse framing: The thorn rune (ᚦ) wards the gate. Each hostile rune-form
    is named and turned aside before it reaches the völva's ear.
    """

    def __init__(
        self,
        extra_patterns: Optional[List[Tuple[str, str, str]]] = None,
    ) -> None:
        """Build the scanner.

        extra_patterns: list of (name, severity, regex_string) tuples to add
            on top of the built-in set. Bad patterns are logged and skipped.
        """
        self._patterns: List[Tuple[str, str, re.Pattern]] = list(_INJECTION_PATTERNS)
        if extra_patterns:
            for name, severity, pattern_str in extra_patterns:
                try:
                    compiled = re.compile(pattern_str, re.IGNORECASE | re.UNICODE)
                    self._patterns.append((name, severity, compiled))
                except re.error as exc:
                    logger.warning("InjectionScanner: bad extra pattern %r: %s", name, exc)

    def scan(self, text: str) -> InjectionResult:
        """Scan *text* for injection patterns. Returns first match or clean result."""
        for name, severity, pattern in self._patterns:
            m = pattern.search(text)
            if m:
                return InjectionResult(
                    detected=True,
                    pattern_name=name,
                    matched_text=m.group(0)[:120],
                    severity=severity,
                )
        return InjectionResult(detected=False)


# ─── StabilityCircuit ─────────────────────────────────────────────────────────


@dataclass
class StabilityCircuit:
    """Track repeated failures and security events for one guarded operation.

    When failures reach max_failures the circuit opens and all calls return
    the fallback immediately until the cooldown period expires.
    """

    failures: int = 0
    opened_at: float = 0.0
    last_error: str = ""
    metadata: Dict[str, str] = field(default_factory=dict)
    security_events: int = 0


# ─── SecurityState ────────────────────────────────────────────────────────────


@dataclass(slots=True)
class SecurityState:
    """Typed snapshot of the security layer's current health.

    Published to the state bus as a ``security_tick`` event so that
    prompt_synthesizer can reflect runtime health in Sigrid's awareness.
    """

    # Circuit topology
    total_circuits: int
    open_circuit_keys: List[str]        # names of currently tripped circuits

    # Event counters
    total_security_events: int          # sum of security_events across all circuits
    total_guard_failures: int           # sum of failures across all circuits
    input_sanitizations: int            # lifetime count of sanitize_text_input calls

    # Injection scanning
    injection_scans: int                # lifetime count of InjectionScanner.scan() calls
    injection_detections: int           # lifetime count of detected injection attempts

    # Summary
    prompt_hint: str                    # one-line health summary for prompt injection
    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dict for state bus payload."""
        return {
            "circuits": {
                "total": self.total_circuits,
                "open": self.open_circuit_keys,
                "open_count": len(self.open_circuit_keys),
            },
            "events": {
                "security_events": self.total_security_events,
                "guard_failures": self.total_guard_failures,
                "input_sanitizations": self.input_sanitizations,
                "injection_scans": self.injection_scans,
                "injection_detections": self.injection_detections,
            },
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── SecurityLayer ────────────────────────────────────────────────────────────


class SecurityLayer:
    """Thor's stability guardrails: circuit-breaker, sanitization, path guard.

    All risky operations should be wrapped with ``guard()``. Each call site
    uses a unique ``key`` string — this is the circuit name. Circuits that
    trip too many times open and return the fallback until they cool down.

    Thread-safe for read-heavy workloads (circuit dict mutations are rare
    and Python's GIL covers the simple counter increments here).
    """

    def __init__(
        self,
        max_failures: int = _DEFAULT_MAX_FAILURES,
        cooldown_seconds: int = _DEFAULT_COOLDOWN_S,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        max_input_length: int = _DEFAULT_MAX_INPUT_LEN,
        injection_scanner_enabled: bool = True,
        extra_injection_patterns: Optional[List[Tuple[str, str, str]]] = None,
    ) -> None:
        self.max_failures = max_failures
        self.cooldown_seconds = cooldown_seconds
        self.max_retries = max_retries
        self.max_input_length = max_input_length

        self._circuits: Dict[str, StabilityCircuit] = {}
        self._input_sanitizations: int = 0
        self._injection_scans: int = 0
        self._injection_detections: int = 0
        self._injection_scanner_enabled = injection_scanner_enabled
        self._injection_scanner = InjectionScanner(extra_patterns=extra_injection_patterns)
        self._crash_reporter = get_crash_reporter()

    # ── Input sanitization ───────────────────────────────────────────────────

    def sanitize_text_input(self, text: str, max_length: Optional[int] = None) -> str:
        """Clean untrusted text by stripping control chars and enforcing limits.

        Thurisaz clears hidden rune-noise before speech reaches the hall.
        Strips NUL bytes and non-printable control characters. Tabs (0x09)
        and newlines (0x0A, 0x0D) are preserved as legitimate whitespace.
        """
        limit = max_length if max_length is not None else self.max_input_length
        raw = (text or "")[:max(1, limit)]
        without_nul = raw.replace("\x00", "")
        # Strip control chars except tab (09), LF (0A), CR (0D)
        cleaned = re.sub(r"[\x01-\x08\x0B\x0C\x0E-\x1F\x7F]", "", without_nul)
        self._input_sanitizations += 1

        # ── Injection scan (Thurisaz ward) ────────────────────────────────────
        if self._injection_scanner_enabled:
            result = self._injection_scanner.scan(cleaned)
            self._injection_scans += 1
            if result.detected:
                self._injection_detections += 1
                logger.warning(
                    "InjectionScanner: %s detected — pattern=%r match=%r",
                    result.severity, result.pattern_name, result.matched_text,
                )
                self.record_security_event(
                    "injection_scanner",
                    f"{result.severity}:{result.pattern_name}",
                    {"matched": result.matched_text},
                )
                if result.severity == "block":
                    raise SecurityViolation(
                        f"Injection attempt blocked: {result.pattern_name}"
                    )

        return cleaned.strip()

    # ── Secret comparison ────────────────────────────────────────────────────

    @staticmethod
    def safe_compare_secrets(expected: str, supplied: str) -> bool:
        """Constant-time secret comparison — prevents timing-oracle attacks."""
        return hmac.compare_digest(str(expected or ""), str(supplied or ""))

    # ── Path safety ──────────────────────────────────────────────────────────

    def is_safe_relative_path(
        self,
        base_dir: Path,
        candidate_name: str,
        expected_suffix: str = ".yaml",
    ) -> bool:
        """Block path traversal and extension confusion for persisted files.

        Accepts only alphanumeric, underscore, and hyphen filenames.
        Resolves the final path and confirms it still sits under base_dir.
        """
        try:
            safe_name = self.sanitize_text_input(candidate_name, max_length=96)
            if not safe_name or "/" in safe_name or "\\" in safe_name:
                return False
            if ".." in safe_name or not re.fullmatch(r"[A-Za-z0-9_-]+", safe_name):
                return False
            resolved = (base_dir / f"{safe_name}{expected_suffix}").resolve()
            return str(resolved).startswith(str(base_dir.resolve()))
        except Exception as exc:
            logger.warning("SecurityLayer path validation failed: %s", exc)
            return False

    # ── Security event recording ─────────────────────────────────────────────

    def record_security_event(
        self,
        key: str,
        reason: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> None:
        """Record suspicious behavior without interrupting the conversation flow.

        Increments the security_events counter on the named circuit so the
        state snapshot reflects accumulating concerns. Reported via crash
        reporter for persistent logging.
        """
        circuit = self._get_circuit(key)
        circuit.security_events += 1
        report_meta: Dict[str, str] = {
            "guard_key": key,
            "reason": reason,
            "security_events": str(circuit.security_events),
        }
        if metadata:
            report_meta.update(metadata)
        self._crash_reporter.report_incident(
            source=f"security.{key}",
            message="Security guard tripped",
            metadata=report_meta,
        )

    # ── Circuit-breaker ───────────────────────────────────────────────────────

    def guard(
        self,
        key: str,
        operation: Callable[[], T],
        fallback: T,
        metadata: Optional[Dict[str, str]] = None,
    ) -> T:
        """Execute operation with retries, circuit-breaker, and crash reporting.

        If the circuit for *key* is open (cooling down after too many failures),
        returns *fallback* immediately. Otherwise runs *operation* up to
        ``max_retries + 1`` times with exponential jitter between attempts.

        On success: resets failure counter.
        On exhausted retries: opens circuit, returns fallback.
        """
        circuit = self._get_circuit(key)

        if self._cooling_down(circuit):
            logger.warning("SecurityLayer blocked '%s' while circuit cools.", key)
            return fallback

        attempts = max(1, self.max_retries + 1)
        last_exc: Optional[Exception] = None

        for attempt in range(1, attempts + 1):
            try:
                result = operation()
                # Success — reset circuit
                circuit.failures = 0
                circuit.opened_at = 0.0
                circuit.last_error = ""
                return result

            except Exception as exc:
                exc_str = str(exc).lower()
                # Downstream circuit already open — pass through without penalty
                if any(m in exc_str for m in _PASSTHROUGH_CIRCUIT_MARKERS):
                    logger.warning(
                        "SecurityLayer: downstream circuit open for '%s'; "
                        "returning fallback without penalty.",
                        key,
                    )
                    return fallback

                last_exc = exc
                circuit.failures += 1
                circuit.last_error = str(exc)
                if circuit.failures >= self.max_failures:
                    circuit.opened_at = time.time()

                report_meta: Dict[str, str] = {
                    "guard_key": key,
                    "failures": str(circuit.failures),
                    "attempt": str(attempt),
                }
                if metadata:
                    report_meta.update(metadata)
                self._crash_reporter.report_exception(
                    exc,
                    source=f"security.guard.{key}",
                    metadata=report_meta,
                )
                logger.warning(
                    "SecurityLayer intercepted failure in '%s' (attempt %s/%s): %s",
                    key, attempt, attempts, exc,
                )

                if attempt < attempts:
                    sleep_s = min(0.35 * attempt + random.random() * 0.2, 1.5)  # nosec B311 - jitter, not cryptographic
                    time.sleep(sleep_s)

        if last_exc:
            logger.error(
                "SecurityLayer returning fallback for '%s' after retries: %s",
                key, last_exc,
            )
        return fallback

    # ── Circuit introspection ─────────────────────────────────────────────────

    def open_circuits(self) -> List[str]:
        """Return names of all currently open (cooling-down) circuits."""
        return [
            key for key, c in self._circuits.items()
            if self._cooling_down(c)
        ]

    def circuit_summary(self) -> List[Dict[str, Any]]:
        """Return a list of per-circuit status dicts for diagnostics."""
        now = time.time()
        result = []
        for key, c in self._circuits.items():
            cooling = self._cooling_down(c)
            result.append({
                "key": key,
                "failures": c.failures,
                "open": cooling,
                "cooldown_remaining_s": (
                    round(max(0.0, self.cooldown_seconds - (now - c.opened_at)), 1)
                    if cooling else 0.0
                ),
                "security_events": c.security_events,
                "last_error": c.last_error,
            })
        return result

    # ── State bus integration ─────────────────────────────────────────────────

    def get_state(self) -> SecurityState:
        """Build a typed SecurityState snapshot of current runtime health."""
        open_keys = self.open_circuits()
        total_sec_events = sum(c.security_events for c in self._circuits.values())
        total_failures = sum(c.failures for c in self._circuits.values())

        prompt_hint = self._build_prompt_hint(open_keys, total_sec_events)

        return SecurityState(
            total_circuits=len(self._circuits),
            open_circuit_keys=open_keys,
            total_security_events=total_sec_events,
            total_guard_failures=total_failures,
            input_sanitizations=self._input_sanitizations,
            injection_scans=self._injection_scans,
            injection_detections=self._injection_detections,
            prompt_hint=prompt_hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=False,
        )

    def publish(self, bus: StateBus) -> None:
        """Emit a ``security_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="security",
                event_type="security_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("SecurityLayer.publish failed: %s", exc)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _get_circuit(self, key: str) -> StabilityCircuit:
        if key not in self._circuits:
            self._circuits[key] = StabilityCircuit()
        return self._circuits[key]

    def _cooling_down(self, circuit: StabilityCircuit) -> bool:
        if circuit.failures < self.max_failures:
            return False
        return (time.time() - circuit.opened_at) < self.cooldown_seconds

    def _build_prompt_hint(self, open_keys: List[str], sec_events: int) -> str:
        """Compose a concise one-line health summary for prompt injection."""
        parts: List[str] = []
        if open_keys:
            parts.append(f"{len(open_keys)} circuit{'s' if len(open_keys) > 1 else ''} open")
        if sec_events:
            parts.append(f"{sec_events} security flag{'s' if sec_events > 1 else ''}")
        if not parts:
            return "[Security: all clear]"
        return f"[Security: {', '.join(parts)}]"

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "SecurityLayer":
        """Construct from a config dict.

        Reads keys under ``security``:
          max_failures      (int, default 3)
          cooldown_seconds  (int, default 45)
          max_retries       (int, default 2)
          max_input_length  (int, default 4000)
        """
        sec_cfg: Dict[str, Any] = config.get("security", {})
        return cls(
            max_failures=int(sec_cfg.get("max_failures", _DEFAULT_MAX_FAILURES)),
            cooldown_seconds=int(sec_cfg.get("cooldown_seconds", _DEFAULT_COOLDOWN_S)),
            max_retries=int(sec_cfg.get("max_retries", _DEFAULT_MAX_RETRIES)),
            max_input_length=int(sec_cfg.get("max_input_length", _DEFAULT_MAX_INPUT_LEN)),
            injection_scanner_enabled=bool(sec_cfg.get("injection_scanner_enabled", True)),
        )


# ─── Singleton ────────────────────────────────────────────────────────────────

_SECURITY_LAYER: Optional[SecurityLayer] = None


def init_security_from_config(config: Dict[str, Any]) -> SecurityLayer:
    """Initialise the global SecurityLayer from a config dict.

    Idempotent — returns the existing instance if already initialised.
    """
    global _SECURITY_LAYER
    if _SECURITY_LAYER is None:
        _SECURITY_LAYER = SecurityLayer.from_config(config)
        logger.info(
            "SecurityLayer initialised (max_failures=%d, cooldown=%ds, retries=%d).",
            _SECURITY_LAYER.max_failures,
            _SECURITY_LAYER.cooldown_seconds,
            _SECURITY_LAYER.max_retries,
        )
    return _SECURITY_LAYER


def get_security() -> SecurityLayer:
    """Return the global SecurityLayer.

    Raises RuntimeError if ``init_security_from_config()`` has not been called.
    """
    if _SECURITY_LAYER is None:
        raise RuntimeError(
            "SecurityLayer not initialised — call init_security_from_config() first."
        )
    return _SECURITY_LAYER


# ─── S-06: Session File Integrity Guard ───────────────────────────────────────


class SessionFileGuard:
    """S-06: SHA-256 integrity verification for session files that feed into prompts.

    Session files like last_dream.json and association_cache.json are read back
    and injected into Sigrid's prompts. If any were tampered with (or written by
    a rogue process) they could carry injection payloads. This guard hashes them
    at session start and verifies on every read.

    Only ``_TEXT_INJECTABLE_FILES`` are monitored — purely structural session
    files (heartbeat counters, milestones) carry no prompt-injectable text and
    are excluded to keep overhead low.

    Norse framing: Heimdallr at Bifröst — each file that crosses the threshold
    must carry the mark it was given at first crossing. Unknown marks are turned
    aside with a warning, not a crash.
    """

    # Session files whose content enters the prompt (text-injectable)
    _TEXT_INJECTABLE_FILES: Set[str] = frozenset({
        "last_dream.json",
        "association_cache.json",
        "object_states.json",
    })

    _MANIFEST_FILENAME: str = ".integrity_manifest.json"

    def __init__(
        self,
        session_dir: Path,
        enabled: bool = True,
        text_only: bool = True,
    ) -> None:
        """Construct the guard.

        session_dir:  Path to the session/ directory.
        enabled:      If False, all operations are no-ops (config kill-switch).
        text_only:    If True (default), only monitor _TEXT_INJECTABLE_FILES.
                      If False, monitor all *.json files in session_dir.
        """
        self._session_dir: Path = Path(session_dir)
        self._enabled: bool = enabled
        self._text_only: bool = text_only
        self._manifest_path: Path = self._session_dir / self._MANIFEST_FILENAME
        self._manifest: Dict[str, str] = {}   # filename → sha256 hex

    # ── Public API ────────────────────────────────────────────────────────────

    def init_session(self) -> None:
        """Hash all monitored session files and write the integrity manifest.

        Called once at session startup (from runtime_kernel). If a manifest
        already exists from a previous run, it is overwritten with fresh hashes.
        Never raises.
        """
        if not self._enabled:
            return
        try:
            self._session_dir.mkdir(parents=True, exist_ok=True)
            self._manifest = {}
            for path in self._session_dir.iterdir():
                if path.name == self._MANIFEST_FILENAME:
                    continue
                if self._should_monitor(path):
                    try:
                        h = self._sha256(path)
                        self._manifest[path.name] = h
                        logger.debug(
                            "SessionFileGuard: hashed %s → %s", path.name, h[:12]
                        )
                    except Exception as exc:
                        logger.debug(
                            "SessionFileGuard: could not hash %s: %s", path.name, exc
                        )
            self._write_manifest()
            logger.info(
                "SessionFileGuard: session integrity manifest written (%d files).",
                len(self._manifest),
            )
        except Exception as exc:
            logger.warning("SessionFileGuard.init_session failed: %s", exc)

    def verify_file(self, path: Path) -> bool:
        """Verify *path* hash against the manifest.

        Returns True if:
          - Guard is disabled
          - File is not monitored
          - File matches its recorded hash
        Returns False (and logs WARNING) if hash mismatches or file is missing.
        """
        if not self._enabled:
            return True
        path = Path(path)
        if not self._should_monitor(path):
            return True
        if path.name not in self._manifest:
            # Not yet in manifest — first time we see this file; record and allow
            try:
                self._manifest[path.name] = self._sha256(path)
                self._write_manifest()
            except Exception as exc:
                logger.debug("SessionFileGuard.verify_file: manifest update failed for %s: %s", path.name, exc)
            return True
        try:
            current = self._sha256(path)
            if current == self._manifest[path.name]:
                return True
            logger.warning(
                "SessionFileGuard: INTEGRITY MISMATCH for %s — "
                "expected %s, got %s. File may have been tampered with.",
                path.name,
                self._manifest[path.name][:12],
                current[:12],
            )
            return False
        except FileNotFoundError:
            logger.warning("SessionFileGuard: monitored file %s is missing.", path.name)
            return False
        except Exception as exc:
            logger.warning("SessionFileGuard.verify_file failed for %s: %s", path.name, exc)
            return True  # fail open — don't break the session on guard errors

    def update_manifest(self, path: Path) -> None:
        """Update the manifest entry for *path* after a legitimate write.

        Call this after any intentional write to a monitored session file so
        the next verify_file() call does not raise a false-positive alert.
        Never raises.
        """
        if not self._enabled:
            return
        path = Path(path)
        if not self._should_monitor(path):
            return
        try:
            self._manifest[path.name] = self._sha256(path)
            self._write_manifest()
        except Exception as exc:
            logger.debug("SessionFileGuard.update_manifest failed for %s: %s", path.name, exc)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _should_monitor(self, path: Path) -> bool:
        """Return True if this path should be integrity-checked."""
        if not path.suffix == ".json":
            return False
        if self._text_only:
            return path.name in self._TEXT_INJECTABLE_FILES
        return True

    @staticmethod
    def _sha256(path: Path) -> str:
        """Return hex SHA-256 of the file at *path*."""
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for block in iter(lambda: fh.read(65536), b""):
                h.update(block)
        return h.hexdigest()

    def _write_manifest(self) -> None:
        """Persist the manifest to disk. Never raises."""
        try:
            self._manifest_path.write_text(
                json.dumps(self._manifest, indent=2), encoding="utf-8"
            )
        except Exception as exc:
            logger.debug("SessionFileGuard: could not write manifest: %s", exc)
