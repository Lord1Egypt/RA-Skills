#!/usr/bin/env python3
"""
小红书评论回复 - 修复版
"""

import json
import os
from time import sleep
from playwright.sync_api import sync_playwright

def main():
    print("🦀 开始加载cookie...")
    cookie_path = os.path.expanduser("~/.openclaw/secrets/xiaohongshu.json")
    
    with open(cookie_path, 'r') as f:
        cookie_dict = json.load(f)
    
    cookies = []
    for name, value in cookie_dict.items():
        cookies.append({
            'name': name,
            'value': value,
            'domain': '.xiaohongshu.com',
            'path': '/'
        })
    print(f"✅ 加载了 {len(cookies)} 个cookie")
    
    # 定义回复内容（需要根据实际评论情况修改）
    replies = [
        "[回复内容1 - 请根据实际评论内容修改]",
        "[回复内容2 - 请根据实际评论内容修改]", 
        "[回复内容3 - 请根据实际评论内容修改]",
    ]
    
    print("🦀 启动浏览器...")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        page.set_default_timeout(20000)
        
        print("🦀 访问通知页面...")
        page.goto('https://www.xiaohongshu.com/notification')
        sleep(4)
        print("✅ 页面加载完成")
        
        # 点击"评论和@"标签
        print("🖱️ 点击'评论和@'标签...")
        try:
            # 尝试多种方式点击
            page.locator('text=评论和@').first.click()
            sleep(3)
            print("✅ 已切换到评论标签")
        except Exception as e:
            print(f"点击标签失败: {e}")
            page.screenshot(path='./debug_error.png')
            browser.close()
            return False
        
        # 截图看看
        page.screenshot(path='./debug_comments.png')
        print("📸 已截图保存到 debug_comments.png")
        
        # 找回复按钮
        reply_buttons = page.get_by_text('回复', exact=True).all()
        print(f"🔍 找到 {len(reply_buttons)} 个回复按钮")
        
        if len(reply_buttons) == 0:
            print("❌ 没有找到回复按钮")
            browser.close()
            return False
        
        # 回复所有
        success_count = 0
        for i in range(min(len(reply_buttons), len(replies))):
            try:
                print(f"📝 回复第 {i+1} 条: {replies[i][:20]}...")
                
                # 重新获取按钮（避免stale element）
                reply_buttons = page.get_by_text('回复', exact=True).all()
                if i >= len(reply_buttons):
                    print("按钮数量变化，跳过")
                    continue
                    
                reply_buttons[i].scroll_into_view_if_needed()
                sleep(1)
                reply_buttons[i].click()
                sleep(2)
                
                # 输入回复
                textarea = page.locator('textarea').first
                textarea.fill(replies[i])
                sleep(1)
                
                # 点击发送
                send_btn = page.get_by_text('发送', exact=True).first
                send_btn.click()
                sleep(3)
                
                print(f"✅ 第 {i+1} 条回复成功")
                success_count += 1
                
            except Exception as e:
                print(f"❌ 第 {i+1} 条失败: {e}")
                continue
        
        browser.close()
        print(f"🎉 完成！成功回复 {success_count} 条")
        return True

if __name__ == "__main__":
    main()
