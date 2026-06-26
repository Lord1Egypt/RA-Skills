#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test auto_trigger with debug output"""

import sys
sys.path.insert(0, r"C:\Users\Xiabi\.openclaw\workspace\skills\rag_search\src")

from auto_trigger import should_trigger_search, extract_search_query, search_and_format

msg = "我之前说过瀑布的事情吗？"
print(f"Message: {msg}")

# Step 1
trigger = should_trigger_search(msg)
print(f"Trigger: {trigger}")

if trigger:
    # Step 2
    query = extract_search_query(msg)
    print(f"Query: '{query}'")
    
    # Step 3
    results = search_and_format(query, k=3)
    print(f"Results length: {len(results)}")
    if results:
        print("SUCCESS!")
        print(results[:300])
    else:
        print("No results")
        
        # Try direct search
        from search import search_memories
        direct_results = search_memories("瀑布", k=3)
        print(f"Direct search '瀑布': {len(direct_results)} results")
