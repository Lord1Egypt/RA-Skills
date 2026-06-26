#!/usr/bin/env python3
"""
Browser session manager for automated login persistence.
Uses Playwright to maintain login sessions across runs.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Optional, Dict
from playwright.async_api import async_playwright, Browser, BrowserContext


class BrowserSessionManager:
    """Manage browser sessions with persistent login state."""

    def __init__(self, base_dir: str = None):
        """Initialize session manager.

        Args:
            base_dir: Base directory for session storage
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent / "sessions"
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.dianping_session_dir = self.base_dir / "dianping"
        self.xhs_session_dir = self.base_dir / "xiaohongshu"

        self.dianping_session_dir.mkdir(exist_ok=True)
        self.xhs_session_dir.mkdir(exist_ok=True)

        self.state_file = self.base_dir / "session_state.json"

    def load_session_state(self) -> Dict:
        """Load session state from disk."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"dianping": {"logged_in": False}, "xiaohongshu": {"logged_in": False}}

    def save_session_state(self, state: Dict):
        """Save session state to disk."""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    async def setup_dianping_session(self, headless: bool = False) -> BrowserContext:
        """Setup or load Dianping session.

        Args:
            headless: Run in headless mode

        Returns:
            BrowserContext with persistent session
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.dianping_session_dir),
                headless=headless,
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            state = self.load_session_state()

            if not state.get("dianping", {}).get("logged_in", False):
                print("\n" + "="*60)
                print("🔐 首次设置：请在浏览器中登录大众点评")
                print("="*60)
                print("1. 浏览器将自动打开大众点评网站")
                print("2. 请使用手机号或微信扫码登录")
                print("3. 登录成功后，关闭浏览器窗口")
                print("4. 脚本将自动保存登录状态")
                print("="*60 + "\n")

                page = browser.new_page()
                await page.goto('https://www.dianping.com')

                # Wait for user to login (wait until browser closes)
                print("⏳ 等待登录...")
                print("💡 登录完成后，请按 Ctrl+C 继续\n")

                try:
                    # Keep browser open until user closes it
                    await browser.wait_for_event('close', timeout=0)
                except KeyboardInterrupt:
                    print("\n✅ 检测到登录完成")

                # Mark as logged in
                state["dianping"]["logged_in"] = True
                state["dianping"]["last_login"] = str(asyncio.get_event_loop().time())
                self.save_session_state(state)

                print("✅ 大众点评登录状态已保存\n")

            await browser.close()

        # Return new context with saved session
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.dianping_session_dir),
                headless=True,
                viewport={'width': 1280, 'height': 720}
            )
            return browser

    async def setup_xiaohongshu_session(self, headless: bool = False) -> BrowserContext:
        """Setup or load Xiaohongshu session.

        Args:
            headless: Run in headless mode

        Returns:
            BrowserContext with persistent session
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.xhs_session_dir),
                headless=headless,
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
            )

            state = self.load_session_state()

            if not state.get("xiaohongshu", {}).get("logged_in", False):
                print("\n" + "="*60)
                print("🔐 首次设置：请在浏览器中登录小红书")
                print("="*60)
                print("1. 浏览器将自动打开小红书网站")
                print("2. 请使用手机号或微信扫码登录")
                print("3. 登录成功后，关闭浏览器窗口")
                print("4. 脚本将自动保存登录状态")
                print("="*60 + "\n")

                page = browser.new_page()
                await page.goto('https://www.xiaohongshu.com')

                # Wait for user to login
                print("⏳ 等待登录...")
                print("💡 登录完成后，请按 Ctrl+C 继续\n")

                try:
                    await browser.wait_for_event('close', timeout=0)
                except KeyboardInterrupt:
                    print("\n✅ 检测到登录完成")

                # Mark as logged in
                state["xiaohongshu"]["logged_in"] = True
                state["xiaohongshu"]["last_login"] = str(asyncio.get_event_loop().time())
                self.save_session_state(state)

                print("✅ 小红书登录状态已保存\n")

            await browser.close()

        # Return new context with saved session
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.xhs_session_dir),
                headless=True,
                viewport={'width': 1280, 'height': 720}
            )
            return browser

    async def check_session_valid(self, platform: str) -> bool:
        """Check if session is still valid.

        Args:
            platform: 'dianping' or 'xiaohongshu'

        Returns:
            True if session is valid
        """
        state = self.load_session_state()
        return state.get(platform, {}).get("logged_in", False)

    async def refresh_session_if_needed(self, platform: str):
        """Refresh session if expired.

        Args:
            platform: 'dianping' or 'xiaohongshu'
        """
        if not await self.check_session_valid(platform):
            print(f"\n⚠️ {platform} 会话已过期，需要重新登录")
            if platform == "dianping":
                await self.setup_dianping_session(headless=False)
            else:
                await self.setup_xiaohongshu_session(headless=False)


def main():
    """Setup browser sessions interactively."""
    import sys

    print("="*60)
    print("🚀 浏览器会话管理器")
    print("="*60)
    print()

    manager = BrowserSessionManager()

    # Check what needs to be setup
    state = manager.load_session_state()

    needs_setup = []
    if not state.get("dianping", {}).get("logged_in", False):
        needs_setup.append("大众点评")
    if not state.get("xiaohongshu", {}).get("logged_in", False):
        needs_setup.append("小红书")

    if not needs_setup:
        print("✅ 所有平台已配置完成！")
        print()
        print("📊 当前状态：")
        print(f"  大众点评: ✅ 已登录")
        print(f"  小红书: ✅ 已登录")
        print()
        print("💡 如果遇到登录问题，运行：")
        print("   python3 scripts/session_manager.py --reset")
        return

    print("需要配置的平台：")
    for platform in needs_setup:
        print(f"  - {platform}")
    print()

    choice = input("是否现在配置？(y/n): ").strip().lower()
    if choice == 'y':
        if "--dianping" in sys.argv or "大众点评" in needs_setup:
            asyncio.run(manager.setup_dianping_session(headless=False))

        if "--xiaohongshu" in sys.argv or "小红书" in needs_setup:
            asyncio.run(manager.setup_xiaohongshu_session(headless=False))

        print("\n✅ 配置完成！现在可以使用自动抓取功能了。")
    else:
        print("稍后可以运行此脚本进行配置：")
        print("  python3 scripts/session_manager.py")


if __name__ == "__main__":
    import sys

    if "--reset" in sys.argv:
        import shutil
        manager = BrowserSessionManager()
        print("🔄 重置所有会话...")
        if manager.dianping_session_dir.exists():
            shutil.rmtree(manager.dianping_session_dir)
            manager.dianping_session_dir.mkdir()
        if manager.xhs_session_dir.exists():
            shutil.rmtree(manager.xhs_session_dir)
            manager.xhs_session_dir.mkdir()
        if manager.state_file.exists():
            manager.state_file.unlink()
        print("✅ 会话已重置，请重新登录")
    else:
        main()
