#!/usr/bin/env python3
"""分析邮件 - 按主题分类"""

import imaplib
import ssl
import json
from email.parser import BytesParser
from pathlib import Path
from collections import defaultdict
import time
import sys
import argparse

CONFIG_FILE = Path.home() / '.openclaw' / 'credentials' / 'email-accounts.json'

def decode_subject(subject):
    """解码 UTF-8 Base64 编码的主题"""
    if subject.startswith('=?'):
        try:
            from email.header import decode_header
            decoded = decode_header(subject)
            return ''.join(
                text.decode(charset or 'utf-8') if isinstance(text, bytes) else text
                for text, charset in decoded
            )
        except:
            return subject
    return subject

def analyze_emails(account='qq_3421', limit=1000):
    """分析邮件"""
    
    with open(CONFIG_FILE) as f:
        config = json.load(f)[account]
    
    print(f"📧 开始分析 {account} 邮箱...\n")
    
    # 连接
    context = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context)
    imap.login(config['email'], config['auth_code'])
    imap.select('INBOX')
    
    # 搜索
    status, messages = imap.search(None, 'ALL')
    msg_ids = messages[0].split()[-limit:]
    
    print(f"📊 找到 {len(msg_ids)} 封邮件\n")
    print("⏳ 正在分析...")
    
    # 分类统计
    categories = defaultdict(list)
    from_stats = defaultdict(int)
    
    start = time.time()
    
    # 批量 fetch
    if msg_ids:
        status, msg_data_list = imap.fetch(b','.join(msg_ids), '(RFC822)')
    else:
        msg_data_list = []
    
    # 解析邮件
    i = 0
    count = 0
    while i < len(msg_data_list):
        if isinstance(msg_data_list[i], tuple):
            try:
                msg = BytesParser().parsebytes(msg_data_list[i][1])
                
                from_addr = msg.get('From', 'Unknown')
                subject = msg.get('Subject', '(no subject)')
                date = msg.get('Date', '')
                
                # 解码主题
                subject = decode_subject(subject)
                
                # 提取发件人
                if '<' in from_addr:
                    from_name = from_addr.split('<')[0].strip()
                else:
                    from_name = from_addr.split('@')[0] if '@' in from_addr else from_addr
                
                from_name = decode_subject(from_name)
                from_stats[from_name] += 1
                
                subject_lower = subject.lower()
                
                if '旅行' in subject_lower or '机票' in subject_lower or '酒店' in subject_lower or 'agoda' in subject_lower:
                    category = '🛫 旅行监控'
                elif 'facebook' in subject_lower or 'twitter' in subject_lower or 'instagram' in subject_lower:
                    category = '📱 社交媒体'
                elif '验证' in subject_lower or 'verify' in subject_lower or 'confirm' in subject_lower:
                    category = '🔐 验证码'
                elif '订单' in subject_lower or 'order' in subject_lower or 'invoice' in subject_lower or 'jd' in subject_lower:
                    category = '🛒 订单'
                elif '通知' in subject_lower or 'notification' in subject_lower or 'alert' in subject_lower:
                    category = '🔔 通知'
                elif 'dsm' in subject_lower or 'synology' in subject_lower or 'nas' in subject_lower or 'truenas' in subject_lower:
                    category = '💾 NAS/服务器'
                elif 'github' in subject_lower or 'gitlab' in subject_lower or 'git' in subject_lower:
                    category = '🔧 开发工具'
                elif 'apple' in subject_lower or 'iphone' in subject_lower:
                    category = '🍎 Apple'
                else:
                    category = '📌 其他'
                
                categories[category].append({
                    'from': from_name,
                    'subject': subject,
                    'date': date,
                })
                
                count += 1
                if count % 100 == 0:
                    print(f"  已处理 {count} 封邮件...")
            
            except Exception as e:
                pass
        
        i += 1
    
    elapsed = time.time() - start
    
    imap.close()
    imap.logout()
    
    print(f"\n✅ 分析完成 ({elapsed:.1f}s)\n")
    
    # 输出统计
    print("=" * 70)
    print("📊 邮件分类统计")
    print("=" * 70)
    
    total = sum(len(v) for v in categories.values())
    
    for category in sorted(categories.keys()):
        emails = categories[category]
        percentage = (len(emails) / total * 100) if total > 0 else 0
        print(f"\n{category}: {len(emails)} 封 ({percentage:.1f}%)")
        
        # 显示该分类的前5个发件人
        from_count = defaultdict(int)
        for email in emails:
            from_count[email['from']] += 1
        
        top_from = sorted(from_count.items(), key=lambda x: x[1], reverse=True)[:5]
        for from_name, count in top_from:
            print(f"  • {from_name}: {count} 封")
    
    print("\n" + "=" * 70)
    print("👥 发件人排行 TOP 20")
    print("=" * 70)
    
    top_senders = sorted(from_stats.items(), key=lambda x: x[1], reverse=True)[:20]
    for i, (sender, count) in enumerate(top_senders, 1):
        percentage = (count / total * 100) if total > 0 else 0
        print(f"{i:2}. {sender:40} {count:4} 封 ({percentage:5.1f}%)")
    
    print(f"\n📈 总计: {total} 封邮件")
    print(f"⏱️  平均处理速度: {total/elapsed:.0f} 封/秒")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='📧 分析邮件')
    parser.add_argument('--account', default='qq_3421', help='账户名称')
    parser.add_argument('--limit', type=int, default=1000, help='分析数量')
    
    args = parser.parse_args()
    
    analyze_emails(args.account, args.limit)
