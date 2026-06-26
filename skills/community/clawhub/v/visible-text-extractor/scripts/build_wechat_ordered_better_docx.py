#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40'
OCR_LOCAL = Path('/root/.openclaw/workspace/skills/ocr-local/scripts/ocr.js')
DOCX = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts/build_transcript_docx.js')


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


def ocr_lang(image_path: Path, lang: str):
    proc = subprocess.run(
        ['node', str(OCR_LOCAL), str(image_path), '--lang', lang, '--json'],
        capture_output=True, text=True, timeout=240
    )
    if proc.returncode != 0:
        return ''
    try:
        data = json.loads(proc.stdout)
        return data.get('text', '') or ''
    except Exception:
        return ''


def compact(s: str):
    return re.sub(r'[\s\-—_.,，。:：;；|｜\[\]()（）<>《》]+', '', (s or '').strip()).lower()


def normalize_line(line: str):
    s = re.sub(r'\s+', ' ', line).strip()
    if sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff') >= 4:
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', s)
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[，。！？：；、）》】])', '', s)
        s = re.sub(r'(?<=[（《【])\s+(?=[\u4e00-\u9fff])', '', s)
    return s.strip()


def clean_text(text: str):
    lines = []
    seen = set()
    for raw in (text or '').splitlines():
        line = normalize_line(raw)
        if not line:
            if lines and lines[-1] != '':
                lines.append('')
            continue
        key = compact(line)
        if len(key) >= 8 and key in seen:
            continue
        if key:
            seen.add(key)
        lines.append(line)
    while lines and lines[-1] == '':
        lines.pop()
    return '\n'.join(lines).strip()


def score_text(text: str):
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    eng_words = len(re.findall(r'[A-Za-z]{2,}', text or ''))
    digits = sum(1 for ch in text if ch.isdigit())
    long_lines = sum(1 for x in (text or '').splitlines() if len(x.strip()) >= 8)
    urlish = len(re.findall(r'(www\.|\.com|\.tech|http)', text or '', re.I))
    return cjk * 2 + eng_words * 4 + digits + long_lines * 3 + urlish * 8


def looks_clear(text: str):
    if not text:
        return False
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    eng_words = len(re.findall(r'[A-Za-z]{2,}', text))
    long_lines = sum(1 for x in text.splitlines() if len(x.strip()) >= 8)
    return (cjk >= 12 and long_lines >= 2) or (eng_words >= 6 and long_lines >= 2) or (cjk >= 6 and eng_words >= 3)


def choose_best_text(image_path: Path):
    candidates = []
    for lang in ['chi_sim+eng', 'eng', 'chi_sim']:
        text = clean_text(ocr_lang(image_path, lang))
        candidates.append((score_text(text), lang, text))
    candidates.sort(reverse=True)
    best = candidates[0][2] if candidates else ''
    return best if looks_clear(best) else ''


def split_body_paragraphs(body_text: str):
    paras = [x.strip() for x in (body_text or '').split('\n\n') if x.strip()]
    return paras


def build_markdown(title: str, body_text: str, image_texts):
    parts = [f'# {title}', '']
    paras = split_body_paragraphs(body_text)
    if not paras:
        paras = [body_text.strip()] if body_text.strip() else []

    # 近似阅读顺序：正文段落在前，但图片文字严格按图片顺序逐段附加，不再单独汇总说明/候选层。
    for p in paras:
        parts.append(p)
        parts.append('')
    for t in image_texts:
        if not t:
            continue
        parts.append(t)
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
    tmpdir = Path(tempfile.mkdtemp(prefix='ordered-better-'))
    imgdir = tmpdir / 'images'
    imgdir.mkdir(parents=True, exist_ok=True)

    image_texts = []
    for idx, img in enumerate(images, 1):
        log(f'[better] image {idx}/{len(images)} download')
        try:
            local = download(img.get('url', ''), imgdir, idx)
        except Exception:
            image_texts.append('')
            continue
        log(f'[better] image {idx}/{len(images)} multi-lang ocr')
        image_texts.append(choose_best_text(local))

    md = build_markdown(title, body_text, image_texts)
    md_path = Path(str(prefix) + '.md')
    docx_path = Path(str(prefix) + '.docx')
    json_path = Path(str(prefix) + '.json')
    md_path.write_text(md, encoding='utf-8')
    json_path.write_text(json.dumps({'title': title, 'body_text': body_text, 'image_texts': image_texts}, ensure_ascii=False, indent=2), encoding='utf-8')

    proc = subprocess.run(['node', str(DOCX), str(md_path), str(docx_path)], capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit((proc.stderr or proc.stdout or 'docx build failed').strip())
    print(json.dumps({'ok': True, 'md': str(md_path), 'json': str(json_path), 'docx': str(docx_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
