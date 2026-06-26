#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理剩余发票 - 浏览器自动化
"""

import os
import sys
import io
import re
import time
from datetime import datetime, date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EMAIL = "181957682@qq.com"
PASSWORD = "dcdrfqjmoczrbhdj"
IMAP_SERVER = "imap.qq.com"
BASE_DIR = r"Z:\OpenClaw\InvoiceOC"

# 自动找到最新的 v1 文件夹（主下载目录）
def get_main_output_dir():
    """获取主输出目录（v1 文件夹）"""
    if os.path.exists(BASE_DIR):
        for d in sorted(os.listdir(BASE_DIR), reverse=True):
            if '_v1' in d:
                return os.path.join(BASE_DIR, d)
    # 默认回退
    return os.path.join(BASE_DIR, "260102-260309_v1")

OUTPUT_DIR = get_main_output_dir()
ATTACHMENTS_DIR = os.path.join(OUTPUT_DIR, "attachments")

def process_remaining():
    print("="*60)
    print("🌐 处理剩余发票（浏览器自动化）")
    print("="*60)
    
    try:
        from playwright.sync_api import sync_playwright
        from imap_tools import MailBox, A
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("💡 请安装: pip install playwright imap-tools")
        return
    
    # 连接邮箱
    print("\n🔌 连接邮箱...")
    try:
        mailbox = MailBox(IMAP_SERVER)
        mailbox.login(EMAIL, PASSWORD)
        print("✅ 登录成功")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return
    
    # 搜索日期范围
    date_from = date(2026, 1, 2)
    date_to = date(2026, 3, 9)
    
    print(f"🔍 搜索 {date_from} ~ {date_to} 的邮件...")
    criteria = A(date_gte=date_from)
    all_msgs = list(mailbox.fetch(criteria, reverse=True, limit=500))
    
    # 筛选需要浏览器处理的发票
    browser_emails = []
    for msg in all_msgs:
        if not msg.subject:
            continue
        
        msg_date = msg.date.date() if isinstance(msg.date, datetime) else msg.date
        if not (date_from <= msg_date <= date_to):
            continue
        
        text = (msg.text or '') + (msg.html or '')
        
        # 和运国际
        if '和运' in msg.subject:
            for url in re.findall(r'https://dppt\.shanghai\.chinatax\.gov\.cn:\d+/v/2_[A-Za-z0-9_]+', text):
                browser_emails.append({
                    'type': '和运国际',
                    'subject': msg.subject,
                    'date': msg_date,
                    'url': url
                })
        # 诺诺发票
        elif '寿司郎' in msg.subject or '诺诺' in text:
            for url in re.findall(r'https://nnfp\.jss\.com\.cn/[A-Za-z0-9_-]+', text):
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
    
    print(f"✅ 找到 {len(browser_emails)} 封需要浏览器处理的发票\n")
    
    # 启动浏览器
    print("🚀 启动浏览器...")
    downloaded = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # 显示浏览器窗口
            context = browser.new_context(accept_downloads=True)
            
            for idx, email in enumerate(browser_emails, 1):
                print(f"\n[{idx}/{len(browser_emails)}] {email['type']}")
                print(f"   主题: {email['subject'][:50]}...")
                
                try:
                    page = context.new_page()
                    page.goto(email['url'], wait_until='networkidle', timeout=60000)
                    time.sleep(3)
                    
                    # 智能按钮检测
                    selectors = [
                        'button:has-text("PDF下载")',
                        'button:has-text("下载")',
                        'a:has-text("PDF")',
                        'a:has-text("下载")',
                    ]
                    
                    found = False
                    for selector in selectors:
                        try:
                            btn = page.locator(selector)
                            if btn.count() > 0:
                                print(f"   找到下载按钮，正在下载...")
                                
                                with page.expect_download(timeout=60000) as download_info:
                                    btn.first.click()
                                    time.sleep(5)
                                
                                download = download_info.value
                                date_str = email['date'].strftime('%Y%m%d')
                                prefix = 'heyun' if email['type'] == '和运国际' else 'nuonuo'
                                filename = f"{prefix}_{date_str}_{int(time.time())}.pdf"
                                save_path = os.path.join(ATTACHMENTS_DIR, filename)
                                
                                download.save_as(save_path)
                                
                                print(f"   ✅ 下载成功: {filename}")
                                downloaded.append(filename)
                                found = True
                                break
                        except Exception as e:
                            continue
                    
                    if not found:
                        print(f"   ❌ 未找到下载按钮")
                    
                    page.close()
                    
                except Exception as e:
                    print(f"   ❌ 失败: {str(e)[:50]}")
                    try:
                        page.close()
                    except:
                        pass
                
                time.sleep(2)
            
            browser.close()
    except Exception as e:
        print(f"⚠️ 浏览器出错: {e}")
    
    mailbox.logout()
    
    # 输出结果
    print("\n" + "="*60)
    print(f"📊 浏览器下载完成: {len(downloaded)}/{len(browser_emails)}")
    print("="*60)
    
    for d in downloaded:
        print(f"   ✅ {d}")

if __name__ == "__main__":
    process_remaining()
