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
ENGLISH_HEAVY = {4, 7, 8, 9, 10, 11}


def log(msg):
    print(msg, flush=True)


def run(cmd, timeout=300):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


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


def enhance(src: Path, dst: Path, profile: str):
    if profile == 'english-chart':
        vf = 'scale=iw*4:ih*4:flags=lanczos,format=gray,eq=contrast=2.0:brightness=0.05,unsharp=7:7:2.0:7:7:0.0'
    else:
        vf = 'scale=iw*3:ih*3:flags=lanczos,format=gray,eq=contrast=1.5:brightness=0.03,unsharp=5:5:1.2:5:5:0.0'
    rc, out, err = run(['ffmpeg', '-y', '-i', str(src), '-vf', vf, str(dst)], timeout=240)
    return rc == 0


def ocr(image_path: Path, lang: str):
    rc, out, err = run(['node', str(OCR_LOCAL), str(image_path), '--lang', lang, '--json'], timeout=240)
    if rc != 0:
        return ''
    try:
        return (json.loads(out).get('text') or '')
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
    out = []
    seen = set()
    for raw in (text or '').splitlines():
        line = normalize_line(raw)
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
    return '\n'.join(out).strip()


def score(text: str):
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    eng_words = len(re.findall(r'[A-Za-z]{2,}', text or ''))
    digits = sum(1 for ch in text if ch.isdigit())
    long_lines = sum(1 for x in (text or '').splitlines() if len(x.strip()) >= 8)
    tech_hits = len(re.findall(r'BohrClaw|Bohrium|RMSE|Energy|Force|Validation|Training|Benchmark|Python|Fortran|GPU|Cloud|Technology|www\.|dp\.tech', text or '', re.I))
    return cjk * 2 + eng_words * 4 + digits + long_lines * 3 + tech_hits * 10


def choose_best(local: Path, idx: int):
    candidates = []

    base_mix = clean_text(ocr(local, 'chi_sim+eng'))
    candidates.append(('base_mix', base_mix, score(base_mix)))

    base_eng = clean_text(ocr(local, 'eng'))
    candidates.append(('base_eng', base_eng, score(base_eng)))

    if idx in ENGLISH_HEAVY:
        enh = local.parent / f'{local.stem}-eng.png'
        if enhance(local, enh, 'english-chart'):
            txt = clean_text(ocr(enh, 'eng'))
            candidates.append(('enh_eng', txt, score(txt)))
            txt2 = clean_text(ocr(enh, 'chi_sim+eng'))
            candidates.append(('enh_mix', txt2, score(txt2)))

    candidates.sort(key=lambda x: x[2], reverse=True)
    best = candidates[0][1] if candidates else ''
    return best


def split_body(body_text: str):
    return [x.strip() for x in (body_text or '').split('\n\n') if x.strip()]


def build_markdown(title: str, body_text: str, image_texts):
    parts = [f'# {title}', '']
    for p in split_body(body_text):
        parts.append(p)
        parts.append('')
    for idx, txt in enumerate(image_texts, 1):
        if not txt:
            continue
        parts.append(txt)
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
    tmpdir = Path(tempfile.mkdtemp(prefix='ordered-precise-'))
    imgdir = tmpdir / 'images'
    imgdir.mkdir(parents=True, exist_ok=True)

    image_texts = []
    for idx, img in enumerate(images, 1):
        log(f'[precise] image {idx}/{len(images)} download')
        try:
            local = download(img.get('url', ''), imgdir, idx)
        except Exception:
            image_texts.append('')
            continue
        log(f'[precise] image {idx}/{len(images)} deep ocr')
        image_texts.append(choose_best(local, idx))

    md = build_markdown(title, body_text, image_texts)
    md_path = Path(str(prefix) + '.md')
    json_path = Path(str(prefix) + '.json')
    docx_path = Path(str(prefix) + '.docx')
    md_path.write_text(md, encoding='utf-8')
    json_path.write_text(json.dumps({'title': title, 'body_text': body_text, 'image_texts': image_texts}, ensure_ascii=False, indent=2), encoding='utf-8')
    rc, out, err = run(['node', str(DOCX), str(md_path), str(docx_path)], timeout=300)
    if rc != 0:
        raise SystemExit((err or out or 'docx build failed').strip())
    print(json.dumps({'ok': True, 'md': str(md_path), 'json': str(json_path), 'docx': str(docx_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
