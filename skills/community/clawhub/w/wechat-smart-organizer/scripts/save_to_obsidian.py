#!/usr/bin/env python3
"""
微信信息存储脚本（支持 Obsidian vault 自动检测）
将提取的信息存储到 Obsidian 并生成日历事件数据
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

OBSIDIAN_CONFIG_PATH = os.path.expanduser("~/Library/Application Support/obsidian/obsidian.json")

def detect_obsidian_vaults():
    """检测 Obsidian vault 列表"""
    if not os.path.exists(OBSIDIAN_CONFIG_PATH):
        return []
    
    try:
        with open(OBSIDIAN_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        vaults = []
        for vault_id, vault_info in config.get('vaults', {}).items():
            vaults.append({
                'id': vault_id,
                'path': vault_info.get('path', ''),
                'open': vault_info.get('open', False),
                'ts': vault_info.get('ts', 0)
            })
        
        return vaults
    except Exception as e:
        print(f"⚠️ 无法读取 Obsidian 配置: {e}", file=sys.stderr)
        return []

def select_vault(vaults):
    """选择合适的 vault"""
    if not vaults:
        return None
    
    # 优先返回当前打开的 vault
    for v in vaults:
        if v['open']:
            return v['path']
    
    # 如果只有一个，直接使用
    if len(vaults) == 1:
        return vaults[0]['path']
    
    # 多个 vault，列出让用户选择
    print("找到多个 Obsidian vault：")
    for i, v in enumerate(vaults):
        status = " (当前打开)" if v['open'] else ""
        print(f"  {i+1}. {v['path']}{status}")
    
    while True:
        try:
            choice = input("请选择 (输入编号): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(vaults):
                return vaults[idx]['path']
        except ValueError:
            pass
        print("无效输入，请重新选择")

def create_obsidian_note(title: str, content: str, category: str, 
                         obsidian_path: str) -> str:
    """创建 Obsidian 笔记"""
    # 创建分类目录
    category_path = os.path.join(obsidian_path, category)
    os.makedirs(category_path, exist_ok=True)
    
    # 生成文件名（移除非法字符）
    safe_title = re.sub(r'[^\w\s\-\u4e00-\u9fff]', '', title)[:50]
    filename = f"{datetime.now().strftime('%Y%m%d')}_{safe_title}.md"
    filepath = os.path.join(category_path, filename)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def generate_obsidian_todo_template(todos: List[Dict]) -> str:
    """生成待办事项 Obsidian 笔记模板"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    content = f"""---
type: wechat-todo
source: {todos[0]['chat'] if todos else '未知'}
created: {now}
tags: [微信, 待办]
---

# 微信待办事项

> 从微信聊天记录中提取的待办事项

## 提取时间
{now}

## 待办清单

"""
    
    for i, todo in enumerate(todos, 1):
        content += f"- [ ] **{todo.get('sender', '未知')}**: {todo.get('content', '')}\n"
        content += f"  - 来源: {todo.get('chat', '')} | {todo.get('time', '')}\n\n"
    
    return content

def copy_wechat_attachments(chat_name: str, obsidian_path: str, category: str):
    """从微信本地文件夹复制附件到 Obsidian"""
    wechat_base = os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/")
    
    # 查找所有文件
    all_files = []
    for root, dirs, files in os.walk(wechat_base):
        for file in files:
            if file.endswith(('.pdf', '.docx', '.epub', '.mp3', '.txt')):
                all_files.append(os.path.join(root, file))
    
    if not all_files:
        print("⚠️ 未在微信本地文件夹中找到文件")
        return
    
    # 创建目标目录
    target_dir = os.path.join(obsidian_path, category)
    os.makedirs(target_dir, exist_ok=True)
    
    # 复制文件（这里需要根据聊天记录来确定具体文件）
    print(f"📁 找到 {len(all_files)} 个文件，请手动筛选需要复制的文件")
    print(f"建议手动复制文件到: {target_dir}")

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else 'help'
    
    if action == 'help':
        print("""
微信信息存储脚本（支持 Obsidian vault 自动检测）

用法:
    python save_to_obsidian.py todos < data.json
    python save_to_obsidian.py meetings < data.json
    python save_to_obsidian.py calendar < data.json
    python save_to_obsidian.py copy-attachments "群名" "分类"

示例:
    # 提取并存储待办
    wechat-cli history "联系人" --limit 100 --format json | python extract_key_info.py | python save_to_obsidian.py todos
    
    # 生成日历事件
    wechat-cli search "会议" --format json | python extract_key_info.py | python save_to_obsidian.py calendar
    
    # 复制微信附件到 Obsidian
    python save_to_obsidian.py copy-attachments "FDSM复二代俱乐部-9群" "幼儿教育"
""")
        return
    
    # 自动检测 Obsidian vault
    print("🔍 检测 Obsidian vault...")
    vaults = detect_obsidian_vaults()
    obsidian_path = select_vault(vaults)
    
    if not obsidian_path:
        obsidian_path = input("请输入 Obsidian 库路径 (默认: ~/Documents/obsidian): ").strip() or "~/Documents/obsidian"
        obsidian_path = os.path.expanduser(obsidian_path)
    
    print(f"✅ 使用 Obsidian vault: {obsidian_path}")
    
    if action == 'copy-attachments':
        chat_name = sys.argv[2] if len(sys.argv) > 2 else ''
        category = sys.argv[3] if len(sys.argv) > 3 else '微信附件'
        copy_wechat_attachments(chat_name, obsidian_path, category)
        return
    
    # 从 stdin 读取提取的数据
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("错误: 无法解析 JSON 数据", file=sys.stderr)
        sys.exit(1)
    
    if action == 'todos':
        todos = data.get('todos', [])
        if not todos:
            print("未找到待办事项")
            return
        
        content = generate_obsidian_todo_template(todos)
        filepath = create_obsidian_note("微信待办汇总", content, "待办事项", obsidian_path)
        print(f"✅ 已创建笔记: {filepath}")
        
    elif action == 'meetings':
        meetings = data.get('dates', [])
        if not meetings:
            print("未找到会议信息")
            return
        
        content = generate_obsidian_todo_template(meetings)  # 这里应该用 meeting 模板
        filepath = create_obsidian_note("微信会议备忘", content, "会议记录", obsidian_path)
        print(f"✅ 已创建笔记: {filepath}")
        
    elif action == 'calendar':
        dates = data.get('dates', [])
        if not dates:
            print("未找到时间相关事项")
            return
        
        events = []
        for item in dates:
            event = {
                'title': item.get('content', '')[:50],
                'time': item.get('time', ''),
                'chat': item.get('chat', ''),
                'sender': item.get('sender', '')
            }
            events.append(event)
        
        print(json.dumps(events, ensure_ascii=False, indent=2))
        print("\n📅 日历事件数据已生成")
        
    else:
        print(f"未知操作: {action}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
