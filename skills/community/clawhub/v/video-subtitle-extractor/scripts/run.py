#!/usr/bin/env python3
"""Video Subtitle Extractor - Main Pipeline

Complete pipeline: Video URL -> Audio -> ASR -> Subtitles -> Calibrate.
Default model: medium (small removed due to poor accuracy).

Selective reuse:
  --skip-download    Reuse existing .m4a in output_dir (find by title or newest)
  --skip-transcribe  Reuse existing transcript files (find .txt in output_dir)
  Both flags → re-run pipeline metadata/summary only (fastest)

Usage:
  python run.py <video_url> [--model medium] [--language zh] [--output-dir .]
  python run.py <video_url> --skip-download           # re-transcribe, keep audio
  python run.py <video_url> --skip-transcribe         # audio already transcribed, fast
"""

import argparse
import os
import re
import sys
import json
import glob
import shutil


# Common ffmpeg install paths on Windows (not always in PATH)
FFMPEG_WIN_PATHS = [
    os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'TRCCCAP', 'ffmpeg.exe'),
    os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'FFmpeg', 'bin', 'ffmpeg.exe'),
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'ffmpeg', 'bin', 'ffmpeg.exe'),
]


def find_ffmpeg():
    """Find ffmpeg executable path."""
    path = shutil.which('ffmpeg')
    if path:
        return path
    for p in FFMPEG_WIN_PATHS:
        if os.path.isfile(p):
            return p
    return None


def ensure_deps():
    """Verify all dependencies are available."""
    missing = []

    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        missing.append('ffmpeg (install via: winget install Gyan.FFmpeg)')
    else:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        if ffmpeg_dir not in os.environ.get('PATH', ''):
            os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
    try:
        import yt_dlp
    except ImportError:
        missing.append('yt-dlp (pip install yt-dlp)')
    # Check at least one ASR backend is available
    try:
        from transcribe import detect_backends
        backends = detect_backends()
        available = [n for n, ok in backends if ok]
        if not available:
            missing.append('ASR backend (install one: pip install openai-whisper)')
        else:
            print(f'  ASR backends available: {", ".join(available)}')
    except Exception:
        missing.append('transcribe.py (module not found)')

    if missing:
        print('[ERROR] Missing dependencies:')
        for m in missing:
            print(f'  - {m}')
        print()
        print('Run install_deps.py first, or install manually.')
        return False
    return True


def find_artifacts_in_dir(output_dir, url=None):
    """Find existing audio + video artifacts in output_dir.

    Returns dict with optional 'm4a' and 'mp4' keys, or None.
    """
    if not os.path.isdir(output_dir):
        return None

    result = {}

    # Strategy 1: try URL slug match for both audio and video
    if url:
        slug_match = re.search(r'/([a-zA-Z0-9]+)(?:\?|$)', url)
        if slug_match:
            slug = slug_match.group(1)
            for f in os.listdir(output_dir):
                if slug in f:
                    full = os.path.join(output_dir, f)
                    if f.endswith('.m4a') and 'm4a' not in result:
                        result['m4a'] = full
                    elif f.endswith('.mp4') and 'mp4' not in result:
                        result['mp4'] = full

    # Strategy 2: fall back to newest files
    if 'm4a' not in result:
        m4a_files = glob.glob(os.path.join(output_dir, '*.m4a'))
        if m4a_files:
            result['m4a'] = max(m4a_files, key=os.path.getmtime)
    if 'mp4' not in result:
        mp4_files = glob.glob(os.path.join(output_dir, '*.mp4'))
        if mp4_files:
            result['mp4'] = max(mp4_files, key=os.path.getmtime)

    return result if result else None


def find_transcript_in_dir(output_dir, audio_path):
    """Find existing transcript files matching the given audio file.

    Matches by: audio filename base → {base}.txt / .srt / .vtt / .json
    Falls back to newest .txt in output_dir if audio_path is None.
    
    Returns dict of {fmt: path} or None.
    """
    if not os.path.isdir(output_dir):
        return None

    base = None
    if audio_path:
        base = os.path.splitext(os.path.basename(audio_path))[0]
        # Check if at least the .txt exists for this audio file
        if os.path.exists(os.path.join(output_dir, base + '.txt')):
            pass  # good
        else:
            base = None  # fall back

    if not base:
        # Fallback: newest raw .txt (exclude _calibrated)
        txt_files = glob.glob(os.path.join(output_dir, '*.txt'))
        raw_txt = [f for f in txt_files if '_calibrated' not in f]
        if not raw_txt:
            return None
        base = os.path.splitext(os.path.basename(raw_txt[0]))[0]

    result = {}
    for ext in ('.txt', '.srt', '.vtt', '.json'):
        candidate = os.path.join(output_dir, base + ext)
        if os.path.exists(candidate):
            result[ext.lstrip('.')] = candidate
    return result if result else None


def run_pipeline(url, model='sensevoice-small', language='zh', output_dir=None,
                 calibrate=False, skip_download=False, skip_transcribe=False,
                 save_video=False, video_quality='best', backend='auto'):
    """Execute the pipeline: download -> transcribe -> calibrate.

    Args:
        url: Video URL
        model: Whisper model size
        language: Language code
        output_dir: Output directory
        calibrate: Run calibrate.py after transcription
        skip_download: Reuse existing .m4a in output_dir
        skip_transcribe: Reuse existing transcript files in output_dir
        save_video: Also download and save the full video (.mp4)
        video_quality: Video quality preset (best/2160/1440/1080/720/480/360)
                       or raw yt-dlp format string. Default: 'best'.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)

    from download_audio import download_audio, download_video
    from transcribe import transcribe, detect_backends

    if output_dir is None:
        output_dir = os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    audio_path = None
    video_path = None
    result = None

    # ---- Step 1: Audio + optional Video ----
    if skip_download or save_video:
        cached = find_artifacts_in_dir(output_dir, url) or {}

    if skip_download:
        audio_path = cached.get('m4a')
        if audio_path and os.path.exists(audio_path):
            print(f'[SKIP] Audio reuse: {audio_path}')
            if save_video:
                video_path = cached.get('mp4')
                if video_path and os.path.exists(video_path):
                    print(f'[SKIP] Video reuse: {video_path}')
        if not audio_path:
            print('[WARN] --skip-download but no .m4a found, downloading instead')
            skip_download = False

    if not skip_download:
        print('=' * 60)
        print('Step 1: Download Audio' + (' + Video' if save_video else ''))
        print('=' * 60)
        audio_path = download_audio(url, output_dir)
        if not audio_path:
            print('[FAILED] Audio download failed.')
            return None
        if save_video:
            video_path = download_video(url, output_dir, quality=video_quality)
            if video_path:
                print(f'[OK] Video saved: {video_path}')
            else:
                print('[WARN] Video download failed (audio OK, continuing...)')
        print()

    # ---- Step 2: Transcription ----
    if skip_transcribe:
        result = find_transcript_in_dir(output_dir, audio_path)
        if result and 'txt' in result:
            print(f'[SKIP] Transcript reuse: {result["txt"]}')
            for fmt, path in result.items():
                print(f'  {fmt.upper()}: {path}')
        else:
            print('[WARN] --skip-transcribe but no .txt found, transcribing instead')
            skip_transcribe = False

    if not skip_transcribe:
        print('=' * 60)
        print('Step 2: ASR Transcription')
        print('=' * 60)
        result = transcribe(
            audio_path,
            model=model,
            language=language,
            output_dir=output_dir,
            output_format='all',
            backend=backend,
        )
        if not result:
            print('[FAILED] Transcription failed.')
            return None
        print()

    # ---- Step 3: Calibration ----
    if calibrate:
        print('=' * 60)
        print('Step 3: Rule-Based Calibration')
        print('=' * 60)
        try:
            from calibrate import calibrate_text
            txt_path = result.get('txt')
            if txt_path:
                calibrated = calibrate_text(txt_path)
                if calibrated:
                    result['calibrated_txt'] = calibrated
        except Exception as e:
            print(f'[WARN] Calibration skipped: {e}')
        print()

    # ---- Summary ----
    print('=' * 60)
    print('Pipeline Complete')
    print('=' * 60)
    print(f'  Audio:   {audio_path}')
    if video_path:
        print(f'  Video:   {video_path}')
    for fmt, path in result.items():
        print(f'  {fmt.upper()}: {path}')

    return {
        'audio': audio_path,
        'video': video_path,
        'transcripts': result,
        'model': model,
        'language': language,
    }


def main():
    parser = argparse.ArgumentParser(
        description='Video Subtitle Extractor - Full Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
Examples:
  # Full pipeline (download + transcribe)
  python run.py https://b23.tv/xxxxx --model medium --output-dir ./out

  # Reuse audio, re-transcribe (e.g. change model or language)
  python run.py https://b23.tv/xxxxx --skip-download

  # Reuse everything, just regenerate metadata
  python run.py https://b23.tv/xxxxx --skip-download --skip-transcribe

  # Full pipeline + run rule-based calibration
  python run.py https://b23.tv/xxxxx --calibrate

  # Save video as middleware (for later reuse)
  python run.py https://b23.tv/xxxxx --save-video --calibrate

  # Save video at 1080p
  python run.py https://b23.tv/xxxxx --save-video --video-quality 1080
        """
    )
    parser.add_argument('url', help='Video URL (Bilibili, Xiaohongshu, YouTube, etc.)')
    parser.add_argument('--model', default='sensevoice-small',
                        help='Model name. Presets: sensevoice-small, medium-q5_1, '
                             'medium, large-v3. See transcribe.py --help for full list.')
    parser.add_argument('--language', default='zh',
                        help='Language code (default: zh)')
    parser.add_argument('--output-dir', '-o', default=None,
                        help='Output directory (default: current)')
    parser.add_argument('--skip-download', action='store_true',
                        help='Reuse existing .m4a in output_dir instead of re-downloading')
    parser.add_argument('--skip-transcribe', action='store_true',
                        help='Reuse existing transcript files in output_dir instead of re-transcribing')
    parser.add_argument('--calibrate', action='store_true',
                        help='Run rule-based calibration after transcription')
    parser.add_argument('--save-video', action='store_true',
                        help='Also download and save the full video file (.mp4)')
    parser.add_argument('--video-quality', default='best',
                        help='Video quality: best, 2160, 1440, 1080, 720, 480, 360, '
                             'or a raw yt-dlp format string (default: best)')
    parser.add_argument('--backend', default='auto',
                        choices=['auto', 'sensevoice', 'whispercpp', 'openai'],
                        help='ASR backend (default: auto = best available)')
    parser.add_argument('--check-deps', action='store_true',
                        help='Check dependencies without running')

    args = parser.parse_args()

    if args.check_deps:
        ok = ensure_deps()
        sys.exit(0 if ok else 1)

    if not ensure_deps():
        sys.exit(1)

    # Sanity check
    if args.skip_download and args.skip_transcribe and not args.calibrate:
        print('[WARN] Both --skip-download and --skip-transcribe set with no --calibrate.')
        print('      Nothing to do. Use --calibrate to re-run metadata/summary.')
        sys.exit(0)

    result = run_pipeline(
        args.url,
        model=args.model,
        language=args.language,
        output_dir=args.output_dir,
        calibrate=args.calibrate,
        skip_download=args.skip_download,
        skip_transcribe=args.skip_transcribe,
        save_video=args.save_video,
        video_quality=args.video_quality,
        backend=args.backend,
    )

    if result:
        meta = {
            'url': args.url,
            'model': args.model,
            'language': args.language,
            'audio_path': result['audio'],
            'video_path': result.get('video'),
            'output_files': result['transcripts'],
        }
        out_dir = args.output_dir or os.getcwd()
        meta_path = os.path.join(out_dir, '_pipeline_meta.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f'\n  Meta:    {meta_path}')
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
