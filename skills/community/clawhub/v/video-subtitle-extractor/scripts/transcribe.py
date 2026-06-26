#!/usr/bin/env python3
"""Video Subtitle Extractor - ASR Transcription Engine (Multi-Backend)

Runs speech-to-text on audio files using configurable ASR backends.
Supported backends (auto-detected in priority order):
  1. sensevoice  — Alibaba SenseVoice Small, Chinese-optimized, ~1.5GB RAM, 22× realtime
  2. whispercpp  — Whisper via GGML/C++, CPU-optimized, quantized models
  3. openai      — openai-whisper (medium/large-v3, default: medium), ~5GB RAM

Auto-downloads models on first use (SenseVoice via ModelScope, others via HuggingFace or local cache).
"""

import subprocess
import sys
import os
import json
import shutil


# Common ffmpeg install paths on Windows (not always in PATH)
FFMPEG_WIN_PATHS = [
    os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'TRCCCAP', 'ffmpeg.exe'),
    os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'FFmpeg', 'bin', 'ffmpeg.exe'),
    os.path.join(os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)'), 'FFmpeg', 'bin', 'ffmpeg.exe'),
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'ffmpeg', 'bin', 'ffmpeg.exe'),
    os.path.join(os.environ.get('USERPROFILE', ''), 'scoop', 'apps', 'ffmpeg', 'current', 'ffmpeg.exe'),
    os.path.join(os.environ.get('USERPROFILE', ''), 'scoop', 'shims', 'ffmpeg.exe'),
    os.path.join(os.environ.get('ChocolateyInstall', r'C:\ProgramData\chocolatey'), 'bin', 'ffmpeg.exe'),
]

# ---------------------------------------------------------------------------
# Model zoo — lightweight CPU-first
# ---------------------------------------------------------------------------
ALL_MODELS = {
    # ---- SenseVoice (Alibaba, Chinese-optimized) ----
    'sensevoice-small': {
        'backend': 'sensevoice',
        'ram': '~1.5GB', 'disk': '~234MB', 'speed': 'very fast (22x)',
        'quality': 'high (Chinese)', 'label': 'SenseVoice Small ⭐ 轻量中文首选',
    },

    # ---- whisper.cpp (GGML quantized) ----
    'tiny-q5_1': {
        'backend': 'whispercpp',
        'ram': '~0.5GB', 'disk': '~32MB', 'speed': 'fastest',
        'quality': 'low', 'label': 'whisper.cpp tiny-q5_1',
    },
    'small-q5_1': {
        'backend': 'whispercpp',
        'ram': '~1GB', 'disk': '~466MB', 'speed': 'fast',
        'quality': 'decent', 'label': 'whisper.cpp small-q5_1',
    },
    'medium-q5_1': {
        'backend': 'whispercpp',
        'ram': '~2GB', 'disk': '~1.1GB', 'speed': 'medium (3-5x faster than openai)',
        'quality': 'high', 'label': 'whisper.cpp medium-q5_1 ⭐ 轻量中文可选',
    },

    # ---- openai-whisper (standard) ----
    'medium': {
        'backend': 'openai',
        'ram': '~5GB', 'disk': '~1.42GB', 'speed': 'medium',
        'quality': 'high', 'label': 'openai-whisper medium（标准）',
    },
    'large-v3': {
        'backend': 'openai',
        'ram': '~10GB', 'disk': '~2.88GB', 'speed': 'slow',
        'quality': 'best', 'label': 'openai-whisper large-v3（旗舰）',
    },
    'large-v3-turbo': {
        'backend': 'openai',
        'ram': '~6GB', 'disk': '~1.6GB', 'speed': 'medium-fast',
        'quality': 'high', 'label': 'openai-whisper large-v3-turbo',
    },
}


def ensure_ffmpeg_in_path():
    """Ensure ffmpeg is in PATH. If found at known location but not in PATH, add it."""
    if shutil.which('ffmpeg'):
        return True
    for p in FFMPEG_WIN_PATHS:
        if os.path.isfile(p):
            ffmpeg_dir = os.path.dirname(p)
            os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
            print(f'  Added ffmpeg to PATH: {ffmpeg_dir}')
            return True
    return False


def detect_backends():
    """Return list of (backend_name, is_available) for all supported backends."""
    backends = []

    # 1. SenseVoice (highest priority for Chinese)
    try:
        from funasr import AutoModel  # noqa: F401
        backends.append(('sensevoice', True))
    except ImportError:
        backends.append(('sensevoice', False))

    # 2. whisper.cpp (next priority)
    try:
        from pywhispercpp.model import Model  # noqa: F401
        backends.append(('whispercpp', True))
    except ImportError:
        backends.append(('whispercpp', False))

    # 3. openai-whisper (fallback)
    try:
        import whisper  # noqa: F401
        backends.append(('openai', True))
    except ImportError:
        backends.append(('openai', False))

    return backends


# ---- Helpers ----
def _fmt_timestamp(seconds):
    """Format seconds to SRT/VTT timestamp."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def _write_srt(segments, path):
    """Write SRT subtitle file."""
    with open(path, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            start = _fmt_timestamp(seg['start'])
            end = _fmt_timestamp(seg['end'])
            f.write(f'{i}\n{start} --> {end}\n{seg["text"].strip()}\n\n')


def _write_vtt(segments, path):
    """Write WebVTT subtitle file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write('WEBVTT\n\n')
        for seg in segments:
            start = _fmt_timestamp(seg['start']).replace(',', '.')
            end = _fmt_timestamp(seg['end']).replace(',', '.')
            f.write(f'{start} --> {end}\n{seg["text"].strip()}\n\n')


def _write_outputs(segments, output_dir, base, output_format='all'):
    """Write transcription segments to disk in requested formats."""
    output_files = {}
    if output_format in ('txt', 'all'):
        txt_path = os.path.join(output_dir, f'{base}.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            for seg in segments:
                f.write(seg['text'].strip() + '\n')
        output_files['txt'] = txt_path
        print(f'  [OK] {txt_path}')

    if output_format in ('srt', 'all'):
        srt_path = os.path.join(output_dir, f'{base}.srt')
        _write_srt(segments, srt_path)
        output_files['srt'] = srt_path
        print(f'  [OK] {srt_path}')

    if output_format in ('vtt', 'all'):
        vtt_path = os.path.join(output_dir, f'{base}.vtt')
        _write_vtt(segments, vtt_path)
        output_files['vtt'] = vtt_path
        print(f'  [OK] {vtt_path}')

    if output_format in ('json', 'all'):
        json_path = os.path.join(output_dir, f'{base}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        output_files['json'] = json_path
        print(f'  [OK] {json_path}')

    return output_files


# ============================================================================
# Backend: SenseVoice (Alibaba FunASR)
# ============================================================================

SENSEVOICE_MODEL_ID = 'iic/SenseVoiceSmall'

# SenseVoice emotion/event tags to strip from output
SENSEVOICE_TAGS = [
    '<|zh|>', '<|en|>', '<|yue|>', '<|ja|>', '<|ko|>',
    '<|HAPPY|>', '<|SAD|>', '<|ANGRY|>', '<|NEUTRAL|>',
    '<|Speech|>', '<|Sing|>', '<|EMO_UNKNOWN|>',
    '<|woitn|>', '<|withitn|>', '<|EMOTIONAL|>',
]


def transcribe_sensevoice(audio_path, model_name=None, language='zh',
                          output_dir=None, output_format='all'):
    """Transcribe using Alibaba SenseVoice Small.

    Args:
        audio_path: Path to audio file
        model_name: Ignored (always uses SenseVoiceSmall)
        language: 'zh' / 'en' / 'auto'
        output_dir: Output directory for results
        output_format: 'txt', 'srt', 'vtt', 'json', or 'all'

    Returns:
        Dict with paths to output files.
    """
    from funasr import AutoModel
    import re

    if output_dir is None:
        output_dir = os.path.dirname(audio_path) or '.'
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(audio_path))[0]

    # Load model (auto-downloads from ModelScope on first use)
    print(f'Loading SenseVoice Small (234MB, ~1.5GB RAM)...')
    model = AutoModel(
        model=SENSEVOICE_MODEL_ID,
        disable_update=True,
        device='cpu',
    )

    # Map language code
    lang_map = {'zh': 'zh', 'en': 'en', 'ja': 'ja', 'ko': 'ko', 'yue': 'yue'}
    lang = lang_map.get(language, 'zh')

    print(f'Transcribing {audio_path}...')
    print(f'  Language: {lang}')
    result = model.generate(input=audio_path, language=lang)

    text = result[0]['text'] if result else ''

    # Strip SenseVoice metadata tags
    for tag in SENSEVOICE_TAGS:
        text = text.replace(tag, '')
    text = re.sub(r'<\|[^|]+\|>', '', text)  # catch any remaining tags
    text = text.strip()

    # SenseVoice doesn't provide timestamps — create one segment
    segments = [{'start': 0.0, 'end': 0.0, 'text': text}]

    output_files = _write_outputs(segments, output_dir, base, output_format)

    return output_files


# ============================================================================
# Backend: whisper.cpp (GGML via pywhispercpp)
# ============================================================================

WHISPERCPP_MODEL_DIR = os.path.join(os.environ.get('USERPROFILE', '~'), '.cache', 'whispercpp')

# GGML model files required for each model name
GGML_MODEL_FILES = {
    'tiny-q5_1':   'ggml-tiny-q5_1.bin',
    'tiny-q8_0':   'ggml-tiny-q8_0.bin',
    'small-q5_1':  'ggml-small-q5_1.bin',
    'small-q8_0':  'ggml-small-q8_0.bin',
    'medium-q5_1': 'ggml-medium-q5_1.bin',
    'medium-q8_0': 'ggml-medium-q8_0.bin',
    'large-v3-q5_1': 'ggml-large-v3-q5_1.bin',
}

GGML_DOWNLOAD_HELP = """
======================================================================
whisper.cpp GGML model not found.

To use the whispercpp backend, download a GGML model file from:
  https://huggingface.co/ggerganov/whisper.cpp

Recommended for Chinese:
  ggml-medium-q5_1.bin  (1.1GB, best quality/size balance)
  ggml-small-q5_1.bin   (466MB, fast, decent quality)

Place the file in: {model_dir}
Then re-run with: --backend whispercpp --model medium-q5_1
======================================================================
"""


def _find_ggml_model(model_name):
    """Find the GGML model file. Returns absolute path or None."""
    filename = GGML_MODEL_FILES.get(model_name)
    if not filename:
        print(f'[ERROR] Unknown whisper.cpp model: {model_name}')
        print(f'  Known: {", ".join(GGML_MODEL_FILES.keys())}')
        return None

    # Check in model dir
    path = os.path.join(WHISPERCPP_MODEL_DIR, filename)
    if os.path.isfile(path):
        return path

    # Check current dir
    if os.path.isfile(filename):
        return filename

    # Not found
    print(f'[ERROR] GGML model not found: {filename}')
    print(GGML_DOWNLOAD_HELP.format(model_dir=WHISPERCPP_MODEL_DIR))
    return None


def transcribe_whispercpp(audio_path, model_name='medium-q5_1', language='zh',
                          output_dir=None, output_format='all'):
    """Transcribe using whisper.cpp via pywhispercpp.

    Args:
        audio_path: Path to audio file
        model_name: GGML model name (tiny-q5_1, small-q5_1, medium-q5_1, etc.)
        language: Language code (zh/en/ja etc.)
        output_dir: Output directory for results
        output_format: 'txt', 'srt', 'vtt', 'json', or 'all'

    Returns:
        Dict with paths to output files, or None if model not found.
    """
    from pywhispercpp.model import Model

    model_path = _find_ggml_model(model_name)
    if not model_path:
        return None

    if output_dir is None:
        output_dir = os.path.dirname(audio_path) or '.'
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(audio_path))[0]

    print(f'Loading whisper.cpp model: {model_name} ({os.path.basename(model_path)})')
    model = Model(model_path, verbose=False)
    print(f'Transcribing {audio_path}...')
    print(f'  Language: {language}')

    raw_segments = model.transcribe(audio_path, language=language)

    segments = []
    for i, seg in enumerate(raw_segments):
        segments.append({
            'id': i,
            'start': round(seg.t0 * 0.01, 3),  # pywhispercpp uses centiseconds
            'end':   round(seg.t1 * 0.01, 3),
            'text':  seg.text.strip(),
        })

    output_files = _write_outputs(segments, output_dir, base, output_format)

    return output_files


# ============================================================================
# Backend: openai-whisper (standard)
# ============================================================================

def transcribe_openai(audio_path, model_name='medium', language='zh',
                      output_dir=None, output_format='txt'):
    """Transcribe using openai-whisper.

    Args:
        audio_path: Path to audio file
        model_name: Whisper model size (tiny/medium/large-v3)
        language: Language code (zh/en/ja etc.)
        output_dir: Output directory for results
        output_format: 'txt', 'srt', 'vtt', 'json', or 'all'

    Returns:
        Dict with paths to output files.
    """
    import whisper

    if output_dir is None:
        output_dir = os.path.dirname(audio_path) or '.'
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(audio_path))[0]

    print(f'Loading whisper model: {model_name}...')
    model = whisper.load_model(model_name)
    print(f'Model loaded. Transcribing {audio_path}...')
    print(f'  Language: {language}')

    use_fp16 = False
    try:
        import torch
        use_fp16 = torch.cuda.is_available()
    except ImportError:
        pass

    result = model.transcribe(
        audio_path,
        language=language,
        verbose=True,
        fp16=use_fp16,
    )

    segments = []
    for seg in result['segments']:
        segments.append({
            'id': seg.get('id', len(segments)),
            'start': seg['start'],
            'end': seg['end'],
            'text': seg['text'].strip(),
        })

    output_files = _write_outputs(segments, output_dir, base, output_format)

    return output_files


# ============================================================================
# Main entry point
# ============================================================================

def transcribe(audio_path, model='sensevoice-small', language='zh',
               output_dir=None, output_format='all', backend='auto'):
    """Main transcription entry point — multi-backend dispatcher.

    Args:
        audio_path:   Path to audio file
        model:        Model name (see ALL_MODELS keys). Default: 'sensevoice-small'
        language:     Language code (zh/en/ja etc.)
        output_dir:   Output directory
        output_format: 'txt', 'srt', 'vtt', 'json', or 'all'
        backend:      'auto' (best available) | 'sensevoice' | 'whispercpp' | 'openai'

    Returns:
        Dict with output file paths, or None on error.
    """
    if not os.path.exists(audio_path):
        print(f'[ERROR] Audio file not found: {audio_path}')
        return None

    if not ensure_ffmpeg_in_path():
        print('[ERROR] ffmpeg not found. Install ffmpeg first.')
        return None

    # Resolve model info
    model_info = ALL_MODELS.get(model, {})
    if model_info:
        print(f'Model: {model} ({model_info.get("label", "")})')
        print(f'       RAM: {model_info.get("ram", "?")} | '
              f'Disk: {model_info.get("disk", "?")} | '
              f'Speed: {model_info.get("speed", "?")} | '
              f'Quality: {model_info.get("quality", "?")}')
    else:
        # Unknown model — use as-is with requested backend
        model_info = {'backend': backend}
        print(f'Model: {model} (custom)')

    # Detect available backends
    backends_available = {name: ok for name, ok in detect_backends()}

    # Resolve which backend to use
    target_backend = model_info.get('backend', 'openai')

    if backend != 'auto':
        # Explicit backend requested — must be available
        target_backend = backend
        if not backends_available.get(target_backend):
            print(f'[ERROR] Requested backend "{target_backend}" is not available.')
            avail = [n for n, ok in backends_available.items() if ok]
            if avail:
                print(f'  Available: {", ".join(avail)}')
            return None
        # For openai backend, override model if current model is not an openai model
        if target_backend == 'openai' and model_info.get('backend') != 'openai':
            # Use model name as-is — openai-whisper will handle unknown gracefully
            pass
    else:
        # Auto mode: prefer user's model's native backend, then fallback
        if not backends_available.get(target_backend):
            # Fallback priority: sensevoice → whispercpp → openai
            for fb in ('sensevoice', 'whispercpp', 'openai'):
                if backends_available.get(fb):
                    target_backend = fb
                    print(f'  (native backend unavailable, auto-fallback → {fb})')
                    break

    print(f'Backend: {target_backend}')
    print()

    # Dispatch
    if target_backend == 'sensevoice':
        return transcribe_sensevoice(audio_path, model, language, output_dir, output_format)

    elif target_backend == 'whispercpp':
        return transcribe_whispercpp(audio_path, model, language, output_dir, output_format)

    elif target_backend == 'openai':
        return transcribe_openai(audio_path, model, language, output_dir, output_format)

    else:
        print(f'[ERROR] Unknown backend: {target_backend}')
        return None


def show_backends():
    """Print a summary of available backends."""
    available = {name: ok for name, ok in detect_backends()}
    print('ASR Backends:')
    print('=' * 60)
    status_icons = {
        'openai': '✅ 标准（5GB RAM，全能）',
        'sensevoice': '✅ 轻量（1.5GB RAM，中文优化，22×实时）',
        'whispercpp': '✅ 轻量（0.5-2GB RAM，GGML量化，CPU极致优化）',
    }
    for name, ok in available.items():
        icon = '✅' if ok else '❌'
        desc = status_icons.get(name, '')
        print(f'  {icon} {name:12s} {desc}')
    print()
    print('Installation:')
    print('  sensevoice:  pip install funasr modelscope')
    print('  whispercpp:  pip install pywhispercpp')
    print('               + download GGML model from huggingface.co/ggerganov/whisper.cpp')
    print('  openai:      pip install openai-whisper')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='ASR Transcription Engine (multi-backend)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Backends:
  sensevoice  Alibaba FunASR - Chinese optimized, lightweight (1.5GB RAM)
  whispercpp  Whisper GGML/C++ - CPU optimized, quantized, fast
  openai      openai-whisper - general purpose (5GB RAM standard)

Model Presets:
  sensevoice-small  SenseVoice Small (234MB) — best for Chinese ⭐
  medium-q5_1       whisper.cpp medium GGML (1.1GB) — lightweight quality
  medium            openai-whisper medium (1.42GB) — standard
  large-v3          openai-whisper large-v3 (2.88GB) — best accuracy

Examples:
  python transcribe.py video.m4a --backend auto                          # best available
  python transcribe.py video.m4a --backend sensevoice --language zh      # Chinese optimized
  python transcribe.py video.m4a --backend whispercpp --model medium-q5_1
  python transcribe.py video.m4a --backend openai --model medium
  python transcribe.py video.m4a --backend auto --format txt,srt         # select formats
        """
    )
    parser.add_argument('audio', help='Audio file path')
    parser.add_argument('--model', default='sensevoice-small',
                        help='Model name (default: sensevoice-small)')
    parser.add_argument('--language', default='zh',
                        help='Language code (default: zh)')
    parser.add_argument('--output-dir', '-o', default=None,
                        help='Output directory')
    parser.add_argument('--format', default='all',
                        choices=['txt', 'srt', 'vtt', 'json', 'all'],
                        help='Output format (default: all)')
    parser.add_argument('--backend', default='auto',
                        choices=['auto', 'sensevoice', 'whispercpp', 'openai'],
                        help='ASR backend (default: auto)')
    parser.add_argument('--show-backends', action='store_true',
                        help='Show available backends and exit')

    args = parser.parse_args()

    if args.show_backends:
        show_backends()
        sys.exit(0)

    result = transcribe(
        args.audio,
        model=args.model,
        language=args.language,
        output_dir=args.output_dir,
        output_format=args.format,
        backend=args.backend,
    )

    if result:
        print()
        print('=== Output files ===')
        for fmt, path in result.items():
            print(f'  {fmt}: {path}')
        sys.exit(0)
    else:
        sys.exit(1)
