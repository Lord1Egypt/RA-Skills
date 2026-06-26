from __future__ import annotations
#!/usr/bin/env python3
"""
YouTube Transcribe — Smart YouTube video transcription.

1. Tries to extract captions/subtitles via yt-dlp (fast, free)
2. Falls back to local Whisper transcription if no captions found
3. Auto-detects best Whisper backend and model for the hardware
"""

import argparse
import glob
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile


# ---------------------------------------------------------------------------
# YouTube URL parsing
# ---------------------------------------------------------------------------

YOUTUBE_URL_PATTERNS = [
    re.compile(r'(?:youtube\.com/watch\?.*v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})'),
]


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    for pattern in YOUTUBE_URL_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    # Maybe it's already a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    return None


# ---------------------------------------------------------------------------
# Video metadata
# ---------------------------------------------------------------------------

def get_video_metadata(url: str) -> dict:
    """Fetch video metadata via yt-dlp."""
    cmd = [
        "yt-dlp", "--dump-json", "--no-download",
        "--no-warnings", "--quiet",
        "--socket-timeout", "15",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                "video_id": data.get("id", ""),
                "title": data.get("title", ""),
                "channel": data.get("channel", data.get("uploader", "")),
                "duration": data.get("duration", 0),
                "language": data.get("language", ""),
                "has_subtitles": bool(data.get("subtitles")),
                "has_auto_captions": bool(data.get("automatic_captions")),
                "subtitle_langs": list((data.get("subtitles") or {}).keys()),
                "auto_caption_langs": list((data.get("automatic_captions") or {}).keys()),
            }
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
        pass
    return {}


# ---------------------------------------------------------------------------
# Caption extraction (Layer 1 — fast, free)
# ---------------------------------------------------------------------------

def build_lang_priority(language: str | None) -> list[str]:
    """Build subtitle language priority list."""
    langs = []
    if language:
        langs.append(language)
        # Add variants for Chinese
        if language.startswith("zh"):
            for v in ["zh-Hant", "zh-Hans", "zh-TW", "zh-CN", "zh"]:
                if v not in langs:
                    langs.append(v)
    else:
        # Default priority: Chinese variants, then English
        langs = ["zh-Hant", "zh-Hans", "zh-TW", "zh-CN", "zh", "en"]
    return langs


def extract_captions(url: str, language: str | None) -> tuple[str | None, str | None, list[dict] | None]:
    """Try to extract captions via yt-dlp.

    Returns: (full_text, detected_language, segments_list) or (None, None, None)
    """
    lang_priority = build_lang_priority(language)
    # Build yt-dlp sub-langs argument: try all priority langs
    sub_langs = ",".join(lang_priority)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Try manual subtitles first, then auto-generated
        for write_flag in [["--write-subs"], ["--write-auto-subs"]]:
            cmd = [
                "yt-dlp",
                "--skip-download",
                *write_flag,
                "--sub-langs", sub_langs,
                "--sub-format", "vtt",
                "--output", os.path.join(tmpdir, "video.%(ext)s"),
                "--quiet", "--no-warnings",
                "--socket-timeout", "15",
                url,
            ]
            try:
                subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            except subprocess.TimeoutExpired:
                continue

            vtt_files = glob.glob(os.path.join(tmpdir, "*.vtt"))
            if vtt_files:
                # Pick the best matching language file
                vtt_file = pick_best_vtt(vtt_files, lang_priority)
                detected_lang = detect_lang_from_filename(vtt_file)
                segments = parse_vtt(vtt_file)
                full_text = " ".join(seg["text"] for seg in segments)
                return full_text, detected_lang, segments

            # Clean up for next attempt
            for f in glob.glob(os.path.join(tmpdir, "*")):
                os.remove(f)

    return None, None, None


def pick_best_vtt(vtt_files: list[str], lang_priority: list[str]) -> str:
    """Pick the VTT file that best matches our language priority."""
    if len(vtt_files) == 1:
        return vtt_files[0]

    for lang in lang_priority:
        for f in vtt_files:
            if f".{lang}." in os.path.basename(f):
                return f
    return vtt_files[0]


def detect_lang_from_filename(filepath: str) -> str:
    """Extract language code from VTT filename like video.zh-Hant.vtt."""
    basename = os.path.basename(filepath)
    parts = basename.rsplit(".", 2)
    if len(parts) >= 3:
        return parts[-2]
    return "unknown"


def parse_vtt(filepath: str) -> list[dict]:
    """Parse a VTT file into segments with timestamps."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    segments = []
    seen_texts = set()
    current_start = None
    current_end = None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue

        # Timestamp line
        ts_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', line)
        if ts_match:
            current_start = parse_timestamp(ts_match.group(1))
            current_end = parse_timestamp(ts_match.group(2))
            continue

        # Skip numeric cue identifiers
        if re.match(r'^\d+$', line):
            continue

        # Text line — strip HTML tags
        text = re.sub(r'<[^>]+>', '', line).strip()
        if text and text not in seen_texts and current_start is not None:
            seen_texts.add(text)
            segments.append({
                "start": current_start,
                "end": current_end,
                "text": text,
            })

    return segments


def parse_timestamp(ts: str) -> float:
    """Parse VTT timestamp (HH:MM:SS.mmm) to seconds."""
    parts = ts.split(":")
    h, m = int(parts[0]), int(parts[1])
    s = float(parts[2])
    return h * 3600 + m * 60 + s


# ---------------------------------------------------------------------------
# Whisper transcription (Layer 2 — fallback)
# ---------------------------------------------------------------------------

def get_available_ram_gb() -> float:
    """Get available system RAM in GB."""
    try:
        if platform.system() == "Darwin":
            # macOS: use sysctl
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                return int(result.stdout.strip()) / (1024 ** 3)
        else:
            # Linux: read /proc/meminfo
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        return kb / (1024 ** 2)
    except Exception:
        pass
    return 8.0  # Conservative default


def detect_whisper_backend(preferred: str | None = None) -> tuple[str, object]:
    """Detect the best available Whisper backend.

    Returns: (backend_name, module)
    Priority: mlx > faster-whisper > openai-whisper
    """
    env_backend = preferred or os.environ.get("YT_WHISPER_BACKEND", "").lower()

    backends = [
        ("mlx", "mlx_whisper"),
        ("faster-whisper", "faster_whisper"),
        ("whisper", "whisper"),
    ]

    # If user specified a backend, try it first
    if env_backend and env_backend != "auto":
        for name, module_name in backends:
            if name == env_backend or module_name == env_backend:
                try:
                    mod = __import__(module_name)
                    return name, mod
                except ImportError:
                    print(f"⚠️  Requested backend '{env_backend}' not installed, trying others...",
                          file=sys.stderr)
                    break

    # Auto-detect
    for name, module_name in backends:
        try:
            mod = __import__(module_name)
            return name, mod
        except ImportError:
            continue

    print("❌ No Whisper backend found. Install one of:", file=sys.stderr)
    print("   pip install mlx-whisper        # Apple Silicon", file=sys.stderr)
    print("   pip install faster-whisper     # CUDA / CPU", file=sys.stderr)
    print("   pip install openai-whisper     # Universal", file=sys.stderr)
    sys.exit(1)


def select_model_size(preferred: str | None = None) -> str:
    """Select Whisper model size based on available RAM."""
    env_model = preferred or os.environ.get("YT_WHISPER_MODEL", "").lower()
    if env_model and env_model != "auto":
        return env_model

    ram_gb = get_available_ram_gb()
    if ram_gb >= 16:
        return "large-v3"
    elif ram_gb >= 8:
        return "medium"
    elif ram_gb >= 4:
        return "small"
    else:
        return "base"


def download_audio(url: str, output_dir: str) -> str:
    """Download audio from YouTube video using yt-dlp."""
    output_path = os.path.join(output_dir, "audio.%(ext)s")
    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
        "--output", output_path,
        "--quiet", "--no-warnings",
        "--socket-timeout", "15",
        url,
    ]
    print("📥 Downloading audio...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"❌ Audio download failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    wav_files = glob.glob(os.path.join(output_dir, "audio.*"))
    if not wav_files:
        print("❌ No audio file produced", file=sys.stderr)
        sys.exit(1)

    return wav_files[0]


def transcribe_with_mlx(audio_path: str, model_size: str, language: str | None) -> list[dict]:
    """Transcribe using MLX Whisper (Apple Silicon)."""
    import mlx_whisper

    model_name = f"mlx-community/whisper-{model_size}-mlx"
    print(f"🧠 Transcribing with MLX Whisper ({model_size})...", file=sys.stderr)

    kwargs = {"path_or_hf_repo": model_name, "verbose": False}
    if language:
        kwargs["language"] = language

    result = mlx_whisper.transcribe(audio_path, **kwargs)

    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })
    return segments


def transcribe_with_faster_whisper(audio_path: str, model_size: str, language: str | None) -> list[dict]:
    """Transcribe using faster-whisper (CTranslate2)."""
    from faster_whisper import WhisperModel

    # Detect CUDA
    device = "cpu"
    compute_type = "int8"
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "float16"
    except ImportError:
        pass

    print(f"🧠 Transcribing with faster-whisper ({model_size}, {device})...", file=sys.stderr)
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    kwargs = {"beam_size": 5}
    if language:
        kwargs["language"] = language

    result_segments, info = model.transcribe(audio_path, **kwargs)

    segments = []
    for seg in result_segments:
        segments.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip(),
        })
    return segments


def transcribe_with_whisper(audio_path: str, model_size: str, language: str | None) -> list[dict]:
    """Transcribe using OpenAI Whisper."""
    import whisper

    print(f"🧠 Transcribing with OpenAI Whisper ({model_size})...", file=sys.stderr)
    model = whisper.load_model(model_size)

    kwargs = {"verbose": False}
    if language:
        kwargs["language"] = language

    result = model.transcribe(audio_path, **kwargs)

    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })
    return segments


def transcribe_audio(url: str, language: str | None, backend_pref: str | None,
                     model_pref: str | None) -> tuple[list[dict], str, str]:
    """Download audio and transcribe with best available backend.

    Returns: (segments, backend_name, model_size)
    """
    backend_name, backend_mod = detect_whisper_backend(backend_pref)
    model_size = select_model_size(model_pref)

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = download_audio(url, tmpdir)

        if backend_name == "mlx":
            segments = transcribe_with_mlx(audio_path, model_size, language)
        elif backend_name == "faster-whisper":
            segments = transcribe_with_faster_whisper(audio_path, model_size, language)
        else:
            segments = transcribe_with_whisper(audio_path, model_size, language)

    return segments, backend_name, model_size


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_srt(segments: list[dict]) -> str:
    """Format segments as SRT subtitles."""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_srt(seg["start"])
        end = format_timestamp_srt(seg["end"])
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"])
        lines.append("")
    return "\n".join(lines)


def format_vtt(segments: list[dict]) -> str:
    """Format segments as WebVTT subtitles."""
    lines = ["WEBVTT", ""]
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_vtt(seg["start"])
        end = format_timestamp_vtt(seg["end"])
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"])
        lines.append("")
    return "\n".join(lines)


def format_timestamp_srt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def format_output(segments: list[dict], metadata: dict, method: str,
                  fmt: str, backend: str = "", model: str = "") -> str:
    """Format the final output."""
    if fmt == "json":
        output = {
            **metadata,
            "method": method,
            "backend": backend,
            "model": model,
            "transcript": segments,
            "full_text": " ".join(seg["text"] for seg in segments),
        }
        return json.dumps(output, ensure_ascii=False, indent=2)
    elif fmt == "srt":
        return format_srt(segments)
    elif fmt == "vtt":
        return format_vtt(segments)
    else:  # text
        return " ".join(seg["text"] for seg in segments)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube videos — captions first, Whisper fallback.",
    )
    parser.add_argument("url", help="YouTube video URL or ID")
    parser.add_argument("--language", "-l", default=None,
                        help="Preferred language code (e.g. zh, en, ja)")
    parser.add_argument("--format", "-f", default="text",
                        choices=["text", "json", "srt", "vtt"],
                        help="Output format (default: text)")
    parser.add_argument("--output", "-o", default=None,
                        help="Save to file instead of stdout")
    parser.add_argument("--force-whisper", action="store_true",
                        help="Skip caption extraction, go straight to Whisper")
    parser.add_argument("--backend", default=None,
                        choices=["auto", "mlx", "faster-whisper", "whisper"],
                        help="Whisper backend (default: auto-detect)")
    parser.add_argument("--model", default=None,
                        help="Whisper model size (default: auto based on RAM)")
    args = parser.parse_args()

    # Validate URL
    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"❌ Invalid YouTube URL: {args.url}", file=sys.stderr)
        sys.exit(1)

    url = f"https://www.youtube.com/watch?v={video_id}"

    # Get metadata
    print(f"📋 Fetching video info...", file=sys.stderr)
    metadata = get_video_metadata(url)
    if metadata:
        title = metadata.get("title", "")
        if title:
            print(f"📺 {title}", file=sys.stderr)

    # Layer 1: Try captions
    segments = None
    method = ""
    backend_used = ""
    model_used = ""

    if not args.force_whisper:
        print("🔍 Looking for captions...", file=sys.stderr)
        full_text, detected_lang, segments = extract_captions(url, args.language)

        if segments:
            method = "captions"
            if detected_lang:
                print(f"✅ Found captions ({detected_lang}), {len(segments)} segments",
                      file=sys.stderr)
                if "language" not in metadata or not metadata["language"]:
                    metadata["language"] = detected_lang
        else:
            print("⚠️  No captions found", file=sys.stderr)

    # Layer 2: Whisper fallback
    if not segments:
        if not shutil.which("ffmpeg"):
            print("❌ ffmpeg required for Whisper transcription but not found", file=sys.stderr)
            print("   Install: brew install ffmpeg", file=sys.stderr)
            sys.exit(1)

        segments, backend_used, model_used = transcribe_audio(
            url, args.language, args.backend, args.model,
        )
        method = "whisper"
        print(f"✅ Transcribed {len(segments)} segments via {backend_used} ({model_used})",
              file=sys.stderr)

    if not segments:
        print("❌ Could not extract any content from this video", file=sys.stderr)
        sys.exit(1)

    # Format output
    output = format_output(
        segments, metadata, method, args.format,
        backend=backend_used, model=model_used,
    )

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"💾 Saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
