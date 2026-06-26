#!/usr/bin/env python3
"""
DealRoadShow 自动化捕获脚本 — Playwright 版
"""

import argparse, os, re, time
from pathlib import Path
from PIL import Image


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--email", default=None)
    p.add_argument("--output", "-o", default="/tmp/dealroadshow_output")
    p.add_argument("--wait", type=float, default=1.5)
    p.add_argument("--max-pages", type=int, default=50)
    p.add_argument("--pdf-only", action="store_true")
    return p.parse_args()


def get_slide_input(page):
    """Return (current_page, total_pages) from DOM"""
    info = page.evaluate('''() => {
        const input = document.querySelector('[data-test="currentSlideInput"]');
        const cur = input ? parseInt(input.value) : null;
        // Find total from "of N" text
        const body = document.body.innerText;
        const m = body.match(/\\bof\\s*(\\d{1,4})\\b/);
        const total = m ? parseInt(m[1]) : null;
        return {cur, total};
    }''')
    return info.get("cur"), info.get("total")


def capture_pages(args):
    from playwright.sync_api import sync_playwright

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    email = args.email or os.environ.get("NRS_EMAIL")
    assert email, "NRS_EMAIL 未设置。"

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()

        print("1. Loading...")
        page.goto(args.url, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        try:
            cb = page.get_by_role("button", name="Ok").first
            if cb.is_visible(timeout=3000): cb.click(); time.sleep(1); print("   Cookies accepted")
        except: pass

        print("2. Email + Launch...")
        page.locator("input[type='email']").first.fill(email)
        time.sleep(0.5)
        page.get_by_text("Launch Deal Roadshow").click()

        for _ in range(15):
            time.sleep(1)
            try:
                if "/login/" not in page.url: break
            except: pass
        print(f"   URL: {page.url}")

        print("3. I Agree...")
        page.locator("button:has-text('I Agree')").first.click(timeout=10000)
        time.sleep(5)
        print(f"   URL: {page.url}")

        # Get counter
        cur, total = get_slide_input(page)
        cur = cur or 1
        total = total or args.max_pages
        print(f"4. Slides: {cur} of {total}")

        # Capture
        print("5. Capturing...")
        for i in range(cur, cur + total):
            time.sleep(args.wait)
            page.screenshot(path=str(out / f"slide_{i:03d}.png"), full_page=False)
            print(f"   Slide {i}/{cur + total - 1}")

            if i < cur + total - 1:
                page.keyboard.press("ArrowRight")
                time.sleep(1)
                # Wait for input value to advance
                for _ in range(10):
                    new_cur, _ = get_slide_input(page)
                    if new_cur and new_cur > i:
                        break
                    time.sleep(0.5)
                else:
                    print(f"   Last page (slide {i})")
                    break

        b.close()
        return sorted(out.glob("slide_*.png"))


def images_to_pdf(paths, output, res=150):
    imgs = [Image.open(f).convert("RGB") for f in paths]
    if not imgs: return False
    imgs[0].save(output, save_all=True, append_images=imgs[1:], format="PDF", resolution=res)
    sz = Path(output).stat().st_size / 1024 / 1024
    print(f"✅ PDF: {output} ({len(imgs)} pages, {sz:.1f} MB)")


def main():
    args = parse_args()
    email = args.email or os.environ.get("NRS_EMAIL")
    assert email, "NRS_EMAIL 未设置。"
    args.email = email
    if args.pdf_only:
        imgs = sorted(Path(args.output).glob("slide_*.png"))
        if imgs: images_to_pdf(imgs, str(Path(args.output) / "dealroadshow.pdf"))
        return
    ss = capture_pages(args)
    if ss: images_to_pdf(ss, str(Path(args.output) / "dealroadshow.pdf"))


if __name__ == "__main__":
    main()
