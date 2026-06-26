#!/usr/bin/env python3
"""Crawl same-host PC/mobile URLs and fail on HTTP 5xx, ThinkPHP errors, malformed links, empty data pages."""
from __future__ import annotations
import argparse, collections, html.parser, json, re, sys, time, urllib.parse, urllib.request

PC_UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36'
MOBILE_UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 Version/17.4 Mobile/15E148 Safari/604.1'
BAD = ['系统发生错误','TemplateNotFound','ErrorException','Call Stack','think_page_trace','cms/page/index/id','cms/Page/index','mobile/Page/index','https://www.900az.comhttps','https://m.900az.comhttps','https//m.900az.com']
class LinkParser(html.parser.HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.imgs=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=='a' and d.get('href'): self.links.append(d['href'])
        if tag=='img' and d.get('src'): self.imgs.append(d['src'])

def fetch(url, timeout=10):
    ua = MOBILE_UA if '://m.' in url else PC_UA
    req=urllib.request.Request(url,headers={'User-Agent':ua})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.geturl(), r.read().decode('utf-8','ignore')

def same_host_abs(base, href):
    if not href or href.startswith(('javascript:','mailto:','#')): return None
    u=urllib.parse.urljoin(base, href)
    pu=urllib.parse.urlparse(u)
    if pu.scheme not in ('http','https'): return None
    if pu.netloc not in ('www.900az.com','m.900az.com'): return None
    return urllib.parse.urlunparse((pu.scheme,pu.netloc,pu.path,'','',''))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--max-pages',type=int,default=120)
    ap.add_argument('--json-out')
    ap.add_argument('urls', nargs='*')
    args=ap.parse_args()
    seeds=args.urls or ['https://www.900az.com/','https://m.900az.com/']
    q=collections.deque(seeds); seen=set(); results=[]; issues=[]
    while q and len(seen)<args.max_pages:
        url=q.popleft()
        if url in seen: continue
        seen.add(url)
        try:
            status, final, body=fetch(url)
        except Exception as e:
            issues.append({'url':url,'type':'fetch_error','error':type(e).__name__+': '+str(e)})
            continue
        parser=LinkParser(); parser.feed(body)
        page_issues=[]
        if status>=500: page_issues.append(f'http_{status}')
        for b in BAD:
            if b in body: page_issues.append('bad:'+b)
        if '://m.' in url and re.search(r"target\s*=\s*['\"]_blank['\"]", body, re.I): page_issues.append('mobile_target_blank')
        if body.count('暂无')>=8: page_issues.append('many_empty_placeholders')
        # Avoid false positives such as "10款" containing the substring "0款".
        if re.search(r'(?<!\\d)0\\s*款', body) and ('/azos/' in url or '/gzos/' in url): page_issues.append('zero_count_list')
        links=[same_host_abs(final, h) for h in parser.links]
        links=[x for x in links if x]
        for l in links[:300]:
            if l not in seen and len(seen)+len(q)<args.max_pages and (l.endswith('/') or l.endswith('.html')):
                q.append(l)
        row={'url':url,'status':status,'final':final,'links':len(links),'imgs':len(parser.imgs),'empty':body.count('暂无'),'issues':page_issues}
        results.append(row)
        if page_issues: issues.append({'url':url,'type':'page_issues','issues':page_issues})
        time.sleep(0.05)
    out={'checked':len(results),'issue_count':len(issues),'issues':issues,'results':results}
    if args.json_out:
        open(args.json_out,'w').write(json.dumps(out,ensure_ascii=False,indent=2))
    for r in results:
        print(('PASS' if not r['issues'] else 'FAIL'), r['url'], 'http='+str(r['status']), 'links='+str(r['links']), 'imgs='+str(r['imgs']), 'empty='+str(r['empty']), 'issues='+'|'.join(r['issues']) if r['issues'] else 'issues=none')
    if issues:
        print('FAIL full_url_scan issues=',len(issues),file=sys.stderr); return 1
    print('PASS full_url_scan checked=',len(results)); return 0
if __name__=='__main__': raise SystemExit(main())
