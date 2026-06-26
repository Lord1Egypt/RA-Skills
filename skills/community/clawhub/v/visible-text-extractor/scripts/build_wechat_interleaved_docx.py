#!/usr/bin/env python3
import argparse
import html
import json
import re
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40'
OCR_LOCAL = Path('/root/.openclaw/workspace/skills/ocr-local/scripts/ocr.js')
DOCX = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts/build_transcript_docx.js')


def log(msg):
    print(msg, flush=True)


class WechatFlowParser(HTMLParser):
    def __init__(self, base_url=''):
        super().__init__()
        self.base_url = base_url
        self.blocks = []
        self.current_text = []
        self.in_skip = 0

    def flush_text(self):
        text = ''.join(self.current_text)
        lines = []
        for raw in text.splitlines():
            line = re.sub(r'\s+', ' ', html.unescape(raw)).strip()
            if line:
                lines.append(line)
        text = '\n'.join(lines).strip()
        if text:
            self.blocks.append({'type': 'text', 'text': text})
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'script', 'style'}:
            self.in_skip += 1
            return
        if self.in_skip:
            return
        if tag == 'img':
            self.flush_text()
            src = attrs.get('data-src') or attrs.get('src') or attrs.get('data-original') or ''
            if src:
                self.blocks.append({'type': 'image', 'src': src})
        if tag in {'p', 'section', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote'}:
            self.current_text.append('\n')

    def handle_endtag(self, tag):
        if tag in {'script', 'style'} and self.in_skip:
            self.in_skip -= 1
            return
        if self.in_skip:
            return
        if tag in {'p', 'section', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote'}:
            self.current_text.append('\n')

    def handle_data(self, data):
        if self.in_skip:
            return
        self.current_text.append(data)


def fetch_html(url: str):
    req = Request(url, headers={'User-Agent': UA})
    with urlopen(req, timeout=60) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        return resp.read().decode(charset, errors='replace')


def extract_fragment(raw: str):
    for pat in [
        r'<div[^>]+id="js_content"[^>]*>(.*?)</div>\s*<script',
        r'<div[^>]+id="js_content"[^>]*>(.*?)</div>',
        r'<div[^>]+class="rich_media_content[^"]*"[^>]*>(.*?)</div>',
    ]:
        m = re.search(pat, raw, re.S)
        if m:
            return m.group(1)
    return ''


def normalize_src(src: str):
    s = (src or '').strip()
    if s.startswith('//'):
        s = 'https:' + s
    return s


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


def ocr(image_path: Path, lang: str):
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


def choose_best_text(local: Path):
    candidates = []
    for lang in ['chi_sim+eng', 'eng', 'chi_sim']:
        txt = clean_text(ocr(local, lang))
        candidates.append((score(txt), txt))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1] if candidates else ''


def build_markdown(title: str, flow_blocks):
    parts = [f'# {title}', '']
    for block in flow_blocks:
        if block['type'] == 'text':
            text = block.get('text', '').strip()
            if text:
                parts.append(text)
                parts.append('')
        elif block['type'] == 'image_text':
            text = block.get('text', '').strip()
            if text:
                parts.append(text)
                parts.append('')
    return '\n'.join(parts).strip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True)
    ap.add_argument('--title')
    ap.add_argument('--output-prefix', required=True)
    args = ap.parse_args()

    raw_html = fetch_html(args.url)
    fragment = extract_fragment(raw_html)
    if not fragment:
        raise SystemExit('Failed to locate js_content fragment')

    parser = WechatFlowParser(base_url=args.url)
    parser.feed(fragment)
    parser.flush_text()
    blocks = parser.blocks

    title = args.title
    if not title:
        m = re.search(r'var\s+msg_title\s*=\s*"((?:\\.|[^"])*)"', raw_html)
        if m:
            title = bytes(m.group(1), 'utf-8').decode('unicode_escape')
        else:
            title = 'WeChat Article'

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    tmpdir = Path(tempfile.mkdtemp(prefix='wechat-interleaved-'))
    imgdir = tmpdir / 'images'
    imgdir.mkdir(parents=True, exist_ok=True)

    flow = []
    image_idx = 0
    for block in blocks:
        if block['type'] == 'text':
            txt = clean_text(block.get('text', ''))
            if txt:
                flow.append({'type': 'text', 'text': txt})
        elif block['type'] == 'image':
            image_idx += 1
            src = normalize_src(block.get('src', ''))
            if not src:
                continue
            log(f'[interleave] image {image_idx} download')
            try:
                local = download(src, imgdir, image_idx)
            except Exception:
                continue
            log(f'[interleave] image {image_idx} ocr')
            txt = choose_best_text(local)
            if txt:
                flow.append({'type': 'image_text', 'text': txt, 'src': src, 'index': image_idx})

    md = build_markdown(title, flow)
    md_path = Path(str(prefix) + '.md')
    json_path = Path(str(prefix) + '.json')
    docx_path = Path(str(prefix) + '.docx')
    md_path.write_text(md, encoding='utf-8')
    json_path.write_text(json.dumps({'title': title, 'flow': flow}, ensure_ascii=False, indent=2), encoding='utf-8')

    proc = subprocess.run(['node', str(DOCX), str(md_path), str(docx_path)], capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit((proc.stderr or proc.stdout or 'docx build failed').strip())
    print(json.dumps({'ok': True, 'md': str(md_path), 'json': str(json_path), 'docx': str(docx_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
