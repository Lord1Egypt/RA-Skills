#!/usr/bin/env python3
"""实战 57: search 独立 runner (multimodal 用, 避免 event loop 冲突)"""
import sys
import json
import asyncio
sys.path.insert(0, '/home/ubuntu/star-search/scripts')

def run():
    arg = json.loads(sys.argv[1])
    query = arg['query']
    top = arg.get('top', 8)
    import search as _s
    loop = asyncio.new_event_loop()
    try:
        out = loop.run_until_complete(_s.search_async(query, top=top))
    finally:
        loop.close()
    # 统一格式
    if isinstance(out, dict):
        results = out.get('results', [])
    else:
        results = out if isinstance(out, list) else []
    print(json.dumps({'results': results, 'count': len(results)}, ensure_ascii=False))

if __name__ == '__main__':
    run()
