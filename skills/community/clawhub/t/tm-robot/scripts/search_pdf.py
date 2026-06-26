#!/usr/bin/env python3
"""Search for SVR/Listen content in TM API manual"""
import fitz

pdf_path = r'D:\思锐工作目录\TM机器人\Software_TM-Robot-Management-API-Manual_1.04_1.02_all-languages\TM Robot Management API User Manual v1.04 Rev1.02_EN.pdf'
doc = fitz.open(pdf_path)
print(f'Total pages: {len(doc)}')

keywords = ['SVR', 'Listen Node', 'State Variable', 'Variable Server', '5891', 'port 5891']

found_pages = []
for i in range(len(doc)):
    text = doc[i].get_text()
    for kw in keywords:
        if kw in text:
            found_pages.append((i+1, kw))
            break

print(f'Found {len(found_pages)} pages')
for pg, kw in found_pages[:20]:
    print(f'Page {pg} contains "{kw}"')

# Extract content from first few relevant pages
for pg_num, _ in found_pages[:5]:
    page = doc[pg_num - 1]
    text = page.get_text()
    print(f'\n=== Page {pg_num} ===')
    print(text[:2500])
