#!/usr/bin/env python3
"""获取QQ邮箱邮件详情，支持单封或多封"""
import argparse
import json
import os
import sys
import imaplib
import ssl
from email.header import decode_header
from email.parser import BytesParser


IMAP_HOST = 'imap.qq.com'
IMAP_PORT = 993

SKILL_ID = '7637538402895773731'
CRED_NAME = 'qq_email'
ENV_EMAIL = 'QQ_EMAIL'
ENV_AUTH_CODE = 'QQ_EMAIL_AUTH_CODE'
LEGACY_ENV_EMAIL = f'COZE_{CRED_NAME}_QQ_EMAIL_{SKILL_ID}'
LEGACY_ENV_AUTH_CODE = f'COZE_{CRED_NAME}_QQ_EMAIL_AUTH_CODE_{SKILL_ID}'


def get_credentials():
    email_addr = os.environ.get(ENV_EMAIL) or os.environ.get(LEGACY_ENV_EMAIL, '')
    auth_code = os.environ.get(ENV_AUTH_CODE) or os.environ.get(LEGACY_ENV_AUTH_CODE, '')
    if not email_addr or not auth_code:
        return None, None
    return email_addr, auth_code


def quote_folder(name):
    """为含空格的文件夹名包裹双引号"""
    if not name:
        return name
    if name.startswith('"') and name.endswith('"'):
        return name
    if ' ' in name:
        return f'"{name}"'
    return name


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


def extract_body_and_attachments(msg):
    """提取正文和附件列表"""
    body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            charset = part.get_content_charset() or 'utf-8'

            filename = part.get_filename()
            if filename:
                attachments.append({'name': decode_str(filename), 'type': ct})
                continue

            if ct == 'text/plain' and not body:
                try:
                    payload = part.get_payload(decode=True)
                    body = payload.decode(charset, errors='replace')
                except Exception as e:
                    print(f"[extract_body] text/plain decode error: {e}", file=sys.stderr)
            elif ct == 'text/html' and not body:
                try:
                    payload = part.get_payload(decode=True)
                    body = payload.decode(charset, errors='replace')
                except Exception as e:
                    print(f"[extract_body] text/html decode error: {e}", file=sys.stderr)
    else:
        charset = msg.get_content_charset() or 'utf-8'
        try:
            payload = msg.get_payload(decode=True)
            body = payload.decode(charset, errors='replace')
        except Exception as e:
            print(f"[extract_body] single part decode error: {e}", file=sys.stderr)

    return body, attachments


def fetch_single_email(mail, mid_str, parser):
    """获取单封邮件详情"""
    status, msg_data = mail.fetch(mid_str.encode(), '(BODY.PEEK[])')
    if status != 'OK' or not msg_data or not msg_data[0]:
        return None

    raw = None
    for item in msg_data:
        if isinstance(item, tuple):
            raw = item[1]
            break
    if not raw:
        return None

    msg = parser.parsebytes(raw)

    subject = decode_str(msg.get('Subject', '')) or '(无主题)'
    sender = decode_str(msg.get('From', ''))
    to = decode_str(msg.get('To', ''))
    cc = decode_str(msg.get('Cc', ''))
    date = msg.get('Date', '')

    body, attachments = extract_body_and_attachments(msg)

    return {
        'mail_id': mid_str,
        'folder': None,  # 由调用方填充
        'subject': subject,
        'sender': sender,
        'to': to,
        'cc': cc,
        'date': date,
        'body': body,
        'attachments': attachments
    }


def get_emails(email_addr, auth_code, mail_ids, folder='INBOX'):
    """获取一封或多封邮件详情"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ssl.create_default_context())
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'

        status, _ = mail.select(quote_folder(folder), readonly=True)
        if status != 'OK':
            return {'status': 'error', 'message': f'无法访问文件夹: {folder}'}

        parser = BytesParser()
        emails = []
        failed = []

        for mid in mail_ids:
            try:
                detail = fetch_single_email(mail, mid, parser)
                if detail:
                    detail['folder'] = folder
                    emails.append(detail)
                else:
                    failed.append(mid)
            except Exception:
                failed.append(mid)

        mail.logout()

        result = {
            'status': 'success',
            'folder': folder,
            'total': len(mail_ids),
            'fetched': len(emails),
            'failed': failed,
            'emails': emails
        }

        if failed and not emails:
            result['status'] = 'error'
            result['message'] = f'所有邮件获取失败: {", ".join(failed)}'
        elif failed:
            result['status'] = 'partial'
            result['message'] = f'{len(emails)} 封获取成功，{len(failed)} 封失败'

        return result

    except imaplib.IMAP4.error as e:
        return {'status': 'error', 'message': f'IMAP错误: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'错误: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description='获取QQ邮箱邮件详情')
    parser.add_argument('--mail_ids', required=True, help='邮件编号(多个逗号分隔，也可传单个)')
    parser.add_argument('--folder', required=True, help='邮箱文件夹（必填）')
    args = parser.parse_args()

    email_addr, auth_code = get_credentials()
    if not email_addr or not auth_code:
        print(json.dumps({'status': 'error', 'message': '缺少凭证信息，请先配置QQ邮箱地址和授权码'}, ensure_ascii=False))
        return

    mail_ids = [mid.strip() for mid in args.mail_ids.split(',') if mid.strip()]

    if not mail_ids:
        print(json.dumps({'status': 'error', 'message': '邮件编号不能为空'}, ensure_ascii=False))
        return

    result = get_emails(email_addr, auth_code, mail_ids, args.folder)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
