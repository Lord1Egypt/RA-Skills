#!/usr/bin/env python3
import argparse
import json
import subprocess
import tempfile
import textwrap
from pathlib import Path


CANVAS_W = 1080
CANVAS_H = 1920


def write_text_image(text: str, width: int, fontsize: int, line_spacing: int, boxcolor: str, boxborderw: int, out: Path):
    wrapped = '\n'.join(textwrap.wrap(text.strip(), width=width)) if text.strip() else ''
    if not wrapped:
        return False
    txt = out.with_suffix('.txt')
    txt.write_text(wrapped)
    vf = (
        'format=rgba,'
        f"drawtext=textfile='{txt}':reload=0:fontcolor=white:fontsize={fontsize}:line_spacing={line_spacing}:"
        f"x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor={boxcolor}:boxborderw={boxborderw}"
    )
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', f'color=c=black@0.0:s={CANVAS_W}x{CANVAS_H}:d=1,format=rgba',
        '-frames:v', '1', '-update', '1', '-vf', vf, str(out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True


def build_scene_clip(bg_image: Path, title: str, subtitle: str, duration: float, out: Path, work: Path, idx: int):
    title_png = work / f'title-{idx}.png'
    subtitle_png = work / f'subtitle-{idx}.png'
    has_title = write_text_image(title, 20, 54, 8, 'black@0.22', 16, title_png)
    has_subtitle = write_text_image(subtitle, 28, 34, 6, 'black@0.45', 14, subtitle_png)

    cmd = ['ffmpeg', '-y', '-loop', '1', '-i', str(bg_image)]
    title_input = None
    sub_input = None
    next_idx = 1
    if has_title:
        cmd += ['-loop', '1', '-i', str(title_png)]
        title_input = next_idx
        next_idx += 1
    if has_subtitle:
        cmd += ['-loop', '1', '-i', str(subtitle_png)]
        sub_input = next_idx
        next_idx += 1

    filter_parts = [
        f'[0:v]scale={CANVAS_W}:{CANVAS_H}:force_original_aspect_ratio=increase,'
        f'crop={CANVAS_W}:{CANVAS_H},'
        'eq=brightness=-0.04:saturation=1.15,format=rgba[bg]'
    ]

    current = 'bg'
    if title_input is not None:
        filter_parts.append(f'[{title_input}:v]format=rgba[title]')
        filter_parts.append(f'[{current}][title]overlay=0:-120:format=auto[tmp_title]')
        current = 'tmp_title'
    if sub_input is not None:
        filter_parts.append(f'[{sub_input}:v]format=rgba[sub]')
        filter_parts.append(f'[{current}][sub]overlay=0:240:format=auto[outv]')
        current = 'outv'
    else:
        filter_parts.append(f'[{current}]copy[outv]')

    cmd += [
        '-t', str(duration),
        '-filter_complex', ';'.join(filter_parts),
        '-map', '[outv]',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '28',
        '-pix_fmt', 'yuv420p',
        str(out)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser(description='Create a more visual vertical reel preview from scene JSON')
    ap.add_argument('--scenes-json', required=True, help='JSON array of scenes with bg,title,subtitle')
    ap.add_argument('--output', required=True)
    ap.add_argument('--scene-duration', type=float, default=5.0)
    args = ap.parse_args()

    scenes = json.loads(Path(args.scenes_json).read_text())
    work = Path(tempfile.mkdtemp(prefix='reelsmith-visual-'))
    clips = []

    for i, scene in enumerate(scenes, 1):
        clip = work / f'scene-{i}.mp4'
        build_scene_clip(
            Path(scene['bg']),
            scene.get('title', ''),
            scene.get('subtitle', ''),
            float(scene.get('duration', args.scene_duration)),
            clip,
            work,
            i,
        )
        clips.append(clip)

    concat = work / 'concat.txt'
    concat.write_text(''.join([f"file '{c}'\n" for c in clips]))
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat), '-c', 'copy', args.output
    ], check=True)
    print(args.output)


if __name__ == '__main__':
    main()
