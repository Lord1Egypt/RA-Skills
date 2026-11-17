#!/usr/bin/env python3
"""v20.51 standalone runner - 独立进程, 不与 uvicorn 共享 loop"""
import sys
import json
import asyncio
import urllib.request
import os
import time

def read_llm_config():
    base = 'https://api.<service-domain>/v1'
    key = ''
    model = 'glm-4-flash'
    timeout = 25
    env_path = '/home/ubuntu/star-search/.env'
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k == 'LLM_BASE_URL' and v: base = v
                elif k == 'LLM_API_KEY' and v: key = v
                elif k == 'LLM_MODEL' and v: model = v
                elif k == 'LLM_TIMEOUT' and v: timeout = int(v)
    return base.rstrip('/') + '/chat/completions', key, model, timeout

def run(query, mode, num):
    # 1) 调 search (独立 asyncio loop)
    import search as _search_mod
    loop = asyncio.new_event_loop()
    try:
        results = loop.run_until_complete(
            _search_mod.search_async(query, num=num, mode='auto')
        )
    finally:
        loop.close()
    if not results:
        return {'error': 'no results', 'query': query, 'mode': mode, 'result': ''}

    # 2) 格式化
    lines = []
    for i, r in enumerate(results[:num], 1):
        title = r.get('title', '')[:80]
        summary = r.get('summary', '')[:200]
        lines.append(f'[{i}] {title}\n    {summary}')
    results_text = '\n\n'.join(lines)

    # 3) prompt
    import discover as _d
    if mode not in _d.PROMPTS:
        return {'error': f'invalid mode: {mode}', 'query': query, 'mode': mode, 'result': ''}
    prompt = _d.PROMPTS[mode].format(query=query, num_results=num, results_text=results_text)

    # 4) LLM
    llm_url, llm_key, llm_model, llm_timeout = read_llm_config()
    req_data = {
        "model": llm_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 800,
    }
    req = urllib.request.Request(
        llm_url, data=json.dumps(req_data).encode(),
        headers={"Authorization": f"Bearer {llm_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=llm_timeout) as r:
        data = json.loads(r.read())
    llm_text = data['choices'][0]['message']['content'].strip()

    return {
        'query': query, 'mode': mode,
        'mode_doc': _d.MODES_DOC.get(mode, ''),
        'result': llm_text,
        'source_count': len(results),
        'cached': False,
    }

if __name__ == '__main__':
    arg = json.loads(sys.argv[1])
    out = run(arg['query'], arg['mode'], arg.get('num', 8))
    print(json.dumps(out, ensure_ascii=False))
