#!/usr/bin/env python3
"""
腾讯企业邮箱 - 发送邮件脚本
使用 SMTP over SSL，服务器：smtp.exmail.qq.com:465
"""

import os
import sys
import argparse
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from pathlib import Path

# ── 服务器配置 ────────────────────────────────────────────
SMTP_HOST = "smtp.exmail.qq.com"
SMTP_PORT = 465  # SSL

# 海外用户备用（取消注释）
# SMTP_HOST = "hwsmtp.exmail.qq.com"


def get_credentials():
    """从环境变量读取凭据"""
    address = os.environ.get("EXMAIL_ADDRESS")
    password = os.environ.get("EXMAIL_PASSWORD")
    if not address or not password:
        print("❌ 错误：请设置环境变量 EXMAIL_ADDRESS 和 EXMAIL_PASSWORD")
        print("   在 OpenClaw 配置的 skills.entries.tencent-exmail.env 中配置")
        sys.exit(1)
    return address, password


def send_email(
    to_list: list[str],
    subject: str,
    body: str,
    cc_list: list[str] = None,
    bcc_list: list[str] = None,
    html: bool = False,
    attachments: list[str] = None,
):
    """发送邮件"""
    sender, password = get_credentials()

    # 构造邮件
    msg = MIMEMultipart("mixed")
    msg["From"] = sender
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject

    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    # 正文
    content_type = "html" if html else "plain"
    msg.attach(MIMEText(body, content_type, "utf-8"))

    # 附件
    if attachments:
        for filepath in attachments:
            path = Path(filepath)
            if not path.exists():
                print(f"⚠️  附件不存在，已跳过：{filepath}")
                continue

            mime_type, _ = mimetypes.guess_type(str(path))
            if mime_type is None:
                mime_type = "application/octet-stream"

            main_type, sub_type = mime_type.split("/", 1)

            with open(path, "rb") as f:
                data = f.read()

            if main_type == "text":
                part = MIMEText(data.decode("utf-8", errors="replace"), sub_type)
            else:
                part = MIMEBase(main_type, sub_type)
                part.set_payload(data)
                encoders.encode_base64(part)

            # 中文文件名处理
            filename = path.name
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=("utf-8", "", filename),
            )
            msg.attach(part)

    # 所有收件人（To + CC + BCC）
    all_recipients = list(to_list)
    if cc_list:
        all_recipients += cc_list
    if bcc_list:
        all_recipients += bcc_list

    # 发送
    try:
        print(f"📤 正在连接 {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(sender, password)
            server.sendmail(sender, all_recipients, msg.as_bytes())

        print(f"✅ 邮件发送成功！")
        print(f"   收件人：{', '.join(to_list)}")
        if cc_list:
            print(f"   抄送：{', '.join(cc_list)}")
        print(f"   主题：{subject}")
        if attachments:
            valid_attachments = [a for a in attachments if Path(a).exists()]
            print(f"   附件数：{len(valid_attachments)}")

    except smtplib.SMTPAuthenticationError:
        print("❌ 认证失败：请检查邮箱地址和密码")
        print("   如果账号绑定了微信，需要使用「客户端专用密码」")
        sys.exit(1)
    except smtplib.SMTPException as e:
        print(f"❌ 发送失败：{e}")
        sys.exit(1)
    except ConnectionRefusedError:
        print(f"❌ 连接被拒绝：请检查网络，确认端口 {SMTP_PORT} 已开放")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="腾讯企业邮箱发信工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 发送普通邮件
  python3 send_email.py --to user@example.com --subject "你好" --body "邮件内容"

  # 带抄送和附件
  python3 send_email.py \\
    --to a@example.com --to b@example.com \\
    --cc boss@company.com \\
    --subject "报告" --body "请查收附件" \\
    --attachment /path/to/report.pdf

  # 发送 HTML 邮件
  python3 send_email.py --to user@example.com --subject "HTML测试" \\
    --body "<h1>你好</h1><p>这是一封 HTML 邮件</p>" --html
        """,
    )
    parser.add_argument("--to", action="append", required=True, metavar="EMAIL", help="收件人（可多次使用）")
    parser.add_argument("--cc", action="append", default=[], metavar="EMAIL", help="抄送（可多次使用）")
    parser.add_argument("--bcc", action="append", default=[], metavar="EMAIL", help="密送（可多次使用）")
    parser.add_argument("--subject", required=True, help="邮件主题")
    parser.add_argument("--body", required=True, help="邮件正文")
    parser.add_argument("--html", action="store_true", help="以 HTML 格式发送正文")
    parser.add_argument("--attachment", action="append", default=[], metavar="FILE", help="附件路径（可多次使用）")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    send_email(
        to_list=args.to,
        subject=args.subject,
        body=args.body,
        cc_list=args.cc or None,
        bcc_list=args.bcc or None,
        html=args.html,
        attachments=args.attachment or None,
    )
