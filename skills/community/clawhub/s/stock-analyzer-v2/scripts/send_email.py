#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送脚本

支持 QQ邮箱 和 Gmail，通过环境变量注入凭证（安全）。

使用方法:
    # 先配置环境变量
    export QQ_EMAIL_AUTH_CODE="your_auth_code"
    
    python scripts/send_email.py --to 收件人@example.com --file report.md
    
    # Gmail
    export GMAIL_APP_PASSWORD="your_app_password"
    python scripts/send_email.py --to 收件人@gmail.com --smtp gmail --app-password "$GMAIL_APP_PASSWORD"
"""

import argparse
import os
import smtplib
import ssl
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def get_auth_code():
    """从环境变量获取 QQ 邮箱授权码"""
    code = os.environ.get('QQ_EMAIL_AUTH_CODE')
    if not code:
        print("❌ 未设置 QQ_EMAIL_AUTH_CODE 环境变量")
        print('请运行: export QQ_EMAIL_AUTH_CODE="your_auth_code"')
        sys.exit(1)
    return code

def get_gmail_password():
    """从环境变量获取 Gmail 应用密码"""
    pw = os.environ.get('GMAIL_APP_PASSWORD')
    if not pw:
        print("❌ 未设置 GMAIL_APP_PASSWORD 环境变量")
        print('请运行: export GMAIL_APP_PASSWORD="your_app_password"')
        sys.exit(1)
    return pw

def send_via_qq(to_email, auth_code, file_path, subject=None):
    """通过 QQ 邮箱发送邮件"""
    SMTP_SERVER = 'smtp.qq.com'
    SMTP_PORT = 465

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    msg = MIMEMultipart()
    msg['From'] = formataddr(('Stock Analyzer', to_email))
    msg['To'] = formataddr(('Recipient', to_email))

    if subject is None:
        import os as _os
        subject = f'📊 股票分析报告 | {_os.path.basename(file_path)}'
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    print(f"正在连接 QQ 邮箱 SMTP 服务器...")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30, context=context) as smtp:
        smtp.login(to_email, auth_code)
        print("✅ 登录成功")
        smtp.sendmail(to_email, to_email, msg.as_string())
        print("✅ 邮件发送成功")

def send_via_gmail(to_email, app_password, file_path, subject=None):
    """通过 Gmail 发送邮件"""
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    msg = MIMEMultipart()
    msg['From'] = to_email
    msg['To'] = to_email

    if subject is None:
        import os as _os
        subject = f'📊 股票分析报告 | {_os.path.basename(file_path)}'
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    print(f"正在连接 Gmail SMTP 服务器...")
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(to_email, app_password)
        print("✅ 登录成功")
        smtp.sendmail(to_email, to_email, msg.as_string())
        print("✅ 邮件发送成功")

def main():
    parser = argparse.ArgumentParser(description='发送邮件（支持 QQ邮箱 / Gmail）')
    parser.add_argument('--to', type=str, required=True, help='收件人邮箱')
    parser.add_argument('--file', type=str, required=True, help='要发送的文件路径')
    parser.add_argument('--subject', type=str, help='邮件主题（可选）')
    parser.add_argument('--smtp', type=str, choices=['qq', 'gmail'], default='qq',
                       help='SMTP 服务类型（默认 qq）')
    parser.add_argument('--auth-code', type=str,
                       help='QQ 邮箱授权码（建议使用 QQ_EMAIL_AUTH_CODE 环境变量）')
    parser.add_argument('--app-password', type=str,
                       help='Gmail 应用密码（建议使用 GMAIL_APP_PASSWORD 环境变量）')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    try:
        if args.smtp == 'qq':
            # 优先使用参数，其次使用环境变量
            auth = args.auth_code or get_auth_code()
            send_via_qq(args.to, auth, args.file, args.subject)
        else:
            pw = args.app_password or get_gmail_password()
            send_via_gmail(args.to, pw, args.file, args.subject)

        print(f"\n📧 已发送到: {args.to}")

    except smtplib.SMTPAuthenticationError:
        print("❌ 认证失败：授权码/应用密码错误或邮箱地址错误")
        sys.exit(1)
    except smtplib.SMTPConnectError:
        print("❌ 连接失败：请检查网络或 SMTP 服务器地址")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
