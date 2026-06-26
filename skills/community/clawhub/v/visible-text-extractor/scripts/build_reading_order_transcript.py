#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def normalize_lines(text: str):
    return [x.strip() for x in (text or '').replace('\r', '\n').splitlines() if x.strip()]


def split_body_chunks(text: str):
    blocks = []
    current = []
    for line in (text or '').replace('\r', '\n').splitlines():
        s = line.strip()
        if not s:
            if current:
                blocks.append('\n'.join(current).strip())
                current = []
            continue
        current.append(s)
    if current:
        blocks.append('\n'.join(current).strip())
    return [b for b in blocks if b]


def looks_credit_block(block: str):
    keys = ['来源：', '文字：', '编辑：', '初审：', '审核：', '审核发布：']
    hit = sum(1 for k in keys if k in block)
    return hit >= 2


def choose_intro_count(body_chunks, image_count):
    if not body_chunks:
        return 0
    if len(body_chunks) == 1:
        return 1
    intro = 0
    for idx, block in enumerate(body_chunks):
        if idx == len(body_chunks) - 1 and looks_credit_block(block):
            break
        intro += 1
        if intro >= 2:
            break
    return max(1, intro)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-json', required=True)
    ap.add_argument('--title', default='')
    ap.add_argument('--output-markdown', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding='utf-8'))
    title = args.title or data.get('page', {}).get('title', '')
    body_chunks = split_body_chunks(data.get('body_text', ''))

    image_texts = []
    for img in data.get('images') or []:
        text = (img.get('ocr_text') or '').strip()
        if text:
            image_texts.append(text)
    for gif in data.get('gifs') or []:
        text = (gif.get('deduped_text') or '').strip()
        if text:
            image_texts.append(text)

    intro_count = choose_intro_count(body_chunks, len(image_texts))
    intro_chunks = body_chunks[:intro_count]
    tail_chunks = body_chunks[intro_count:]

    parts = []
    if title:
        parts.append(f'# {title}')
        parts.append('')

    for block in intro_chunks:
        parts.append(block)
        parts.append('')

    for idx, text in enumerate(image_texts, 1):
        parts.append(f'## 图片 {idx}')
        parts.append(text)
        parts.append('')

    for block in tail_chunks:
        parts.append(block)
        parts.append('')

    out = '\n'.join(parts).strip() + '\n'
    Path(args.output_markdown).write_text(out, encoding='utf-8')
    print(args.output_markdown)


if __name__ == '__main__':
    main()
