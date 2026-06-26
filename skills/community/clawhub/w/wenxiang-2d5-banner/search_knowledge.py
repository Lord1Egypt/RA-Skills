#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge 知识库搜索工具
- 从 openclaw_knowledge 集合搜索
- 支持自定义查询和返回数量
"""

import sys
import io
from pathlib import Path

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from openai import OpenAI
import chromadb

# 配置
WORKSPACE = Path(r"C:\Users\Xiabi\.openclaw\workspace")
CHROMA_PATH = WORKSPACE / "chroma_db"
API_KEY = 'sk-1f3847debc3e492e81f64115b20c6d82'
BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
MODEL = 'text-embedding-v3'

# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = chroma_client.get_collection('openclaw_knowledge')

def get_embedding(text):
    """获取向量"""
    response = client.embeddings.create(model=MODEL, input=[text])
    return response.data[0].embedding

def search_knowledge(query, k=3):
    """搜索知识库"""
    print(f"\n🔍 搜索：'{query}' (top {k})\n")
    
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    if results and results['documents']:
        for i, doc in enumerate(results['documents'][0]):
            source = results['metadatas'][0][i]['source']
            doc_type = results['metadatas'][0][i]['doc_type']
            print(f"【{i+1}】来源：{source}")
            print(f"    类型：{doc_type}")
            print(f"    内容：{doc[:300]}...\n")
        
        return results
    else:
        print("未找到结果")
        return []

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:-1]) if sys.argv[-1].isdigit() else " ".join(sys.argv[1:])
        k = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 3
        search_knowledge(query, k)
    else:
        # 交互式搜索
        print("🦞 虾虾的知识库搜索工具！输入 query 开始搜索（输入 q 退出）\n")
        while True:
            query = input("搜索：").strip()
            if query.lower() in ['q', 'quit', 'exit']:
                break
            if query:
                search_knowledge(query, 3)
