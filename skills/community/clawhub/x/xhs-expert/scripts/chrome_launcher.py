"""
XHS Expert - Chrome启动器
支持多Profile隔离、CDP连接、Stealth注入
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_PROFILE = "default"
CHROME_DATA_DIR = Path.home() / ".config" / "xiaohongshu" / "profiles"


class ChromeLauncher:
    """
    Chrome启动器核心类

    功能：
    - Chrome Profile隔离（多账号支持）
    - CDP连接建立
    - Stealth注入（绕过自动化检测）
    """

    def __init__(
        self,
        profile: str = DEFAULT_PROFILE,
        headless: bool = False,
        port: int = 9222,
        stealth: bool = True
    ):
        self.profile = profile
        self.headless = headless
        self.port = port
        self.stealth = stealth
        self.browser = None
        self.context = None
        self.profile_dir = CHROME_DATA_DIR / profile

    async def launch(self) -> Dict[str, Any]:
        """
        启动Chrome浏览器

        返回: {"success": bool, "browser": Browser, "context": BrowserContext, ...}
        """
        from playwright.async_api import async_playwright

        self.profile_dir.mkdir(parents=True, exist_ok=True)

        playwright_instance = await async_playwright().start()

        chrome_args = [
            f"--remote-debugging-port={self.port}",
            f"--user-data-dir={self.profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
        ]

        if self.headless:
            chrome_args.append("--headless=new")

        browser = await playwright_instance.chromium.launch(
            args=chrome_args,
            headless=self.headless
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )

        if self.stealth:
            await self._inject_stealth(context)

        self.browser = browser
        self.context = context

        return {
            "success": True,
            "browser": browser,
            "context": context,
            "cdp_url": f"http://localhost:{self.port}",
            "profile": self.profile
        }

    async def _inject_stealth(self, context):
        """注入stealth脚本，绕过自动化检测"""
        # 方法1: 通过CDP注入JavaScript
        page = await context.new_page()
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en']
            });
            window.chrome = { runtime: {} };
        """)
        await page.close()

        # 方法2: 移除自动化特征属性
        await context.add_init_script("""
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """)

    async def connect_remote(self, ws_endpoint: str) -> Dict[str, Any]:
        """连接已存在的Chrome实例（通过WebSocket）"""
        from playwright.async_api import async_playwright

        playwright_instance = await async_playwright().start()
        browser = await playwright_instance.chromium.connect_over_cdp(ws_endpoint)
        contexts = browser.contexts

        context = contexts[0] if contexts else await browser.new_context()

        return {
            "success": True,
            "browser": browser,
            "context": context,
            "ws_endpoint": ws_endpoint
        }

    async def get_cdp_info(self) -> Optional[Dict[str, Any]]:
        """获取CDP连接信息"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://localhost:{self.port}/json/version"
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception:
            return None

    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.context:
            await self.context.close()
