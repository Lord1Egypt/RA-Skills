#!/usr/bin/env python3
"""语义搜索：拉取指定文件夹的邮件（Header+正文），预处理后输出供智能体做语义分析"""
import argparse
import json
import os
import sys
import imaplib
import re
import ssl
from email.header import decode_header
from email.parser import BytesParser
from email.utils import parseaddr


IMAP_HOST = 'imap.qq.com'
IMAP_PORT = 993

SKILL_ID = '7637538402895773731'
CRED_NAME = 'qq_email'
ENV_EMAIL = 'QQ_EMAIL'
ENV_AUTH_CODE = 'QQ_EMAIL_AUTH_CODE'
LEGACY_ENV_EMAIL = f'COZE_{CRED_NAME}_QQ_EMAIL_{SKILL_ID}'
LEGACY_ENV_AUTH_CODE = f'COZE_{CRED_NAME}_QQ_EMAIL_AUTH_CODE_{SKILL_ID}'

def quote_folder(name):
    """为含空格的文件夹名包裹双引号"""
    if not name:
        return name
    if name.startswith('"') and name.endswith('"'):
        return name
    if ' ' in name:
        return f'"{name}"'
    return name


MAX_FETCH = 100
BODY_PREVIEW_LEN = 500


def get_credentials():
    email_addr = os.environ.get(ENV_EMAIL) or os.environ.get(LEGACY_ENV_EMAIL, '')
    auth_code = os.environ.get(ENV_AUTH_CODE) or os.environ.get(LEGACY_ENV_AUTH_CODE, '')
    if not email_addr or not auth_code:
        return None, None
    return email_addr, auth_code


def decode_str(s):
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(charset or 'utf-8', errors='replace'))
            except (LookupError, UnicodeDecodeError):
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)


def strip_html(html):
    """去除HTML标签，提取纯文本"""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_body_text(msg, max_len=BODY_PREVIEW_LEN):
    """提取邮件正文纯文本，截断到max_len"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition', ''))
            if 'attachment' in content_disposition:
                continue
            if content_type == 'text/plain':
                charset = part.get_content_charset() or 'utf-8'
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode(charset, errors='replace')
                        break
                except (LookupError, UnicodeDecodeError):
                    continue
            elif content_type == 'text/html' and not body:
                charset = part.get_content_charset() or 'utf-8'
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = strip_html(payload.decode(charset, errors='replace'))
                except (LookupError, UnicodeDecodeError):
                    continue
    else:
        content_type = msg.get_content_type()
        charset = msg.get_content_charset() or 'utf-8'
        payload = msg.get_payload(decode=True)
        if payload:
            try:
                text = payload.decode(charset, errors='replace')
                if content_type == 'text/html':
                    body = strip_html(text)
                else:
                    body = text
            except (LookupError, UnicodeDecodeError):
                body = ""

    body = body.strip()
    if len(body) > max_len:
        body = body[:max_len] + "..."
    return body


def parse_date(msg):
    """解析邮件日期"""
    date_str = msg.get('Date', '')
    if not date_str:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return date_str


def has_attachments(msg):
    """判断邮件是否包含附件"""
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get('Content-Disposition', ''))
            if 'attachment' in content_disposition:
                return True
    return False


def fetch_folder_emails(mail, folder, limit):
    """从指定文件夹拉取邮件，返回预处理后的列表"""
    try:
        status, _ = mail.select(quote_folder(folder), readonly=True)
        if status != 'OK':
            return [], 0

        status, data = mail.search(None, 'ALL')
        if status != 'OK' or not data[0]:
            return [], 0

        mail_ids = data[0].split()
        total = len(mail_ids)

        # 取最新的 limit 封（倒序）
        mail_ids = mail_ids[-limit:] if limit > 0 else mail_ids
        mail_ids = list(reversed(mail_ids))

        results = []
        parser = BytesParser()

        for mid in mail_ids:
            try:
                status, msg_data = mail.fetch(mid, '(BODY.PEEK[])')
                if status != 'OK' or not msg_data or not msg_data[0]:
                    continue

                raw = None
                for item in msg_data:
                    if isinstance(item, tuple):
                        raw = item[1]
                        break
                if not raw:
                    continue

                msg = parser.parsebytes(raw)
                message_id = msg.get('Message-ID', '') or ''
                message_id = message_id.strip()

                results.append({
                    "mail_id": int(mid),
                    "folder": folder,
                    "subject": decode_str(msg.get('Subject', '')),
                    "from": decode_str(msg.get('From', '')),
                    "to": decode_str(msg.get('To', '')),
                    "date": parse_date(msg),
                    "body_preview": extract_body_text(msg),
                    "has_attachment": has_attachments(msg),
                    "message_id": message_id
                })
            except Exception as e:
                print(f"Warning: Failed to parse mail {mid}: {str(e)}", file=sys.stderr)

        return results, total

    except Exception as e:
        print(f"Error: Failed to fetch folder {folder}: {str(e)}", file=sys.stderr)
        return [], 0


def main():
    parser = argparse.ArgumentParser(description='语义搜索：拉取邮件供智能体做语义分析')
    parser.add_argument('--folder', required=True, help='邮箱文件夹名称')
    parser.add_argument('--limit', type=int, default=MAX_FETCH,
                        help=f'拉取邮件数量上限，默认{MAX_FETCH}；传0表示不限（最多{MAX_FETCH}）')
    args = parser.parse_args()

    email_addr, auth_code = get_credentials()
    if not email_addr or not auth_code:
        result = {"status": "error", "message": "缺少邮箱凭证，请配置QQ邮箱授权码"}
        print(json.dumps(result, ensure_ascii=False))
        return

    limit = args.limit if args.limit > 0 else MAX_FETCH
    limit = min(limit, MAX_FETCH)

    try:
        ctx = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'

        emails, total = fetch_folder_emails(mail, args.folder, limit)

        mail.logout()

        result = {
            "status": "success",
            "folder": args.folder,
            "total_in_folder": total,
            "total_fetched": len(emails),
            "fetched_limit": limit,
            "has_more": total > limit,
            "emails": emails
        }
        print(json.dumps(result, ensure_ascii=False))

    except imaplib.IMAP4.error as e:
        result = {"status": "error", "message": f"IMAP错误: {str(e)}"}
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        result = {"status": "error", "message": f"连接失败: {str(e)}"}
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
