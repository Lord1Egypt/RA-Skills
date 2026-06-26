import smtplib
import ssl
from email.message import EmailMessage
import os

def load_credentials(env_path=r"C:\Users\Administrator\.openclaw\secrets\mail_qq.env"):
    """从env文件加载MAIL_USER和MAIL_PASS。"""
    creds = {}
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        k, v = line.split('=', 1)
                        creds[k.strip()] = v.strip()
    return creds

def build_message(sender, to, subject, body, cc=None, bcc=None):
    """构建带有适当编码的EmailMessage。"""
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = to
    if cc:
        msg['Cc'] = cc
    if bcc:
        msg['Bcc'] = bcc
    msg['Subject'] = subject
    msg.set_content(body, charset='utf-8')
    return msg

def send_email(to, subject, body, cc=None, bcc=None):
    """
    通过QQ SMTP发送邮件。
    使用SSL连接端口465。
    """
    creds = load_credentials()
    user = creds.get('MAIL_USER')
    password = creds.get('MAIL_PASS')
    if not user or not password:
        raise ValueError("凭据文件中缺少MAIL_USER或MAIL_PASS。")

    msg = build_message(user, to, subject, body, cc, bcc)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.qq.com', 465, context=context) as server:
        server.login(user, password)
        server.send_message(msg)
    print(f"邮件已发送至 {to}")

if __name__ == "__main__":
    # 示例用途（可保留用于测试或删除）
    import sys
    if len(sys.argv) >= 4:
        send_email(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("用法: python qq_mail_sender.py <收件人> <主题> <正文>")