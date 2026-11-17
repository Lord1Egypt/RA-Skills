#!/usr/bin/env python3
"""
拉取各邮箱最近未处理的邮件候选，供 Agent 判断是否为招聘邮件。

本脚本【不做关键词判定】——只负责：
1. 连接邮箱，扫描最近 N 封
2. 跳过已处理邮件、跳过明确的营销/通知类发件域名（避免浪费 Agent 注意力）
3. 提取 主题/发件人/日期/正文预览/链接 等结构化信息
4. 写入 pending_candidates.json，由 Agent 逐封判断

用法:
    python3 scripts/fetch-emails.py
"""

import poplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 本地配置文件（含邮箱账号等敏感信息，不随 Skill 发布）
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')


def load_config():
    """加载本地配置（email_accounts 等）"""
    if not os.path.exists(CONFIG_FILE):
        print("❌ 缺少本地配置文件 scripts/config.json", file=sys.stderr)
        print("   请参考 scripts/config.example.json 创建（包含 email_accounts 与 feishu_target）", file=sys.stderr)
        sys.exit(2)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# 多邮箱配置：从本地 config.json 加载，不硬编码凭据
EMAIL_ACCOUNTS = []

# 营销/通知类发件域名（预过滤：这些发件人几乎不可能发招聘邮件，直接跳过）
NOISE_DOMAINS = [
    'humblebundle.com', 'mailer.humblebundle.com',
    'deliver.ieee.org', 'ieee.org',
    'researchgatemail.net',
    'linkedin.com',
    'qdrant.com',
    'marketo.com'
]

# 已知招聘系统/企业招聘发件域名（仅作为 hint 提示 Agent，不直接判定）
KNOWN_RECRUITER_DOMAINS = [
    'oppo.com', 'nowcoder.org', 'nowcoder.com', 'joinus.cc',
    'dji.com', 'netease.com', 'mokahr.com', 'moka.ai',
    'tencent.com', 'meituan.com', 'bytedance.com'
]

PROCESSED_FILE = os.path.join(SCRIPT_DIR, 'processed_emails.json')
CANDIDATES_FILE = os.path.join(SCRIPT_DIR, 'pending_candidates.json')

MAX_SCAN_PER_ACCOUNT = 50
MAX_CANDIDATES = 40
BODY_PREVIEW_LEN = 600


def decode_mime_words(s):
    """解码 MIME 编码的字符串"""
    if not s:
        return ''
    out = []
    for part, encoding in decode_header(s):
        if isinstance(part, bytes):
            try:
                out.append(part.decode(encoding or 'utf-8', errors='ignore'))
            except Exception:
                out.append(part.decode('utf-8', errors='ignore'))
        else:
            out.append(part)
    return ''.join(out)


def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def get_email_unique_id(msg):
    """生成邮件唯一标识（与旧版一致，保证去重连续性）"""
    msg_id = msg.get('Message-ID', '')
    if msg_id:
        return msg_id
    from_addr = msg.get('From', '')
    subject = msg.get('Subject', '')
    date = msg.get('Date', '')
    return f"{from_addr}|{subject}|{date}"


def extract_text_body(msg):
    """提取纯文本正文；HTML 邮件粗略去标签"""
    def strip_html(html):
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get_content_disposition())
            if 'attachment' in cd:
                continue
            try:
                payload = part.get_payload(decode=True)
            except Exception:
                payload = None
            if not payload:
                continue
            try:
                text = payload.decode('utf-8', errors='ignore')
            except Exception:
                continue
            if ct == 'text/plain':
                if text.strip():
                    return text.strip()
            elif ct == 'text/html':
                cleaned = strip_html(text)
                if cleaned:
                    return cleaned
        return ''
    try:
        payload = msg.get_payload(decode=True)
        if payload is None:
            return str(msg.get_payload())
        text = payload.decode('utf-8', errors='ignore')
        if msg.get_content_type() == 'text/html':
            return strip_html(text)
        return text.strip()
    except Exception:
        return str(msg.get_payload())


def extract_first_link(body):
    """提取正文中第一个有意义的链接（跳过图片 CDN）"""
    urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', body)
    for u in urls:
        if any(x in u for x in ['alicdn.com', 'imgextra', 'cdn.m.tencent.com/hr']):
            continue
        return u
    return None


def fetch_candidates():
    processed = load_processed()
    candidates = []

    for acct in EMAIL_ACCOUNTS:
        pop3 = None
        account_short = 'QQ' if 'qq.com' in acct['user'] else '163'
        try:
            pop3 = poplib.POP3_SSL(acct['host'], acct['port'], timeout=30)
            pop3.user(acct['user'])
            pop3.pass_(acct['password'])
            num = len(pop3.list()[1])

            for i in range(num, max(num - MAX_SCAN_PER_ACCOUNT, 0), -1):
                try:
                    resp, lines, octets = pop3.retr(i)
                    msg = email.message_from_bytes(b'\r\n'.join(lines))
                    uid = get_email_unique_id(msg)
                    if uid in processed:
                        continue

                    from_addr = decode_mime_words(msg.get('From', ''))
                    m = re.search(r'@([a-zA-Z0-9.-]+)', from_addr)
                    sender_domain = m.group(1).lower() if m else ''

                    # 预过滤：明确营销/通知发件人
                    if any(sender_domain == d or sender_domain.endswith('.' + d)
                           for d in NOISE_DOMAINS):
                        continue

                    subject = decode_mime_words(msg.get('Subject', '')).strip()
                    date_str = msg.get('Date', '')
                    try:
                        d = parsedate_to_datetime(date_str).strftime('%Y-%m-%d %H:%M')
                    except Exception:
                        d = datetime.now().strftime('%Y-%m-%d %H:%M')

                    body = extract_text_body(msg)
                    body_preview = body[:BODY_PREVIEW_LEN].strip()

                    hint = any(sender_domain == d2 or sender_domain.endswith('.' + d2)
                               for d2 in KNOWN_RECRUITER_DOMAINS)

                    candidates.append({
                        'id': len(candidates) + 1,
                        'account': account_short,
                        'date': d,
                        'from': from_addr,
                        'sender_domain': sender_domain,
                        'subject': subject,
                        'body_preview': body_preview,
                        'link': extract_first_link(body),
                        'hint_recruiter_domain': hint,
                        'uid': uid,
                    })
                    if len(candidates) >= MAX_CANDIDATES:
                        break
                except Exception:
                    continue
            pop3.quit()
        except Exception as e:
            print(f"[{acct['name']}] 拉取失败: {e}", file=sys.stderr)
            if pop3:
                try:
                    pop3.quit()
                except Exception:
                    pass
        if len(candidates) >= MAX_CANDIDATES:
            break

    with open(CANDIDATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)

    print(f"已拉取 {len(candidates)} 封未处理邮件候选 -> {CANDIDATES_FILE}")
    for c in candidates:
        hint_mark = ' [招聘系统域名]' if c['hint_recruiter_domain'] else ''
        print(f"  #{c['id']} {c['date']} | {c['subject'][:50]}{hint_mark}")


def main():
    global EMAIL_ACCOUNTS
    cfg = load_config()
    EMAIL_ACCOUNTS = cfg.get('email_accounts', [])
    if not EMAIL_ACCOUNTS:
        print("❌ config.json 中未配置 email_accounts", file=sys.stderr)
        sys.exit(2)
    fetch_candidates()


if __name__ == '__main__':
    main()
