#!/usr/bin/env python3
"""
Qwen3-TTS batch generator (MLX) — no server required.

Loads the model once, then synthesizes speech for all slides in a JSON file.
Reads configuration directly from config/project.json.

Usage:
    python scripts/tts_qwen.py [--config config/project.json] [--content content/subtitles.json]

Prerequisites:
    Activate your Python env (conda or venv) with mlx-audio, soundfile, numpy installed.
    Run via: make tts-qwen (reads env config from config/project.json)
"""

import os
import re
import sys
import time

import numpy as np
import soundfile as sf

from tts_utils import resolve_project_root, parse_tts_args, load_config_and_content, resolve_audio_dir


# ---- Max tokens estimation ----
# Qwen3-TTS at 12Hz: 1 second of audio ~ 12 tokens.
# Default constants (overridden by config at runtime)
_TOKENS_PER_CHAR = 4
_MIN_MAX_TOKENS = 180       # floor ~ 15 seconds
_MAX_MAX_TOKENS = 2400      # hard ceiling (~200 seconds max)
_AUDIO_HZ = 12              # model codec frame-rate

def _estimate_max_tokens(text: str) -> int:
    """Estimate a safe max_tokens limit based on text length."""
    estimated = len(text) * _TOKENS_PER_CHAR
    return max(_MIN_MAX_TOKENS, min(estimated, _MAX_MAX_TOKENS))


def split_sentences(text: str) -> list[str]:
    """Split Chinese text into sentences at punctuation boundaries."""
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
    if buf.strip():
        sentences.append(buf.strip())
    return sentences


# Short text threshold and sentence gap (overridden by config at runtime)
_SHORT_TEXT_THRESHOLD = 200
_SENTENCE_GAP_SEC = 0.15
# Silence trimming defaults (overridden by config at runtime)
_SILENCE_THRESHOLD = 0.005
# Hallucination trimming defaults (overridden by config at runtime)
_CHARS_PER_SECOND = 4.0
_HALLUCINATION_HEADROOM = 2.0

def _trim_silence(
    audio: np.ndarray,
    sr: int,
    threshold: float = 0.005,
    min_silence_ms: int = 100,
    keep_leading_ms: int = 80,
    keep_trailing_ms: int = 150,
) -> np.ndarray:
    """Trim leading and trailing silence from audio."""
    if len(audio) == 0:
        return audio

    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio

    abs_audio = np.abs(audio)
    cutoff = peak * threshold

    nonsilent = np.where(abs_audio > cutoff)[0]
    if len(nonsilent) == 0:
        return audio

    first_sound = nonsilent[0]
    last_sound = nonsilent[-1]

    min_silence_samples = int(sr * min_silence_ms / 1000)
    keep_lead = int(sr * keep_leading_ms / 1000)
    keep_trail = int(sr * keep_trailing_ms / 1000)

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
    chars_per_second: float = _CHARS_PER_SECOND,
    headroom: float = _HALLUCINATION_HEADROOM,
) -> np.ndarray:
    """Hard-trim audio that exceeds the expected duration based on text length."""
    expected_sec = text_len / chars_per_second
    max_sec = max(expected_sec * headroom, 5.0)
    max_samples = int(sr * max_sec)

    if len(audio) > max_samples:
        actual_sec = len(audio) / sr
        print(f"[TRIM-HALLUCINATION] Audio {actual_sec:.1f}s exceeds "
              f"expected {expected_sec:.1f}s x {headroom} = {max_sec:.1f}s cap. "
              f"Hard-trimming to {max_sec:.1f}s")
        audio = audio[:max_samples]
        fade_samples = int(sr * 0.05)
        if len(audio) > fade_samples:
            fade = np.linspace(1.0, 0.0, fade_samples, dtype=audio.dtype)
            audio[-fade_samples:] *= fade

    return audio





def synthesize_one(model, text, voice, lang_code, speed, temperature):
    """Synthesize a single text segment. Returns raw audio numpy array."""
    import mlx.core as mx

    max_tokens = _estimate_max_tokens(text)
    expected_max_sec = max_tokens / _AUDIO_HZ
    print(f"[TTS] text={len(text)} chars, max_tokens={max_tokens} "
          f"(~{expected_max_sec:.0f}s cap)")

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

    results = model.generate(**gen_kwargs)

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

    actual_sec = len(audio) / model.sample_rate
    if actual_sec > expected_max_sec * 0.95:
        print(f"[WARN] Audio hit max_tokens cap: {actual_sec:.1f}s "
              f"(cap={expected_max_sec:.0f}s) for text: {text[:40]}")

    return audio


def synthesize_speech(model, text, voice, lang_code, speed, temperature):
    """
    Generate speech audio from text using MLX Qwen3-TTS.

    Strategy:
      - Short texts (< 200 chars): synthesize as a single chunk.
      - Long texts (>= 200 chars): split into sentences and concatenate.

    Returns:
        tuple: (audio_numpy_array, sample_rate)
    """
    sr = model.sample_rate

    if len(text) < _SHORT_TEXT_THRESHOLD:
        print(f"[TTS] Short text ({len(text)} chars), synthesizing as single chunk")
        audio = synthesize_one(model, text, voice, lang_code, speed, temperature)
        audio = _trim_silence(audio, sr, threshold=_SILENCE_THRESHOLD)
        audio = _trim_hallucination(audio, sr, len(text))
        return audio, sr

    sentences = split_sentences(text)

    if len(sentences) <= 1:
        audio = synthesize_one(model, text, voice, lang_code, speed, temperature)
        audio = _trim_silence(audio, sr, threshold=_SILENCE_THRESHOLD)
        audio = _trim_hallucination(audio, sr, len(text))
        return audio, sr

    # Multiple sentences — per-sentence synthesis
    print(f"[TTS] Long text ({len(text)} chars), splitting into "
          f"{len(sentences)} sentences")

    gap_samples = int(sr * _SENTENCE_GAP_SEC)
    silence = np.zeros(gap_samples, dtype=np.float32)

    all_parts = []
    for i, sent in enumerate(sentences):
        seg_start = time.time()
        audio_seg = synthesize_one(
            model, sent, voice, lang_code, speed, temperature
        )
        audio_seg = _trim_silence(audio_seg, sr, threshold=_SILENCE_THRESHOLD)
        audio_seg = _trim_hallucination(audio_seg, sr, len(sent))
        seg_elapsed = time.time() - seg_start

        seg_dur = len(audio_seg) / sr
        print(f"  [{i+1}/{len(sentences)}] {len(sent)} chars -> "
              f"{seg_dur:.1f}s audio ({seg_elapsed:.1f}s wall)")

        all_parts.append(audio_seg)
        if i < len(sentences) - 1:
            all_parts.append(silence)

    audio = np.concatenate(all_parts, axis=0)
    return audio, sr


def main():
    args = parse_tts_args("Qwen3-TTS batch generator (MLX) — reads config directly")
    root = resolve_project_root()
    config, content, _, _ = load_config_and_content(args, root)
    output_dir = resolve_audio_dir(config, root)

    qwen_config = config["tts"]["qwen"]
    slides = content.get("slides", [])
    if not slides:
        print("[ERROR] No slides found in content file")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Extract config values
    model_id = qwen_config.get("model", "mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-bf16")
    voice = qwen_config.get("voice", "Chelsie")
    lang_code = qwen_config.get("lang_code", "zh")
    # Apply global speedRate multiplier to per-engine speed
    global_speed_rate = config["tts"].get("speedRate", 1.0)
    engine_speed = qwen_config.get("speed", 1.0)
    speed = engine_speed * global_speed_rate
    temperature = qwen_config.get("temperature", 0.3)

    # Override module-level algorithm constants from config
    global _TOKENS_PER_CHAR, _MIN_MAX_TOKENS, _MAX_MAX_TOKENS
    global _SHORT_TEXT_THRESHOLD, _SENTENCE_GAP_SEC
    global _SILENCE_THRESHOLD, _CHARS_PER_SECOND, _HALLUCINATION_HEADROOM
    _TOKENS_PER_CHAR = qwen_config.get("tokens_per_char", _TOKENS_PER_CHAR)
    _MIN_MAX_TOKENS = qwen_config.get("min_max_tokens", _MIN_MAX_TOKENS)
    _MAX_MAX_TOKENS = qwen_config.get("max_max_tokens", _MAX_MAX_TOKENS)
    _SHORT_TEXT_THRESHOLD = qwen_config.get("short_text_threshold", _SHORT_TEXT_THRESHOLD)
    _SENTENCE_GAP_SEC = qwen_config.get("sentence_gap_sec", _SENTENCE_GAP_SEC)
    _SILENCE_THRESHOLD = qwen_config.get("silence_threshold", _SILENCE_THRESHOLD)
    _CHARS_PER_SECOND = qwen_config.get("chars_per_second", _CHARS_PER_SECOND)
    _HALLUCINATION_HEADROOM = qwen_config.get("hallucination_headroom", _HALLUCINATION_HEADROOM)

    # Load model once
    from mlx_audio.tts.utils import load_model

    print(f"\n{'=' * 50}")
    print(f"  Qwen3-TTS Batch Generator (MLX)")
    print(f"{'=' * 50}")
    print(f"  Model     : {model_id}")
    print(f"  Voice     : {voice}")
    print(f"  SpeedRate : {global_speed_rate}x (engine: {engine_speed} → effective: {speed})")
    print(f"  Slides    : {len(slides)}")
    print(f"{'=' * 50}")

    print(f"\n[INFO] Loading MLX model: {model_id}")
    t0 = time.time()
    model = load_model(model_path=model_id)
    print(f"[INFO] Model loaded in {time.time() - t0:.1f}s "
          f"(sample_rate={model.sample_rate})\n")

    # Process each slide
    total_audio_sec = 0.0
    total_wall_sec = 0.0

    for slide in slides:
        slide_id = slide["id"]
        text = slide["text"]
        out_file = os.path.join(output_dir, f"{slide_id}.wav")

        if os.path.exists(out_file):
            print(f"  [SKIP] {slide_id} — already exists")
            continue

        print(f'  [GEN]  {slide_id} — "{text[:40]}..."')

        try:
            t0 = time.time()
            audio, sr = synthesize_speech(
                model=model,
                text=text,
                voice=voice,
                lang_code=lang_code,
                speed=speed,
                temperature=temperature,
            )
            elapsed = time.time() - t0
            duration = len(audio) / sr

            sf.write(out_file, audio, sr)
            print(f"         ✅ {out_file} "
                  f"({duration:.1f}s audio, {elapsed:.1f}s wall)")

            total_audio_sec += duration
            total_wall_sec += elapsed

        except Exception as e:
            print(f"         ❌ Failed: {e}")

    print(f"\n✅ Qwen TTS generation complete!")
    print(f"   Total audio: {total_audio_sec:.1f}s")
    print(f"   Total wall:  {total_wall_sec:.1f}s")
    print(f"   Output: {output_dir}")


if __name__ == "__main__":
    main()
