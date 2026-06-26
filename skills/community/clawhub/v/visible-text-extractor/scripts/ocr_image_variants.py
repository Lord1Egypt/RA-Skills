#!/usr/bin/env python3
import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

BASE = Path('/root/.openclaw/workspace')
OCR = BASE / 'skills' / 'ocr-local' / 'scripts' / 'ocr.js'


def run(cmd, timeout=240):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ffmpeg_filter(src, dst, vf):
    r = run(['ffmpeg', '-y', '-i', str(src), '-vf', vf, str(dst)])
    return r.returncode == 0


def ocr(path, lang='chi_sim+eng'):
    r = run(['node', str(OCR), str(path), '--lang', lang, '--json'], timeout=300)
    if r.returncode != 0:
        return {'ok': False, 'text': '', 'error': (r.stderr or r.stdout).strip()}
    try:
        data = json.loads(r.stdout)
        return {'ok': True, 'text': (data.get('text') or '').strip(), 'error': ''}
    except Exception as e:
        return {'ok': False, 'text': '', 'error': str(e)}


def score(text):
    if not text:
        return 0
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    digits = sum(1 for ch in text if ch.isdigit())
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    long_lines = sum(1 for x in lines if len(x) >= 8)
    bad = text.count('@@') + text.count('�')
    return cjk * 2 + digits + long_lines * 3 - bad * 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image')
    ap.add_argument('--output')
    args = ap.parse_args()
    src = Path(args.image).resolve()
    tmp = Path(tempfile.mkdtemp(prefix='ocr-variants-'))

    variants = []
    base_out = tmp / 'base.png'
    ffmpeg_filter(src, base_out, 'format=gray')
    variants.append(('base-gray', base_out))

    up2 = tmp / 'up2.png'
    ffmpeg_filter(src, up2, 'scale=iw*2:ih*2:flags=lanczos,format=gray')
    variants.append(('up2-gray', up2))

    up3 = tmp / 'up3-contrast.png'
    ffmpeg_filter(src, up3, 'scale=iw*3:ih*3:flags=lanczos,eq=contrast=1.4:brightness=0.03:saturation=0,unsharp=5:5:1.2:5:5:0.0')
    variants.append(('up3-contrast', up3))

    thr = tmp / 'up3-thresh.png'
    ffmpeg_filter(src, thr, 'scale=iw*3:ih*3:flags=lanczos,format=gray,eq=contrast=1.8:brightness=0.06')
    variants.append(('up3-high-contrast', thr))

    sharp = tmp / 'up4-sharp.png'
    ffmpeg_filter(src, sharp, 'scale=iw*4:ih*4:flags=lanczos,format=gray,eq=contrast=1.5:brightness=0.04,unsharp=7:7:1.8:7:7:0.0')
    variants.append(('up4-sharp', sharp))

    results = []
    for name, path in variants:
        if not path.exists():
            continue
        res = ocr(path)
        results.append({
            'name': name,
            'path': str(path),
            'ok': res['ok'],
            'score': score(res['text']),
            'text': res['text'],
            'error': res['error'],
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    out = {'image': str(src), 'results': results}
    if args.output:
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
