#!/usr/bin/env python3
import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import struct
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

HIGH_OCR_PYTHON = Path('/root/.openclaw/venvs/ocrstack/bin/python')
HIGH_OCR_SCRIPT = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts/ocr_high_accuracy.py')

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36'
WECHAT_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40'
BASE_DIR = Path(__file__).resolve().parent.parent
OCR_SCRIPT = BASE_DIR / 'ocr-local' / 'scripts' / 'ocr.js'
if not OCR_SCRIPT.exists():
    OCR_SCRIPT = Path('/root/.openclaw/workspace/skills/ocr-local/scripts/ocr.js')
BROWSER_SCRIPT = BASE_DIR / 'visible-text-extractor' / 'scripts' / 'extract_with_browser.js'
if not BROWSER_SCRIPT.exists():
    BROWSER_SCRIPT = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts/extract_with_browser.js')
WECHAT_SCRIPT = Path('/root/.openclaw/workspace/skills/wechat-mp-reader/scripts/read_wechat_article.js')

BLOCK_TAGS = {
    'p', 'div', 'section', 'article', 'main', 'aside', 'header', 'footer', 'li', 'ul', 'ol',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'br', 'hr', 'tr', 'td'
}
SKIP_TAGS = {'script', 'style', 'noscript', 'svg', 'canvas'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.svg'}


def now_iso():
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def fetch_url(url: str, user_agent: str = UA) -> str:
    req = Request(url, headers={'User-Agent': user_agent})
    with urlopen(req) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        return resp.read().decode(charset, errors='replace')


class VisibleHTMLParser(HTMLParser):
    def __init__(self, base_url=''):
        super().__init__()
        self.base_url = base_url
        self.in_skip = 0
        self.title = ''
        self.in_title = False
        self.text_parts = []
        self.images = []
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in SKIP_TAGS:
            self.in_skip += 1
            return
        if tag == 'title':
            self.in_title = True
        if tag in BLOCK_TAGS:
            self.text_parts.append('\n')
        if tag == 'meta':
            key = attrs.get('property') or attrs.get('name') or ''
            val = attrs.get('content') or ''
            if key and val:
                self.meta[key] = val
        if tag == 'img':
            src = attrs.get('src') or attrs.get('data-src') or attrs.get('data-original') or ''
            if src:
                self.images.append(urljoin(self.base_url, src))
        if tag == 'source':
            srcset = attrs.get('srcset') or ''
            if srcset:
                first = srcset.split(',')[0].strip().split(' ')[0]
                if first:
                    self.images.append(urljoin(self.base_url, first))

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.in_skip:
            self.in_skip -= 1
            return
        if tag == 'title':
            self.in_title = False
        if tag in BLOCK_TAGS:
            self.text_parts.append('\n')

    def handle_data(self, data):
        if self.in_skip:
            return
        s = data.strip()
        if not s:
            return
        if self.in_title:
            self.title += s
        self.text_parts.append(s)
        self.text_parts.append('\n')


class FragmentParser(HTMLParser):
    def __init__(self, base_url=''):
        super().__init__()
        self.base_url = base_url
        self.in_skip = 0
        self.parts = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in SKIP_TAGS:
            self.in_skip += 1
            return
        if tag in BLOCK_TAGS:
            self.parts.append('\n')
        if tag == 'img':
            src = attrs.get('src') or attrs.get('data-src') or attrs.get('data-original') or ''
            if src:
                self.images.append(urljoin(self.base_url, src))

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.in_skip:
            self.in_skip -= 1
            return
        if tag in BLOCK_TAGS:
            self.parts.append('\n')

    def handle_data(self, data):
        if self.in_skip:
            return
        s = data.strip()
        if s:
            self.parts.append(s)
            self.parts.append('\n')


def normalize_lines(text: str) -> str:
    text = html.unescape(text)
    lines = [re.sub(r'\s+', ' ', x).strip() for x in text.splitlines()]
    out = []
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                out.append('')
            prev_blank = True
            continue
        out.append(line)
        prev_blank = False
    return '\n'.join(out).strip()


def unique_keep_order(items):
    seen = set()
    out = []
    for x in items:
        key = str(x)
        if key in seen:
            continue
        seen.add(key)
        out.append(x)
    return out


def split_gifs(items):
    gifs = []
    others = []
    for u in items:
        lu = str(u).lower()
        if '.gif' in lu or lu.endswith('.gif'):
            gifs.append(u)
        else:
            others.append(u)
    return others, gifs


def download_file(url: str, suffix=''):
    req = Request(url, headers={'User-Agent': UA})
    with urlopen(req) as resp:
        data = resp.read()
        ctype = resp.headers.get('Content-Type', '')
    if not suffix:
        path = urlparse(url).path.lower()
        for ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.svg']:
            if path.endswith(ext):
                suffix = ext
                break
    if not suffix:
        if 'png' in ctype:
            suffix = '.png'
        elif 'jpeg' in ctype or 'jpg' in ctype:
            suffix = '.jpg'
        elif 'webp' in ctype:
            suffix = '.webp'
        elif 'gif' in ctype:
            suffix = '.gif'
        elif 'svg' in ctype:
            suffix = '.svg'
        else:
            suffix = '.bin'
    fd, tmp = tempfile.mkstemp(prefix='visible-text-', suffix=suffix)
    os.close(fd)
    Path(tmp).write_bytes(data)
    return tmp


def run_ocr(image_path: str, lang='chi_sim+eng', timeout=300):
    if not OCR_SCRIPT.exists():
        return {'status': 'error', 'ocr_text': '', 'uncertain': ['ocr-local script not found']}
    try:
        proc = subprocess.run(
            ['node', str(OCR_SCRIPT), image_path, '--lang', lang, '--json'],
            capture_output=True, text=True, timeout=timeout
        )
    except Exception as e:
        return {'status': 'error', 'ocr_text': '', 'uncertain': [f'ocr launch failed: {e}']}
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or '').strip()
        return {'status': 'error', 'ocr_text': '', 'uncertain': [msg or 'ocr failed']}
    try:
        data = json.loads(proc.stdout)
        return {'status': 'ok', 'ocr_text': (data.get('text') or '').strip(), 'uncertain': []}
    except Exception as e:
        return {'status': 'error', 'ocr_text': '', 'uncertain': [f'bad ocr json: {e}']}


def ocr_text_score(text: str) -> int:
    if not text:
        return 0
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    digits = sum(1 for ch in text if ch.isdigit())
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    long_lines = sum(1 for x in lines if len(x) >= 8)
    bad = text.count('@@') + text.count('�') + text.count('|||')
    return cjk * 2 + digits + long_lines * 3 - bad * 5


def ffmpeg_variant(src: str, dst: str, vf: str):
    proc = subprocess.run(['ffmpeg', '-y', '-i', src, '-vf', vf, dst], capture_output=True, text=True, timeout=240)
    return proc.returncode == 0


def run_ocr_best_variant(image_path: str, lang='chi_sim+eng'):
    high_ocr_timeout = int(os.environ.get('VISIBLE_TEXT_HIGH_OCR_TIMEOUT', '120'))
    if HIGH_OCR_PYTHON.exists() and HIGH_OCR_SCRIPT.exists():
        out_path = Path(tempfile.mktemp(prefix='high-ocr-result-', suffix='.json'))
        try:
            proc = subprocess.run(
                [str(HIGH_OCR_PYTHON), str(HIGH_OCR_SCRIPT), image_path, '--output', str(out_path)],
                capture_output=True, text=True, timeout=high_ocr_timeout
            )
        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'ocr_text': '',
                'uncertain': [f'高精度 OCR 单图处理超时（{high_ocr_timeout}s），已降级到快速 OCR。'],
                'variants': [],
                'segments': [],
                'segment_mode': False,
            }
        if proc.returncode == 0 and out_path.exists():
            try:
                data = json.loads(out_path.read_text(encoding='utf-8'))
                best = data.get('best') or {}
                candidates = data.get('results') or []
                uncertain = []
                if best.get('name'):
                    uncertain.append(f"已使用高精度 OCR 管线，采用最佳结果：{best['name']}。")
                return {
                    'status': 'ok' if best.get('text') else 'error',
                    'ocr_text': best.get('text', ''),
                    'uncertain': uncertain,
                    'variants': candidates,
                    'segments': best.get('segments', []),
                    'segment_mode': bool(best.get('segmented')),
                }
            except Exception:
                pass

    src = Path(image_path)
    tmp_dir = Path(tempfile.mkdtemp(prefix='visible-ocr-variant-'))
    candidates = []
    variant_specs = [
        ('base-gray', 'format=gray'),
        ('up2-gray', 'scale=iw*2:ih*2:flags=lanczos,format=gray'),
        ('up3-contrast', 'scale=iw*3:ih*3:flags=lanczos,eq=contrast=1.4:brightness=0.03:saturation=0,unsharp=5:5:1.2:5:5:0.0'),
        ('up4-sharp', 'scale=iw*4:ih*4:flags=lanczos,format=gray,eq=contrast=1.5:brightness=0.04,unsharp=7:7:1.8:7:7:0.0'),
    ]
    for name, vf in variant_specs:
        out = tmp_dir / f'{name}.png'
        if not ffmpeg_variant(str(src), str(out), vf):
            continue
        ocr = run_ocr(str(out), lang=lang, timeout=300)
        text = ocr.get('ocr_text', '')
        candidates.append({
            'name': name,
            'path': str(out),
            'status': ocr.get('status', 'error'),
            'ocr_text': text,
            'score': ocr_text_score(text),
            'uncertain': ocr.get('uncertain', []),
        })
    if not candidates:
        base = run_ocr(str(src), lang=lang)
        return {
            'status': base.get('status', 'error'),
            'ocr_text': base.get('ocr_text', ''),
            'uncertain': base.get('uncertain', []),
            'variants': []
        }
    candidates.sort(key=lambda x: x['score'], reverse=True)
    best = candidates[0]
    uncertain = list(best.get('uncertain', []))
    if best['name'] != 'base-gray':
        uncertain.append(f"已比较多种图像增强 OCR，采用效果最佳版本：{best['name']}。")
    return {
        'status': best.get('status', 'error'),
        'ocr_text': best.get('ocr_text', ''),
        'uncertain': uncertain,
        'variants': candidates,
        'segments': [],
        'segment_mode': False,
    }


def looks_blocked(body_text: str, title: str = ''):
    t = f"{title}\n{body_text}".strip()
    patterns = [
        '环境异常', '完成验证后即可继续访问', '去验证', '访问过于频繁',
        '请在微信客户端打开链接', '账号异常', '内容无法访问', 'the page you are looking for'
    ]
    return any(p in t for p in patterns)


def is_wechat_mp_url(url: str) -> bool:
    try:
        host = (urlparse(url).netloc or '').lower()
    except Exception:
        return False
    return host.endswith('mp.weixin.qq.com')


def browser_fetch(url: str):
    if not BROWSER_SCRIPT.exists() or not shutil.which('node'):
        return None
    html_path = tempfile.mktemp(prefix='browser-render-', suffix='.html')
    shot_path = tempfile.mktemp(prefix='browser-render-', suffix='.png')
    proc = subprocess.run(
        ['node', str(BROWSER_SCRIPT), '--url', url, '--output-html', html_path, '--output-shot', shot_path],
        capture_output=True, text=True, timeout=240
    )
    if proc.returncode != 0:
        return {
            'ok': False,
            'html_path': html_path,
            'shot_path': shot_path,
            'error': (proc.stderr or proc.stdout or '').strip() or 'browser render failed'
        }
    return {
        'ok': True,
        'html_path': html_path,
        'shot_path': shot_path,
        'error': ''
    }


def run_wechat_reader(url: str):
    if not WECHAT_SCRIPT.exists() or not shutil.which('node'):
        return None
    out_path = tempfile.mktemp(prefix='wechat-reader-', suffix='.json')
    proc = subprocess.run(
        ['node', str(WECHAT_SCRIPT), '--url', url, '--output', out_path],
        capture_output=True, text=True, timeout=240
    )
    if proc.returncode != 0:
        return {
            'ok': False,
            'error': (proc.stderr or proc.stdout or '').strip() or 'wechat reader failed',
            'path': out_path,
        }
    try:
        data = json.loads(Path(out_path).read_text(encoding='utf-8'))
    except Exception as e:
        return {
            'ok': False,
            'error': f'wechat reader output parse failed: {e}',
            'path': out_path,
        }
    data['ok'] = True
    data['path'] = out_path
    return data


def parse_html_text(raw: str, base_url: str = ''):
    parser = VisibleHTMLParser(base_url=base_url)
    parser.feed(raw)
    title = parser.title or parser.meta.get('og:title') or ''
    body_text = normalize_lines('\n'.join(parser.text_parts))
    image_urls = unique_keep_order(parser.images)
    return title, body_text, image_urls, parser.meta


def extract_fragment_text(fragment: str, base_url: str = ''):
    parser = FragmentParser(base_url=base_url)
    parser.feed(fragment)
    return normalize_lines('\n'.join(parser.parts)), unique_keep_order(parser.images)


def extract_wechat_static(raw: str, base_url: str = ''):
    result = {'title': '', 'body_text': '', 'image_urls': [], 'uncertain': []}
    title_patterns = [
        r'var\s+msg_title\s*=\s*"((?:\\.|[^"])*)"',
        r"var\s+msg_title\s*=\s*'((?:\\.|[^'])*)'",
        r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"',
    ]
    for pat in title_patterns:
        m = re.search(pat, raw)
        if m:
            value = m.group(1)
            if '\\u' in value or '\\x' in value:
                try:
                    result['title'] = bytes(value, 'utf-8').decode('unicode_escape')
                except Exception:
                    result['title'] = html.unescape(value)
            else:
                result['title'] = html.unescape(value)
            break

    fragment = None
    for pat in [
        r'<div[^>]+id="js_content"[^>]*>(.*?)</div>\s*<script',
        r'<div[^>]+id="js_content"[^>]*>(.*?)</div>\s*</div>\s*<section',
        r'<div[^>]+id="js_content"[^>]*>(.*?)</div>',
        r'<div[^>]+class="rich_media_content[^"]*"[^>]*>(.*?)</div>',
    ]:
        m = re.search(pat, raw, re.S)
        if m and len(m.group(1).strip()) > 100:
            fragment = m.group(1)
            break

    if fragment:
        body_text, image_urls = extract_fragment_text(fragment, base_url=base_url)
        result['body_text'] = body_text
        result['image_urls'] = image_urls
    else:
        result['uncertain'].append('未在公众号 HTML 中定位到 js_content/rich_media_content 容器。')

    return result


def read_local_html(path: Path):
    raw = path.read_text(encoding='utf-8', errors='replace')
    title, body_text, image_urls, meta = parse_html_text(raw, base_url=path.resolve().as_uri())
    return {
        'title': title or path.stem,
        'body_text': body_text,
        'image_urls': image_urls,
        'meta': meta,
        'uncertain': []
    }


def collect_image_inputs(image_paths, image_dir):
    items = []
    for p in image_paths or []:
        pp = Path(p)
        if pp.exists() and pp.is_file():
            items.append(pp.resolve())
    if image_dir:
        d = Path(image_dir)
        if d.exists() and d.is_dir():
            for p in sorted(d.iterdir()):
                if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                    items.append(p.resolve())
    return unique_keep_order(items)


def run_gif_frames(gif_path: Path, limit=8):
    script = BASE_DIR / 'visible-text-extractor' / 'scripts' / 'extract_gif_frames.sh'
    if not script.exists():
        script = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts/extract_gif_frames.sh')
    if not script.exists() or not shutil.which('bash'):
        return {'status': 'placeholder', 'frames': [], 'uncertain': ['GIF 抽帧脚本不存在。']}
    out_dir = Path(tempfile.mkdtemp(prefix='gif-frames-'))
    proc = subprocess.run(
        ['bash', str(script), str(gif_path), str(out_dir)],
        capture_output=True, text=True, timeout=240
    )
    if proc.returncode != 0:
        return {'status': 'placeholder', 'frames': [], 'uncertain': [(proc.stderr or proc.stdout or '').strip() or 'GIF 抽帧失败']}
    frames = sorted([p for p in out_dir.iterdir() if p.is_file()])[:limit]
    return {'status': 'ok', 'frames': frames, 'uncertain': []}


def read_image_size(path: Path):
    suffix = path.suffix.lower()
    if suffix == '.png':
        b = path.read_bytes()
        if len(b) >= 24:
            return struct.unpack('>II', b[16:24])
    if suffix in {'.jpg', '.jpeg'}:
        data = path.read_bytes()
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            while i < len(data) and data[i] == 0xFF:
                i += 1
            if i >= len(data):
                break
            marker = data[i]
            i += 1
            if marker in (0xD8, 0xD9):
                continue
            if i + 1 >= len(data):
                break
            seglen = (data[i] << 8) + data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h = (data[i + 3] << 8) + data[i + 4]
                w = (data[i + 5] << 8) + data[i + 6]
                return (w, h)
            i += seglen
    return (0, 0)


def compact_text_key(line: str) -> str:
    return re.sub(r'[\s\-—_.,，。:：;；|｜\[\]()（）<>《》]+', '', (line or '').strip()).lower()


def clean_ocr_lines(text: str):
    lines = []
    seen = set()
    prev_blank = False
    for raw in (text or '').replace('\r', '\n').splitlines():
        line = re.sub(r'\s+', ' ', raw).strip()
        if not line:
            if lines and not prev_blank:
                lines.append('')
            prev_blank = True
            continue
        key = compact_text_key(line)
        if len(key) >= 6 and key in seen:
            continue
        if key:
            seen.add(key)
        lines.append(line)
        prev_blank = False
    while lines and not lines[-1]:
        lines.pop()
    return lines


def merge_segment_texts(segment_entries):
    merged = []
    seen = set()
    for seg in segment_entries:
        for line in clean_ocr_lines(seg.get('ocr_text', '')):
            if not line:
                if merged and merged[-1] != '':
                    merged.append('')
                continue
            key = compact_text_key(line)
            if len(key) >= 8 and key in seen:
                continue
            if key:
                seen.add(key)
            merged.append(line)
    while merged and not merged[-1]:
        merged.pop()
    return '\n'.join(merged).strip()


def should_segment_image(width: int, height: int) -> bool:
    if width <= 0 or height <= 0:
        return False
    if height >= 1600:
        return True
    if height >= 1100 and height / max(width, 1) >= 1.15:
        return True
    return False


def segment_image(path: Path, width: int, height: int):
    if not shutil.which('ffmpeg'):
        return []
    out_dir = Path(tempfile.mkdtemp(prefix='visible-text-seg-'))
    tile_h = 900 if height > 2200 else 700
    overlap = 120
    y = 0
    idx = 1
    parts = []
    while y < height:
        crop_h = min(tile_h, height - y)
        dst = out_dir / f'{path.stem}-part-{idx:02d}.png'
        cmd = ['ffmpeg', '-y', '-i', str(path), '-vf', f'crop={width}:{crop_h}:0:{y}', str(dst)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        if proc.returncode != 0:
            break
        parts.append({'path': str(dst), 'y': y, 'height': crop_h})
        idx += 1
        if y + crop_h >= height:
            break
        y += max(tile_h - overlap, 1)
    return parts


def ocr_image_with_segments(local_path: str, lang='chi_sim+eng'):
    p = Path(local_path)
    width, height = read_image_size(p)
    result = {
        'ocr_text': '',
        'status': 'skipped',
        'uncertain': [],
        'local_path': str(p),
        'size': {'width': width, 'height': height},
        'full_ocr_text': '',
        'segment_mode': False,
        'segments': [],
        'variants': []
    }
    full = run_ocr_best_variant(str(p), lang=lang)
    if full.get('status') == 'timeout' or (not full.get('ocr_text') and full.get('status') != 'ok'):
        fallback = run_ocr(str(p), lang=lang, timeout=180)
        full = {
            'status': fallback.get('status', 'error'),
            'ocr_text': fallback.get('ocr_text', ''),
            'uncertain': list(full.get('uncertain', [])) + list(fallback.get('uncertain', [])),
            'variants': full.get('variants', []),
            'segments': [],
            'segment_mode': False,
        }
        if full.get('ocr_text'):
            full['uncertain'].append('已从高精度 OCR 降级到快速 OCR，以避免任务长时间卡住。')
    result['status'] = full.get('status', 'error')
    result['ocr_text'] = full.get('ocr_text', '')
    result['full_ocr_text'] = result['ocr_text']
    result['uncertain'].extend(full.get('uncertain', []))
    result['variants'] = full.get('variants', [])

    if full.get('segments'):
        result['segments'] = full.get('segments', [])
        result['segment_mode'] = bool(full.get('segment_mode'))
        return result

    if should_segment_image(width, height):
        parts = segment_image(p, width, height)
        if parts:
            result['segment_mode'] = True
            for part in parts:
                ocr = run_ocr_best_variant(part['path'], lang=lang)
                entry = {
                    'path': part['path'],
                    'y': part['y'],
                    'height': part['height'],
                    'status': ocr.get('status', 'error'),
                    'ocr_text': ocr.get('ocr_text', ''),
                    'uncertain': ocr.get('uncertain', [])
                }
                result['segments'].append(entry)
            merged = merge_segment_texts(result['segments'])
            if len(compact_text_key(merged)) > len(compact_text_key(result['ocr_text'])):
                result['ocr_text'] = merged
                result['status'] = 'ok'
                result['uncertain'].append('已对长图执行分段 OCR，并以合并结果覆盖整图 OCR。')
            else:
                result['uncertain'].append('已对长图执行分段 OCR，但整图 OCR 结果更完整，保留整图结果。')
        else:
            result['uncertain'].append('图片疑似长图，但当前环境无法完成分段裁切。')
    return result


def build_markdown(result):
    page = result['page']
    parts = []
    parts.append('# 页面基础信息')
    parts.append(f"- 标题：{page.get('title', '')}")
    parts.append(f"- 来源链接：{page.get('source_url', '')}")
    parts.append(f"- 来源类型：{page.get('source_type', '')}")
    parts.append(f"- 提取时间：{page.get('extracted_at', '')}")
    if page.get('blocked') is not None:
        parts.append(f"- blocked：{str(page.get('blocked')).lower()}")
    parts.append('')
    parts.append('# 正文文本')
    parts.append(result.get('body_text', '') or '(无)')
    parts.append('')
    parts.append('# 图片文本')
    if result['images']:
        for img in result['images']:
            parts.append(f"## 图片 {img['index']}")
            parts.append(f"- 来源：{img['url']}")
            parts.append(f"- 状态：{img['status']}")
            if img.get('size'):
                parts.append(f"- 尺寸：{img['size'].get('width', 0)}x{img['size'].get('height', 0)}")
            if img.get('segment_mode'):
                parts.append('- 模式：分段 OCR')
            parts.append((img.get('ocr_text') or '(无提取文本)').strip() or '(无提取文本)')
            if img.get('segments'):
                parts.append('- 分段结果：')
                for seg in img['segments']:
                    parts.append(f"  - y={seg.get('y', 0)} h={seg.get('height', 0)} status={seg.get('status', '')}")
            if img.get('uncertain'):
                parts.append('- 不确定：')
                for u in img['uncertain']:
                    parts.append(f"  - {u}")
            parts.append('')
    else:
        parts.append('(未发现图片)')
        parts.append('')
    parts.append('# 动图 / GIF 文本')
    if result['gifs']:
        for g in result['gifs']:
            parts.append(f"## GIF {g['index']}")
            parts.append(f"- 来源：{g['url']}")
            parts.append(f"- 状态：{g['status']}")
            parts.append((g.get('deduped_text') or '(当前环境未提取 GIF 帧文字)').strip() or '(当前环境未提取 GIF 帧文字)')
            if g.get('uncertain'):
                parts.append('- 不确定：')
                for u in g['uncertain']:
                    parts.append(f"  - {u}")
            parts.append('')
    else:
        parts.append('(未发现 GIF)')
        parts.append('')
    parts.append('# 不确定内容')
    if result['uncertain']:
        for u in result['uncertain']:
            parts.append(f"- {u}")
    else:
        parts.append('(无)')
    parts.append('')
    parts.append('# 最终合并文本')
    parts.append(result.get('merged_text', ''))
    parts.append('')
    return '\n'.join(parts).strip() + '\n'


def merge_text(body_text, images, gifs, dedupe=False):
    chunks = []
    if body_text:
        chunks.append(body_text.strip())
    for img in images:
        if img.get('ocr_text'):
            chunks.append(img['ocr_text'].strip())
    for g in gifs:
        if g.get('deduped_text'):
            chunks.append(g['deduped_text'].strip())
    merged = '\n\n'.join([c for c in chunks if c])
    if not dedupe:
        return merged
    lines = []
    seen = set()
    for line in merged.splitlines():
        key = line.strip()
        if not key:
            lines.append('')
            continue
        if key in seen:
            continue
        seen.add(key)
        lines.append(line)
    return '\n'.join(lines).strip()


def process_image_like_inputs(local_images, ocr_images, gif_mode):
    images = []
    gifs = []
    for path in local_images:
        suffix = path.suffix.lower()
        as_url = path.as_uri()
        if suffix == '.gif':
            entry = {
                'index': len(gifs) + 1,
                'url': as_url,
                'status': 'skipped',
                'frames': [],
                'deduped_text': '',
                'uncertain': []
            }
            if gif_mode == 'none':
                entry['status'] = 'skipped'
                entry['uncertain'].append('GIF 提取已禁用。')
            else:
                frame_res = run_gif_frames(path)
                entry['status'] = frame_res['status']
                entry['uncertain'].extend(frame_res.get('uncertain', []))
                frame_texts = []
                for f in frame_res.get('frames', []):
                    ocr = run_ocr(str(f)) if ocr_images else {'status': 'skipped', 'ocr_text': '', 'uncertain': ['未启用 OCR']}
                    entry['frames'].append({
                        'path': str(f),
                        'status': ocr.get('status', 'error'),
                        'ocr_text': ocr.get('ocr_text', ''),
                        'uncertain': ocr.get('uncertain', [])
                    })
                    if ocr.get('ocr_text'):
                        frame_texts.append(ocr['ocr_text'].strip())
                entry['deduped_text'] = '\n'.join(unique_keep_order([t for t in frame_texts if t]))
            gifs.append(entry)
        else:
            item = {
                'index': len(images) + 1,
                'url': as_url,
                'ocr_text': '',
                'status': 'skipped',
                'uncertain': [],
                'segments': [],
                'segment_mode': False,
                'size': None,
                'full_ocr_text': '',
                'local_path': str(path),
                'variants': []
            }
            if ocr_images:
                ocr = ocr_image_with_segments(str(path))
                item['ocr_text'] = ocr.get('ocr_text', '')
                item['status'] = ocr.get('status', 'error')
                item['uncertain'].extend(ocr.get('uncertain', []))
                item['segments'] = ocr.get('segments', [])
                item['segment_mode'] = ocr.get('segment_mode', False)
                item['size'] = ocr.get('size')
                item['full_ocr_text'] = ocr.get('full_ocr_text', '')
                item['local_path'] = ocr.get('local_path', str(path))
                item['variants'] = ocr.get('variants', [])
            images.append(item)
    return images, gifs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url')
    ap.add_argument('--text-file')
    ap.add_argument('--html-file')
    ap.add_argument('--image', action='append', default=[])
    ap.add_argument('--image-dir')
    ap.add_argument('--format', choices=['markdown', 'json'], default='markdown')
    ap.add_argument('--output')
    ap.add_argument('--keep-order', action='store_true')
    ap.add_argument('--dedupe', action='store_true')
    ap.add_argument('--group-by-image', action='store_true')
    ap.add_argument('--ocr-images', action='store_true')
    ap.add_argument('--gif-mode', choices=['none', 'placeholder'], default='placeholder')
    ap.add_argument('--browser-fallback', action='store_true')
    ap.add_argument('--page-screenshot-ocr', action='store_true')
    args = ap.parse_args()

    if not any([args.url, args.text_file, args.html_file, args.image, args.image_dir]):
        raise SystemExit('Provide --url, --text-file, --html-file, --image, or --image-dir')

    title = ''
    source_url = args.url or ''
    source_type = 'mixed'
    body_text = ''
    image_urls = []
    uncertain = []
    blocked = None

    if args.url:
        source_type = 'url'
        raw = ''
        if is_wechat_mp_url(args.url):
            source_type = 'wechat-mp-url'
            try:
                raw = fetch_url(args.url, user_agent=WECHAT_UA)
                ws = extract_wechat_static(raw, base_url=args.url)
                title = ws.get('title') or title
                body_text = ws.get('body_text') or body_text
                image_urls = unique_keep_order(image_urls + ws.get('image_urls', []))
                uncertain.append('公众号 URL 已优先走静态 HTML 专用正文容器提取。')
                uncertain.extend(ws.get('uncertain', []))
                if body_text:
                    blocked = looks_blocked(body_text, title)
            except Exception as e:
                uncertain.append(f'公众号静态提取失败：{e}')

            wr = run_wechat_reader(args.url)
            if wr and wr.get('ok'):
                browser_title = normalize_lines(wr.get('title') or '')
                browser_text = normalize_lines(wr.get('body_text') or '')
                browser_blocked = bool(wr.get('blocked'))
                browser_images = unique_keep_order(wr.get('image_urls') or [])
                source_url = wr.get('url') or args.url
                image_urls = unique_keep_order(image_urls + browser_images)
                if not body_text or (browser_text and not browser_blocked and len(browser_text) > len(body_text)):
                    title = browser_title or title
                    body_text = browser_text or body_text
                    blocked = browser_blocked
                    uncertain.append('公众号 URL 也尝试了 wechat-mp-reader 浏览器链路。')
                elif browser_blocked:
                    uncertain.append('公众号浏览器链路命中 blocked/验证态，未覆盖已提取到的静态正文。')
                if browser_images:
                    uncertain.append(f'公众号浏览器链路额外发现 {len(browser_images)} 个公开图片资源。')
            elif wr:
                uncertain.append(f"公众号专用浏览器链路失败：{wr.get('error', 'unknown error')}")

        try:
            if not raw:
                raw = fetch_url(args.url)
            title0, body0, image_urls0, _meta0 = parse_html_text(raw, base_url=args.url)
            if not title:
                title = title0
            if not body_text and body0:
                body_text = body0
            image_urls = unique_keep_order(image_urls + image_urls0)
            if body0 and blocked is None:
                blocked = looks_blocked(body0, title0)
            if not body0 and not body_text:
                uncertain.append('HTML 抓到了，但未提取到明显正文；页面可能依赖 JS 渲染。')

            should_try_browser = args.browser_fallback and (not body_text or bool(blocked))
            if should_try_browser:
                bf = browser_fetch(args.url)
                if not bf:
                    uncertain.append('浏览器兜底未启用或脚本不存在。')
                elif not bf.get('ok'):
                    uncertain.append(f"浏览器渲染失败：{bf.get('error', 'unknown error')}")
                else:
                    rendered_html = Path(bf['html_path']).read_text(encoding='utf-8', errors='replace')
                    title2, body2, imgs2, _meta2 = parse_html_text(rendered_html, base_url=args.url)
                    browser_blocked = looks_blocked(body2, title2)
                    if body2 and not browser_blocked and len(body2) > len(body_text):
                        title = title2 or title
                        body_text = body2
                        image_urls = unique_keep_order(image_urls + imgs2)
                        blocked = False
                        uncertain.append('已使用浏览器渲染兜底提取页面内容。')
                    elif browser_blocked:
                        uncertain.append('浏览器渲染结果命中 blocked/验证态，未覆盖已有正文。')
                    if args.page_screenshot_ocr and Path(bf['shot_path']).exists() and (not body_text or bool(blocked)):
                        ocr = run_ocr(bf['shot_path'])
                        shot_text = (ocr.get('ocr_text') or '').strip()
                        if shot_text:
                            uncertain.append('已对整页截图执行 OCR 作为兜底补充。')
                            if not body_text:
                                body_text = shot_text
                                blocked = looks_blocked(body_text, title)
                            else:
                                body_text = (body_text + '\n\n[整页截图 OCR 补充]\n' + shot_text).strip()
                        else:
                            uncertain.extend(ocr.get('uncertain', []))
        except Exception as e:
            uncertain.append(f'URL 抓取失败：{e}')

    if args.text_file:
        p = Path(args.text_file)
        source_type = 'text-file' if source_type == 'mixed' else source_type
        txt = p.read_text(encoding='utf-8', errors='replace').strip()
        body_text = '\n\n'.join([x for x in [body_text, txt] if x]).strip()
        if not title:
            title = p.stem

    if args.html_file:
        p = Path(args.html_file)
        source_type = 'html-file' if source_type == 'mixed' else source_type
        local = read_local_html(p)
        body_text = '\n\n'.join([x for x in [body_text, local['body_text']] if x]).strip()
        image_urls = unique_keep_order(image_urls + local['image_urls'])
        if not title:
            title = local['title']
        uncertain.extend(local['uncertain'])

    image_urls, gif_urls = split_gifs(image_urls)

    images = []
    for idx, url in enumerate(image_urls, 1):
        item = {
            'index': idx,
            'url': str(url),
            'ocr_text': '',
            'status': 'skipped',
            'uncertain': [],
            'segments': [],
            'segment_mode': False,
            'size': None,
            'full_ocr_text': '',
            'local_path': ''
        }
        if args.ocr_images:
            try:
                local = download_file(str(url))
                ocr = ocr_image_with_segments(local)
                item['ocr_text'] = ocr.get('ocr_text', '')
                item['status'] = ocr.get('status', 'error')
                item['uncertain'].extend(ocr.get('uncertain', []))
                item['segments'] = ocr.get('segments', [])
                item['segment_mode'] = ocr.get('segment_mode', False)
                item['size'] = ocr.get('size')
                item['full_ocr_text'] = ocr.get('full_ocr_text', '')
                item['local_path'] = ocr.get('local_path', local)
                item['variants'] = ocr.get('variants', [])
            except Exception as e:
                item['status'] = 'error'
                item['uncertain'].append(str(e))
        images.append(item)

    gifs = []
    for idx, url in enumerate(gif_urls, 1):
        entry = {
            'index': idx,
            'url': str(url),
            'status': 'placeholder' if args.gif_mode == 'placeholder' else 'skipped',
            'frames': [],
            'deduped_text': '',
            'uncertain': ['远端 GIF 当前仅做占位；如需更强提取，建议先保存为本地文件再走抽帧 OCR。']
        }
        gifs.append(entry)

    local_images = collect_image_inputs(args.image, args.image_dir)
    local_img_results, local_gif_results = process_image_like_inputs(local_images, args.ocr_images, args.gif_mode)
    for item in local_img_results:
        item['index'] = len(images) + 1
        images.append(item)
    for item in local_gif_results:
        item['index'] = len(gifs) + 1
        gifs.append(item)

    if blocked is None:
        blocked = looks_blocked(body_text, title) if body_text else False

    result = {
        'page': {
            'title': title,
            'source_url': source_url,
            'source_type': source_type,
            'extracted_at': now_iso(),
            'blocked': blocked,
        },
        'body_text': body_text,
        'images': images,
        'gifs': gifs,
        'uncertain': unique_keep_order(uncertain),
        'merged_text': merge_text(body_text, images, gifs, dedupe=args.dedupe),
    }

    output = json.dumps(result, ensure_ascii=False, indent=2) if args.format == 'json' else build_markdown(result)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(args.output)
    else:
        print(output)


if __name__ == '__main__':
    main()
