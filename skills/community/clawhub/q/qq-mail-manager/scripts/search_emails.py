#!/usr/bin/env python3
"""查询QQ邮箱中的邮件（浏览 + 搜索 + 跨文件夹搜索）"""
import argparse
import base64
import json
import os
import sys
import imaplib
import re
import ssl
from datetime import datetime, timedelta, timezone
from email.header import decode_header
from email.parser import BytesParser


IMAP_HOST = 'imap.qq.com'
IMAP_PORT = 993
# QQ邮箱IMAP服务器在UTC+8时区，SINCE/BEFORE按服务器本地日期判断
# 脚本运行环境可能是UTC，因此日期计算统一使用UTC+8，确保与服务器一致
UTC8 = timezone(timedelta(hours=8))

SKILL_ID = '7637538402895773731'
CRED_NAME = 'qq_email'
ENV_EMAIL = 'QQ_EMAIL'
ENV_AUTH_CODE = 'QQ_EMAIL_AUTH_CODE'
LEGACY_ENV_EMAIL = f'COZE_{CRED_NAME}_QQ_EMAIL_{SKILL_ID}'
LEGACY_ENV_AUTH_CODE = f'COZE_{CRED_NAME}_QQ_EMAIL_AUTH_CODE_{SKILL_ID}'


def get_credentials():
    """从环境变量获取凭证"""
    email_addr = os.environ.get(ENV_EMAIL) or os.environ.get(LEGACY_ENV_EMAIL, '')
    auth_code = os.environ.get(ENV_AUTH_CODE) or os.environ.get(LEGACY_ENV_AUTH_CODE, '')
    if not email_addr or not auth_code:
        return None, None
    return email_addr, auth_code


def decode_str(s):
    """解码邮件头部字符串"""
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


def extract_preview(msg, max_len=300):
    """提取正文摘要"""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or 'utf-8'
                    return payload.decode(charset, errors='replace')[:max_len]
                except Exception as e:
                    print(f"[peek_body] multipart decode error: {e}", file=sys.stderr)
        return ""
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or 'utf-8'
                return payload.decode(charset, errors='replace')[:max_len]
        except Exception as e:
            print(f"[peek_body] single part decode error: {e}", file=sys.stderr)
        return ""


def parse_date_arg(date_str):
    """将输入日期转为IMAP格式 DD-Mon-YYYY，支持多种输入格式。
    用户输入的日期基于本地理解（即UTC+8），直接转为IMAP格式即可，无需偏移。"""
    for fmt in ['%d-%b-%Y', '%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y']:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%d-%b-%Y')
        except ValueError:
            continue
    raise ValueError(f'无法解析日期: {date_str}，支持格式: YYYY-MM-DD, YYYY/MM/DD, DD-Mon-YYYY')


def parse_recent_arg(recent_str):
    """解析相对时间表达式，返回 (IMAP SINCE日期字符串, 精确截止datetime对象)。
    使用UTC+8时区计算当前时间，与QQ邮箱IMAP服务器保持一致。
    SINCE日期向前多取1天以确保不漏，精确过滤由二次筛选完成。"""
    match = re.match(r'^(\d+)([mhdw])$', recent_str.lower().strip())
    if not match:
        raise ValueError(f'无法解析相对时间: {recent_str}，支持格式: 30m(分钟), 2h(小时), 7d(天), 1w(周)')

    value = int(match.group(1))
    unit = match.group(2)

    now = datetime.now(UTC8)
    if unit == 'm':
        since_dt = now - timedelta(minutes=value)
    elif unit == 'h':
        since_dt = now - timedelta(hours=value)
    elif unit == 'd':
        since_dt = now - timedelta(days=value)
    elif unit == 'w':
        since_dt = now - timedelta(weeks=value)
    else:
        raise ValueError(f'不支持的时间单位: {unit}')

    # SINCE日期向前多取1天，确保不漏；精确过滤由二次筛选完成
    imap_since = (since_dt - timedelta(days=1)).strftime('%d-%b-%Y')
    return imap_since, since_dt


def decode_imap_utf7(s):
    """将 IMAP modified UTF-7 编码的文件夹名解码为可读字符串"""
    if '&' not in s:
        return s
    result = []
    i = 0
    while i < len(s):
        if s[i] == '&':
            j = s.find('-', i)
            if j == -1:
                result.append(s[i:])
                break
            if j == i + 1:
                result.append('&')
            else:
                b64 = s[i + 1:j].replace(',', '/')
                pad = (4 - len(b64) % 4) % 4
                b64 += '=' * pad
                try:
                    result.append(base64.b64decode(b64).decode('utf-16-be'))
                except Exception:
                    result.append(s[i:j + 1])
            i = j + 1
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


def get_all_folders(mail):
    """获取所有文件夹列表（含 IMAP 原始名和可读显示名）"""
    status, folders = mail.list()
    if status != 'OK':
        return []
    result = []
    for folder in folders:
        if not folder:
            continue
        folder_str = folder.decode() if isinstance(folder, bytes) else str(folder)
        parts = folder_str.split('"')
        name = ''
        for i in range(len(parts) - 1, -1, -1):
            p = parts[i].strip()
            if p and p not in ('/', '.', '\\'):
                name = p
                break
        if name:
            result.append({'name': name, 'display': decode_imap_utf7(name)})
    return result


def build_search_criteria(query=None, from_addr=None, subject=None,
                          since=None, before=None, seen=None):
    """构建IMAP搜索条件列表，返回 (criteria_parts, is_fuzzy)"""
    has_field_filter = from_addr or subject

    if has_field_filter:
        # 精确字段搜索
        criteria_parts = []
        if from_addr:
            criteria_parts.append(f'FROM "{from_addr}"')
        if subject:
            criteria_parts.append(f'SUBJECT "{subject}"')
        if since:
            criteria_parts.append(f'SINCE {since}')
        if before:
            criteria_parts.append(f'BEFORE {before}')
        if seen is True:
            criteria_parts.append('SEEN')
        elif seen is False:
            criteria_parts.append('UNSEEN')
        if not criteria_parts:
            criteria_parts = ['ALL']
        return criteria_parts, False

    elif query and query != '*':
        # 模糊三字段搜索（需要在调用方拆分为3次搜索取并集）
        base_criteria = []
        if since:
            base_criteria.append(f'SINCE {since}')
        if before:
            base_criteria.append(f'BEFORE {before}')
        if seen is True:
            base_criteria.append('SEEN')
        elif seen is False:
            base_criteria.append('UNSEEN')
        return base_criteria, True

    else:
        # 无关键词、无字段过滤：仅按条件搜索或ALL
        criteria_parts = []
        if since:
            criteria_parts.append(f'SINCE {since}')
        if before:
            criteria_parts.append(f'BEFORE {before}')
        if seen is True:
            criteria_parts.append('SEEN')
        elif seen is False:
            criteria_parts.append('UNSEEN')
        if not criteria_parts:
            criteria_parts = ['ALL']
        return criteria_parts, False


def search_in_folder(mail, folder, query=None, from_addr=None, subject=None,
                     since=None, before=None, seen=None):
    """在单个文件夹中搜索，返回 (mail_id_bytes_list, folder_name)"""
    # 文件夹名含空格需加引号
    folder_arg = quote_folder(folder)
    status, _ = mail.select(folder_arg, readonly=True)
    if status != 'OK':
        return [], folder

    criteria_parts, is_fuzzy = build_search_criteria(
        query, from_addr, subject, since, before, seen
    )

    if is_fuzzy:
        # 模糊三字段搜索，取并集
        id_set = set()
        for field in [f'SUBJECT "{query}"', f'FROM "{query}"', f'TO "{query}"']:
            parts = [field] + criteria_parts
            status, msgs = mail.search(None, *parts)
            if status == 'OK' and msgs[0]:
                id_set.update(msgs[0].split())
        return list(id_set), folder
    else:
        # 精确字段搜索
        if from_addr:
            # QQ邮箱IMAP对FROM搜索匹配不稳定，需同时搜FROM和SUBJECT取并集
            id_set = set()
            for field in [f'FROM "{from_addr}"', f'SUBJECT "{from_addr}"']:
                parts = [field] + [c for c in criteria_parts if not c.startswith('FROM')]
                status, msgs = mail.search(None, *parts)
                if status == 'OK' and msgs[0]:
                    id_set.update(msgs[0].split())
            return list(id_set), folder
        else:
            status, msgs = mail.search(None, *criteria_parts)
            if status == 'OK' and msgs[0]:
                return msgs[0].split(), folder
            return [], folder


def fetch_email_summaries(mail, mail_ids, folder, max_len=150):
    """批量获取邮件摘要"""
    emails = []
    parser = BytesParser()
    for mid in mail_ids:
        mid_str = mid.decode() if isinstance(mid, bytes) else str(mid)
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

            email_subject = decode_str(msg.get('Subject', '')) or '(无主题)'
            sender = decode_str(msg.get('From', ''))
            date = msg.get('Date', '')
            preview = extract_preview(msg, max_len)

            emails.append({
                'mail_id': mid_str,
                'subject': email_subject,
                'sender': sender,
                'date': date,
                'preview': preview,
                'folder': folder
            })
        except Exception as e:
            print(f"[fetch_summaries] mail_id={mid} error: {e}", file=sys.stderr)
            continue
    return emails


def query_emails(email_addr, auth_code, query=None, from_addr=None, subject=None,
                 folder='INBOX', all_folders=False, since=None, before=None,
                 recent=None, seen=None, limit=None, offset=0):
    """统一查询邮件（浏览 + 搜索 + 跨文件夹）

    分页规则：
    - limit=None（不指定）: 用户期望全部结果
    - limit ≤ 15: 一次返回，不分页
    - limit > 15 且 total_matched > 15: 按15分页
    - limit > 15 且 total_matched ≤ 15: 一次返回，不分页
    """
    PAGE_SIZE = 15

    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ssl.create_default_context())
        mail.login(email_addr, auth_code)
        mail._encoding = 'utf-8'

        # 处理 --recent
        recent_dt = None
        if recent:
            recent_since, recent_dt = parse_recent_arg(recent)
            if since:
                since_dt = datetime.strptime(since, '%d-%b-%Y').replace(tzinfo=UTC8)
                since = max(since_dt, recent_dt).strftime('%d-%b-%Y')
            else:
                since = recent_since

        # 确定搜索的文件夹列表
        if all_folders:
            folder_dicts = get_all_folders(mail)
            if not folder_dicts:
                folder_dicts = [{'name': folder, 'display': folder}]
            folder_list = [(f['name'], f['display']) for f in folder_dicts]
        else:
            folder_list = [(folder, folder)]

        # 在各文件夹中搜索
        all_results = []  # [(mail_id_bytes, folder_name), ...]
        for fld, fld_display in folder_list:
            ids, fld_name = search_in_folder(
                mail, fld, query, from_addr, subject,
                since, before, seen
            )
            for mid in ids:
                all_results.append((mid, fld_name))

        if not all_results:
            mail.logout()
            result = {
                'status': 'success',
                'folder': folder if not all_folders else 'ALL',
                'since': since,
                'before': before,
                'recent': recent,
                'seen': seen,
                'total_matched': 0,
                'has_more': False,
                'emails': []
            }
            if query:
                result['query'] = query
            if from_addr:
                result['from'] = from_addr
            if subject:
                result['subject'] = subject
            return result

        # 按编号倒序（最新在前）
        all_results.sort(key=lambda x: int(x[0]), reverse=True)

        # --recent 精确时间过滤（IMAP SINCE 只精确到天，此处按邮件 Date 精确到分钟/小时）
        # 必须在分页前完成，确保 total_matched 是过滤后的真实值
        if recent_dt:
            # 轻量级获取所有结果的 Date 字段，精确过滤
            filtered_results = []
            for mid, fld in all_results:
                fld_arg = quote_folder(fld)
                try:
                    mail.select(fld_arg, readonly=True)
                    status, msg_data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (DATE)])')
                    if status == 'OK' and msg_data and msg_data[0]:
                        raw_header = None
                        for item in msg_data:
                            if isinstance(item, tuple):
                                raw_header = item[1]
                                break
                        if raw_header:
                            from email.utils import parsedate_to_datetime
                            header_str = raw_header.decode('utf-8', errors='replace')
                            for line in header_str.splitlines():
                                if line.lower().startswith('date:'):
                                    date_val = line[5:].strip()
                                    try:
                                        mail_dt = parsedate_to_datetime(date_val)
                                        if mail_dt and mail_dt.astimezone(UTC8) >= recent_dt:
                                            filtered_results.append((mid, fld))
                                    except Exception:
                                        filtered_results.append((mid, fld))  # 解析失败的保留
                                    break
                    if not filtered_results or filtered_results[-1] != (mid, fld):
                        # 没匹配到但也没加入（fetch失败），保留
                        pass
                except Exception:
                    filtered_results.append((mid, fld))  # 异常保留
            all_results = filtered_results

        total_matched = len(all_results)

        if total_matched == 0:
            mail.logout()
            result = {
                'status': 'success',
                'folder': folder if not all_folders else 'ALL',
                'since': since,
                'before': before,
                'recent': recent,
                'seen': seen,
                'total_matched': 0,
                'has_more': False,
                'emails': []
            }
            if query:
                result['query'] = query
            if from_addr:
                result['from'] = from_addr
            if subject:
                result['subject'] = subject
            return result

        # limit=None 表示用户期望全部结果
        if limit is None:
            limit = total_matched

        # 分页判断：limit ≤ 15 不分页；limit > 15 且 total_matched > 15 按 PAGE_SIZE 分页
        if limit <= PAGE_SIZE or total_matched <= PAGE_SIZE:
            # 不分页：返回 min(limit, total_matched) 封
            page_results = all_results[offset:offset + limit]
            has_more = False
            tip = None
        else:
            # 分页：每页 PAGE_SIZE 封，最多返回 limit 封
            effective_limit = min(PAGE_SIZE, limit - offset) if offset < limit else 0
            page_results = all_results[offset:offset + effective_limit]
            has_more = (offset + PAGE_SIZE) < limit and (offset + PAGE_SIZE) < total_matched
            if has_more:
                next_offset = offset + PAGE_SIZE
                tip = f'还有更多结果，使用 --offset {next_offset} 查看下一页'
            else:
                tip = None

        # 按文件夹分组 fetch（减少 select 切换次数）
        folder_groups = {}
        for mid, fld in page_results:
            folder_groups.setdefault(fld, []).append(mid)

        emails = []
        for fld, mids in folder_groups.items():
            fld_arg = quote_folder(fld)
            mail.select(fld_arg, readonly=True)
            # 保持原始排序
            sorted_mids = [m for m, f in page_results if f == fld]
            summaries = fetch_email_summaries(mail, sorted_mids, fld)
            for s in summaries:
                s['folder'] = fld
            emails.extend(summaries)

        id_order = {mid if isinstance(mid, str) else mid.decode(): i for i, (mid, _) in enumerate(page_results)}
        emails.sort(key=lambda e: id_order.get(e['mail_id'], 999))

        mail.logout()

        result = {
            'status': 'success',
            'folder': folder if not all_folders else 'ALL',
            'since': since,
            'before': before,
            'recent': recent,
            'seen': seen,
            'total_matched': total_matched,
            'has_more': has_more,
            'total': len(emails),
            'emails': emails
        }

        if tip:
            result['tip'] = tip

        if query:
            result['query'] = query
        if from_addr:
            result['from'] = from_addr
        if subject:
            result['subject'] = subject

        return result

    except imaplib.IMAP4.error as e:
        return {'status': 'error', 'message': f'IMAP错误: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'错误: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description='查询QQ邮箱邮件（浏览+搜索+跨文件夹）')

    # 搜索条件（均为可选，不传则浏览全部）
    parser.add_argument('--query', help='模糊搜索关键词（匹配发件人、主题、收件人）；传 * 表示不限关键词')
    parser.add_argument('--from', dest='from_addr', help='精确按发件人搜索')
    parser.add_argument('--subject', help='精确按主题搜索')

    # 文件夹
    parser.add_argument('--folder', default='INBOX', help='邮箱文件夹，默认 INBOX')
    parser.add_argument('--all-folders', action='store_true', help='搜索所有文件夹（跨文件夹搜索）')

    # 日期过滤
    parser.add_argument('--since', help='起始日期，含当天（格式: YYYY-MM-DD）')
    parser.add_argument('--before', help='截止日期，不含当天（格式: YYYY-MM-DD）')
    parser.add_argument('--recent', help='最近时间段（如 30m、2h、7d、1w）')

    # 已读/未读
    seen_group = parser.add_mutually_exclusive_group()
    seen_group.add_argument('--seen', action='store_true', help='仅已读邮件')
    seen_group.add_argument('--unseen', action='store_true', help='仅未读邮件')

    # 分页
    parser.add_argument('--limit', type=int, default=None, help='期望返回的总结果数；不指定则返回全部；≤15不分页，>15按15分页')
    parser.add_argument('--offset', type=int, default=0, help='分页偏移量，默认0')

    args = parser.parse_args()

    # 判断已读/未读
    seen_val = None
    if args.seen:
        seen_val = True
    elif args.unseen:
        seen_val = False

    # 解析日期
    since_imap = None
    before_imap = None
    if args.since:
        since_imap = parse_date_arg(args.since)
    if args.before:
        before_imap = parse_date_arg(args.before)

    email_addr, auth_code = get_credentials()
    if not email_addr or not auth_code:
        print(json.dumps({'status': 'error', 'message': '缺少凭证信息，请先配置QQ邮箱地址和授权码'}, ensure_ascii=False))
        return

    result = query_emails(
        email_addr, auth_code,
        query=args.query,
        from_addr=args.from_addr,
        subject=args.subject,
        folder=args.folder,
        all_folders=args.all_folders,
        since=since_imap,
        before=before_imap,
        recent=args.recent,
        seen=seen_val,
        limit=args.limit,
        offset=args.offset
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
