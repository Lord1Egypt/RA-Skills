#!/usr/bin/env python3
"""
Audio Transcription Script - Transcribe audio to text using Whisper.
Supports:
  1. Local Whisper (faster-whisper or openai-whisper)
  2. OpenAI-compatible API (local or cloud)
"""
import argparse
import os
import shutil
import sys
import time
from pathlib import Path

# Torch is needed for GPU detection
try:
    import torch
except ImportError:
    torch = None

# ── Platform Detection ───────────────────────────────────────────────────────
IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"

# ── Default Paths ────────────────────────────────────────────────────────────
def get_default_output_dir():
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                              os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "stt-recognizer", "transcriptions")


def get_skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_model_search_paths():
    """Get search paths for Whisper models, in priority order."""
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                              os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    skill_dir = get_skill_dir()
    # 按技能命名的统一缓存位置
    skill_cache_dir = os.path.expanduser("~/.cache/huggingface/modules/stt-recognizer")
    return [
        os.environ.get("STT_MODEL_PATH", ""),
        # 统一缓存位置（按技能命名）
        os.path.join(skill_cache_dir, "small"),
        os.path.join(skill_cache_dir, "base"),
        os.path.join(skill_cache_dir, "tiny"),
        os.path.join(skill_cache_dir, "medium"),
        os.path.join(skill_cache_dir, "large"),
        skill_cache_dir,
        # 工作区备份
        os.path.join(skill_dir, "models"),
        os.path.join(workspace, "stt-recognizer", "models"),
        # 通用 HuggingFace 缓存（faster-whisper 默认位置）
        os.path.expanduser("~/.cache/huggingface/modules"),
        ".",
    ]


def find_model(model_name_or_path):
    """Find Whisper model file or directory.
    
    faster-whisper models are directories (e.g. ~/.cache/huggingface/modules/stt-recognizer/small/)
    containing model.bin, config.json, etc. This function resolves a bare model name
    like "small" to the correct directory path.
    """
    path = Path(model_name_or_path)

    if path.is_absolute() and path.exists():
        return str(path)

    # If it's a directory (like faster-whisper models), return as-is
    if path.is_dir():
        return str(path)

    # If it's just a name like "small", search for a directory with that name
    for search_dir in get_model_search_paths():
        if not search_dir:
            continue
        # Check if search_dir itself is the model directory (e.g. ~/.cache/.../stt-recognizer/small)
        candidate_dir = Path(search_dir)
        if candidate_dir.name == path.name and candidate_dir.is_dir():
            return str(candidate_dir)
        # Also check subdirectory named after the model (backwards compat)
        candidate = candidate_dir / path.name
        if candidate.exists():
            return str(candidate)

    return model_name_or_path  # Return original, let faster-whisper handle it


# ── Transcription Engines ────────────────────────────────────────────────────
def transcribe_with_faster_whisper(audio_path, model_name_or_path, language, output_path, task="transcribe"):
    """Transcribe using faster-whisper (local, GPU/CPU efficient)."""
    from faster_whisper import WhisperModel

    model_path = find_model(model_name_or_path)

    # Determine compute type based on hardware
    # Note: GTX 10xx (Pascal, compute capability 6.x) does NOT support efficient float16
    # Use float32 or int8_float16 on these GPUs
    if torch.cuda.is_available():
        try:
            gpu_name = torch.cuda.get_device_name(0)
            if "GTX 10" in gpu_name or "GTX 16" in gpu_name or "Pascal" in gpu_name:
                # Pascal (GTX 10xx, 16xx) - use float32
                compute_type = "float32"
            elif IS_MACOS:
                compute_type = "int8"  # Apple Silicon
            else:
                compute_type = "float16"  # Ampere and newer
        except Exception:
            compute_type = "float32"  # Fallback
    elif IS_MACOS:
        compute_type = "int8"  # Apple Silicon
    else:
        compute_type = "int8"

    print(f"  Loading faster-whisper model: {model_path}")
    print(f"  Compute type: {compute_type}")

    model = WhisperModel(
        model_path,
        compute_type=compute_type,
        device="cuda" if torch.cuda.is_available() else "cpu"
    )

    # Task: transcribe or translate
    do_translate = task == "translate"

    print(f"  Transcribing...")
    segments, info = model.transcribe(
        audio_path,
        language=language if language else None,
        task="translate" if do_translate else "transcribe",
        beam_size=5,
        vad_filter=True  # Voice activity detection
    )

    print(f"  Detected language: {info.language} (probability: {info.language_probability:.2f})")

    # Collect results
    full_text = []
    with open(output_path, 'w', encoding='utf-8') as f:
        for segment in segments:
            text = segment.text.strip()
            full_text.append(text)
            start = time.strftime("%H:%M:%S", time.gmtime(segment.start))
            end = time.strftime("%H:%M:%S", time.gmtime(segment.end))
            f.write(f"[{start} --> {end}] {text}\n")

    return ' '.join(full_text)


def transcribe_with_whisper(audio_path, model_name_or_path, language, output_path, task="transcribe"):
    """Transcribe using openai-whisper (local, full model)."""
    import whisper

    model_path = find_model(model_name_or_path)

    print(f"  Loading whisper model: {model_path}")
    model = whisper.load_model(model_path)

    print(f"  Transcribing...")
    options = {
        "task": task,
        "language": language if language else None,
        "beam_size": 5,
    }

    # Check for GPU
    if torch.cuda.is_available():
        model = model.cuda()

    result = model.transcribe(audio_path, **options)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        for segment in result['segments']:
            start = time.strftime("%H:%M:%S", time.gmtime(segment['start']))
            end = time.strftime("%H:%M:%S", time.gmtime(segment['end']))
            f.write(f"[{start} --> {end}] {segment['text'].strip()}\n")

    return result['text'].strip()


def transcribe_with_api(audio_path, api_url, api_key, model_name, language, output_path):
    """Transcribe using OpenAI-compatible API."""
    import openai
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=api_url)

    print(f"  Sending to API: {api_url}")
    print(f"  Model: {model_name}")

    with open(audio_path, 'rb') as f:
        transcript = client.audio.transcriptions.create(
            model=model_name,
            file=f,
            language=language if language else None,
            response_format="verbose_json",
        )

    # Write output
    text = transcript.text if hasattr(transcript, 'text') else str(transcript)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    return text


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio to text using Whisper (local or API)."
    )
    parser.add_argument("audio_file", help="Audio file to transcribe (WAV, MP3, OGG, etc.)")
    parser.add_argument("--model", default="base",
                        help="Model name or path (default: 'base'). "
                             "Local: 'tiny', 'base', 'small', 'medium', 'large'. "
                             "API: model identifier")
    parser.add_argument("--language", default=None,
                        help="Source language code (e.g., 'zh', 'en', 'ja'). Auto-detect if not specified.")
    parser.add_argument("--task", default="transcribe", choices=["transcribe", "translate"],
                        help="Task: 'transcribe' (default) or 'translate' (to English)")
    parser.add_argument("--engine", default="auto", choices=["auto", "faster-whisper", "whisper", "api"],
                        help="Transcription engine (default: auto-detect)")
    parser.add_argument("--api-url", default=os.environ.get("STT_API_URL", ""),
                        help="OpenAI-compatible API URL (for api engine)")
    parser.add_argument("--api-key", default=os.environ.get("STT_API_KEY", ""),
                        help="API key (for api engine)")
    parser.add_argument("--output-dir", default=None,
                        help=f"Output directory (default: ~/.../projects/stt-recognizer/transcriptions)")
    parser.add_argument("--output-format", default="txt", choices=["txt", "srt", "vtt"],
                        help="Output format (default: txt)")
    args = parser.parse_args()

    # Validate audio file
    if not os.path.exists(args.audio_file):
        print(f"ERROR: Audio file not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    # Setup output
    output_dir = args.output_dir or get_default_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename
    audio_basename = os.path.splitext(os.path.basename(args.audio_file))[0]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"{audio_basename}_{timestamp}.{args.output_format}")

    print("[Audio Transcription] Starting...")
    print(f"  Audio:       {args.audio_file}")
    print(f"  Model:       {args.model}")
    print(f"  Language:    {args.language or 'auto-detect'}")
    print(f"  Task:        {args.task}")
    print(f"  Engine:      {args.engine}")
    print(f"  Output:      {output_path}")
    print()

    # Auto-detect engine if needed
    if args.engine == "auto":
        if args.api_url and args.api_key:
            args.engine = "api"
        elif shutil.which("python3"):
            try:
                import faster_whisper
                args.engine = "faster-whisper"
            except ImportError:
                try:
                    import whisper
                    args.engine = "whisper"
                except ImportError:
                    args.engine = "api"  # Fallback to API
        else:
            args.engine = "api"

    print(f"Using engine: {args.engine}")
    print()

    # Run transcription
    start_time = time.time()

    try:
        if args.engine == "api":
            text = transcribe_with_api(
                args.audio_file,
                args.api_url,
                args.api_key,
                args.model,
                args.language,
                output_path
            )
        elif args.engine == "faster-whisper":
            text = transcribe_with_faster_whisper(
                args.audio_file,
                args.model,
                args.language,
                output_path,
                args.task
            )
        elif args.engine == "whisper":
            text = transcribe_with_whisper(
                args.audio_file,
                args.model,
                args.language,
                output_path,
                args.task
            )
    except Exception as e:
        print(f"ERROR: Transcription failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    elapsed = time.time() - start_time

    print()
    print(f"Done! Transcription saved: {output_path}")
    print(f"  Time: {elapsed:.1f}s")
    print()
    print("=" * 60)
    print("TRANSCRIPTION RESULT:")
    print("=" * 60)
    print(text)
    print("=" * 60)

    return text


if __name__ == "__main__":
    main()
