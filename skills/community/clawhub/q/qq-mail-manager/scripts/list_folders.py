#!/usr/bin/env python3
"""列出QQ邮箱所有文件夹"""

import argparse
import imaplib
import json
import os
import ssl
import base64

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


def decode_imap_utf7(s):
    """解码 IMAP modified UTF-7 编码的字符串
    
    IMAP modified UTF-7 规则：
    - ASCII 可打印字符直接表示
    - 非 ASCII 字符用 &...- 包裹，其中 ... 是 modified base64 编码
    - & 本身用 &- 表示
    例如: &UXZO1mWHTvZZOQ- 解码为 "已删除邮件"
    """
    if not s:
        return s
    
    result = []
    i = 0
    while i < len(s):
        if s[i] == '&' and i + 1 < len(s):
            # 找到结束的 -
            j = s.find('-', i + 1)
            if j == -1:
                # 没有找到结束符，原样保留
                result.append(s[i])
                i += 1
                continue
            
            encoded = s[i + 1:j]
            if not encoded:
                # &- 表示 & 本身
                result.append('&')
            else:
                # modified base64 解码
                # modified UTF-7 使用的是标准 base64，但编码的是 UTF-16BE
                try:
                    # 补齐 base64 padding
                    padding = (4 - len(encoded) % 4) % 4
                    padded = encoded + '=' * padding
                    decoded_bytes = base64.b64decode(padded)
                    # 从 UTF-16BE 解码为 Unicode
                    text = decoded_bytes.decode('utf-16-be')
                    result.append(text)
                except Exception:
                    # 解码失败，原样返回
                    result.append(s[i:j + 1])
            
            i = j + 1
        else:
            result.append(s[i])
            i += 1
    
    return ''.join(result)


def parse_folder_name(folder_str):
    """从 IMAP LIST 响应中解析文件夹名并解码
    
    响应格式: (\\HasNoChildren) "/" "Sent Messages"
    或: (\\HasNoChildren) "/" "&UXZO1mWHTvZZOQ-"
    """
    parts = folder_str.split('"')
    # 取最后一个非空非分隔符的部分作为文件夹名
    name = ''
    for p in reversed(parts):
        p = p.strip()
        if p and p != '/' and not p.startswith('('):
            name = p
            break
    
    # 解码 modified UTF-7
    decoded_name = decode_imap_utf7(name)
    
    return name, decoded_name


def list_folders(email_addr, auth_code):
    """列出邮箱所有文件夹"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ssl.create_default_context())
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'

        status, folders = mail.list()
        if status != 'OK':
            return {'status': 'error', 'message': '无法获取文件夹列表'}

        result = []
        for f in folders:
            if isinstance(f, bytes):
                f = f.decode('utf-8', errors='replace')
            
            name, decoded_name = parse_folder_name(f)
            result.append({
                'name': name,           # IMAP 原始名（用于脚本参数）
                'display': decoded_name, # 解码后的可读名（给用户看）
                'raw': f
            })

        mail.logout()

        return {
            'status': 'success',
            'folders': result,
            'total': len(result)
        }

    except imaplib.IMAP4.error as e:
        return {'status': 'error', 'message': f'IMAP错误: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'错误: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description='列出QQ邮箱所有文件夹')
    args = parser.parse_args()

    email_addr, auth_code = get_credentials()
    if not email_addr or not auth_code:
        print(json.dumps({'status': 'error', 'message': '缺少凭证信息，请先配置QQ邮箱地址和授权码'}, ensure_ascii=False))
        return

    result = list_folders(email_addr, auth_code)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
