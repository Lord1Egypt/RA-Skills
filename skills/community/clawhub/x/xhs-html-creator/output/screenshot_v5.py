import sys, os
shots_dir = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\output\shots'
os.makedirs(shots_dir, exist_ok=True)
from playwright.sync_api import sync_playwright

pages = [
    ('daishengbao_cover_v5.html',    'cover_v5'),
    ('daishengbao_doc_v5.html',       'doc_v5'),
    ('daishengbao_baby1_v5.html',    'baby1_v5'),
    ('daishengbao_baby2_v5.html',    'baby2_v5'),
    ('daishengbao_mom1_v5.html',     'mom1_v5'),
    ('daishengbao_mom2_v5.html',     'mom2_v5'),
    ('daishengbao_ending_v5.html',   'ending_v5'),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 1350})
    for html, name in pages:
        url = f'http://127.0.0.1:8899/{html}'
        page.goto(url, wait_until='networkidle', timeout=15000)
        page.wait_for_timeout(1500)
        out = os.path.join(shots_dir, f'daishengbao_{name}.png')
        page.screenshot(path=out)
        print(f'Saved {name}')
    browser.close()
print('All done!')
