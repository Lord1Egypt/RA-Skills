"""浏览器会话启动（系统 Chrome/Edge + Playwright persistent context）。"""

from __future__ import annotations

import logging
import os
from typing import Any, Optional, Tuple

from util.constants import DEFAULT_START_URL

logger = logging.getLogger(__name__)

DEFAULT_PAGE_TIMEOUT_MS = 15_000
GOTO_TIMEOUT_MS = 60_000

STEALTH_INIT_SCRIPT = """
(() => {
  try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); } catch (e) {}
})();
"""


def get_start_url() -> str:
    return (os.getenv("TARGET_START_URL") or DEFAULT_START_URL).strip() or DEFAULT_START_URL


def _headless_from_env() -> bool:
    v = (os.getenv("OPENCLAW_BROWSER_HEADLESS") or "0").strip().lower()
    return v in ("1", "true", "yes", "on")


def _find_chrome_executable() -> str | None:
    try:
        from jiangchang_skill_core.runtime_env import find_chrome_executable

        chrome = find_chrome_executable()
        if chrome and os.path.isfile(chrome):
            return chrome
    except ImportError:
        pass

    candidates = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


async def start_browser_session(
    profile_dir: str,
    *,
    headless: Optional[bool] = None,
) -> Tuple[Any, Any, Any]:
    """
    启动持久化 Chrome profile，new_page + goto 入口页，返回 (playwright, context, page)。

    真实 skill 需要安装 playwright 与 jiangchang_skill_core。
    """
    from playwright.async_api import async_playwright

    hl = headless if headless is not None else _headless_from_env()
    start_url = get_start_url()
    chrome = _find_chrome_executable()
    if not chrome:
        raise RuntimeError(
            "ERROR:MISSING_BROWSER 未检测到 Chrome 或 Edge 浏览器，请先安装系统浏览器后重试。"
        )

    launch_args = ["--start-maximized", "--disable-blink-features=AutomationControlled"]
    logger.info(
        "browser_launch chrome=%s profile_dir=%s start_url=%s args=%s headless=%s",
        chrome,
        profile_dir,
        start_url,
        launch_args,
        hl,
    )
    print(f"[浏览器] 系统 Chrome: {chrome}")
    print(f"[浏览器] profile_dir: [{profile_dir}]")
    print(f"[浏览器] startup_url={start_url}")
    print(f"[浏览器] args={launch_args}")

    pw = await async_playwright().start()
    context = None
    try:
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=hl,
            executable_path=chrome,
            locale="zh-CN",
            no_viewport=True,
            args=launch_args,
            ignore_default_args=["--enable-automation"],
        )
        await context.add_init_script(STEALTH_INIT_SCRIPT)

        page = await context.new_page()
        page.set_default_timeout(DEFAULT_PAGE_TIMEOUT_MS)

        try:
            await page.goto(start_url, wait_until="domcontentloaded", timeout=GOTO_TIMEOUT_MS)
        except Exception as exc:
            raise RuntimeError(
                f"浏览器已启动，但未能打开目标首页 {start_url}。"
                "请检查网络、Chrome profile、代理或页面访问状态。"
                f"（{exc}）"
            ) from exc

        return pw, context, page
    except Exception:
        if context is not None:
            try:
                await context.close()
            except Exception:
                pass
        await pw.stop()
        raise


async def close_browser_context(pw, context) -> None:
    try:
        if context is not None:
            await context.close()
    except Exception:
        pass
    try:
        if pw is not None:
            await pw.stop()
    except Exception:
        pass
