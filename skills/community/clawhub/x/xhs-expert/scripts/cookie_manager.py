"""
XHS Expert - Cookie管理器
登录态持久化、多账号切换、状态检测
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

DEFAULT_PROFILE = "default"
COOKIES_DIR = Path.home() / ".config" / "xiaohongshu" / "profiles"


class CookieManager:
    """
    Cookie管理器

    功能：
    - Cookie持久化存储
    - 多账号切换
    - 登录状态检测
    - 从浏览器同步Cookie
    """

    def __init__(self, profile: str = DEFAULT_PROFILE):
        self.profile = profile
        self.profile_dir = COOKIES_DIR / profile
        self.cookies_file = self.profile_dir / "cookies.json"
        self.profile_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """从文件加载Cookie数据"""
        if not self.cookies_file.exists():
            return {}

        try:
            with open(self.cookies_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self, data: Dict[str, Any]):
        """保存Cookie数据到文件"""
        data["updated_at"] = time.time()
        with open(self.cookies_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_cookies(self) -> Dict[str, str]:
        """获取Cookie字典"""
        data = self.load()
        return data.get("cookies", {})

    def set_cookies(self, cookies: Dict[str, str], extra: Optional[Dict] = None):
        """保存Cookie字典"""
        data = self.load()
        data["cookies"] = cookies
        if extra:
            data.update(extra)
        self.save(data)

    def is_valid(self) -> bool:
        """检查Cookie是否有效"""
        data = self.load()
        cookies = data.get("cookies", {})

        required = ["web_session", "a1", "webId"]
        return all(k in cookies for k in required)

    async def sync_from_browser(self, context) -> bool:
        """
        从Playwright BrowserContext同步Cookie

        参数：
            context: playwright BrowserContext 对象
        """
        try:
            cookies = await context.cookies()
            cookie_dict = {c["name"]: c["value"] for c in cookies}

            extra = {
                "synced_at": time.time(),
                "profile": self.profile
            }

            self.set_cookies(cookie_dict, extra)
            return True
        except Exception as e:
            print(f"Cookie同步失败: {e}")
            return False

    def get_extra(self, key: str) -> Any:
        """获取额外字段"""
        data = self.load()
        return data.get(key)


def check_login_status(cookies_path: Optional[Path] = None) -> Dict[str, Any]:
    """检查登录状态（同步版本）"""
    if cookies_path:
        cookies_file = cookies_path
    else:
        cookies_file = COOKIES_DIR / DEFAULT_PROFILE / "cookies.json"

    if not cookies_file.exists():
        return {
            "logged_in": False,
            "reason": "未找到Cookie文件"
        }

    try:
        with open(cookies_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        cookies = data.get("cookies", {})

        required = ["web_session", "a1"]
        missing = [k for k in required if k not in cookies]

        if missing:
            return {
                "logged_in": False,
                "reason": f"缺少Cookie字段: {missing}"
            }

        updated_at = data.get("updated_at", 0)
        age_days = (time.time() - updated_at) / 86400 if updated_at else 999

        return {
            "logged_in": True,
            "age_days": round(age_days, 1),
            "has_web_session": "web_session" in cookies,
            "profile": data.get("profile", DEFAULT_PROFILE)
        }

    except Exception as e:
        return {
            "logged_in": False,
            "reason": str(e)
        }


async def login_with_browser(
    profile: str = DEFAULT_PROFILE,
    headless: bool = False
) -> Dict[str, Any]:
    """
    通过浏览器扫码登录

    打开小红书登录页面，用户扫码后自动保存Cookie
    """
    from chrome_launcher import ChromeLauncher
    from playwright.async_api import TimeoutError as PlaywrightTimeout

    launcher = ChromeLauncher(profile=profile, headless=headless, stealth=True)
    result = await launcher.launch()

    if not result["success"]:
        return {"success": False, "error": "浏览器启动失败"}

    context = result["context"]
    page = await context.new_page()

    try:
        # 打开小红书登录页
        await page.goto(
            "https://www.xiaohongshu.com",
            wait_until="networkidle",
            timeout=30000
        )

        # 等待用户登录（检测登录按钮消失）
        print("请在浏览器中扫码登录...")
        print("登录成功后请在控制台按回车继续...")

        # 等待用户手动确认（通过输入）
        # 这里可以改进为自动检测登录状态
        input("登录完成后按回车继续...")

        # 同步Cookie
        manager = CookieManager(profile=profile)
        await manager.sync_from_browser(context)

        # 验证
        if manager.is_valid():
            await launcher.close()
            return {"success": True, "profile": profile}

        return {"success": False, "error": "Cookie保存失败"}

    except PlaywrightTimeout:
        return {"success": False, "error": "页面加载超时"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        await launcher.close()
