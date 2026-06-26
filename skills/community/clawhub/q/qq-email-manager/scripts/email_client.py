#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""企业邮箱管理客户端 - 腾讯企业邮箱 IMAP/SMTP"""

import argparse
import imaplib
import smtplib
import email
import email.utils
import email.header
import email.mime.text
import email.mime.multipart
import email.mime.base
import email.mime.application
import json
import os
import sys
import ssl
import re
import datetime
import mimetypes
from email.header import decode_header as _decode_header

# ── Config ──────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, '..', 'config', 'email-config.json')

def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        error_exit(f"配置文件不存在: {os.path.abspath(CONFIG_PATH)}")
    except json.JSONDecodeError as e:
        error_exit(f"配置文件格式错误: {e}")

def error_exit(msg):
    print(json.dumps({"error": msg}, ensure_ascii=False))
    sys.exit(1)

def ok_result(data):
    print(json.dumps(data, ensure_ascii=False, default=str))
    sys.exit(0)

# ── Helpers ─────────────────────────────────────────────────────────────────

def decode_header_value(value):
    """解码邮件头（支持中文编码）"""
    if value is None:
        return ""
    parts = _decode_header(value)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            for enc in [charset, 'utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin-1']:
                if enc:
                    try:
                        result.append(part.decode(enc))
                        break
                    except (UnicodeDecodeError, LookupError):
                        continue
            else:
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(str(part))
    return ''.join(result)

def decode_payload(part):
    """解码邮件正文 payload"""
    payload = part.get_payload(decode=True)
    if payload is None:
        return ""
    charset = part.get_content_charset()
    for enc in [charset, 'utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin-1']:
        if enc:
            try:
                return payload.decode(enc)
            except (UnicodeDecodeError, LookupError):
                continue
    return payload.decode('utf-8', errors='replace')

def strip_html(html):
    """简单去除 HTML 标签"""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def get_body(msg):
    """提取邮件正文，优先 text/plain"""
    body_text = ""
    body_html = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))
            if "attachment" in cd:
                continue
            if ct == "text/plain" and not body_text:
                body_text = decode_payload(part)
            elif ct == "text/html" and not body_html:
                body_html = decode_payload(part)
    else:
        ct = msg.get_content_type()
        if ct == "text/plain":
            body_text = decode_payload(msg)
        elif ct == "text/html":
            body_html = decode_payload(msg)
    return body_text, body_html

def get_attachments(msg):
    """提取附件列表"""
    attachments = []
    if not msg.is_multipart():
        return attachments
    for part in msg.walk():
        cd = str(part.get("Content-Disposition", ""))
        if "attachment" in cd or "inline" in cd:
            filename = part.get_filename()
            if filename:
                filename = decode_header_value(filename)
                size = len(part.get_payload(decode=True) or b"")
                attachments.append({"filename": filename, "size": size, "content_type": part.get_content_type()})
    return attachments

def has_attachment(msg):
    """检查是否有附件"""
    if not msg.is_multipart():
        return False
    for part in msg.walk():
        cd = str(part.get("Content-Disposition", ""))
        if "attachment" in cd:
            return True
    return False

def parse_date(date_str):
    """解析邮件日期"""
    if not date_str:
        return ""
    try:
        parsed = email.utils.parsedate_to_datetime(date_str)
        return parsed.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return date_str

def connect_imap(config):
    """连接 IMAP"""
    try:
        ctx = ssl.create_default_context()
        imap = imaplib.IMAP4_SSL(
            config['imap']['host'],
            config['imap']['port'],
            ssl_context=ctx
        )
        imap.login(config['account']['username'], config['account']['password'])
        return imap
    except imaplib.IMAP4.error as e:
        error_exit(f"IMAP 认证失败: {e}")
    except Exception as e:
        error_exit(f"IMAP 连接失败: {e}")

def connect_smtp(config):
    """连接 SMTP"""
    try:
        ctx = ssl.create_default_context()
        smtp = smtplib.SMTP_SSL(
            config['smtp']['host'],
            config['smtp']['port'],
            context=ctx
        )
        smtp.login(config['account']['username'], config['account']['password'])
        return smtp
    except smtplib.SMTPAuthenticationError as e:
        error_exit(f"SMTP 认证失败: {e}")
    except Exception as e:
        error_exit(f"SMTP 连接失败: {e}")

def imap_utf7_decode(s):
    """解码 IMAP 修改版 UTF-7 编码"""
    result = []
    i = 0
    while i < len(s):
        if s[i] == '&':
            j = s.index('-', i + 1)
            if j == i + 1:
                result.append('&')
            else:
                encoded = s[i+1:j]
                # IMAP modified UTF-7: & -> +, , -> /
                b64 = '+' + encoded.replace(',', '/') + '-'
                try:
                    result.append(b64.encode('ascii').decode('utf-7'))
                except (UnicodeDecodeError, UnicodeEncodeError):
                    result.append(s[i:j+1])
            i = j + 1
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)

def decode_folder_name(folder_bytes):
    """解码 IMAP 文件夹名（支持修改版 UTF-7）"""
    if isinstance(folder_bytes, bytes):
        folder_str = folder_bytes.decode('utf-8', errors='replace')
    else:
        folder_str = folder_bytes
    # Extract folder name from IMAP response like '(\\HasNoChildren) "/" "INBOX"'
    match = re.search(r'"([^"]*)"$', folder_str)
    if match:
        name = match.group(1)
    else:
        parts = folder_str.split(' ')
        name = parts[-1].strip('"')
    return imap_utf7_decode(name)

# ── Commands ────────────────────────────────────────────────────────────────

def cmd_list(args):
    config = load_config()
    imap = connect_imap(config)
    try:
        folder = args.folder or "INBOX"
        status, _ = imap.select(folder, readonly=True)
        if status != 'OK':
            error_exit(f"无法打开文件夹: {folder}")

        criteria = []
        if args.unread:
            criteria.append('UNSEEN')
        if args.days:
            since_date = (datetime.datetime.now() - datetime.timedelta(days=args.days)).strftime("%d-%b-%Y")
            criteria.append(f'SINCE {since_date}')
        
        search_str = ' '.join(criteria) if criteria else 'ALL'
        status, data = imap.search(None, search_str)
        if status != 'OK':
            error_exit("搜索邮件失败")

        ids = data[0].split()
        if not ids:
            ok_result({"count": 0, "emails": []})

        # 取最新的 limit 封
        limit = args.limit or 20
        ids = ids[-limit:]
        ids.reverse()

        emails = []
        for mid in ids:
            status, msg_data = imap.fetch(mid, '(FLAGS RFC822.HEADER)')
            if status != 'OK':
                continue
            
            flags = ""
            raw_header = b""
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    if b'FLAGS' in response_part[0]:
                        flags = response_part[0].decode('utf-8', errors='replace')
                    raw_header = response_part[1]
                elif isinstance(response_part, bytes):
                    if b'FLAGS' in response_part:
                        flags = response_part.decode('utf-8', errors='replace')

            msg = email.message_from_bytes(raw_header)
            is_read = '\\Seen' in flags
            
            emails.append({
                "id": mid.decode(),
                "subject": decode_header_value(msg.get("Subject", "")),
                "from": decode_header_value(msg.get("From", "")),
                "date": parse_date(msg.get("Date", "")),
                "is_read": is_read,
                "has_attachment": "attachment" in msg.get("Content-Type", "").lower() or 
                                  bool(msg.get("Content-Disposition", ""))
            })

        ok_result({"count": len(emails), "emails": emails})
    finally:
        imap.logout()

def cmd_read(args):
    if not args.id:
        error_exit("请指定邮件ID: --id <message_id>")
    config = load_config()
    imap = connect_imap(config)
    try:
        imap.select("INBOX", readonly=True)
        status, msg_data = imap.fetch(args.id.encode(), '(RFC822)')
        if status != 'OK':
            error_exit(f"无法获取邮件 {args.id}")

        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        body_text, body_html = get_body(msg)
        attachments = get_attachments(msg)

        if not body_text and body_html:
            body_text = strip_html(body_html)

        result = {
            "subject": decode_header_value(msg.get("Subject", "")),
            "from": decode_header_value(msg.get("From", "")),
            "to": decode_header_value(msg.get("To", "")),
            "cc": decode_header_value(msg.get("Cc", "")),
            "date": parse_date(msg.get("Date", "")),
            "body_text": body_text,
            "body_html": body_html[:2000] if body_html else "",
            "attachments": attachments
        }
        ok_result(result)
    finally:
        imap.logout()

def cmd_send(args):
    if not args.to:
        error_exit("请指定收件人: --to")
    if not args.subject:
        error_exit("请指定主题: --subject")
    if not args.body:
        error_exit("请指定正文: --body")

    config = load_config()
    sender = config['account']['username']

    msg = email.mime.multipart.MIMEMultipart()
    msg['From'] = sender
    msg['To'] = args.to
    if args.cc:
        msg['Cc'] = args.cc
    msg['Subject'] = args.subject
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid(domain=sender.split('@')[1])

    if args.html:
        msg.attach(email.mime.text.MIMEText(args.body, 'html', 'utf-8'))
    else:
        msg.attach(email.mime.text.MIMEText(args.body, 'plain', 'utf-8'))

    if args.attachment:
        for filepath in args.attachment.split(','):
            filepath = filepath.strip()
            if not os.path.isfile(filepath):
                error_exit(f"附件不存在: {filepath}")
            filename = os.path.basename(filepath)
            ctype, _ = mimetypes.guess_type(filepath)
            if ctype is None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(filepath, 'rb') as f:
                att = email.mime.application.MIMEApplication(f.read(), Name=filename)
            att['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(att)

    recipients = [a.strip() for a in args.to.split(',')]
    if args.cc:
        recipients += [a.strip() for a in args.cc.split(',')]

    smtp = connect_smtp(config)
    try:
        smtp.sendmail(sender, recipients, msg.as_string())
        ok_result({"success": True, "message": f"邮件已发送至 {args.to}"})
    except Exception as e:
        error_exit(f"发送失败: {e}")
    finally:
        smtp.quit()

def cmd_reply(args):
    if not args.id:
        error_exit("请指定原邮件ID: --id")
    if not args.body:
        error_exit("请指定回复内容: --body")

    config = load_config()
    sender = config['account']['username']
    imap = connect_imap(config)
    try:
        imap.select("INBOX", readonly=True)
        status, msg_data = imap.fetch(args.id.encode(), '(RFC822)')
        if status != 'OK':
            error_exit(f"无法获取原邮件 {args.id}")
        
        orig = email.message_from_bytes(msg_data[0][1])
        orig_from = decode_header_value(orig.get("From", ""))
        orig_subject = decode_header_value(orig.get("Subject", ""))
        orig_msg_id = orig.get("Message-ID", "")
        orig_to = decode_header_value(orig.get("To", ""))
        orig_cc = decode_header_value(orig.get("Cc", ""))
    finally:
        imap.logout()

    subject = orig_subject if orig_subject.lower().startswith("re:") else f"Re: {orig_subject}"

    reply = email.mime.multipart.MIMEMultipart()
    reply['From'] = sender
    reply['Subject'] = subject
    reply['Date'] = email.utils.formatdate(localtime=True)
    reply['Message-ID'] = email.utils.make_msgid(domain=sender.split('@')[1])
    if orig_msg_id:
        reply['In-Reply-To'] = orig_msg_id
        reply['References'] = orig_msg_id

    recipients = [orig_from]
    if args.all:
        # 回复全部：加上原 To 和 Cc（排除自己）
        for addr_str in [orig_to, orig_cc]:
            if addr_str:
                for a in addr_str.split(','):
                    a = a.strip()
                    if a and sender not in a:
                        recipients.append(a)
    
    reply['To'] = ', '.join(recipients)
    reply.attach(email.mime.text.MIMEText(args.body, 'plain', 'utf-8'))

    smtp = connect_smtp(config)
    try:
        smtp.sendmail(sender, [r.strip() for r in recipients], reply.as_string())
        ok_result({"success": True, "message": f"已回复邮件: {subject}"})
    except Exception as e:
        error_exit(f"回复失败: {e}")
    finally:
        smtp.quit()

def cmd_forward(args):
    if not args.id:
        error_exit("请指定原邮件ID: --id")
    if not args.to:
        error_exit("请指定转发目标: --to")

    config = load_config()
    sender = config['account']['username']
    imap = connect_imap(config)
    try:
        imap.select("INBOX", readonly=True)
        status, msg_data = imap.fetch(args.id.encode(), '(RFC822)')
        if status != 'OK':
            error_exit(f"无法获取原邮件 {args.id}")
        
        orig = email.message_from_bytes(msg_data[0][1])
        orig_subject = decode_header_value(orig.get("Subject", ""))
        body_text, body_html = get_body(orig)
        if not body_text and body_html:
            body_text = strip_html(body_html)
        orig_attachments = []
        if orig.is_multipart():
            for part in orig.walk():
                cd = str(part.get("Content-Disposition", ""))
                if "attachment" in cd:
                    orig_attachments.append(part)
    finally:
        imap.logout()

    subject = orig_subject if orig_subject.lower().startswith("fwd:") else f"Fwd: {orig_subject}"
    
    fwd = email.mime.multipart.MIMEMultipart()
    fwd['From'] = sender
    fwd['To'] = args.to
    fwd['Subject'] = subject
    fwd['Date'] = email.utils.formatdate(localtime=True)
    fwd['Message-ID'] = email.utils.make_msgid(domain=sender.split('@')[1])

    fwd_body = ""
    if args.body:
        fwd_body = args.body + "\n\n"
    fwd_body += f"---------- 转发邮件 ----------\n{body_text}"
    fwd.attach(email.mime.text.MIMEText(fwd_body, 'plain', 'utf-8'))

    for att_part in orig_attachments:
        fwd.attach(att_part)

    recipients = [a.strip() for a in args.to.split(',')]
    smtp = connect_smtp(config)
    try:
        smtp.sendmail(sender, recipients, fwd.as_string())
        ok_result({"success": True, "message": f"已转发邮件至 {args.to}"})
    except Exception as e:
        error_exit(f"转发失败: {e}")
    finally:
        smtp.quit()

def cmd_mark(args):
    if not args.id:
        error_exit("请指定邮件ID: --id")

    config = load_config()
    imap = connect_imap(config)
    try:
        imap.select("INBOX")
        actions = []
        if args.read:
            imap.store(args.id.encode(), '+FLAGS', '\\Seen')
            actions.append("已读")
        if args.unread:
            imap.store(args.id.encode(), '-FLAGS', '\\Seen')
            actions.append("未读")
        if args.star:
            imap.store(args.id.encode(), '+FLAGS', '\\Flagged')
            actions.append("星标")
        if args.unstar:
            imap.store(args.id.encode(), '-FLAGS', '\\Flagged')
            actions.append("取消星标")
        
        if not actions:
            error_exit("请指定标记操作: --read/--unread/--star/--unstar")
        
        ok_result({"success": True, "message": f"邮件 {args.id} 已标记为: {', '.join(actions)}"})
    finally:
        imap.logout()

def cmd_search(args):
    config = load_config()
    imap = connect_imap(config)
    try:
        imap.select("INBOX", readonly=True)
        
        criteria = []
        if args.query:
            criteria.append(f'SUBJECT "{args.query}"')
        if getattr(args, 'from_addr', None):
            criteria.append(f'FROM "{args.from_addr}"')
        if args.since:
            # Convert YYYY-MM-DD to DD-Mon-YYYY
            d = datetime.datetime.strptime(args.since, "%Y-%m-%d")
            criteria.append(f'SINCE {d.strftime("%d-%b-%Y")}')
        if args.before:
            d = datetime.datetime.strptime(args.before, "%Y-%m-%d")
            criteria.append(f'BEFORE {d.strftime("%d-%b-%Y")}')
        
        if not criteria:
            error_exit("请指定搜索条件: --query/--from/--since/--before")

        search_str = ' '.join(criteria)
        status, data = imap.search(None, search_str)
        if status != 'OK':
            error_exit("搜索失败")

        ids = data[0].split()
        limit = args.limit or 20
        ids = ids[-limit:]
        ids.reverse()

        emails = []
        for mid in ids:
            status, msg_data = imap.fetch(mid, '(FLAGS RFC822.HEADER)')
            if status != 'OK':
                continue
            flags = ""
            raw_header = b""
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    if b'FLAGS' in response_part[0]:
                        flags = response_part[0].decode('utf-8', errors='replace')
                    raw_header = response_part[1]
            
            msg = email.message_from_bytes(raw_header)
            is_read = '\\Seen' in flags
            emails.append({
                "id": mid.decode(),
                "subject": decode_header_value(msg.get("Subject", "")),
                "from": decode_header_value(msg.get("From", "")),
                "date": parse_date(msg.get("Date", "")),
                "is_read": is_read
            })

        ok_result({"count": len(emails), "query": search_str, "emails": emails})
    finally:
        imap.logout()

def cmd_folders(args):
    config = load_config()
    imap = connect_imap(config)
    try:
        status, folders = imap.list()
        if status != 'OK':
            error_exit("获取文件夹列表失败")
        
        folder_list = []
        for f in folders:
            name = decode_folder_name(f)
            folder_list.append(name)
        
        ok_result({"folders": folder_list})
    finally:
        imap.logout()

def get_raw_folder_name(folder_bytes):
    """从 IMAP LIST 响应中提取原始文件夹名（不解码 UTF-7）"""
    if isinstance(folder_bytes, bytes):
        folder_str = folder_bytes.decode('utf-8', errors='replace')
    else:
        folder_str = folder_bytes
    match = re.search(r'"([^"]*)"$', folder_str)
    if match:
        return match.group(1)
    parts = folder_str.split(' ')
    return parts[-1].strip('"')

def cmd_stats(args):
    config = load_config()
    imap = connect_imap(config)
    try:
        status, folders = imap.list()
        if status != 'OK':
            error_exit("获取文件夹列表失败")

        stats = {"folders": {}, "total": 0, "unread": 0}
        
        for f in folders:
            display_name = decode_folder_name(f)
            raw_name = get_raw_folder_name(f)
            try:
                st, count_data = imap.select('"' + raw_name + '"', readonly=True)
                if st == 'OK':
                    total = int(count_data[0])
                    st2, unseen_data = imap.search(None, 'UNSEEN')
                    unread = len(unseen_data[0].split()) if st2 == 'OK' and unseen_data[0] else 0
                    stats["folders"][display_name] = {"total": total, "unread": unread}
                    stats["total"] += total
                    stats["unread"] += unread
                else:
                    stats["folders"][display_name] = {"total": 0, "unread": 0, "error": "无法访问"}
            except Exception:
                stats["folders"][display_name] = {"total": 0, "unread": 0, "error": "无法访问"}

        ok_result(stats)
    finally:
        imap.logout()

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='企业邮箱管理客户端')
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # list
    p_list = subparsers.add_parser('list', help='查看邮件列表')
    p_list.add_argument('--folder', default='INBOX', help='文件夹（默认 INBOX）')
    p_list.add_argument('--unread', action='store_true', help='只看未读')
    p_list.add_argument('--limit', type=int, default=20, help='限制数量')
    p_list.add_argument('--days', type=int, help='最近N天')

    # read
    p_read = subparsers.add_parser('read', help='读取邮件正文')
    p_read.add_argument('--id', required=True, help='邮件ID')

    # send
    p_send = subparsers.add_parser('send', help='发送邮件')
    p_send.add_argument('--to', required=True, help='收件人（逗号分隔）')
    p_send.add_argument('--cc', help='抄送')
    p_send.add_argument('--subject', required=True, help='主题')
    p_send.add_argument('--body', required=True, help='正文')
    p_send.add_argument('--html', action='store_true', help='HTML格式')
    p_send.add_argument('--attachment', help='附件路径（逗号分隔）')

    # reply
    p_reply = subparsers.add_parser('reply', help='回复邮件')
    p_reply.add_argument('--id', required=True, help='原邮件ID')
    p_reply.add_argument('--body', required=True, help='回复内容')
    p_reply.add_argument('--all', action='store_true', help='回复全部')

    # forward
    p_fwd = subparsers.add_parser('forward', help='转发邮件')
    p_fwd.add_argument('--id', required=True, help='原邮件ID')
    p_fwd.add_argument('--to', required=True, help='转发目标')
    p_fwd.add_argument('--body', help='转发说明')

    # mark
    p_mark = subparsers.add_parser('mark', help='标记邮件')
    p_mark.add_argument('--id', required=True, help='邮件ID')
    p_mark.add_argument('--read', action='store_true', help='标记已读')
    p_mark.add_argument('--unread', action='store_true', help='标记未读')
    p_mark.add_argument('--star', action='store_true', help='星标')
    p_mark.add_argument('--unstar', action='store_true', help='取消星标')

    # search
    p_search = subparsers.add_parser('search', help='搜索邮件')
    p_search.add_argument('--query', help='搜索关键词')
    p_search.add_argument('--from', dest='from_addr', help='发件人')
    p_search.add_argument('--since', help='起始日期 YYYY-MM-DD')
    p_search.add_argument('--before', help='截止日期 YYYY-MM-DD')
    p_search.add_argument('--limit', type=int, default=20, help='限制数量')

    # folders
    subparsers.add_parser('folders', help='列出文件夹')

    # stats
    subparsers.add_parser('stats', help='邮箱统计')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        'list': cmd_list,
        'read': cmd_read,
        'send': cmd_send,
        'reply': cmd_reply,
        'forward': cmd_forward,
        'mark': cmd_mark,
        'search': cmd_search,
        'folders': cmd_folders,
        'stats': cmd_stats,
    }
    commands[args.command](args)

if __name__ == '__main__':
    main()
