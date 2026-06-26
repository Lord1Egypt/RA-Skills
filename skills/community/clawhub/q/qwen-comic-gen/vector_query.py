#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量查询集成模块
- 在回答前查询 ChromaDB 获取相关上下文
- 将相关片段作为上下文提供给 LLM
"""

import sys
import io
from pathlib import Path
from openai import OpenAI
import chromadb

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置
WORKSPACE = Path(r"C:\Users\Xiabi\.openclaw\workspace")
CHROMA_PATH = WORKSPACE / "chroma_db"
API_KEY = 'sk-1f3847debc3e492e81f64115b20c6d82'
BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
MODEL = 'text-embedding-v3'

# 初始化
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = chroma_client.get_collection("openclaw_memory")

def get_embedding(text):
    """获取文本向量"""
    response = client.embeddings.create(model=MODEL, input=[text])
    return response.data[0].embedding

def search_similar(query, n_results=5):
    """搜索相似片段"""
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return results

def format_context(results):
    """格式化上下文"""
    context_parts = []
    if results and results['documents']:
        for i, (doc, meta, dist) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            source = Path(meta['source']).name
            context_parts.append(f"[来源：{source}] {doc.strip()}")
    return "\n\n---\n\n".join(context_parts)

def query_knowledge(user_question):
    """主查询函数"""
    print(f"🔍 查询：{user_question}")
    results = search_similar(user_question, n_results=5)
    context = format_context(results)
    print(f"📚 找到 {len(results['documents'][0]) if results and results['documents'] else 0} 个相关片段")
    return context

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        context = query_knowledge(query)
        print("\n" + "="*60)
        print("相关上下文:")
        print("="*60)
        print(context[:2000] if len(context) > 2000 else context)
    else:
        print("用法：python vector_query.py <查询内容>")
