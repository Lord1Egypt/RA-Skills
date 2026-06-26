#!/usr/bin/env python3
"""
发送邮件脚本
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.qq.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '465'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')

def check_config():
    """检查配置"""
    if not SMTP_USER or not SMTP_PASS:
        print("错误: 请在 .env 文件中填入 SMTP_USER 和 SMTP_PASS")
        print("\n配置示例:")
        print("SMTP_USER=your_email@qq.com")
        print("SMTP_PASS=your_auth_code")
        sys.exit(1)

def send_email(to_email, subject, body):
    """发送邮件"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        print(f"发送邮件到: {to_email}")
        print(f"主题: {subject}")
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 连接SMTP服务器并发送
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())
        server.quit()
        
        print("\n✅ 邮件发送成功!")
        return True
        
    except Exception as e:
        print(f"\n❌ 发送失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='发送邮件')
    parser.add_argument('--to', required=True, help='收件人邮箱')
    parser.add_argument('--subject', required=True, help='邮件主题')
    parser.add_argument('--body', required=True, help='邮件正文')
    parser.add_argument('--file', help='从文件读取正文')
    
    args = parser.parse_args()
    
    check_config()
    
    # 读取邮件正文
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                body = f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            sys.exit(1)
    else:
        body = args.body
    
    send_email(args.to, args.subject, body)

if __name__ == '__main__':
    main()
