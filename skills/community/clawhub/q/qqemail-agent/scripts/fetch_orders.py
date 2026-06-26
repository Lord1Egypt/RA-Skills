#!/usr/bin/env python3
"""
读取QQ邮箱订单邮件脚本
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

IMAP_HOST = os.getenv('IMAP_HOST', 'imap.qq.com')
IMAP_PORT = int(os.getenv('IMAP_PORT', '993'))
IMAP_USER = os.getenv('IMAP_USER', '')
IMAP_PASS = os.getenv('IMAP_PASS', '')

def check_config():
    """检查配置"""
    if not IMAP_USER or not IMAP_PASS:
        print("错误: 请在 .env 文件中填入 IMAP_USER 和 IMAP_PASS")
        print("\n配置示例:")
        print("IMAP_USER=your_email@qq.com")
        print("IMAP_PASS=your_auth_code")
        sys.exit(1)

def fetch_emails(days=30):
    """读取最近N天的邮件"""
    try:
        from imap_tools import MailBox, AND
        
        print(f"连接邮箱: {IMAP_USER}")
        print(f"服务器: {IMAP_HOST}:{IMAP_PORT}")
        
        with MailBox(IMAP_HOST, IMAP_PORT).login(IMAP_USER, IMAP_PASS) as mailbox:
            # 获取最近N天的邮件
            date_since = datetime.now() - timedelta(days=days)
            print(f"\n读取最近 {days} 天的邮件...\n")
            
            emails = []
            for msg in mailbox.fetch(AND(date_gte=date_since.date()), limit=50, reverse=True):
                emails.append({
                    'subject': msg.subject,
                    'from': msg.from_,
                    'date': msg.date,
                    'text': msg.text or msg.html
                })
            
            print(f"共获取 {len(emails)} 封邮件\n")
            
            for i, email in enumerate(emails, 1):
                print(f"{i}. [{email['date']}] {email['subject']}")
                print(f"   From: {email['from']}")
                print()
            
            return emails
            
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    check_config()
    
    # 默认读取30天，可通过参数指定
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except:
            pass
    
    emails = fetch_emails(days)
    
    print("\n" + "="*50)
    print("提示: 邮件内容已获取")
    print("后续解析订单请交由 AI 处理")
    print("="*50)
