#!/usr/bin/env python3
"""Video Subtitle Extractor - Audio Downloader

Downloads audio from video URLs using yt-dlp.
Supports Bilibili, YouTube, and all yt-dlp compatible platforms.
"""

import subprocess
import sys
import os
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


def find_ffmpeg():
    """Find ffmpeg executable path."""
    path = shutil.which('ffmpeg')
    if path:
        return path
    for p in FFMPEG_WIN_PATHS:
        if os.path.isfile(p):
            return p
    return None


def find_yt_dlp():
    """Find yt-dlp executable path."""
    yt_dlp = shutil.which('yt-dlp')
    if yt_dlp:
        return yt_dlp
    # Try python module path
    try:
        import yt_dlp
        return yt_dlp.__file__
    except ImportError:
        pass
    return None


# Quality presets → yt-dlp format selectors
# Uses height<= filters so it gracefully falls back if the target isn't available
VIDEO_QUALITY_PRESETS = {
    'best': 'bestvideo+bestaudio/best',
    '2160': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
    '1440': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
    '1080': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    '720': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    '480': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
    '360': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
}


def _build_video_format(quality):
    """Build yt-dlp -f selector from a quality preset or raw string.

    Recognised presets: best, 2160, 1440, 1080, 720, 480, 360.
    Anything else is passed through as a raw yt-dlp format expression.
    """
    q = str(quality).strip().lower()
    if q in VIDEO_QUALITY_PRESETS:
        return VIDEO_QUALITY_PRESETS[q]
    # Raw passthrough (e.g. 'bestvideo[height<=720]+bestaudio')
    return quality


def download_video(url, output_dir=None, filename=None, quality='best'):
    """Download video+audio from a video URL.

    Args:
        url: Video URL (Bilibili, YouTube, etc.)
        output_dir: Output directory (default: current dir)
        filename: Custom output filename without extension
                  (default: derived from yt-dlp title)
        quality: Video quality preset or yt-dlp format string.
                 Presets: best, 2160, 1440, 1080, 720, 480, 360.
                 Default: 'best' (highest available).
                 Note: higher presets gracefully fall back to the best
                 available under that height limit.

    Returns:
        Path to downloaded video file, or None on failure.
    """
    if output_dir is None:
        output_dir = os.getcwd()

    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
    if filename:
        output_template = os.path.join(output_dir, f'{filename}.%(ext)s')

    fmt = _build_video_format(quality)
    cmd = [
        sys.executable, '-m', 'yt_dlp',
        '-f', fmt,
        '--merge-output-format', 'mp4',
        '--no-playlist',
        '--no-warnings',
        '-o', output_template,
    ]

    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        cmd.extend(['--ffmpeg-location', ffmpeg_dir])

    cmd.append(url)

    preset_label = VIDEO_QUALITY_PRESETS.get(str(quality).strip().lower())
    qlabel = quality if preset_label else 'custom'
    print(f'Downloading video from: {url}')
    print(f'Quality: {qlabel} | Output: {output_dir}')
    print()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        dest = None
        for line in result.stdout.splitlines():
            if 'Destination:' in line:
                dest = line.split('Destination:')[1].strip()
                break
            if 'has already been downloaded' in line:
                for l in result.stdout.splitlines():
                    if output_dir in l and not l.startswith('['):
                        cand = l.strip()
                        if cand.endswith('.mp4'):
                            dest = cand
                            break
                break
            if 'Merging formats into' in line:
                continue  # merging is normal, not an error

        # Fallback: find mp4 files in output dir
        if not dest or not os.path.exists(dest):
            mp4_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
            if mp4_files:
                latest = max(mp4_files, key=lambda f: os.path.getmtime(
                    os.path.join(output_dir, f)))
                dest = os.path.join(output_dir, latest)

        if dest and os.path.exists(dest) and os.path.getsize(dest) > 0:
            if result.returncode != 0:
                print(f'[WARN] yt-dlp exit code {result.returncode} (non-fatal)')
            print(f'[OK] Video saved: {dest}')
            return dest

        if result.returncode != 0:
            if result.stderr:
                print('yt-dlp stderr:', result.stderr[:500])
            print(f'[ERROR] yt-dlp video download failed with code {result.returncode}')
            return None

        print('[ERROR] Could not locate output video file')
        return None

    except subprocess.TimeoutExpired:
        print('[ERROR] Video download timed out (>10 minutes)')
        return None
    except Exception as e:
        print(f'[ERROR] {e}')
        return None


def download_audio(url, output_dir=None, filename=None):
    """Download best audio from a video URL.

    Args:
        url: Video URL (Bilibili, YouTube, etc.)
        output_dir: Output directory (default: current dir or system temp)
        filename: Custom output filename without extension
                   (default: derived from yt-dlp title)

    Returns:
        Path to downloaded audio file, or None on failure.
    """
    if output_dir is None:
        output_dir = os.getcwd()

    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
    if filename:
        output_template = os.path.join(output_dir, f'{filename}.%(ext)s')

    # yt-dlp command: best audio only, m4a format preferred
    cmd = [
        sys.executable, '-m', 'yt_dlp',
        '-f', 'bestaudio[ext=m4a]/bestaudio/best',
        '--extract-audio',
        '--audio-format', 'm4a',
        '--no-playlist',
        '--no-warnings',
        '-o', output_template,
    ]

    # Add ffmpeg location if found (needed for post-processing on Windows)
    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        cmd.extend(['--ffmpeg-location', ffmpeg_dir])

    cmd.append(url)

    print(f'Downloading audio from: {url}')
    print(f'Output directory: {output_dir}')
    print()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        combined_output = (result.stdout or '') + (result.stderr or '')

        # First try to find the output file from the output
        dest = None
        for line in result.stdout.splitlines():
            if 'Destination:' in line:
                dest = line.split('Destination:')[1].strip()
                break
            if 'has already been downloaded' in line:
                for l in result.stdout.splitlines():
                    if output_dir in l and not l.startswith('['):
                        dest = l.strip()
                        break

        # Fallback: find m4a files in output dir
        if not dest or not os.path.exists(dest):
            m4a_files = [f for f in os.listdir(output_dir) if f.endswith('.m4a')]
            if m4a_files:
                latest = max(m4a_files, key=lambda f: os.path.getmtime(
                    os.path.join(output_dir, f)))
                dest = os.path.join(output_dir, latest)

        # If we found a valid file, return it even if yt-dlp reported errors
        if dest and os.path.exists(dest) and os.path.getsize(dest) > 0:
            if result.returncode != 0:
                print(f'[WARN] yt-dlp exit code {result.returncode} (non-fatal)')
            print(f'[OK] Audio saved: {dest}')
            return dest

        if result.returncode != 0:
            # Print errors for debugging
            if result.stderr:
                print('yt-dlp stderr:', result.stderr[:500])
            print(f'[ERROR] yt-dlp failed with code {result.returncode}')
            return None

        print('[ERROR] Could not locate output file')
        return None

    except subprocess.TimeoutExpired:
        print('[ERROR] Download timed out (>5 minutes)')
        return None
    except Exception as e:
        print(f'[ERROR] {e}')
        return None


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Download audio (or video) from a video URL'
    )
    parser.add_argument('url', help='Video URL (Bilibili, YouTube, etc.)')
    parser.add_argument('output_dir', nargs='?', default=None,
                        help='Output directory (default: current)')
    parser.add_argument('filename', nargs='?', default=None,
                        help='Custom filename (without extension)')
    parser.add_argument('--save-video', action='store_true',
                        help='Also download the full video file (.mp4)')
    parser.add_argument('--video-quality', default='best',
                        help='Video quality: best, 2160, 1440, 1080, 720, 480, 360, '
                             'or a raw yt-dlp format string (default: best)')

    args = parser.parse_args()

    # Always download audio (needed for ASR)
    audio = download_audio(args.url, args.output_dir, args.filename)

    video = None
    if args.save_video:
        video = download_video(args.url, args.output_dir, args.filename,
                               quality=args.video_quality)

    if audio or video:
        if audio:
            print(audio)
        if video:
            print(video)
        sys.exit(0)
    else:
        sys.exit(1)