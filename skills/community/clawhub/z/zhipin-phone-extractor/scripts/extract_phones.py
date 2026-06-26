#!/usr/bin/env python3
"""
BOSS直聘手机号提取器
从 zhipin.com 的聊天消息中自动提取手机号
"""

import argparse
import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

try:
    from playwright.async_api import async_playwright, Browser, Page
except ImportError:
    print("❌ 请先安装 Playwright: pip install playwright && playwright install chromium")
    exit(1)


class ZhipinPhoneExtractor:
    """BOSS直聘手机号提取器"""

    def __init__(self, output_file: str = None, headless: bool = False, limit: int = None):
        self.output_file = output_file or str(Path.home() / "Desktop" / "猎聘手机号记录.txt")
        self.headless = headless
        self.limit = limit
        self.phones: List[Tuple[str, str, str]] = []  # (姓名, 手机号, 公司)

    async def extract(self):
        """主提取流程"""
        print("🚀 启动 BOSS直聘手机号提取器...")

        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = await context.new_page()

            try:
                # 1. 访问 BOSS直聘
                print("📱 正在访问 zhipin.com...")
                await page.goto("https://www.zhipin.com", wait_until="networkidle")

                # 2. 检查登录状态
                if await self._check_login_required(page):
                    print("⚠️  需要登录！请在打开的浏览器中手动登录...")
                    await self._wait_for_login(page)

                # 3. 导航到消息页面
                print("💬 正在打开消息页面...")
                await page.click('a[href*="/web/geek/chat"]', timeout=10000)
                await page.wait_for_load_state("networkidle")

                # 4. 提取手机号
                print("🔍 正在提取手机号...")
                await self._extract_phones_from_messages(page)

                # 5. 保存结果
                self._save_results()

            except Exception as e:
                print(f"❌ 提取失败: {e}")
                raise
            finally:
                await browser.close()

    async def _check_login_required(self, page: Page) -> bool:
        """检查是否需要登录"""
        try:
            login_btn = await page.query_selector('a[href*="login"]')
            return login_btn is not None
        except:
            return True

    async def _wait_for_login(self, page: Page):
        """等待用户手动登录"""
        print("⏳ 等待登录完成（最长等待 2 分钟）...")
        try:
            await page.wait_for_selector('.nav-figure', timeout=120000)
            print("✅ 登录成功！")
        except:
            raise TimeoutError("登录超时，请重试")

    async def _extract_phones_from_messages(self, page: Page):
        """从消息列表中提取手机号"""
        # 获取所有消息项
        message_items = await page.query_selector_all('.chat-list-item')
        if not message_items:
            print("⚠️  未找到消息，请检查页面结构")
            return

        limit_count = 0
        phone_pattern = re.compile(r'1[3-9]\d{9}')

        for item in message_items:
            if self.limit and limit_count >= self.limit:
                break

            try:
                # 点击消息项
                await item.click()
                await page.wait_for_timeout(500)  # 等待消息加载

                # 提取发送者姓名
                name_elem = await item.query_selector('.name-text')
                name = await name_elem.inner_text() if name_elem else "未知"

                # 提取公司名称（如果有）
                company_elem = await item.query_selector('.company-text')
                company = await company_elem.inner_text() if company_elem else ""

                # 提取消息内容
                messages = await page.query_selector_all('.message-text')
                for msg_elem in messages:
                    msg_text = await msg_elem.inner_text()

                    # 查找手机号
                    phones = phone_pattern.findall(msg_text)
                    for phone in phones:
                        self.phones.append((name.strip(), phone, company.strip()))

                limit_count += 1

            except Exception as e:
                print(f"⚠️  处理消息失败: {e}")
                continue

    def _save_results(self):
        """保存提取结果"""
        if not self.phones:
            print("📭 未提取到任何手机号")
            return

        # 去重
        unique_phones = list(set(self.phones))
        unique_phones.sort(key=lambda x: x[1])  # 按手机号排序

        # 确保输出目录存在
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件（追加模式）
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(f"\n=== {timestamp} ===\n")
            for name, phone, company in unique_phones:
                f.write(f"{name} - {phone} - {company}\n")

        # 打印报告
        print("\n" + "=" * 50)
        print("📊 提取报告")
        print("=" * 50)
        print(f"✅ 提取手机号: {len(unique_phones)} 个")
        print(f"📁 保存位置: {output_path}")
        print("\n提取结果:")
        for i, (name, phone, company) in enumerate(unique_phones, 1):
            print(f"{i}. {name} - {phone} - {company}")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="BOSS直聘手机号提取器")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--headless", action="store_true", help="无头模式（不显示浏览器）")
    parser.add_argument("--limit", "-l", type=int, help="限制提取的消息数量")

    args = parser.parse_args()

    extractor = ZhipinPhoneExtractor(
        output_file=args.output,
        headless=args.headless,
        limit=args.limit
    )

    asyncio.run(extractor.extract())


if __name__ == "__main__":
    main()
