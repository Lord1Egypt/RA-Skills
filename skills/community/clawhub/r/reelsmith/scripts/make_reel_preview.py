#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
import textwrap
from pathlib import Path


def wrap_scene(text: str, width: int = 18) -> str:
    parts = []
    for block in text.splitlines():
        block = block.strip()
        if not block:
            continue
        parts.extend(textwrap.wrap(block, width=width) or [''])
    return '\n'.join(parts)


def main():
    ap = argparse.ArgumentParser(description='Create a simple vertical reel preview from scene text cards')
    ap.add_argument('--title', required=True)
    ap.add_argument('--scenes-file', required=True, help='Text file with one scene per paragraph')
    ap.add_argument('--output', required=True)
    ap.add_argument('--scene-duration', type=float, default=4.8)
    args = ap.parse_args()

    scenes = [s.strip() for s in Path(args.scenes_file).read_text().split('\n\n') if s.strip()]
    work = Path(tempfile.mkdtemp(prefix='reelsmith-'))
    clips = []

    for i, scene in enumerate(scenes, 1):
        img = work / f'scene-{i}.png'
        clip = work / f'scene-{i}.mp4'
        txt = work / f'scene-{i}.txt'
        txt.write_text(wrap_scene(scene, width=18))
        draw = (
            f"drawtext=textfile='{txt}':reload=0"
            f":fontcolor=white:fontsize=38"
            f":line_spacing=12"
            f":x=(w-text_w)/2:y=(h-text_h)/2"
            f":box=1:boxcolor=black@0.55:boxborderw=34"
        )
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi', '-i', f'color=c=black:s=1080x1920:d={args.scene_duration}',
            '-vf', draw,
            '-frames:v', '1', str(img)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([
            'ffmpeg', '-y', '-loop', '1', '-i', str(img), '-t', str(args.scene_duration), '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', str(clip)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips.append(clip)

    concat = work / 'concat.txt'
    concat.write_text(''.join([f"file '{c}'\n" for c in clips]))
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat), '-c', 'copy', args.output], check=True)
    print(args.output)


if __name__ == '__main__':
    main()
