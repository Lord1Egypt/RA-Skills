#!/usr/bin/env python3
"""video-insight Bilibili module: download + whisper transcription + optional keyframes."""

import os
import sys
import glob
import json
import subprocess
from typing import Dict, Optional, List

from utils import (
    extract_bilibili_id, progress, load_settings, get_setting,
    TempManager, check_disk_space, ok_result, err_result
)

SETTINGS = load_settings()


def _get_bilibili_title(url: str) -> str:
    """Get Bilibili video title via yt-dlp --print title."""
    retries = int(get_setting("yt_dlp_retries", 3, settings=SETTINGS))
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "title", "--retries", str(retries), "--no-warnings", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return "B站视频"


def _get_bilibili_duration(url: str) -> int:
    """Get Bilibili video duration via yt-dlp."""
    retries = int(get_setting("yt_dlp_retries", 3, settings=SETTINGS))
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "duration", "--retries", str(retries), "--no-warnings", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return int(float(result.stdout.strip()))
    except Exception:
        pass
    return 0


def _get_bilibili_channel(url: str) -> str:
    """Get Bilibili uploader name via yt-dlp."""
    retries = int(get_setting("yt_dlp_retries", 3, settings=SETTINGS))
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "uploader", "--retries", str(retries), "--no-warnings", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return "Bilibili"


def select_key_frames(frame_files: list, target_count: int = 10, oversample_ratio: float = 1.5) -> list:
    """Select key frames from extracted frames using uniform sampling."""
    total = len(frame_files)
    actual_count = min(round(target_count * oversample_ratio), total)

    if total <= actual_count + 3:
        return frame_files

    indices = [0]
    step = (total - 1) / (actual_count - 1)
    for i in range(1, actual_count - 1):
        indices.append(round(i * step))
    indices.append(total - 1)
    indices = sorted(set(indices))
    return [frame_files[i] for i in indices]


def process_bilibili(
    url: str,
    cache=None,
    no_cache: bool = False,
    extract_frames: bool = False,
    whisper_model: str = None,
    frame_interval: int = None,
    max_frames: int = None,
    temp_manager: TempManager = None,
) -> dict:
    """Process a Bilibili video. Returns unified result dict."""
    video_id = extract_bilibili_id(url)
    progress(f"🎬 Bilibili: {video_id}")

    # Check cache
    if cache and not no_cache:
        cached = cache.get("bilibili", video_id)
        if cached:
            progress("  ✅ Cache hit")
            return cached

    # Load settings
    whisper_model = whisper_model or get_setting("whisper_model", "small", "WHISPER_MODEL", SETTINGS)
    frame_interval = frame_interval or int(get_setting("frame_interval", 30, "FRAME_INTERVAL", SETTINGS))
    max_frames = max_frames or int(get_setting("max_frames", 15, "MAX_FRAMES", SETTINGS))
    retries = str(get_setting("yt_dlp_retries", 3, settings=SETTINGS))
    frag_retries = str(get_setting("yt_dlp_fragment_retries", 3, settings=SETTINGS))
    yt_dlp_timeout = int(get_setting("yt_dlp_timeout", 300, settings=SETTINGS))
    ffmpeg_timeout = int(get_setting("ffmpeg_timeout", 120, settings=SETTINGS))

    # Disk space check
    threshold = float(get_setting("disk_space_threshold_gb", 5.0, settings=SETTINGS))
    space_ok, free_gb = check_disk_space("/tmp", threshold)
    if not space_ok:
        return err_result(f"Disk space too low: {free_gb:.1f} GB free, need {threshold} GB", "DISK_SPACE")

    # Set up temp directory
    own_temp = False
    if temp_manager is None:
        temp_manager = TempManager()
        own_temp = True

    video_path = temp_manager.get_path(f"bili_{video_id}.mp4")
    audio_path = temp_manager.get_path(f"bili_{video_id}_audio.mp3")
    frames_dir = temp_manager.get_path(f"bili_{video_id}_frames")

    try:
        # Step 0: Get metadata
        progress("  📋 Fetching metadata...")
        title = _get_bilibili_title(url)
        channel = _get_bilibili_channel(url)
        duration = _get_bilibili_duration(url)
        progress(f"  📋 Title: {title}")

        # Step 1: Download video
        progress("  📥 Downloading video...")
        base_cmd = [
            "yt-dlp",
            "--no-check-certificates",
            "--retries", retries,
            "--fragment-retries", frag_retries,
            "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "--merge-output-format", "mp4",
            "-o", video_path,
            url,
        ]
        try:
            subprocess.run(base_cmd, check=True, timeout=yt_dlp_timeout, capture_output=True)
        except subprocess.CalledProcessError:
            progress("  ⚠️  Retrying with browser cookies...")
            cookie_cmd = [
                "yt-dlp",
                "--cookies-from-browser", "chrome",
                "--no-check-certificates",
                "--retries", retries,
                "--fragment-retries", frag_retries,
                "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "--merge-output-format", "mp4",
                "-o", video_path,
                url,
            ]
            subprocess.run(cookie_cmd, check=True, timeout=yt_dlp_timeout, capture_output=True)

        # Step 2: Extract audio
        progress("  🎵 Extracting audio...")
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-q:a", "2", audio_path],
            check=True, timeout=ffmpeg_timeout, capture_output=True,
        )

        # Step 3: Whisper transcription (language=auto)
        progress(f"  🗣️  Transcribing (whisper {whisper_model})...")
        from faster_whisper import WhisperModel

        whisper_device = os.environ.get("WHISPER_DEVICE", get_setting("whisper_device", "auto", settings=SETTINGS))
        whisper_compute = get_setting("whisper_compute_type", "auto", settings=SETTINGS)

        if whisper_device == "auto":
            try:
                import ctranslate2 as _ct2
                cuda_types = _ct2.get_supported_compute_types("cuda")
                whisper_device = "cuda"
                whisper_compute = "float16" if "float16" in cuda_types else "int8"
            except Exception:
                whisper_device = "cpu"
                whisper_compute = "int8"

        progress(f"  🖥️  Whisper device: {whisper_device} ({whisper_compute})")
        model = WhisperModel(whisper_model, device=whisper_device, compute_type=whisper_compute)

        # language=None means auto-detect (fixes C4)
        whisper_lang = get_setting("whisper_language", "auto", settings=SETTINGS)
        lang_param = None if whisper_lang == "auto" else whisper_lang

        segments_iter, info = model.transcribe(audio_path, language=lang_param)
        segments_list = list(segments_iter)

        progress(f"  🗣️  Detected language: {info.language} (prob={info.language_probability:.2f})")

        transcript_lines = [f"[{s.start:.1f}-{s.end:.1f}] {s.text}" for s in segments_list]
        transcript_with_timestamps = "\n".join(transcript_lines)
        transcript_plain = " ".join(s.text for s in segments_list)

        progress(f"  ✅ Transcript: {len(transcript_plain)} chars")

        # Remove video immediately after audio extraction (save disk)
        temp_manager.remove_early(video_path)

        # Step 4: Extract keyframes (optional)
        frames = []
        if extract_frames:
            progress(f"  🖼️  Extracting keyframes (every {frame_interval}s)...")
            os.makedirs(frames_dir, exist_ok=True)
            subprocess.run(
                [
                    "ffmpeg", "-y", "-i", video_path if os.path.exists(video_path) else audio_path,
                    "-vf", f"fps=1/{frame_interval}", "-q:v", "2",
                    os.path.join(frames_dir, "frame_%03d.jpg"),
                ],
                check=True, timeout=ffmpeg_timeout, capture_output=True,
            )
            frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
            selected = select_key_frames(frame_files, max_frames)
            frame_offset = int(os.environ.get("FRAME_TIME_OFFSET", "5"))
            for fp in selected:
                num = int(os.path.basename(fp).split("_")[1].split(".")[0])
                frames.append({
                    "file": fp,
                    "time_sec": (num - 1) * frame_interval + frame_offset,
                })
            progress(f"  ✅ Keyframes: {len(frames)}")

        result = {
            "video_id": video_id,
            "platform": "bilibili",
            "title": title,
            "channel": channel,
            "duration_seconds": duration,
            "transcript": transcript_plain,
            "transcript_with_timestamps": transcript_with_timestamps,
            "frames": frames,
            "cached": False,
        }

        # Cache transcript
        if cache:
            cache.put("bilibili", video_id, result)
            progress("  💾 Cached")

        progress(f"  ✅ Done: {len(transcript_plain)} chars")
        return result

    except FileNotFoundError as e:
        cmd = str(e).split("'")[-2] if "'" in str(e) else "unknown"
        return err_result(f"Missing dependency: {cmd}. Run setup.sh first.", "MISSING_DEP")
    except subprocess.CalledProcessError as e:
        return err_result(f"Command failed: {e.cmd[0] if e.cmd else 'unknown'} (exit {e.returncode})", "CMD_FAILED")
    except subprocess.TimeoutExpired:
        return err_result("Processing timed out. Video may be too large or network too slow.", "TIMEOUT")
    except ImportError as e:
        return err_result(f"Missing Python package: {e.name}. Run setup.sh to install.", "MISSING_PACKAGE")
    except Exception as e:
        return err_result(f"Unexpected error: {type(e).__name__}: {e}", "UNKNOWN")
    finally:
        if own_temp:
            temp_manager.cleanup()
