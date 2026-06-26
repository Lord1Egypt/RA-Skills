#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts')
POST = BASE / 'postprocess_ocr_text.py'
DOCX = BASE / 'build_deliverable_docx.js'
EXTRACT = BASE / 'extract_visible_text.py'
BROWSER = BASE / 'extract_with_browser.js'
FEISHU_SENDER = Path('/root/.openclaw/workspace/skills/feishu-file-sender/scripts/feishu_file_sender.py')

BLOCK_PATTERNS = [
    '环境异常', '完成验证后即可继续访问', '去验证', '访问过于频繁',
    '请在微信客户端打开链接', '账号异常', '内容无法访问'
]


def log(msg):
    print(msg, flush=True)


def run(cmd, stage, allow_empty_stdout=False):
    log(f'[stage] {stage}')
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.stdout.strip():
        print(p.stdout.strip(), flush=True)
    if p.returncode != 0:
        err = (p.stderr or p.stdout or 'command failed').strip()
        raise SystemExit(f'[{stage}] {err}')
    if p.stderr.strip() and not allow_empty_stdout:
        print(p.stderr.strip(), flush=True)
    return p.stdout.strip()


def ensure_exists(path_str, label):
    p = Path(path_str)
    if not p.exists() or p.stat().st_size == 0:
        raise SystemExit(f'[{label}] expected output missing: {p}')
    return p


def looks_blocked(text: str):
    t = (text or '').strip()
    return any(p in t for p in BLOCK_PATTERNS)


def maybe_send_to_feishu(docx_path: Path, receive_id: str):
    if not receive_id:
        return None
    if not FEISHU_SENDER.exists():
        raise SystemExit('[send] feishu sender script not found')
    out = run([
        'python3', str(FEISHU_SENDER),
        '--file', str(docx_path),
        '--receive-id', receive_id,
    ], stage='send-docx')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url')
    ap.add_argument('--html-file')
    ap.add_argument('--image', action='append', default=[])
    ap.add_argument('--image-dir')
    ap.add_argument('--title')
    ap.add_argument('--output-prefix', required=True)
    ap.add_argument('--browser-capture', action='store_true')
    ap.add_argument('--selector')
    ap.add_argument('--wait-ms', type=int, default=5000)
    ap.add_argument('--ocr-images', action='store_true')
    ap.add_argument('--dedupe', action='store_true')
    ap.add_argument('--send-feishu-receive-id')
    ap.add_argument('--fast-fail-on-blocked', action='store_true')
    args = ap.parse_args()

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    raw_json = str(prefix) + '.raw.json'
    clean_json = str(prefix) + '.clean.json'
    clean_md = str(prefix) + '.clean.md'
    final_docx = str(prefix) + '.docx'

    html_file = args.html_file
    shot_file = None
    body_text_override = ''

    if args.browser_capture:
        if not args.url:
            raise SystemExit('--browser-capture requires --url')
        log('[status] starting browser capture')
        if not html_file:
            html_file = tempfile.mktemp(prefix='authorized-capture-', suffix='.html')
        shot_file = tempfile.mktemp(prefix='authorized-capture-', suffix='.png')
        body_txt = tempfile.mktemp(prefix='authorized-capture-', suffix='.txt')
        cmd = [
            'node', str(BROWSER),
            '--url', args.url,
            '--output-html', html_file,
            '--output-shot', shot_file,
            '--output-text', body_txt,
            '--wait-ms', str(args.wait_ms),
        ]
        if args.selector:
            cmd += ['--selector', args.selector]
        run(cmd, stage='browser-capture', allow_empty_stdout=True)
        ensure_exists(html_file, 'browser-capture-html')
        ensure_exists(body_txt, 'browser-capture-text')
        body_text_override = Path(body_txt).read_text(encoding='utf-8', errors='replace').strip()
        log(f'[status] browser visible text length={len(body_text_override)} blocked={looks_blocked(body_text_override)}')
        if shot_file and Path(shot_file).exists():
            args.image.append(shot_file)

    if args.fast_fail_on_blocked and looks_blocked(body_text_override):
        raise SystemExit('[browser-capture] page appears blocked by validation/interstitial; stopping before heavy OCR')

    cmd = ['python3', str(EXTRACT), '--format', 'json', '--output', raw_json]
    if args.url:
        cmd += ['--url', args.url]
    if html_file:
        cmd += ['--html-file', html_file]
    if args.image_dir:
        cmd += ['--image-dir', args.image_dir]
    for img in args.image:
        cmd += ['--image', img]
    if args.ocr_images:
        cmd.append('--ocr-images')
    if args.dedupe:
        cmd.append('--dedupe')
    run(cmd, stage='extract-visible-text')
    ensure_exists(raw_json, 'extract-visible-text-output')

    raw = json.loads(Path(raw_json).read_text(encoding='utf-8'))
    title = args.title or raw.get('page', {}).get('title', '')
    body = body_text_override or raw.get('body_text', '')
    blocked = bool(raw.get('page', {}).get('blocked')) or looks_blocked(body)
    log(f'[status] extracted title={title!r} blocked={blocked} images={len(raw.get("images", []))}')

    run([
        'python3', str(POST),
        '--input-json', raw_json,
        '--title', title,
        '--body-text', body,
        '--output-json', clean_json,
        '--output-markdown', clean_md,
    ], stage='postprocess')
    ensure_exists(clean_json, 'postprocess-json')
    ensure_exists(clean_md, 'postprocess-markdown')

    run(['node', str(DOCX), clean_md, final_docx], stage='build-docx')
    ensure_exists(final_docx, 'build-docx-output')

    send_result = None
    if args.send_feishu_receive_id:
        send_result = maybe_send_to_feishu(Path(final_docx), args.send_feishu_receive_id)

    print(json.dumps({
        'ok': True,
        'raw_json': raw_json,
        'clean_json': clean_json,
        'clean_markdown': clean_md,
        'docx': final_docx,
        'html_file': html_file,
        'screenshot': shot_file,
        'blocked': blocked,
        'sent': bool(send_result),
        'send_result': json.loads(send_result) if send_result else None,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            os._exit(0)
