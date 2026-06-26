#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试向量搜索"""

import sys
import os
sys.path.insert(0, 'scripts')
os.environ['ALIYUN_API_KEY'] = 'sk-1f3847debc3e492e81f64115b20c6d82'

from index_user_preferences import AliyunEmbeddings
from langchain_chroma import Chroma

print("=" * 70)
print("Vector Search Test")
print("=" * 70)

# Load vector store
db = Chroma(
    persist_directory="chroma_db",
    collection_name="user_preferences",
    embedding_function=AliyunEmbeddings('sk-1f3847debc3e492e81f64115b20c6d82')
)

# Test queries
test_queries = [
    "视觉学习者 Mermaid 图表",
    "表情图片发送顺序",
    "供应商直连系统",
]

print(f"\n[Database Info]")
print(f"  Collection: user_preferences")
print(f"  Total vectors: {db._collection.count()}")

print(f"\n[Search Tests]")
for query in test_queries:
    print(f"\nQuery: '{query}'")
    results = db.similarity_search(query, k=3)
    
    if results:
        print(f"  ✅ Found {len(results)} results:")
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get("source", "Unknown")
            preview = doc.page_content[:100].replace("\n", " ")
            print(f"  {i}. [{source}] {preview}...")
    else:
        print(f"  ❌ No results found")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
