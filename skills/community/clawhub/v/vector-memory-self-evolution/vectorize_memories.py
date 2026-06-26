#!/usr/bin/env python3
"""
记忆向量化脚本 - 将 L2/L3 记忆向量化到 L4 向量库
"""
import os
import json
import chromadb
from pathlib import Path
from datetime import datetime
import requests

# 路径配置
WORKSPACE = Path.home() / '.openclaw/workspace'
MEMORY_DIR = WORKSPACE / 'memory'
VECTOR_DB_DIR = WORKSPACE / 'vector_db'

def get_embedding(text):
    """获取 BGE 向量"""
    try:
        response = requests.post(
            'http://localhost:11434/api/embeddings',
            json={
                'prompt': text  # BGE 服务使用 prompt 字段
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()['embedding']
    except Exception as e:
        print(f"❌ 获取向量失败: {e}")
        return None

def vectorize_memories():
    """向量化所有记忆"""
    print("🚀 开始向量化记忆...")
    
    # 确保向量库目录存在
    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # 初始化 Chroma
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    
    # 创建集合
    try:
        collection = client.get_collection("memories")
        print("✅ 使用现有向量库")
    except:
        collection = client.create_collection("memories")
        print("✅ 创建新向量库")
    
    # 收集所有记忆
    all_memories = []
    
    # 1. 从日期文件收集
    for md_file in sorted(MEMORY_DIR.glob("*.md")):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 entries
        entries = content.split('---\n')
        
        for entry in entries:
            if not entry.strip():
                continue
            
            # 简单解析
            lines = entry.strip().split('\n')
            metadata = {}
            body_lines = []
            
            in_header = False
            for line in lines:
                if line.startswith('---'):
                    in_header = not in_header
                    continue
                if in_header and ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
                else:
                    body_lines.append(line)
            
            if body_lines:
                all_memories.append({
                    'text': '\n'.join(body_lines),
                    'metadata': {
                        **metadata,
                        'source': md_file.name,
                        'vectorized_at': datetime.now().isoformat()
                    }
                })
    
    # 2. 向量化并存储
    print(f"📝 共发现 {len(all_memories)} 条记忆")
    
    success_count = 0
    for i, memory in enumerate(all_memories):
        print(f"⏳ 向量化 {i+1}/{len(all_memories)}: {memory['text'][:50]}...")
        
        embedding = get_embedding(memory['text'])
        if embedding is None:
            continue
        
        try:
            collection.add(
                documents=[memory['text']],
                embeddings=[embedding],
                metadatas=[memory['metadata']],
                ids=[f"memory_{i}_{datetime.now().timestamp()}"]
            )
            success_count += 1
        except Exception as e:
            print(f"⚠️  存储失败: {e}")
    
    print(f"\n✅ 向量化完成！成功处理 {success_count}/{len(all_memories)} 条记忆")
    print(f"📦 向量库位置: {VECTOR_DB_DIR}")

if __name__ == '__main__':
    vectorize_memories()