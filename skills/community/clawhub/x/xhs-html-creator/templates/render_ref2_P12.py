import asyncio, os, playwright.async_api as pw
CDP = 'http://127.0.0.1:18800'
TEMPLATES = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\templates'
OUTPUT = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\outputs'

async def render(name):
    async with pw.async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        ctx = await browser.new_context(viewport={'width': 1080, 'height': 1350})
        page = await ctx.new_page()
        with open(os.path.join(TEMPLATES, f'{name}.html'), 'r', encoding='utf-8') as f:
            html = f.read()
        await page.set_content(html, timeout=15000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(OUTPUT, f'{name}.png'), type='png')
        await ctx.close()
        await browser.close()
        print(f'{name} OK')

async def main():
    await render('ref2_P1')
    await render('ref2_P2')

asyncio.run(main())
