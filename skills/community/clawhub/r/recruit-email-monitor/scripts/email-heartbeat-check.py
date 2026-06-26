#!/usr/bin/env python3
"""
心跳时检查招聘邮件并记录到表格
每 30 分钟运行一次
"""

import poplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
import json
import openpyxl
import os

# 多邮箱配置
EMAIL_ACCOUNTS = [
    {
        'name': 'QQ 邮箱',
        'user': '2623274405@qq.com',
        'password': 'bxfwjdtvienzdihi',
        'host': 'pop.qq.com',
        'port': 995,
    },
    {
        'name': '163 邮箱',
        'user': 'haoxian_niu@163.com',
        'password': 'XStys36TXuV6geTq',
        'host': 'pop.163.com',
        'port': 995,
    }
]

# 招聘相关关键词
RECRUITMENT_KEYWORDS = [
    '招聘', '诚聘', '招贤纳士', '诚聘英才', '招募',
    '职位', '岗位', '工作机会', 'job opportunity', 'hiring',
    '简历', '面试', 'offer', '录用', '入职',
    '人力资源', '人事部', '加入我们', '团队招聘',
    '美团', 'meituan', '腾讯', 'tencent', '蚂蚁', 'ant'
]

# 高优先级关键词
HIGH_PRIORITY_KEYWORDS = [
    '招聘', '诚聘', '招贤纳士', '诚聘英才',
    'job opportunity', 'hiring', '加入我们', '美团', 'meituan'
]

# 表格路径
EXCEL_PATH = '/home/erhao/shared/招聘邮件汇总.xlsx'

# 已处理邮件记录文件（避免重复记录）
PROCESSED_FILE = '/home/erhao/.openclaw/scripts/processed_emails.json'

def decode_mime_words(s):
    """解码 MIME 编码的字符串"""
    if not s:
        return ''
    decoded = []
    for part, encoding in decode_header(s):
        if isinstance(part, bytes):
            try:
                decoded.append(part.decode(encoding or 'utf-8', errors='ignore'))
            except:
                decoded.append(part.decode('utf-8', errors='ignore'))
        else:
            decoded.append(part)
    return ''.join(decoded)

def load_processed_emails():
    """加载已处理的邮件 ID 列表"""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_processed_emails(processed):
    """保存已处理的邮件 ID 列表"""
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

def get_email_unique_id(msg):
    """生成邮件唯一标识"""
    msg_id = msg.get('Message-ID', '')
    if msg_id:
        return msg_id
    
    # 如果没有 Message-ID，用发件人 + 主题 + 日期作为标识
    from_addr = msg.get('From', '')
    subject = msg.get('Subject', '')
    date = msg.get('Date', '')
    return f"{from_addr}|{subject}|{date}"

def classify_email_type(subject, body):
    """根据邮件内容分类"""
    subject_lower = subject.lower()
    body_lower = body.lower()
    
    if any(kw in subject_lower for kw in ['笔试', '在线笔试', '笔试通知']):
        return '笔试/测评'
    elif any(kw in subject_lower for kw in ['测评', '人才测评', '性格测评']):
        return '笔试/测评'
    elif any(kw in subject_lower for kw in ['面试', '面试邀请', '面试通知']):
        return '面试'
    elif any(kw in subject_lower for kw in ['offer', '录用', '签约', '三方']):
        return 'Offer/录用'
    elif any(kw in subject_lower for kw in ['宣讲会', '说明会', 'open day']):
        return '宣讲会'
    elif any(kw in subject_lower for kw in ['投递成功', '简历', '申请']):
        return '投递确认'
    else:
        return '其他'

def extract_links(body):
    """从邮件正文提取链接"""
    import re
    urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', body)
    return urls[0] if urls else None

def clean_from_address(from_addr):
    """清理发件人地址，格式与旧数据保持一致"""
    # 如果已经是 "name" <email> 格式，保持不变
    if from_addr.startswith('"') and '<' in from_addr:
        return from_addr
    # 如果是 name <email> 格式，添加引号
    if '<' in from_addr and not from_addr.startswith('"'):
        parts = from_addr.split('<')
        name = parts[0].strip()
        email = '<' + parts[1]
        if name and not name.startswith('"'):
            return f'"{name}" {email}'
        return from_addr
    return from_addr

def clean_links(links):
    """清理链接，移除无意义的图片链接"""
    if not links:
        return None
    
    # 如果是单个链接
    if isinstance(links, str):
        # 移除图片 CDN 链接
        if 'alicdn.com' in links or 'imgextra' in links or 'cdn.m.tencent.com/hr' in links:
            return None
        return links
    
    # 如果是多个链接（列表）
    if isinstance(links, list):
        meaningful = []
        for link in links:
            if link and 'http' in link:
                # 跳过图片 CDN
                if 'alicdn.com' in link or 'imgextra' in link or 'cdn.m.tencent.com/hr' in link:
                    continue
                meaningful.append(link)
        return '; '.join(meaningful) if meaningful else None
    
    return None

def check_emails_for_account(account_config, processed_emails):
    """检查单个邮箱的招聘邮件"""
    new_emails = []
    pop3 = None
    
    try:
        pop3 = poplib.POP3_SSL(account_config['host'], account_config['port'])
        pop3.user(account_config['user'])
        pop3.pass_(account_config['password'])
        
        num_messages = len(pop3.list()[1])
        
        # 检查最近 50 封邮件
        max_check = min(num_messages, 50)
        
        for i in range(num_messages, num_messages - max_check, -1):
            try:
                response, lines, octets = pop3.retr(i)
                msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
                msg = email.message_from_string(msg_content)
                
                # 生成唯一 ID
                email_id = get_email_unique_id(msg)
                
                # 跳过已处理的邮件
                if email_id in processed_emails:
                    continue
                
                subject = decode_mime_words(msg.get('Subject', ''))
                from_addr = decode_mime_words(msg.get('From', ''))
                date_str = msg.get('Date', '')
                
                # 提取正文
                body = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get_content_disposition())
                        if content_type == 'text/plain' and 'attachment' not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            except:
                                pass
                            break
                else:
                    try:
                        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        body = msg.get_payload()
                
                # 检查关键词
                subject_lower = subject.lower()
                body_lower = body.lower()
                
                matched_keywords = [kw for kw in RECRUITMENT_KEYWORDS 
                                   if kw.lower() in subject_lower or kw.lower() in body_lower]
                
                has_high_priority = any(kw.lower() in subject_lower 
                                       for kw in HIGH_PRIORITY_KEYWORDS)
                
                # 至少匹配 2 个关键词，或者包含高优先级关键词
                if len(matched_keywords) >= 2 or has_high_priority:
                    # 分类
                    email_type = classify_email_type(subject, body)
                    
                    # 提取并清理链接
                    raw_links = extract_links(body)
                    link = clean_links(raw_links)
                    
                    # 解析日期
                    try:
                        email_date = parsedate_to_datetime(date_str)
                        formatted_date = email_date.strftime('%Y-%m-%d %H:%M')
                    except:
                        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                    
                    # 清理发件人格式
                    clean_from = clean_from_address(from_addr)
                    
                    new_emails.append({
                        'date': formatted_date,
                        'account': 'QQ' if 'qq.com' in account_config['user'] else '163',
                        'subject': subject.strip(),
                        'from': clean_from,
                        'status': '⏳ 待处理',
                        'type': email_type,
                        'link': link,
                        'deadline': None  # 可以后续解析
                    })
                    
                    # 标记为已处理
                    processed_emails.append(email_id)
                    
                    print(f"📧 发现新招聘邮件 [{account_config['name']}]:")
                    print(f"   主题：{subject}")
                    print(f"   发件人：{clean_from}")
                    print(f"   类型：{email_type}")
                    
            except Exception as e:
                continue
        
        pop3.quit()
        
    except Exception as e:
        print(f"[{account_config['name']}] 检查失败：{e}")
        if pop3:
            try:
                pop3.quit()
            except:
                pass
    
    return new_emails

def append_to_excel(new_emails):
    """将新邮件添加到 Excel 表格"""
    if not new_emails:
        return
    
    try:
        # 加载工作簿
        wb = openpyxl.load_workbook(EXCEL_PATH)
        ws = wb.active
        
        # 添加新行 (列顺序：日期，邮箱，主题，发件人，状态，类型，链接，截止日期)
        for email_data in new_emails:
            ws.append([
                email_data['date'],
                email_data['account'],
                email_data['subject'],
                email_data['from'],
                email_data.get('status', '⏳ 待处理'),
                email_data['type'],
                email_data['link'],
                email_data['deadline']
            ])
        
        # 保存
        wb.save(EXCEL_PATH)
        print(f"\n✅ 已添加 {len(new_emails)} 封邮件到表格")
        
    except Exception as e:
        print(f"❌ 写入表格失败：{e}")

def send_feishu_notification(new_emails):
    """通过 Feishu 发送新邮件通知"""
    import subprocess
    
    if not new_emails:
        return
    
    # 生成通知内容
    message = f"📧 收到 {len(new_emails)} 封新招聘邮件\n\n"
    
    for i, email in enumerate(new_emails[:5], 1):  # 最多显示 5 封
        emoji = {
            '笔试/测评': '✍️',
            '面试': '🎤',
            'Offer/录用': '🎉',
            '宣讲会': '📢',
            '投递确认': '✅',
            '其他': '📧'
        }.get(email['type'], '📧')
        
        message += f"{i}. {emoji} {email['subject']}\n"
        message += f"   类型：{email['type']} | 邮箱：{email['account']}\n\n"
    
    if len(new_emails) > 5:
        message += f"... 还有 {len(new_emails) - 5} 封，请查看表格\n"
    
    message += f"\n⏰ 检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # 通过 OpenClaw CLI 发送
    try:
        cmd = [
            'openclaw', 'message', 'send',
            '--channel', 'feishu',
            '--target', 'user:ou_8de02604ccd510eeb4897ffd70d96c1d',
            '--message', message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Feishu 通知已发送")
        else:
            print(f"❌ 发送失败：{result.stderr}")
    except subprocess.TimeoutExpired:
        print("❌ 发送超时")
    except Exception as e:
        print(f"❌ 发送异常：{e}")

def main():
    print('🔍 心跳检查：招聘邮件监控\n')
    print(f'检查时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    # 加载已处理邮件
    processed_emails = load_processed_emails()
    
    # 检查所有邮箱
    new_emails = []
    for account in EMAIL_ACCOUNTS:
        emails = check_emails_for_account(account, processed_emails)
        new_emails.extend(emails)
    
    # 保存到表格并发送通知
    if new_emails:
        append_to_excel(new_emails)
        
        # 发送 Feishu 通知
        send_feishu_notification(new_emails)
        
        # 保存已处理邮件列表
        save_processed_emails(processed_emails)
        
        print(f"\n📊 本次发现 {len(new_emails)} 封新招聘邮件")
    else:
        print("\n✅ 没有新的招聘邮件")
    
    print("\n" + "=" * 50)
    print("心跳检查完成")

if __name__ == '__main__':
    main()
