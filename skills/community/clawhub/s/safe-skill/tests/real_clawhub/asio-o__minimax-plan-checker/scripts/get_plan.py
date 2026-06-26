"""
MiniMax 套餐信息获取脚本
使用浏览器自动化获取套餐名称、额度、当前使用情况
"""

import asyncio
import re
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("请先安装 playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

MINIMAX_URL = "https://platform.minimaxi.com/user-center/payment/coding-plan"

async def get_plan_info():
    """获取 MiniMax 套餐信息"""
    
    print("正在启动浏览器...")
    print("-" * 60)
    
    async with async_playwright() as p:
        try:
            # 启动浏览器
            browser = await p.chromium.launch(headless=False, slow_mo=300)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()
            page.set_default_timeout(60000)
            
            print(f"正在打开 {MINIMAX_URL} ...")
            await page.goto(MINIMAX_URL, wait_until="domcontentloaded", timeout=60000)
            
            # 等待页面加载
            await asyncio.sleep(3)
            
            # 检查是否需要登录
            if "login" in page.url.lower():
                print("\n⚠️ 需要登录")
                print("请在浏览器中完成登录，然后按回车键继续...")
                input()
                await page.goto(MINIMAX_URL, wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(2)
            
            print("\n正在提取套餐信息...\n")
            
            # 提取页面文本
            text_content = await page.evaluate("""() => {
                return document.body.innerText;
            }""")
            
            # 使用 JavaScript 提取关键数据
            plan_info = await page.evaluate("""() => {
                const result = {};
                
                // 查找套餐名称
                const heading = document.querySelector('h1, h2');
                if (heading) {
                    result.plan_name = heading.innerText.trim();
                }
                
                // 查找额度信息
                const quotaElements = document.querySelectorAll('p, span, div');
                for (const el of quotaElements) {
                    const text = el.innerText;
                    if (text.includes('可用额度')) {
                        result.quota = text.trim();
                    }
                    if (text.includes('已使用')) {
                        result.used = text.trim();
                    }
                    if (text.includes('重置')) {
                        result.reset = text.trim();
                    }
                }
                
                // 查找 API Key
                const apiKeyEl = document.querySelector('[class*="key"], [class*="api"]');
                if (apiKeyEl) {
                    const text = apiKeyEl.innerText;
                    const match = text.match(/sk-cp-[a-zA-Z0-9]+/);
                    if (match) {
                        result.api_key = match[0];
                    }
                }
                
                // 查找进度条百分比
                const progressBar = document.querySelector('[role="progressbar"], progress');
                if (progressBar) {
                    const ariaValue = progressBar.getAttribute('aria-valuenow');
                    if (ariaValue) {
                        result.percent = ariaValue + '%';
                    }
                }
                
                return result;
            }""")
            
            # 使用正则表达式从文本中提取
            extracted = {}
            
            # 套餐名称
            name_match = re.search(r'([A-Za-z]+-[\u4e00-\u9fa5]+)', text_content)
            if name_match:
                extracted['plan_name'] = name_match.group(1)
            
            # 可用额度
            quota_match = re.search(r'可用额度[：:]\s*([^\n]+)', text_content)
            if quota_match:
                extracted['quota'] = quota_match.group(1).strip()
            
            # 已使用百分比
            used_match = re.search(r'(\d+)%\s*已使用', text_content)
            if used_match:
                extracted['used_percent'] = used_match.group(1) + '%'
            
            # 重置时间
            reset_match = re.search(r'(\d{2}:\d{2}.*重置)', text_content)
            if reset_match:
                extracted['reset_time'] = reset_match.group(1)
            
            # API Key
            key_match = re.search(r'(sk-cp-[a-zA-Z0-9]+)', text_content)
            if key_match:
                extracted['api_key'] = key_match.group(1)
            
            await browser.close()
            
            # 合并结果
            result = {**plan_info, **extracted}
            
            # 输出结果
            print("=" * 50)
            print("📊 MiniMax 套餐信息")
            print("=" * 50)
            
            if result.get('plan_name'):
                print(f"  套餐名称: {result['plan_name']}")
            if result.get('quota'):
                print(f"  可用额度: {result['quota']}")
            if result.get('used_percent'):
                print(f"  当前使用: {result['used_percent']}")
            elif result.get('percent'):
                print(f"  当前使用: {result['percent']} 已使用")
            if result.get('reset_time'):
                print(f"  重置时间: {result['reset_time']}")
            if result.get('api_key'):
                print(f"  API Key: {result['api_key']}...")
            
            print("=" * 50)
            
            return result
            
        except Exception as e:
            print(f"发生错误: {e}")
            import traceback
            traceback.print_exc()
            return {}

if __name__ == "__main__":
    print("=" * 60)
    print("  MiniMax 套餐信息查询工具")
    print("=" * 60)
    asyncio.run(get_plan_info())
