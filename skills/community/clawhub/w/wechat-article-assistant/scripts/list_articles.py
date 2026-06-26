#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io, json, subprocess
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

result = subprocess.run(
    [sys.executable, 'scripts/wechat_article_assistant.py', 
     'list-account-articles', '--fakeid', 'MzA4NTMxODEzOQ==', 
     '--remote', 'true', '--count', '5', '--json'],
    capture_output=True
)

# Try UTF-8 first, fallback to GBK (Windows Chinese encoding)
try:
    output = result.stdout.decode('utf-8')
except UnicodeDecodeError:
    output = result.stdout.decode('gbk')

data = json.loads(output)
articles = data['data']['articles'][:5]

for i, a in enumerate(articles, 1):
    t = datetime.fromtimestamp(a['create_time']).strftime('%Y-%m-%d %H:%M')
    title = a['title']
    link = a['link']
    print(f"{i}. [{t}] {title}")
    print(f"   {link}")
    print()
