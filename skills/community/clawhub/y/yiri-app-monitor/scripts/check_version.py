#!/usr/bin/env python3
"""查询一日记账 App 版本 - 使用 Playwright"""
import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright

APP_ID = "com.ericple.onebill"
APP_NAME = "一日记账"
URL = f"https://appgallery.huawei.com/app/detail?id={APP_ID}"
SELECTOR = "span.content-value"

async def check_version():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(URL, wait_until="networkidle", timeout=30000)
            await page.wait_for_selector(SELECTOR, timeout=20000)
            version_elem = await page.query_selector(SELECTOR)
            version = await version_elem.text_content()
            await browser.close()

            return {
                "app_name": APP_NAME,
                "app_id": APP_ID,
                "version": version.strip() if version else "未找到",
                "url": URL,
                "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        return {
            "app_name": APP_NAME,
            "app_id": APP_ID,
            "version": "获取失败",
            "error": str(e),
            "url": URL,
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    result = asyncio.run(check_version())
    print(json.dumps(result, ensure_ascii=False, indent=2))
