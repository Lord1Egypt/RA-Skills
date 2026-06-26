#!/usr/bin/env python3
"""
QQ邮箱 IMAP 监听脚本
功能：监控白名单联系人的邮件，通过 openclaw message send 直接发 QQ 通知
"""

import os
import json
import imaplib
import email
from email.header import decode_header
import schedule
import time
import subprocess
from datetime import datetime

# ========== 配置区 ==========
EMAIL = "1257037084@qq.com"
AUTH_CODE = "xtepatkcgckvhjhf"
IMAP_SERVER = "imap.qq.com"
IMAP_PORT = 993

WHITELIST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whitelist.json")
PROCESSED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "processed_emails.json")
QQ_TARGET = "6E07D3F2F7EC1C7107ECF9D495FF4755"
# ==================================

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, 'r') as f:
            return [e.lower().strip() for e in json.load(f)]
    return []

def load_processed_ids():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except:
                return set()
    return set()

def save_processed_ids(ids):
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(list(ids), f, ensure_ascii=False)

def decode_str(s):
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            charset = charset or 'utf-8'
            try:
                result.append(part.decode(charset, errors='replace'))
            except:
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(str(part))
    return ''.join(result)

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='replace')
                    break
                except:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='replace')
        except:
            pass
    return body[:500]

def connect_mail():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, AUTH_CODE)
        mail.select('INBOX')
        return mail
    except Exception as e:
        print(f"[{datetime.now()}] 连接失败: {e}")
        return None

def summarize_with_ai(subject, body):
    """调用 OpenClaw AI 总结邮件内容（隔离session，不打扰用户）"""
    prompt = f"""你是邮件摘要助手。收到邮件后，提取关键信息，简洁输出。

邮件主题: {subject}
邮件内容: {body[:800]}

要求：
1. 一句话内说明邮件目的
2. 提取所有关键信息（验证码、金额、日期、链接等）用【】标注
3. 直接输出摘要，不要前缀"摘要："之类的废话
4. 50字以内
"""
    try:
        result = subprocess.run(
            [
                "openclaw", "agent",
                "--session-id", "email-summarizer",
                "-m", prompt,
                "--thinking", "off"
            ],
            capture_output=True, text=True, timeout=30,
            env={**os.environ, "OPENCLAW_SESSION_ID": "email-summarizer"}
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            print(f"AI 总结失败: {result.stderr[:100] if result.stderr else 'no output'}")
    except Exception as e:
        print(f"AI 总结异常: {e}")
    return None

def send_qq_message(msg):
    """直接通过 openclaw message send 发 QQ 消息，不创建会话"""
    escaped = msg.replace('"', '\\"').replace('\n', '\\n')
    cmd = [
        "openclaw", "message", "send",
        "--channel", "qqbot",
        "--target", QQ_TARGET,
        "--message", msg
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            return True
        else:
            print(f"发送失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"发送异常: {e}")
        return False

def fetch_new_emails():
    whitelist = load_whitelist()
    processed_ids = load_processed_ids()

    if not whitelist:
        print(f"[{datetime.now()}] 白名单为空，跳过检查")
        return

    mail = connect_mail()
    if mail is None:
        return

    try:
        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            return

        email_ids = messages[0].split()
        if not email_ids:
            return

        # 初始化已处理记录：首次运行时设为最新邮件ID，避免重复处理旧邮件
        if not processed_ids and email_ids:
            latest_id = email_ids[-1].decode()
            processed_ids.add(latest_id)
            save_processed_ids(processed_ids)
            print(f"[{datetime.now()}] 首次运行，初始化已处理记录: {latest_id}")

        new_count = 0

        # 反转遍历顺序：从最新到最旧
        # 一旦遇到已处理的ID，说明更旧的都已在 processed_ids 中，直接跳过
        for eid in reversed(email_ids[-20:]):
            status, msg_data = mail.fetch(eid, '(RFC822)')
            if status != 'OK':
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            msg_id = eid.decode()

            if msg_id in processed_ids:
                break  # 遇到已处理的，说明更旧的都处理过了，跳过

            from_addr = msg.get('From', '')
            sender = from_addr.lower()

            if '<' in sender and '>' in sender:
                sender_email = sender.split('<')[1].split('>')[0].strip()
            else:
                sender_email = sender.strip()

            is_whitelisted = any(
                w in sender_email or w in sender
                for w in whitelist
            )

            if not is_whitelisted:
                continue

            subject = decode_str(msg.get('Subject', '(无主题)'))
            body = get_email_body(msg)
            date = msg.get('Date', '')

            # AI 智能总结
            ai_summary = summarize_with_ai(subject, body)
            if ai_summary:
                preview = ai_summary
            elif len(body) <= 200:
                preview = body.replace('\n', ' ').strip()
            else:
                sentences = body.split('.')[:3]
                preview = '. '.join(sentences).strip()
                if len(preview) > 200:
                    preview = preview[:200]
                preview += '...'
            summary = f"📧 [{subject}]\n👤 {from_addr}\n📝 {preview}"

            if send_qq_message(summary):
                processed_ids.add(msg_id)
                new_count += 1

        if new_count > 0:
            save_processed_ids(processed_ids)
            print(f"[{datetime.now()}] 发送 {new_count} 条通知")
    finally:
        try:
            mail.logout()
        except:
            pass

def job():
    print(f"[{datetime.now()}] 检查新邮件...")
    fetch_new_emails()

def run_scheduler():
    schedule.every(30).seconds.do(job)
    print(f"[{datetime.now()}] 邮件监听服务已启动，每30秒检查一次")
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    whitelist = load_whitelist()
    if not whitelist:
        print("白名单为空，请先在 whitelist.json 中添加邮箱")
    else:
        print(f"白名单: {whitelist}")

    job()
    run_scheduler()
