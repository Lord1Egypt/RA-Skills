#!/usr/bin/env python3
"""
Qwen3-TTS HTTP Server (MLX version) — Model stays loaded in memory.

Uses mlx-audio for native Apple Silicon GPU acceleration.
Start once, use forever. No need to reload the model each time.

Usage:
    conda activate d2l_3.13
    python scripts/tts_server.py

    # Background (keeps running after terminal closes):
    nohup python scripts/tts_server.py > tts_server.log 2>&1 &

API endpoints:
    POST /tts          — Synthesize speech from text, returns WAV audio
    POST /tts/slides   — Synthesize all slides from script.md
    GET  /health       — Health check (model loaded?)
    GET  /info         — Model info and stats

Prerequisites:
    pip install -U mlx-audio soundfile numpy fastapi uvicorn python-multipart
"""

import io
import re
import time
import argparse
from pathlib import Path
from contextlib import asynccontextmanager

import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field

from utils import (
    PROJECT_ROOT, SCRIPT_MD, AUDIO_DIR as OUTPUT_DIR,
    load_config, parse_script,
    get_tts_config, get_config_section
)


# ---- Load config defaults using new helper functions ----
_tts_cfg = get_tts_config()

DEFAULT_VOICE = _tts_cfg.get("voice_name", "Chelsie")
DEFAULT_LANG_CODE = _tts_cfg.get("lang_code", "zh")
DEFAULT_TEMPERATURE = _tts_cfg.get("base_temperature", 0.3)
DEFAULT_SPEED = _tts_cfg.get("speech_speed", 1.0)

# ---- Other settings ----
DEFAULT_MODEL_ID = "mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-bf16"

# ---- Global state ----
_model = None
_request_count = 0
_start_time = None


# ---- Model loading ----

def load_mlx_model(model_id: str):
    """Load Qwen3-TTS model using mlx-audio library."""
    from mlx_audio.tts.utils import load_model

    print(f"[INFO] Loading MLX model: {model_id}")
    model = load_model(model_path=model_id)
    print(f"[INFO] Model loaded successfully! Sample rate: {model.sample_rate}")
    return model


def split_sentences(text: str) -> list[str]:
    """
    Split Chinese text into sentences for per-sentence TTS synthesis.

    Strategy:
      1. Split at sentence-ending punctuation: 。！？!?
      2. Keep the punctuation attached to the preceding sentence.
      3. Filter out empty strings.

    This ensures each TTS call receives a short, manageable chunk,
    which improves both speed and audio quality.
    """
    parts = re.split(r'([。！？!?])', text)
    sentences = []
    buf = ""
    for p in parts:
        buf += p
        if re.match(r'[。！？!?]', p):
            s = buf.strip()
            if s:
                sentences.append(s)
            buf = ""
    # Leftover text without ending punctuation
    if buf.strip():
        sentences.append(buf.strip())
    return sentences


# ---- Max tokens estimation ----
# Qwen3-TTS at 12Hz: 1 second of audio ≈ 12 tokens.
# Chinese speech averages ~0.3s per character → ~3.6 tokens/char.
# We use a modest 1.1x headroom.  Previous 3x headroom caused the
# model to hallucinate garbage audio far beyond the actual speech.
_TOKENS_PER_CHAR = 4        # ~3.6 * 1.1 headroom
_MIN_MAX_TOKENS  = 180      # floor ≈ 15 seconds
_MAX_MAX_TOKENS  = 2400     # hard ceiling (~200 seconds max)
_AUDIO_HZ        = 12       # model codec frame-rate


def _estimate_max_tokens(text: str) -> int:
    """Estimate a safe max_tokens limit based on text length."""
    estimated = len(text) * _TOKENS_PER_CHAR
    return max(_MIN_MAX_TOKENS, min(estimated, _MAX_MAX_TOKENS))


def _synthesize_one(
    text: str,
    voice: str = None,
    lang_code: str = None,
    speed: float = None,
    temperature: float = None,
    ref_audio_path: str | None = None,
    ref_text: str | None = None,
) -> np.ndarray:
    """
    Synthesize a single (short) text segment.
    Returns raw audio numpy array.

    Applies a dynamic max_tokens limit based on text length to prevent
    the model from generating excessively long audio ("hallucination").
    """
    import mlx.core as mx
    from mlx_audio.utils import load_audio

    global _model

    # Apply config defaults for any unset parameters
    if voice is None:
        voice = DEFAULT_VOICE
    if lang_code is None:
        lang_code = DEFAULT_LANG_CODE
    if speed is None:
        speed = DEFAULT_SPEED
    if temperature is None:
        temperature = DEFAULT_TEMPERATURE

    max_tokens = _estimate_max_tokens(text)
    expected_max_sec = max_tokens / _AUDIO_HZ
    print(f"[TTS] text={len(text)} chars, max_tokens={max_tokens} (~{expected_max_sec:.0f}s cap)")

    gen_kwargs = dict(
        text=text,
        voice=voice,
        speed=speed,
        lang_code=lang_code,
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=False,
        stream=False,
    )

    # Load reference audio if provided
    if ref_audio_path:
        ref_audio = load_audio(
            ref_audio_path, sample_rate=_model.sample_rate, volume_normalize=False
        )
        gen_kwargs["ref_audio"] = ref_audio
        if ref_text:
            gen_kwargs["ref_text"] = ref_text

    results = _model.generate(**gen_kwargs)

    audio_segments = []
    for result in results:
        audio_data = result.audio
        if isinstance(audio_data, mx.array):
            audio_data = np.array(audio_data)
        audio_segments.append(audio_data)

    if not audio_segments:
        raise RuntimeError(f"No audio generated for: {text[:30]}")

    if len(audio_segments) == 1:
        audio = audio_segments[0].squeeze()
    else:
        audio = np.concatenate(audio_segments, axis=0).squeeze()

    # Sanity check: warn if generated audio is suspiciously long
    actual_sec = len(audio) / _model.sample_rate
    if actual_sec > expected_max_sec * 0.95:
        print(f"[WARN] Audio hit max_tokens cap: {actual_sec:.1f}s "
              f"(cap={expected_max_sec:.0f}s) for text: {text[:40]}")

    return audio


# Silence gap between sentences (150ms at 24kHz)
_SENTENCE_GAP_SEC = 0.15


def _trim_silence(
    audio: np.ndarray,
    sr: int,
    threshold: float = 0.005,
    min_silence_ms: int = 100,
    keep_leading_ms: int = 80,
    keep_trailing_ms: int = 150,
) -> np.ndarray:
    """
    Trim leading and trailing silence from audio.

    The TTS model often produces several seconds of silence at the
    beginning (and sometimes at the end). This function detects the
    first / last sample above *threshold* (relative to peak) and
    removes the surrounding silence while keeping a tiny natural
    buffer on each side.

    Args:
        audio: 1-D float numpy array.
        sr: sample rate.
        threshold: amplitude fraction of peak to consider "silence".
        min_silence_ms: ignore leading silence shorter than this (ms).
        keep_leading_ms: ms of silence to keep before first sound.
        keep_trailing_ms: ms of silence to keep after last sound.

    Returns:
        Trimmed audio numpy array.
    """
    if len(audio) == 0:
        return audio

    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio  # completely silent, nothing to trim

    abs_audio = np.abs(audio)
    cutoff = peak * threshold

    # Find first and last sample above the threshold
    nonsilent = np.where(abs_audio > cutoff)[0]
    if len(nonsilent) == 0:
        return audio

    first_sound = nonsilent[0]
    last_sound = nonsilent[-1]

    min_silence_samples = int(sr * min_silence_ms / 1000)
    keep_lead = int(sr * keep_leading_ms / 1000)
    keep_trail = int(sr * keep_trailing_ms / 1000)

    # Only trim leading silence if it's longer than min_silence_ms
    if first_sound > min_silence_samples:
        start = max(0, first_sound - keep_lead)
    else:
        start = 0

    end = min(len(audio), last_sound + keep_trail)

    trimmed_lead = first_sound / sr
    trimmed_trail = (len(audio) - last_sound) / sr
    if trimmed_lead > 0.1 or trimmed_trail > 0.1:
        print(f"[TRIM] Removed {trimmed_lead:.2f}s leading + "
              f"{trimmed_trail:.2f}s trailing silence")

    return audio[start:end]


def _trim_hallucination(
    audio: np.ndarray,
    sr: int,
    text_len: int,
    chars_per_second: float = 4.0,
    headroom: float = 2.0,
) -> np.ndarray:
    """
    Hard-trim audio that exceeds the expected duration based on text length.

    TTS hallucination often manifests as the model continuing to generate
    audio (not silence, but repetitive/garbled speech) far beyond the
    actual content.  This function enforces a hard ceiling based on the
    expected reading duration.

    Args:
        audio: 1-D float numpy array.
        sr: sample rate.
        text_len: number of characters in the source text.
        chars_per_second: expected Chinese reading speed (chars/sec).
        headroom: multiplier above expected duration before hard-trim.

    Returns:
        Possibly truncated audio.
    """
    expected_sec = text_len / chars_per_second
    max_sec = max(expected_sec * headroom, 5.0)  # at least 5 seconds
    max_samples = int(sr * max_sec)

    if len(audio) > max_samples:
        actual_sec = len(audio) / sr
        print(f"[TRIM-HALLUCINATION] Audio {actual_sec:.1f}s exceeds "
              f"expected {expected_sec:.1f}s × {headroom} = {max_sec:.1f}s cap. "
              f"Hard-trimming to {max_sec:.1f}s")
        audio = audio[:max_samples]
        # Apply a short fade-out (50ms) to avoid click
        fade_samples = int(sr * 0.05)
        if len(audio) > fade_samples:
            fade = np.linspace(1.0, 0.0, fade_samples, dtype=audio.dtype)
            audio[-fade_samples:] *= fade

    return audio

# Short text threshold: texts shorter than this will be synthesized
# as a single chunk (no sentence splitting) to avoid per-sentence overhead.
_SHORT_TEXT_THRESHOLD = 200


def synthesize_speech(
    text: str,
    voice: str = None,
    lang_code: str = None,
    speed: float = None,
    temperature: float = None,
    ref_audio_path: str | None = None,
    ref_text: str | None = None,
) -> tuple[np.ndarray, int]:
    """
    Generate speech audio from text using MLX Qwen3-TTS.

    Strategy:
      - Short texts (< 200 chars): synthesize as a single chunk for speed.
      - Long texts (>= 200 chars): split into sentences and synthesize each
        separately, then concatenate with short silence gaps.

    Returns:
        tuple: (audio_numpy_array, sample_rate)
    """
    global _model
    sr = _model.sample_rate

    # For short texts, synthesize as a single chunk to avoid
    # per-sentence overhead (tokenize, infer, decode for each sentence).
    if len(text) < _SHORT_TEXT_THRESHOLD:
        print(f"[TTS] Short text ({len(text)} chars), synthesizing as single chunk")
        audio = _synthesize_one(
            text=text, voice=voice, lang_code=lang_code,
            speed=speed, temperature=temperature,
            ref_audio_path=ref_audio_path, ref_text=ref_text,
        )
        audio = _trim_silence(audio, sr)
        audio = _trim_hallucination(audio, sr, len(text))
        return audio, sr

    sentences = split_sentences(text)
    gap_samples = int(sr * _SENTENCE_GAP_SEC)
    silence = np.zeros(gap_samples, dtype=np.float32)

    if len(sentences) <= 1:
        # Single sentence — synthesize directly
        audio = _synthesize_one(
            text=text, voice=voice, lang_code=lang_code,
            speed=speed, temperature=temperature,
            ref_audio_path=ref_audio_path, ref_text=ref_text,
        )
        return audio, sr

    # Multiple sentences — per-sentence synthesis
    print(f"[TTS] Long text ({len(text)} chars), splitting into {len(sentences)} sentences")
    all_parts = []
    for i, sent in enumerate(sentences):
        seg_start = time.time()
        audio_seg = _synthesize_one(
            text=sent, voice=voice, lang_code=lang_code,
            speed=speed, temperature=temperature,
            ref_audio_path=ref_audio_path, ref_text=ref_text,
        )
        # Per-sentence hallucination guard
        audio_seg = _trim_hallucination(audio_seg, sr, len(sent))
        seg_elapsed = time.time() - seg_start
        seg_dur = len(audio_seg) / sr
        print(f"  [{i+1}/{len(sentences)}] {sent[:25]:25s} | {seg_elapsed:.1f}s infer | {seg_dur:.1f}s audio")
        all_parts.append(audio_seg)
        # Add silence gap between sentences (not after the last one)
        if i < len(sentences) - 1:
            all_parts.append(silence)

    audio = np.concatenate(all_parts, axis=0)
    audio = _trim_silence(audio, sr)
    return audio, sr


def extract_speaker_notes(script_path: Path) -> list[dict]:
    """
    Extract speaker notes from script.md.
    Wraps utils.parse_script() to return list format for API compatibility.
    """
    slides_dict = parse_script(script_path)
    return [
        {"slide_num": num, "title": info["title"], "text": info["text"]}
        for num, info in sorted(slides_dict.items())
    ]


# ---- Pydantic models ----

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize")
    voice: str = Field(default=None, description="Voice/speaker name (e.g., Chelsie, Ethan, Vivian). Default from config.json")
    lang_code: str = Field(default=None, description="Language code: zh / en. Default from config.json")
    speed: float = Field(default=None, description="Playback speed multiplier. Default from config.json")
    temperature: float = Field(default=None, description="Generation temperature (lower = more stable quality). Default from config.json")
    ref_audio: str | None = Field(default=None, description="Reference audio path for voice cloning (optional)")
    ref_text: str | None = Field(default=None, description="Reference audio transcript (optional)")
    save_to_file: str | None = Field(default=None, description="If set, save WAV to this filename in output/audio/")


class SlidesTTSRequest(BaseModel):
    script_path: str = Field(default=str(SCRIPT_MD), description="Path to script.md")
    voice: str = Field(default=None, description="Voice/speaker name. Default from config.json")
    lang_code: str = Field(default=None, description="Language code for TTS. Default from config.json")
    speed: float = Field(default=None, description="Playback speed multiplier. Default from config.json")
    temperature: float = Field(default=None, description="Generation temperature (lower = more stable quality). Default from config.json")
    slides: list[int] | None = Field(default=None, description="Specific slide numbers (None = all)")
    ref_audio: str | None = Field(default=None, description="Reference audio path for voice cloning")


# ---- FastAPI app ----

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, cleanup on shutdown."""
    global _model, _start_time
    _start_time = time.time()

    model_id = app.state.model_id
    _model = load_mlx_model(model_id)

    # ---- Warmup: run a short inference to compile Metal shaders ----
    print(f"[INFO] Warming up model (first inference compiles Metal shaders)...")
    warmup_start = time.time()
    try:
        _synthesize_one(text="你好", voice="Chelsie", lang_code="zh", speed=1.0, temperature=0.3)
        warmup_elapsed = time.time() - warmup_start
        print(f"[INFO] Warmup complete in {warmup_elapsed:.1f}s (future inferences will be faster)")
    except Exception as e:
        print(f"[WARN] Warmup failed (non-fatal): {e}")

    print(f"\n{'='*60}")
    print(f"  ✅ TTS Server Ready! (MLX)")
    print(f"  Model:       {model_id}")
    print(f"  Device:      Apple Silicon GPU (Metal)")
    print(f"  Sample Rate: {_model.sample_rate}")
    print(f"  URL:         http://localhost:{app.state.port}")
    print(f"{'='*60}\n")

    yield

    # Cleanup
    print("[INFO] Shutting down TTS server...")
    import mlx.core as mx
    _model = None
    mx.clear_cache()


app = FastAPI(
    title="Qwen3-TTS Server (MLX)",
    description="Qwen3-TTS model (MLX) loaded in memory. Native Apple Silicon GPU acceleration.",
    version="2.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Check if model is loaded and ready."""
    return {
        "status": "ok" if _model is not None else "loading",
        "model_loaded": _model is not None,
        "device": "Apple Silicon GPU (Metal/MLX)",
        "uptime_seconds": int(time.time() - _start_time) if _start_time else 0,
        "total_requests": _request_count,
    }


@app.get("/info")
async def model_info():
    """Get model info and server statistics."""
    uptime = int(time.time() - _start_time) if _start_time else 0
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    return {
        "model": app.state.model_id,
        "device": "Apple Silicon GPU (Metal/MLX)",
        "sample_rate": _model.sample_rate if _model else None,
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "total_requests": _request_count,
        "output_dir": str(OUTPUT_DIR),
    }


@app.post("/tts")
async def tts_endpoint(req: TTSRequest):
    """
    Synthesize speech from text.

    Returns WAV audio as binary stream, or saves to file if save_to_file is set.

    Example:
        curl -X POST http://localhost:8100/tts \
             -H "Content-Type: application/json" \
             -d '{"text": "你好，世界！"}' \
             --output hello.wav
    """
    global _request_count

    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    _request_count += 1
    start = time.time()

    try:
        audio, sr = synthesize_speech(
            text=req.text,
            voice=req.voice,
            lang_code=req.lang_code,
            speed=req.speed,
            temperature=req.temperature,
            ref_audio_path=req.ref_audio,
            ref_text=req.ref_text,
        )

        elapsed = time.time() - start
        duration = len(audio) / sr
        print(f"[TTS] {req.text[:50]}... | {elapsed:.1f}s | {duration:.1f}s audio")

        # Save to file if requested
        if req.save_to_file:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path = OUTPUT_DIR / req.save_to_file
            sf.write(str(out_path), audio, sr)
            return JSONResponse({
                "status": "ok",
                "file": str(out_path),
                "duration_seconds": round(duration, 2),
                "inference_seconds": round(elapsed, 2),
            })

        # Return WAV binary stream
        buf = io.BytesIO()
        sf.write(buf, audio, sr, format="WAV")
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type="audio/wav",
            headers={
                "X-Audio-Duration": str(round(duration, 2)),
                "X-Inference-Time": str(round(elapsed, 2)),
            },
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")


@app.post("/tts/slides")
async def tts_slides_endpoint(req: SlidesTTSRequest):
    """
    Generate audio for all slides from script.md.

    Example:
        curl -X POST http://localhost:8100/tts/slides \
             -H "Content-Type: application/json" \
             -d '{}'
    """
    global _request_count

    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    script_path = Path(req.script_path)
    if not script_path.exists():
        raise HTTPException(status_code=404, detail=f"Script not found: {script_path}")

    slides = extract_speaker_notes(script_path)
    if not slides:
        raise HTTPException(status_code=400, detail="No speaker notes found")

    # Filter specific slides
    if req.slides:
        slides = [s for s in slides if s["slide_num"] in req.slides]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for slide in slides:
        _request_count += 1
        start = time.time()
        out_path = OUTPUT_DIR / f"slide_{slide['slide_num']:02d}.wav"

        try:
            audio, sr = synthesize_speech(
                text=slide["text"],
                voice=req.voice,
                lang_code=req.lang_code,
                speed=req.speed,
                temperature=req.temperature,
                ref_audio_path=req.ref_audio,
            )
            sf.write(str(out_path), audio, sr)
            elapsed = time.time() - start
            duration = len(audio) / sr

            print(f"[TTS] Slide {slide['slide_num']:2d} | {elapsed:.1f}s | {duration:.1f}s audio")
            results.append({
                "slide_num": slide["slide_num"],
                "title": slide["title"],
                "file": str(out_path),
                "duration_seconds": round(duration, 2),
                "inference_seconds": round(elapsed, 2),
                "status": "ok",
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ERROR] Slide {slide['slide_num']}: {e}")
            results.append({
                "slide_num": slide["slide_num"],
                "title": slide["title"],
                "status": "error",
                "error": str(e),
            })

    ok_count = sum(1 for r in results if r["status"] == "ok")
    return {
        "total": len(slides),
        "success": ok_count,
        "failed": len(slides) - ok_count,
        "results": results,
    }


# ---- Entry point ----

def main():
    parser = argparse.ArgumentParser(description="Qwen3-TTS HTTP Server (MLX)")
    parser.add_argument(
        "--model", type=str, default=DEFAULT_MODEL_ID,
        help=f"Model ID or local path (default: {DEFAULT_MODEL_ID})",
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0",
        help="Server host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port", type=int, default=8100,
        help="Server port (default: 8100)",
    )
    args = parser.parse_args()

    # Pass config to app state
    app.state.model_id = args.model
    app.state.port = args.port

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()