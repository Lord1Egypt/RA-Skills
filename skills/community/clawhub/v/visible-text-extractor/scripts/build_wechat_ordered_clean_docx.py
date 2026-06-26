#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40'
BASE = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts')
DOCX = BASE / 'build_transcript_docx.js'
OCR_LOCAL = Path('/root/.openclaw/workspace/skills/ocr-local/scripts/ocr.js')
HIGH_OCR = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts/ocr_high_accuracy.py')
HIGH_OCR_PY = Path('/root/.openclaw/venvs/ocrstack/bin/python')


def log(msg):
    print(msg, flush=True)


def download(url: str, out_dir: Path, idx: int):
    req = Request(url, headers={'User-Agent': UA})
    with urlopen(req, timeout=120) as resp:
        data = resp.read()
        ctype = resp.headers.get('Content-Type', '')
    ext = '.bin'
    if 'png' in ctype or 'wx_fmt=png' in url:
        ext = '.png'
    elif 'jpeg' in ctype or 'jpg' in ctype or 'wx_fmt=jpeg' in url or 'wx_fmt=jpg' in url:
        ext = '.jpg'
    elif 'webp' in ctype or 'wx_fmt=webp' in url:
        ext = '.webp'
    p = out_dir / f'image-{idx:02d}{ext}'
    p.write_bytes(data)
    return p


def compact(s: str):
    return re.sub(r'[\s\-—_.,，。:：;；|｜\[\]()（）<>《》]+', '', (s or '').strip()).lower()


def normalize_cn_spacing(line: str):
    s = line
    if sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff') >= 4:
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', s)
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[，。！？：；、）》】])', '', s)
        s = re.sub(r'(?<=[（《【])\s+(?=[\u4e00-\u9fff])', '', s)
    return s.strip()


def clean_text(text: str):
    out = []
    seen = set()
    for raw in (text or '').splitlines():
        line = re.sub(r'\s+', ' ', raw).strip()
        if not line:
            if out and out[-1] != '':
                out.append('')
            continue
        line = normalize_cn_spacing(line)
        key = compact(line)
        if len(key) >= 8 and key in seen:
            continue
        if key:
            seen.add(key)
        out.append(line)
    while out and out[-1] == '':
        out.pop()
    return '\n'.join(out).strip()


def is_clear_enough(text: str):
    if not text:
        return False
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    eng_words = len(re.findall(r'[A-Za-z]{2,}', text))
    digits = sum(1 for ch in text if ch.isdigit())
    long_lines = sum(1 for x in text.splitlines() if len(x.strip()) >= 8)
    if cjk >= 20:
        return True
    if eng_words >= 8 and long_lines >= 3:
        return True
    if cjk >= 8 and digits >= 4 and long_lines >= 2:
        return True
    return False


def fast_ocr(image_path: Path):
    proc = subprocess.run(
        ['node', str(OCR_LOCAL), str(image_path), '--lang', 'chi_sim+eng', '--json'],
        capture_output=True, text=True, timeout=180
    )
    if proc.returncode != 0:
        return ''
    try:
        data = json.loads(proc.stdout)
        return data.get('text', '')
    except Exception:
        return ''


def high_ocr(image_path: Path):
    if not (HIGH_OCR.exists() and HIGH_OCR_PY.exists()):
        return ''
    out = Path(tempfile.mktemp(prefix='ordered-clean-high-', suffix='.json'))
    try:
        proc = subprocess.run(
            [str(HIGH_OCR_PY), str(HIGH_OCR), str(image_path), '--output', str(out)],
            capture_output=True, text=True, timeout=90
        )
    except subprocess.TimeoutExpired:
        return ''
    if proc.returncode != 0 or not out.exists():
        return ''
    try:
        data = json.loads(out.read_text(encoding='utf-8'))
        return (data.get('best') or {}).get('text', '')
    except Exception:
        return ''


def choose_text(local_path: Path, idx: int):
    fast_text = clean_text(fast_ocr(local_path))
    if is_clear_enough(fast_text):
        return fast_text
    if idx <= 6 or len(fast_text) >= 40:
        hi_text = clean_text(high_ocr(local_path))
        if is_clear_enough(hi_text) and len(compact(hi_text)) >= len(compact(fast_text)):
            return hi_text
    return fast_text if is_clear_enough(fast_text) else ''


def build_markdown(title: str, body_text: str, images):
    parts = [f'# {title}', '']
    if body_text:
        parts.append(body_text.strip())
        parts.append('')
    for item in images:
        text = item.get('text', '').strip()
        if not text:
            continue
        parts.append(text)
        parts.append('')
    return '\n'.join(parts).strip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-json', required=True)
    ap.add_argument('--output-prefix', required=True)
    args = ap.parse_args()

    raw = json.loads(Path(args.raw_json).read_text(encoding='utf-8'))
    title = raw.get('page', {}).get('title', 'Article')
    body_text = raw.get('body_text', '')
    images = raw.get('images', []) or []

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    tmpdir = Path(tempfile.mkdtemp(prefix='ordered-clean-'))
    imgdir = tmpdir / 'images'
    imgdir.mkdir(parents=True, exist_ok=True)

    ordered = []
    for idx, img in enumerate(images, 1):
        log(f'[ordered] image {idx}/{len(images)} download')
        try:
            local = download(img.get('url', ''), imgdir, idx)
        except Exception:
            ordered.append({'index': idx, 'text': ''})
            continue
        log(f'[ordered] image {idx}/{len(images)} ocr')
        txt = choose_text(local, idx)
        ordered.append({'index': idx, 'text': txt})

    md = build_markdown(title, body_text, ordered)
    md_path = Path(str(prefix) + '.md')
    docx_path = Path(str(prefix) + '.docx')
    json_path = Path(str(prefix) + '.json')
    md_path.write_text(md, encoding='utf-8')
    json_path.write_text(json.dumps({'title': title, 'body_text': body_text, 'images': ordered}, ensure_ascii=False, indent=2), encoding='utf-8')

    proc = subprocess.run(['node', str(DOCX), str(md_path), str(docx_path)], capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit((proc.stderr or proc.stdout or 'docx build failed').strip())
    print(json.dumps({'ok': True, 'md': str(md_path), 'json': str(json_path), 'docx': str(docx_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
