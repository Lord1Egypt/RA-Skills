#!/usr/bin/env python3
"""发送/回复QQ邮件"""
import argparse
import json
import os
import smtplib
import ssl
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate


SMTP_HOST = 'smtp.qq.com'
SMTP_PORT = 587
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


def get_credentials():
    email_addr = os.environ.get(ENV_EMAIL) or os.environ.get(LEGACY_ENV_EMAIL, '')
    auth_code = os.environ.get(ENV_AUTH_CODE) or os.environ.get(LEGACY_ENV_AUTH_CODE, '')
    if not email_addr or not auth_code:
        return None, None
    return email_addr, auth_code


def decode_str(s):
    """解码邮件头部字段"""
    if not s:
        return ''
    parts = decode_header(s)
    result = []
    for data, charset in parts:
        if isinstance(data, bytes):
            result.append(data.decode(charset or 'utf-8', errors='replace'))
        else:
            result.append(data)
    return ''.join(result)


def read_file_content(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def get_original_email(email_addr, auth_code, mail_id, folder):
    """通过IMAP获取原始邮件，提取回复所需信息"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'
        mail.select(quote_folder(folder), readonly=True)

        status, data = mail.fetch(str(mail_id), '(BODY.PEEK[])')
        mail.logout()

        if status != 'OK' or not data or not data[0]:
            return None

        raw = None
        for item in data:
            if isinstance(item, tuple):
                raw = item[1]
                break
        if not raw:
            return None

        msg = email.message_from_bytes(raw)

        message_id = msg.get('Message-ID', '')
        references = msg.get('References', '')
        subject = decode_str(msg.get('Subject', ''))
        from_addr = decode_str(msg.get('From', ''))
        reply_to_addr = decode_str(msg.get('Reply-To', ''))

        # 提取纯文本正文用于引用
        body_text = ''
        if msg.is_multipart():
            for part in msg.walk():
                ct = part.get_content_type()
                if ct == 'text/plain':
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or 'utf-8'
                    body_text = payload.decode(charset, errors='replace')
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or 'utf-8'
                body_text = payload.decode(charset, errors='replace')

        # 截取正文前500字符作为引用
        if len(body_text) > 500:
            body_text = body_text[:500] + '...'

        return {
            'message_id': message_id,
            'references': references,
            'subject': subject,
            'from': from_addr,
            'reply_to': reply_to_addr,
            'body_snippet': body_text
        }

    except Exception as e:
        return None


def send_email(email_addr, auth_code, to, subject, body, cc=None, bcc=None,
               html=False, attachments=None, in_reply_to=None, references=None):
    """发送邮件"""
    try:
        msg = MIMEMultipart()
        msg['From'] = email_addr
        msg['To'] = to
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)

        if cc:
            msg['Cc'] = cc

        # 回复邮件头
        if in_reply_to:
            msg['In-Reply-To'] = in_reply_to
        if references:
            msg['References'] = references

        content_type = 'html' if html else 'plain'
        msg.attach(MIMEText(body, content_type, 'utf-8'))

        if attachments:
            for filepath in attachments:
                filepath = filepath.strip()
                try:
                    with open(filepath, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        filename = os.path.basename(filepath)
                        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                        msg.attach(part)
                except Exception as e:
                    return {'status': 'error', 'message': f'无法添加附件 {filepath}: {str(e)}'}

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(email_addr, auth_code)

            recipients = [addr.strip() for addr in to.split(',')]
            if cc:
                recipients.extend([addr.strip() for addr in cc.split(',')])
            if bcc:
                recipients.extend([addr.strip() for addr in bcc.split(',')])
            server.sendmail(email_addr, recipients, msg.as_string())

        return {
            'status': 'success',
            'message': '邮件发送成功',
            'to': to,
            'subject': subject,
            'html': html,
            'is_reply': bool(in_reply_to)
        }

    except smtplib.SMTPAuthenticationError:
        return {'status': 'error', 'message': 'SMTP认证失败，请检查授权码是否正确'}
    except smtplib.SMTPException as e:
        return {'status': 'error', 'message': f'SMTP错误: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'错误: {str(e)}'}


def test_smtp(email_addr, auth_code):
    """测试SMTP连接，向自己发送测试邮件"""
    try:
        subject = f'SMTP连接测试 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        body = '这是一封SMTP连接测试邮件，确认您的邮箱配置正确。'
        result = send_email(email_addr, auth_code, to=email_addr, subject=subject, body=body)
        if result['status'] == 'success':
            result['message'] = 'SMTP连接测试成功，测试邮件已发送至自己的邮箱'
        return result
    except Exception as e:
        return {'status': 'error', 'message': f'SMTP连接测试失败: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description='发送/回复QQ邮件')
    # 测试模式
    parser.add_argument('--test', action='store_true', help='测试SMTP连接，向自己发送测试邮件')
    # 收件人（回复模式下可省略，自动填充原发件人）
    parser.add_argument('--to', help='收件人邮箱(多个逗号分隔)')
    # 回复模式
    parser.add_argument('--reply-to-id', help='回复指定邮件：原始邮件编号')
    parser.add_argument('--reply-folder', required=False, help='原始邮件所在文件夹(回复模式必填)')
    parser.add_argument('--reply-quote', action='store_true', help='在正文中引用原邮件内容')
    # 主题（--subject 或 --subject-file 二选一；回复模式下可省略，自动加Re:前缀）
    parser.add_argument('--subject', help='邮件主题')
    parser.add_argument('--subject-file', help='从文件读取邮件主题')
    # 正文（--body 或 --body-file 二选一）
    parser.add_argument('--body', help='邮件正文(纯文本)')
    parser.add_argument('--body-file', help='从文件读取邮件正文')
    # 格式
    parser.add_argument('--html', action='store_true', help='以HTML格式发送正文')
    # 抄送/密送
    parser.add_argument('--cc', help='抄送(多个逗号分隔)')
    parser.add_argument('--bcc', help='密送(多个逗号分隔)')
    # 附件
    parser.add_argument('--attachments', help='附件路径(多个逗号分隔)')

    args = parser.parse_args()

    email_addr, auth_code = get_credentials()
    if not email_addr or not auth_code:
        print(json.dumps({'status': 'error', 'message': '缺少凭证信息，请先配置QQ邮箱地址和授权码'}, ensure_ascii=False))
        return

    # 测试模式
    if args.test:
        result = test_smtp(email_addr, auth_code)
        print(json.dumps(result, ensure_ascii=False))
        return

    # ---- 回复模式 ----
    in_reply_to = None
    references = None
    to = args.to
    subject = args.subject

    if args.reply_to_id:
        if not args.reply_folder:
            print(json.dumps({'status': 'error', 'message': '回复邮件时 --reply-folder 为必填参数'}, ensure_ascii=False))
            return
        orig = get_original_email(email_addr, auth_code, args.reply_to_id, args.reply_folder)
        if not orig:
            print(json.dumps({'status': 'error', 'message': f'无法获取原始邮件(编号:{args.reply_to_id}, 文件夹:{args.reply_folder})'}, ensure_ascii=False))
            return

        # 自动填充收件人：优先 Reply-To，其次 From
        if not to:
            to = orig['reply_to'] or orig['from']

        # 自动填充主题：加 Re: 前缀
        if not subject and not args.subject_file:
            orig_subject = orig['subject']
            if not orig_subject.startswith('Re:'):
                subject = f'Re: {orig_subject}'
            else:
                subject = orig_subject

        # 设置回复邮件头
        in_reply_to = orig['message_id']
        if orig['references']:
            references = f"{orig['references']} {orig['message_id']}"
        else:
            references = orig['message_id']

        # 引用原邮件正文
        if args.reply_quote and orig['body_snippet']:
            body = args.body or ''
            if args.body_file:
                file_content = read_file_content(args.body_file)
                if file_content is None:
                    print(json.dumps({'status': 'error', 'message': f'无法读取正文文件: {args.body_file}'}, ensure_ascii=False))
                    return
                body = file_content

            quote_header = f"\n\n--- 原始邮件 ---\n发件人: {orig['from']}\n主题: {orig['subject']}\n\n"
            body = body + quote_header + orig['body_snippet']
        else:
            body = args.body
            if args.body_file:
                file_content = read_file_content(args.body_file)
                if file_content is None:
                    print(json.dumps({'status': 'error', 'message': f'无法读取正文文件: {args.body_file}'}, ensure_ascii=False))
                    return
                body = file_content
    else:
        # ---- 新邮件模式 ----
        if not to:
            parser.error('发送邮件需要 --to 参数（或使用 --reply-to-id 回复邮件）')

        body = args.body
        if args.body_file:
            file_content = read_file_content(args.body_file)
            if file_content is None:
                print(json.dumps({'status': 'error', 'message': f'无法读取正文文件: {args.body_file}'}, ensure_ascii=False))
                return
            body = file_content

    # 解析主题文件
    if args.subject_file:
        file_content = read_file_content(args.subject_file)
        if file_content is None:
            print(json.dumps({'status': 'error', 'message': f'无法读取主题文件: {args.subject_file}'}, ensure_ascii=False))
            return
        subject = file_content.strip()

    if not subject:
        parser.error('邮件主题不能为空，请通过 --subject 或 --subject-file 提供')

    if not body:
        parser.error('邮件正文不能为空，请通过 --body 或 --body-file 提供')

    attachments = [p.strip() for p in args.attachments.split(',')] if args.attachments else None

    result = send_email(
        email_addr, auth_code,
        to=to,
        subject=subject,
        body=body,
        cc=args.cc,
        bcc=args.bcc,
        html=args.html,
        attachments=attachments,
        in_reply_to=in_reply_to,
        references=references
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
