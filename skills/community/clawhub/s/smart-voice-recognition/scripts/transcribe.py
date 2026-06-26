#!/usr/bin/env python3
"""
Intelligent Voice Recognition — Smart Auto-Model Selection

Transcribe audio files using OpenAI Whisper (local, no API key).
Automatically analyzes audio length and complexity, then selects the 
optimal model for speed vs accuracy.

Features:
  - Smart model auto-selection based on audio duration and complexity
  - Supports Chinese, English, Cantonese, Spanish, and 99+ languages
  - No API key required, runs fully locally
  - Segment-level timestamps for long recordings

Supported formats: .ogg, .wav, .mp3, .m4a, .flac, .opus
"""
import sys
import os

# Ensure whisper venv is in path (fallback for different Python versions)
_VENV_PATHS = [
    '/tmp/whisper-venv/lib/python3.12/site-packages',
    '/tmp/whisper-venv/lib/python3.11/site-packages',
    '/tmp/whisper-venv/lib/python3.10/site-packages',
]
for p in _VENV_PATHS:
    if os.path.exists(p):
        sys.path.insert(0, p)
        break

import whisper
import soundfile as sf
import numpy as np
import argparse
import time


# Auto-selection rules
_AUTO_RULES = {
    # (max_duration_seconds, is_complex) -> model
    # Simple = single-language, clean speech
    # Complex = mixed languages, noise, accents
    'short_simple':   (10,  False, 'base'),     # <10s, clean → fast & accurate
    'short_complex':  (10,  True,  'small'),    # <10s, mixed → small
    'medium_simple':  (60,  False, 'base'),     # <60s, clean → base (fast)
    'medium_complex': (60,  True,  'small'),    # <60s, mixed → small
    'long_simple':    (120, False, 'small'),    # <2min → small for accuracy
    'long_complex':   (120, True,  'small'),    # <2min mixed → small
    'very_long':      (999, False, 'medium'),   # 2min+ → medium for context
}


def analyze_audio(audio_path):
    """Load audio and return (audio_array, sample_rate, duration_seconds)."""
    audio, sr = sf.read(audio_path)
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)
    audio = audio.astype(np.float32)
    duration = len(audio) / sr
    return audio, sr, duration


def detect_complexity(audio, sr):
    """
    Heuristic complexity detection.
    Returns True if audio likely contains mixed languages or noise.
    """
    duration = len(audio) / sr
    
    # Long audio always gets higher model (more context to process)
    if duration > 60:
        return True
    
    # Check energy variance — high variance may indicate language switches
    frame_length = int(sr * 0.5)  # 500ms frames
    if len(audio) > frame_length * 2:
        frames = []
        for i in range(0, len(audio) - frame_length, frame_length // 2):
            frames.append(np.sqrt(np.mean(audio[i:i+frame_length]**2)))
        energy_std = np.std(frames) if frames else 0
        energy_mean = np.mean(frames) if frames else 1
        cv = energy_std / (energy_mean + 1e-8)
        if duration < 10:
            return cv > 3.0  # Very short: only flag if extreme
        elif duration < 30:
            return cv > 1.5  # Short: moderate threshold
        else:
            return cv > 0.6  # Longer: more sensitive
    return False


def auto_select_model(duration, is_complex):
    """Select the best model based on audio characteristics."""
    thresholds = [
        (duration <= 10,  not is_complex, 'short_simple',  'base'),
        (duration <= 10,  is_complex,     'short_complex', 'small'),
        (duration <= 60,  not is_complex, 'medium_simple', 'base'),
        (duration <= 60,  is_complex,     'medium_complex','small'),
        (duration <= 120, not is_complex, 'long_simple',   'small'),
        (duration <= 120, is_complex,     'long_complex',  'small'),
    ]
    for cond_dur, cond_cpx, key, model in thresholds:
        if cond_dur and cond_cpx:
            return model, key
    return 'medium', 'very_long'


def transcribe(audio_path, model_name=None, language=None, auto_mode=True):
    """
    Transcribe an audio file with smart model selection.

    Args:
        audio_path: Path to audio file
        model_name: Force a specific model (overrides auto)
        language: Language hint (None = auto-detect)
        auto_mode: Enable smart model auto-selection

    Returns:
        dict with keys: text, segments, model_used, duration, auto_info
    """
    start = time.time()
    result = {'duration': 0, 'model_used': model_name or 'auto', 'auto_info': {}}

    # Load and analyze audio
    print(f"📂 Loading audio: {os.path.basename(audio_path)}", file=sys.stderr, flush=True)
    audio, sr, duration = analyze_audio(audio_path)
    result['duration'] = duration
    print(f"⏱  Duration: {duration:.1f}s | Sample rate: {sr}Hz", file=sys.stderr, flush=True)

    # Auto-select model
    if auto_mode and model_name is None:
        is_complex = detect_complexity(audio, sr)
        model_name, rule_key = auto_select_model(duration, is_complex)
        result['auto_info'] = {
            'duration': f"{duration:.1f}s",
            'complex': is_complex,
            'rule': rule_key,
        }
        print(f"🧠 Auto-selected model: {model_name.upper()}", file=sys.stderr, flush=True)
        if is_complex:
            print(f"   ↳ Reason: Longer audio or mixed-language content detected", file=sys.stderr, flush=True)
        else:
            print(f"   ↳ Reason: Short/clean audio, prioritizing speed", file=sys.stderr, flush=True)
    else:
        model_name = model_name or 'base'

    result['model_used'] = model_name

    # Load model
    model = whisper.load_model(model_name)
    load_time = time.time() - start
    print(f"✓ Model loaded ({load_time:.1f}s)", file=sys.stderr, flush=True)

    # Transcribe
    print(f"🎯 Transcribing...", file=sys.stderr, flush=True)
    kwargs = {}
    if language:
        kwargs['language'] = language
    whisper_result = model.transcribe(audio, **kwargs)
    total_time = time.time() - start
    print(f"✅ Done ({total_time:.1f}s total)", file=sys.stderr, flush=True)

    result['text'] = whisper_result["text"].strip()
    result['segments'] = whisper_result.get("segments", [])
    result['total_time'] = total_time
    return result


def format_output(result, show_segments=False):
    """Format transcription result as a clean string."""
    lines = []
    lines.append(result['text'])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="🎤 Voice Recognition — Smart model auto-selection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s voice.ogg                    # Auto-select best model\n"
            "  %(prog)s voice.ogg --model small      # Force small model\n"
            "  %(prog)s voice.ogg --language en      # English transcription\n"
            "  %(prog)s voice.ogg --segments         # Show timestamps\n"
            "  %(prog)s voice.ogg --auto-off         # Disable auto-selection\n"
        )
    )
    parser.add_argument("audio_path", help="Path to audio file (.ogg/.wav/.mp3/.m4a/.flac/.opus)")
    parser.add_argument("--model", "-m", default=None,
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Force specific model (default: auto-select)")
    parser.add_argument("--language", "-l", default=None,
                        help="Language hint (default: auto-detect). Examples: zh, en, yue, ja, es")
    parser.add_argument("--auto-off", action="store_true",
                        help="Disable smart auto-selection, use base model")
    parser.add_argument("--output", "-o", help="Save transcription to file")
    parser.add_argument("--segments", "-s", action="store_true",
                        help="Show segment-level timestamps")

    args = parser.parse_args()

    if not os.path.exists(args.audio_path):
        print(f"❌ Error: File not found: {args.audio_path}", file=sys.stderr)
        sys.exit(1)

    # Run transcription
    result = transcribe(
        args.audio_path,
        model_name='base' if args.auto_off else args.model,
        language=args.language,
        auto_mode=not args.auto_off and args.model is None,
    )

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result['text'] + "\n")
        print(f"💾 Saved to: {args.output}", file=sys.stderr)
    else:
        print(result['text'])

    # Segments to stderr
    if args.segments and result.get('segments'):
        print("\n📝 Segments:", file=sys.stderr)
        for seg in result['segments']:
            print(f"   [{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}", file=sys.stderr)


if __name__ == "__main__":
    main()
