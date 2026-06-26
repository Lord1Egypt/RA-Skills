import sys, os
sys.path.insert(0, 'C:/Users/95116/.openclaw/workspace/skills/xhs-content-matrix/output')

shots_dir = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\output\shots'
os.makedirs(shots_dir, exist_ok=True)

from playwright.sync_api import sync_playwright

pages = [
    ('daishengbao_cover_v3.html', 'cover_v3'),
    ('daishengbao_doc_v3.html', 'doc_v3'),
    ('daishengbao_baby1_v3.html', 'baby1_v3'),
    ('daishengbao_baby2_v3.html', 'baby2_v3'),
    ('daishengbao_mom_v3.html', 'mom_v3'),
    ('daishengbao_ending_v3.html', 'ending_v3'),
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
