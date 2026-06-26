import asyncio
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

SESSION_FILE = Path(__file__).resolve().parents[1] / "data" / "tiktok_session.json"


async def main():
    print("Opening TikTok login page...", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )
        page = await context.new_page()

        await page.goto("https://www.tiktok.com/login", timeout=60000, wait_until="networkidle")
        print("=" * 60, flush=True)
        print("请在弹出的浏览器窗口中登录 TikTok。", flush=True)
        print("登录成功后，脚本会自动检测并保存 session。", flush=True)
        print("如不想继续，关闭浏览器窗口即可退出。", flush=True)
        print("=" * 60, flush=True)

        # Wait for navigation away from /login page (indicates login success)
        logged_in = False
        for _ in range(300):  # 5 minutes max
            current = page.url
            if "/login" not in current and "tiktok.com" in current:
                logged_in = True
                break
            await asyncio.sleep(1)
        else:
            print("登录超时。如果已登录，按 Ctrl+C 手动保存。", flush=True)

        if not logged_in:
            await browser.close()
            print("未检测到登录，退出。", flush=True)
            return

        await asyncio.sleep(3)  # Let cookies/state settle

        # Save storage state
        state = await context.storage_state()
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        SESSION_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 登录态已保存到: {SESSION_FILE}", flush=True)
        print(f"Cookies: {len(state.get('cookies', []))} 个", flush=True)

        # Quick verification
        await page.goto("https://www.tiktok.com/search/video?q=test", timeout=30000, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        title = await page.title()
        print(f"搜索页标题: {title}", flush=True)
        if "Log in" not in title:
            print("✅ 登录状态有效！可关闭浏览器窗口。", flush=True)
        else:
            print("⚠️ 登录可能未成功，请重试", flush=True)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
