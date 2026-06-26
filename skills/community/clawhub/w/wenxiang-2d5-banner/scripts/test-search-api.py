#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test RAG Search API"""

import sys
sys.path.insert(0, 'skills')

from rag_search.src.search import search_memories

print("=" * 60)
print("Testing RAG Search API")
print("=" * 60)

test_queries = ["瀑布", "TTS", "memory", "Aliyun"]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    results = search_memories(query, k=3)
    
    if results:
        print(f"  Found {len(results)} results:")
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['source']}] sim={r['similarity']}")
    else:
        print("  No results found")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
