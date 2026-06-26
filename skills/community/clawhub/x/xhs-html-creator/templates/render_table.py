import asyncio, os, playwright.async_api as pw

CDP = 'http://127.0.0.1:18800'
TEMPLATES = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\templates'
OUTPUT = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\outputs'

pages = [
    ('table_封面.html', '表格风_01_封面.png'),
    ('table_宝宝住院篇.html', '表格风_02_宝宝住院篇.png'),
    ('table_妈妈住院篇.html', '表格风_03_妈妈住院篇.png'),
    ('table_结尾.html', '表格风_04_结尾.png'),
]

async def main():
    async with pw.async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        for fname, oname in pages:
            fpath = os.path.join(TEMPLATES, fname)
            opath = os.path.join(OUTPUT, oname)
            with open(fpath, 'r', encoding='utf-8') as f:
                html = f.read()
            ctx = await browser.new_context(viewport={'width': 1080, 'height': 1350})
            page = await ctx.new_page()
            await page.set_content(html, timeout=15000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=opath, type='png')
            await ctx.close()
            print(f'OK: {oname}')
        await browser.close()

asyncio.run(main())
