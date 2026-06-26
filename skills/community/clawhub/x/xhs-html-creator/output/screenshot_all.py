import subprocess, time, os

pages = [
    ('daishengbao_cover_v2.html', 'cover_v2'),
    ('daishengbao_doc_v2.html', 'doc_v2'),
    ('daishengbao_baby1_v2.html', 'baby1_v2'),
    ('daishengbao_baby2_v2.html', 'baby2_v2'),
    ('daishengbao_mom_v2.html', 'mom_v2'),
    ('daishengbao_ending_v2.html', 'ending_v2'),
]

# Start CDP screenshot via a simple approach - use playwright python
from playwright.sync_api import sync_playwright

shot_dir = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\output\shots'
os.makedirs(shot_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 1350})
    
    for html_file, name in pages:
        url = f'http://127.0.0.1:8899/{html_file}'
        page.goto(url, wait_until='networkidle', timeout=10000)
        page.wait_for_timeout(1000)
        out_path = os.path.join(shot_dir, f'daishengbao_{name}.png')
        page.screenshot(path=out_path)
        print(f'Saved: {out_path}')
    
    browser.close()

print('Done!')
