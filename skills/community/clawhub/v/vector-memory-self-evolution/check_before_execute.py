#!/usr/bin/env python3
"""
执行前记忆检查 - 避免重复错误
检查命令/操作相关的历史记忆（错误、纠正、最佳实践）
"""
import json
import chromadb
from pathlib import Path
import os

# 设置环境变量

# 路径配置
WORKSPACE = Path.home() / '.openclaw/workspace'
MEMORY_DIR = WORKSPACE / 'memory'
VECTOR_DB_DIR = WORKSPACE / 'vector_db'

def load_memory(typ, limit=10):
    """加载指定类型的记忆文件"""
    memories = []
    type_dir = MEMORY_DIR / typ
    if not type_dir.exists():
        return memories
    
    for md_file in sorted(type_dir.glob("*.md"), reverse=True)[:limit]:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 解析 YAML front matter
            entries = content.split('---\n')
            for entry in entries:
                if 'title:' in entry:
                    memories.append(entry)
    return memories

def search_vector_memory(query, typ=None, n_results=3):
    """使用 Chroma 向量库搜索"""
    if not VECTOR_DB_DIR.exists():
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
        print(f"向量搜索失败: {e}")
        return []

def check_before_execute(command):
    """执行命令前检查相关记忆"""
    print(f"\n🔍 检查命令: {command}")
    
    # 1. 检查错误记忆
    errors = load_memory('errors', limit=5)
    if errors:
        print("\n⚠️  发现相关错误记忆:")
        for err in errors:
            print(f"  {err[:200]}...")
    
    # 2. 检查纠正记忆
    corrections = load_memory('corrections', limit=5)
    if corrections:
        print("\n⚠️  发现相关纠正:")
        for corr in corrections:
            print(f"  {corr[:200]}...")
    
    # 3. 检查最佳实践
    practices = load_memory('practices', limit=5)
    if practices:
        print("\n✅ 发现最佳实践:")
        for prac in practices:
            print(f"  {prac[:200]}...")
    
    # 4. 向量语义搜索
    vector_results = search_vector_memory(command, n_results=3)
    if vector_results and vector_results.get('documents'):
        print("\n🔮 语义搜索结果:")
        for doc in vector_results['documents'][0]:
            print(f"  {doc[:200]}...")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        check_before_execute(command)
    else:
        print("用法: python3 check_before_execute.py <命令>")
        print("示例: python3 check_before_execute.py npm install xxx")