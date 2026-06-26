#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12306火车票发票下载器 - 直接下载附件链接
"""

import os
import sys
import re
import io
import requests
import time
import zipfile
import shutil
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

def process_12306():
    """处理12306火车票发票"""
    print("="*70)
    print("🚄 12306火车票发票下载器")
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
    
    # 搜索12306邮件
    criteria = A(date_gte=date_from)
    all_msgs = list(mailbox.fetch(criteria, reverse=True, limit=500))
    
    target_emails = []
    
    for msg in all_msgs:
        if not msg.subject:
            continue
        
        msg_date = msg.date.date() if isinstance(msg.date, datetime) else msg.date
        if not (date_from <= msg_date <= date_to):
            continue
        
        # 12306相关邮件
        if '网上购票' in msg.subject and ('改签' in msg.subject or '支付' in msg.subject):
            text = (msg.text or "") + (msg.html or "")
            
            # 查找电子发票链接（通常是zip压缩包）
            # 12306的发票链接格式
            invoice_links = re.findall(r'https?://[^\s"<>]+\.zip[^\s"<>]*', text)
            
            # 也查找一般的发票下载链接
            if not invoice_links:
                # 查找包含 invoice、download、fapiao 的链接
                all_links = re.findall(r'https?://[^\s"<>]+12306[^\s"<>]+', text)
                invoice_links = [l for l in all_links if any(k in l.lower() for k in ['invoice', 'download', 'fapiao', '电子发票'])]
            
            if invoice_links:
                target_emails.append({
                    'subject': msg.subject,
                    'date': msg_date,
                    'links': invoice_links[:2]  # 最多2个链接
                })
    
    if not target_emails:
        print("⚠️ 未找到12306发票邮件")
        mailbox.logout()
        return
    
    print(f"✅ 找到 {len(target_emails)} 封12306发票邮件\n")
    
    downloaded = []
    failed = []
    
    for idx, email in enumerate(target_emails):
        print(f"[{idx+1}/{len(target_emails)}] {email['subject'][:50]}...")
        print(f"   日期: {email['date']}")
        
        for link in email['links']:
            print(f"   🔗 链接: {link[:60]}...")
            
            success, data, error = download_with_retry(link)
            
            if success:
                # 判断文件类型
                is_zip = data[:4] == b'\x50\x4b\x03\x04'  # ZIP magic number
                
                if is_zip:
                    # 保存ZIP文件
                    date_str = email['date'].strftime('%Y%m%d')
                    zip_filename = f"12306_{date_str}_{int(time.time())}.zip"
                    zip_path = os.path.join(ATTACHMENTS_DIR, zip_filename)
                    
                    with open(zip_path, 'wb') as f:
                        f.write(data)
                    
                    print(f"   ✅ ZIP下载成功: {zip_filename}")
                    
                    # 解压ZIP
                    try:
                        import tempfile
                        with tempfile.TemporaryDirectory() as tmpdir:
                            with zipfile.ZipFile(zip_path, 'r') as zf:
                                zf.extractall(tmpdir)
                                
                                # 移动PDF文件
                                for f in os.listdir(tmpdir):
                                    if f.lower().endswith('.pdf'):
                                        src = os.path.join(tmpdir, f)
                                        pdf_filename = f"12306_{date_str}_{f}"
                                        dst = os.path.join(ATTACHMENTS_DIR, pdf_filename)
                                        shutil.copy2(src, dst)
                                        
                                        print(f"   ✅ 解压PDF: {pdf_filename}")
                                        downloaded.append({
                                            'filename': pdf_filename,
                                            'subject': email['subject'],
                                            'date': email['date'].strftime('%Y-%m-%d'),
                                            'source': '12306火车票'
                                        })
                        
                        # 删除ZIP文件
                        os.remove(zip_path)
                        
                    except Exception as e:
                        print(f"   ⚠️ 解压失败: {e}")
                        # 保留ZIP文件供手动解压
                        downloaded.append({
                            'filename': zip_filename,
                            'subject': email['subject'],
                            'date': email['date'].strftime('%Y-%m-%d'),
                            'source': '12306火车票(ZIP)'
                        })
                else:
                    # 直接是PDF
                    date_str = email['date'].strftime('%Y%m%d')
                    filename = f"12306_{date_str}_{int(time.time())}.pdf"
                    save_path = os.path.join(ATTACHMENTS_DIR, filename)
                    
                    with open(save_path, 'wb') as f:
                        f.write(data)
                    
                    print(f"   ✅ PDF下载成功: {filename}")
                    downloaded.append({
                        'filename': filename,
                        'subject': email['subject'],
                        'date': email['date'].strftime('%Y-%m-%d'),
                        'source': '12306火车票'
                    })
            else:
                print(f"   ❌ 下载失败: {error}")
                failed.append({'subject': email['subject'], 'error': error})
    
    mailbox.logout()
    
    # 输出结果
    print("\n" + "="*70)
    print(f"📊 12306下载完成: {len(downloaded)} 张")
    print("="*70)
    
    for d in downloaded:
        print(f"   ✅ {d['filename']}")
    
    if failed:
        print(f"\n❌ 失败: {len(failed)} 张")
        for f in failed:
            print(f"   - {f['subject'][:40]}...")
    
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
                    '发件人': f"download@{d['source']}",
                    '发票金额': '',
                    '分类': 'A',
                    '状态': 'success',
                    '备注': f'链接下载 [{d["source"]}]',
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
    process_12306()
