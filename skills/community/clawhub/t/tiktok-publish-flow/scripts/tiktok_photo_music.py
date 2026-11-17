#!/usr/bin/env python3
"""Single photo post to TikTok Studio with a TikTok music track selected."""
import argparse, os, pathlib, sys, time
from playwright.sync_api import sync_playwright

PROFILE = os.environ.get('TIKTOK_PROFILE_DIR', str(pathlib.Path.home() / '.tiktok-poster' / 'profile'))
SHOTS = pathlib.Path(os.environ.get('TIKTOK_SHOTS_DIR', str(pathlib.Path.home() / '.tiktok-poster' / 'shots')))

def shot(page, name):
    path = SHOTS / f'{name}.png'
    page.screenshot(path=str(path))
    print(f'SCREENSHOT={path}', flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', required=True)
    ap.add_argument('--caption', required=True)
    ap.add_argument('--query', default='golden hour')
    ap.add_argument('--tag', default='photo01')
    a = ap.parse_args()
    img = pathlib.Path(a.image)
    if not img.exists():
        print(f'ERR: missing {img}'); sys.exit(1)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=False, viewport={'width': 1280, 'height': 950},
            user_agent=('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'))
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto('https://www.tiktok.com/tiktokstudio/upload', timeout=90000, wait_until='domcontentloaded')

        # switch to the Photos tab BEFORE touching the file input
        photo_tab = None
        end = time.time() + 30
        while time.time() < end:
            try:
                t = page.get_by_text('Photos', exact=True)
                if t.count() > 0:
                    photo_tab = t.first
                    break
            except Exception:
                pass
            time.sleep(2)
        if photo_tab is None:
            print('NO_PHOTOS_TAB'); shot(page, f'{a.tag}-no-photos-tab.png'); sys.exit(7)
        photo_tab.click(timeout=8000)
        print('PHOTOS_TAB_CLICKED', flush=True)
        time.sleep(3)

        fi = None
        end = time.time() + 45
        while time.time() < end:
            try:
                loc = page.locator('input[type="file"]')
                if loc.count() > 0:
                    fi = loc.first; break
            except Exception:
                pass
            time.sleep(2)
        if fi is None:
            print('LOGIN_OR_FORM_TIMEOUT'); shot(page, f'{a.tag}-no-form.png'); sys.exit(2)

        fi.set_input_files(str(img), timeout=60000)
        print('FILE_SET', flush=True)

        cap = None
        end = time.time() + 120
        appeared = False
        while time.time() < end:
            try:
                cap = page.locator('[contenteditable="true"]').first
                if cap.count() > 0:
                    appeared = True
                    break
            except Exception:
                pass
            time.sleep(3)
        if not appeared:
            print('NO_CAPTION_EDITOR'); shot(page, f'{a.tag}-no-editor.png'); sys.exit(3)
        time.sleep(3)
        cap.click(); cap.fill('')
        page.keyboard.type(a.caption, delay=15)
        print('CAPTION_SET', flush=True)
        time.sleep(2)

        page.keyboard.press('Escape')
        time.sleep(1)
        page.mouse.click(400, 300)
        time.sleep(1)
        print('POPUP_CLOSED', flush=True)
        shot(page, f'{a.tag}-before-sound.png')

        # --- open the sound picker (real button) ---
        opened = False
        for sel in ('button:has-text("Add sound")', 'button:has-text("Adaugă sunet")'):
            try:
                b = page.locator(sel)
                if b.count() > 0:
                    b.first.click(timeout=6000)
                    opened = True
                    print(f'SOUND_OPENED {sel}', flush=True)
                    break
            except Exception as e:
                print(f'sound try {sel}: {type(e).__name__}', flush=True)
        if not opened:
            print('NO_SOUND_PICKER'); shot(page, f'{a.tag}-no-sound.png'); sys.exit(4)

        # wait for the modal's search input (scoped to modal/dialog or placeholder)
        sbox = None
        end = time.time() + 20
        while time.time() < end:
            try:
                for sel in ('[role="dialog"] input', '[class*="modal"] input',
                            'input[placeholder*="earch" i]', 'input[placeholder*="ound" i]'):
                    loc = page.locator(sel)
                    if loc.count() > 0:
                        sbox = loc.first
                        break
                if sbox is not None and sbox.count() > 0:
                    break
            except Exception:
                pass
            time.sleep(2)
        shot(page, f'{a.tag}-sound-panel.png')
        if sbox is None:
            print('NO_SEARCH_BOX'); shot(page, f'{a.tag}-no-search.png'); sys.exit(5)

        sbox.click(); sbox.fill(a.query)
        time.sleep(4)
        shot(page, f'{a.tag}-search-results.png')

        # --- pick a track: refine to 'golden hour jvke' suggestion, then JS-click a visible Use ---
        picked = False
        try:
            sug = page.get_by_text('golden hour jvke', exact=False)
            if sug.count() > 0:
                sug.first.click(timeout=4000)
                time.sleep(3)
                print('SUGGESTION_JVKE_CLICKED', flush=True)
        except Exception as e:
            print(f'suggestion err {type(e).__name__}', flush=True)
        shot(page, f'{a.tag}-search-results.png')

        for attempt in range(4):
            res = page.evaluate("""() => {
              const btns = [...document.querySelectorAll('button')]
                .filter(b => /^Use/.test((b.textContent||'').trim()) && b.offsetParent !== null);
              if (!btns.length) return null;
              const jvke = btns.find(b => (b.closest('div')?.textContent||'').toLowerCase().includes('jvke'));
              const target = jvke || btns[0];
              target.click();
              return target.textContent.trim();
            }""")
            if res:
                picked = True
                print(f'TRACK_USE_JS {res} (attempt {attempt})', flush=True)
                break
            time.sleep(3)
        shot(page, f'{a.tag}-picked.png')
        if not picked:
            print('NO_TRACK_PICKED'); sys.exit(6)

        # close panel if still open
        try:
            close = page.locator('[role="dialog"] [aria-label="Close"], [class*="modal"] [aria-label="Close"]')
            if close.count() > 0:
                close.first.click(timeout=3000)
            else:
                page.keyboard.press('Escape')
        except Exception:
            page.keyboard.press('Escape')
        time.sleep(2)

        page.mouse.wheel(0, 900)
        time.sleep(2)
        for label in ('Toată lumea', 'Everyone'):
            try:
                els = page.get_by_text(label, exact=False)
                if els.count() > 0:
                    (els.last if els.count() > 1 else els.first).click(timeout=4000)
                    print(f'PRIVACY_SET {label}', flush=True); break
            except Exception as e:
                print('privacy try', label, type(e).__name__, flush=True)
        time.sleep(1)

        shot(page, f'{a.tag}-settings.png')
        page.locator('button:has-text("Post")').last.click(timeout=8000)
        print('POST_CLICKED', flush=True)

        clicked_now = False
        end = time.time() + 30
        while time.time() < end:
            try:
                pn = page.locator('button:has-text("Post now")')
                if pn.count() > 0:
                    pn.first.click(timeout=3000)
                    clicked_now = True
                    print('POST_NOW_CLICKED', flush=True)
                    break
            except Exception:
                pass
            if '/content' in page.url:
                break
            time.sleep(1)
        print('DIALOG_HANDLED clicked_now=', clicked_now, flush=True)

        end = time.time() + 90
        while time.time() < end:
            if '/content' in page.url:
                print('REDIRECTED_TO_CONTENT', flush=True); break
            time.sleep(2)
        time.sleep(10)
        page.reload(timeout=60000)
        time.sleep(6)
        shot(page, f'{a.tag}-final.png')
        print(f'FINAL_URL={page.url}', flush=True)
        print('DONE', flush=True)
        ctx.close()

if __name__ == '__main__':
    main()