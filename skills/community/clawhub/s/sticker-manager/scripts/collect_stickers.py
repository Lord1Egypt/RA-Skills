#!/usr/bin/env python3
"""Batch collector for stickers from URLs or local files."""
from __future__ import annotations
import argparse
import hashlib
import io
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image, ImageSequence

from common import get_lang, SUPPORTED_EXTS, build_vision_plan

DEFAULT_TARGET_COUNT = 15
DEFAULT_MIN_BYTES = 10 * 1024
DEFAULT_WORKERS = 1
DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com/'}
ANIMATED_CONTENT_TYPES = {'image/gif', 'video/mp4', 'video/webm'}


def build_semantic_batch(final_items: list[dict], lang: str) -> dict:
    return {
        'task': 'After collection, analyze each selected sticker image for meaning, emotion, scene, and suitable reaction use.',
        'language': lang,
        'items': [
            {
                'name': item['name'],
                'path': item['path'],
                'vision_plan': build_vision_plan(item['path'], 'Describe sticker meaning, emotion, scene, and reaction use.', lang),
            }
            for item in final_items
        ],
    }


def infer_extension(source: str, fallback: str = '.bin', content_type: str | None = None) -> str:
    parsed = urlparse(source)
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext in SUPPORTED_EXTS:
        return ext
    local_ext = os.path.splitext(source)[1].lower()
    if local_ext in SUPPORTED_EXTS:
        return local_ext
    content_type = (content_type or '').lower()
    if 'gif' in content_type:
        return '.gif'
    if 'webp' in content_type:
        return '.webp'
    if 'png' in content_type:
        return '.png'
    if 'jpeg' in content_type or 'jpg' in content_type:
        return '.jpg'
    return fallback


def is_animated_bytes(data: bytes, content_type: str | None = None) -> bool:
    content_type = (content_type or '').lower().split(';', 1)[0].strip()
    if content_type in ANIMATED_CONTENT_TYPES:
        return True
    if data.startswith((b'GIF87a', b'GIF89a')):
        try:
            with Image.open(io.BytesIO(data)) as img:
                return bool(getattr(img, 'is_animated', False) or getattr(img, 'n_frames', 1) > 1)
        except Exception:
            return True
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        try:
            with Image.open(io.BytesIO(data)) as img:
                return bool(getattr(img, 'is_animated', False) or getattr(img, 'n_frames', 1) > 1)
        except Exception:
            return b'ANIM' in data[:256]
    return False


def is_probably_animated_reference(source: str, content_type: str | None = None) -> bool:
    lowered = source.lower()
    ext = os.path.splitext(urlparse(lowered).path)[1]
    if ext == '.gif':
        return True
    if ext in {'.mp4', '.webm'}:
        return True
    content_type = (content_type or '').lower().split(';', 1)[0].strip()
    return content_type in ANIMATED_CONTENT_TYPES


def resolve_remote_source(source: str) -> tuple[str, str | None, dict]:
    """Resolve remote pages to the best downloadable media URL.

    Generic rule: prefer animated assets whenever the reference or the fetched
    resource indicates animation. Static previews are fallback-only.
    """
    meta = {'resolved_from': source, 'animated_preferred': False, 'resolver': 'direct'}
    if not (source.startswith('http://') or source.startswith('https://')):
        return source, None, meta

    parsed = urlparse(source)
    direct_ext = os.path.splitext(parsed.path)[1].lower()
    if direct_ext in SUPPORTED_EXTS:
        return source, None, meta

    host = parsed.netloc.lower()
    if 'giphy.com' not in host:
        return source, None, meta

    response = requests.get(source, headers=DEFAULT_HEADERS, timeout=30)
    response.raise_for_status()
    html = response.text

    matches = re.findall(r'https://media\d*\.giphy\.com/(?:media|stickers)/[^"\'\s<]+', html)
    normalized = []
    for item in matches:
        item = item.replace('\\u002F', '/').replace('\\/', '/')
        if item not in normalized:
            normalized.append(item)

    def pick_variant(suffixes: list[str]) -> str | None:
        for item in normalized:
            for suffix in suffixes:
                if item.endswith(suffix):
                    return item
        return None

    gif_url = pick_variant(['giphy.gif'])
    webp_url = pick_variant(['giphy.webp'])
    png_url = pick_variant(['giphy.png'])

    if gif_url:
        meta['animated_preferred'] = True
        meta['resolver'] = 'giphy-page'
        return gif_url, '.gif', meta
    if webp_url:
        meta['resolver'] = 'giphy-page'
        return webp_url, '.webp', meta
    if png_url:
        meta['resolver'] = 'giphy-page'
        return png_url, '.png', meta

    media_base = next((item for item in normalized if '/media/' in item or '/stickers/' in item), None)
    if media_base:
        meta['resolver'] = 'giphy-page'
        meta['animated_preferred'] = True
        return media_base.rstrip('/') + '/giphy.gif', '.gif', meta

    return source, None, meta


def load_sources(args_sources: list[str], sources_file: str | None) -> list[str]:
    values = list(args_sources)
    if sources_file:
        for line in Path(sources_file).read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                values.append(line)
    return values


def read_bytes(source: str) -> tuple[bytes, str | None, str, dict]:
    if source.startswith('http://') or source.startswith('https://'):
        resolved_source, forced_ext, meta = resolve_remote_source(source)
        r = requests.get(resolved_source, headers=DEFAULT_HEADERS, timeout=30)
        r.raise_for_status()
        content_type = r.headers.get('Content-Type')
        meta['animated_detected'] = is_animated_bytes(r.content, content_type)
        meta['animation_reference'] = is_probably_animated_reference(resolved_source, content_type)
        return r.content, content_type, forced_ext or resolved_source, meta
    data = Path(source).read_bytes()
    meta = {
        'resolved_from': source,
        'animated_preferred': False,
        'resolver': 'local',
        'animated_detected': is_animated_bytes(data, None),
        'animation_reference': is_probably_animated_reference(source, None),
    }
    return data, None, source, meta


def collect_one(item: tuple[int, str], prefix: str, out_dir: Path, min_bytes: int) -> dict:
    idx, source = item
    data, content_type, resolved_hint, meta = read_bytes(source)
    size = len(data)
    if size < min_bytes:
        return {'source': source, 'status': 'low_quality', 'size': size, 'content_type': content_type, **meta}

    animation_reference = bool(meta.get('animation_reference'))
    animated_detected = bool(meta.get('animated_detected'))
    if animation_reference and not animated_detected:
        return {
            'source': source,
            'status': 'static_fallback_rejected',
            'size': size,
            'content_type': content_type,
            **meta,
        }

    ext = infer_extension(resolved_hint, '.gif', content_type)
    digest = hashlib.md5(data).hexdigest()
    name = f'{prefix}_{idx:02d}{ext}'
    path = out_dir / name
    path.write_bytes(data)
    return {
        'source': source,
        'status': 'saved',
        'size': size,
        'hash': digest,
        'path': str(path),
        'name': name,
        'content_type': content_type,
        **meta,
    }


def dedupe_saved(results: list[dict]) -> tuple[list[dict], list[dict]]:
    seen = {}
    keep = []
    dropped = []
    for item in results:
        if item.get('status') != 'saved':
            continue
        digest = item['hash']
        if digest in seen:
            Path(item['path']).unlink(missing_ok=True)
            item['status'] = 'duplicate'
            dropped.append(item)
        else:
            seen[digest] = item['path']
            keep.append(item)
    return keep, dropped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('sources', nargs='*')
    parser.add_argument('--sources-file')
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--prefix', default='sticker')
    parser.add_argument('--target-count', type=int, default=DEFAULT_TARGET_COUNT)
    parser.add_argument('--min-bytes', type=int, default=DEFAULT_MIN_BYTES)
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS, help='Deprecated. Collector now runs in single-thread mode; values other than 1 are ignored.')
    parser.add_argument('--lang')
    parser.add_argument('--no-semantic-plan', action='store_true')
    args = parser.parse_args()

    lang = get_lang(args.lang)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sources = load_sources(args.sources, args.sources_file)
    if not sources:
        print('No sources provided.')
        return 1

    indexed = list(enumerate(sources, start=1))
    results = []
    effective_workers = 1
    if args.workers != 1:
        print(f'WORKERS_IGNORED={args.workers}')
    print(f'EFFECTIVE_WORKERS={effective_workers}')
    for item in indexed:
        results.append(collect_one(item, args.prefix, out_dir, args.min_bytes))

    keep, dropped = dedupe_saved(results)
    low_quality = [r for r in results if r.get('status') == 'low_quality']
    static_fallback_rejected = [r for r in results if r.get('status') == 'static_fallback_rejected']
    kept_sorted = sorted(keep, key=lambda x: x['size'], reverse=True)
    final = kept_sorted[:args.target_count]
    extra = kept_sorted[args.target_count:]
    for item in extra:
        Path(item['path']).unlink(missing_ok=True)
        item['status'] = 'trimmed'

    print(f'TARGET_COUNT={args.target_count}')
    print(f'SAVED_UNIQUE={len(keep)}')
    print(f'LOW_QUALITY={len(low_quality)}')
    print(f'STATIC_FALLBACK_REJECTED={len(static_fallback_rejected)}')
    print(f'DUPLICATES={len(dropped)}')
    print(f'FINAL_COUNT={len(final)}')
    for item in final:
        print(f"KEEP {item['name']} {item['size']}")
    if not args.no_semantic_plan:
        import json
        print('__SEMANTIC_BATCH__:' + json.dumps(build_semantic_batch(final, lang), ensure_ascii=False))
    if len(final) < args.target_count:
        print(f'NEED_MORE={args.target_count - len(final)}')
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
