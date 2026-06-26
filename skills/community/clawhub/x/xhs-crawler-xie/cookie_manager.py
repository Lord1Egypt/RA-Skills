#!/usr/bin/env python3
"""
小红书 Cookie 管理模块
- 检测 Cookie 有效性
- 从 Chrome Profile 提取 Cookie
- 保存和读取 Cookie
"""

import asyncio
import logging
import json
from pathlib import Path
from typing import Optional

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from config import (
    XHS_USER_DATA_DIR,
    COOKIE_FILE,
    BROWSER_VIEWPORT_WIDTH,
    BROWSER_VIEWPORT_HEIGHT,
    CHECK_TIMEOUT,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
)

# 初始化日志
LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


class CookieManager:
    """小红书 Cookie 管理器"""

    def __init__(self):
        self.user_data_dir = XHS_USER_DATA_DIR
        self.cookie_file = COOKIE_FILE

    async def check_cookie_valid(self) -> bool:
        """
        检查 Cookie 是否有效
        
        Returns:
            bool: True=有效，False=失效
        """
        if not PLAYWRIGHT_AVAILABLE:
            log.error("Playwright 未安装，无法检测 Cookie 状态")
            log.error("请安装: pip install playwright")
            return False

        log.info("正在检查小红书 Cookie 有效性...")

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=True,
                    args=["--no-first-run", "--no-default-browser-check"],
                    viewport={
                        "width": BROWSER_VIEWPORT_WIDTH,
                        "height": BROWSER_VIEWPORT_HEIGHT
                    },
                )

                page = await browser.new_page()

                # 访问个人主页
                await page.goto(
                    "https://www.xiaohongshu.com/user/profile",
                    timeout=CHECK_TIMEOUT * 1000
                )
                await page.wait_for_timeout(3000)

                current_url = page.url
                log.info(f"当前 URL: {current_url}")

                # 检查是否被风控（461错误）
                if "461" in current_url or "error" in current_url.lower():
                    log.error("🚫 IP被风控（HTTP 461），请更换网络或等待解封")
                    log.error("建议: 切换到手机热点，或等待2-4小时后重试")
                    await browser.close()
                    return False
                
                # 如果 URL 包含 login，说明未登录
                is_valid = "login" not in current_url.lower()

                await browser.close()

                if is_valid:
                    log.info("✅ Cookie 有效")
                else:
                    log.warning("⚠️ Cookie 已失效")

                return is_valid

        except Exception as e:
            log.error(f"检查 Cookie 时出错: {e}")
            return False

    async def extract_cookie_from_browser(self) -> Optional[str]:
        """
        从 Chrome Profile 中提取 Cookie 字符串
        
        Returns:
            str: Cookie 字符串，提取失败返回 None
        """
        if not PLAYWRIGHT_AVAILABLE:
            log.error("Playwright 未安装")
            return None

        log.info("正在从浏览器提取 Cookie...")

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=True,
                    args=["--no-first-run", "--no-default-browser-check"],
                )

                page = await browser.new_page()
                await page.goto("https://www.xiaohongshu.com", timeout=30000)
                await page.wait_for_timeout(2000)

                # 获取所有 Cookie
                cookies = await browser.cookies()
                await browser.close()

                # 转换为字符串格式
                cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

                # 保存到文件
                self.save_cookie(cookie_str)

                log.info("✅ Cookie 提取成功")
                return cookie_str

        except Exception as e:
            log.error(f"提取 Cookie 失败: {e}")
            return None

    def save_cookie(self, cookie_str: str):
        """
        保存 Cookie 到文件
        
        Args:
            cookie_str: Cookie 字符串
        """
        try:
            self.cookie_file.write_text(cookie_str, encoding="utf-8")
            log.info(f"Cookie 已保存到: {self.cookie_file}")
        except Exception as e:
            log.error(f"保存 Cookie 失败: {e}")

    def load_cookie(self) -> Optional[str]:
        """
        从文件加载 Cookie
        
        Returns:
            str: Cookie 字符串，文件不存在返回 None
        """
        if not self.cookie_file.exists():
            log.warning(f"Cookie 文件不存在: {self.cookie_file}")
            return None

        try:
            cookie_str = self.cookie_file.read_text(encoding="utf-8").strip()
            if cookie_str:
                log.info("✅ Cookie 加载成功")
                return cookie_str
            else:
                log.warning("Cookie 文件为空")
                return None
        except Exception as e:
            log.error(f"加载 Cookie 失败: {e}")
            return None

    def get_cookie_dict(self, cookie_str: Optional[str] = None) -> dict:
        """
        将 Cookie 字符串转换为字典
        
        Args:
            cookie_str: Cookie 字符串，为 None 则从文件加载
            
        Returns:
            dict: Cookie 字典
        """
        if cookie_str is None:
            cookie_str = self.load_cookie()

        if not cookie_str:
            return {}

        cookie_dict = {}
        for item in cookie_str.split(";"):
            item = item.strip()
            if "=" in item:
                key, value = item.split("=", 1)
                cookie_dict[key] = value

        return cookie_dict

    def get_a1_value(self, cookie_str: Optional[str] = None) -> Optional[str]:
        """
        从 Cookie 中提取 a1 值（小红书签名需要）
        
        Args:
            cookie_str: Cookie 字符串
            
        Returns:
            str: a1 值
        """
        cookie_dict = self.get_cookie_dict(cookie_str)
        return cookie_dict.get("a1")

    async def ensure_valid_cookie(self, chat_id: str = None) -> Optional[str]:
        """
        确保有有效的 Cookie，如果没有则自动触发二维码登录
        
        Args:
            chat_id: 飞书群聊 ID，用于发送二维码，为 None 则只提示手动登录
            
        Returns:
            str: 有效的 Cookie 字符串，失败返回 None
        """
        # 先检查现有 Cookie 是否有效
        is_valid = await self.check_cookie_valid()

        if is_valid:
            # 有效则重新提取最新的 Cookie
            cookie = await self.extract_cookie_from_browser()
            return cookie
        else:
            log.warning("Cookie 已失效")
            
            # 如果提供了 chat_id，尝试自动二维码登录
            if chat_id:
                log.info("尝试自动二维码登录...")
                try:
                    from auto_login_with_qrcode import auto_login_if_needed
                    login_success = await auto_login_if_needed(chat_id)
                    if login_success:
                        # 重新提取 Cookie
                        cookie = await self.extract_cookie_from_browser()
                        return cookie
                except Exception as e:
                    log.error(f"自动登录失败: {e}")
            
            # 自动登录失败或未提供 chat_id，提示手动登录
            log.error("=" * 50)
            log.error("Cookie 已失效，请重新登录")
            log.error("=" * 50)
            log.error("方式1 - 自动登录（需要配置飞书）:")
            log.error("  系统会自动发送二维码到飞书群")
            log.error("")
            log.error("方式2 - 手动登录:")
            log.error("  python login.py")
            log.error("")
            log.error("登录完成后，再次运行本程序")
            return None


# 同步包装函数
def check_cookie_valid_sync() -> bool:
    """同步版本：检查 Cookie 有效性"""
    manager = CookieManager()
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(manager.check_cookie_valid())


def get_cookie_sync() -> Optional[str]:
    """同步版本：获取有效 Cookie"""
    manager = CookieManager()
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(manager.ensure_valid_cookie())


def load_cookie_sync() -> Optional[str]:
    """同步版本：从文件加载 Cookie"""
    manager = CookieManager()
    return manager.load_cookie()


if __name__ == "__main__":
    # 测试
    async def test():
        manager = CookieManager()

        # 检查 Cookie 有效性
        is_valid = await manager.check_cookie_valid()
        print(f"Cookie 有效: {is_valid}")

        if is_valid:
            # 提取并保存 Cookie
            cookie = await manager.extract_cookie_from_browser()
            print(f"提取的 Cookie: {cookie[:100]}..." if cookie else "提取失败")

            # 加载 Cookie
            loaded = manager.load_cookie()
            print(f"加载的 Cookie: {loaded[:100]}..." if loaded else "加载失败")

            # 获取 a1
            a1 = manager.get_a1_value()
            print(f"a1 值: {a1}")

    asyncio.run(test())
