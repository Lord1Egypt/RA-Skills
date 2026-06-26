#!/usr/bin/env python3
"""
邮件发送脚本 - szzg007-product-promotion 配套工具

使用方式:
    python3 send-email.py <email_html_path> <to_email> [--subject <subject>]
"""

import sys
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime

# 配置
SMTP_HOST = "smtp.163.com"
SMTP_PORT = 465
SMTP_USER = "m13430467261@163.com"
SMTP_PASS = "FC27pgp77tc5Vvhv"
SMTP_FROM = "Judy <m13430467261@163.com>"


def send_email(html_path: str, to_email: str, subject: str = None) -> bool:
    """发送 HTML 邮件"""
    
    # 读取 HTML 内容
    html_file = Path(html_path)
    if not html_file.exists():
        print(f"❌ 文件不存在：{html_path}")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 生成主题
    if not subject:
        subject = f"✨ Special Offer - {datetime.now().strftime('%Y-%m-%d')}"
    
    # 创建邮件
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    
    # 添加纯文本版本 (备用)
    text_content = f"""
Special Offer - {datetime.now().strftime('%Y-%m-%d')}

View this email in your browser for the best experience.

{html_path}

Questions? Reply to this email.
"""
    
    part1 = MIMEText(text_content, "plain", "utf-8")
    part2 = MIMEText(html_content, "html", "utf-8")
    
    msg.attach(part1)
    msg.attach(part2)
    
    # 发送邮件
    try:
        print(f"\n📧 正在发送邮件到 {to_email}...")
        
        # 创建 SSL 上下文 (禁用证书验证用于测试)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # 连接 SMTP 服务器 (SSL)
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM, to_email, msg.as_string())
        
        print(f"✅ 邮件发送成功！")
        print(f"📬 收件人：{to_email}")
        print(f"📝 主题：{subject}")
        
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法：python3 send-email.py <email_html_path> <to_email> [--subject <subject>]")
        print("示例：python3 send-email.py /path/to/email.html test@example.com")
        sys.exit(1)
    
    html_path = sys.argv[1]
    to_email = sys.argv[2]
    subject = None
    
    if '--subject' in sys.argv:
        idx = sys.argv.index('--subject')
        if idx + 1 < len(sys.argv):
            subject = sys.argv[idx + 1]
    
    success = send_email(html_path, to_email, subject)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    sys.exit(main())
