#!/usr/bin/env python3
"""
记忆 API - 统一的记忆操作接口
"""
import json
import datetime
from pathlib import Path
import os
import chromadb

# 设置环境变量

# 路径配置
WORKSPACE = Path.home() / '.openclaw/workspace'
MEMORY_DIR = WORKSPACE / 'memory'
VECTOR_DB_DIR = WORKSPACE / 'vector_db'

def capture(typ, title, content, context=''):
    """捕获记忆到 L2"""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = MEMORY_DIR / f"{today}.md"
    timestamp = datetime.datetime.now().isoformat()
    
    entry = f"""---
type: {typ}
timestamp: {timestamp}
title: {title}
context: {context}
---

{content}

---
"""
    
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    print(f"✅ Captured {typ}: {title}")
    return True

def search(query, typ=None, n_results=5):
    """语义搜索记忆"""
    if not VECTOR_DB_DIR.exists():
        print("❌ 向量库不存在，请先运行向量化脚本")
        return []
    
    try:
        client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        collection = client.get_collection("memories")
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return []

def check_before_execute(command):
    """执行前检查记忆"""
    print(f"\n🔍 检查命令: {command}")
    
    # 检查各类记忆
    for typ in ['errors', 'corrections', 'practices']:
        type_dir = MEMORY_DIR / typ
        if not type_dir.exists():
            continue
        
        for md_file in sorted(type_dir.glob("*.md"), reverse=True)[:3]:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 简单关键词匹配
            if any(word in content for word in command.split()):
                print(f"\n⚠️  发现相关 {typ.upper()}:")
                print(f"  文件: {md_file.name}")
                # 提取并显示前200字
                lines = content.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('-'):
                        print(f"  {line[:200]}...")
                        break

# 便捷函数
def capture_error(command, error, context='', suggested_fix=''):
    """捕获错误"""
    return capture('error', command, f"错误: {error}\n建议: {suggested_fix}", context)

def capture_correction(topic, wrong, correct, context=''):
    """捕获纠正"""
    return capture('correction', topic, f"错误做法: {wrong}\n正确做法: {correct}", context)

def capture_practice(category, practice, reason='', context=''):
    """捕获最佳实践"""
    return capture('practice', category, f"实践: {practice}\n原因: {reason}", context)

if __name__ == '__main__':
    import sys
    
    # 简单测试
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        check_before_execute(command)
    else:
        # 测试捕获
        capture_error("npm install", "permission denied", "全局安装", "使用 sudo")
        capture_correction("代码风格", "双引号", "单引号", "项目规范")
        capture_practice("高效安装", "pip install -e .", "可编辑模式", "Python开发")