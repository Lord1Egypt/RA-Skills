#!/usr/bin/env python3
import argparse
import html
import json
import os
import pathlib
import re
import subprocess
import sys
from shutil import which
from typing import Optional

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
DEFAULT_ARCHIVE = pathlib.Path.cwd() / 'webpage-exports'


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def fetch_html(url: str) -> str:
    result = run(['curl', '-L', '--max-time', '30', '-A', UA, url])
    return result.stdout


def pick(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.S | re.I)
    return m.group(1).strip() if m else ''


def html_to_text(fragment: str) -> str:
    fragment = re.sub(r'<script.*?</script>', '', fragment, flags=re.S | re.I)
    fragment = re.sub(r'<style.*?</style>', '', fragment, flags=re.S | re.I)
    fragment = re.sub(r'<noscript.*?</noscript>', '', fragment, flags=re.S | re.I)
    fragment = re.sub(r'<br\s*/?>', '\n', fragment, flags=re.I)
    fragment = re.sub(r'</p>|</section>|</div>|</li>|</h\d>|</tr>|</article>|</main>', '\n', fragment, flags=re.I)
    fragment = re.sub(r'<li[^>]*>', '• ', fragment, flags=re.I)
    fragment = re.sub(r'<[^>]+>', '', fragment)
    fragment = html.unescape(fragment)
    fragment = fragment.replace('\xa0', ' ')
    fragment = re.sub(r'\n{3,}', '\n\n', fragment)
    fragment = re.sub(r'[ \t]+', ' ', fragment)
    return fragment.strip()


def extract_title(raw: str) -> str:
    return (
        pick(r'<meta property="og:title" content="(.*?)"', raw)
        or pick(r'<meta name="twitter:title" content="(.*?)"', raw)
        or pick(r'<title[^>]*>(.*?)</title>', raw)
        or '网页内容提取'
    )


def extract_source(raw: str) -> str:
    return (
        pick(r'id="js_name">\s*(.*?)\s*</a>', raw)
        or pick(r'<meta name="author" content="(.*?)"', raw)
        or pick(r'<meta property="og:article:author" content="(.*?)"', raw)
        or pick(r'<meta property="article:author" content="(.*?)"', raw)
        or ''
    )


def extract_publish(raw: str) -> str:
    return (
        pick(r'id="publish_time"[^>]*>\s*(.*?)\s*</', raw)
        or pick(r'<meta property="article:published_time" content="(.*?)"', raw)
        or pick(r'<time[^>]*datetime="(.*?)"', raw)
        or ''
    )


def body_candidates():
    return [
        ('wechat-js-content', r'<div class="rich_media_content js_underline_content[^"]*"\s+id="js_content"[^>]*>(.*?)</div>'),
        ('article', r'<article[^>]*>(.*?)</article>'),
        ('main', r'<main[^>]*>(.*?)</main>'),
        ('post-content', r'<div[^>]+class="[^"]*(?:post-content|article-content|content-detail|content-main|entry-content|content-wrapper|detail-content)[^"]*"[^>]*>(.*?)</div>'),
        ('body', r'<body[^>]*>(.*?)</body>'),
    ]


NOISE_PATTERNS = [
    r'点击上方.*关注',
    r'上一篇',
    r'下一篇',
    r'责任编辑',
    r'版权所有',
    r'ICP备',
]


def assess_content(text: str, title: str):
    warnings = []
    score = 0
    word_count = len(text)
    lowered = text.lower()

    if word_count >= 800:
        score += 3
    elif word_count >= 300:
        score += 2
    elif word_count >= 120:
        score += 1
    else:
        warnings.append('content_too_short')

    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    long_paragraphs = [p for p in paragraphs if len(p) >= 40]
    if len(long_paragraphs) >= 3:
        score += 2
    elif len(long_paragraphs) >= 1:
        score += 1
    else:
        warnings.append('few_long_paragraphs')

    title_tokens = [t for t in re.split(r'[\s\-_:：，,（）()]+', title) if len(t) >= 2]
    if title_tokens and any(tok in text for tok in title_tokens[:4]):
        score += 1
    else:
        warnings.append('title_tokens_not_found_in_text')

    noise_hits = sum(1 for pat in NOISE_PATTERNS if re.search(pat, text, re.I))
    if noise_hits >= 3 and word_count < 400:
        warnings.append('possible_shell_or_noise_heavy_page')

    if 'javascript' in lowered and word_count < 120:
        warnings.append('possible_dynamic_page')

    if word_count < 120 or 'possible_shell_or_noise_heavy_page' in warnings:
        quality = 'low'
    elif word_count < 300 or len(warnings) >= 2:
        quality = 'medium'
    else:
        quality = 'high'

    needs_browser_review = quality == 'low' or 'possible_dynamic_page' in warnings
    return {
        'word_count': word_count,
        'quality': quality,
        'warnings': warnings,
        'needs_browser_review': needs_browser_review,
        'paragraph_count': len(paragraphs),
        'long_paragraph_count': len(long_paragraphs),
        'score': score,
    }


def extract_best_content(raw: str, title: str):
    best = {
        'candidate': '',
        'content': '',
        'quality': {
            'word_count': 0,
            'score': -1,
            'quality': 'low',
            'warnings': ['no_content'],
            'needs_browser_review': True,
            'paragraph_count': 0,
            'long_paragraph_count': 0,
        },
    }
    for candidate_name, pat in body_candidates():
        body = pick(pat, raw)
        if not body:
            continue
        body_text = html_to_text(body)
        quality = assess_content(body_text, title)
        if quality['score'] > best['quality']['score']:
            best = {
                'candidate': candidate_name,
                'content': body_text,
                'quality': quality,
            }

    if not best['content']:
        fallback_text = html_to_text(raw)
        quality = assess_content(fallback_text, title)
        best = {
            'candidate': 'full-html-fallback',
            'content': fallback_text,
            'quality': quality,
        }
    return best


def chrome_path() -> str:
    candidates = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
    ]
    for c in candidates:
        if pathlib.Path(c).exists():
            return c
    return ''


def fetch_rendered_dom(url: str, virtual_time_budget: int) -> str:
    chrome = chrome_path()
    if not chrome:
        raise RuntimeError('未找到 Chrome/Chromium，无法获取浏览器渲染后的 DOM')
    result = run([
        chrome,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        f'--virtual-time-budget={virtual_time_budget}',
        '--dump-dom',
        url,
    ])
    return result.stdout


def fetch_browser_visible_text(url: str, out_path: pathlib.Path, virtual_time_budget: int):
    chrome = chrome_path()
    if not chrome:
        raise RuntimeError('未找到 Chrome/Chromium，无法执行浏览器文本提取')
    script = """
const fs = require('fs');
(async () => {
  const url = process.argv[1];
  const out = process.argv[2];
  const chrome = process.env.CHROME_BIN;
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ headless: true, executablePath: chrome });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
  await page.evaluate(async () => {
    await new Promise(r => setTimeout(r, 2000));
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(r => setTimeout(r, 1500));
    window.scrollTo(0, 0);
  });
  const payload = await page.evaluate(() => {
    const title = document.title || '';
    const bodyText = (document.body && document.body.innerText) ? document.body.innerText : '';
    const metas = {};
    for (const el of document.querySelectorAll('meta')) {
      const k = el.getAttribute('property') || el.getAttribute('name');
      const v = el.getAttribute('content');
      if (k && v) metas[k] = v;
    }
    return { title, bodyText, metas };
  });
  fs.writeFileSync(out, JSON.stringify(payload), 'utf8');
  await browser.close();
})().catch(err => { console.error(String(err)); process.exit(1); });
"""
    child_env = {
        'PATH': os.environ.get('PATH', ''),
        'HOME': os.environ.get('HOME', ''),
        'CHROME_BIN': chrome,
    }
    subprocess.run([
        'node',
        '-e',
        script,
        url,
        str(out_path),
    ], check=True, env=child_env)


def extract(url: str, raw: str, enable_browser_fallback: bool, virtual_time_budget: int, browser_text_temp: Optional[pathlib.Path] = None):
    title = extract_title(raw)
    source = extract_source(raw)
    publish = extract_publish(raw)
    best = extract_best_content(raw, title)
    text_source = 'static_html'
    browser_fallback_used = False
    browser_fallback_error = ''

    if enable_browser_fallback and best['quality']['needs_browser_review']:
        try:
            rendered = fetch_rendered_dom(url, virtual_time_budget)
            rendered_title = extract_title(rendered) or title
            browser_best = extract_best_content(rendered, rendered_title)
            if browser_best['quality']['score'] > best['quality']['score']:
                title = rendered_title or title
                source = extract_source(rendered) or source
                publish = extract_publish(rendered) or publish
                best = browser_best
                text_source = 'browser_rendered_dom'
                browser_fallback_used = True
        except Exception as e:
            browser_fallback_error = str(e)

    if enable_browser_fallback and best['quality']['needs_browser_review'] and browser_text_temp is not None:
        try:
            fetch_browser_visible_text(url, browser_text_temp, virtual_time_budget)
            browser_payload = json.loads(browser_text_temp.read_text(encoding='utf-8'))
            browser_text = (browser_payload.get('bodyText') or '').strip()
            browser_title = (browser_payload.get('title') or '').strip() or title
            browser_quality = assess_content(browser_text, browser_title)
            if browser_quality['score'] > best['quality']['score']:
                title = browser_title
                source = browser_payload.get('metas', {}).get('author', '') or source
                publish = browser_payload.get('metas', {}).get('article:published_time', '') or publish
                best = {
                    'candidate': 'browser-visible-text',
                    'content': browser_text,
                    'quality': browser_quality,
                }
                text_source = 'browser_visible_text'
                browser_fallback_used = True
        except Exception as e:
            if browser_fallback_error:
                browser_fallback_error += ' || '
            browser_fallback_error += f'browser_visible_text:{e}'

    return {
        'title': title,
        'source': source,
        'publish': publish,
        'url': url,
        'content': best['content'],
        'content_candidate': best['candidate'],
        'content_quality': best['quality'],
        'text_source': text_source,
        'browser_fallback_used': browser_fallback_used,
        'browser_fallback_error': browser_fallback_error,
    }


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\n\r]+', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:80] or 'webpage-export'


def build_text(doc: dict) -> str:
    warnings = ', '.join(doc['content_quality']['warnings']) if doc['content_quality']['warnings'] else '无'
    return (
        f"标题：{doc['title']}\n"
        f"来源：{doc['source'] or '未提取到'}\n"
        f"发布时间：{doc['publish'] or '未直接提取到'}\n"
        f"原始链接：{doc['url']}\n"
        f"文本来源：{doc['text_source']}\n"
        f"正文候选：{doc['content_candidate']}\n"
        f"提取质量：{doc['content_quality']['quality']}\n"
        f"字数：{doc['content_quality']['word_count']}\n"
        f"告警：{warnings}\n\n"
        f"正文：\n\n{doc['content']}\n"
    )


def write_txt(text: str, path: pathlib.Path):
    path.write_text(text, encoding='utf-8')


def write_json(payload: dict, path: pathlib.Path):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def write_docx(txt_path: pathlib.Path, docx_path: pathlib.Path):
    if which('textutil') is None:
        raise RuntimeError('textutil 不可用，无法生成 docx')
    subprocess.run(['textutil', '-convert', 'docx', str(txt_path), '-output', str(docx_path)], check=True)


def write_pdf(url: str, pdf_path: pathlib.Path, virtual_time_budget: int):
    chrome = chrome_path()
    if not chrome:
        raise RuntimeError('未找到 Chrome/Chromium，无法生成 PDF')
    subprocess.run([
        chrome,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        f'--virtual-time-budget={virtual_time_budget}',
        f'--print-to-pdf={pdf_path}',
        url,
    ], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--outdir', default=str(DEFAULT_ARCHIVE / 'temp'))
    ap.add_argument('--basename', default='')
    ap.add_argument('--docx', action='store_true')
    ap.add_argument('--pdf', action='store_true')
    ap.add_argument('--json', action='store_true', help='always emit metadata json (default true)')
    ap.add_argument('--no-json', dest='json', action='store_false')
    ap.add_argument('--virtual-time-budget', type=int, default=15000)
    ap.add_argument('--disable-browser-fallback', action='store_true')
    ap.set_defaults(json=True)
    args = ap.parse_args()

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    metadata = {
        'url': args.url,
        'status': 'failed',
        'title': '',
        'source': '',
        'publish': '',
        'content_candidate': '',
        'content_quality': {},
        'text_source': '',
        'browser_fallback_used': False,
        'browser_fallback_error': '',
        'paths': {},
        'warnings': [],
        'steps': {
            'txt': 'pending',
            'docx': 'skipped',
            'pdf': 'skipped',
        },
    }

    raw = fetch_html(args.url)
    browser_text_temp = outdir / '.browser_text_tmp.json'
    doc = extract(args.url, raw, not args.disable_browser_fallback, args.virtual_time_budget, browser_text_temp=browser_text_temp)
    basename = args.basename or sanitize_filename(doc['title'])
    txt_path = outdir / f'{basename}.txt'
    json_path = outdir / f'{basename}.json'

    metadata.update({
        'title': doc['title'],
        'source': doc['source'],
        'publish': doc['publish'],
        'content_candidate': doc['content_candidate'],
        'content_quality': doc['content_quality'],
        'text_source': doc['text_source'],
        'browser_fallback_used': doc['browser_fallback_used'],
        'browser_fallback_error': doc['browser_fallback_error'],
        'paths': {'txt': str(txt_path)},
    })
    metadata['warnings'].extend(doc['content_quality']['warnings'])
    if doc['content_quality']['needs_browser_review']:
        metadata['warnings'].append('needs_browser_review')
    if doc['browser_fallback_used']:
        metadata['warnings'].append('browser_fallback_used')
    if doc['browser_fallback_error']:
        metadata['warnings'].append(f'browser_fallback_error:{doc["browser_fallback_error"]}')

    text = build_text(doc)
    write_txt(text, txt_path)
    metadata['steps']['txt'] = 'success'

    if args.docx:
        docx_path = outdir / f'{basename}.docx'
        metadata['paths']['docx'] = str(docx_path)
        try:
            write_docx(txt_path, docx_path)
            metadata['steps']['docx'] = 'success'
        except Exception as e:
            metadata['steps']['docx'] = 'failed'
            metadata['warnings'].append(f'docx_failed:{e}')

    if args.pdf:
        pdf_path = outdir / f'{basename}.pdf'
        metadata['paths']['pdf'] = str(pdf_path)
        try:
            write_pdf(args.url, pdf_path, args.virtual_time_budget)
            if pdf_path.exists() and pdf_path.stat().st_size > 1024:
                metadata['steps']['pdf'] = 'success'
            else:
                metadata['steps']['pdf'] = 'failed'
                metadata['warnings'].append('pdf_failed:missing_or_too_small')
        except Exception as e:
            metadata['steps']['pdf'] = 'failed'
            metadata['warnings'].append(f'pdf_failed:{e}')

    succeeded = [k for k, v in metadata['steps'].items() if v == 'success']
    if metadata['steps']['txt'] == 'success' and len(succeeded) == 1 and (args.docx or args.pdf):
        metadata['status'] = 'partial'
    elif metadata['steps']['txt'] == 'success':
        metadata['status'] = 'success'
    else:
        metadata['status'] = 'failed'

    if args.json:
        write_json(metadata, json_path)
        metadata['paths']['json'] = str(json_path)

    print(f'TXT={txt_path}')
    print(f'TITLE={doc["title"]}')
    print(f'SOURCE={doc["source"]}')
    print(f'TEXT_SOURCE={doc["text_source"]}')
    print(f'QUALITY={doc["content_quality"]["quality"]}')
    print(f'WORDS={doc["content_quality"]["word_count"]}')
    print(f'STATUS={metadata["status"]}')
    if args.json:
        print(f'JSON={json_path}')

    if args.docx and 'docx' in metadata['paths'] and metadata['steps']['docx'] == 'success':
        print(f'DOCX={metadata["paths"]["docx"]}')

    if args.pdf and 'pdf' in metadata['paths'] and metadata['steps']['pdf'] == 'success':
        print(f'PDF={metadata["paths"]["pdf"]}')

    if metadata['warnings']:
        print('WARNINGS=' + ' | '.join(metadata['warnings']))


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr or str(e))
        sys.exit(e.returncode or 1)
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)
