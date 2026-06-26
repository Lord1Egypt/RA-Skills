#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器处理工具 - 单独运行，处理待下载发票
用法: python browser_tool.py <日期范围目录>
示例: python browser_tool.py 260106-260308_v6
"""

import os
import sys
import re
import io
import time
from datetime import datetime, date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EMAIL = "181957682@qq.com"
PASSWORD = "dcdrfqjmoczrbhdj"
IMAP_SERVER = "imap.qq.com"
BASE_DIR = r"Z:\OpenClaw\InvoiceOC"

def process_browser_only(date_range_dir):
    """仅处理浏览器下载"""
    output_dir = os.path.join(BASE_DIR, date_range_dir)
    attachments_dir = os.path.join(output_dir, "attachments")
    
    if not os.path.exists(output_dir):
        print(f"❌ 目录不存在: {output_dir}")
        return
    
    print("="*70)
    print("🌐 浏览器处理工具")
    print("="*70)
    print(f"📁 目标目录: {output_dir}\n")
    
    try:
        from playwright.sync_api import sync_playwright
        from imap_tools import MailBox, A
        from datetime import datetime as dt
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return
    
    # 解析日期范围
    try:
        date_part = date_range_dir.split('_v')[0]
        start_str, end_str = date_part.split('-')
        date_from = date(2000 + int(start_str[:2]), int(start_str[2:4]), int(start_str[4:6]))
        date_to = date(2000 + int(end_str[:2]), int(end_str[2:4]), int(end_str[4:6]))
    except:
        print("❌ 无法解析日期范围")
        return
    
    # 连接邮箱
    print("🔌 连接邮箱...")
    try:
        mailbox = MailBox(IMAP_SERVER)
        mailbox.login(EMAIL, PASSWORD)
        print("✅ 登录成功\n")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return
    
    # 搜索目标邮件
    criteria = A(date_gte=date_from)
    all_msgs = list(mailbox.fetch(criteria, reverse=True, limit=500))
    
    browser_emails = []
    
    for msg in all_msgs:
        if not msg.subject or not msg.date:
            continue
        
        msg_date = msg.date.date() if isinstance(msg.date, dt) else msg.date
        if msg_date < date_from or msg_date > date_to:
            continue
        
        text = (msg.text or '') + (msg.html or '')
        
        # 和运国际
        if '和运' in msg.subject:
            matches = re.findall(r'https://dppt\.shanghai\.chinatax\.gov\.cn:\d+/v/2_[A-Za-z0-9_]+', text)
            for url in matches:
                browser_emails.append({
                    'type': '和运国际',
                    'subject': msg.subject,
                    'date': msg_date,
                    'url': url
                })
        
        # 诺诺发票
        elif '寿司郎' in msg.subject or 'nuonuo' in text.lower():
            matches = re.findall(r'https://nnfp\.jss\.com\.cn/[A-Za-z0-9_-]+', text)
            for url in matches:
                if url not in [e['url'] for e in browser_emails]:
                    browser_emails.append({
                        'type': '诺诺发票',
                        'subject': msg.subject,
                        'date': msg_date,
                        'url': url
                    })
    
    if not browser_emails:
        print("⚠️ 未找到需要浏览器处理的发票")
        mailbox.logout()
        return
    
    print(f"✅ 找到 {len(browser_emails)} 个需要浏览器处理的发票\n")
    
    # 启动浏览器
    print("🚀 启动浏览器（请稍候，会弹出浏览器窗口）...")
    downloaded = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        
        for i, item in enumerate(browser_emails):
            print(f"\n[{i+1}/{len(browser_emails)}] {item['type']}")
            print(f"   {item['subject'][:50]}...")
            
            try:
                page = context.new_page()
                page.goto(item['url'], wait_until='networkidle', timeout=60000)
                time.sleep(3)
                
                # 尝试下载按钮
                selectors = [
                    'button:has-text("PDF下载")',
                    'button:has-text("下载")',
                    'a:has-text("PDF")',
                    'a:has-text("下载")'
                ]
                
                found = False
                for selector in selectors:
                    try:
                        btn = page.locator(selector)
                        if btn.count() > 0:
                            print(f"   点击下载按钮...")
                            
                            with page.expect_download(timeout=60000) as download_info:
                                btn.first.click()
                                time.sleep(5)
                            
                            download = download_info.value
                            
                            # 生成文件名
                            date_str = item['date'].strftime('%Y%m%d')
                            if item['type'] == '和运国际':
                                match = re.search(r'cs=2_(\d+)', item['url'])
                                inv_num = match.group(1) if match else str(int(time.time()))
                                filename = f"heyun_{date_str}_{inv_num}.pdf"
                            else:
                                filename = f"nuonuo_{date_str}_{int(time.time())}.pdf"
                            
                            save_path = os.path.join(attachments_dir, filename)
                            download.save_as(save_path)
                            
                            print(f"   ✅ 成功: {filename}")
                            downloaded.append(filename)
                            found = True
                            break
                    except Exception as e:
                        continue
                
                if not found:
                    print(f"   ⚠️ 未找到下载按钮")
                
                page.close()
                
            except Exception as e:
                print(f"   ❌ 失败: {str(e)[:50]}")
                try:
                    page.close()
                except:
                    pass
            
            time.sleep(2)
        
        browser.close()
    
    mailbox.logout()
    
    print("\n" + "="*70)
    print(f"📊 完成: {len(downloaded)}/{len(browser_emails)}")
    print("="*70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python browser_tool.py <日期范围目录>")
        print("示例: python browser_tool.py 260106-260308_v6")
        sys.exit(1)
    
    process_browser_only(sys.argv[1])
