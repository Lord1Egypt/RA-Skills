"""
批量渲染8张小红书图文模板
"""
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from playwright.async_api import async_playwright

TEMPLATE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(TEMPLATE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CDP_URL = "http://127.0.0.1:18800"

SLIDES = [
    ("ref_封面.html",   "01_封面.png",        "封面"),
    ("ref_p2.html",     "02_妈妈必买清单.png",  "妈妈必买清单"),
    ("ref_p3.html",     "03_妈妈不买清单.png",  "妈妈不买清单"),
    ("ref_p4.html",     "04_宝宝必买清单一.png","宝宝必买清单（一）"),
    ("ref_p5.html",     "05_宝宝必买清单二.png","宝宝必买清单（二）"),
    ("ref_p6.html",     "06_宝宝不买清单一.png","宝宝不买清单（一）"),
    ("ref_p7.html",     "07_宝宝不买清单二.png","宝宝不买清单（二）"),
    ("ref_p8.html",     "08_结尾页.png",       "结尾页"),
]

async def render_slide(browser, src_file, out_file, label):
    page = await browser.new_page()
    src_path = os.path.join(TEMPLATE_DIR, src_file)
    out_path = os.path.join(OUTPUT_DIR, out_file)
    url = "file:///" + src_path.replace(chr(92), "/")
    await page.goto(url, timeout=15000)
    await page.wait_for_timeout(1500)
    await page.screenshot(path=out_path, type="png", full_page=False)
    size = os.path.getsize(out_path)
    print(f"  [{label}] {out_file} ({size//1024}KB)")
    await page.close()

async def main():
    print(f"Connecting to CDP at {CDP_URL}...")
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        print(f"Rendering {len(SLIDES)} slides...\n")
        for src, out, label in SLIDES:
            await render_slide(browser, src, out, label)
        await browser.close()
    print("\nAll done!")

if __name__ == "__main__":
    asyncio.run(main())
