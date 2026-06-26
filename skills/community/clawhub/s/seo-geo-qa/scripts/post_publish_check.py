#!/usr/bin/env python3
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = []
        self.in_title = False
        self.h1 = []
        self.current_h1 = False
        self.meta_description = None
        self.canonical = None
        self.robots = None
        self.json_ld = 0
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()
        if tag == 'title':
            self.in_title = True
        elif tag == 'h1':
            self.current_h1 = True
        elif tag == 'meta':
            name = attrs.get('name', '').lower()
            if name == 'description':
                self.meta_description = attrs.get('content')
            elif name == 'robots':
                self.robots = attrs.get('content', '')
        elif tag == 'link' and 'canonical' in attrs.get('rel', '').split():
            self.canonical = attrs.get('href')
        elif tag == 'script' and attrs.get('type','').lower() == 'application/ld+json':
            self.json_ld += 1
        elif tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'title':
            self.in_title = False
        elif tag == 'h1':
            self.current_h1 = False
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self.in_title:
            self.title.append(data)
        if self.current_h1:
            self.h1.append(data)


def fetch(url: str):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=15) as resp:
            return resp.status, resp.geturl(), resp.read(200000).decode('utf-8', errors='ignore')
    except HTTPError as e:
        return e.code, url, e.read(200000).decode('utf-8', errors='ignore') if hasattr(e, 'read') else ''
    except URLError:
        return 0, url, ''
    except Exception:
        return 0, url, ''


def main():
    ap = argparse.ArgumentParser(description='Post-publish page QA check')
    ap.add_argument('url')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    status, final_url, body = fetch(args.url)
    parser = PageParser()
    parser.feed(body)
    robots = parser.robots or ''
    report = {
        'url': args.url,
        'final_url': final_url,
        'status': status,
        'title': ' '.join(parser.title),
        'h1': ' '.join(parser.h1),
        'meta_description': parser.meta_description,
        'canonical': parser.canonical,
        'robots': robots,
        'json_ld_count': parser.json_ld,
        'link_count': len(parser.links),
        'issues': [],
    }
    if status < 200 or status >= 400:
        report['issues'].append(f'HTTP status {status}')
    if not report['title']:
        report['issues'].append('missing <title>')
    if not report['h1']:
        report['issues'].append('missing H1')
    if not report['meta_description']:
        report['issues'].append('missing meta description')
    if not report['canonical']:
        report['issues'].append('missing canonical')
    if 'noindex' in robots.lower():
        report['issues'].append('page has noindex — will not appear in search results')
    if 'nofollow' in robots.lower():
        report['issues'].append('page has nofollow — link equity will not pass')
    if report['json_ld_count'] == 0:
        report['issues'].append('missing JSON-LD')
    if report['link_count'] < 3:
        report['issues'].append('unexpectedly low link count on published page')

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"## Post-Publish QA\n\n- URL: {report['url']}\n- Final URL: {report['final_url']}\n- Status: {report['status']}\n- Title: {report['title'] or '(missing)'}\n- H1: {report['h1'] or '(missing)'}\n- Meta description: {'present' if report['meta_description'] else 'missing'}\n- Canonical: {report['canonical'] or '(missing)'}\n- Robots: {report['robots'] or '(none)'}\n- JSON-LD blocks: {report['json_ld_count']}\n- Link count: {report['link_count']}\n")
        if report['issues']:
            print('### Issues')
            for item in report['issues']:
                print(f'- {item}')
        else:
            print('### Issues\n- None')

if __name__ == '__main__':
    main()
