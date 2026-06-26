#!/usr/bin/env python3
"""Cookie 自动刷新工具

当东方财富 Cookie 过期时，通过 Playwright 浏览器访问官网尝试续签。
如果服务器端 session 仍然有效，cookie 会被自动刷新。
如果完全失效，则需要用户手动从浏览器复制 Cookie。

用法:
    python scripts/refresh_cookie.py
"""

import logging
import os
import sys

import requests
import json

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("refresh_cookie")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COOKIE_PATH = os.path.join(SKILL_DIR, "cookie.txt")


def main():
    if not os.path.exists(COOKIE_PATH):
        logger.error("Cookie 文件不存在: %s", COOKIE_PATH)
        sys.exit(1)

    with open(COOKIE_PATH) as f:
        old_cookie = f.read().strip()
    logger.info("当前 Cookie: %d 字符", len(old_cookie))

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("需要安装 playwright: pip install playwright && playwright install chromium")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # 注入现有 Cookie
        for item in old_cookie.split(";"):
            item = item.strip()
            if "=" not in item:
                continue
            name, value = item.split("=", 1)
            try:
                context.add_cookies([{
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": ".eastmoney.com",
                    "path": "/",
                }])
            except (ValueError, TypeError):
                pass

        # 访问东方财富自选股页面
        page = context.new_page()
        logger.info("正在访问东方财富自选股页面...")
        try:
            page.goto(
                "https://quote.eastmoney.com/zixuan/lite.html",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            logger.info("页面加载完成")
        except (TimeoutError, OSError) as e:
            logger.warning("页面加载超时或失败: %s（继续执行）", e)

        # 获取刷新后的 Cookie
        all_cookies = context.cookies()
        em_cookies = [
            c for c in all_cookies
            if "eastmoney" in c.get("domain", "") or "dfcfw" in c.get("domain", "")
        ]
        browser.close()

    new_cookie = "; ".join(
        [f"{c['name']}={c['value']}" for c in em_cookies]
    )

    if not new_cookie:
        logger.error("未获取到任何 Cookie！")
        sys.exit(1)

    with open(COOKIE_PATH, "w") as f:
        f.write(new_cookie)
    logger.info("Cookie 已写入: %d 字符", len(new_cookie))

    if old_cookie != new_cookie:
        logger.info("Cookie 内容已更新！")
    else:
        logger.info("Cookie 内容未变化（可能 session 未续签）")

    # 验证 Cookie 有效性
    logger.info("正在验证 Cookie...")
    sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
    try:
        from eastmoney_api import get_stocks
        logging.getLogger("eastmoney_api").setLevel(logging.CRITICAL)

        stocks = get_stocks(COOKIE_PATH)
        if stocks:
            logger.info("✅ Cookie 有效！自选股共 %d 只", len(stocks))
            logger.info("   前 5 只: %s",
                        ", ".join([f"{s['name']}({s['code']})" for s in stocks[:5]]))
        else:
            logger.warning("❌ Cookie 无效，需要手动从浏览器复制新 Cookie")
            logger.warning("   步骤: 打开 https://quote.eastmoney.com/zixuan/lite.html")
            logger.warning("         → F12 → Console → copy(document.cookie)")
            logger.warning("         → 粘贴覆盖 cookie.txt")
            sys.exit(1)
    except (requests.RequestException, json.JSONDecodeError, OSError) as e:
        logger.warning("验证失败: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
