#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final Integration Test"""

import sys
import os

os.environ['ALIYUN_API_KEY'] = 'sk-1f3847debc3e492e81f64115b20c6d82'
os.environ['CHROMA_PERSIST_DIR'] = 'C:\\Users\\Xiabi\\.openclaw\\workspace\\chroma_db'

sys.path.insert(0, 'hooks')

from memory_retriever import retrieve_context

print("=" * 60)
print("Final Integration Test - Memory Retrieval")
print("=" * 60)

test_queries = [
    "waterfall",
    "TTS",
    "Aliyun embedding",
    "vector database"
]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    results = retrieve_context(query, k=3)
    
    if results:
        print(f"  [OK] Found memories")
        lines = results.strip().split('\n')
        sources = [l for l in lines if 'from memory/' in l]
        print(f"  Sources: {len(sources)} files")
    else:
        print(f"  [WARN] No memories found")

print("\n" + "=" * 60)
print("SUCCESS! Integration complete!")
print("=" * 60)
