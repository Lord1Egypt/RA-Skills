#!/usr/bin/env python3
"""
环境初始化脚本。
- 复用或新建 AgentBay session
- 检测小红书登录状态
- 已登录：更新 config.json 的 session_id，status.md 写入 running
- 未登录：status.md 写入 login_required + resource_url，程序退出（退出码 1）
  调用方看到 login_required 后，通知用户通过 resource_url 远程登录
"""

import sys
import asyncio
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (
    load_config, save_config, write_status, setup_env, validate_agentbay_env, setup_logging,
    create_or_reuse_session, get_cdp_url, check_login_status, cleanup,
)
from playwright.async_api import async_playwright

# 模块级 logger，setup_logging() 调用后自动生效
log = logging.getLogger("xhs")


async def main():
    setup_logging("env_setup")

    cfg = load_config()
    setup_env(cfg)

    ok, err = validate_agentbay_env(cfg)
    if not ok:
        log.error(f"❌ 环境检查失败: {err}")
        write_status("error", {"说明": err})
        sys.exit(1)

    agent_bay, session, is_reused = await create_or_reuse_session(cfg)
    cdp_url = await get_cdp_url(session, is_reused, cfg)

    cfg["session_id"] = session.session_id
    save_config(cfg)

    resource_url = ""
    try:
        info = await session.info()
        if info.success and info.data:
            resource_url = info.data.resource_url or ""
    except Exception:
        pass

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)
        default_context = browser.contexts[0]
        pages = default_context.pages
        if pages:
            for p_extra in pages[:-1]:
                await p_extra.close()
            page = pages[-1]
        else:
            page = await default_context.new_page()

        await page.goto("https://www.xiaohongshu.com/")
        await page.wait_for_timeout(3000)

        agent = session.browser.operator
        is_logged_in = await check_login_status(agent, page)

        if not is_logged_in:
            write_status(
                "login_required",
                {
                    "说明": "请通过 resource_url 远程连接到沙箱浏览器完成小红书登录，登录后重新运行 env_setup.py",
                    "session_id": session.session_id,
                    "resource_url": resource_url,
                },
            )
            await browser.close()
            log.error("❌ 未登录，请先登录。status.md 已记录登录信息。")
            sys.exit(1)

        write_status(
            "running",
            {
                "session_id": session.session_id,
                "说明": "环境就绪，可运行 search_notes.py 开始采集",
            },
        )
        await browser.close()
        log.info("✅ 环境初始化完成，已登录，session_id 已写入 config.json")


if __name__ == "__main__":
    asyncio.run(main())
