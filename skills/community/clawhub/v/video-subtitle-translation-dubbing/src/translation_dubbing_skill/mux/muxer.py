"""Audio/video muxing for the two processing modes.

``VideoMuxer`` exposes two methods, one per processing mode:

* :meth:`VideoMuxer.mux_full` — ``subtitle_and_dubbing`` mode. Emits an
  ``.mkv`` with the original video stream (``copy``), two audio streams
  (Chinese dub encoded to AAC as the default track, original English
  ``copy`` as non-default), and two subtitle streams (Chinese ``default``,
  English non-default). Language tags are ``zho`` / ``eng``.

* :meth:`VideoMuxer.mux_subtitle_only` — ``subtitle_only`` mode. Emits an
  ``.mkv`` with the original video and audio streams (``copy``, English
  as the sole audio track) plus both subtitle streams (Chinese default,
  English non-default). No Chinese dub track is generated.

Both methods accept an optional ``runner`` callable so unit and property
tests can stub out the real ``ffmpeg`` subprocess. The default runner
shells out to ``ffmpeg`` via :func:`subprocess.run`.

Error handling
--------------

``ffmpeg`` failures are inspected using a small classifier:

* A non-zero exit with ``Invalid data found when processing input`` or
  similar on the video stream surfaces as :class:`VideoDecodeError`
  (R9.14).
* A non-zero exit that clearly points at the original audio stream
  surfaces as :class:`OriginalAudioExtractionError` (R9.15).

Anything else re-raises the underlying :class:`RuntimeError` so the caller
can bubble a generic muxing failure.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable, Sequence

from translation_dubbing_skill.errors import (
    OriginalAudioExtractionError,
    VideoDecodeError,
)

#: Callable signature for the pluggable ffmpeg runner.
#:
#: The runner takes the full argv for an ``ffmpeg`` invocation and returns
#: a :class:`subprocess.CompletedProcess`. Tests inject a stub that writes
#: a dummy ``.mkv``-like payload to the output path without invoking the
#: real toolchain.
Runner = Callable[[Sequence[str]], "subprocess.CompletedProcess[bytes]"]


def _default_runner(cmd: Sequence[str]) -> "subprocess.CompletedProcess[bytes]":
    """Default ffmpeg runner: shell out via :func:`subprocess.run`."""
    return subprocess.run(list(cmd), capture_output=True)


def _as_ffmpeg_path(path: Path | str) -> str:
    """Convert ``path`` to a form ffmpeg will not misinterpret.

    ffmpeg ≥ 6.0 treats bare paths containing ``[``, ``?``, ``%``, ``:``
    and similar characters as protocol specifiers or glob patterns,
    which breaks outputs for YouTube-style filenames like
    ``Title [videoid].mkv``. Prefixing the absolute path with
    ``file:`` disables that parsing and forces the file protocol.

    Returns:
        The path rendered as ``file:<absolute>`` — safe to use in any
        position where ffmpeg expects a filename (``-i`` input,
        trailing output argument, etc.).
    """
    return "file:" + str(Path(path).resolve())


def _classify_failure(stderr: str) -> type[VideoDecodeError] | type[OriginalAudioExtractionError] | None:
    """Classify an ``ffmpeg`` stderr snippet into a specific error type.

    Returns the error class to raise, or ``None`` if the stderr doesn't
    match any of the well-known patterns (caller then raises a generic
    ``RuntimeError`` so the failure still propagates).
    """
    lower = stderr.lower()
    # Heuristic ordering: check audio-extraction markers before generic
    # video-decode markers so a "can't find audio stream" error is not
    # mis-classified as a video-decode failure.
    audio_markers = (
        "stream map '0:a",
        "does not contain any stream",
        "no audio stream",
        "cannot find audio",
    )
    if any(marker in lower for marker in audio_markers):
        return OriginalAudioExtractionError
    video_markers = (
        "invalid data found when processing input",
        "could not find codec parameters for stream 0",
        "decoder not found",
    )
    if any(marker in lower for marker in video_markers):
        return VideoDecodeError
    return None


def _raise_for_failure(
    cmd: Sequence[str],
    completed: "subprocess.CompletedProcess[bytes]",
) -> None:
    """Raise an appropriate :class:`SkillError` if ``completed`` failed."""
    if completed.returncode == 0:
        return
    stderr = completed.stderr.decode("utf-8", errors="replace") if completed.stderr else ""
    err_cls = _classify_failure(stderr)
    context = {
        "command": list(cmd),
        "returncode": completed.returncode,
        "stderr": stderr,
    }
    if err_cls is VideoDecodeError:
        raise VideoDecodeError(
            "input video could not be decoded by ffmpeg",
            context=context,
        )
    if err_cls is OriginalAudioExtractionError:
        raise OriginalAudioExtractionError(
            "original English audio track could not be extracted",
            context=context,
        )
    # Unknown failure mode — let the caller see the raw error.
    raise RuntimeError(
        f"ffmpeg exited with {completed.returncode}: stderr={stderr!r}"
    )


class VideoMuxer:
    """Assemble the final ``.mkv`` output for both processing modes.

    Args:
        runner: Optional ffmpeg runner. Defaults to :func:`_default_runner`
            which shells out to the system ``ffmpeg``. Tests inject a
            stub that fabricates an output file without invoking the
            real toolchain. Can also be overridden per-call via the
            ``runner=`` argument on :meth:`mux_full` / :meth:`mux_subtitle_only`.
    """

    def __init__(self, runner: Runner | None = None) -> None:
        self._runner: Runner = runner if runner is not None else _default_runner

    # ------------------------------------------------------------------
    # subtitle_and_dubbing mode
    # ------------------------------------------------------------------

    def mux_full(
        self,
        input_video: Path,
        aligned_zh_audio: Path,
        zh_subtitle: Path,
        en_subtitle: Path,
        output_path: Path,
        *,
        runner: Runner | None = None,
        normalize_loudness: bool = True,
    ) -> Path:
        """Mux a ``subtitle_and_dubbing`` output.

        Stream order in the output (which matches ``-map`` order below):

        * ``0:v:0`` — original video, ``copy``.
        * ``1:a:0`` — Chinese dub (AAC, ``default``), ``language=zho``.
        * ``0:a:0`` — original English audio (``copy``, non-default),
          ``language=eng``.
        * ``2:s:0`` — Chinese subtitle (``default``), ``language=zho``.
        * ``3:s:0`` — English subtitle (non-default), ``language=eng``.

        Args:
            input_video: Input video file.
            aligned_zh_audio: Aligned Chinese audio track produced by the
                :class:`AudioAligner`. Expected to be a WAV.
            zh_subtitle: Path to the Chinese SRT/VTT file.
            en_subtitle: Path to the English SRT/VTT file.
            output_path: Destination for the muxed ``.mkv``.
            runner: Per-call runner override; falls back to the
                instance-level runner when ``None``.
            normalize_loudness: When ``True`` (the default) pipe the
                Chinese dub through ``loudnorm`` (EBU R128, ``I=-16
                LRA=11 TP=-1.5``). This matches typical streaming
                platform targets and keeps the new dub from being
                drastically quieter or louder than the original audio.
                Applied to the Chinese track only; the English copy
                passes through untouched.

        Returns:
            The ``output_path`` that was written, for call-chain convenience.

        Raises:
            VideoDecodeError: If ffmpeg reports the input video stream is
                not decodable (R9.14).
            OriginalAudioExtractionError: If ffmpeg can't locate or
                extract the original English audio track (R9.15).
            RuntimeError: For any other non-zero ffmpeg exit.
        """
        cmd: list[str] = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            # Inputs (order matters for the -map args below).
            "-i", _as_ffmpeg_path(input_video),
            "-i", _as_ffmpeg_path(aligned_zh_audio),
            "-i", _as_ffmpeg_path(zh_subtitle),
            "-i", _as_ffmpeg_path(en_subtitle),
            # Output stream selection.
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-map", "0:a:0",
            "-map", "2:s:0",
            "-map", "3:s:0",
            # Codec selection.
            "-c:v", "copy",
            "-c:a:0", "aac",
            "-c:a:1", "copy",
            "-c:s", "srt",
        ]

        if normalize_loudness:
            # EBU R128 targets commonly used for streaming platforms.
            # Applied to the *Chinese* audio stream (a:0 in the output
            # mapping) only. ``-filter:a:0`` addresses that stream
            # unambiguously without touching the English copy.
            cmd.extend(
                [
                    "-filter:a:0",
                    "loudnorm=I=-16:LRA=11:TP=-1.5",
                ]
            )

        cmd.extend(
            [
                # Audio metadata.
                "-metadata:s:a:0", "language=zho",
                "-metadata:s:a:0", "title=中文配音",
                "-metadata:s:a:1", "language=eng",
                "-metadata:s:a:1", "title=Original English",
                # Subtitle metadata.
                "-metadata:s:s:0", "language=zho",
                "-metadata:s:s:0", "title=中文",
                "-metadata:s:s:1", "language=eng",
                "-metadata:s:s:1", "title=English",
                # Disposition flags (audio and subtitle default flags are
                # independent — R9.7).
                "-disposition:a:0", "default",
                "-disposition:a:1", "0",
                "-disposition:s:0", "default",
                "-disposition:s:1", "0",
                _as_ffmpeg_path(output_path),
            ]
        )

        effective_runner = runner if runner is not None else self._runner
        completed = effective_runner(cmd)
        _raise_for_failure(cmd, completed)
        return output_path

    # ------------------------------------------------------------------
    # subtitle_only mode
    # ------------------------------------------------------------------

    def mux_subtitle_only(
        self,
        input_video: Path,
        zh_subtitle: Path,
        en_subtitle: Path,
        output_path: Path,
        *,
        runner: Runner | None = None,
    ) -> Path:
        """Mux a ``subtitle_only`` output.

        Stream order in the output:

        * ``0:v:0`` — original video, ``copy``.
        * ``0:a:0`` — original English audio (``copy``, ``default``),
          ``language=eng`` (R9.9).
        * ``1:s:0`` — Chinese subtitle (``default``), ``language=zho``.
        * ``2:s:0`` — English subtitle (non-default), ``language=eng``.

        No Chinese dub track is emitted (R9.8).

        Args:
            input_video: Input video file.
            zh_subtitle: Path to the Chinese SRT/VTT file.
            en_subtitle: Path to the English SRT/VTT file.
            output_path: Destination for the muxed ``.mkv``.
            runner: Per-call runner override; falls back to the
                instance-level runner when ``None``.

        Returns:
            The ``output_path`` that was written.

        Raises:
            VideoDecodeError: If ffmpeg reports the input video stream is
                not decodable (R9.14).
            OriginalAudioExtractionError: If ffmpeg can't locate or
                extract the original English audio track (R9.15).
            RuntimeError: For any other non-zero ffmpeg exit.
        """
        cmd: list[str] = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i", _as_ffmpeg_path(input_video),
            "-i", _as_ffmpeg_path(zh_subtitle),
            "-i", _as_ffmpeg_path(en_subtitle),
            "-map", "0:v:0",
            "-map", "0:a:0",
            "-map", "1:s:0",
            "-map", "2:s:0",
            "-c:v", "copy",
            "-c:a", "copy",
            "-c:s", "srt",
            # Audio metadata (single English track).
            "-metadata:s:a:0", "language=eng",
            "-metadata:s:a:0", "title=Original English",
            # Subtitle metadata.
            "-metadata:s:s:0", "language=zho",
            "-metadata:s:s:0", "title=中文",
            "-metadata:s:s:1", "language=eng",
            "-metadata:s:s:1", "title=English",
            # Dispositions.
            "-disposition:a:0", "default",
            "-disposition:s:0", "default",
            "-disposition:s:1", "0",
            _as_ffmpeg_path(output_path),
        ]

        effective_runner = runner if runner is not None else self._runner
        completed = effective_runner(cmd)
        _raise_for_failure(cmd, completed)
        return output_path


__all__ = ["VideoMuxer", "Runner"]
