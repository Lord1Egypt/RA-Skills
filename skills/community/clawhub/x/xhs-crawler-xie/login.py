#!/usr/bin/env python3
"""
小红书首次登录脚本
运行后会弹出 Chrome 窗口，手动登录小红书，登录完成后按 Enter 保存 Cookie。
之后爬虫会自动复用此 Cookie，无需每次登录。
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ 请先安装 Playwright:")
    print("   pip install playwright")
    print("   playwright install chromium")
    sys.exit(1)

from config import XHS_USER_DATA_DIR, BROWSER_VIEWPORT_WIDTH, BROWSER_VIEWPORT_HEIGHT


async def login():
    """首次登录并保存 Cookie"""
    print("=" * 60)
    print("小红书登录工具")
    print("=" * 60)
    print()
    print("🚀 正在启动浏览器...")
    print(f"📁 用户数据将保存到: {XHS_USER_DATA_DIR}")
    print()

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(XHS_USER_DATA_DIR),
            headless=False,  # 必须可见，方便用户操作
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

        # 添加重试机制
        max_retries = 3
        for i in range(max_retries):
            try:
                print(f"🌐 正在访问小红书... (尝试 {i+1}/{max_retries})")
                await page.goto("https://www.xiaohongshu.com", timeout=30000)
                break
            except Exception as e:
                print(f"⚠️ 第 {i+1} 次尝试失败: {e}")
                if i < max_retries - 1:
                    print("🔄 3秒后重试...")
                    await asyncio.sleep(3)
                else:
                    print("❌ 无法访问小红书，请检查网络连接")
                    await browser.close()
                    return

        print()
        print("✅ 浏览器已打开")
        print()
        print("📱 请在弹出的 Chrome 窗口中手动登录小红书")
        print("   支持以下登录方式:")
        print("   • 扫码登录（推荐）")
        print("   • 手机号登录")
        print("   • 账号密码登录")
        print()
        print("⚠️ 注意:")
        print("   1. 请确保登录成功后再继续")
        print("   2. 如果遇到验证码，请手动完成")
        print("   3. 登录成功后，回到此窗口继续")
        print()

        input("✅ 登录完成后，按 Enter 键保存 Cookie...")

        await browser.close()

        print()
        print("=" * 60)
        print("✅ Cookie 已保存！")
        print("=" * 60)
        print()
        print(f"📁 数据保存位置: {XHS_USER_DATA_DIR}")
        print()
        print("🎉 登录完成！")
        print()
        print("现在可以运行爬虫程序了:")
        print("   python xhs_crawler.py")
        print()
        print("Cookie 有效期:")
        print("   • 通常可以持续数天到数周")
        print("   • 如果提示 Cookie 失效，请重新运行此脚本")
        print()


def main():
    """主函数"""
    try:
        asyncio.run(login())
    except KeyboardInterrupt:
        print()
        print("\n⚠️ 用户取消操作")
    except Exception as e:
        print()
        print(f"❌ 发生错误: {e}")
        print()
        print("常见问题:")
        print("1. 如果提示 Chrome 未找到，请确保已安装 Chrome 浏览器")
        print("2. 如果提示 Playwright 错误，请运行: playwright install chromium")


if __name__ == "__main__":
    main()
