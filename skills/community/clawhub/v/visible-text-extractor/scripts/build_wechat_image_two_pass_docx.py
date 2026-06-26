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


def clean_lines(text: str):
    out = []
    seen = set()
    for raw in (text or '').splitlines():
        line = re.sub(r'\s+', ' ', raw).strip()
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
    while out and out[-1] == '':
        out.pop()
    return out


def normalize_cn_spacing(line: str):
    s = line
    if sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff') >= 4:
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', s)
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[，。！？：；、）》】])', '', s)
        s = re.sub(r'(?<=[（《【])\s+(?=[\u4e00-\u9fff])', '', s)
    return s.strip()


def fast_ocr(image_path: Path):
    proc = subprocess.run(
        ['node', str(OCR_LOCAL), str(image_path), '--lang', 'chi_sim+eng', '--json'],
        capture_output=True, text=True, timeout=180
    )
    if proc.returncode != 0:
        return {'ok': False, 'text': '', 'error': (proc.stderr or proc.stdout or 'fast ocr failed').strip()}
    try:
        data = json.loads(proc.stdout)
        return {'ok': True, 'text': data.get('text', '')}
    except Exception as e:
        return {'ok': False, 'text': '', 'error': f'bad fast ocr json: {e}'}


def high_ocr(image_path: Path):
    if not (HIGH_OCR.exists() and HIGH_OCR_PY.exists()):
        return {'ok': False, 'text': '', 'error': 'high ocr unavailable'}
    out = Path(tempfile.mktemp(prefix='two-pass-high-', suffix='.json'))
    try:
        proc = subprocess.run(
            [str(HIGH_OCR_PY), str(HIGH_OCR), str(image_path), '--output', str(out)],
            capture_output=True, text=True, timeout=90
        )
    except subprocess.TimeoutExpired:
        return {'ok': False, 'text': '', 'error': 'high ocr timeout'}
    if proc.returncode != 0 or not out.exists():
        return {'ok': False, 'text': '', 'error': (proc.stderr or proc.stdout or 'high ocr failed').strip()}
    try:
        data = json.loads(out.read_text(encoding='utf-8'))
        best = data.get('best') or {}
        return {'ok': True, 'text': best.get('text', '')}
    except Exception as e:
        return {'ok': False, 'text': '', 'error': f'bad high ocr json: {e}'}


def score_candidate(text: str):
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    eng = len(re.findall(r'[A-Za-z]{2,}', text or ''))
    digits = sum(1 for ch in text if ch.isdigit())
    keywords = ['BohrClaw', 'Bohrium', 'Skill', 'GPU', 'RMSE', 'Energy', 'Force', 'Claude', 'Python', 'Fortran', 'Benchmark']
    hit = sum((text or '').count(k) for k in keywords)
    return cjk * 2 + eng * 3 + digits + hit * 8 + len([x for x in (text or '').splitlines() if x.strip()]) * 2


def refine_text(text: str):
    cleaned = []
    for line in clean_lines(text):
        if not line:
            if cleaned and cleaned[-1] != '':
                cleaned.append('')
            continue
        line = normalize_cn_spacing(line)
        cleaned.append(line)
    while cleaned and cleaned[-1] == '':
        cleaned.pop()
    return '\n'.join(cleaned).strip()


def build_md(title: str, body_text: str, results):
    parts = [f'# {title}', '']
    parts += ['## 正文', body_text or '(无)', '']
    parts += ['## 图片提取（整理版）']
    any_clean = False
    for item in results:
        if item.get('refined_text'):
            any_clean = True
            parts.append(f"### 图片 {item['index']}")
            parts.append(item['refined_text'])
            parts.append('')
    if not any_clean:
        parts += ['(暂无可靠图片文字)', '']
    parts += ['## 图片提取（候选原文，含噪音但可能有用）']
    for item in results:
        raw = (item.get('best_text') or '').strip()
        if not raw:
            continue
        parts.append(f"### 图片 {item['index']}")
        parts.append(raw)
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
    tmp = Path(tempfile.mkdtemp(prefix='two-pass-ocr-'))
    img_dir = tmp / 'img'
    img_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for idx, img in enumerate(images, 1):
        url = img.get('url')
        log(f'[pass1] image {idx}/{len(images)} download')
        try:
            local = download(url, img_dir, idx)
        except Exception as e:
            results.append({'index': idx, 'url': url, 'error': f'download failed: {e}', 'best_text': '', 'refined_text': ''})
            continue
        log(f'[pass1] image {idx}/{len(images)} fast ocr')
        fast = fast_ocr(local)
        fast_text = fast.get('text', '') if fast.get('ok') else ''
        best_text = fast_text
        best_score = score_candidate(fast_text)
        use_high = best_score >= 20 or idx <= 4
        if use_high:
            log(f'[pass2] image {idx}/{len(images)} selective high ocr')
            hi = high_ocr(local)
            hi_text = hi.get('text', '') if hi.get('ok') else ''
            hi_score = score_candidate(hi_text)
            if hi_score > best_score:
                best_text = hi_text
                best_score = hi_score
        refined = refine_text(best_text)
        results.append({
            'index': idx,
            'url': url,
            'best_text': best_text.strip(),
            'refined_text': refined,
            'score': best_score,
        })

    md = build_md(title, body_text, results)
    md_path = Path(str(prefix) + '.md')
    json_path = Path(str(prefix) + '.json')
    docx_path = Path(str(prefix) + '.docx')
    md_path.write_text(md, encoding='utf-8')
    json_path.write_text(json.dumps({'title': title, 'body_text': body_text, 'images': results}, ensure_ascii=False, indent=2), encoding='utf-8')
    proc = subprocess.run(['node', str(DOCX), str(md_path), str(docx_path)], capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit((proc.stderr or proc.stdout or 'docx build failed').strip())
    print(json.dumps({'ok': True, 'md': str(md_path), 'json': str(json_path), 'docx': str(docx_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
