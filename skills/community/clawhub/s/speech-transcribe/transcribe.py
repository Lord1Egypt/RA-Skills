"""
Modal service: Whisper transcription pipeline.

ffmpeg conversion (CPU) and model loading (GPU) run in parallel via ThreadPoolExecutor.
GPU inference generates both plain text (.txt) and subtitle (.srt) outputs.

Usage:
    modal run transcribe.py --slug <slug> --model <model>

Options:
    --model  Whisper model size: tiny, base, small, medium, large-v3 (default: large-v3)
"""

import concurrent.futures
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import src.config as config
import src.images as images

# Whisper native sample rate (16kHz), different from denoise/isolate at 48kHz
_TRANSCRIBE_SAMPLE_RATE = 16000
_TRANSCRIBE_CHANNELS = 1


# ============================================================
# SRT Generation
# ============================================================


def _format_srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def _segments_to_srt(segments: list[dict]) -> str:
    """Convert Whisper segments to SRT format (sentence-level timestamps)."""
    srt_lines = []
    for i, seg in enumerate(segments, start=1):
        start = _format_srt_time(seg["start"])
        end = _format_srt_time(seg["end"])
        text = seg["text"].strip()
        srt_lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(srt_lines)


def _segments_to_txt(segments: list[dict]) -> str:
    """Convert Whisper segments to plain text."""
    return "\n\n".join(seg["text"].strip() for seg in segments)


# ============================================================
# FFmpeg Conversion
# ============================================================


def _run_ffmpeg(
    upload_dir: Path, intermediate_dir: Path
) -> tuple[list[dict], list[str]]:
    """
    Convert all audio/video files in upload/ to 16kHz mono .flac (Whisper native sample rate).
    Output goes to /tmp/speech2srt-transcribe/<slug>/.
    Runs in ThreadPool. Returns (results, log_lines).
    """
    intermediate_dir.mkdir(parents=True, exist_ok=True)
    log_lines: list[str] = []
    results: list[dict] = []

    upload_files = sorted(f for f in upload_dir.iterdir() if f.is_file())
    if not upload_files:
        return results, log_lines

    for upload_file in upload_files:
        probe_cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(upload_file),
        ]
        audio_duration = 0.0
        try:
            probe_result = subprocess.run(
                probe_cmd,
                capture_output=True,
                text=True,
                timeout=config.FFPROBE_TIMEOUT,
            )
            data = json.loads(probe_result.stdout)
            streams = data.get("streams", [])
            has_audio = any(s.get("codec_type") == "audio" for s in streams)
            if has_audio:
                audio_duration = float(data.get("format", {}).get("duration", 0))
        except Exception:
            has_audio = False

        if not has_audio:
            log_lines.append(f"  {upload_file.name}  [skip - no audio]")
            continue

        output_file = intermediate_dir / f"{upload_file.stem}{config.FLAC_EXTENSION}"

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(upload_file),
            "-vn",
            "-acodec",
            "flac",
            "-ar",
            str(_TRANSCRIBE_SAMPLE_RATE),
            "-ac",
            str(_TRANSCRIBE_CHANNELS),
            str(output_file),
        ]

        conv_t0 = time.monotonic()
        subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=config.FFMPEG_TIMEOUT,
            check=True,
        )
        conv_elapsed = time.monotonic() - conv_t0
        input_size_mb = upload_file.stat().st_size / (1024 * 1024)
        output_size_mb = output_file.stat().st_size / (1024 * 1024)
        rtf = conv_elapsed / audio_duration if audio_duration > 0 else 0

        log_lines.append(
            f"  {upload_file.name} -> {output_file.name}"
            f"  {input_size_mb:.2f}MB -> {output_size_mb:.2f}MB"
            f"  [{conv_elapsed:.1f}s, RTF={rtf:.4f}x]"
        )

        results.append(
            {
                "original": upload_file.name,
                "converted": output_file.name,
                "input_size_mb": round(input_size_mb, 2),
                "output_size_mb": round(output_size_mb, 2),
                "duration_sec": round(audio_duration, 2),
                "rtf": round(rtf, 4),
            }
        )

    return results, log_lines


# ============================================================
# Model Loading
# ============================================================


def _load_model(model: str) -> tuple:
    """
    Load Whisper model. Runs in ThreadPool while ffmpeg is running.
    Returns (whisper_model, model, log_lines).
    """
    import torch
    import stable_whisper

    log_lines: list[str] = []

    # Symlink ~/.cache to volume models directory so downloaded models persist to volume
    cache_dir = Path.home() / ".cache"
    models_dir = Path(config.MOUNT_MODELS)

    cache_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    if not cache_dir.is_symlink():
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        cache_dir.symlink_to(models_dir, target_is_directory=True)

    # Calculate cache size (entire ~/.cache)
    cache_mb = 0.0
    if cache_dir.exists():
        cache_mb = sum(
            f.stat().st_size for f in cache_dir.rglob("*") if f.is_file()
        ) / (1024 * 1024)

    log_lines.append(f"  whisper {model}  [cache: {cache_mb:.2f}MB]")

    model_t0 = time.monotonic()

    # device="cuda": use GPU
    # compute_type="int8_float16": L4 optimized precision/speed balance
    # cpu_threads=4, num_workers=4: CPU thread pool for data preprocessing
    whisper_model = stable_whisper.load_faster_whisper(
        model,
        device="cuda",
        compute_type="int8_float16",
        cpu_threads=4,
        num_workers=4,
    )
    model_elapsed = time.monotonic() - model_t0

    device = "GPU" if torch.cuda.is_available() else "CPU"
    log_lines.append(f"  model init: {model_elapsed:.1f}s ({device})")
    return whisper_model, model, log_lines


# ============================================================
# Main Modal Function
# ============================================================


@images.app_whisper.function(
    image=images.image_whisper,
    gpu=config.GPU_TYPE,
    volumes={
        config.MOUNT_DATA: images.volume_data,
        config.MOUNT_MODELS: images.volume_models,
    },
    timeout=config.TIMEOUT_TRANSCRIBE,
    retries=0,
)
def transcribe(slug: str, model: str = "large-v3") -> list[dict]:
    """
    Single-stage Whisper transcription on L4 GPU.

    ffmpeg conversion (CPU) and model loading (GPU) run in parallel via ThreadPoolExecutor.
    GPU inference generates .txt (plain text) and .srt (subtitles) for each audio file.
    Supports int8_float16.

    Args:
        slug: Project slug for input/output directories.
        model: Whisper model size. Options: tiny, base, small, medium, large-v3.
               Default: large-v3 (highest accuracy).
    """
    t0 = time.monotonic()

    upload_dir = Path(config.MOUNT_DATA) / slug / config.DIR_UPLOAD
    intermediate_dir = Path(config.TMP_PREFIX_TRANSCRIBE) / slug
    output_dir = Path(config.MOUNT_DATA) / slug / config.DIR_OUTPUT
    output_dir.mkdir(parents=True, exist_ok=True)

    if not upload_dir.exists():
        print(f"[ERROR] Upload directory does not exist: {upload_dir}")
        return []

    upload_files = [f for f in upload_dir.iterdir() if f.is_file()]
    print(f"[ffmpeg] {len(upload_files)} file(s) to convert")
    print("[model]  loading...")

    # -----------------------------------------------------------
    # Parallel: ffmpeg (CPU) + model load (GPU)
    # -----------------------------------------------------------
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        ffmpeg_future = executor.submit(_run_ffmpeg, upload_dir, intermediate_dir)
        model_future = executor.submit(_load_model, model)

        ffmpeg_results, ffmpeg_lines = ffmpeg_future.result()
        whisper_model, model, model_lines = model_future.result()

    # Print buffered parallel-phase logs
    for line in ffmpeg_lines:
        print(line)
    for line in model_lines:
        print(line)

    if not ffmpeg_results:
        print("[ffmpeg] no audio files found")
        return []

    # -----------------------------------------------------------
    # Serial: GPU inference on each .flac file
    # -----------------------------------------------------------
    flac_files = sorted(intermediate_dir.glob(f"*{config.FLAC_EXTENSION}"))
    total_audio_sec = 0.0

    print(f"\n[gpu]  {len(flac_files)} file(s) to process")
    results = []

    for flac_file in flac_files:
        # Output file paths
        txt_path = output_dir / f"{flac_file.stem}{config.TRANSCRIPTION_SUFFIX}.txt"
        srt_path = output_dir / f"{flac_file.stem}{config.TRANSCRIPTION_SUFFIX}.srt"

        # Get audio duration
        audio_duration = 0.0
        try:
            probe_cmd = [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                str(flac_file),
            ]
            probe_result = subprocess.run(
                probe_cmd, capture_output=True, text=True, timeout=30
            )
            data = json.loads(probe_result.stdout)
            audio_duration = float(data.get("format", {}).get("duration", 0))
        except Exception:
            pass

        total_audio_sec += audio_duration
        file_size = flac_file.stat().st_size / (1024 * 1024)

        proc_t0 = time.monotonic()
        sys.stdout.flush()

        # GPU inference with sentence-level timestamps
        result = whisper_model.transcribe(
            audio=str(flac_file),
            language=None,  # auto-detect
            vad=True,  # enable Silero VAD for better timestamps
            word_timestamps=True,  # for sentence-level merging
            suppress_silence=True,  # suppress silent segments
        )

        # Collect segment results
        segment_list = [
            {"start": seg.start, "end": seg.end, "text": seg.text}
            for seg in result.segments
        ]

        proc_elapsed = time.monotonic() - proc_t0
        rtf = proc_elapsed / audio_duration if audio_duration > 0 else 0

        # Write .txt and .srt
        txt_content = _segments_to_txt(segment_list)
        srt_content = _segments_to_srt(segment_list)

        txt_path.write_text(txt_content, encoding="utf-8")
        srt_path.write_text(srt_content, encoding="utf-8")

        txt_size = txt_path.stat().st_size / 1024
        srt_size = srt_path.stat().st_size / 1024

        print(
            f"  {flac_file.stem}"
            f"  {file_size:.2f}MB"
            f"  [{proc_elapsed:.1f}s, RTF={rtf:.2f}x]"
            f"  dur={audio_duration:.0f}s"
        )
        print(
            f"    -> {txt_path.name}  ({txt_size:.1f}KB)"
            f"  + {srt_path.name}  ({srt_size:.1f}KB)"
        )

        results.append(
            {
                "input": flac_file.name,
                "txt": txt_path.name,
                "srt": srt_path.name,
                "input_size_mb": round(file_size, 2),
                "duration_sec": round(audio_duration, 2),
                "rtf": round(rtf, 3),
            }
        )

    # Clean up intermediate .flac files from container SSD
    shutil.rmtree(Path(config.TMP_PREFIX_TRANSCRIBE) / slug, ignore_errors=True)

    elapsed = time.monotonic() - t0
    total_rtf = elapsed / total_audio_sec if total_audio_sec > 0 else 0

    bar = "-" * 50
    print(f"\n{bar}")
    print(
        f"  done. {len(results)} files,"
        f"  audio={total_audio_sec:.0f}s,"
        f"  wall={elapsed:.1f}s,"
        f"  RTF={total_rtf:.2f}x"
    )
    print(bar)

    images.volume_data.commit()

    return results


@images.app_whisper.local_entrypoint()
def main(slug: str, model: str = "large-v3") -> None:
    """CLI entry point: modal run transcribe.py --slug <slug> --model <model>"""
    results = transcribe.remote(slug, model=model)

    if results:
        print(f"\nPipeline complete. Transcribed {len(results)} files.")
    else:
        print("\nPipeline completed but no files were processed.")


if __name__ == "__main__":
    images.app_whisper.run()
