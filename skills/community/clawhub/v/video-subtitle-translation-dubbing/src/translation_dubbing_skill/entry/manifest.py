"""Manifest parameter parsing and validation.

This module turns the loosely-typed ``dict`` delivered by the OpenClaw
runtime (populated from the manifest YAML) into a strongly-typed
:class:`ManifestParams` record that the skill entry point can consume
without further defensive checks. Every validation error raised here is a
:class:`~translation_dubbing_skill.errors.SkillError` subclass so the
caller can route the failure exactly as it routes runtime errors from the
rest of the pipeline.

Design mapping: design §"技能入口 · Manifest" and §"自适应调度器 ·
ProviderRateLimitConfig"; requirements R1.2–R1.7, R1.10–R1.12,
R10.1–R10.4, R12.3, R12.4.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Mapping

from translation_dubbing_skill.errors import (
    ManifestParamMissingError,
    SubtitleFileInaccessibleError,
    UnsupportedProcessingModeError,
    UnsupportedProviderTypeError,
    UnsupportedSubtitleFormatError,
    UnsupportedVideoFormatError,
    VideoFileInaccessibleError,
)
from translation_dubbing_skill.models import (
    DEFAULT_PROCESSING_MODE,
    ProcessingMode,
)
from translation_dubbing_skill.scheduler.config import (
    PayloadUnit,
    ProviderRateLimitConfig,
)

# ---------------------------------------------------------------------------
# Enumerations and defaults
# ---------------------------------------------------------------------------

# Allowed provider-type identifiers, as declared by the manifest schema
# (R1.12, design §"清单文件 Schema"). Any value outside this set raises
# ``UnsupportedProviderTypeError`` — regardless of what the registry would
# accept at provider-resolution time. (R1.12 talks about manifest-schema
# enum, not runtime registration.)
ALLOWED_PROVIDER_TYPES: Final[tuple[str, ...]] = ("llm", "web", "edge", "minimax")

# Per-kind allowed provider types. Translation accepts only the generic
# ``llm``/``web`` pair; TTS additionally accepts ``edge`` (Microsoft Edge
# Read-Aloud) and ``minimax`` (MiniMax t2a_v2 HTTP). Kept separate from
# the global enum so the error messages remain accurate for each kind.
_ALLOWED_TRANSLATION_TYPES: Final[tuple[str, ...]] = ("llm", "web")
_ALLOWED_TTS_TYPES: Final[tuple[str, ...]] = ("llm", "web", "edge", "minimax")

# Allowed processing-mode strings, mirroring ``ProcessingMode``. Declared
# separately so the error message can list them as plain strings without
# the caller having to reach into the Enum.
ALLOWED_PROCESSING_MODES: Final[tuple[str, ...]] = tuple(m.value for m in ProcessingMode)

# Default video container formats accepted by the skill. Matches the
# manifest schema's ``supported_video_formats`` default (design §"清单
# 文件 Schema"). Comparisons are case-insensitive; values are stored
# lowercase and without a leading dot.
DEFAULT_SUPPORTED_VIDEO_FORMATS: Final[tuple[str, ...]] = (
    "mp4",
    "mkv",
    "mov",
    "webm",
    "avi",
    "flv",
    "ts",
    "wmv",
)

# Supported subtitle extensions (R10.4). Same normalization rules as for
# video formats.
_SUPPORTED_SUBTITLE_FORMATS: Final[tuple[str, ...]] = ("srt", "vtt")


# Default rate-limit configurations for each provider kind. Mirrors the
# manifest schema defaults in design §"清单文件 Schema". They are applied
# field-by-field to user-supplied overrides so callers can tweak a single
# knob without restating the entire object.

_DEFAULT_TRANSLATION_RATE_LIMIT: Final[Mapping[str, Any]] = {
    "batch_size_initial": 20,
    "batch_size_min": 1,
    "batch_size_max": 50,
    "payload_size_initial": 4000,
    "payload_size_min": 500,
    "payload_size_max": 32000,
    "payload_unit": "tokens",
    "concurrency_initial": 2,
    "concurrency_min": 1,
    "concurrency_max": 8,
    "max_retries": 5,
    "backoff_base_ms": 500,
    "backoff_jitter_ms": 300,
    "probe_up_every_n_success": 10,
    "supports_batch": True,
}

_DEFAULT_TTS_RATE_LIMIT: Final[Mapping[str, Any]] = {
    "batch_size_initial": 1,
    "batch_size_min": 1,
    "batch_size_max": 16,
    "payload_size_initial": 1000,
    "payload_size_min": 200,
    "payload_size_max": 5000,
    "payload_unit": "chars",
    "concurrency_initial": 4,
    "concurrency_min": 1,
    "concurrency_max": 16,
    "max_retries": 5,
    "backoff_base_ms": 500,
    "backoff_jitter_ms": 300,
    "probe_up_every_n_success": 10,
    "supports_batch": False,
}


# ---------------------------------------------------------------------------
# Parsed params container
# ---------------------------------------------------------------------------


@dataclass
class ManifestParams:
    """Validated manifest parameters handed to the skill entry point.

    The schema intentionally flattens the manifest into Python-native
    types so downstream subsystems can consume it without re-validating.

    Attributes:
        video_path: Path to the input video (R1.2).
        subtitle_path: Optional path to an external subtitle file. When
            ``None`` the skill extracts the embedded English subtitle
            stream from the video (R2.6).
        target_language: Target translation language identifier
            (fixed to ``"zh-CN"`` by the manifest schema).
        processing_mode: Selected pipeline mode (R1.3).
        voice_id: Optional voice identifier for TTS. Ignored under
            :data:`ProcessingMode.SUBTITLE_ONLY` (R1.7).
        translation_provider: Enum string identifying the translation
            provider implementation (R1.4).
        translation_endpoint: HTTP endpoint for the translation provider.
        translation_credential: Secret credential for the translation
            provider (redacted in logs and error contexts).
        translation_extra: Provider-specific key/value bag.
        translation_rate_limit: Fully-populated rate-limit configuration.
        tts_provider: Enum string identifying the TTS provider (may be
            ``None`` under :data:`ProcessingMode.SUBTITLE_ONLY`, R1.7).
        tts_endpoint: HTTP endpoint for the TTS provider (may be ``None``
            under ``SUBTITLE_ONLY``).
        tts_credential: Secret credential for the TTS provider
            (may be ``None`` under ``SUBTITLE_ONLY``).
        tts_extra: Provider-specific key/value bag for TTS.
        tts_rate_limit: Fully-populated rate-limit configuration; ``None``
            under ``SUBTITLE_ONLY`` (no TTS is invoked).
        supported_video_formats: List of accepted video extensions
            (lowercase, dot-free).
    """

    video_path: Path
    subtitle_path: Path | None
    target_language: str
    processing_mode: ProcessingMode
    voice_id: str | None
    translation_provider: str
    translation_endpoint: str
    translation_credential: str
    source_language: str = "en"
    translation_extra: dict[str, Any] = field(default_factory=dict)
    translation_rate_limit: ProviderRateLimitConfig = field(
        default_factory=lambda: ProviderRateLimitConfig(**_DEFAULT_TRANSLATION_RATE_LIMIT)
    )
    tts_provider: str | None = None
    tts_endpoint: str | None = None
    tts_credential: str | None = None
    tts_extra: dict[str, Any] = field(default_factory=dict)
    tts_rate_limit: ProviderRateLimitConfig | None = None
    supported_video_formats: list[str] = field(
        default_factory=lambda: list(DEFAULT_SUPPORTED_VIDEO_FORMATS)
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_ext(path: os.PathLike[str] | str) -> str:
    """Return the lowercase extension of ``path`` without the leading dot.

    ``Path("foo.MKV").suffix`` is ``".MKV"`` so we strip the dot and
    lowercase for stable comparison against the allowed lists.
    """
    suffix = Path(os.fspath(path)).suffix
    if not suffix:
        return ""
    # suffix starts with ".": drop it before lowercasing.
    return suffix[1:].lower()


def _require_str(
    value: Any,
    field_name: str,
    *,
    missing: list[str],
) -> str | None:
    """Coerce ``value`` to a non-empty ``str`` or record the missing field.

    Returns ``None`` and appends to ``missing`` when ``value`` is ``None``,
    not a ``str``, or a blank string. The caller is expected to raise
    :class:`ManifestParamMissingError` after collecting all missing names.
    """
    if value is None:
        missing.append(field_name)
        return None
    if not isinstance(value, str):
        missing.append(field_name)
        return None
    if value.strip() == "":
        missing.append(field_name)
        return None
    return value


def _merge_rate_limit(
    user: Mapping[str, Any] | None,
    defaults: Mapping[str, Any],
    *,
    field_name: str,
) -> ProviderRateLimitConfig:
    """Merge user-provided rate-limit dict with ``defaults`` and validate.

    Construction delegates to :class:`ProviderRateLimitConfig`, whose
    ``__post_init__`` enforces the scheduler's invariants (R12.3, R12.4,
    and ``batch_size_min <= initial <= max`` on every dimension). A
    ``ValueError`` from that validation is re-raised as a
    :class:`ManifestParamMissingError` carrying the offending field path,
    so callers get the same shape of error whether the value was missing
    outright or merely out of range.
    """
    merged: dict[str, Any] = dict(defaults)
    if user is not None:
        if not isinstance(user, Mapping):
            raise ManifestParamMissingError(
                f"{field_name} must be an object",
                context={"field": field_name, "given_type": type(user).__name__},
            )
        # Copy user fields over the defaults so any field the caller does
        # not mention keeps its default (design §"清单文件 Schema" →
        # "声明齐全且默认值落在合法区间").
        for key, value in user.items():
            merged[key] = value
    try:
        return ProviderRateLimitConfig(**merged)
    except TypeError as exc:
        # ``TypeError`` here means an unknown field was passed in. Treat
        # it the same way as a malformed manifest entry.
        raise ManifestParamMissingError(
            f"{field_name} has an invalid field: {exc}",
            context={"field": field_name, "detail": str(exc)},
        ) from exc
    except ValueError as exc:
        raise ManifestParamMissingError(
            f"{field_name} failed validation: {exc}",
            context={"field": field_name, "detail": str(exc)},
        ) from exc


def _validate_video_path(
    raw: Any,
    *,
    supported: list[str],
) -> Path:
    """Check ``raw`` is a readable video path with a supported extension.

    Order of checks matches the requirements:
    R10.3 (format) fires before R10.1 (accessibility) so that a wrong
    extension is reported as a format error rather than being masked by
    "file not found" errors when the caller passes a non-existent path
    with an unsupported extension. The design's requirement-level
    ordering (R10 sequence) does not pin a precedence, but flagging the
    format problem first is strictly more informative.
    """
    if raw is None or not isinstance(raw, (str, os.PathLike)):
        raise ManifestParamMissingError(
            "video_path is required",
            context={"missing_fields": ["video_path"]},
        )
    path = Path(os.fspath(raw))
    ext = _normalize_ext(path)
    supported_lower = [s.lower().lstrip(".") for s in supported]
    if ext not in supported_lower:
        raise UnsupportedVideoFormatError(
            f"unsupported video format: {ext!r}",
            context={
                "given_ext": ext,
                "supported": list(supported_lower),
                "path": str(path),
            },
        )
    if not path.exists() or not path.is_file() or not os.access(path, os.R_OK):
        raise VideoFileInaccessibleError(
            f"video file is not accessible: {path}",
            context={"path": str(path)},
        )
    return path


def _validate_subtitle_path(raw: Any) -> Path | None:
    """Return the validated subtitle path or ``None`` if the caller omitted it.

    Matches the same ordering rationale as :func:`_validate_video_path`:
    format first (R10.4), then accessibility (R10.2). Unsupported
    extensions short-circuit before touching the filesystem.
    """
    if raw is None:
        return None
    if not isinstance(raw, (str, os.PathLike)):
        raise SubtitleFileInaccessibleError(
            "subtitle_path must be a path-like value",
            context={"given_type": type(raw).__name__},
        )
    path = Path(os.fspath(raw))
    ext = _normalize_ext(path)
    if ext not in _SUPPORTED_SUBTITLE_FORMATS:
        raise UnsupportedSubtitleFormatError(
            f"unsupported subtitle format: {ext!r}",
            context={
                "given_ext": ext,
                "supported": list(_SUPPORTED_SUBTITLE_FORMATS),
                "path": str(path),
            },
        )
    if not path.exists() or not path.is_file() or not os.access(path, os.R_OK):
        raise SubtitleFileInaccessibleError(
            f"subtitle file is not accessible: {path}",
            context={"path": str(path)},
        )
    return path


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def parse_manifest(
    params: Mapping[str, Any],
    *,
    video_format_check: bool = True,
) -> ManifestParams:
    """Validate ``params`` and return a :class:`ManifestParams` record.

    Args:
        params: Raw parameter dict as delivered by the OpenClaw runtime.
        video_format_check: When ``True`` (default), enforce R10.3 against
            the caller-provided (or default) ``supported_video_formats``.
            Tests that synthesize fake video paths can disable this to
            bypass the existence check on the path.

    Raises:
        UnsupportedProcessingModeError: ``processing_mode`` is not one of
            :data:`ALLOWED_PROCESSING_MODES` (R1.11, P31).
        UnsupportedProviderTypeError: A provider-type enum value is not
            one of :data:`ALLOWED_PROVIDER_TYPES` (R1.12, P11).
        ManifestParamMissingError: A required field is missing or an
            included field failed range/type validation (R1.10, R1.6,
            R12.3, R12.4, P30).
        UnsupportedVideoFormatError: Video extension not in the supported
            list (R10.3, P22).
        UnsupportedSubtitleFormatError: Subtitle extension not ``.srt``
            or ``.vtt`` (R10.4, P23).
        VideoFileInaccessibleError: Video path missing or unreadable
            (R10.1).
        SubtitleFileInaccessibleError: External subtitle path missing or
            unreadable (R10.2).

    Returns:
        A fully-validated :class:`ManifestParams` instance.
    """
    if not isinstance(params, Mapping):
        raise ManifestParamMissingError(
            "manifest params must be a mapping",
            context={"given_type": type(params).__name__},
        )

    # ---- processing_mode (R1.3, R1.11, P31) ----------------------------------
    raw_mode = params.get("processing_mode")
    if raw_mode is None:
        processing_mode = DEFAULT_PROCESSING_MODE
    else:
        if not isinstance(raw_mode, (str, ProcessingMode)):
            raise UnsupportedProcessingModeError(
                f"processing_mode must be a string, got {type(raw_mode).__name__}",
                context={
                    "requested_mode": raw_mode,
                    "allowed_modes": list(ALLOWED_PROCESSING_MODES),
                },
            )
        mode_value = raw_mode.value if isinstance(raw_mode, ProcessingMode) else raw_mode
        if mode_value not in ALLOWED_PROCESSING_MODES:
            raise UnsupportedProcessingModeError(
                f"unsupported processing_mode: {mode_value!r}; "
                f"allowed: {list(ALLOWED_PROCESSING_MODES)}",
                context={
                    "requested_mode": mode_value,
                    "allowed_modes": list(ALLOWED_PROCESSING_MODES),
                },
            )
        processing_mode = ProcessingMode(mode_value)

    # ---- supported_video_formats --------------------------------------------
    supported_formats_raw = params.get("supported_video_formats")
    if supported_formats_raw is None:
        supported_video_formats = list(DEFAULT_SUPPORTED_VIDEO_FORMATS)
    else:
        if not isinstance(supported_formats_raw, (list, tuple)) or not all(
            isinstance(v, str) for v in supported_formats_raw
        ):
            raise ManifestParamMissingError(
                "supported_video_formats must be a list of strings",
                context={"field": "supported_video_formats"},
            )
        supported_video_formats = [v.lower().lstrip(".") for v in supported_formats_raw]

    # ---- translation_provider (R1.4, R1.12) ---------------------------------
    translation_provider_raw = params.get("translation_provider")
    translation_provider = _validate_provider_enum(
        translation_provider_raw, kind="translation", field_name="translation_provider"
    )

    # ---- translation_endpoint / credential / extra (R1.4, R1.10) ------------
    missing: list[str] = []
    translation_endpoint = _require_str(
        params.get("translation_endpoint"),
        "translation_endpoint",
        missing=missing,
    )
    translation_credential = _require_str(
        params.get("translation_credential"),
        "translation_credential",
        missing=missing,
    )
    if missing:
        raise ManifestParamMissingError(
            f"missing required translation fields: {missing}",
            context={
                "missing_fields": missing,
                "processing_mode": processing_mode.value,
            },
        )
    translation_extra = _coerce_extra(
        params.get("translation_extra"), field_name="translation_extra"
    )
    translation_rate_limit = _merge_rate_limit(
        params.get("translation_rate_limit"),
        _DEFAULT_TRANSLATION_RATE_LIMIT,
        field_name="translation_rate_limit",
    )

    # ---- source_language (R1.2) ---------------------------------------------
    raw_source = params.get("source_language", "en")
    if not isinstance(raw_source, str) or raw_source.strip() == "":
        raise ManifestParamMissingError(
            "source_language must be a non-empty string",
            context={"missing_fields": ["source_language"]},
        )
    source_language = raw_source

    # ---- target_language (R1.2) ---------------------------------------------
    raw_target = params.get("target_language", "zh-CN")
    if not isinstance(raw_target, str) or raw_target.strip() == "":
        raise ManifestParamMissingError(
            "target_language must be a non-empty string",
            context={"missing_fields": ["target_language"]},
        )
    target_language = raw_target

    # ---- TTS params (R1.6, R1.7, R1.10, P30) --------------------------------
    tts_provider: str | None = None
    tts_endpoint: str | None = None
    tts_credential: str | None = None
    tts_extra: dict[str, Any] = {}
    tts_rate_limit: ProviderRateLimitConfig | None = None
    voice_id: str | None = None

    if processing_mode is ProcessingMode.SUBTITLE_AND_DUBBING:
        # Collect every missing TTS field first (R1.6, R1.10, P30). A
        # *present but blank* provider string is treated as missing too,
        # matching the behavior of the other two required strings — a
        # caller who supplies ``""`` has effectively not supplied the
        # field. Only a non-blank, non-enum value triggers
        # ``UnsupportedProviderTypeError`` (R1.12, P11).
        missing_tts: list[str] = []
        tts_provider_raw = params.get("tts_provider")
        if tts_provider_raw is None or (
            isinstance(tts_provider_raw, str) and tts_provider_raw.strip() == ""
        ):
            missing_tts.append("tts_provider")
            tts_provider = None
        else:
            tts_provider = _validate_provider_enum(
                tts_provider_raw, kind="tts", field_name="tts_provider"
            )

        tts_endpoint = _require_str(
            params.get("tts_endpoint"), "tts_endpoint", missing=missing_tts
        )
        tts_credential = _require_str(
            params.get("tts_credential"), "tts_credential", missing=missing_tts
        )
        if missing_tts:
            raise ManifestParamMissingError(
                f"missing required TTS fields under subtitle_and_dubbing: {missing_tts}",
                context={
                    "missing_fields": missing_tts,
                    "processing_mode": processing_mode.value,
                },
            )
        tts_extra = _coerce_extra(params.get("tts_extra"), field_name="tts_extra")
        tts_rate_limit = _merge_rate_limit(
            params.get("tts_rate_limit"),
            _DEFAULT_TTS_RATE_LIMIT,
            field_name="tts_rate_limit",
        )

        raw_voice = params.get("voice_id")
        if raw_voice is not None:
            if not isinstance(raw_voice, str):
                raise ManifestParamMissingError(
                    "voice_id must be a string when provided",
                    context={"field": "voice_id"},
                )
            voice_id = raw_voice if raw_voice != "" else None
    # SUBTITLE_ONLY: tts_* and voice_id are ignored entirely (R1.7).

    # ---- video / subtitle paths (R10.1, R10.2, R10.3, R10.4) ----------------
    if video_format_check:
        video_path = _validate_video_path(
            params.get("video_path"), supported=supported_video_formats
        )
    else:
        raw_video = params.get("video_path")
        if raw_video is None or not isinstance(raw_video, (str, os.PathLike)):
            raise ManifestParamMissingError(
                "video_path is required",
                context={"missing_fields": ["video_path"]},
            )
        video_path = Path(os.fspath(raw_video))

    subtitle_path = _validate_subtitle_path(params.get("subtitle_path"))

    return ManifestParams(
        video_path=video_path,
        subtitle_path=subtitle_path,
        source_language=source_language,
        target_language=target_language,
        processing_mode=processing_mode,
        voice_id=voice_id,
        translation_provider=translation_provider,
        translation_endpoint=translation_endpoint,  # type: ignore[arg-type]
        translation_credential=translation_credential,  # type: ignore[arg-type]
        translation_extra=translation_extra,
        translation_rate_limit=translation_rate_limit,
        tts_provider=tts_provider,
        tts_endpoint=tts_endpoint,
        tts_credential=tts_credential,
        tts_extra=tts_extra,
        tts_rate_limit=tts_rate_limit,
        supported_video_formats=supported_video_formats,
    )


def _validate_provider_enum(
    raw: Any,
    *,
    kind: str,
    field_name: str,
) -> str:
    """Validate ``raw`` is a string and belongs to the per-kind enum.

    Translation accepts ``{llm, web}``; TTS additionally accepts
    ``edge``. The error context always carries the allowed list for the
    *current* kind so the end-user sees the right set of choices.
    """
    allowed = (
        _ALLOWED_TTS_TYPES if kind == "tts" else _ALLOWED_TRANSLATION_TYPES
    )
    if raw is None:
        raise ManifestParamMissingError(
            f"{field_name} is required",
            context={"missing_fields": [field_name], "kind": kind},
        )
    if not isinstance(raw, str):
        raise UnsupportedProviderTypeError(
            f"{field_name} must be a string; got {type(raw).__name__}",
            context={
                "requested_type": raw,
                "allowed_types": list(allowed),
                "kind": kind,
            },
        )
    if raw not in allowed:
        raise UnsupportedProviderTypeError(
            f"unsupported {field_name}: {raw!r}; allowed: {list(allowed)}",
            context={
                "requested_type": raw,
                "allowed_types": list(allowed),
                "kind": kind,
            },
        )
    return raw


def _coerce_extra(raw: Any, *, field_name: str) -> dict[str, Any]:
    """Return a plain-``dict`` copy of ``raw`` or an empty dict when absent."""
    if raw is None:
        return {}
    if not isinstance(raw, Mapping):
        raise ManifestParamMissingError(
            f"{field_name} must be an object",
            context={"field": field_name, "given_type": type(raw).__name__},
        )
    return dict(raw)


__all__ = [
    "ManifestParams",
    "parse_manifest",
    "ALLOWED_PROCESSING_MODES",
    "ALLOWED_PROVIDER_TYPES",
    "DEFAULT_SUPPORTED_VIDEO_FORMATS",
]
