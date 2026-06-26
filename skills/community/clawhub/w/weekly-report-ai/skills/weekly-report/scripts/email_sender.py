#!/usr/bin/env python3
"""
邮件发送脚本
支持SMTP发送周报邮件
"""

import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime


def send_email(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    to_addrs: list,
    subject: str,
    content: str,
    is_html: bool = False
) -> dict:
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = username
        msg['To'] = ', '.join(to_addrs)
        
        # 添加内容
        content_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(content, content_type, 'utf-8'))
        
        # 连接SMTP服务器
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
        
        # 登录
        server.login(username, password)
        
        # 发送
        server.send_message(msg)
        server.quit()
        
        return {"success": True, "message": "邮件发送成功"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def markdown_to_html(markdown: str) -> str:
    """简单的Markdown转HTML"""
    import re
    
    html = markdown
    
    # 标题
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 链接
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # 列表
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html)
    
    # 换行
    html = html.replace('\n\n', '</p><p>')
    
    # 包裹完整HTML
    html = f'''
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 20px; }}
            h1, h2, h3 {{ color: #333; }}
            ul {{ padding-left: 20px; }}
            li {{ margin: 5px 0; }}
            code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    '''
    
    return html


def main():
    parser = argparse.ArgumentParser(description="发送周报邮件")
    parser.add_argument("--smtp-host", required=True, help="SMTP服务器地址")
    parser.add_argument("--smtp-port", type=int, default=465, help="SMTP端口")
    parser.add_argument("--username", required=True, help="邮箱账号")
    parser.add_argument("--password", required=True, help="邮箱密码/授权码")
    parser.add_argument("--to", nargs="+", required=True, help="收件人列表")
    parser.add_argument("--subject", required=True, help="邮件主题")
    parser.add_argument("--content", required=True, help="邮件内容")
    parser.add_argument("--html", action="store_true", help="内容为HTML格式")
    
    args = parser.parse_args()
    
    result = send_email(
        smtp_host=args.smtp_host,
        smtp_port=args.smtp_port,
        username=args.username,
        password=args.password,
        to_addrs=args.to,
        subject=args.subject,
        content=args.content,
        is_html=args.html
    )
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
