#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

os.environ.setdefault('PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK', 'True')

from PIL import Image
from rapidocr_onnxruntime import RapidOCR


def ffmpeg_variant(src: str, dst: str, vf: str):
    proc = subprocess.run(['ffmpeg', '-y', '-i', src, '-vf', vf, dst], capture_output=True, text=True, timeout=240)
    return proc.returncode == 0


def read_size(path: Path):
    with Image.open(path) as im:
        return im.size


def split_vertical(src: Path, out_dir: Path, tile_h=1200, overlap=180):
    w, h = read_size(src)
    parts = []
    y = 0
    idx = 1
    while y < h:
        crop_h = min(tile_h, h - y)
        dst = out_dir / f'{src.stem}-part-{idx:02d}.png'
        if not ffmpeg_variant(str(src), str(dst), f'crop={w}:{crop_h}:0:{y}'):
            break
        parts.append({'path': str(dst), 'y': y, 'height': crop_h})
        idx += 1
        if y + crop_h >= h:
            break
        y += max(tile_h - overlap, 1)
    return parts


def normalize_line(s: str):
    s = (s or '').replace('\u3000', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def compact(s: str):
    return re.sub(r'[\s\-—_.,，。:：;；|｜\[\]()（）<>《》]+', '', s or '').lower()


def merge_lines(lines):
    out = []
    seen = set()
    for line in lines:
        line = normalize_line(line)
        if not line:
            if out and out[-1] != '':
                out.append('')
            continue
        key = compact(line)
        if len(key) >= 8 and key in seen:
            continue
        if key:
            seen.add(key)
        out.append(line)
    while out and not out[-1]:
        out.pop()
    return out


def score_text(text: str):
    if not text:
        return 0
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    digits = sum(1 for ch in text if ch.isdigit())
    lines = [x for x in text.splitlines() if x.strip()]
    long_lines = sum(1 for x in lines if len(x.strip()) >= 8)
    bad = text.count('@@') + text.count('�') + text.count('|||')
    return cjk * 3 + digits + long_lines * 3 - bad * 8


def run_rapidocr(img_path: str, engine):
    result, _ = engine(img_path)
    lines = []
    if result:
        for item in result:
            if len(item) >= 2:
                txt = item[1]
                if isinstance(txt, tuple):
                    txt = txt[0]
                lines.append(str(txt))
    merged = merge_lines(lines)
    return '\n'.join(merged).strip()


def build_variants(src: Path, tmp_dir: Path):
    variants = []
    specs = [
        ('base-gray', 'format=gray'),
        ('up2-gray', 'scale=iw*2:ih*2:flags=lanczos,format=gray'),
        ('up3-contrast', 'scale=iw*3:ih*3:flags=lanczos,eq=contrast=1.4:brightness=0.03:saturation=0,unsharp=5:5:1.2:5:5:0.0'),
        ('up4-sharp', 'scale=iw*4:ih*4:flags=lanczos,format=gray,eq=contrast=1.5:brightness=0.04,unsharp=7:7:1.8:7:7:0.0'),
    ]
    for name, vf in specs:
        dst = tmp_dir / f'{name}.png'
        if ffmpeg_variant(str(src), str(dst), vf):
            variants.append((name, dst))
    return variants


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image')
    ap.add_argument('--output')
    args = ap.parse_args()

    src = Path(args.image).resolve()
    tmp_dir = Path(tempfile.mkdtemp(prefix='high-ocr-'))
    engine = RapidOCR()

    variants = build_variants(src, tmp_dir)
    all_results = []

    for name, path in variants:
        text = run_rapidocr(str(path), engine)
        all_results.append({
            'name': name,
            'path': str(path),
            'text': text,
            'score': score_text(text),
            'segmented': False,
            'segments': []
        })

        w, h = read_size(path)
        if h >= 1400:
            seg_dir = tmp_dir / f'{name}-segments'
            seg_dir.mkdir(parents=True, exist_ok=True)
            segs = split_vertical(path, seg_dir)
            seg_texts = []
            seg_entries = []
            for seg in segs:
                seg_text = run_rapidocr(seg['path'], engine)
                seg_texts.extend(seg_text.splitlines())
                seg_entries.append({**seg, 'text': seg_text})
            merged = '\n'.join(merge_lines(seg_texts)).strip()
            all_results.append({
                'name': f'{name}-segmented',
                'path': str(path),
                'text': merged,
                'score': score_text(merged),
                'segmented': True,
                'segments': seg_entries
            })

    all_results.sort(key=lambda x: x['score'], reverse=True)
    out = {
        'image': str(src),
        'results': all_results,
        'best': all_results[0] if all_results else None
    }

    if args.output:
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
