#!/usr/bin/env python3
"""
NetRoadShow 自动化捕获脚本 — Playwright 版

已验证可靠的完整工作流（2026-05-12，KODIT Audio Roadshow Plus，32 slides）：

  1. Playwright 直接导航到 show URL（不要用 Camofox browser_navigate）
  2. Angular 路由正常解析，显示邮箱输入框
  3. 填邮箱 → 用 expect_popup() 阻塞等待弹窗（不用 page.on('popup')）
  4. 弹窗进入 disclaimer 页 → Agree 按钮是 <div> 不是 <button>
     → 必须用 page.evaluate('document.querySelector(".btn-agree").click()')
  5. Agree 后出现 Resume/Start from beginning 选项 → 选 Start
  6. 进入 /MediaSlides → ArrowRight 逐页翻 → 截图 → Pillow 合成 PDF

依赖：
  pip install playwright pillow
  playwright install chromium

用法：
  python netroadshow-capture.py --url "https://www.netroadshow.com/nrs/home/#!/?show=SHOW_ID"
  python netroadshow-capture.py --url "..." --email "other@email.com" --output /path/to/out
"""

import argparse
import os
import re
import time
from pathlib import Path
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(description="NetRoadShow page capture (Playwright)")
    parser.add_argument("--url", required=True, help="路演 URL（含 ?show=SHOW_ID）")
    parser.add_argument("--email", default=None, help="查看人邮箱（默认取 NRS_EMAIL 环境变量）")
    parser.add_argument("--output", "-o", default="/tmp/roadshow_output", help="输出目录")
    parser.add_argument("--wait", type=float, default=1.5, help="翻页后等待秒数")
    parser.add_argument("--pdf-only", action="store_true", help="仅合成 PDF，跳过截屏")
    return parser.parse_args()


def extract_total_slides(pp):
    """从页面文本中提取幻灯片总数"""
    text = pp.inner_text("body")
    m = re.search(r'(\d+)\s*Slide', text, re.I)
    return int(m.group(1)) if m else None


def capture_pages(args):
    from playwright.sync_api import sync_playwright

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, user_agent=UA)
        page = ctx.new_page()

        # ---- Step 1: Navigate to show URL (Playwright handles Angular hash routing correctly) ----
        print(f"1. Navigating to show URL...")
        page.goto(args.url, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # ---- Step 2: Fill email ----
        print(f"2. Filling email: {args.email}")
        email_input = page.locator("#homeEmailInput").first
        email_input.fill(args.email)
        time.sleep(0.3)

        # ---- Step 3: Launch Show + expect_popup ----
        # MUST use expect_popup(), NOT page.on("popup") — the event fires too late
        print(f"3. Launching show...")
        with page.expect_popup() as popup_info:
            page.get_by_text("Launch Show").click()

        pp = popup_info.value
        pp.wait_for_load_state("networkidle")
        time.sleep(3)
        print(f"   Popup: {pp.url}")

        # ---- Step 4: Accept disclaimer (div buttons, NOT <button>) ----
        print(f"4. Accepting disclaimer...")
        pp.evaluate('document.querySelector(".btn-agree").click()')
        time.sleep(2)
        pp.wait_for_load_state("networkidle")
        print(f"   URL after agree: {pp.url}")

        # ---- Step 5: Start from beginning ----
        print(f"5. Starting from beginning...")
        try:
            pp.get_by_text("Start from beginning").first.click(timeout=5000)
        except Exception:
            # Fallback: evaluate to find and click
            pp.evaluate(
                '''[...document.querySelectorAll("*")].find(el =>
                    el.textContent.trim() === "Start from beginning")?.click()'''
            )

        time.sleep(3)
        pp.wait_for_load_state("networkidle")
        print(f"   URL: {pp.url}")
        pp.screenshot(path=str(output_dir / "slide_area.png"))

        # ---- Step 6: Detect total slides ----
        total = extract_total_slides(pp)
        if total is None:
            # Fallback: parse from HTML
            html = pp.content()
            m = re.search(r'(\d+)\s*Slide', html, re.I)
            total = int(m.group(1)) if m else 32
        print(f"6. Total slides: {total}")

        # ---- Step 7: Capture all slides via ArrowRight ----
        print(f"7. Capturing {total} slides...")
        for i in range(total):
            time.sleep(args.wait)
            path = str(output_dir / f"slide_{i+1:03d}.png")
            pp.screenshot(path=path, full_page=False)
            print(f"   Slide {i+1}/{total}")

            if i < total - 1:
                pp.keyboard.press("ArrowRight")
                time.sleep(0.5)
                pp.wait_for_load_state("networkidle")

        browser.close()
        return sorted(output_dir.glob("slide_*.png"))


def images_to_pdf(image_paths, output_path, resolution=150):
    imgs = [Image.open(f).convert("RGB") for f in image_paths]
    if not imgs:
        print("❌ No images to convert")
        return False
    imgs[0].save(
        output_path,
        save_all=True,
        append_images=imgs[1:],
        format="PDF",
        resolution=resolution,
    )
    print(f"✅ PDF: {output_path} ({len(imgs)} pages, {Path(output_path).stat().st_size / 1024 / 1024:.1f} MB)")
    return True


def main():
    args = parse_args()

    # Resolve email: CLI arg → env var → prompt via agent instructions
    email = args.email or os.environ.get("NRS_EMAIL")
    assert email, "NRS_EMAIL 未设置。请通过 --email 参数或 export NRS_EMAIL=your-email@company.com 设置邮箱。"
    args.email = email

    if args.pdf_only:
        images = sorted(Path(args.output).glob("slide_*.png"))
        if images:
            images_to_pdf(images, str(Path(args.output) / "roadshow.pdf"))
        return

    screenshots = capture_pages(args)
    if screenshots:
        pdf_path = Path(args.output) / "roadshow.pdf"
        images_to_pdf(screenshots, str(pdf_path))


if __name__ == "__main__":
    main()
