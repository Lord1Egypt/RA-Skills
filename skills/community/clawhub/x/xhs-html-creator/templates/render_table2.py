import asyncio, os, playwright.async_api as pw

CDP = 'http://127.0.0.1:18800'
TEMPLATES = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\templates'
OUTPUT = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\outputs'

pages = [
    ('table2_封面.html', '表格2_01_封面.png'),
    ('table2_宝宝产房篇.html', '表格2_02_宝宝产房篇.png'),
    ('table2_妈妈产房篇.html', '表格2_03_妈妈产房篇.png'),
    ('table2_宝宝住院篇.html', '表格2_04_宝宝住院篇.png'),
    ('table2_妈妈住院篇.html', '表格2_05_妈妈住院篇.png'),
    ('table2_结尾.html', '表格2_06_结尾.png'),
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
