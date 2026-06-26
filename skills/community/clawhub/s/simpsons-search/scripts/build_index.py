#!/usr/bin/env python3
import json
import re
import sys
import urllib.request
from html import unescape
from pathlib import Path

SOURCE_URL = 'https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-simpsons'
SKILL_DIR = Path(__file__).resolve().parent.parent
OUT = SKILL_DIR / 'references' / 'simpsons-episodes.json'

html = urllib.request.urlopen(SOURCE_URL).read().decode('utf-8', errors='replace')

pattern = re.compile(r'<a\s+href="([^"]*episode_scripts\.php\?[^"#]*episode=[^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
seen = set()
episodes = []
for href, label in pattern.findall(html):
    text = re.sub(r'<[^>]+>', '', label)
    text = unescape(text).strip()
    if not text:
        continue
    if href.startswith('/'):
        url = 'https://www.springfieldspringfield.co.uk' + href
    elif href.startswith('http'):
        url = href
    else:
        url = 'https://www.springfieldspringfield.co.uk/' + href.lstrip('/')
    key = (text, url)
    if key in seen:
        continue
    seen.add(key)
    episodes.append({'title': text, 'url': url})

episodes.sort(key=lambda x: x['title'].lower())
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'source': SOURCE_URL, 'count': len(episodes), 'episodes': episodes}, indent=2), encoding='utf-8')
print(json.dumps({'written': str(OUT), 'count': len(episodes)}))
