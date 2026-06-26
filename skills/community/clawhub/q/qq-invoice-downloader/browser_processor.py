#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器处理待下载发票
"""

import os
import re
import sys
import io
from datetime import datetime

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

def extract_tax_links(text):
    """提取税务平台链接"""
    # 和运国际
    heyun_pattern = r'https://dppt\.shanghai\.chinatax\.gov\.cn:\d+/v/2_[A-Za-z0-9_]+'
    links = re.findall(heyun_pattern, text)
    return links

def process_with_browser():
    """使用浏览器处理"""
    print("="*60)
    print("🌐 启动浏览器处理待下载发票")
    print("="*60)
    
    try:
        from playwright.sync_api import sync_playwright
        from imap_tools import MailBox, A
        from datetime import date
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("💡 请安装: pip install playwright imap-tools")
        print("   playwright install chromium")
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
    
    # 搜索日期范围内的邮件
    date_from = date(2026, 1, 6)
    date_to = date(2026, 3, 8)
    
    print(f"🔍 搜索 {date_from} ~ {date_to} 的邮件...")
    criteria = A(date_gte=date_from)
    all_msgs = list(mailbox.fetch(criteria, reverse=True, limit=500))
    
    # 筛选和运国际邮件
    tax_emails = []
    for msg in all_msgs:
        if not msg.subject:
            continue
        if '和运' in msg.subject or '和运国际' in (msg.text or '') + (msg.html or ''):
            msg_date = msg.date.date() if isinstance(msg.date, datetime) else msg.date
            if date_from <= msg_date <= date_to:
                text = (msg.text or '') + (msg.html or '')
                links = extract_tax_links(text)
                if links:
                    tax_emails.append({
                        'subject': msg.subject,
                        'date': msg_date,
                        'links': links
                    })
    
    if not tax_emails:
        print("⚠️ 未找到需要浏览器处理的和运国际发票")
        mailbox.logout()
        return
    
    print(f"✅ 找到 {len(tax_emails)} 封和运国际发票邮件")
    print(f"   共 {sum(len(e['links']) for e in tax_emails)} 个下载链接\n")
    
    # 启动浏览器
    print("🚀 启动浏览器...")
    downloaded = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        
        for idx, email in enumerate(tax_emails):
            for link_idx, link in enumerate(email['links']):
                print(f"\n[{idx+1}/{len(tax_emails)}] {email['subject'][:40]}...")
                print(f"   链接: {link[:60]}...")
                
                try:
                    page = context.new_page()
                    page.goto(link, wait_until='networkidle', timeout=60000)
                    time.sleep(3)
                    
                    # 找PDF下载按钮
                    selectors = [
                        'button:has-text("PDF下载")',
                        'button:has-text("下载")',
                        'a:has-text("PDF")'
                    ]
                    
                    found = False
                    for selector in selectors:
                        try:
                            btn = page.locator(selector)
                            if btn.count() > 0:
                                print(f"   找到按钮: {selector}")
                                
                                with page.expect_download(timeout=60000) as download_info:
                                    btn.first.click()
                                    time.sleep(5)
                                
                                download = download_info.value
                                
                                # 生成文件名
                                date_str = email['date'].strftime('%Y%m%d')
                                match = re.search(r'cs=2_(\d+)', link)
                                inv_num = match.group(1) if match else str(int(time.time()))
                                filename = f"heyun_{date_str}_{inv_num}.pdf"
                                save_path = os.path.join(ATTACHMENTS_DIR, filename)
                                
                                download.save_as(save_path)
                                
                                print(f"   ✅ 下载成功: {filename}")
                                downloaded.append({
                                    'filename': filename,
                                    'subject': email['subject'],
                                    'date': email['date'].strftime('%Y-%m-%d')
                                })
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
    
    mailbox.logout()
    
    # 输出结果
    print("\n" + "="*60)
    print(f"📊 浏览器下载完成: {len(downloaded)}/{sum(len(e['links']) for e in tax_emails)}")
    print("="*60)
    
    for d in downloaded:
        print(f"   ✅ {d['filename']} ({d['date']})")
    
    # 更新Excel
    if downloaded:
        print("\n📝 更新Excel报告...")
        try:
            import pandas as pd
            excel_path = os.path.join(OUTPUT_DIR, "发票目录.xlsx")
            df = pd.read_excel(excel_path)
            
            # 添加新记录
            new_records = []
            for d in downloaded:
                new_records.append({
                    '邮件主题': d['subject'],
                    '邮件时间': d['date'],
                    '发件人': 'browser@和运国际',
                    '发票金额': '',
                    '分类': 'A',
                    '状态': 'success',
                    '备注': '浏览器下载',
                    '附件名称': d['filename'],
                    '保存名称': d['filename'],
                    '错误类型': ''
                })
            
            df_new = pd.DataFrame(new_records)
            df = pd.concat([df, df_new], ignore_index=True)
            df.to_excel(excel_path, index=False)
            print(f"✅ Excel已更新: {excel_path}")
        except Exception as e:
            print(f"⚠️ Excel更新失败: {e}")

if __name__ == "__main__":
    import time
    process_with_browser()
