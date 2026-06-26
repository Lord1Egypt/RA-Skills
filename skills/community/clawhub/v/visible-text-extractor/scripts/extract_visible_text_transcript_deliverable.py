#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXTRACT = BASE_DIR / 'scripts' / 'extract_visible_text.py'
TRANSCRIPT = BASE_DIR / 'scripts' / 'build_fulltext_transcript.py'
DOCX = BASE_DIR / 'scripts' / 'build_transcript_docx.js'


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit((p.stderr or p.stdout or 'command failed').strip())
    return p.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url')
    ap.add_argument('--output-prefix', required=True)
    ap.add_argument('--ocr-images', action='store_true')
    ap.add_argument('--browser-fallback', action='store_true')
    ap.add_argument('--page-screenshot-ocr', action='store_true')
    ap.add_argument('--dedupe', action='store_true')
    ap.add_argument('--title-override')
    args = ap.parse_args()

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    raw_json = str(prefix) + '.raw.json'
    transcript_md = str(prefix) + '.transcript.md'
    final_docx = str(prefix) + '.docx'

    cmd = ['python3', str(EXTRACT), '--format', 'json', '--output', raw_json]
    if args.url:
        cmd += ['--url', args.url]
    if args.ocr_images:
        cmd.append('--ocr-images')
    if args.browser_fallback:
        cmd.append('--browser-fallback')
    if args.page_screenshot_ocr:
        cmd.append('--page-screenshot-ocr')
    if args.dedupe:
        cmd.append('--dedupe')
    run(cmd)

    raw = json.loads(Path(raw_json).read_text(encoding='utf-8'))
    title = args.title_override or raw.get('page', {}).get('title', '')

    run([
        'python3', str(TRANSCRIPT),
        '--input-json', raw_json,
        '--title', title,
        '--output-markdown', transcript_md,
    ])

    run(['node', str(DOCX), transcript_md, final_docx])

    print(json.dumps({
        'ok': True,
        'raw_json': raw_json,
        'transcript_markdown': transcript_md,
        'docx': final_docx,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
