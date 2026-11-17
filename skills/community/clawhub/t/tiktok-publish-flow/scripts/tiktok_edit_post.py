#!/usr/bin/env python3
"""Edit Alex's #1HourChallenge post: click the pencil icon via mouse coords, set caption, save."""
import argparse, os, pathlib, sys, time
from playwright.sync_api import sync_playwright

PROFILE = os.environ.get('TIKTOK_PROFILE_DIR', str(pathlib.Path.home() / '.tiktok-poster' / 'profile'))
SHOTS = pathlib.Path(os.environ.get('TIKTOK_SHOTS_DIR', str(pathlib.Path.home() / '.tiktok-poster' / 'shots')))

ap = argparse.ArgumentParser(description='Edit an existing TikTok post caption via TikTok Studio')
ap.add_argument('--match', required=True, help='caption fragment identifying the target post row')
ap.add_argument('--caption', required=True, help='full new caption text')
ap.add_argument('--guard', default=None, help='expected fragment of the CURRENT caption (safety check; default: --match)')
ap.add_argument('--tag', default='edit')
a = ap.parse_args()
GUARD = a.guard or a.match

def shot(page, name):
    path = SHOTS / f'{name}.png'
    page.screenshot(path=str(path))
    print(f'SCREENSHOT={path}', flush=True)

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        PROFILE, headless=False, viewport={'width': 1280, 'height': 950},
        user_agent=('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'))
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto('https://www.tiktok.com/tiktokstudio/content', timeout=90000, wait_until='domcontentloaded')
    time.sleep(8)
    shot(page, f'{a.tag}-list.png')

    rect = page.evaluate("""() => {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node, hit = null;
      while ((node = walker.nextNode())) {
        if (node.textContent.trim().startsWith('#1HourChallenge')) { hit = node.parentElement; break; }
      }
      if (!hit) return null;
      let el = hit, row = null;
      while (el && el !== document.body) {
        if (el.querySelectorAll('svg').length >= 4 && el.textContent.length < 200) { row = el; break; }
        el = el.parentElement;
      }
      if (!row) return null;
      const icons = [...row.querySelectorAll('span.px-icon')]
        .map(ic => ic.getBoundingClientRect())
        .filter(r => r.width > 0 && r.x > window.innerWidth * 0.65);
      if (!icons.length) return null;
      icons.sort((a, b) => a.x - b.x);
      const r = icons[0];
      return {x: r.x + r.width / 2, y: r.y + r.height / 2,
              rowText: row.textContent.replace(/\\s+/g, ' ').slice(0, 80)};
    }""")
    if not rect:
        print('NO_ROW_OR_ICON'); sys.exit(2)
    print(f"ICON at ({rect['x']:.0f},{rect['y']:.0f}) row={rect['rowText']!r}", flush=True)
    if a.match not in rect['rowText']:
        print('WRONG_ROW_ABORT'); sys.exit(5)

    page.mouse.click(rect['x'], rect['y'])
    time.sleep(6)
    shot(page, f'{a.tag}-after-pencil.png')
    print(f'URL={page.url}', flush=True)

    # wait for the editor (page or modal)
    cap = None
    end = time.time() + 30
    appeared = False
    while time.time() < end:
        try:
            loc = page.locator('[contenteditable="true"]')
            if loc.count() > 0:
                cap = loc.first
                appeared = True
                break
        except Exception:
            pass
        time.sleep(2)
    if not appeared:
        print('NO_EDIT_EDITOR'); shot(page, f'{a.tag}-no-editor.png'); sys.exit(3)
    time.sleep(2)
    current = (cap.text_content() or '').strip()
    print(f'EDITOR_CURRENT={current[:120]!r}', flush=True)
    if GUARD not in current:
        print('WRONG_POST_ABORT'); sys.exit(5)
    cap.click()
    page.keyboard.press('Control+A')
    page.keyboard.press('Meta+A')
    page.keyboard.type(CAPTION, delay=15)
    print('CAPTION_SET', flush=True)
    time.sleep(2)
    shot(page, f'{a.tag}-caption-set.png')

    page.keyboard.press('Escape')
    time.sleep(1)
    page.mouse.click(400, 300)
    time.sleep(1)

    saved = False
    for label in ('Save', 'Post', 'Salvează'):
        try:
            b = page.locator(f'button:has-text("{label}")')
            if b.count() > 0:
                b.last.click(timeout=6000)
                saved = True
                print(f'SAVE_CLICKED {label}', flush=True)
                break
        except Exception as e:
            print(f'save try {label}: {type(e).__name__}', flush=True)
    if not saved:
        print('NO_SAVE_BUTTON'); shot(page, f'{a.tag}-no-save.png'); sys.exit(4)

    time.sleep(8)
    shot(page, f'{a.tag}-after-save.png')
    print(f'FINAL_URL={page.url}', flush=True)
    print('DONE', flush=True)
    ctx.close()