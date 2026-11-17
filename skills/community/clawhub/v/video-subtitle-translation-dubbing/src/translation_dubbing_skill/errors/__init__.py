"""Unified error hierarchy for the translation-dubbing skill.

Every error raised by any subsystem inherits from :class:`SkillError` and
carries a canonical ``(stage, code, reason, context)`` 4-tuple so that the
OpenClaw runtime can uniformly route the failure back to the caller.

Design mapping
--------------

- ``stage``: which pipeline phase produced the error
  (``"input" | "parsing" | "translating" | "tts" | "aligning" | "muxing"``).
- ``code``: machine-readable error code, stable across releases.
- ``reason``: short human-readable summary (the ``Exception.args[0]``).
- ``context``: free-form dict with error-specific fields (entry indices,
  provider types, file paths, ...). Rendered via :meth:`SkillError.to_dict`
  with sensitive keys (``credential``, ``api_key``, ``authorization``)
  redacted to ``"***"`` regardless of case.

Each subclass fixes a default ``stage`` and ``code`` matching the
requirement it serves (R1.10–R1.12, R2.4–R2.7, R5.7–R5.9, R6.8–R6.10, R7.6,
R9.14–R9.15, R10.1–R10.5).

The error types themselves are deliberately simple: no state machine, no
magic. Subclasses exist to let callers ``except SubtitleParseError`` rather
than string-matching on ``code``.
"""

from __future__ import annotations

from typing import Any, ClassVar, Final, Literal, Mapping

SkillErrorStage = Literal[
    "input",
    "parsing",
    "translating",
    "tts",
    "aligning",
    "muxing",
]
"""Closed set of pipeline stages an error may originate from."""

_VALID_STAGES: Final[frozenset[str]] = frozenset(
    {"input", "parsing", "translating", "tts", "aligning", "muxing"}
)

# Case-insensitive set of context keys whose values must be redacted when
# an error object is serialized via ``to_dict``. Kept lowercase; lookups
# lowercase the candidate key before comparing.
_REDACTED_KEYS: Final[frozenset[str]] = frozenset(
    {"credential", "api_key", "authorization"}
)

_REDACTED_PLACEHOLDER: Final[str] = "***"


def _redact(value: Any) -> Any:
    """Recursively redact sensitive keys within an arbitrary structure.

    - ``Mapping`` values have their keys inspected case-insensitively; keys
      matching :data:`_REDACTED_KEYS` get replaced with ``"***"``. Other
      values are recursed into.
    - ``list`` / ``tuple`` values are recursed element-wise, preserving
      their container kind.
    - Everything else is returned as-is.

    The function never mutates its input.
    """
    if isinstance(value, Mapping):
        redacted: dict[Any, Any] = {}
        for key, inner in value.items():
            if isinstance(key, str) and key.lower() in _REDACTED_KEYS:
                redacted[key] = _REDACTED_PLACEHOLDER
            else:
                redacted[key] = _redact(inner)
        return redacted
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact(item) for item in value)
    return value


class SkillError(Exception):
    """Base class for every error raised by the translation-dubbing skill.

    All subclasses fix a default ``stage`` and ``code`` via class variables;
    individual instances may override ``stage``/``code`` at construction
    time when a subsystem reuses a subclass for a closely related failure.

    Attributes:
        stage: Pipeline stage the error originated from.
        code: Machine-readable error code.
        reason: Short human-readable summary.
        context: Arbitrary dict of error-specific fields. Sensitive keys
            are redacted by :meth:`to_dict`.
    """

    # Subclasses MUST override these two class variables.
    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "skill_error"

    def __init__(
        self,
        reason: str,
        *,
        context: dict[str, Any] | None = None,
        stage: SkillErrorStage | None = None,
        code: str | None = None,
    ) -> None:
        """Initialize a skill error.

        Args:
            reason: Short human-readable description of the failure.
            context: Optional dict of context fields; defaults to an empty
                dict so callers may always treat ``context`` as a ``dict``.
            stage: Override the class-level default stage.
            code: Override the class-level default code.
        """
        super().__init__(reason)
        resolved_stage: SkillErrorStage = stage if stage is not None else self.default_stage
        if resolved_stage not in _VALID_STAGES:
            raise ValueError(
                f"invalid stage {resolved_stage!r}; "
                f"expected one of {sorted(_VALID_STAGES)}"
            )
        self.stage: SkillErrorStage = resolved_stage
        self.code: str = code if code is not None else self.default_code
        self.reason: str = reason
        self.context: dict[str, Any] = dict(context) if context else {}

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict representation of the error.

        The returned dict always contains the four canonical keys
        ``code / stage / reason / context``; ``context`` is a deep copy of
        :attr:`context` with sensitive keys redacted to ``"***"``. The
        redaction walks recursively into nested dicts, lists, and tuples so
        that credentials embedded under ``extra.credential`` or similar
        structures are also masked.
        """
        return {
            "code": self.code,
            "stage": self.stage,
            "reason": self.reason,
            "context": _redact(self.context),
        }

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"{type(self).__name__}(code={self.code!r}, stage={self.stage!r}, "
            f"reason={self.reason!r}, context={self.context!r})"
        )


# ---------------------------------------------------------------------------
# Input stage errors (R1.10, R1.11, R1.12, R10.1–R10.4)
# ---------------------------------------------------------------------------


class ManifestParamMissingError(SkillError):
    """Required manifest parameter is missing (R1.10)."""

    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "manifest_param_missing"


class UnsupportedProcessingModeError(SkillError):
    """``processing_mode`` is not one of the enum values (R1.11)."""

    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "unsupported_processing_mode"


class UnsupportedProviderTypeError(SkillError):
    """Provider type is not in the manifest-declared enum (R1.12)."""

    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "unsupported_provider_type"


class VideoFileInaccessibleError(SkillError):
    """Video file path does not exist or is not readable (R10.1)."""

    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "video_file_inaccessible"


class SubtitleFileInaccessibleError(SkillError):
    """Subtitle file path does not exist or is not readable (R10.2)."""

    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "subtitle_file_inaccessible"


class UnsupportedVideoFormatError(SkillError):
    """Video extension is not in the manifest's supported list (R10.3)."""

    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "unsupported_video_format"


class UnsupportedSubtitleFormatError(SkillError):
    """Subtitle extension is neither ``.srt`` nor ``.vtt`` (R10.4)."""

    default_stage: ClassVar[SkillErrorStage] = "input"
    default_code: ClassVar[str] = "unsupported_subtitle_format"


# ---------------------------------------------------------------------------
# Parsing stage errors (R2.4, R2.5, R2.7)
# ---------------------------------------------------------------------------


class SubtitleParseError(SkillError):
    """Subtitle syntax is invalid (R2.4)."""

    default_stage: ClassVar[SkillErrorStage] = "parsing"
    default_code: ClassVar[str] = "subtitle_parse_error"


class InvalidTimestampError(SkillError):
    """Subtitle entry has ``start_ms > end_ms`` (R2.5)."""

    default_stage: ClassVar[SkillErrorStage] = "parsing"
    default_code: ClassVar[str] = "invalid_timestamp"


class NoEnglishSubtitleError(SkillError):
    """No English subtitle track could be located (R2.7)."""

    default_stage: ClassVar[SkillErrorStage] = "parsing"
    default_code: ClassVar[str] = "no_english_subtitle"


# ---------------------------------------------------------------------------
# Translating / TTS / provider-contract errors
# (R5.7–R5.9, R6.8–R6.10, R7.6)
# ---------------------------------------------------------------------------


class ProviderNotRegisteredError(SkillError):
    """Requested provider type has no implementation registered (R5.7, R6.8).

    The default ``stage`` is ``"translating"``; callers raising this from
    the TTS engine should pass ``stage="tts"`` explicitly.
    """

    default_stage: ClassVar[SkillErrorStage] = "translating"
    default_code: ClassVar[str] = "provider_not_registered"


class ProviderUnavailableError(SkillError):
    """Provider is unreachable or misconfigured (R5.8, R6.9).

    Default ``stage`` is ``"translating"``; override to ``"tts"`` when the
    failure surfaces from the TTS engine.
    """

    default_stage: ClassVar[SkillErrorStage] = "translating"
    default_code: ClassVar[str] = "provider_unavailable"


class TranslationError(SkillError):
    """Translation provider call failed after retries (R5.9)."""

    default_stage: ClassVar[SkillErrorStage] = "translating"
    default_code: ClassVar[str] = "translation_error"


class TTSError(SkillError):
    """TTS provider call failed after retries (R6.10)."""

    default_stage: ClassVar[SkillErrorStage] = "tts"
    default_code: ClassVar[str] = "tts_error"


class ProviderContractViolationError(SkillError):
    """Provider response violated the structural/semantic contract (R7.6).

    Default ``stage`` is ``"translating"``; override to ``"tts"`` when the
    violating provider is a TTS provider.
    """

    default_stage: ClassVar[SkillErrorStage] = "translating"
    default_code: ClassVar[str] = "provider_contract_violation"


# ---------------------------------------------------------------------------
# Muxing stage errors (R9.14, R9.15)
# ---------------------------------------------------------------------------


class VideoDecodeError(SkillError):
    """Input video stream failed to decode (R9.14)."""

    default_stage: ClassVar[SkillErrorStage] = "muxing"
    default_code: ClassVar[str] = "video_decode_error"


class OriginalAudioExtractionError(SkillError):
    """Original English audio track could not be extracted (R9.15)."""

    default_stage: ClassVar[SkillErrorStage] = "muxing"
    default_code: ClassVar[str] = "original_audio_extraction_error"


__all__ = [
    "SkillError",
    "SkillErrorStage",
    # input
    "ManifestParamMissingError",
    "UnsupportedProcessingModeError",
    "UnsupportedProviderTypeError",
    "VideoFileInaccessibleError",
    "SubtitleFileInaccessibleError",
    "UnsupportedVideoFormatError",
    "UnsupportedSubtitleFormatError",
    # parsing
    "SubtitleParseError",
    "InvalidTimestampError",
    "NoEnglishSubtitleError",
    # translating / tts / contract
    "ProviderNotRegisteredError",
    "ProviderUnavailableError",
    "TranslationError",
    "TTSError",
    "ProviderContractViolationError",
    # muxing
    "VideoDecodeError",
    "OriginalAudioExtractionError",
]
