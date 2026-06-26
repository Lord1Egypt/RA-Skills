#!/usr/bin/env python3
"""
Pipeline: End-to-end video generation with PPTX support and Edge TTS priority.

Three-stage workflow:
  Stage 1: Big loop over ALL slides — for each slide:
             Generate TTS audio → immediately validate via STT (small loop)
             Validation: audio→text similarity >= threshold (default 0.6)
             Retry up to max_retries (default 5) times per slide
             If any slide fails after all retries → ABORT
  Stage 2: Generate video for each slide (image + validated audio + subtitle)
  Stage 3: Merge all slide videos into final output

PPTX Support:
  - Auto-detection: Uses PPTX if PDF not available
  - High-quality: PPTX → PDF → PNG via LibreOffice (recommended)
  - Fallback: Python-pptx based conversion when LibreOffice not available

TTS Priority: Edge TTS (default) → Qwen3-TTS → HTTP Service
"""

import argparse
import asyncio
import json
import subprocess
import sys
import time
import wave
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from utils import (
    PROJECT_ROOT, SLIDES_DIR, SCRIPTS_DIR, OUTPUT_DIR,
    IMAGES_DIR, AUDIO_DIR, VIDEO_DIR, SCRIPT_JSON, PDF_PATH, PPTX_PATH, CONFIG_PATH,
    load_config, parse_json_subtitles, parse_slide_range,
    normalize_text, compute_similarity, compute_char_coverage,
    flush_print, format_duration,
)


# ============================================================
# Load configuration from config.json
# ============================================================

_config = load_config()

# ---- TTS settings (from config.json) ----
VOICE_NAME = _config["tts"]["voice_name"]
LANG_CODE = _config["tts"]["lang_code"]
SPEECH_SPEED = _config["tts"]["speech_speed"]
BASE_TEMPERATURE = _config["tts"]["base_temperature"]

# ---- Edge TTS settings (from config.json) ----
_edge_tts_cfg = _config.get("edge_tts", {})
EDGE_TTS_VOICE = _edge_tts_cfg.get("voice", "zh-CN-YunyangNeural")
EDGE_TTS_RATE = _edge_tts_cfg.get("rate", "+0%")
EDGE_TTS_VOLUME = _edge_tts_cfg.get("volume", "+0%")

# ---- Validation settings (from config.json) ----
DEFAULT_THRESHOLD = _config["validation"]["threshold"]
DEFAULT_MAX_RETRIES = _config["validation"]["max_retries"]
CHARS_PER_SEC = _config["validation"]["chars_per_sec"]
DURATION_TOLERANCE = _config["validation"]["duration_tolerance"]

# ---- Video settings (from config.json) ----
VIDEO_FPS = _config["video"]["fps"]
VIDEO_FPS_FAST = _config["video"]["fps_fast"]
VIDEO_CODEC = _config["video"]["video_codec"]
AUDIO_CODEC = _config["video"]["audio_codec"]

# ---- STT model (from config.json) ----
STT_MODEL_ID = _config["stt"]["model_id"]


# ============================================================
# TTS mode management (Edge TTS as default)
# ============================================================

_tts_mode = "edge"   # "edge" (default), "direct", or "http"
_tts_http_url = None   # HTTP server URL (only used in http mode)
_tts_loaded = False

DEFAULT_TTS_URL = "http://localhost:8100"


def set_tts_mode(mode: str, url: str = None):
    """Configure TTS mode: 'direct' (Qwen3-TTS), 'http', or 'edge' (default)."""
    global _tts_mode, _tts_http_url
    _tts_mode = mode
    _tts_http_url = url or DEFAULT_TTS_URL


def _override_edge_settings(voice: str = None, rate: str = None):
    """Override Edge TTS settings from CLI arguments."""
    global EDGE_TTS_VOICE, EDGE_TTS_RATE
    if voice:
        EDGE_TTS_VOICE = voice
    if rate:
        EDGE_TTS_RATE = rate


def load_tts_model():
    """
    Load TTS model. Behavior depends on current mode:
      - edge: verify edge-tts package available (default)
      - direct: load Qwen3-TTS model into memory
      - http: verify HTTP server is reachable
    """
    global _tts_loaded

    if _tts_loaded:
        return

    if _tts_mode == "edge":
        # Edge TTS: no model to load, just verify the package is available
        flush_print(f"\n[TTS] Edge TTS mode — voice: {EDGE_TTS_VOICE}, rate: {EDGE_TTS_RATE}")
        try:
            import edge_tts  # noqa: F401
            flush_print(f"[TTS] ✅ edge-tts package ready (v{edge_tts.__version__})")
        except ImportError:
            flush_print(f"[TTS] ❌ edge-tts not installed! Run: pip install edge-tts")
            sys.exit(1)
        _tts_loaded = True
        return

    if _tts_mode == "http":
        # Verify HTTP server is reachable
        flush_print(f"\n[TTS] HTTP mode — checking server at {_tts_http_url}...")
        try:
            req = Request(f"{_tts_http_url}/health")
            resp = urlopen(req, timeout=10)
            data = json.loads(resp.read().decode())
            if data.get("model_loaded"):
                flush_print(f"[TTS] ✅ Server ready (uptime: {data.get('uptime_seconds', '?')}s)")
            else:
                flush_print(f"[TTS] ⚠️  Server responding but model not loaded yet")
                flush_print(f"[TTS] Wait for model to finish loading, then retry.")
                sys.exit(1)
        except (URLError, OSError) as e:
            flush_print(f"[TTS] ❌ Cannot reach TTS server at {_tts_http_url}")
            flush_print(f"[TTS]    Error: {e}")
            flush_print(f"[TTS]    Start the server first: python scripts/tts_server.py")
            sys.exit(1)
        _tts_loaded = True
        return

    # Direct mode: load Qwen3-TTS model into memory
    try:
        import tts_server
    except ImportError:
        flush_print(f"[TTS] ❌ tts_server module not found")
        flush_print(f"[TTS] Install Qwen3-TTS dependencies: pip install mlx-llm")
        sys.exit(1)

    flush_print(f"\n[TTS] Direct mode — loading Qwen3-TTS model into memory...")
    start = time.time()
    tts_server._model = tts_server.load_mlx_model(tts_server.DEFAULT_MODEL_ID)
    elapsed = time.time() - start
    flush_print(f"[TTS] Model loaded in {elapsed:.1f}s (sample rate: {tts_server._model.sample_rate})")

    # Warmup: first inference compiles Metal shaders
    flush_print(f"[TTS] Warming up model (compiling Metal shaders)...")
    warmup_start = time.time()
    try:
        tts_server._synthesize_one(text="你好", voice="Chelsie", lang_code="zh", speed=1.0, temperature=0.3)
        warmup_elapsed = time.time() - warmup_start
        flush_print(f"[TTS] Warmup complete in {warmup_elapsed:.1f}s")
    except Exception as e:
        flush_print(f"[TTS] Warmup failed (non-fatal): {e}")

    _tts_loaded = True
    flush_print(f"[TTS] ✅ Model ready!")


def generate_tts(slide_num: int, text: str, temperature: float = BASE_TEMPERATURE) -> dict:
    """
    Generate TTS audio for a slide.
    Routes to Edge TTS (default), direct model call, or HTTP request based on current mode.
    Returns: {"duration_seconds": ..., "inference_seconds": ..., "file": ...}
    """
    if _tts_mode == "edge":
        return _generate_tts_edge(slide_num, text)
    if _tts_mode == "http":
        return _generate_tts_http(slide_num, text, temperature)
    return _generate_tts_direct(slide_num, text, temperature)


def _generate_tts_edge(slide_num: int, text: str) -> dict:
    """Generate TTS using Microsoft Edge TTS (free online API)."""
    import edge_tts

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    # Edge TTS outputs mp3 by default; we save as mp3 then convert to wav
    out_path = AUDIO_DIR / f"slide_{slide_num:02d}.wav"
    tmp_mp3 = AUDIO_DIR / f"slide_{slide_num:02d}.tmp.mp3"

    start = time.time()

    async def _run():
        communicate = edge_tts.Communicate(
            text=text,
            voice=EDGE_TTS_VOICE,
            rate=EDGE_TTS_RATE,
            volume=EDGE_TTS_VOLUME,
        )
        await communicate.save(str(tmp_mp3))

    # Run async edge-tts in sync context
    asyncio.run(_run())

    # Convert mp3 → wav (24kHz mono, matching Qwen TTS output format)
    cmd = [
        "ffmpeg", "-y", "-i", str(tmp_mp3),
        "-ar", "24000", "-ac", "1",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg mp3→wav conversion failed: {result.stderr[:200]}")

    # Cleanup tmp mp3
    tmp_mp3.unlink(missing_ok=True)

    elapsed = time.time() - start

    # Read duration from wav
    with wave.open(str(out_path), "r") as wf:
        duration = wf.getnframes() / wf.getframerate()

    return {
        "duration_seconds": round(duration, 2),
        "inference_seconds": round(elapsed, 2),
        "file": str(out_path),
    }


def _generate_tts_direct(slide_num: int, text: str, temperature: float) -> dict:
    """Generate TTS by directly calling the in-memory Qwen3-TTS model."""
    import tts_server

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIO_DIR / f"slide_{slide_num:02d}.wav"

    start = time.time()
    audio, sr = tts_server.synthesize_speech(
        text=text,
        voice=VOICE_NAME,
        lang_code=LANG_CODE,
        speed=SPEECH_SPEED,
        temperature=temperature,
    )
    elapsed = time.time() - start

    import soundfile as sf
    sf.write(str(out_path), audio, sr)
    duration = len(audio) / sr

    return {
        "duration_seconds": round(duration, 2),
        "inference_seconds": round(elapsed, 2),
        "file": str(out_path),
    }


def _generate_tts_http(slide_num: int, text: str, temperature: float) -> dict:
    """Generate TTS by calling the HTTP server."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIO_DIR / f"slide_{slide_num:02d}.wav"

    payload = json.dumps({
        "text": text,
        "voice": VOICE_NAME,
        "lang_code": LANG_CODE,
        "speed": SPEECH_SPEED,
        "temperature": temperature,
    }).encode("utf-8")

    req = Request(
        f"{_tts_http_url}/tts",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    start = time.time()
    try:
        resp = urlopen(req, timeout=300)  # 5min timeout for long texts
    except (URLError, OSError) as e:
        raise RuntimeError(f"HTTP TTS request failed: {e}")

    elapsed = time.time() - start

    # Save response WAV data to file
    wav_data = resp.read()
    with open(out_path, "wb") as f:
        f.write(wav_data)

    # Read duration from saved file
    with wave.open(str(out_path), "r") as wf:
        duration = wf.getnframes() / wf.getframerate()

    return {
        "duration_seconds": round(duration, 2),
        "inference_seconds": round(elapsed, 2),
        "file": str(out_path),
    }


# ============================================================
# STT (Speech-to-Text) for validation
# ============================================================

_stt_model = None


def load_stt_model():
    """Load STT model (cached after first call)."""
    global _stt_model
    if _stt_model is not None:
        return _stt_model

    flush_print(f"\n[STT] Loading SenseVoiceSmall model...")
    start = time.time()

    from mlx_audio.stt.utils import load_model
    _stt_model = load_model(STT_MODEL_ID)

    elapsed = time.time() - start
    flush_print(f"[STT] Model loaded in {elapsed:.1f}s")
    return _stt_model


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file to text using SenseVoiceSmall."""
    model = load_stt_model()
    from mlx_audio.stt.utils import load_audio, SAMPLE_RATE
    audio = load_audio(audio_path, SAMPLE_RATE)
    result = model.generate(audio, language="zh")
    return result.text


def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds."""
    with wave.open(audio_path, "r") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / rate


# ============================================================
# Stage 1: Generate & validate audio for each slide (big loop)
# ============================================================

def stage1_generate_and_validate_audio(
    slides: dict,
    slide_nums: list[int],
    threshold: float = DEFAULT_THRESHOLD,
    max_retries: int = DEFAULT_MAX_RETRIES,
    force: bool = False,
    skip_validation: bool = False,
) -> bool:
    """
    Stage 1: Big loop — for each slide, generate audio then immediately validate.

    For each slide:
      1. Generate TTS audio (or use existing if not forced)
      2. Immediately validate via STT: audio→text similarity >= threshold
      3. If validation fails → regenerate and retry (small loop, up to max_retries)
      4. If all retries exhausted → ABORT entire pipeline

    Returns: True if all slides passed, False if any failed.
    """
    flush_print(f"\n{'='*60}")
    flush_print(f"  Stage 1: Generate & Validate Audio (per-slide)")
    flush_print(f"{'='*60}")
    flush_print(f"  Voice:        {VOICE_NAME}")
    flush_print(f"  Speed:        {SPEECH_SPEED}")
    flush_print(f"  Temperature:  {BASE_TEMPERATURE}")
    flush_print(f"  Threshold:    {threshold:.0%}")
    flush_print(f"  Max retries:  {max_retries}")
    flush_print(f"  Slides:       {slide_nums}")
    flush_print(f"  Force regen:  {'Yes' if force else 'No'}")
    flush_print(f"  Validation:   {'Skip' if skip_validation else 'Enabled'}")
    flush_print(f"{'='*60}\n")

    # Load TTS model (once, stays in memory for all slides)
    load_tts_model()
    
    # Pre-load STT model once (unless skipping validation)
    if not skip_validation:
        load_stt_model()

    validation_results = {}
    all_passed = True

    for slide_num in slide_nums:
        info = slides[slide_num]
        original_text = info["text"]
        audio_path = AUDIO_DIR / f"slide_{slide_num:02d}.wav"
        
        flush_print(f"\n  {'─'*55}")
        flush_print(f"  Slide {slide_num}: {info['title']}")
        flush_print(f"  {'─'*55}")
        
        passed = False
        force_regen = force
        validation_result = {}
        
        for attempt in range(1, max_retries + 1):
            temperature = BASE_TEMPERATURE + (attempt - 1) * 0.05
            
            try:
                # Step A: Generate audio
                need_generate = force_regen or not audio_path.exists()
                
                # On first attempt, check if existing audio is readable
                if not need_generate:
                    try:
                        dur = get_audio_duration(str(audio_path))
                        flush_print(f"    📁 Existing audio found ({dur:.1f}s)")
                    except Exception:
                        flush_print(f"    ⚠️  Existing audio unreadable, regenerating")
                        need_generate = True
                
                if need_generate:
                    flush_print(f"    🔊 Generating audio (temp={temperature:.2f})...", end="")
                    try:
                        result = generate_tts(slide_num, original_text, temperature=temperature)
                        dur = result.get("duration_seconds", 0)
                        inf_time = result.get("inference_seconds", 0)
                        flush_print(f" ✅ {dur:.1f}s (inference: {inf_time:.1f}s)")
                    except Exception as e:
                        flush_print(f" ❌ TTS failed: {e}")
                        raise
                
                # Step B: Skip validation if requested
                if skip_validation:
                    audio_dur = result.get("duration_seconds", 0) if need_generate else get_audio_duration(str(audio_path))
                    flush_print(f"    ⏭️  Validation skipped, audio accepted ({audio_dur:.1f}s)")
                    passed = True
                    validation_result = {
                        "similarity": None,
                        "coverage": None,
                        "duration": audio_dur,
                        "attempts": attempt,
                        "skipped_validation": True,
                    }
                    break
                
                # Step C: Validate audio quality
                # Read audio duration
                try:
                    audio_dur = get_audio_duration(str(audio_path))
                except Exception as e:
                    flush_print(f"    ❌ Cannot read audio: {e}")
                    raise
                
                # Transcribe
                flush_print(f"    🎙️  Validating: transcribing ({audio_dur:.1f}s audio)...", end="")
                start = time.time()
                try:
                    transcription = transcribe_audio(str(audio_path))
                except Exception as e:
                    flush_print(f" ❌ STT error: {e}")
                    raise
                stt_time = time.time() - start
                flush_print(f" done ({stt_time:.1f}s)")
                
                # Compute similarity
                similarity = compute_similarity(original_text, transcription)
                coverage = compute_char_coverage(original_text, transcription)
                
                # Check duration sanity
                text_len = len(original_text)
                expected_dur = text_len / CHARS_PER_SEC
                min_dur = expected_dur / DURATION_TOLERANCE
                max_dur = expected_dur * DURATION_TOLERANCE
                duration_ok = min_dur <= audio_dur <= max_dur
                
                # Report
                sim_icon = "✅" if similarity >= threshold else "❌"
                dur_icon = "✅" if duration_ok else "❌"
                flush_print(f"    📊 Similarity:  {similarity:.1%} {sim_icon} (threshold: {threshold:.0%})")
                flush_print(f"    📊 Coverage:    {coverage:.1%}")
                flush_print(f"    📊 Duration:    {audio_dur:.1f}s (expected: ~{expected_dur:.0f}s) {dur_icon}")
                flush_print(f"    📊 STT output:  {transcription[:80]}...")
                
                if similarity >= threshold and duration_ok:
                    flush_print(f"    🎉 PASSED! (attempt {attempt})")
                    passed = True
                    validation_result = {
                        "similarity": similarity,
                        "coverage": coverage,
                        "duration": audio_dur,
                        "attempts": attempt,
                    }
                    break
                else:
                    reasons = []
                    if similarity < threshold:
                        reasons.append(f"similarity {similarity:.1%} < {threshold:.0%}")
                    if not duration_ok:
                        reasons.append(f"duration {audio_dur:.1f}s out of range")
                    flush_print(f"    ⚠️  FAILED: {', '.join(reasons)}")
                    
                    if attempt < max_retries:
                        flush_print(f"    🔄 Will regenerate and retry (attempt {attempt+1}/{max_retries})...")
                        time.sleep(1)
                        force_regen = True
                        
            except Exception as e:
                if attempt < max_retries:
                    flush_print(f"    ⏳ Waiting 2s before retry...")
                    time.sleep(2)
                    force_regen = True
                    continue
                else:
                    flush_print(f"    💀 All {max_retries} attempts exhausted!")
                    break
        
        if passed:
            validation_results[slide_num] = validation_result
        else:
            flush_print(f"\n    💀 Slide {slide_num} FAILED after {max_retries} attempts!")
            flush_print(f"    🛑 ABORTING PIPELINE — fix this slide before continuing.")
            all_passed = False
            break

    # ---- Stage 1 Summary ----
    flush_print(f"\n  {'='*55}")
    flush_print(f"  Stage 1 Summary: Audio Generation & Validation")
    flush_print(f"  {'='*55}")
    for num in slide_nums:
        if num in validation_results:
            r = validation_results[num]
            if r.get("skipped_validation"):
                flush_print(f"    Slide {num:2d}: ⏭️  audio ok (validation skipped), {r['duration']:.1f}s")
            else:
                flush_print(f"    Slide {num:2d}: ✅ PASSED (sim={r['similarity']:.1%}, attempts={r['attempts']}, {r['duration']:.1f}s)")
        elif not all_passed and num == slide_num:
            flush_print(f"    Slide {num:2d}: ❌ FAILED")
        elif num not in validation_results:
            flush_print(f"    Slide {num:2d}: ⏭️  not reached")
    flush_print(f"  {'='*55}")

    return all_passed


# ============================================================
# Stage 2: Generate video for each slide
# ============================================================

def stage2_generate_videos(slides: dict, slide_nums: list[int],
                           fast: bool = False) -> bool:
    """
    Stage 2: Generate video for each individual slide.
    Each video = image + audio + subtitle.

    Returns: True if all succeeded, False otherwise.
    """
    flush_print(f"\n{'='*60}")
    flush_print(f"  Stage 2: Generate Video for Each Slide")
    flush_print(f"{'='*60}")
    flush_print(f"  Mode:    {'⚡ FAST' if fast else 'HQ'}")
    flush_print(f"  Slides:  {slide_nums}")
    flush_print(f"{'='*60}\n")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    all_ok = True
    for slide_num in slide_nums:
        info = slides[slide_num]
        image_path = IMAGES_DIR / f"slide_{slide_num:02d}.png"
        audio_path = AUDIO_DIR / f"slide_{slide_num:02d}.wav"
        video_path = VIDEO_DIR / f"slide_{slide_num:02d}.mp4"

        # Verify inputs exist
        if not image_path.exists():
            flush_print(f"  ❌ Slide {slide_num}: image not found: {image_path}")
            all_ok = False
            break
        if not audio_path.exists():
            flush_print(f"  ❌ Slide {slide_num}: audio not found: {audio_path}")
            all_ok = False
            break

        flush_print(f"  🎬 Slide {slide_num:2d} | {info['title'][:30]:30s} | composing...", end="")
        start = time.time()

        try:
            # Use slide_to_video.py for single slide
            cmd = [
                sys.executable,
                str(SCRIPTS_DIR / "slide_to_video.py"),
                "--slide", str(slide_num),
                "--output", str(video_path),
            ]
            if fast:
                cmd.append("--fast")

            result = subprocess.run(
                cmd,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                flush_print(f" ❌ failed!")
                flush_print(f"    stderr: {result.stderr[-300:]}")
                all_ok = False
                break

            elapsed = time.time() - start
            if video_path.exists():
                size_mb = video_path.stat().st_size / (1024 * 1024)
                # Get duration
                try:
                    dur = get_video_duration(str(video_path))
                    flush_print(f" ✅ {dur:.1f}s, {size_mb:.2f}MB ({elapsed:.1f}s)")
                except Exception:
                    flush_print(f" ✅ {size_mb:.2f}MB ({elapsed:.1f}s)")
            else:
                flush_print(f" ❌ output file not created!")
                all_ok = False
                break

        except Exception as e:
            flush_print(f" ❌ error: {e}")
            all_ok = False
            break

    if all_ok:
        flush_print(f"\n  ✅ Stage 2 complete: {len(slide_nums)} videos generated")
    else:
        flush_print(f"\n  ❌ Stage 2 failed!")

    return all_ok


def get_video_duration(video_path: str) -> float:
    """Get video duration via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet",
         "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1",
         video_path],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return float(result.stdout.strip())
    return 0.0


# ============================================================
# Stage 3: Merge all videos into final output
# ============================================================

def stage3_merge_videos(slide_nums: list[int], fast: bool = False) -> bool:
    """
    Stage 3: Merge all individual slide videos into final output.

    Returns: True if succeeded.
    """
    flush_print(f"\n{'='*60}")
    flush_print(f"  Stage 3: Merge All Videos into Final Output")
    flush_print(f"{'='*60}")
    flush_print(f"  Slides:  {slide_nums}")
    flush_print(f"{'='*60}\n")

    # Verify all slide videos exist
    missing = []
    for num in slide_nums:
        video_path = VIDEO_DIR / f"slide_{num:02d}.mp4"
        if not video_path.exists():
            missing.append(num)
    if missing:
        flush_print(f"  ❌ Missing slide videos: {missing}")
        return False

    # Determine output path
    if len(slide_nums) == 1:
        flush_print(f"  ℹ️  Only 1 slide, no merge needed.")
        return True

    slides_arg = ",".join(str(n) for n in slide_nums)
    output_path = VIDEO_DIR / "final.mp4"

    flush_print(f"  🔗 Merging {len(slide_nums)} videos...")
    start = time.time()

    # Use FFmpeg concat demuxer for efficient merging
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for n in slide_nums:
            video_path = VIDEO_DIR / f"slide_{n:02d}.mp4"
            f.write(f"file '{video_path.resolve()}\n")
        filelist = f.name

    try:
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", filelist,
               "-c", "copy", "-avoid_negative_ts", "make_zero",
               "-movflags", "+faststart", str(output_path)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            flush_print(f"  ❌ Concat failed: {r.stderr[-300:]}")
            return False
    finally:
        Path(filelist).unlink(missing_ok=True)

    elapsed = time.time() - start

    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        try:
            dur = get_video_duration(str(output_path))
            minutes = int(dur) // 60
            secs = dur - minutes * 60
            dur_str = f"{minutes}m {secs:.1f}s" if minutes else f"{secs:.1f}s"
        except Exception:
            dur_str = "unknown"

        flush_print(f"\n  {'='*55}")
        flush_print(f"  ✅ Final video created!")
        flush_print(f"  📹 Output:   {output_path}")
        flush_print(f"  📏 Size:     {size_mb:.2f} MB")
        flush_print(f"  ⏱️  Duration: {dur_str}")
        flush_print(f"  🕐 Merge:    {format_duration(elapsed)}")
        flush_print(f"  {'='*55}")
    else:
        flush_print(f"  ❌ Output file not created!")
        return False

    return True


# ============================================================
# Main: 3-stage pipeline
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="End-to-end pipeline: TTS audio generation → validation → video → merge"
    )
    parser.add_argument(
        "--slides", type=str, default=None,
        help="Slide range (e.g., 1-3 or 1,3,5). Default: all slides.",
    )
    parser.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help=f"Minimum similarity for validation (default: {DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--max-retries", type=int, default=DEFAULT_MAX_RETRIES,
        help=f"Max retries per slide in validation (default: {DEFAULT_MAX_RETRIES})",
    )
    parser.add_argument(
        "--force-audio", action="store_true",
        help="Force regenerate all audio (ignore existing files)",
    )
    parser.add_argument(
        "--skip-images", action="store_true",
        help="Skip image generation (use existing images)",
    )
    parser.add_argument(
        "--skip-validation", action="store_true",
        help="Skip Stage 2 audio validation (use existing audio as-is)",
    )
    parser.add_argument(
        "--fast", action="store_true",
        help="Fast preview mode (lower quality, quicker encoding)",
    )
    parser.add_argument(
        "--use-pptx", action="store_true",
        help="Use PPTX file instead of PDF (if both exist)",
    )
    parser.add_argument(
        "--tts-direct", action="store_true",
        help="Use Qwen3-TTS direct model loading (requires local GPU model)",
    )
    parser.add_argument(
        "--tts-http", action="store_true",
        help="Use HTTP TTS server instead of direct model loading",
    )
    parser.add_argument(
        "--tts-url", type=str, default=DEFAULT_TTS_URL,
        help=f"TTS HTTP server URL (default: {DEFAULT_TTS_URL})",
    )
    parser.add_argument(
        "--tts-edge", action="store_true",
        help="Use Microsoft Edge TTS (free online API, no local model needed)",
    )
    parser.add_argument(
        "--edge-voice", type=str, default=None,
        help=f"Edge TTS voice name (default from config: {EDGE_TTS_VOICE})",
    )
    parser.add_argument(
        "--edge-rate", type=str, default=None,
        help="Edge TTS rate, e.g. '+20%%' or '-10%%' (default from config: %(default)s)",
    )
    args = parser.parse_args()

    # Configure TTS mode (edge > direct > http)
    if args.tts_edge:
        # Override edge-tts settings from CLI if provided
        _override_edge_settings(args.edge_voice, args.edge_rate)
        set_tts_mode("edge")
    elif args.tts_direct:
        set_tts_mode("direct")
    elif args.tts_http:
        set_tts_mode("http", args.tts_url)
    else:
        # Default: Edge TTS (no local model needed)
        set_tts_mode("edge")

    pipeline_start = time.time()
    timings = {}

    # ---- Parse script.md ----
    if not SCRIPT_JSON.exists():
        flush_print(f"[ERROR] JSON subtitles not found: {SCRIPT_JSON}")
        sys.exit(1)

    all_slides = parse_json_subtitles()
    if not all_slides:
        flush_print("[ERROR] No speaker notes found in subtitles.json")
        sys.exit(1)

    # Determine which slides to process
    if args.slides:
        slide_nums = parse_slide_range(args.slides)
    else:
        slide_nums = sorted(all_slides.keys())

    # Validate requested slides exist in script
    missing = [n for n in slide_nums if n not in all_slides]
    if missing:
        flush_print(f"[ERROR] Slides not found in subtitles.json: {missing}")
        flush_print(f"[INFO] Available: {sorted(all_slides.keys())}")
        sys.exit(1)

    # ---- Banner ----
    flush_print(f"\n{'='*60}")
    flush_print(f"  🚀 Pipeline: Text → Audio → Video")
    flush_print(f"{'='*60}")
    flush_print(f"  Slides:       {slide_nums} ({len(slide_nums)} pages)")
    flush_print(f"  Voice:        {VOICE_NAME}")
    flush_print(f"  Speed:        {SPEECH_SPEED}")
    flush_print(f"  Threshold:    {args.threshold:.0%}")
    flush_print(f"  Max retries:  {args.max_retries}")
    flush_print(f"  Force audio:  {'Yes' if args.force_audio else 'No'}")
    flush_print(f"  Fast mode:    {'Yes' if args.fast else 'No'}")
    if args.tts_direct:
        tts_mode_str = "Direct (Qwen3-TTS in-memory)"
    elif args.tts_edge:
        tts_mode_str = f"Edge TTS ({EDGE_TTS_VOICE}, rate={EDGE_TTS_RATE})"
    elif args.tts_http:
        tts_mode_str = f"HTTP ({args.tts_url})"
    else:
        tts_mode_str = f"Edge TTS ({EDGE_TTS_VOICE}, rate={EDGE_TTS_RATE}) (default)"
    flush_print(f"  TTS mode:     {tts_mode_str}")
    flush_print(f"  Started:      {time.strftime('%Y-%m-%d %H:%M:%S')}")
    flush_print(f"{'='*60}")

    # ---- Pre-flight checks ----
    flush_print(f"\n[INFO] Pre-flight checks...")

    # Check source file (PDF or PPTX) / images
    if not args.skip_images:
        has_pdf = PDF_PATH.exists()
        has_pptx = PPTX_PATH.exists()
        
        if not has_pdf and not has_pptx:
            flush_print(f"[ERROR] No source file found:")
            flush_print(f"  - PDF:  {PDF_PATH}")
            flush_print(f"  - PPTX: {PPTX_PATH}")
            sys.exit(1)
        
        if has_pdf and has_pptx:
            if args.use_pptx:
                flush_print(f"  Source:       ✅ PPTX (explicitly selected)")
                flush_print(f"  PPTX:         {PPTX_PATH}")
            else:
                flush_print(f"  Source:       ✅ PDF (default) + PPTX (available)")
                flush_print(f"  PDF:          {PDF_PATH}")
        elif has_pdf:
            flush_print(f"  Source:       ✅ PDF")
            flush_print(f"  PDF:          {PDF_PATH}")
        else:
            flush_print(f"  Source:       ✅ PPTX")
            flush_print(f"  PPTX:         {PPTX_PATH}")
    else:
        image_count = len(list(IMAGES_DIR.glob("slide_*.png"))) if IMAGES_DIR.exists() else 0
        flush_print(f"  Images:       ✅ {image_count} existing (skipping generation)")
        if image_count == 0:
            flush_print(f"[WARN] No images found — video assembly will be skipped")

    if args.tts_edge:
        flush_print(f"  TTS engine:   ✅ Edge TTS (online, no local model)")
    elif args.tts_http:
        flush_print(f"  TTS server:   ✅ HTTP mode ({args.tts_url})")
    else:
        flush_print(f"  TTS model:    will load at Stage 1 start")

    # ---- Step 0: Source → Images (if needed) ----
    if not args.skip_images:
        has_pdf = PDF_PATH.exists()
        has_pptx = PPTX_PATH.exists()
        
        # Determine which source to use
        use_pptx = args.use_pptx or not has_pdf
        
        if has_pdf and not use_pptx:
            # Use PDF if available and not explicitly requesting PPTX
            flush_print(f"\n[INFO] Converting PDF → images...")
            start = time.time()
            cmd = [sys.executable, str(SCRIPTS_DIR / "pdf_to_images.py")]
            if args.fast:
                cmd.append("--fast")
            result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
            if result.returncode != 0:
                flush_print("[ERROR] PDF → images failed!")
                sys.exit(1)
            timings["PDF → Images"] = time.time() - start
            flush_print(f"  ⏱️  PDF → Images: {format_duration(timings['PDF → Images'])}")
        elif use_pptx and has_pptx:
            # Use PPTX if explicitly requested or PDF not available
            flush_print(f"\n[INFO] Converting PPTX → images...")
            start = time.time()
            cmd = [sys.executable, str(SCRIPTS_DIR / "pptx_to_images.py")]
            if args.fast:
                cmd.append("--fast")
            result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
            if result.returncode != 0:
                # If failed, try fallback mode
                flush_print("[WARN] LibreOffice conversion failed, trying fallback mode...")
                cmd.append("--fallback")
                result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
                if result.returncode != 0:
                    flush_print("[ERROR] PPTX → images failed!")
                    sys.exit(1)
            timings["PPTX → Images"] = time.time() - start
            flush_print(f"  ⏱️  PPTX → Images: {format_duration(timings['PPTX → Images'])}")
        else:
            flush_print("[ERROR] No source file available for image generation!")
            sys.exit(1)

    # Verify images exist for requested slides
    for num in slide_nums:
        img = IMAGES_DIR / f"slide_{num:02d}.png"
        if not img.exists():
            flush_print(f"[ERROR] Image not found for slide {num}: {img}")
            sys.exit(1)

    # ============================================================
    # Stage 1: Generate & validate audio (big loop, per-slide)
    # ============================================================
    start = time.time()
    stage1_ok = stage1_generate_and_validate_audio(
        all_slides, slide_nums,
        threshold=args.threshold,
        max_retries=args.max_retries,
        force=args.force_audio,
        skip_validation=args.skip_validation,
    )
    timings["Stage 1: Audio Gen+Val"] = time.time() - start

    if not stage1_ok:
        flush_print(f"\n{'='*60}")
        flush_print(f"  🛑 PIPELINE ABORTED — Audio generation/validation failed!")
        flush_print(f"{'='*60}")
        flush_print(f"  [HINT] Try increasing --max-retries or lowering --threshold")
        flush_print(f"  [HINT] Or check TTS server for issues")
        sys.exit(1)

    # ============================================================
    # Stage 2: Generate each slide's video
    # ============================================================
    image_count = len(list(IMAGES_DIR.glob("slide_*.png"))) if IMAGES_DIR.exists() else 0
    if image_count == 0:
        flush_print(f"\n[INFO] No slide images found — skipping Stage 2 (video gen) & Stage 3 (merge)")
        timings["Stage 2: Video Gen"] = 0
        timings["Stage 3: Merge"] = 0
    else:
        start = time.time()
        stage2_ok = stage2_generate_videos(all_slides, slide_nums, fast=args.fast)
        timings["Stage 2: Video Gen"] = time.time() - start

        if not stage2_ok:
            flush_print(f"\n[ERROR] Stage 2 failed! Cannot proceed to merge.")
            sys.exit(1)

        # ============================================================
        # Stage 3: Merge all videos
        # ============================================================
        start = time.time()
        stage3_ok = stage3_merge_videos(slide_nums, fast=args.fast)
        timings["Stage 3: Merge"] = time.time() - start

        if not stage3_ok:
            flush_print(f"\n[ERROR] Stage 3 merge failed!")
            sys.exit(1)

    # ============================================================
    # Final report
    # ============================================================
    pipeline_elapsed = time.time() - pipeline_start

    flush_print(f"\n{'='*60}")
    flush_print(f"  🎉 Pipeline Complete!")
    flush_print(f"{'='*60}")
    flush_print(f"  Finished: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    flush_print()
    flush_print(f"  {'Step':<30s} {'Time':>12s}")
    flush_print(f"  {'─'*30} {'─'*12}")
    for name, elapsed in timings.items():
        flush_print(f"  {name:<30s} {format_duration(elapsed):>12s}")
    flush_print(f"  {'─'*30} {'─'*12}")
    flush_print(f"  {'Total Pipeline':<30s} {format_duration(pipeline_elapsed):>12s}")
    flush_print()

    final_video = VIDEO_DIR / "final.mp4"

    if final_video.exists():
        size_mb = final_video.stat().st_size / (1024 * 1024)
        flush_print(f"  📹 Final video: {final_video}")
        flush_print(f"     Size: {size_mb:.2f} MB")
        try:
            dur = get_video_duration(str(final_video))
            flush_print(f"     Duration: {format_duration(dur)}")
        except Exception:
            pass

    flush_print(f"\n  ✅ Done!\n")


if __name__ == "__main__":
    main()