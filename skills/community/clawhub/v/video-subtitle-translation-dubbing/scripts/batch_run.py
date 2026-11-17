"""Batch-process a directory of (video, subtitle) pairs.

Walks ``--input-dir``, pairs every video file with its matching
``<stem>.en.srt`` or ``<stem>.en.vtt`` sidecar, cleans the YouTube
auto-caption rolling window into sentence-level cues, then runs the
full ``translation_dubbing_skill`` pipeline on each pair with
``subtitle_and_dubbing`` mode (Chinese dub + Chinese subtitles).

Usage::

    export TRANSLATION_CREDENTIAL=sk-minimax-xxx
    python scripts/batch_run.py \
        --input-dir /path/to/clips \
        --out-dir ./out \
        --mode subtitle_and_dubbing \
        --voice-id zh-CN-YunxiNeural \
        --translation-model MiniMax-M2.7

Design notes
------------

* Videos and sidecars are matched by stem. A file is considered a
  video when its suffix lives in ``_VIDEO_SUFFIXES``; its sidecar is
  the same stem with ``.en.srt`` / ``.en.vtt`` replacing the suffix.
  Videos without a sidecar are skipped (with a warning) — we never
  rely on embedded subtitle extraction for the batch runner because
  YouTube clips frequently ship without an embedded English track.
* Each clip gets its own output subdirectory so the per-clip filenames
  produced by the skill (``output-<uuid>.mkv`` etc.) don't collide and
  so the user can see which inputs produced which artefacts.
* The runner invokes the in-process :func:`translation_dubbing_skill.run`
  rather than shelling out to ``run_real.py`` — this keeps the MiniMax
  API client warm across clips so subsequent translations start faster.
* Exceptions are caught per-clip and recorded; the runner keeps going
  so a single bad file doesn't abort the batch. A summary is printed
  at the end with the pass/fail count and failure reasons.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

# Make sure the script works when invoked from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from translation_dubbing_skill import parse_manifest, run
from translation_dubbing_skill.models import ProgressEvent
from translation_dubbing_skill.progress import ProgressReporter

from clean_youtube_vtt import clean as clean_subtitle


_VIDEO_SUFFIXES: tuple[str, ...] = (".mp4", ".mkv", ".mov", ".webm")
_SUBTITLE_SUFFIXES: tuple[str, ...] = (".srt", ".vtt")


@dataclass
class _ClipJob:
    """One batch job: a video + its English sidecar subtitle."""

    video: Path
    subtitle: Path
    # Suffix of the sidecar so we write a matching cleaned copy.
    subtitle_suffix: str


@dataclass
class _ClipResult:
    """Outcome of processing one clip."""

    clip: _ClipJob
    ok: bool
    message: str


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def _find_sidecar(video: Path) -> Path | None:
    """Return the ``.en.srt`` / ``.en.vtt`` sibling for ``video``, or None.

    YouTube clips downloaded with ``yt-dlp`` usually export sidecars in
    the form ``<stem>.en.srt`` or ``<stem>.en.vtt``. We search both and
    prefer ``.srt`` when both exist (the skill can parse either, but
    SRT emits cleaner Chinese subtitle output by default).

    ``yt-dlp`` sometimes appends a format selector (e.g. ``.f251``) to
    the video stem but not to the subtitle sidecar, so we also try a
    fallback where the trailing ``.f<digits>`` component is stripped.
    """
    stem_dir = video.parent
    bases: list[str] = [video.stem]
    # yt-dlp format suffix: ``Title [id].f251.webm`` paired with
    # ``Title [id].en.vtt``. Drop the ``.f<digits>`` tail if present.
    stripped = re.sub(r"\.f\d+$", "", video.stem)
    if stripped != video.stem:
        bases.append(stripped)
    for base in bases:
        for suffix in (".en.srt", ".en.vtt"):
            candidate = stem_dir / f"{base}{suffix}"
            if candidate.is_file():
                return candidate
    return None


def _probe_has_video_stream(video: Path) -> bool:
    """Return ``True`` if ``video`` contains at least one video stream.

    yt-dlp's ``.f251.webm`` (and similar audio-only format codes) give
    you a container with only an ``audio`` stream — our muxer's
    ``-map 0:v:0`` rightfully fails on those because there is no video
    to copy. Rather than burn a full run (translate + TTS + mux) only
    to fail at the last step, short-circuit during discovery.

    Falls back to "assume there IS a video stream" when ffprobe is
    unavailable — that way environments without ffprobe on PATH can
    still attempt to process clips and surface a real downstream error
    instead of silently dropping everything.
    """
    import subprocess

    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v",
                "-show_entries",
                "stream=codec_type",
                "-of",
                "csv=p=0",
                str(video),
            ],
            capture_output=True,
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return True
    if result.returncode != 0:
        return True
    output = result.stdout.decode("utf-8", errors="replace").strip()
    return "video" in output


def _discover_jobs(input_dir: Path) -> list[_ClipJob]:
    """Enumerate every (video, sidecar) pair under ``input_dir``.

    Hidden files (``.DS_Store`` and friends) are skipped. Videos that
    lack a matching sidecar are skipped with a warning so the operator
    can decide whether to re-download them; we never fall back to
    embedded-subtitle extraction because several of the test clips
    have no embedded English track.
    """
    jobs: list[_ClipJob] = []
    for path in sorted(input_dir.iterdir()):
        if path.name.startswith("."):
            continue
        if path.suffix.lower() not in _VIDEO_SUFFIXES:
            continue
        sidecar = _find_sidecar(path)
        if sidecar is None:
            print(f"[skip] no sidecar subtitle for {path.name}", file=sys.stderr)
            continue
        if not _probe_has_video_stream(path):
            print(
                f"[skip] {path.name}: container has no video stream "
                "(likely a yt-dlp audio-only format such as .f251)",
                file=sys.stderr,
            )
            continue
        # Strip ``.en`` from the subtitle stem when picking its final
        # suffix; the cleaner writes out the same extension as the
        # input so the downstream parser's format sniffing still works.
        subtitle_suffix = sidecar.suffix.lower()
        jobs.append(
            _ClipJob(
                video=path,
                subtitle=sidecar,
                subtitle_suffix=subtitle_suffix,
            )
        )
    return jobs


# ---------------------------------------------------------------------------
# Per-clip execution
# ---------------------------------------------------------------------------


def _clean_and_write(job: _ClipJob, work_dir: Path) -> Path:
    """Clean the YouTube auto-caption rolling window and write a sidecar.

    The cleaned file is written next to the clip output so repeated
    batch runs can reuse it, and so the operator can inspect the
    sentence-level cues that actually drove the translation.
    """
    raw_text = job.subtitle.read_text(encoding="utf-8")
    # Emit the same extension so the skill's format sniffing still works.
    output_format = "srt" if job.subtitle_suffix == ".srt" else "vtt"
    cleaned_text = clean_subtitle(raw_text, output_format=output_format)
    cleaned_path = work_dir / f"cleaned{job.subtitle_suffix}"
    cleaned_path.write_text(cleaned_text, encoding="utf-8")
    return cleaned_path


def _build_progress_callback(prefix: str) -> ProgressReporter:
    """Return a :class:`ProgressReporter` that prefixes each event with ``prefix``.

    Every line is flushed to stdout immediately so long-running batch
    jobs show live progress instead of buffering everything until the
    clip finishes.
    """

    def _sink(event: ProgressEvent) -> None:
        if event.completed is not None and event.total is not None:
            line = (
                f"{prefix} [{event.stage}] {event.message} "
                f"({event.completed}/{event.total})"
            )
        else:
            line = f"{prefix} [{event.stage}] {event.message}"
        print(line, flush=True)

    return ProgressReporter(_sink)


async def _process_one(
    job: _ClipJob,
    args: argparse.Namespace,
    credential: str,
    tts_credential: str,
    global_out_dir: Path,
) -> _ClipResult:
    """Run the full pipeline on one clip; return a :class:`_ClipResult`."""
    clip_out = global_out_dir / job.video.stem
    clip_out.mkdir(parents=True, exist_ok=True)
    prefix = f"[{job.video.stem[:40]}...]"

    # Idempotency: if a successful ``output-*.mkv`` already exists in
    # the clip's output dir, the pipeline previously completed — skip
    # the MiniMax + TTS round trip on re-runs. Operators who want to
    # force a re-run can delete the output directory or pass
    # ``--force``.
    existing = sorted(clip_out.glob("output-*.mkv"))
    if existing and not args.force:
        return _ClipResult(
            job,
            True,
            f"skipped (already processed): {existing[0].name}",
        )

    try:
        cleaned_subtitle = _clean_and_write(job, clip_out)
    except Exception as exc:
        return _ClipResult(job, False, f"subtitle cleaning failed: {exc!r}")

    manifest: dict = {
        "video_path": str(job.video),
        "subtitle_path": str(cleaned_subtitle),
        "processing_mode": args.mode,
        "translation_provider": "llm",
        "translation_endpoint": args.translation_endpoint,
        "translation_credential": credential,
        "translation_extra": {
            "model_name": args.translation_model,
            # Offload M2.7's <think> block into reasoning_details so the
            # content field is clean JSON and the response ends sooner.
            "reasoning_split": True,
            # M2.7 thinking can take over a minute on a 20-cue batch;
            # give it a generous ceiling so a slow turn doesn't trip
            # the scheduler's retry budget.
            "timeout_s": args.translation_timeout_s,
        },
    }
    if args.mode == "subtitle_and_dubbing":
        tts_extra: dict = {"default_voice": args.voice_id}
        if args.tts_model:
            tts_extra["model_name"] = args.tts_model
        # Pick a provider-appropriate endpoint. Edge uses a
        # placeholder — the library talks WebSockets directly, not via
        # our HTTP client — while MiniMax / llm / web hit a real URL.
        if args.tts_provider == "edge":
            tts_endpoint = args.tts_endpoint or "ws://edge-tts"
        elif args.tts_provider == "minimax":
            tts_endpoint = (
                args.tts_endpoint or "https://api.minimaxi.com/v1/t2a_v2"
            )
        else:
            if not args.tts_endpoint:
                raise RuntimeError(
                    f"tts-provider={args.tts_provider} requires --tts-endpoint"
                )
            tts_endpoint = args.tts_endpoint
        manifest.update(
            {
                "tts_provider": args.tts_provider,
                "tts_endpoint": tts_endpoint,
                "tts_credential": tts_credential,
                "tts_extra": tts_extra,
                "voice_id": args.voice_id,
            }
        )

    try:
        params = parse_manifest(manifest)
    except Exception as exc:
        return _ClipResult(job, False, f"manifest parse failed: {exc!r}")

    reporter = _build_progress_callback(prefix)

    try:
        result = await run(
            params,
            reporter=reporter,
            output_dir_factory=lambda: clip_out,
        )
    except Exception as exc:
        traceback.print_exc()
        return _ClipResult(job, False, f"pipeline failed: {exc!r}")

    return _ClipResult(
        job,
        True,
        f"video={result.output_video_path.name} subtitle={result.output_subtitle_path.name}",
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch-process a directory of clips.")
    p.add_argument(
        "--input-dir",
        required=True,
        type=Path,
        help="Directory containing .mkv/.mp4/.webm + .en.srt/.en.vtt pairs.",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path("./out"),
        help="Root output directory; each clip gets its own subfolder.",
    )
    p.add_argument(
        "--mode",
        choices=["subtitle_only", "subtitle_and_dubbing"],
        default="subtitle_and_dubbing",
    )
    p.add_argument(
        "--translation-endpoint",
        default="https://api.minimaxi.com/v1/chat/completions",
    )
    p.add_argument("--translation-model", default="MiniMax-M2.7")
    p.add_argument(
        "--translation-timeout-s",
        type=float,
        default=240.0,
        help=(
            "Per-request HTTP timeout for the LLM translation call, in "
            "seconds. Raise this for thinking-heavy models (M2.7) on "
            "large batches; lower it when you prefer fast-fail "
            "behaviour over waiting out a stuck upstream."
        ),
    )
    p.add_argument("--voice-id", default="zh-CN-YunxiNeural")
    p.add_argument(
        "--tts-provider",
        choices=["edge", "minimax", "llm", "web"],
        default="edge",
        help=(
            "Which TTS backend to use. 'edge' (default) hits Microsoft "
            "Read-Aloud and is free but English-hosted. 'minimax' hits "
            "MiniMax's t2a_v2 API (needs MINIMAX_API_KEY / --tts-credential). "
            "'llm' / 'web' are the generic provider types."
        ),
    )
    p.add_argument(
        "--tts-endpoint",
        default="",
        help=(
            "Override the TTS endpoint URL. Ignored when "
            "--tts-provider=edge. Defaults depend on provider."
        ),
    )
    p.add_argument(
        "--tts-model",
        default="",
        help=(
            "Optional TTS model name, e.g. 'speech-2.8-hd' for MiniMax."
        ),
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only process the first N clips (useful for smoke tests).",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help=(
            "Re-process clips even when a completed output.mkv already "
            "exists. Without this flag, clips whose output directory "
            "already contains a muxed .mkv are skipped — a cheap "
            "safety net after partial batch failures so we don't pay "
            "the LLM + TTS bill twice."
        ),
    )
    return p.parse_args()


async def _main() -> int:
    args = _parse_args()

    if not args.input_dir.is_dir():
        print(f"ERROR: input dir does not exist: {args.input_dir}", file=sys.stderr)
        return 2

    credential = os.environ.get("TRANSLATION_CREDENTIAL")
    if not credential:
        print("ERROR: set TRANSLATION_CREDENTIAL env var", file=sys.stderr)
        return 2
    tts_credential = os.environ.get("TTS_CREDENTIAL")
    if not tts_credential:
        # Convenience: for MiniMax TTS the same key works as translation,
        # so fall back silently rather than making operators export the
        # same secret twice. Edge doesn't need a real credential at all.
        if args.tts_provider == "minimax":
            tts_credential = credential
        else:
            tts_credential = "none"

    args.out_dir.mkdir(parents=True, exist_ok=True)

    jobs = _discover_jobs(args.input_dir)
    if args.limit is not None:
        jobs = jobs[: args.limit]
    if not jobs:
        print(f"ERROR: no (video, subtitle) pairs found under {args.input_dir}")
        return 1

    print(f"found {len(jobs)} clip(s)")
    for j in jobs:
        print(f"  - {j.video.name}")

    results: list[_ClipResult] = []
    for i, job in enumerate(jobs, start=1):
        print(f"\n[{i}/{len(jobs)}] {job.video.name}")
        result = await _process_one(
            job, args, credential, tts_credential, args.out_dir
        )
        results.append(result)
        status = "ok" if result.ok else "FAIL"
        print(f"  -> {status}: {result.message}")

    print("\n================ summary ================")
    ok = sum(1 for r in results if r.ok)
    fail = len(results) - ok
    print(f"processed: {len(results)}   ok: {ok}   failed: {fail}")
    if fail:
        print("\nfailures:")
        for r in results:
            if not r.ok:
                print(f"  - {r.clip.video.name}: {r.message}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(_main()))
