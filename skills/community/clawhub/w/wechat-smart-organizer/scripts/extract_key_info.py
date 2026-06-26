#!/usr/bin/env python3
"""
微信聊天记录关键信息提取脚本
从 wechat-cli 输出的 JSON 数据中提取关键信息
"""

import json
import sys
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

def extract_todos(messages: List[Dict]) -> List[Dict]:
    """从消息列表中提取待办事项"""
    todo_patterns = [
        r'(需要|要|得|麻烦|帮我|请|帮我|记得|别忘)',
        r'(完成|做好|做完|提交|发送|处理|整理)',
        r'(todo|TODO|待办|任务)',
    ]
    
    todos = []
    for msg in messages:
        if msg.get('type') != 'text':
            continue
        content = msg.get('content', '')
        for pattern in todo_patterns:
            if re.search(pattern, content):
                todos.append({
                    'content': content,
                    'sender': msg.get('sender', '未知'),
                    'time': msg.get('time', ''),
                    'chat': msg.get('chat', '')
                })
                break
    return todos

def extract_dates(messages: List[Dict]) -> List[Dict]:
    """从消息列表中提取时间相关事项"""
    date_patterns = [
        (r'周[一二三四五六日天]', '星期'),
        (r'下*周[一二三四五六日天]', '下星期'),
        (r'\d+号', '日期'),
        (r'今天|明天|后天', '相对日期'),
        (r'下午\d+|上午\d+|晚上\d+|早上\d+', '时间段'),
        (r'\d+:\d+', '具体时间'),
    ]
    
    date_items = []
    for msg in messages:
        if msg.get('type') != 'text':
            continue
        content = msg.get('content', '')
        for pattern, date_type in date_patterns:
            if re.search(pattern, content):
                date_items.append({
                    'content': content,
                    'matched_type': date_type,
                    'matched_text': re.search(pattern, content).group(),
                    'sender': msg.get('sender', '未知'),
                    'time': msg.get('time', ''),
                    'chat': msg.get('chat', '')
                })
                break
    return date_items

def extract_contacts(messages: List[Dict]) -> List[Dict]:
    """从消息列表中提取联系方式"""
    contact_patterns = [
        (r'微信[：:]?\s*(\w+)', '微信号'),
        (r'电话[：:]?\s*(\d[\d\-\s]{10,})', '电话'),
        (r'邮箱[：:]?\s*(\w+@\w+\.\w+)', '邮箱'),
        (r'加我.*?(微信|QQ)[：:]?\s*(\w+)', '联系方式'),
    ]
    
    contacts = []
    for msg in messages:
        if msg.get('type') != 'text':
            continue
        content = msg.get('content', '')
        for pattern, contact_type in contact_patterns:
            match = re.search(pattern, content)
            if match:
                contacts.append({
                    'content': content,
                    'type': contact_type,
                    'value': match.group(1) if match.groups() else '',
                    'sender': msg.get('sender', '未知'),
                    'time': msg.get('time', ''),
                    'chat': msg.get('chat', '')
                })
                break
    return contacts

def extract_links(messages: List[Dict]) -> List[Dict]:
    """从消息列表中提取链接信息"""
    links = []
    for msg in messages:
        if msg.get('type') == 'link':
            links.append({
                'title': msg.get('title', '无标题'),
                'url': msg.get('url', ''),
                'description': msg.get('description', ''),
                'sender': msg.get('sender', '未知'),
                'time': msg.get('time', ''),
                'chat': msg.get('chat', '')
            })
    return links

def generate_obsidian_note(data_type: str, items: List[Dict], title: str) -> str:
    """生成 Obsidian 格式的笔记"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    note = f"""---
type: wechat-extract
source: {items[0]['chat'] if items else '未知'}
category: {data_type}
created: {now}
tags: [微信, {data_type}]
---

# {title}

> 从微信聊天记录中提取的 {data_type} 信息

## 提取时间
{now}

## 提取内容

"""
    
    for i, item in enumerate(items, 1):
        note += f"### {i}. {item.get('sender', '未知')} ({item.get('time', '')}')\n\n"
        note += f"> {item.get('content', '')}\n\n"
        if item.get('url'):
            note += f"- 链接: {item.get('url')}\n"
        note += "\n"
    
    return note

def main():
    # 从 stdin 读取 JSON 数据
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("错误: 无法解析 JSON 数据", file=sys.stderr)
        print("请使用 --format json 参数获取数据", file=sys.stderr)
        sys.exit(1)
    
    # 提取各类信息
    todos = extract_todos(data.get('messages', []))
    dates = extract_dates(data.get('messages', []))
    contacts = extract_contacts(data.get('messages', []))
    links = extract_links(data.get('messages', []))
    
    # 输出结果
    result = {
        'summary': {
            'total_messages': len(data.get('messages', [])),
            'todos_count': len(todos),
            'dates_count': len(dates),
            'contacts_count': len(contacts),
            'links_count': len(links)
        },
        'todos': todos,
        'dates': dates,
        'contacts': contacts,
        'links': links
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
