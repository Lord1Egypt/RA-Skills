#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ], text=True).strip()
    return float(out)


def main():
    parser = argparse.ArgumentParser(description='Export slideshow PNGs to MP4 with per-slide sync durations.')
    parser.add_argument('input_dir', help='Directory containing slide PNGs')
    parser.add_argument('audio_dir', help='Directory containing ordered per-line audio files')
    parser.add_argument('output', help='Output MP4 path')
    parser.add_argument('--glob', default='slide_*.png', help='Glob for slide images inside input_dir')
    parser.add_argument('--audio-glob', default='line_*.mp3', help='Glob for ordered line audio files')
    parser.add_argument('--fps', type=int, default=30, help='Output video FPS')
    parser.add_argument('--padding', type=float, default=0.18, help='Extra hold time added to each slide in seconds')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing output')
    args = parser.parse_args()

    input_dir = Path(args.input_dir).expanduser().resolve()
    audio_dir = Path(args.audio_dir).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    slides = sorted(input_dir.glob(args.glob))
    audios = sorted(audio_dir.glob(args.audio_glob))
    if not slides:
        raise SystemExit(f'No slides matched {args.glob} in {input_dir}')
    if len(slides) != len(audios):
        raise SystemExit(f'Slide/audio count mismatch: {len(slides)} slides vs {len(audios)} audio files')

    work_dir = output.parent
    work_dir.mkdir(parents=True, exist_ok=True)
    audio_concat = work_dir / f'{output.stem}.audio.concat.txt'
    video_concat = work_dir / f'{output.stem}.video.concat.txt'
    merged_audio = work_dir / f'{output.stem}.voice.mp3'
    sync_json = work_dir / f'{output.stem}.sync.json'

    durations = []
    with audio_concat.open('w', encoding='utf-8') as fa, video_concat.open('w', encoding='utf-8') as fv:
        for slide, audio in zip(slides, audios):
            fa.write(f"file '{audio.as_posix()}'\n")
            duration = ffprobe_duration(audio) + args.padding
            durations.append({
                'slide': slide.name,
                'audio': audio.name,
                'durationSeconds': round(duration, 3),
            })
            fv.write(f"file '{slide.as_posix()}'\n")
            fv.write(f'duration {duration:.3f}\n')
        fv.write(f"file '{slides[-1].as_posix()}'\n")

    subprocess.run([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-f', 'concat', '-safe', '0', '-i', str(audio_concat),
        '-c:a', 'libmp3lame', '-q:a', '2', str(merged_audio)
    ], check=True)

    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error',
        '-f', 'concat', '-safe', '0', '-i', str(video_concat),
        '-i', str(merged_audio),
        '-vf', f'fps={args.fps},scale=1080:1920,format=yuv420p',
        '-r', str(args.fps),
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-shortest',
        str(output),
    ]
    if args.overwrite:
        cmd.insert(1, '-y')
    subprocess.run(cmd, check=True)

    sync_json.write_text(json.dumps({
        'slides': durations,
        'mergedAudioPath': str(merged_audio),
        'outputPath': str(output),
        'totalDurationSeconds': round(sum(item['durationSeconds'] for item in durations), 3),
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✓ {output}')
    print(str(sync_json))


if __name__ == '__main__':
    main()
