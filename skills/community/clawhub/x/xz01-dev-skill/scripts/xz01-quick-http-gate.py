#!/usr/bin/env python3
import re, sys, urllib.request

URLS = sys.argv[1:] or [
    'https://www.900az.com/',
    'https://www.900az.com/yyalzos001/6064.html',
    'https://www.900az.com/zoszx04/3102.html',
    'https://m.900az.com/azos08/620.html',
    'https://m.900az.com/azos/',
]
MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1'
PC_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36'
BAD_SUBSTRINGS = ['系统发生错误', 'TemplateNotFound', 'ErrorException', 'Call Stack', 'think_page_trace', 'cms/page/index/id', 'https://www.900az.comhttps', 'https://m.900az.comhttps', 'https//m.900az.com']
failed = False
for url in URLS:
    ua = MOBILE_UA if '://m.' in url else PC_UA
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            status = r.status
            body = r.read().decode('utf-8', 'ignore')
    except Exception as e:
        print(f'FAIL fetch {url} {type(e).__name__}: {e}')
        failed = True
        continue
    issues = []
    if status != 200:
        issues.append(f'http={status}')
    for bad in BAD_SUBSTRINGS:
        if bad in body:
            issues.append(f'bad:{bad}')
    if '://m.' in url and ('target="_blank"' in body or "target='_blank'" in body):
        issues.append('mobile_target_blank')
    if url.endswith('/') and '://www.' in url:
        real_links = len(re.findall(r'https://www\.900az\.com/[^"\'<>\s]+/(["\'])', body))
    else:
        real_links = len(re.findall(r'https://(?:www|m)\.900az\.com/[^"\'<>\s]+\.html', body))
    imgs = len(re.findall(r'<img\b[^>]+src=["\'](?!data:)(?![^"\']*app-\d+\.svg)(?![^"\']*banner-\d+\.svg)(?![^"\']*topic-\d+\.svg)', body, re.I))
    empty_count = body.count('暂无')
    if url in ('https://www.900az.com/', 'https://m.900az.com/azos/') and real_links == 0:
        issues.append('no_real_links')
    if url == 'https://www.900az.com/' and imgs == 0:
        issues.append('no_real_images')
    status_text = 'PASS' if not issues else 'FAIL'
    print(f'{status_text} {url} http={status} links={real_links} imgs={imgs} empty={empty_count} issues={"|".join(issues) if issues else "none"}')
    failed = failed or bool(issues)
sys.exit(1 if failed else 0)
