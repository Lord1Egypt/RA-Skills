#!/usr/bin/env python3
"""
小红书自动登录（二维码版）
- 检测到 Cookie 过期时自动触发
- 截图登录二维码发送到飞书
- 用户手机扫码后自动保存 Cookie
- 无需在电脑旁操作
"""

import asyncio
import time
import logging
from pathlib import Path
from typing import Optional

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from config import (
    XHS_USER_DATA_DIR,
    BROWSER_VIEWPORT_WIDTH,
    BROWSER_VIEWPORT_HEIGHT,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
)
from feishu_app_bot import FeishuAppBot

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


class AutoLoginWithQRCode:
    """二维码自动登录器"""

    def __init__(self, chat_id: str):
        """
        初始化
        
        Args:
            chat_id: 飞书群聊 ID，用于发送二维码
        """
        self.chat_id = chat_id
        self.bot = FeishuAppBot()
        self.qr_code_path = Path(__file__).parent / "qrcode.png"

    async def capture_qr_code(self) -> Optional[Path]:
        """
        打开小红书登录页并截取二维码
        
        Returns:
            Path: 二维码图片路径，失败返回 None
        """
        if not PLAYWRIGHT_AVAILABLE:
            log.error("Playwright 未安装")
            return None

        log.info("正在打开小红书登录页面...")

        async with async_playwright() as p:
            # 使用临时用户数据目录（避免影响已有登录状态）
            temp_user_dir = XHS_USER_DATA_DIR.parent / "xhs_temp_login"
            
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(temp_user_dir),
                headless=True,  # 无头模式，后台运行
                viewport={
                    "width": BROWSER_VIEWPORT_WIDTH,
                    "height": BROWSER_VIEWPORT_HEIGHT
                },
                args=[
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-blink-features=AutomationControlled",
                ],
            )

            page = await browser.new_page()

            try:
                # 访问小红书首页（会弹出登录窗口）
                log.info("正在打开小红书首页...")
                await page.goto(
                    "https://www.xiaohongshu.com/explore",
                    timeout=30000,
                    wait_until="networkidle"
                )
                
                # 等待页面加载
                await page.wait_for_timeout(3000)
                
                # 检查是否需要登录（查找登录按钮或弹窗）
                log.info("检查登录状态...")
                
                # 尝试点击登录按钮触发弹窗
                try:
                    # 查找登录按钮（多种可能的选择器）
                    login_selectors = [
                        'text=登录',
                        'text=登入',
                        '[class*="login"]',
                        'button:has-text("登录")',
                        '.login-btn'
                    ]
                    
                    for selector in login_selectors:
                        try:
                            if await page.locator(selector).count() > 0:
                                log.info(f"找到登录按钮: {selector}")
                                await page.click(selector)
                                await page.wait_for_timeout(2000)
                                break
                        except:
                            continue
                except Exception as e:
                    log.warning(f"点击登录按钮失败: {e}")
                
                # 等待二维码加载（登录弹窗出现）
                log.info("等待登录弹窗加载...")
                await page.wait_for_timeout(5000)
                
                # 检查是否有登录弹窗/二维码
                page_content = await page.content()
                if '二维码' in page_content or '扫码' in page_content or 'qrcode' in page_content.lower():
                    log.info("✅ 检测到登录弹窗")
                else:
                    log.warning("未检测到登录弹窗，将截取当前页面")

                # 截取整个页面（包含登录弹窗和二维码）
                log.info("正在截取登录页面...")
                await page.screenshot(
                    path=str(self.qr_code_path),
                    full_page=False  # 只截取视口区域
                )
                
                log.info(f"✅ 登录页面截图已保存: {self.qr_code_path}")
                
                await browser.close()
                return self.qr_code_path

            except Exception as e:
                log.error(f"打开登录页失败: {e}")
                await browser.close()
                return None

    def send_qr_code_to_feishu(self) -> bool:
        """
        发送二维码图片到飞书
        
        Returns:
            bool: 发送是否成功
        """
        if not self.qr_code_path.exists():
            log.error("二维码图片不存在")
            return False

        try:
            # 发送文字说明
            self.bot.send_text_to_chat(
                self.chat_id,
                "⚠️ 小红书 Cookie 已过期\n"
                "📱 请查看下方截图，使用微信或小红书 APP 扫码登录\n"
                "⏰ 二维码有效期 5 分钟，请尽快扫码\n"
                "✅ 登录成功后系统会自动检测并保存，无需操作电脑"
            )
            
            # 发送二维码图片
            success = self.bot.send_image_to_chat(self.chat_id, self.qr_code_path)
            
            if success:
                log.info("✅ 二维码图片已发送到飞书")
            else:
                # 图片发送失败，发送文字提示
                self.bot.send_text_to_chat(
                    self.chat_id,
                    "❌ 图片发送失败，请手动查看服务器上的二维码:\n"
                    f"{self.qr_code_path.absolute()}"
                )
            
            return True
            
        except Exception as e:
            log.error(f"发送二维码到飞书失败: {e}")
            return False

    async def wait_for_login(self, timeout: int = 300) -> bool:
        """
        等待用户扫码登录完成
        
        Args:
            timeout: 最长等待时间（秒），默认 5 分钟
            
        Returns:
            bool: 是否登录成功
        """
        log.info(f"等待用户扫码登录，最长等待 {timeout} 秒...")
        
        # 先等待10秒，让用户有时间扫码登录
        log.info("⏳ 等待10秒，让用户完成扫码登录...")
        await asyncio.sleep(10)
        log.info("🔍 开始检测登录状态...")
        
        start_time = time.time()
        check_interval = 5  # 每 5 秒检查一次
        
        while time.time() - start_time < timeout:
            # 检查是否已登录
            from cookie_manager import CookieManager
            
            manager = CookieManager()
            is_valid = await manager.check_cookie_valid()
            
            if is_valid:
                log.info("✅ 检测到登录成功！")
                
                # 提取并保存新的 Cookie
                cookie = await manager.extract_cookie_from_browser()
                if cookie:
                    self.bot.send_text_to_chat(
                        self.chat_id,
                        "✅ 小红书登录成功！Cookie 已自动保存，可以继续使用。"
                    )
                    return True
            
            await asyncio.sleep(check_interval)
        
        log.warning("⏰ 等待登录超时")
        self.bot.send_text_to_chat(
            self.chat_id,
            "⏰ 二维码已过期，请重新触发登录流程"
        )
        return False

    async def run(self) -> bool:
        """
        执行完整的自动登录流程
        
        Returns:
            bool: 登录是否成功
        """
        log.info("=" * 50)
        log.info("启动二维码自动登录流程")
        log.info("=" * 50)
        
        # 1. 截取二维码
        qr_path = await self.capture_qr_code()
        if not qr_path:
            self.bot.send_text_to_chat(
                self.chat_id,
                "❌ 获取登录二维码失败，请检查网络或手动登录"
            )
            return False
        
        # 2. 发送到飞书
        if not self.send_qr_code_to_feishu():
            return False
        
        # 3. 等待用户扫码
        return await self.wait_for_login()


async def auto_login_if_needed(chat_id: str) -> bool:
    """
    检查 Cookie 状态，如需登录则自动触发二维码流程
    
    Args:
        chat_id: 飞书群聊 ID
        
    Returns:
        bool: Cookie 是否有效（或登录成功）
    """
    from cookie_manager import CookieManager
    
    manager = CookieManager()
    
    # 检查当前 Cookie 是否有效
    is_valid = await manager.check_cookie_valid()
    
    if is_valid:
        log.info("Cookie 有效，无需登录")
        return True
    
    log.warning("Cookie 已过期，启动自动登录流程")
    
    # 启动二维码登录
    auto_login = AutoLoginWithQRCode(chat_id)
    return await auto_login.run()


if __name__ == "__main__":
    # 测试
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python auto_login_with_qrcode.py <chat_id>")
        print("示例: python auto_login_with_qrcode.py oc_xxxxxxxxxxxxxxxx")
        sys.exit(1)
    
    chat_id = sys.argv[1]
    
    print(f"🚀 测试自动登录，群ID: {chat_id}")
    result = asyncio.run(auto_login_if_needed(chat_id))
    
    if result:
        print("✅ Cookie 有效或登录成功")
    else:
        print("❌ 登录失败")
