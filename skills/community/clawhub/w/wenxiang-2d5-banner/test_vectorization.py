# -*- coding: utf-8 -*-
"""测试向量化搜索结果"""
import os
import sys
import requests
import chromadb
from chromadb.config import Settings

# 配置
WORKSPACE = r"C:\Users\Xiabi\.openclaw\workspace"
CHROMA_DB_PATH = os.path.join(WORKSPACE, "chroma_db")
ALIYUN_API_KEY = "sk-1f3847debc3e492e81f64115b20c6d82"
ALIYUN_EMBEDDING_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

def get_embedding(text):
    """获取向量"""
    headers = {
        "Authorization": f"Bearer {ALIYUN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "text-embedding-v2",
        "input": {"texts": [text]}
    }
    
    response = requests.post(ALIYUN_EMBEDDING_URL, headers=headers, json=payload, timeout=30)
    result = response.json()
    
    if "output" in result and "embeddings" in result["output"]:
        return result["output"]["embeddings"][0]["embedding"]
    else:
        raise Exception(f"API 错误：{result}")

# 初始化 Chroma
print("=" * 60)
print("向量化结果验证")
print("=" * 60)

client = chromadb.PersistentClient(path=CHROMA_DB_PATH, settings=Settings(anonymized_telemetry=False))
collection = client.get_collection("memory_vectors")

# 统计信息
total_count = collection.count()
print(f"\n向量总数：{total_count}")

# 获取集合元数据
print(f"集合名称：memory_vectors")

# 测试搜索
test_queries = [
    "Thomas 的偏好是什么",
    "供应商直连系统进度",
    "技能选择原则",
    "阿香角色设定"
]

print("\n" + "=" * 60)
print("搜索功能测试")
print("=" * 60)

for query in test_queries:
    print(f"\n搜索：'{query}'")
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )
    
    if results and results['documents'] and results['documents'][0]:
        for i, (doc, meta, dist) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            preview = doc[:150].replace('\n', ' ').strip()
            print(f"  [{i+1}] {meta['source_file']} (相似度：{1-dist:.3f})")
            print(f"      {preview}...")
    else:
        print("  无结果")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
