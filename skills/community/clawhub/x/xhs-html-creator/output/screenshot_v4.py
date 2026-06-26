import sys, os
shots_dir = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\output\shots'
os.makedirs(shots_dir, exist_ok=True)
from playwright.sync_api import sync_playwright

pages = [
    ('daishengbao_cover_v4.html', 'cover_v4'),
    ('daishengbao_doc_v4.html', 'doc_v4'),
    ('daishengbao_baby1_v4.html', 'baby1_v4'),
    ('daishengbao_baby2_v4.html', 'baby2_v4'),
    ('daishengbao_mom_v4.html', 'mom_v4'),
    ('daishengbao_ending_v4.html', 'ending_v4'),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 1350})
    for html_file, name in pages:
        url = f'http://127.0.0.1:8899/{html_file}'
        page.goto(url, wait_until='networkidle', timeout=15000)
        page.wait_for_timeout(1500)
        out_path = os.path.join(shots_dir, f'daishengbao_{name}.png')
        page.screenshot(path=out_path)
        print(f'Saved: {out_path}')
    browser.close()

print('All done!')
