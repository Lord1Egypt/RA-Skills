#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截图封面图
"""
# 此脚本使用 Playwright 将 HTML 截图为 PNG
# 需要安装: pip install playwright && playwright install chromium

async def screenshot_cover(html_path, output_path, width=900, height=383):
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': width, 'height': height})
        await page.goto(f'file://{html_path}')
        await page.screenshot(path=output_path, full_page=False)
        await browser.close()
    
    print(f"✅ 截图已生成: {output_path}")

if __name__ == "__main__":
    print("截图脚本已加载")
    print("使用方法: await screenshot_cover(html_path, output_path)")
