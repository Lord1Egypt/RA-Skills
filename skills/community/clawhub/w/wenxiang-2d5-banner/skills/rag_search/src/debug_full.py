#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug full auto_search flow"""

import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, r"C:\Users\Xiabi\.openclaw\workspace\skills\rag_search\src")

MEMORY_KEYWORDS = [
    "之前说过", "之前提过", "之前讲过", "之前提到",
    "我记得", "我有印象", "我好像说过",
    "上次", "上上次", "上一次",
    "之前", "从前", "说过", "提过", "讲过",
]

MEMORY_PATTERN = re.compile('|'.join(re.escape(kw) for kw in MEMORY_KEYWORDS))

def should_trigger_search(user_message: str) -> bool:
    if MEMORY_PATTERN.search(user_message):
        return True
    return False

def extract_search_query(user_message: str) -> str:
    query = user_message
    query = re.sub(r'[吗？?]', '', query)
    fillers = ["我", "你", "他", "她", "它", "的", "了", "过", "吗", "呢", "吧", "啊", "呀"]
    for filler in fillers:
        query = query.replace(filler, '')
    if len(query) > 30:
        query = query[-30:]
    return query.strip()

msg = "我之前说过瀑布的事情吗？"
print(f"Message: {msg}")

# Step 1: Check trigger
trigger = should_trigger_search(msg)
print(f"Step 1 - Should trigger: {trigger}")

if not trigger:
    print("STOP: Not triggered")
    sys.exit(0)

# Step 2: Extract query
query = extract_search_query(msg)
print(f"Step 2 - Extracted query: '{query}' (length: {len(query)})")

if not query or len(query) < 2:
    print("STOP: Query too short")
    sys.exit(0)

# Step 3: Search
print("Step 3 - Searching...")
from search import search_memories
results = search_memories(query, k=3)
print(f"Found {len(results)} results")

if not results:
    print("STOP: No results")
    sys.exit(0)

print("SUCCESS!")
for i, r in enumerate(results):
    source = r['source'].split('\\')[-1]
    print(f"{i+1}. {source} - sim:{r['similarity']}")
