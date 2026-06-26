import asyncio, os, playwright.async_api as pw

CDP = 'http://127.0.0.1:18800'
TEMPLATES = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\templates'
OUTPUT = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\outputs'

async def main():
    async with pw.async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        fpath = os.path.join(TEMPLATES, 'memoV2_封面.html')
        opath = os.path.join(OUTPUT, 'memoV2_封面.png')
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        ctx = await browser.new_context(viewport={'width': 1080, 'height': 1350})
        page = await ctx.new_page()
        await page.set_content(html, timeout=15000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path=opath, type='png')
        await ctx.close()
        print(f'OK: memoV2_封面.png')
        await browser.close()

asyncio.run(main())
