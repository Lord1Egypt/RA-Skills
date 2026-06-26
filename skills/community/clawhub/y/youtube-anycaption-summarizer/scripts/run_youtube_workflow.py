#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from prepare_video_paths import sanitize_title
from normalize_transcript_text import normalize_transcript_text

SUPPORTED_MODELS = {
    "ggml-base": "ggml-base.bin",
    "ggml-small": "ggml-small.bin",
    "ggml-medium": "ggml-medium.bin",
}

SUBTITLE_EXTENSIONS = (".vtt", ".srt", ".srv3", ".ttml")
TIMESTAMP_PAIR_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2}[\.,]\d{3})\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2}[\.,]\d{3})"
)


def canonicalize_language_tag(tag: Optional[str]) -> str:
    if not tag:
        return "unknown"
    text = tag.strip()
    if not text or text.lower() == "auto":
        return "unknown"
    text = re.sub(r"-(orig|auto)$", "", text, flags=re.IGNORECASE)
    return text or "unknown"


def summary_language_display(requested: str, detected: str) -> str:
    if requested == "source":
        return canonicalize_language_tag(detected)
    return requested


def summary_language_instruction(requested: str, detected: str) -> str:
    if requested == "source":
        canon = canonicalize_language_tag(detected)
        if canon == "unknown":
            return "the same language as the source transcript when it is clear; otherwise use your best judgment"
        return "the same language as the source video"
    return requested


def parse_timestamp_seconds(ts: str) -> float:
    normalized = ts.replace(",", ".")
    hours, minutes, rest = normalized.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(rest)


def sanitize_timestamp_range(text: str) -> Optional[Tuple[str, str]]:
    match = TIMESTAMP_PAIR_RE.search(text)
    if not match:
        return None
    start = match.group("start").replace(",", ".")
    end = match.group("end").replace(",", ".")
    return start, end


def clean_subtitle_text(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", "", text)
    cleaned = cleaned.replace("&nbsp;", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def strip_leading_overlap(previous: str, current: str) -> str:
    if not previous:
        return current
    if current == previous:
        return ""
    previous_words = previous.split()
    current_words = current.split()
    max_overlap = min(len(previous_words), len(current_words), 48)
    for size in range(max_overlap, 0, -1):
        if previous_words[-size:] == current_words[:size]:
            return " ".join(current_words[size:]).strip()
    return current


def append_text_with_overlap(base: str, addition: str) -> str:
    if not base:
        return addition
    if not addition:
        return base
    if addition == base:
        return base

    base_words = base.split()
    addition_words = addition.split()
    max_overlap = min(len(base_words), len(addition_words), 48)
    for size in range(max_overlap, 0, -1):
        if base_words[-size:] == addition_words[:size]:
            merged_tail = " ".join(addition_words[size:]).strip()
            return base if not merged_tail else f"{base} {merged_tail}".strip()
    return f"{base} {addition}".strip()


def merge_subtitle_segments(segments: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
    if not segments:
        return []

    merged: List[Tuple[str, str, str]] = []
    current_start, current_end, current_text = segments[0]
    epsilon = 1e-6
    max_window_seconds = 8.0
    max_window_chars = 240

    for next_start, next_end, next_text in segments[1:]:
        current_end_seconds = parse_timestamp_seconds(current_end)
        next_start_seconds = parse_timestamp_seconds(next_start)
        next_end_seconds = parse_timestamp_seconds(next_end)
        merged_candidate_text = append_text_with_overlap(current_text, next_text)
        merged_candidate_duration = next_end_seconds - parse_timestamp_seconds(current_start)

        if (
            next_start_seconds - epsilon <= current_end_seconds <= next_end_seconds + epsilon
            and merged_candidate_duration <= max_window_seconds
            and len(merged_candidate_text) <= max_window_chars
        ):
            current_end = next_end
            current_text = merged_candidate_text
            continue

        merged.append((current_start, current_end, current_text))
        deduped_next_text = strip_leading_overlap(current_text, next_text)
        current_start, current_end, current_text = next_start, next_end, deduped_next_text or next_text

    merged.append((current_start, current_end, current_text))
    return merged


# Timeout defaults (seconds)
DEFAULT_CMD_TIMEOUT = 300       # 5 min for most operations
DEFAULT_LONG_TIMEOUT = 900      # 15 min for transcription / large downloads


def run(cmd: List[str], *, check: bool = True, cwd: Optional[Path] = None, timeout: Optional[int] = DEFAULT_CMD_TIMEOUT) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=check, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Command timed out after {timeout}s: {' '.join(cmd)}") from exc


def run_with_retries(cmd: List[str], retries: int, backoff: float, *, cwd: Optional[Path] = None, timeout: Optional[int] = DEFAULT_LONG_TIMEOUT) -> subprocess.CompletedProcess:
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            result = run(cmd, check=False, cwd=cwd, timeout=timeout)
        except RuntimeError as exc:
            # timeout → treat as retriable
            last_err = exc
            if attempt < retries:
                time.sleep(backoff * attempt)
            continue
        if result.returncode == 0:
            return result
        last_err = result
        if attempt < retries:
            time.sleep(backoff * attempt)
    if isinstance(last_err, RuntimeError):
        raise last_err
    raise RuntimeError(f"Command failed after {retries} attempts: {' '.join(cmd)}\n{last_err.stderr or last_err.stdout}")


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required tool not found in PATH: {name}")


def yt_dlp_base_args(args) -> List[str]:
    base = ["yt-dlp", "--no-warnings", "--no-playlist"]
    if args.cookies:
        base += ["--cookies", args.cookies]
    if args.cookies_from_browser:
        base += ["--cookies-from-browser", args.cookies_from_browser]
    return base


def resolve_model_file(model: str, models_dir: Path) -> Path:
    filename = SUPPORTED_MODELS[model]
    candidate = models_dir / filename
    if candidate.exists():
        return candidate
    raise RuntimeError(f"Model file not found: {candidate}")


def fetch_metadata(url: str, args) -> Dict:
    cmd = yt_dlp_base_args(args) + ["--dump-single-json", "--skip-download", url]
    result = run_with_retries(cmd, args.retries, args.retry_backoff)
    return json.loads(result.stdout)


def existing_folder_matches_video(folder: Path, video_id: str) -> bool:
    if not folder.exists():
        return False
    for suffix in ("_transcript_raw.md", "_Summary.md"):
        for path in folder.glob(f"*{suffix}"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if video_id in text:
                return True
    return False


def build_paths(title: str, video_id: str, parent: Path) -> Dict[str, Path]:
    safe_title = sanitize_title(title)
    folder = parent / safe_title
    if folder.exists() and not existing_folder_matches_video(folder, video_id):
        folder = parent / f"{safe_title}__{video_id}"
    return {
        "safe_title": Path(safe_title),
        "folder": folder,
        "raw_transcript": folder / f"{safe_title}_transcript_raw.md",
        "summary": folder / f"{safe_title}_Summary.md",
        "wav": folder / f"{safe_title}.wav",
        "media_prefix": folder / safe_title,
    }


def choose_subtitle_track(metadata: Dict, preferred_language: str) -> Tuple[Optional[str], Optional[str]]:
    manual = metadata.get("subtitles") or {}
    auto = metadata.get("automatic_captions") or {}
    meta_lang = metadata.get("language") or metadata.get("language_preference") or ""

    def candidates(d: Dict, preferred: Optional[str]) -> List[str]:
        keys = list(d.keys())
        ordered: List[str] = []
        seen = set()
        for probe in [preferred, meta_lang, "en", "en-US", "en-GB"]:
            if not probe:
                continue
            for key in keys:
                if key == probe or key.startswith(probe + "-"):
                    if key not in seen:
                        ordered.append(key)
                        seen.add(key)
        for key in keys:
            if key not in seen:
                ordered.append(key)
                seen.add(key)
        return ordered

    pref = None if preferred_language == "auto" else preferred_language
    if manual:
        ordered = candidates(manual, pref)
        if ordered:
            return ("manual", ordered[0])
    if auto:
        ordered = candidates(auto, pref)
        if ordered:
            return ("auto", ordered[0])
    return (None, None)


def find_subtitle_file(folder: Path, prefix_name: str, lang: str) -> Optional[Path]:
    patterns = [
        f"{prefix_name}*.{lang}*",
        f"{prefix_name}*",
    ]
    candidates: List[Path] = []
    for pattern in patterns:
        for path in folder.glob(pattern):
            if path.suffix.lower() in SUBTITLE_EXTENSIONS:
                candidates.append(path)
    if not candidates:
        return None
    candidates.sort(key=lambda p: (0 if lang in p.name else 1, len(p.name)))
    return candidates[0]


def download_subtitles(url: str, folder: Path, media_prefix: Path, track_type: str, lang: str, args) -> Optional[Path]:
    cmd = yt_dlp_base_args(args) + [
        "--skip-download",
        "--sub-langs",
        lang,
        "--sub-format",
        "vtt/srt/best",
        "--output",
        str(media_prefix) + ".%(ext)s",
    ]
    if track_type == "manual":
        cmd.append("--write-subs")
    else:
        cmd.append("--write-auto-subs")
    cmd.append(url)
    run_with_retries(cmd, args.retries, args.retry_backoff, cwd=folder)
    return find_subtitle_file(folder, media_prefix.name, lang)


def parse_subtitle_to_transcript(sub_path: Path) -> str:
    text = sub_path.read_text(encoding="utf-8", errors="ignore")
    raw_segments: List[Tuple[str, str, str]] = []
    current_range: Optional[Tuple[str, str]] = None
    current_lines: List[str] = []

    def flush_segment() -> None:
        nonlocal current_range, current_lines
        if not current_range:
            current_lines = []
            return
        content = clean_subtitle_text(" ".join(current_lines))
        if content:
            raw_segments.append((current_range[0], current_range[1], content))
        current_range = None
        current_lines = []

    for raw in text.splitlines():
        line = raw.strip().replace("\ufeff", "")
        if not line or line == "WEBVTT" or line.startswith(("NOTE", "STYLE", "REGION")):
            flush_segment()
            continue
        if re.fullmatch(r"\d+", line) and current_range is None:
            continue

        timestamp_range = sanitize_timestamp_range(line)
        if timestamp_range:
            flush_segment()
            current_range = timestamp_range
            continue

        if current_range:
            clean = clean_subtitle_text(line)
            if clean:
                current_lines.append(clean)

    flush_segment()

    merged_segments = merge_subtitle_segments(raw_segments)
    return "\n".join(f"[{start} --> {end}] {content}" for start, end, content in merged_segments).strip()


def download_media(url: str, output_prefix: Path, full_video: bool, args) -> Path:
    if full_video:
        cmd = yt_dlp_base_args(args) + [
            "-f",
            "bestvideo*+bestaudio/best",
            "--merge-output-format",
            "mp4",
            "--output",
            str(output_prefix) + ".%(ext)s",
            "--print",
            "after_move:filepath",
            url,
        ]
    else:
        cmd = yt_dlp_base_args(args) + [
            "-f",
            "bestaudio/best",
            "--output",
            str(output_prefix) + ".%(ext)s",
            "--print",
            "after_move:filepath",
            url,
        ]
    result = run_with_retries(cmd, args.retries, args.retry_backoff)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("yt-dlp did not return a downloaded file path")
    return Path(lines[-1])


def convert_to_wav(source: Path, wav_path: Path) -> None:
    run(["ffmpeg", "-y", "-i", str(source), "-ar", "16000", "-ac", "1", str(wav_path)], timeout=DEFAULT_LONG_TIMEOUT)


def detect_language(model_path: Path, wav_path: Path) -> str:
    # NOTE: do NOT use -np here — it suppresses the language detection output line
    result = run(["whisper-cli", "-m", str(model_path), "-f", str(wav_path), "-l", "auto", "-dl"], check=False, timeout=DEFAULT_LONG_TIMEOUT)
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    for pattern in [r"auto[- ]detected language:\s*([A-Za-z-]+)", r"detected language:\s*([A-Za-z-]+)"]:
        match = re.search(pattern, combined, re.IGNORECASE)
        if match:
            return match.group(1)
    return "auto"


def transcribe(model_path: Path, wav_path: Path, language: str) -> str:
    result = run(["whisper-cli", "-m", str(model_path), "-f", str(wav_path), "-l", language, "-np"], timeout=DEFAULT_LONG_TIMEOUT)
    text = result.stdout.strip()
    if not text:
        raise RuntimeError("whisper-cli returned an empty transcript")
    return text


def write_raw_transcript(path: Path, *, title: str, url: str, video_id: str, model: str, language: str, transcript: str, workflow_metadata: Dict) -> None:
    content = f"""# {title} — Raw Transcript\n\n## 视频标题 / Video Title\n{title}\n\n## 来源 / Source\n{url}\n\n## Video ID\n{video_id}\n\n## Whisper Model\n{model}\n\n## Language\n{language}\n\n## Generated At\n{dt.datetime.now().isoformat(timespec='seconds')}\n\n## Workflow Metadata (JSON)\n```json\n{json.dumps(workflow_metadata, ensure_ascii=False, indent=2)}\n```\n\n## Transcript\n\n{transcript}\n"""
    path.write_text(content, encoding="utf-8")


def write_summary_placeholder(path: Path, *, title: str, url: str, video_id: str, transcript_path: Path, summary_language: str, source_language: str, source_method: str) -> None:
    language_text = source_language if summary_language == "source" else summary_language
    content = f"""# {title} — Summary\n\n## 视频标题 / Video Title\n{title}\n\n## 来源 / Source\n{url}\n\n## Video ID\n{video_id}\n\n## Source Transcript\n{transcript_path.name}\n\n## Summary Language\n{language_text}\n\n## Transcript Source Method\n{source_method}\n\n## Status\nPlaceholder created by workflow script. This is not the final deliverable. Replace this file completely with the final polished summary using the current OpenClaw session model.\n\n## Required sections\n- 视频标题 / Video Title\n- 来源 / Source\n- Executive Summary\n- Key Takeaways\n- Step-by-Step Execution / Deployment Details\n- Tools / Platforms Mentioned\n- Caveats / Notes\n- Bottom Line\n"""
    path.write_text(content, encoding="utf-8")


def cleanup_known_intermediates(paths: List[Path]) -> None:
    seen = set()
    for item in paths:
        if not item:
            continue
        try:
            resolved = item.resolve()
        except FileNotFoundError:
            resolved = item
        if resolved in seen:
            continue
        seen.add(resolved)
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            item.unlink(missing_ok=True)


def format_seconds(value: Optional[float]) -> Optional[str]:
    if value is None:
        return None
    return f"{value:.2f}s"


def collect_urls(url: Optional[str], batch_file: Optional[str]) -> List[str]:
    urls: List[str] = []
    if url:
        urls.append(url)
    if batch_file:
        for line in Path(batch_file).read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            urls.append(stripped)
    return urls


def process_one(url: str, args) -> Dict:
    timings: Dict[str, float] = {}
    workflow_started = time.time()
    perf_start = time.perf_counter()

    # metadata
    t = time.perf_counter()
    metadata = fetch_metadata(url, args)
    timings["metadata_fetch"] = time.perf_counter() - t

    title = metadata.get("title") or metadata.get("fulltitle") or metadata.get("id") or "youtube_video"
    video_id = metadata.get("id")
    if not video_id:
        raise RuntimeError("Could not determine video ID from metadata")

    parent = Path(os.path.expanduser(args.parent)).resolve()
    paths = build_paths(title, video_id, parent)
    folder = paths["folder"]
    raw_transcript = paths["raw_transcript"]
    summary = paths["summary"]
    wav_path = paths["wav"]
    media_prefix = paths["media_prefix"]
    safe_title = paths["safe_title"].name

    if args.dry_run:
        return {
            "mode": "dry-run",
            "title": title,
            "video_id": video_id,
            "safe_title": safe_title,
            "folder": str(folder),
            "raw_transcript": str(raw_transcript),
            "summary": str(summary),
            "model": args.model,
            "language": args.language,
            "summary_language": args.summary_language,
            "media_mode": "full-video" if args.full_video else "audio-only",
            "timings": {k: format_seconds(v) for k, v in timings.items()},
            "total": format_seconds(time.perf_counter() - perf_start),
        }

    t = time.perf_counter()
    folder.mkdir(parents=True, exist_ok=True)
    timings["folder_creation"] = time.perf_counter() - t

    transcript_text: Optional[str] = None
    detected_language = metadata.get("language") or "auto"
    source_language_display = canonicalize_language_tag(detected_language)
    source_method = "whisper"
    subtitle_track = None
    subtitle_type = None
    created_intermediates: List[Path] = []

    if args.subtitle_first:
        t = time.perf_counter()
        subtitle_type, subtitle_track = choose_subtitle_track(metadata, args.language)
        if subtitle_track:
            sub_path = download_subtitles(url, folder, media_prefix, subtitle_type, subtitle_track, args)
            if sub_path:
                created_intermediates.append(sub_path)
                parsed = parse_subtitle_to_transcript(sub_path)
                if parsed:
                    transcript_text = parsed
                    detected_language = subtitle_track
                    source_language_display = canonicalize_language_tag(detected_language)
                    source_method = f"subtitles:{subtitle_type}"
        timings["subtitle_fetch"] = time.perf_counter() - t
    else:
        timings["subtitle_fetch"] = 0.0

    model_path = None
    if transcript_text is None:
        model_path = resolve_model_file(args.model, Path(os.path.expanduser(args.models_dir)).resolve())
        t = time.perf_counter()
        downloaded_media = download_media(url, media_prefix, args.full_video, args)
        created_intermediates.append(downloaded_media)
        timings["media_download"] = time.perf_counter() - t

        t = time.perf_counter()
        convert_to_wav(downloaded_media, wav_path)
        created_intermediates.append(wav_path)
        timings["wav_conversion"] = time.perf_counter() - t

        if args.language == "auto":
            t = time.perf_counter()
            detected_language = detect_language(model_path, wav_path)
            source_language_display = canonicalize_language_tag(detected_language)
            timings["language_detection"] = time.perf_counter() - t
            whisper_language = detected_language if detected_language != "auto" else "auto"
        else:
            detected_language = args.language
            source_language_display = canonicalize_language_tag(detected_language)
            whisper_language = args.language

        t = time.perf_counter()
        transcript_text = transcribe(model_path, wav_path, whisper_language)
        timings["transcription"] = time.perf_counter() - t

    t = time.perf_counter()
    normalized_transcript = normalize_transcript_text(transcript_text)
    timings["transcript_cleanup"] = time.perf_counter() - t

    script_total_so_far = time.perf_counter() - perf_start
    workflow_metadata = {
        "title": title,
        "video_id": video_id,
        "safe_title": safe_title,
        "source_url": url,
        "source_method": source_method,
        "subtitle_track": subtitle_track,
        "summary_language_request": args.summary_language,
        "detected_language_raw": detected_language,
        "detected_language": source_language_display,
        "language_detection_confident": source_language_display != "unknown",
        "workflow_started_at_epoch": workflow_started,
        "timings_seconds": {k: round(v, 2) for k, v in timings.items()},
        "normalized_transcript_char_count": len(normalized_transcript),
        "script_total_so_far": round(script_total_so_far, 2),
    }
    workflow_metadata["timings_seconds"]["script_total_so_far"] = round(script_total_so_far, 2)

    write_raw_transcript(
        raw_transcript,
        title=title,
        url=url,
        video_id=video_id,
        model=args.model,
        language=source_language_display,
        transcript=transcript_text,
        workflow_metadata=workflow_metadata,
    )
    write_summary_placeholder(
        summary,
        title=title,
        url=url,
        video_id=video_id,
        transcript_path=raw_transcript,
        summary_language=args.summary_language,
        source_language=source_language_display,
        source_method=source_method,
    )

    t = time.perf_counter()
    if not args.keep_intermediates:
        cleanup_known_intermediates(created_intermediates)
    timings["cleanup"] = time.perf_counter() - t

    script_total = time.perf_counter() - perf_start
    summary_target_language = summary_language_display(args.summary_language, source_language_display)
    summary_instruction_language = summary_language_instruction(args.summary_language, source_language_display)
    normalize_cmd = f"python3 scripts/normalize_transcript_text.py '{raw_transcript}'"
    language_backfill_needed = source_language_display == "unknown"
    language_backfill_cmd_template = (
        f"python3 scripts/backfill_detected_language.py '{raw_transcript}' '{summary}' --language <language-tag>"
        if language_backfill_needed else None
    )
    finalize_cmd_template = f"python3 scripts/finalize_youtube_summary.py '{raw_transcript}' '{summary}' --summary-start-epoch <epoch>"
    completion_cmd_template = (
        f"python3 scripts/complete_youtube_summary.py '{raw_transcript}' '{summary}'"
        + (" --language <language-tag>" if language_backfill_needed else "")
        + " --summary-start-epoch <epoch>"
    )
    session_report_cmd_template = completion_cmd_template + " --format session"
    backfill_instruction = ""
    if language_backfill_needed:
        backfill_instruction = (
            "First inspect the transcript body and decide the main spoken language yourself. "
            f"Then backfill that language into both markdown files, either explicitly with {language_backfill_cmd_template} or implicitly by passing the same language to the completion command. "
        )
    summary_prompt = (
        f"Read '{raw_transcript}' and generate a polished markdown summary into '{summary}'. "
        f"Write the summary in {summary_instruction_language}. Use the current OpenClaw session model. "
        + backfill_instruction +
        "Correct obvious transcript errors when context makes the fix clear. Replace the placeholder summary completely rather than leaving the placeholder status text. Follow the summary template exactly, including metadata sections like Summary Language and Transcript Source Method. Make `Step-by-Step Execution / Deployment Details` especially detailed and workflow-driven so a beginner can reproduce the same strategy, deployment, setup, and operational flow using only the transcript-backed details. "
        f"Before writing the summary, you may clean the transcript with: {normalize_cmd}. "
        f"After overwriting the placeholder summary, run this exact completion command to validate/finalize the item: {completion_cmd_template}. "
        f"Then run this session-report command and return its output to the current OpenClaw session: {session_report_cmd_template}"
    )

    return {
        "title": title,
        "video_id": video_id,
        "safe_title": safe_title,
        "folder": str(folder),
        "model": args.model,
        "model_file": str(model_path) if model_path else None,
        "language": source_language_display,
        "summary_language": summary_target_language,
        "media_mode": "full-video" if args.full_video else "audio-only",
        "source_method": source_method,
        "raw_transcript": str(raw_transcript),
        "summary": str(summary),
        "summary_status": "placeholder",
        "postprocess_required": True,
        "language_backfill_needed": language_backfill_needed,
        "language_backfill_command": language_backfill_cmd_template,
        "normalize_command": normalize_cmd,
        "summary_prompt": summary_prompt,
        "completion_command": completion_cmd_template,
        "session_report_command": session_report_cmd_template,
        "finalize_command": finalize_cmd_template,
        "timings": {k: format_seconds(v) for k, v in timings.items()},
        "total": format_seconds(script_total),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Download, transcribe, and prepare a YouTube transcript workflow (v2)")
    parser.add_argument("url", nargs="?", help="YouTube video URL")
    parser.add_argument("--batch-file", help="Plain text file with one YouTube URL per line")
    parser.add_argument("--parent", default=str(Path.home() / "Downloads"), help="Parent output folder")
    parser.add_argument("--model", choices=sorted(SUPPORTED_MODELS.keys()), default="ggml-medium")
    parser.add_argument("--models-dir", default=str(Path.home() / ".openclaw" / "workspace"), help="Directory containing ggml model files")
    parser.add_argument("--language", default="auto", help="Whisper/source language code or 'auto'")
    parser.add_argument("--summary-language", default="source", help="Summary language, or 'source' to match source language")
    parser.add_argument("--full-video", action="store_true", help="Download full video instead of audio-only")
    parser.add_argument("--keep-intermediates", action="store_true", help="Do not delete intermediate files")
    parser.add_argument("--dry-run", action="store_true", help="Fetch metadata and planned paths only")
    parser.add_argument("--subtitle-first", action="store_true", default=True, help="Try subtitles before local transcription")
    parser.add_argument("--no-subtitle-first", dest="subtitle_first", action="store_false", help="Skip subtitle-first attempt")
    parser.add_argument("--cookies", help="Path to yt-dlp cookies file")
    parser.add_argument("--cookies-from-browser", help="Browser name for yt-dlp cookie extraction, e.g. chrome or safari")
    parser.add_argument("--retries", type=int, default=3, help="Retry count for yt-dlp operations")
    parser.add_argument("--retry-backoff", type=float, default=3.0, help="Base backoff seconds for yt-dlp retries")
    parser.add_argument("--continue-on-error", action="store_true", help="In batch mode, continue processing after an item fails")
    args = parser.parse_args()

    if not args.url and not args.batch_file:
        parser.error("Provide a URL or --batch-file")

    for tool in ("yt-dlp", "ffmpeg", "whisper-cli"):
        require_tool(tool)

    urls = collect_urls(args.url, args.batch_file)
    results = []
    failures = []

    for url in urls:
        try:
            results.append(process_one(url, args))
        except Exception as exc:
            error_item = {"url": url, "error": str(exc)}
            if args.continue_on_error and len(urls) > 1:
                failures.append(error_item)
                continue
            print(json.dumps(error_item, ensure_ascii=False, indent=2), file=sys.stderr)
            return 1

    if len(urls) == 1:
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"queue_mode": True, "count": len(urls), "results": results, "failures": failures}, ensure_ascii=False, indent=2))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
