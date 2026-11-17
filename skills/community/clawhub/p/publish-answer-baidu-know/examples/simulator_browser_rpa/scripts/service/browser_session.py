"""浏览器会话启动（系统 Chrome/Edge + async Playwright persistent context）。"""

from __future__ import annotations

import logging
import os
from typing import Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

DEFAULT_PAGE_TIMEOUT_MS = 15_000

CHROME_LAUNCH_ARGS: List[str] = [
    "--start-maximized",
    "--disable-blink-features=AutomationControlled",
]

STEALTH_INIT_SCRIPT = """
(() => {
  try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); } catch (e) {}
})();
"""


def chrome_launch_args() -> List[str]:
    return list(CHROME_LAUNCH_ARGS)


def _headless_from_env() -> bool:
    v = (os.getenv("OPENCLAW_BROWSER_HEADLESS") or "0").strip().lower()
    return v in ("1", "true", "yes", "on")


def find_chrome_executable() -> str | None:
    try:
        from jiangchang_skill_core.runtime_env import find_chrome_executable as _find

        chrome = _find()
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


def _clear_node_options() -> None:
    os.environ.pop("NODE_OPTIONS", None)


async def start_browser_session(
    profile_dir: str,
    *,
    headless: Optional[bool] = None,
) -> Tuple[Any, Any, Any]:
    """
    启动持久化 Chrome profile，返回 (playwright, context, page)。

    URL 不在此文件打开；由 simulator_playwright.py 负责 page.goto。
    """
    from playwright.async_api import async_playwright

    _clear_node_options()
    hl = headless if headless is not None else _headless_from_env()
    chrome = find_chrome_executable()
    if not chrome:
        raise RuntimeError(
            "ERROR:MISSING_BROWSER 未检测到 Chrome 或 Edge 浏览器，请先安装系统浏览器后重试。"
        )

    args = chrome_launch_args()
    logger.info(
        "browser_launch chrome=%s profile_dir=%s args=%s headless=%s",
        chrome,
        profile_dir,
        args,
        hl,
    )

    pw = await async_playwright().start()
    context = None
    try:
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=hl,
            executable_path=chrome,
            locale="zh-CN",
            no_viewport=True,
            args=args,
            ignore_default_args=["--enable-automation"],
        )
        await context.add_init_script(STEALTH_INIT_SCRIPT)

        page = context.pages[0] if context.pages else await context.new_page()
        page.set_default_timeout(DEFAULT_PAGE_TIMEOUT_MS)
        return pw, context, page
    except Exception:
        if context is not None:
            try:
                await context.close()
            except Exception:
                pass
        await pw.stop()
        raise


async def close_browser_session(playwright: Any, context: Any) -> None:
    try:
        if context is not None:
            await context.close()
    except Exception:
        pass
    try:
        if playwright is not None:
            await playwright.stop()
    except Exception:
        pass
