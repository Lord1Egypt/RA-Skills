#!/usr/bin/env python3
"""TikTok upload flow v3: like v2 but handles the 'Continue to post?' check dialog
by clicking 'Post now' immediately when it appears."""
import argparse, os, pathlib, sys, time
from playwright.sync_api import sync_playwright

PROFILE = os.environ.get('TIKTOK_PROFILE_DIR', str(pathlib.Path.home() / '.tiktok-poster' / 'profile'))
SHOTS = pathlib.Path(os.environ.get('TIKTOK_SHOTS_DIR', str(pathlib.Path.home() / '.tiktok-poster' / 'shots')))

def shot(page, name):
    SHOTS.mkdir(parents=True, exist_ok=True)
    path = SHOTS / f'{name}.png'
    page.screenshot(path=str(path))
    print(f'SCREENSHOT={path}', flush=True)
    return str(path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video', required=True)
    ap.add_argument('--caption', required=True)
    ap.add_argument('--tag', default='clip')
    a = ap.parse_args()
    video = pathlib.Path(a.video)
    if not video.exists():
        print(f'ERR: missing {video}'); sys.exit(1)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=False, viewport={'width': 1280, 'height': 950},
            user_agent=('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'))
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto('https://www.tiktok.com/tiktokstudio/upload', timeout=90000, wait_until='domcontentloaded')

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

        fi.set_input_files(str(video), timeout=60000)
        print('FILE_SET', flush=True)

        cap = None
        end = time.time() + 90
        while time.time() < end:
            try:
                cap = page.locator('[contenteditable="true"]').first
                if cap.count() > 0:
                    break
            except Exception:
                pass
            time.sleep(3)
        if cap is None:
            print('NO_CAPTION_EDITOR'); shot(page, f'{a.tag}-no-editor.png'); sys.exit(3)
        cap.click(); cap.fill('')
        page.keyboard.type(a.caption, delay=15)
        print('CAPTION_SET', flush=True)
        time.sleep(2)

        page.keyboard.press('Escape')
        time.sleep(1)
        page.mouse.click(400, 300)
        time.sleep(1)
        print('POPUP_CLOSED', flush=True)

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

        for label in ('AI-generated', 'generat de AI', 'generată de AI'):
            try:
                t = page.get_by_text(label, exact=False).first
                if t.count() > 0:
                    t.click(timeout=4000, force=True)
                    print(f'AIGC_TOGGLED {label}', flush=True); break
            except Exception as e:
                print('aigc try', label, type(e).__name__, flush=True)

        shot(page, f'{a.tag}-settings.png')
        page.locator('button:has-text("Post")').last.click(timeout=8000)
        print('POST_CLICKED', flush=True)

        # handle the 'Continue to post?' dialog: click 'Post now' as soon as it appears
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
            # also detect success redirect
            if '/content' in page.url:
                break
            time.sleep(1)
        print('DIALOG_HANDLED clicked_now=', clicked_now, flush=True)

        # wait for the /content redirect
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