"""Skill entry-point orchestration (processing-mode dispatch).

:func:`run` is the async top-level function an OpenClaw runtime invokes
after loading the skill. It wires together every subsystem built in the
preceding tasks and dispatches on
:class:`~translation_dubbing_skill.models.ProcessingMode`:

* ``subtitle_and_dubbing`` — parse → translate → serialize → TTS →
  audio-align → mux_full.
* ``subtitle_only`` — parse → translate → serialize → mux_subtitle_only.
  The TTS engine and audio aligner are *never* instantiated and never
  invoked; no ``stage="tts"`` progress event is emitted.

The module is intentionally assembly code: every non-trivial decision
lives in the subsystem it belongs to. The only routing-specific logic
here is the processing-mode switch in step 5 of :func:`run`.

Dependency injection
--------------------

Every external collaborator — parser, serializer, translator, TTS engine,
audio aligner, muxer, progress reporter, registry, extractor, video
duration probe, and output-directory allocator — is exposed as a keyword
argument with a production-ready default. Callers (and property tests)
can override any of them without reaching into private state.

Design mapping: design §"技能入口（Entry）" and §"端到端顺序图".
Requirements: R1.9, R2.6, R2.7, R5.3, R6.3, R6.7, R8.7, R9.16, R10.5,
R11.1–R11.6.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any, Callable, Protocol

from translation_dubbing_skill.align.aligner import AudioAligner
from translation_dubbing_skill.entry.manifest import ManifestParams
from translation_dubbing_skill.errors import NoEnglishSubtitleError
from translation_dubbing_skill.models import (
    ProcessingMode,
    ProgressEvent,
    ProviderConfig,
    SkillResult,
    SubtitleEntry,
)
from translation_dubbing_skill.mux.muxer import VideoMuxer
from translation_dubbing_skill.progress.reporter import ProgressReporter
from translation_dubbing_skill.providers.registry import (
    ProviderRegistry,
    default_registry,
)
from translation_dubbing_skill.subtitle.extractor import extract_from_video
from translation_dubbing_skill.subtitle.parser import SubtitleParser
from translation_dubbing_skill.subtitle.serializer import SubtitleSerializer
from translation_dubbing_skill.translation.translator import Translator
from translation_dubbing_skill.tts.engine import TTSEngine

# ---------------------------------------------------------------------------
# Injectable types
# ---------------------------------------------------------------------------


class _ReporterLike(Protocol):
    """Minimal shape the entry needs from a progress reporter."""

    def report(self, event: ProgressEvent) -> None: ...  # pragma: no cover


#: Callable that reads the subtitle path's content and returns ``(text,
#: hint_format)``. Injected so tests can serve a canned SRT/VTT string
#: without hitting the filesystem.
SubtitleReaderFn = Callable[[Path], tuple[str, str | None]]


#: Callable that extracts the embedded English subtitle track from a
#: video and returns ``(text, hint_format)``. Default delegates to
#: :func:`translation_dubbing_skill.subtitle.extract_from_video`.
SubtitleExtractorFn = Callable[[Path], tuple[str, str]]


#: Callable that returns the video's total duration in milliseconds.
#: The default implementation shells out to ``ffprobe``; tests inject a
#: constant so they can run without ffmpeg.
DurationProbeFn = Callable[[Path], int]


#: Callable that yields a fresh, empty directory into which the skill
#: writes its subtitle + video artifacts. Defaults to
#: :func:`tempfile.mkdtemp`; tests inject a ``tmp_path`` fixture.
OutputDirFn = Callable[[], Path]


# ---------------------------------------------------------------------------
# Default collaborators
# ---------------------------------------------------------------------------


def _default_subtitle_reader(path: Path) -> tuple[str, str | None]:
    """Read ``path`` as UTF-8 and infer the format hint from the suffix.

    Returns a ``(text, hint_format)`` pair suitable for passing to
    :meth:`SubtitleParser.parse_auto`. ``hint_format`` is ``"srt"`` /
    ``"vtt"`` when the suffix is recognised, ``None`` otherwise (in
    which case the parser falls back to ``WEBVTT`` header sniffing).
    """
    suffix = path.suffix.lower().lstrip(".")
    hint: str | None
    if suffix == "srt":
        hint = "srt"
    elif suffix == "vtt":
        hint = "vtt"
    else:
        hint = None
    # ``errors="strict"`` on purpose: an unreadable subtitle file is a
    # parsing-stage failure, not something we should silently paper over.
    return path.read_text(encoding="utf-8"), hint


def _default_duration_probe(video_path: Path) -> int:
    """Return the video duration in ms via ``ffprobe``.

    Falls back to :class:`NoEnglishSubtitleError`-style failure handling
    for the same reasons the subtitle extractor does — the skill cannot
    proceed without knowing the target track length for the audio
    aligner. In practice this is only called on the
    ``subtitle_and_dubbing`` branch.
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(video_path),
        ],
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
        raise RuntimeError(
            f"ffprobe failed to read duration: path={str(video_path)!r} stderr={stderr!r}"
        )
    payload = json.loads(result.stdout.decode("utf-8", errors="replace"))
    raw_duration = payload.get("format", {}).get("duration")
    if raw_duration is None:
        raise RuntimeError(
            f"ffprobe did not report a duration for {str(video_path)!r}"
        )
    # ffprobe returns a decimal-string in seconds; convert to ms using
    # ``float`` + ``round`` so sub-millisecond precision snaps to the
    # nearest integer.
    return int(round(float(raw_duration) * 1000))


def _default_output_dir() -> Path:
    """Allocate a fresh temporary directory for the skill's outputs."""
    return Path(tempfile.mkdtemp(prefix="translation_dubbing_skill_"))


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


async def run(
    params: ManifestParams,
    *,
    reporter: _ReporterLike | None = None,
    registry: ProviderRegistry | None = None,
    parser: SubtitleParser | None = None,
    serializer: SubtitleSerializer | None = None,
    translator: Translator | None = None,
    tts_engine: TTSEngine | None = None,
    aligner: AudioAligner | None = None,
    muxer: VideoMuxer | None = None,
    subtitle_reader: SubtitleReaderFn | None = None,
    subtitle_extractor: SubtitleExtractorFn | None = None,
    duration_probe: DurationProbeFn | None = None,
    output_dir_factory: OutputDirFn | None = None,
) -> SkillResult:
    """Run the skill end-to-end for ``params`` and return the final result.

    The function is fully async so providers (both translation and TTS)
    can pipeline their HTTP calls through the adaptive scheduler without
    blocking the event loop.

    Args:
        params: Validated manifest parameters; typically produced by
            :func:`translation_dubbing_skill.entry.parse_manifest`.
        reporter: Optional progress reporter. When ``None``, no progress
            events are emitted (the coordinators handle ``None`` via
            the same shortcut).
        registry: Provider registry used to resolve translation / TTS
            provider types. Defaults to the module-level
            :data:`~translation_dubbing_skill.providers.default_registry`.
        parser: Subtitle parser. Defaults to a fresh :class:`SubtitleParser`.
        serializer: Subtitle serializer. Defaults to a fresh
            :class:`SubtitleSerializer`.
        translator: Translation coordinator. Defaults to a
            :class:`Translator` wired to ``registry`` + ``reporter``.
        tts_engine: TTS coordinator. Only instantiated (via the default)
            when ``params.processing_mode`` is ``subtitle_and_dubbing``
            (R6.7, R8.7). Callers providing a custom engine for
            ``subtitle_only`` will find it unused — a deliberate choice
            so the property tests can assert *zero* calls on an
            injected stub.
        aligner: Audio aligner. Same gating as ``tts_engine``.
        muxer: Video muxer. Defaults to :class:`VideoMuxer`.
        subtitle_reader: Reads an external subtitle path. Defaults to
            :func:`_default_subtitle_reader`.
        subtitle_extractor: Extracts the embedded English subtitle track
            from a video file. Defaults to
            :func:`translation_dubbing_skill.subtitle.extract_from_video`.
        duration_probe: Returns the video duration in ms. Only invoked
            on the ``subtitle_and_dubbing`` branch. Defaults to
            :func:`_default_duration_probe` (ffprobe-based).
        output_dir_factory: Allocates a fresh directory for the skill's
            output artefacts. Defaults to
            :func:`_default_output_dir` (``tempfile.mkdtemp``).

    Returns:
        :class:`SkillResult` carrying the muxed video path and the
        Chinese subtitle path (R9.16).

    Raises:
        SkillError: Any subsystem-level failure is bubbled unchanged so
            callers can route on the concrete subclass. The entry
            itself never wraps errors — subsystems already attach the
            right ``stage`` / ``code`` / ``context``.
    """
    # --- 1. Resolve collaborators. ---------------------------------------
    # Done up-front so the ``processing_mode`` branch below only has to
    # deal with *which* collaborators to call, never *how* to build them.
    registry = registry if registry is not None else default_registry
    parser = parser if parser is not None else SubtitleParser()
    serializer = serializer if serializer is not None else SubtitleSerializer()
    translator = translator if translator is not None else Translator(registry, reporter)
    muxer = muxer if muxer is not None else VideoMuxer()
    subtitle_reader = subtitle_reader if subtitle_reader is not None else _default_subtitle_reader
    subtitle_extractor = (
        subtitle_extractor if subtitle_extractor is not None else extract_from_video
    )
    duration_probe = duration_probe if duration_probe is not None else _default_duration_probe
    output_dir_factory = (
        output_dir_factory if output_dir_factory is not None else _default_output_dir
    )

    # Allocate a scratch directory for the output artefacts.
    output_dir = output_dir_factory()
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- 2. Stage: parsing (R11.1) ---------------------------------------
    _report(
        reporter,
        ProgressEvent(stage="parsing", message="字幕解析中"),
    )
    en_entries = _parse_subtitles(
        params=params,
        parser=parser,
        subtitle_reader=subtitle_reader,
        subtitle_extractor=subtitle_extractor,
    )

    # --- 3. Stage: translating (R11.2) -----------------------------------
    _report(
        reporter,
        ProgressEvent(
            stage="translating",
            message="翻译中",
            total=len(en_entries),
            completed=0,
        ),
    )
    translation_config = ProviderConfig(
        endpoint=params.translation_endpoint,
        credential=params.translation_credential,
        extra=dict(params.translation_extra),
    )
    zh_entries = await translator.translate(
        en_entries,
        provider_type=params.translation_provider,
        config=translation_config,
        rate_limit_config=params.translation_rate_limit,
        target_language=params.target_language,
        source_language=params.source_language,
    )

    # --- 4. Serialize both subtitle tracks to UTF-8 files. ---------------
    # The source subtitle format dictates the output format so round-trip
    # stays loss-less. ``_pick_format`` falls back to SRT when the user
    # didn't supply an external file (the extractor always returns SRT).
    output_format = _pick_format(
        external_subtitle_path=params.subtitle_path,
    )
    run_id = uuid.uuid4().hex[:12]
    en_subtitle_path = output_dir / f"en-{run_id}.{output_format}"
    zh_subtitle_path = output_dir / f"zh-{run_id}.{output_format}"
    _serialize(serializer, en_entries, en_subtitle_path, output_format)
    _serialize(serializer, zh_entries, zh_subtitle_path, output_format)

    # --- 5. Dispatch on processing mode. --------------------------------
    output_video_path = output_dir / f"output-{run_id}.mkv"

    if params.processing_mode is ProcessingMode.SUBTITLE_AND_DUBBING:
        # 5a. Stage: tts (R11.3). Construct + invoke TTS engine and
        # aligner eagerly — they are scoped to this branch (R6.7, R8.7).
        tts_engine = tts_engine if tts_engine is not None else TTSEngine(registry, reporter)
        aligner = aligner if aligner is not None else AudioAligner()

        _report(
            reporter,
            ProgressEvent(
                stage="tts",
                message="语音合成中",
                total=_count_non_empty(zh_entries),
                completed=0,
            ),
        )
        # ``tts_rate_limit`` is guaranteed non-None by parse_manifest in
        # this mode (R1.6 / R1.10 enforce the required knobs).
        assert params.tts_rate_limit is not None  # narrowed by manifest
        assert params.tts_provider is not None
        assert params.tts_endpoint is not None
        assert params.tts_credential is not None

        tts_config = ProviderConfig(
            endpoint=params.tts_endpoint,
            credential=params.tts_credential,
            extra=dict(params.tts_extra),
        )
        # Fallback to target_language code if voice_id is not explicitly given,
        # so target-language voice mapping takes effect in TTS providers (like Edge).
        effective_voice_id = params.voice_id or params.target_language
        clips = await tts_engine.synthesize(
            zh_entries,
            voice_id=effective_voice_id,
            provider_type=params.tts_provider,
            config=tts_config,
            rate_limit_config=params.tts_rate_limit,
        )

        video_duration_ms = duration_probe(params.video_path)
        aligned_audio_path = aligner.align(clips, video_duration_ms)

        # 5b. Stage: muxing (R11.5).
        _report(reporter, ProgressEvent(stage="muxing", message="视频合成中"))
        muxer.mux_full(
            input_video=params.video_path,
            aligned_zh_audio=aligned_audio_path,
            zh_subtitle=zh_subtitle_path,
            en_subtitle=en_subtitle_path,
            output_path=output_video_path,
        )
    else:
        # SUBTITLE_ONLY: do NOT instantiate TTS engine or aligner, do NOT
        # emit a tts stage event (R6.7, R8.7, R11.4). The ``tts_engine``
        # / ``aligner`` kwargs may still be passed by a caller, but they
        # remain unused here — property tests rely on that.
        _report(reporter, ProgressEvent(stage="muxing", message="视频合成中"))
        muxer.mux_subtitle_only(
            input_video=params.video_path,
            zh_subtitle=zh_subtitle_path,
            en_subtitle=en_subtitle_path,
            output_path=output_video_path,
        )

    # --- 6. Stage: done (R11.6) -----------------------------------------
    _report(
        reporter,
        ProgressEvent(
            stage="done",
            message="完成",
            extra={
                "output_video_path": str(output_video_path),
                "output_subtitle_path": str(zh_subtitle_path),
            },
        ),
    )

    return SkillResult(
        output_video_path=output_video_path,
        output_subtitle_path=zh_subtitle_path,
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _report(reporter: _ReporterLike | None, event: ProgressEvent) -> None:
    """Forward ``event`` to ``reporter`` if one is attached."""
    if reporter is None:
        return
    reporter.report(event)


def _parse_subtitles(
    *,
    params: ManifestParams,
    parser: SubtitleParser,
    subtitle_reader: SubtitleReaderFn,
    subtitle_extractor: SubtitleExtractorFn,
) -> list[SubtitleEntry]:
    """Produce the English subtitle entries from the manifest.

    When ``params.subtitle_path`` is set, the external file is read and
    parsed via the supplied ``subtitle_reader`` + parser. Otherwise the
    embedded English track is pulled from the video via
    ``subtitle_extractor`` (R2.6) and handed to the same parser. The
    extractor raises :class:`NoEnglishSubtitleError` when no such track
    exists (R2.7); we let that propagate unchanged.
    """
    if params.subtitle_path is not None:
        text, hint = subtitle_reader(params.subtitle_path)
        hint_literal = hint if hint in ("srt", "vtt") else None
        return parser.parse_auto(text, hint_format=hint_literal)  # type: ignore[arg-type]

    # No external subtitle — pull the embedded English track.
    text, fmt = subtitle_extractor(params.video_path)
    hint_literal = fmt if fmt in ("srt", "vtt") else None
    entries = parser.parse_auto(text, hint_format=hint_literal)  # type: ignore[arg-type]
    if not entries:
        # An empty result is indistinguishable from "no track" from the
        # skill's perspective — raise the same error so callers have a
        # uniform failure mode (R2.7).
        raise NoEnglishSubtitleError(
            "extracted English subtitle track is empty",
            context={"video_path": str(params.video_path)},
        )
    return entries


def _pick_format(*, external_subtitle_path: Path | None) -> str:
    """Return ``"srt"`` or ``"vtt"`` for the output subtitle files.

    Preserves the input format when an external subtitle was supplied;
    otherwise defaults to ``"srt"`` (matching what
    :func:`extract_from_video` produces).
    """
    if external_subtitle_path is None:
        return "srt"
    suffix = external_subtitle_path.suffix.lower().lstrip(".")
    if suffix == "vtt":
        return "vtt"
    return "srt"


def _serialize(
    serializer: SubtitleSerializer,
    entries: list[SubtitleEntry],
    output_path: Path,
    output_format: str,
) -> None:
    """Serialize ``entries`` and write to ``output_path`` using UTF-8."""
    if output_format == "vtt":
        content = serializer.to_vtt(entries)
    else:
        content = serializer.to_srt(entries)
    serializer.write_file(output_path, content)


def _count_non_empty(entries: list[SubtitleEntry]) -> int:
    """Count entries whose text is non-blank (matches TTS's own filter)."""
    return sum(1 for e in entries if e.text.strip())


__all__ = [
    "run",
    "SubtitleReaderFn",
    "SubtitleExtractorFn",
    "DurationProbeFn",
    "OutputDirFn",
]
