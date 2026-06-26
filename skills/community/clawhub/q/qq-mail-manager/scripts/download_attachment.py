#!/usr/bin/env python3
"""下载QQ邮箱邮件附件"""
import argparse
import json
import os
import re
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
    if name.startswith('"') and name.endswith('"'):
        return name
    if ' ' in name:
        return f'"{name}"'
    return name


def safe_filename(filename):
    """清洗文件名，防止路径遍历攻击"""
    name = os.path.basename(filename)
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name.replace('..', '_')
    if not name or name.strip('.') == '':
        name = 'attachment'
    return name


def download_attachments_for_mail(mail, mail_id, folder, output_dir='.', target_file=None):
    """下载单封邮件的附件"""
    try:
        status, msg_data = mail.fetch(mail_id.encode(), '(BODY.PEEK[])')
        if status != 'OK':
            return {'mail_id': mail_id, 'folder': folder, 'status': 'error', 'message': f'无法获取邮件'}

        raw = None
        for item in msg_data:
            if isinstance(item, tuple):
                raw = item[1]
                break
        if not raw:
            return {'mail_id': mail_id, 'folder': folder, 'status': 'error', 'message': f'无法获取邮件内容'}

        msg = BytesParser().parsebytes(raw)

        downloaded = []
        skipped = []

        for part in msg.walk():
            filename = part.get_filename()
            if not filename:
                continue

            decoded_filename = decode_str(filename)

            if target_file and decoded_filename != target_file:
                skipped.append(decoded_filename)
                continue

            payload = part.get_payload(decode=True)
            if payload is None:
                skipped.append(decoded_filename)
                continue

            # 安全：清洗文件名
            safe_name = safe_filename(decoded_filename)
            save_path = os.path.join(output_dir, safe_name)
            if os.path.exists(save_path):
                name, ext = os.path.splitext(safe_name)
                counter = 1
                while os.path.exists(os.path.join(output_dir, f'{name}_{counter}{ext}')):
                    counter += 1
                save_path = os.path.join(output_dir, f'{name}_{counter}{ext}')

            with open(save_path, 'wb') as f:
                f.write(payload)

            downloaded.append({
                'name': safe_name,
                'size': len(payload),
                'path': os.path.abspath(save_path)
            })

        if target_file and not downloaded:
            return {
                'mail_id': mail_id,
                'folder': folder,
                'status': 'error',
                'message': f'未找到附件: {target_file}',
                'available': skipped
            }

        return {
            'mail_id': mail_id,
            'folder': folder,
            'status': 'success',
            'downloaded': downloaded,
            'download_count': len(downloaded),
            'total_size': sum(d['size'] for d in downloaded)
        }

    except Exception as e:
        print(f"[download_attachment] mail_id={mail_id} error: {e}", file=sys.stderr)
        return {'mail_id': mail_id, 'folder': folder, 'status': 'error', 'message': str(e)}


def main():
    parser = argparse.ArgumentParser(description='下载QQ邮箱邮件附件')
    parser.add_argument('--mail_ids', required=True, help='邮件编号，多个逗号分隔')
    parser.add_argument('--folder', required=True, help='邮箱文件夹（必填）')
    parser.add_argument('--dir', default='.', help='输出目录（默认当前目录）')
    parser.add_argument('--file', help='仅下载指定附件名（不传则下载全部）')
    args = parser.parse_args()

    email_addr, auth_code = get_credentials()
    if not email_addr or not auth_code:
        print(json.dumps({'status': 'error', 'message': '缺少凭证信息，请先配置QQ邮箱地址和授权码'}, ensure_ascii=False))
        return

    mail_ids = [m.strip() for m in args.mail_ids.split(',') if m.strip()]

    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ssl.create_default_context())
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'

        status, _ = mail.select(quote_folder(args.folder), readonly=True)
        if status != 'OK':
            print(json.dumps({'status': 'error', 'message': f'无法访问文件夹: {args.folder}'}, ensure_ascii=False))
            return

        os.makedirs(args.dir, exist_ok=True)

        results = []
        for mid in mail_ids:
            result = download_attachments_for_mail(mail, mid, args.folder, args.dir, args.file)
            results.append(result)

        mail.logout()

        total_downloaded = sum(r.get('download_count', 0) for r in results)
        total_size = sum(r.get('total_size', 0) for r in results)
        errors = [r for r in results if r.get('status') == 'error']

        output = {
            'status': 'error' if errors else 'success',
            'folder': args.folder,
            'total_mails': len(mail_ids),
            'total_downloaded': total_downloaded,
            'total_size': total_size,
            'results': results
        }
        if errors:
            output['message'] = f'{len(errors)}/{len(mail_ids)} 封邮件处理失败'
        else:
            output['message'] = f'已处理 {len(mail_ids)} 封邮件，下载 {total_downloaded} 个附件'

        print(json.dumps(output, ensure_ascii=False))

    except imaplib.IMAP4.error as e:
        print(json.dumps({'status': 'error', 'message': f'IMAP错误: {str(e)}'}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'status': 'error', 'message': f'错误: {str(e)}'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
