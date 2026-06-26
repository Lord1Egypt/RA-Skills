#!/usr/bin/env python3
# smtp_send.py — 使用系统 Python smtplib + QQ 邮箱发送科技简报打包 ZIP。
# 用法: python3 scripts/smtp_send.py <zip_path> <收件人邮箱> [--subject 标题] [--sender 发件人邮箱] [--passwd 密码]
#
# 环境变量覆盖:
# SMTP_SENDER      QQ 邮箱发件人（默认从参数/环境变量读）
# SMTP_PASSWD     QQ 客户端授权码（默认从参数/环境变量读）
# SMTP_SERVER      服务器（默认 smtp.qq.com）
# SMTP_PORT        端口（默认 465）

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr

DEFAULT_SENDER = os.environ.get("SMTP_SENDER", sys.argv[2] if len(sys.argv) > 2 else "")
DEFAULT_PASSWD = os.environ.get("SMTP_PASSWD", "")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))


def send_email_with_attachment(
    zip_path: str,
    recipient: str,
    subject: str = None,
    sender: str = None,
    password: str = None,
    server: str = SMTP_SERVER,
    port: int = SMTP_PORT
) -> bool:
    """发送带附件的邮件。

    Args:
        zip_path: 完整路径的 ZIP 文件
        recipient: 收件人邮箱
        subject: 邮件主题，默认 "科技简报-今日xx班新闻信息"
        sender: 发件人 QQ 邮箱
        password: QQ 客户端授权码
        server: SMTP 服务器地址
        port: 端口（默认 465 SSL）

    Returns:
        是否发送成功
    """
    subject = subject or f"科技简报-{os.path.basename(zip_path).replace('.zip','')}"
    sender = sender or DEFAULT_SENDER
    password = password or DEFAULT_PASSWD

    if not all([sender, password, recipient, zip_path, os.path.exists(zip_path)]):
        print("[错误] 缺少必要参数或 ZIP 不存在", file=sys.stderr)
        return False

    msg = MIMEMultipart()
    msg["From"] = formataddr(("科技简报机器人", sender))
    msg["To"] = recipient
    msg["Subject"] = subject

    body = "请查收今日科技新闻简报文件包。"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with open(zip_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(zip_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(zip_path)}"'
        msg.attach(part)
    except Exception as e:
        print(f"[错误] 附件添加失败: {e}", file=sys.stderr)
        return False

    try:
        smtp = smtplib.SMTP_SSL(server, port)
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, msg.as_string())
        smtp.quit()
        print(f"[成功] 邮件已发送到 {recipient}")
        return True
    except Exception as e:
        print(f"[错误] 邮件发送失败: {e}", file=sys.stderr)
        return False




if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/smtp_send.py <zip_path> <收件人邮箱> [--subject 标题] [--sender 发件人邮箱] [--passwd 密码]", file=sys.stderr)
        sys.exit(1)

    zip_path = os.path.abspath(sys.argv[1])
    recipient = sys.argv[2]

    subject = None
    sender = None
    password = None
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--subject" and i + 1 < len(sys.argv):
            subject = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--sender" and i + 1 < len(sys.argv):
            sender = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--passwd" and i + 1 < len(sys.argv):
            password = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    ok = send_email_with_attachment(zip_path, recipient, subject=subject, sender=sender, password=password)
    sys.exit(0 if ok else 1)
