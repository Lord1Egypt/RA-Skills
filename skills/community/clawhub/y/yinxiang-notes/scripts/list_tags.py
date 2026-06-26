#!/usr/bin/env python3
"""
获取所有标签列表
"""

import sys
import os

# 手动计算路径
script_path = os.path.abspath(__file__)
scripts_dir = os.path.dirname(script_path)
skill_dir = os.path.dirname(scripts_dir)
skills_dir = os.path.dirname(skill_dir)
workspace_dir = os.path.dirname(skills_dir)
env_path = os.path.join(workspace_dir, '.env')

print(f"工作目录: {workspace_dir}")
print(f"ENV文件: {env_path}")
print(f"存在: {os.path.exists(env_path)}")

# 读取配置
token = None
note_store_url = None

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('EVERNOTE_TOKEN='):
                token = line.split('=', 1)[1].strip()
            elif line.startswith('EVERNOTE_NOTESTORE_URL='):
                note_store_url = line.split('=', 1)[1].strip()

print(f"Token: {token[:30] if token else 'None'}...")
print(f"URL: {note_store_url}")

import evernote.edam.notestore.NoteStore as NoteStore
import thrift.transport.THttpClient as THttpClient
import thrift.protocol.TBinaryProtocol as TBinaryProtocol


def list_tags():
    print("\n🔄 正在获取标签...")
    
    transport = THttpClient.THttpClient(note_store_url)
    transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    note_store = NoteStore.Client(protocol)

    # 获取标签
    tags = note_store.listTags(token)
    
    print(f"\n🏷️ 标签列表 (共 {len(tags)} 个):\n")
    
    # 按类型分组
    categories = {
        '状态/行动': [],
        '主题领域': [],
        '项目/产品': [],
        '其他': []
    }
    
    for tag in tags:
        name = tag.name
        if any(kw in name for kw in ['待办', 'TODO', '重要', '紧急', '草稿']):
            categories['状态/行动'].append(name)
        elif any(kw in name for kw in ['AI', 'Python', '投资', '产品', '技术']):
            categories['主题领域'].append(name)
        elif any(kw in name for kw in ['Smartb', '葡萄城', '微信']):
            categories['项目/产品'].append(name)
        else:
            categories['其他'].append(name)
    
    for cat, names in categories.items():
        if names:
            print(f"【{cat}】")
            for name in sorted(names):
                print(f"  • {name}")
            print()
    
    print(f"📊 统计: 共 {len(tags)} 个标签")
    
    return tags


if __name__ == '__main__':
    list_tags()
