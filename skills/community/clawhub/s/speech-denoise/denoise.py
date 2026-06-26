"""
Modal service: Single-stage speech enhancement pipeline.

ffmpeg conversion (CPU) and model loading (GPU) run in parallel via ThreadPoolExecutor.
GPU inference then processes each .flac file sequentially.

Usage:
    modal run denoise.py --slug <slug>
"""

import concurrent.futures
import io
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import src.config as config
import src.images as images


def _run_ffmpeg(
    upload_dir: Path, intermediate_dir: Path
) -> tuple[list[dict], list[str]]:
    """
    Convert all audio/video files in upload/ to 48kHz .flac.
    Output goes to /tmp/speech2srt-denoise/<slug>/.
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
            str(config.AUDIO_SAMPLE_RATE),
            "-ac",
            str(config.AUDIO_CHANNELS),
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
            f"  {upload_file.name} → {output_file.name}"
            f"  {input_size_mb:.2f}MB → {output_size_mb:.2f}MB"
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


def _load_model():
    """
    Load ClearerVoice-Studio model. Runs in ThreadPool while ffmpeg is running.
    Returns (model, log_lines).
    """
    from clearvoice import ClearVoice

    log_lines = []
    MODELS_DIR = Path(config.MOUNT_MODELS)
    CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
    workdir_checkpoints = Path.home() / "checkpoints"

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    if not workdir_checkpoints.exists() or not workdir_checkpoints.is_symlink():
        workdir_checkpoints.parent.mkdir(parents=True, exist_ok=True)
        if workdir_checkpoints.exists():
            workdir_checkpoints.rmdir()
        workdir_checkpoints.symlink_to(CHECKPOINTS_DIR)

    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

    if CHECKPOINTS_DIR.exists():
        total_size = sum(
            f.stat().st_size for f in CHECKPOINTS_DIR.rglob("*") if f.is_file()
        )
        cache_mb = total_size / (1024 * 1024)
    else:
        cache_mb = 0.0

    log_lines.append(
        f"  ClearerVoice-Studio MossFormer2_SE_48K  [cache: {cache_mb:.2f}MB]"
    )

    model_t0 = time.monotonic()
    myClearVoice = ClearVoice(
        task="speech_enhancement", model_names=["MossFormer2_SE_48K"]
    )
    model_elapsed = time.monotonic() - model_t0
    log_lines.append(f"  model init: {model_elapsed:.1f}s")

    return myClearVoice, log_lines


@images.app.function(
    image=images.image_denoise,
    gpu=config.GPU_TYPE,
    volumes={
        config.MOUNT_DATA: images.volume_data,
        config.MOUNT_MODELS: images.volume_models,
    },
    timeout=config.TIMEOUT_DENOISE,
    retries=0,
)
def denoise(slug: str) -> list[dict]:
    """
    Single-stage speech enhancement on L4 GPU.

    ffmpeg conversion (CPU) and model loading (GPU) run in parallel via ThreadPoolExecutor.
    Then GPU inference processes each .flac file sequentially.
    """
    t0 = time.monotonic()

    upload_dir = Path(config.MOUNT_DATA) / slug / config.DIR_UPLOAD
    intermediate_dir = Path(config.TMP_PREFIX_DENOISE) / slug
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
        model_future = executor.submit(_load_model)

        ffmpeg_results, ffmpeg_lines = ffmpeg_future.result()
        myClearVoice, model_lines = model_future.result()

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
    import soundfile as sf

    flac_files = sorted(intermediate_dir.glob(f"*{config.FLAC_EXTENSION}"))
    total_audio_sec = 0.0

    print(f"\n[gpu]  {len(flac_files)} file(s) to process")
    results = []

    for flac_file in flac_files:
        output_path = output_dir / f"{flac_file.stem}{config.ENHANCED_SUFFIX}"

        audio_info = sf.info(str(flac_file))
        audio_duration = audio_info.frames / audio_info.samplerate
        total_audio_sec += audio_duration

        file_size = flac_file.stat().st_size / (1024 * 1024)

        proc_t0 = time.monotonic()
        sys.stdout.flush()

        output_wav = myClearVoice(input_path=str(flac_file), online_write=False)
        proc_elapsed = time.monotonic() - proc_t0
        rtf = proc_elapsed / audio_duration if audio_duration > 0 else 0

        # Write enhanced audio to Volume
        if output_wav.ndim == config.AUDIO_STEREO_NDIM:
            output_wav = output_wav.T

        buffer = io.BytesIO()
        sf.write(
            buffer,
            output_wav,
            samplerate=config.AUDIO_SAMPLE_RATE,
            subtype=config.AUDIO_SUBTYPE,
            format=config.AUDIO_FORMAT,
        )
        buffer.seek(0)
        output_path.write_bytes(buffer.getvalue())

        output_size = output_path.stat().st_size / (1024 * 1024)

        print(
            f"  {output_path.name}"
            f"  {file_size:.2f}MB → {output_size:.2f}MB"
            f"  [{proc_elapsed:.1f}s, RTF={rtf:.2f}x]"
            f"  dur={audio_duration:.0f}s"
        )

        results.append(
            {
                "input": flac_file.name,
                "output": output_path.name,
                "input_size_mb": round(file_size, 2),
                "output_size_mb": round(output_size, 2),
                "duration_sec": round(audio_duration, 2),
                "rtf": round(rtf, 3),
            }
        )

    # Clean up intermediate .flac files from container SSD
    shutil.rmtree(Path(config.TMP_PREFIX_DENOISE) / slug, ignore_errors=True)

    elapsed = time.monotonic() - t0
    total_rtf = elapsed / total_audio_sec if total_audio_sec > 0 else 0

    bar = "─" * 50
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


@images.app.local_entrypoint()
def main(slug: str) -> None:
    """CLI entry point: modal run denoise.py --slug <slug>"""
    results = denoise.remote(slug)

    if results:
        print(f"\nPipeline complete. Enhanced {len(results)} files.")
    else:
        print("\nPipeline completed but no files were enhanced.")


if __name__ == "__main__":
    images.app.run()
