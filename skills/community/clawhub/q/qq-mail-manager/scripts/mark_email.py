#!/usr/bin/env python3
"""标记QQ邮箱邮件为已读或未读"""
import argparse
import json
import os
import sys
import imaplib
import ssl


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


def mark_emails(email_addr, auth_code, mail_ids, action, folder='INBOX'):
    """标记邮件已读或未读"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ssl.create_default_context())
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'

        status, _ = mail.select(quote_folder(folder))
        if status != 'OK':
            return {'status': 'error', 'message': f'无法访问文件夹: {folder}'}

        if action == 'read':
            flag_op = '+FLAGS'
            flag_name = '\\Seen'
            action_text = '已读'
        else:
            flag_op = '-FLAGS'
            flag_name = '\\Seen'
            action_text = '未读'

        success_ids = []
        failed_ids = []

        for mid in mail_ids:
            try:
                status, _ = mail.store(mid.encode(), flag_op, flag_name)
                if status == 'OK':
                    success_ids.append(mid)
                else:
                    failed_ids.append(mid)
            except Exception as e:
                print(f"[mark_email] mail_id={mid} error: {e}", file=sys.stderr)
                failed_ids.append(mid)

        mail.logout()

        result = {
            'status': 'success',
            'action': action_text,
            'folder': folder,
            'success': success_ids,
            'failed': failed_ids,
            'total': len(mail_ids),
            'success_count': len(success_ids),
            'message': f'已将 {len(success_ids)}/{len(mail_ids)} 封邮件标记为{action_text}'
        }

        if failed_ids:
            result['status'] = 'partial'

        return result

    except imaplib.IMAP4.error as e:
        return {'status': 'error', 'message': f'IMAP错误: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'错误: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description='标记QQ邮箱邮件为已读或未读')
    parser.add_argument('--mail_ids', required=True, help='邮件编号(多个逗号分隔)')
    parser.add_argument('--action', required=True, choices=['read', 'unread'], help='标记操作: read=已读, unread=未读')
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

    result = mark_emails(email_addr, auth_code, mail_ids, args.action, args.folder)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
