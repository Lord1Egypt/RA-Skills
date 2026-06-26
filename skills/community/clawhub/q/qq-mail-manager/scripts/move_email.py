#!/usr/bin/env python3
"""移动QQ邮箱邮件（含删除=移动到垃圾箱）"""
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


def decode_str(s):
    """解码邮件头部编码字符串"""
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


def quote_folder(name):
    """为含空格的文件夹名包裹双引号"""
    if not name:
        return name
    # 如果已经有引号包裹则不再处理
    if name.startswith('"') and name.endswith('"'):
        return name
    if ' ' in name:
        return f'"{name}"'
    return name


def decode_imap_utf7(s):
    """将 IMAP modified UTF-7 编码的文件夹名解码为可读字符串"""
    try:
        import base64
        result = []
        i = 0
        while i < len(s):
            if s[i] == '&':
                j = s.find('-', i + 1)
                if j == -1:
                    result.append(s[i:])
                    break
                if j == i + 1:
                    result.append('&')
                else:
                    b64 = s[i + 1:j]
                    b64 += '=' * (4 - len(b64) % 4) if len(b64) % 4 else ''
                    decoded = base64.b64decode(b64)
                    result.append(decoded.decode('utf-16-be'))
                i = j + 1
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)
    except Exception:
        return s


def find_trash_folder(mail):
    """查找垃圾箱/已删除文件夹名（保留IMAP所需的双引号包裹）"""
    status, folders = mail.list()
    if status != 'OK':
        return None
    for folder_info in folders:
        folder_str = folder_info.decode() if isinstance(folder_info, bytes) else str(folder_info)
        # 标准解析：按双引号分割，最后一个非空段即为文件夹名
        parts = folder_str.split('"')
        for i in range(len(parts) - 1, -1, -1):
            p = parts[i].strip()
            if p and p not in ('/', '.', '\\'):
                decoded = decode_imap_utf7(p)
                if 'Trash' in decoded or '垃圾' in decoded or 'Deleted' in decoded or '已删除' in decoded:
                    if ' ' in p:
                        return f'"{p}"'
                    return p
    return None


def preview_emails(mail, mail_ids, folder_name):
    """预览邮件信息（标题、发件人、收件时间）"""
    parser = BytesParser()
    previews = []
    not_found = []

    for mid in mail_ids:
        try:
            status, msg_data = mail.fetch(mid.encode(), '(BODY.PEEK[])')
            if status != 'OK' or not msg_data or not msg_data[0]:
                not_found.append(mid)
                continue
            raw = None
            for item in msg_data:
                if isinstance(item, tuple):
                    raw = item[1]
                    break
            if not raw:
                not_found.append(mid)
                continue
            msg = parser.parsebytes(raw)
            previews.append({
                'mail_id': mid,
                'folder': folder_name,
                'subject': decode_str(msg.get('Subject', '')) or '(无主题)',
                'sender': decode_str(msg.get('From', '')),
                'date': msg.get('Date', '')
            })
        except Exception as e:
            print(f"[preview_emails] mail_id={mid} error: {e}", file=sys.stderr)
            not_found.append(mid)

    return previews, not_found


def move_emails(email_addr, auth_code, mail_ids, src_folder='INBOX', dst_folder=None, delete=False, confirm=False):
    """移动或删除邮件"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ssl.create_default_context())
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'

        # --delete 模式：先查找垃圾箱（需在select前执行list，无需select）
        if delete:
            dst_folder = find_trash_folder(mail)
            if not dst_folder:
                return {'status': 'error', 'message': '未找到垃圾箱/已删除文件夹，请使用 --dst_folder 手动指定目标文件夹'}

        if not dst_folder:
            return {'status': 'error', 'message': '请通过 --dst_folder 指定目标文件夹，或使用 --delete 移至垃圾箱'}

        # 确保目标文件夹名含空格时有双引号包裹
        dst_folder_quoted = quote_folder(dst_folder)

        # 预览阶段：readonly + BODY.PEEK，避免标记已读
        status, _ = mail.select(quote_folder(src_folder), readonly=True)
        if status != 'OK':
            return {'status': 'error', 'message': f'无法访问源文件夹: {src_folder}'}

        # 预览邮件信息
        previews, not_found = preview_emails(mail, mail_ids, src_folder)

        if not previews:
            mail.logout()
            return {'status': 'error', 'message': '未找到任何可操作的邮件', 'not_found': not_found}

        # 未确认时仅返回预览
        if not confirm:
            mail.logout()
            return {
                'status': 'preview',
                'action': '删除' if delete else '移动',
                'src_folder': src_folder,
                'dst_folder': dst_folder,
                'emails': previews,
                'not_found': not_found,
                'message': f'即将将 {len(previews)} 封邮件从 {src_folder} {"删除(移至" + dst_folder + ")" if delete else "移动到 " + dst_folder}，请加 --confirm 确认执行'
            }

        # 确认执行：重新select（非readonly），逐封复制+删除
        status, _ = mail.select(quote_folder(src_folder))
        if status != 'OK':
            mail.logout()
            return {'status': 'error', 'message': f'无法访问源文件夹: {src_folder}'}

        success = []
        failed = []

        for mid in mail_ids:
            try:
                # 复制到目标文件夹
                status, _ = mail.copy(mid.encode(), dst_folder_quoted)
                if status != 'OK':
                    print(f"[move_emails] copy failed for mail_id={mid}", file=sys.stderr)
                    failed.append(mid)
                    continue
                # 标记删除并清理
                mail.store(mid.encode(), '+FLAGS', '\\Deleted')
                success.append(mid)
            except Exception as e:
                print(f"[move_emails] mail_id={mid} error: {e}", file=sys.stderr)
                failed.append(mid)

        mail.expunge()
        mail.logout()

        action_text = '删除' if delete else f'移动到 {dst_folder}'
        result = {
            'status': 'success',
            'action': action_text,
            'src_folder': src_folder,
            'dst_folder': dst_folder,
            'total': len(mail_ids),
            'success_count': len(success),
            'failed_count': len(failed),
            'emails': previews,
            'message': f'已将 {len(success)}/{len(mail_ids)} 封邮件{action_text}'
        }

        if failed:
            result['failed'] = failed
            result['status'] = 'partial'

        return result

    except imaplib.IMAP4.error as e:
        return {'status': 'error', 'message': f'IMAP错误: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'错误: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description='移动或删除QQ邮箱邮件')
    parser.add_argument('--mail_ids', required=True, help='邮件编号(多个逗号分隔)')
    parser.add_argument('--src_folder', required=True, help='源文件夹（必填）')
    parser.add_argument('--dst_folder', help='目标文件夹')
    parser.add_argument('--delete', action='store_true', help='删除邮件(移至垃圾箱，等同于 --dst_folder 垃圾箱)')
    parser.add_argument('--confirm', action='store_true', help='确认执行操作(不加则仅返回预览)')
    args = parser.parse_args()

    email_addr, auth_code = get_credentials()
    if not email_addr or not auth_code:
        print(json.dumps({'status': 'error', 'message': '缺少凭证信息，请先配置QQ邮箱地址和授权码'}, ensure_ascii=False))
        return

    mail_ids = [mid.strip() for mid in args.mail_ids.split(',') if mid.strip()]
    if not mail_ids:
        print(json.dumps({'status': 'error', 'message': '邮件编号不能为空'}, ensure_ascii=False))
        return

    if not args.dst_folder and not args.delete:
        parser.error('请指定 --dst_folder 或 --delete')

    result = move_emails(email_addr, auth_code, mail_ids, args.src_folder, args.dst_folder, args.delete, args.confirm)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
