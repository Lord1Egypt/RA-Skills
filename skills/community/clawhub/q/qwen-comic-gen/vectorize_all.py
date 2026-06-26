#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量化所有文档脚本
- 读取技能文档、MEMORY.md、memory 文件
- 调用阿里云 Embedding API 生成向量
- 存入 ChromaDB
"""

import os
import sys
import hashlib
from pathlib import Path
from openai import OpenAI
import chromadb
from chromadb.config import Settings
import chardet

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置
WORKSPACE = Path(r"C:\Users\Xiabi\.openclaw\workspace")
CHROMA_PATH = WORKSPACE / "chroma_db"
API_KEY = 'sk-1f3847debc3e492e81f64115b20c6d82'
BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
MODEL = 'text-embedding-v3'
CHUNK_SIZE = 800  # 每段字符数
CHUNK_OVERLAP = 100  # 重叠字符数

# 初始化 OpenAI 客户端（阿里云兼容）
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 初始化 ChromaDB
chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = chroma_client.get_or_create_collection(
    name="openclaw_memory",
    metadata={"hnsw:space": "cosine"}
)

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result['encoding'] or 'utf-8'

def read_file_safe(file_path):
    """安全读取文件，自动检测编码"""
    try:
        # 先尝试 UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 检测编码并重试
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """将文本分块"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start >= len(text):
            break
    return chunks

def get_embedding(text):
    """获取文本的向量嵌入"""
    try:
        response = client.embeddings.create(
            model=MODEL,
            input=[text]
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding 错误：{e}")
        return None

def generate_id(text):
    """生成唯一 ID"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def vectorize_file(file_path, doc_type):
    """向量化单个文件"""
    print(f"处理：{file_path}")
    
    try:
        content = read_file_safe(file_path)
        if not content or len(content.strip()) == 0:
            print(f"  ⚠️ 空文件，跳过")
            return 0
        
        chunks = chunk_text(content)
        print(f"  分成 {len(chunks)} 个片段")
        
        count = 0
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # 跳过太短的片段
                continue
            
            embedding = get_embedding(chunk)
            if embedding:
                doc_id = generate_id(f"{file_path}:{i}")
                collection.upsert(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        "source": str(file_path),
                        "doc_type": doc_type,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }]
                )
                count += 1
        
        print(f"  ✅ 向量化 {count} 个片段")
        return count
    except Exception as e:
        print(f"  ❌ 错误：{e}")
        return 0

def main():
    print("🦞 虾虾的向量化工作开始！✨")
    print("=" * 60)
    
    total_chunks = 0
    files_processed = 0
    
    # 1. 向量化技能文档
    print("\n📚 第一部分：技能文档向量化")
    print("-" * 60)
    skills_dir = WORKSPACE / "skills"
    if skills_dir.exists():
        skill_files = list(skills_dir.rglob("SKILL.md"))
        print(f"找到 {len(skill_files)} 个技能文档")
        for file_path in skill_files:
            chunks = vectorize_file(file_path, "skill")
            total_chunks += chunks
            files_processed += 1
    
    # 2. 向量化 MEMORY.md
    print("\n🧠 第二部分：MEMORY.md 向量化")
    print("-" * 60)
    memory_file = WORKSPACE / "MEMORY.md"
    if memory_file.exists():
        chunks = vectorize_file(memory_file, "memory_main")
        total_chunks += chunks
        files_processed += 1
    
    # 3. 向量化 memory/*.md 文件
    print("\n📝 第三部分：memory 文件向量化")
    print("-" * 60)
    memory_dir = WORKSPACE / "memory"
    if memory_dir.exists():
        memory_files = list(memory_dir.glob("*.md"))
        print(f"找到 {len(memory_files)} 个 memory 文件")
        for file_path in memory_files:
            chunks = vectorize_file(file_path, "memory_daily")
            total_chunks += chunks
            files_processed += 1
    
    # 4. 向量化 worklog.txt（如果有）
    print("\n📋 第四部分：worklog.txt 向量化")
    print("-" * 60)
    worklog_file = WORKSPACE / "worklog.txt"
    if worklog_file.exists():
        chunks = vectorize_file(worklog_file, "worklog")
        total_chunks += chunks
        files_processed += 1
    else:
        print("  ⚠️ worklog.txt 不存在，跳过")
    
    # 统计
    print("\n" + "=" * 60)
    print("🎉 向量化完成！")
    print(f"  处理文件数：{files_processed}")
    print(f"  总片段数：{total_chunks}")
    print(f"  向量维度：1024")
    print(f"  存储位置：{CHROMA_PATH}")
    print("=" * 60)
    
    # 测试查询
    print("\n🧪 测试向量查询...")
    test_queries = [
        "如何开通飞书文档权限",
        "Mermaid 图表生成流程",
        "SOUL.md 文件位置"
    ]
    
    for query in test_queries:
        print(f"\n  查询：'{query}'")
        query_embedding = get_embedding(query)
        if query_embedding:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3
            )
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0][:2]):
                    source = results['metadatas'][0][i]['source']
                    print(f"    [{i+1}] {source[:50]}...")
                    print(f"        {doc[:100]}...")
    
    print("\n✨ 虾虾的向量化工作全部完成！哼～")

if __name__ == "__main__":
    main()
