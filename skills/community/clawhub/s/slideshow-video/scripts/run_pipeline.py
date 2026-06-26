#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
GENERATE = SKILL_DIR / 'scripts' / 'generate_slides.py'
EXPORT = SKILL_DIR / 'scripts' / 'export_mp4.py'
RESOLVE = SKILL_DIR / 'scripts' / 'resolve_images.py'


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description='Run slideshow pipeline from a JSON project file.')
    parser.add_argument('project', help='Pipeline JSON file')
    parser.add_argument('--output-root', default='build', help='Root output directory')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite MP4 output if it exists')
    parser.add_argument('--image-source', default='pinterest', choices=['pinterest', 'unsplash', 'openai', 'kie'], help='How to resolve imageQuery values')
    parser.add_argument('--image-size', default=None, help='Image size hint for GPT image generation, for example 1024x1536 or 1536x1024')
    args = parser.parse_args()

    project_path = Path(args.project).expanduser().resolve()
    with open(project_path, 'r', encoding='utf-8') as f:
        project = json.load(f)

    slug = project.get('slug', project_path.stem)
    output_root = Path(args.output_root).expanduser().resolve() / slug
    output_root.mkdir(parents=True, exist_ok=True)
    slides_dir = output_root / 'slides'
    cache_dir = output_root / 'cache'
    resolved_project_path = output_root / 'resolved-project.json'
    video_path = output_root / f'{slug}.mp4'

    resolve_cmd = [
        'python3',
        str(RESOLVE),
        str(project_path),
        '--output',
        str(resolved_project_path),
        '--source',
        str(args.image_source),
    ]
    if args.image_size:
        resolve_cmd.extend(['--image-size', str(args.image_size)])
    run(resolve_cmd)

    with open(resolved_project_path, 'r', encoding='utf-8') as f:
        project = json.load(f)

    run([
        'python3',
        str(GENERATE),
        str(resolved_project_path),
        '--output-dir',
        str(slides_dir),
        '--cache-dir',
        str(cache_dir),
    ])

    if project.get('video', {}).get('enabled', True):
        cmd = [
            'python3',
            str(EXPORT),
            str(slides_dir),
            str(video_path),
            '--seconds-per-slide',
            str(project.get('video', {}).get('secondsPerSlide', 3.0)),
            '--fps',
            str(project.get('video', {}).get('fps', 30)),
        ]
        if project.get('video', {}).get('zoom'):
            cmd.append('--zoom')
        fade = project.get('video', {}).get('fade', 0)
        if fade:
            cmd.extend(['--fade', str(fade)])
        audio = project.get('audio', {}).get('path') or project.get('audio', {}).get('url')
        if audio:
            cmd.extend(['--audio', str(audio)])
            cmd.extend(['--audio-volume', str(project.get('audio', {}).get('volume', 0.22))])
        if args.overwrite:
            cmd.append('--overwrite')
        run(cmd)

    summary = {
        'slug': slug,
        'slidesDir': str(slides_dir),
        'cacheDir': str(cache_dir),
        'resolvedProjectPath': str(resolved_project_path),
        'videoPath': str(video_path) if project.get('video', {}).get('enabled', True) else None,
        'audio': project.get('audio'),
        'caption': project.get('caption'),
        'hashtags': project.get('hashtags', []),
        'imageSource': args.image_source,
        'imageSize': args.image_size,
    }
    with open(output_root / 'summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
