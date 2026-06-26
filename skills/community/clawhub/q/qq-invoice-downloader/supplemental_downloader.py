#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充发票下载器 - 处理寿司郎、中海油等
"""

import os
import sys
import re
import io
import requests
import time
from datetime import datetime, date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EMAIL = "181957682@qq.com"
PASSWORD = "dcdrfqjmoczrbhdj"
IMAP_SERVER = "imap.qq.com"

OUTPUT_DIR = r"Z:\OpenClaw\InvoiceOC\260106-260308_v5"
ATTACHMENTS_DIR = os.path.join(OUTPUT_DIR, "attachments")

def download_with_retry(url, max_retries=3):
    """带重试的下载"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 100:
                return True, resp.content, ""
            else:
                error = f"HTTP {resp.status_code}"
        except Exception as e:
            error = str(e)[:40]
        
        if attempt < max_retries - 1:
            wait = 2 * (attempt + 1)
            print(f"      ⏳ 重试 {attempt+1}/{max_retries}...")
            time.sleep(wait)
    
    return False, None, error

def process_supplemental():
    """处理补充发票"""
    print("="*70)
    print("📥 补充发票下载器")
    print("="*70)
    
    try:
        from imap_tools import MailBox, A
    except ImportError:
        print("❌ 请先安装: pip install imap-tools")
        return
    
    # 连接邮箱
    print("\n🔌 连接邮箱...")
    try:
        mailbox = MailBox(IMAP_SERVER)
        mailbox.login(EMAIL, PASSWORD)
        print("✅ 登录成功\n")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return
    
    date_from = date(2026, 1, 6)
    date_to = date(2026, 3, 8)
    
    downloaded = []
    failed = []
    
    # 1. 处理寿司郎（诺诺发票）
    print("🔍 搜索寿司郎发票...")
    criteria = A(date_gte=date_from)
    all_msgs = list(mailbox.fetch(criteria, reverse=True, limit=500))
    
    for msg in all_msgs:
        if not msg.subject or '寿司郎' not in msg.subject:
            continue
        
        msg_date = msg.date.date() if isinstance(msg.date, datetime) else msg.date
        if not (date_from <= msg_date <= date_to):
            continue
        
        print(f"\n📧 {msg.subject[:50]}...")
        
        text = (msg.text or "") + (msg.html or "")
        
        # 查找诺诺发票链接
        # 格式: https://nnfp.jss.com.cn/xxxxx
        nnfp_links = re.findall(r'https://nnfp\.jss\.com\.cn/[A-Za-z0-9_-]+', text)
        
        if nnfp_links:
            for link in nnfp_links:
                print(f"   🔗 诺诺发票链接: {link[:50]}...")
                
                # 尝试下载
                success, data, error = download_with_retry(link)
                
                if success:
                    # 检查是否是PDF
                    if data[:4] == b'%PDF':
                        filename = f"shuweilang_{msg_date.strftime('%Y%m%d')}_{int(time.time())}.pdf"
                        save_path = os.path.join(ATTACHMENTS_DIR, filename)
                        
                        with open(save_path, 'wb') as f:
                            f.write(data)
                        
                        print(f"   ✅ 下载成功: {filename}")
                        downloaded.append({
                            'filename': filename,
                            'subject': msg.subject,
                            'date': msg_date.strftime('%Y-%m-%d'),
                            'source': '诺诺发票'
                        })
                        break
                    else:
                        print(f"   ⚠️ 不是PDF文件")
                else:
                    print(f"   ❌ 下载失败: {error}")
                    failed.append({'subject': msg.subject, 'error': error})
        else:
            print(f"   ⚠️ 未找到诺诺发票链接")
    
    # 2. 处理中海油电子发票
    print("\n🔍 搜索中海油发票...")
    for msg in all_msgs:
        if not msg.subject or '电子发票下载' not in msg.subject:
            continue
        
        msg_date = msg.date.date() if isinstance(msg.date, datetime) else msg.date
        if not (date_from <= msg_date <= date_to):
            continue
        
        print(f"\n📧 {msg.subject[:50]}...")
        
        text = (msg.text or "") + (msg.html or "")
        
        # 查找中海油下载链接
        cnooc_links = re.findall(r'https://mobile-zzslg\.cnooc\.com\.cn/eetb/api-eetb/invoice/[^\s"<>]+', text)
        
        if cnooc_links:
            for link in cnooc_links:
                print(f"   🔗 中海油链接: {link[:50]}...")
                
                success, data, error = download_with_retry(link)
                
                if success:
                    filename = f"cnooc_{msg_date.strftime('%Y%m%d')}_{int(time.time())}.pdf"
                    save_path = os.path.join(ATTACHMENTS_DIR, filename)
                    
                    with open(save_path, 'wb') as f:
                        f.write(data)
                    
                    print(f"   ✅ 下载成功: {filename}")
                    downloaded.append({
                        'filename': filename,
                        'subject': msg.subject,
                        'date': msg_date.strftime('%Y-%m-%d'),
                        'source': '中海油'
                    })
                    break
                else:
                    print(f"   ❌ 下载失败: {error}")
        else:
            print(f"   ⚠️ 未找到中海油链接")
    
    # 3. 处理支付宝发票（重新尝试附件）
    print("\n🔍 重新处理支付宝发票...")
    for msg in all_msgs:
        if not msg.subject or '发票文件导出成功' not in msg.subject:
            continue
        
        msg_date = msg.date.date() if isinstance(msg.date, datetime) else msg.date
        if not (date_from <= msg_date <= date_to):
            continue
        
        print(f"\n📧 {msg.subject[:50]}...")
        
        if msg.attachments:
            for att in msg.attachments:
                filename = att.filename
                if filename and filename.lower().endswith('.pdf'):
                    try:
                        unique_name = f"alipay_{msg_date.strftime('%Y%m%d')}_{int(time.time())}.pdf"
                        save_path = os.path.join(ATTACHMENTS_DIR, unique_name)
                        
                        with open(save_path, 'wb') as f:
                            f.write(att.payload)
                        
                        print(f"   ✅ 附件下载成功: {unique_name}")
                        downloaded.append({
                            'filename': unique_name,
                            'subject': msg.subject,
                            'date': msg_date.strftime('%Y-%m-%d'),
                            'source': '支付宝'
                        })
                    except Exception as e:
                        print(f"   ❌ 附件保存失败: {e}")
        else:
            print(f"   ⚠️ 无附件")
    
    mailbox.logout()
    
    # 输出结果
    print("\n" + "="*70)
    print(f"📊 补充下载完成: {len(downloaded)} 张")
    print("="*70)
    
    for d in downloaded:
        print(f"   ✅ {d['filename']} ({d['source']})")
    
    if failed:
        print(f"\n❌ 失败: {len(failed)} 张")
        for f in failed:
            print(f"   - {f['subject'][:40]}...: {f['error']}")
    
    # 更新Excel
    if downloaded:
        print("\n📝 更新Excel报告...")
        try:
            import pandas as pd
            excel_path = os.path.join(OUTPUT_DIR, "发票目录.xlsx")
            df = pd.read_excel(excel_path)
            
            new_records = []
            for d in downloaded:
                new_records.append({
                    '邮件主题': d['subject'],
                    '邮件时间': d['date'],
                    '发件人': f"supplemental@{d['source']}",
                    '发票金额': '',
                    '分类': 'A',
                    '状态': 'success',
                    '备注': f'补充下载 [{d["source"]}]',
                    '附件名称': d['filename'],
                    '保存名称': d['filename'],
                    '错误类型': ''
                })
            
            df_new = pd.DataFrame(new_records)
            df = pd.concat([df, df_new], ignore_index=True)
            df.to_excel(excel_path, index=False)
            print(f"✅ Excel已更新")
        except Exception as e:
            print(f"⚠️ Excel更新失败: {e}")

if __name__ == "__main__":
    process_supplemental()
