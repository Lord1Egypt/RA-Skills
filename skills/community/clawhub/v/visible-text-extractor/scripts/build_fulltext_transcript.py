#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-json', required=True)
    ap.add_argument('--title', default='')
    ap.add_argument('--output-markdown', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding='utf-8'))
    title = args.title or data.get('page', {}).get('title', '')

    parts = []
    if title:
        parts.append(f'# {title}')
        parts.append('')

    body = (data.get('body_text') or '').strip()
    if body:
        parts.append('## 正文')
        parts.append(body)
        parts.append('')

    images = data.get('images') or []
    visible_idx = 1
    for img in images:
        text = (img.get('ocr_text') or '').strip()
        if not text:
            continue
        parts.append(f'## 图片 {visible_idx}')
        parts.append(text)
        parts.append('')
        visible_idx += 1

    gifs = data.get('gifs') or []
    for gif in gifs:
        text = (gif.get('deduped_text') or '').strip()
        if not text:
            continue
        parts.append(f'## GIF {visible_idx}')
        parts.append(text)
        parts.append('')
        visible_idx += 1

    out = '\n'.join(parts).strip() + '\n'
    Path(args.output_markdown).write_text(out, encoding='utf-8')
    print(args.output_markdown)


if __name__ == '__main__':
    main()
