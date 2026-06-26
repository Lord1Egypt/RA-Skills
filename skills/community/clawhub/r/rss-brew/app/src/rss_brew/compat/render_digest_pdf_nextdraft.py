#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from typing import Any, Dict, List


def parse_digest(md_path: Path) -> Dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = "RSS Brew Daily Digest"
    date = md_path.stem.replace("daily-digest-", "")
    articles: List[Dict[str, Any]] = []
    others: List[Dict[str, Any]] = []
    section = None
    current: Dict[str, Any] | None = None
    last_field: str | None = None

    field_prefixes = [
        ('- Score:', 'score'),
        ('- Category:', 'category'),
        ('- Source:', 'source'),
        ('- URL:', 'url'),
        ('- English Summary:', 'en_summary'),
        ('- 中文摘要:', 'zh_summary'),
        ('- Deep Analysis:', 'deep_analysis'),
        ('- 备注:', 'note'),
    ]

    for raw in lines:
        line = raw.rstrip()
        if line.startswith('# RSS Brew Daily Digest'):
            m = re.search(r'(\d{4}-\d{2}-\d{2})', line)
            if m:
                date = m.group(1)
            title = line.replace('# ', '').strip()
            continue
        if line == '## Deep Set':
            section = 'deep'
            continue
        if line == '## Other New Articles':
            if current:
                (articles if section == 'deep' else others).append(current)
                current = None
            section = 'other'
            continue
        if line.startswith('## '):
            if current:
                (articles if section == 'deep' else others).append(current)
                current = None
            section = None
            continue
        if line.startswith('### '):
            if current:
                (articles if section == 'deep' else others).append(current)
            current = {
                'title': line[4:].strip(), 'score': '', 'category': '', 'source': '', 'url': '',
                'en_summary': '', 'zh_summary': '', 'deep_analysis': [], 'underwater': '', 'golden_quotes': [], 'note': ''
            }
            last_field = None
            continue
        if section == 'other' and line.startswith('- '):
            if current:
                others.append(current)
            current = {
                'title': line[2:].strip(), 'score': '', 'category': '', 'source': '', 'url': '',
                'en_summary': '', 'zh_summary': '', 'deep_analysis': [], 'underwater': '', 'golden_quotes': [], 'note': ''
            }
            last_field = None
            continue
        if current is None:
            continue

        matched = False
        candidate = line.lstrip() if section == 'other' else line
        for prefix, key in field_prefixes:
            if candidate.startswith(prefix):
                val = candidate[len(prefix):].strip()
                current[key] = [] if key == 'deep_analysis' else val
                last_field = key
                matched = True
                break
        if matched:
            continue

        if line.startswith('  - '):
            item = line[4:].strip()
            if last_field == 'deep_analysis':
                if item.startswith('Underwater Insights:'):
                    current['underwater'] = item.replace('Underwater Insights:', '', 1).strip()
                elif item == 'Golden Quotes:':
                    last_field = 'golden_quotes'
                else:
                    current['deep_analysis'].append(item)
            elif last_field == 'golden_quotes':
                current['golden_quotes'].append(item.lstrip('- ').strip().strip('"'))
            elif last_field:
                current[last_field] += ('\n' if current[last_field] else '') + item
            continue
        if line.startswith('    - ') and last_field == 'golden_quotes':
            current['golden_quotes'].append(line[6:].strip().strip('"'))
            continue
        if line.strip() and last_field:
            if last_field == 'deep_analysis':
                current['deep_analysis'].append(line.strip())
            elif last_field == 'golden_quotes':
                current['golden_quotes'].append(line.strip().strip('"'))
            else:
                current[last_field] += ('\n' if current[last_field] else '') + line.strip()

    if current:
        (articles if section == 'deep' else others).append(current)

    return {"title": title, "date": date, "articles": articles, "others": others}


def esc(s: str) -> str:
    return html.escape(s or '')


def linkify(s: str) -> str:
    s = esc(s)
    return re.sub(r'(https?://[^\s<]+)', r'<a href="\1">\1</a>', s)


def paras(text: str, cls: str = '') -> str:
    if not text:
        return ''
    bits = [b.strip() for b in text.split('\n') if b.strip()]
    return ''.join(f'<p class="{cls}">{linkify(b)}</p>' for b in bits)


def bullets(items: List[str], cls: str = '') -> str:
    if not items:
        return ''
    lis = ''.join(f'<li>{linkify(x)}</li>' for x in items if x.strip())
    return f'<ul class="{cls}">{lis}</ul>' if lis else ''


def render_html(data: Dict[str, Any]) -> str:
    title = data['title']
    date = data['date']
    articles = data['articles']
    others = data['others']

    stats_html = f'''
    <div class="stats">
      <div class="stat"><span class="n">{len(articles)}</span><span class="k">Deep Set</span></div>
      <div class="stat"><span class="n">{len(others)}</span><span class="k">Other Articles</span></div>
    </div>
    '''

    article_blocks = []
    for i, a in enumerate(articles, 1):
        meta = ' · '.join(x for x in [a['score'], a['category'], a['source']] if x)
        quote_html = ''.join(f'<blockquote>{linkify(q)}</blockquote>' for q in a['golden_quotes'])
        article_blocks.append(f'''
        <article class="entry">
          <div class="eyebrow">Deep Set #{i}</div>
          <h2>{esc(a['title'])}</h2>
          <div class="meta">{esc(meta)}</div>
          <section><h3>English Summary</h3>{paras(a['en_summary'])}</section>
          <section><h3>中文摘要</h3>{paras(a['zh_summary'], 'zh')}</section>
          <section><h3>Deep Analysis</h3>{bullets(a['deep_analysis'], 'analysis')}</section>
          {f'<section><h3>Underwater Insight</h3>{paras(a["underwater"], "zh")}</section>' if a['underwater'] else ''}
          {f'<section><h3>Quote</h3>{quote_html}</section>' if quote_html else ''}
          {f'<div class="source-link"><a href="{esc(a["url"])}">Source</a></div>' if a['url'] else ''}
        </article>
        ''')

    other_blocks = []
    for a in others:
        meta = ' · '.join(x for x in [a['score'], a['source']] if x)
        summary = a['note'] or a['en_summary'] or a['zh_summary']
        other_blocks.append(f'''
        <div class="skim-item">
          <h4>{esc(a['title'])}</h4>
          <div class="meta slim">{esc(meta)}</div>
          {paras(summary)}
          {f'<div class="source-link small"><a href="{esc(a["url"])}">Source</a></div>' if a['url'] else ''}
        </div>
        ''')

    return f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{esc(title)}</title>
<style>
@page {{ size: A4; margin: 16mm 14mm 18mm; }}
body {{ font-family: "Noto Serif CJK SC", "Source Han Serif SC", "Songti SC", serif; color: #161616; background: #fff; font-size: 11pt; line-height: 1.72; }}
.wrap {{ max-width: 780px; margin: 0 auto; }}
.header {{ margin-bottom: 28px; border-bottom: 1px solid #d8d8d8; padding-bottom: 18px; }}
.kicker {{ font-family: "Noto Sans CJK SC", "Source Han Sans SC", sans-serif; letter-spacing: .08em; text-transform: uppercase; font-size: 9pt; color: #666; margin-bottom: 8px; }}
h1 {{ font-size: 28pt; line-height: 1.15; margin: 0 0 8px; font-weight: 700; }}
.deck {{ font-size: 12.5pt; color: #444; max-width: 680px; margin: 0 0 10px; }}
.date {{ font-family: "Noto Sans CJK SC", sans-serif; font-size: 9.5pt; color: #777; }}
.stats {{ margin-top: 18px; font-size: 0; }}
.stat {{ display: inline-block; vertical-align: top; border-left: 2px solid #111; padding-left: 10px; margin-right: 28px; min-width: 110px; }}
.stat .n {{ display:block; font-family: "Noto Sans CJK SC", sans-serif; font-size: 17pt; font-weight: 700; }}
.stat .k {{ display:block; font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.5pt; letter-spacing: .05em; text-transform: uppercase; color:#666; }}
.section-title {{ font-family: "Noto Sans CJK SC", sans-serif; font-size: 11pt; letter-spacing: .08em; text-transform: uppercase; color:#555; margin: 26px 0 10px; }}
.entry {{ margin: 0 0 34px; padding-bottom: 26px; border-bottom: 1px solid #ececec; }}
.eyebrow {{ font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color:#888; margin-bottom: 6px; }}
h2 {{ font-size: 19pt; line-height: 1.22; margin: 0 0 8px; font-weight: 700; }}
h3 {{ font-family: "Noto Sans CJK SC", sans-serif; font-size: 9.2pt; text-transform: uppercase; letter-spacing: .06em; color:#666; margin: 16px 0 6px; }}
h4 {{ font-size: 13.5pt; margin: 0 0 4px; }}
.meta {{ font-family: "Noto Sans CJK SC", sans-serif; font-size: 9pt; color:#707070; margin-bottom: 10px; }}
.meta.slim {{ margin-bottom: 6px; }}
p {{ margin: 0 0 10px; }}
p.zh {{ font-family: "Noto Serif CJK SC", "Source Han Serif SC", serif; }}
ul.analysis {{ margin: 0; padding-left: 18px; }}
ul.analysis li {{ margin: 0 0 8px; }}
blockquote {{ margin: 10px 0; padding: 0 0 0 14px; border-left: 3px solid #111; font-style: italic; color:#333; }}
a {{ color:#111; text-decoration: none; border-bottom: 1px solid #bbb; }}
.source-link {{ margin-top: 10px; font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.5pt; color:#666; }}
.source-link.small {{ margin-top: 6px; }}
.skim-item {{ margin: 0 0 18px; padding-bottom: 14px; border-bottom: 1px solid #f0f0f0; }}
.footer {{ margin-top: 28px; font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.5pt; color:#777; border-top: 1px solid #ddd; padding-top: 10px; }}
</style>
</head>
<body>
<div class="wrap">
<header class="header">
<div class="kicker">RSS Brew · Daily Digest</div>
<h1>{esc(title)}</h1>
<div class="deck">A curated daily briefing with deep-set analysis, bilingual summaries, and editorial-style presentation inspired by modern newsletter layouts.</div>
<div class="date">{esc(date)}</div>
{stats_html}
</header>
<div class="section-title">Deep Set</div>
{''.join(article_blocks)}
<div class="section-title">Other New Articles</div>
{''.join(other_blocks)}
<div class="footer">Generated by RSS-Brew · NextDraft-inspired layout · Chinese fonts embedded with Noto CJK.</div>
</div>
</body>
</html>'''


def main() -> None:
    ap = argparse.ArgumentParser(description='Render RSS-Brew digest markdown to NextDraft-style PDF')
    ap.add_argument('--input', required=True, help='Path to daily-digest-YYYY-MM-DD.md')
    ap.add_argument('--html-output', required=False, help='Optional HTML output path')
    ap.add_argument('--pdf-output', required=True, help='PDF output path')
    args = ap.parse_args()

    md_path = Path(args.input)
    html_path = Path(args.html_output) if args.html_output else Path(args.pdf_output).with_suffix('.html')
    pdf_path = Path(args.pdf_output)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    data = parse_digest(md_path)
    html_doc = render_html(data)
    html_path.write_text(html_doc, encoding='utf-8')

    import subprocess
    subprocess.run(['weasyprint', str(html_path), str(pdf_path)], check=True)
    print(pdf_path)


if __name__ == '__main__':
    main()
