#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
BUILD = SCRIPT_DIR / 'build_reentry_context.py'
RENDER = SCRIPT_DIR / 'render_continue_reentry.py'
GENERATE_IMAGE = SCRIPT_DIR / 'generate_image.py'
OUTBOUND_YUMFU = Path.home() / '.openclaw' / 'media' / 'outbound' / 'yumfu'


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or 'continue-reentry'


def run_json(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return {
            'success': False,
            'error': proc.stderr.strip() or proc.stdout.strip() or f'command failed ({proc.returncode})',
            'command': cmd,
        }
    stdout = proc.stdout.strip()
    if not stdout:
        return {'success': False, 'error': 'empty stdout', 'command': cmd}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {'success': False, 'error': 'stdout was not valid JSON', 'stdout': stdout, 'command': cmd}


def run_proc(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': proc.returncode == 0,
        'returncode': proc.returncode,
        'stdout': proc.stdout.strip(),
        'stderr': proc.stderr.strip(),
        'command': cmd,
    }


def prepare_image(user_id: str, universe: str, image_prompt: str | None, latest_image_path: str | None) -> dict[str, Any]:
    if latest_image_path and Path(latest_image_path).exists():
        return {
            'generated': True,
            'reused': True,
            'path': latest_image_path,
            'provider': 'existing-yumfu',
        }

    if not image_prompt:
        return {
            'generated': False,
            'reused': False,
            'error': 'no image prompt for continue reentry',
        }

    OUTBOUND_YUMFU.mkdir(parents=True, exist_ok=True)
    filename = OUTBOUND_YUMFU / f"{universe}-user-{user_id}-{slugify('continue-reentry-' + datetime.now().strftime('%Y%m%d-%H%M%S'))}.png"
    result = run_proc([
        'uv', 'run', str(GENERATE_IMAGE),
        '--prompt', image_prompt,
        '--filename', str(filename),
        '--resolution', '1K',
        '--aspect-ratio', '4:5',
    ])
    if result['success'] and filename.exists():
        return {
            'generated': True,
            'reused': False,
            'path': str(filename),
            'provider': 'local-yumfu',
            'stdout': result['stdout'],
        }
    return {
        'generated': False,
        'reused': False,
        'path': str(filename),
        'error': result['stderr'] or result['stdout'] or 'continue reentry image generation failed',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Prepare YumFu continue/reentry delivery assets')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--recent-text', action='append', default=[])
    parser.add_argument('--recent-texts-json', default=None)
    args = parser.parse_args()

    build_cmd = ['python3', str(BUILD), '--user-id', args.user_id, '--universe', args.universe]
    render_cmd = ['python3', str(RENDER), '--user-id', args.user_id, '--universe', args.universe]
    for text in args.recent_text:
        build_cmd.extend(['--recent-text', text])
        render_cmd.extend(['--recent-text', text])
    if args.recent_texts_json:
        build_cmd.extend(['--recent-texts-json', args.recent_texts_json])
        render_cmd.extend(['--recent-texts-json', args.recent_texts_json])

    context = run_json(build_cmd)
    if not context.get('success'):
        print(json.dumps(context, ensure_ascii=False))
        sys.exit(1)

    rendered = run_json(render_cmd)
    if not rendered.get('success'):
        print(json.dumps(rendered, ensure_ascii=False))
        sys.exit(1)

    image = prepare_image(
        user_id=args.user_id,
        universe=args.universe,
        image_prompt=context.get('image_prompt'),
        latest_image_path=rendered.get('latest_image_path'),
    )

    result = {
        'success': True,
        'kind': 'continue-reentry-delivery',
        'user_id': args.user_id,
        'universe': args.universe,
        'target': args.target,
        'preferred_language': rendered.get('preferred_language'),
        'text': rendered.get('text'),
        'image': image,
        'context': context,
        'next_actions': {
            'send_image_with_caption': bool(image.get('generated')),
            'send_text_only_fallback': not bool(image.get('generated')),
            'continue_delivery_requires_image': True,
        },
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
