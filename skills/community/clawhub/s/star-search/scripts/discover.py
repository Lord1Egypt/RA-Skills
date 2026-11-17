#!/usr/bin/env python3
"""v20.51 P3-23 Perplexity 风格探索发现 (2026-06-15)"""
import os
import json
import time
import hashlib
import asyncio
import urllib.request
from typing import List, Dict

# ==================== 3 个 Prompt 模板 ====================

TIMELINE_PROMPT = """你是时间线整理助手. 任务: 根据用户 query 和提供的搜索结果, 整理一个清晰的时间线.

要求:
1. 时间倒序: 最新的事件在前, 旧的在后
2. 年份+月份: 每条都标日期 (YYYY-MM 或 YYYY)
3. 3-7 个关键节点: 不要超过 7 条
4. 每条 1-2 句: 简洁陈述事实
5. 来源标注: 重要事实标 [N], N 对应源序号

格式 (Markdown):
### 📅 时间线
- **YYYY-MM-DD** [1] 事件描述
- **YYYY-MM** [2] 事件描述
- ...

⚠️ 诚实原则:
- 搜索结果里没出现的时间点不编
- 模糊时间标 "近期" / "20XX年"
- 来源不够时建议查 [具体网站]

=== 用户 query ===
{query}

=== 搜索结果 (前 {num_results} 条) ===
{results_text}

输出 (只要时间线部分, 不要其他):"""

COMPARISON_PROMPT = """你是多角度对比助手. 任务: 根据用户 query 和搜索结果, 列出 3 个不同角度的观点.

要求:
1. 3 个角度: 支持 / 反对 / 中立 或 3 个具体维度
2. 每个角度 2-3 句: 简洁但有观点
3. 重要事实标 [N]: N 对应源序号
4. 不强行统一: 矛盾观点明确列出

格式 (Markdown):
### 🔍 多角度对比
**🟢 支持**:
- 观点 1 [1]
- 观点 2 [2]

**🔴 反对**:
- 观点 1 [3]

**🟡 中立/其他**:
- 观点 1

⚠️ 诚实原则:
- 搜索结果没覆盖的角度不编
- 来源不够时建议查 [具体网站]

=== 用户 query ===
{query}

=== 搜索结果 (前 {num_results} 条) ===
{results_text}

输出 (只要对比部分, 不要其他):"""

RELATED_PROMPT = """你是相关问题深挖助手. 任务: 根据用户 query 和搜索结果, 列出 6-9 个相关问题.

要求:
1. 3 类问题各 2-3 个:
   - 深挖: 顺着 query 往下挖细节
   - 横向: 同类对比
   - 纵向: 时间/因果
2. 每个问题 1 行: 不要 markdown 格式
3. 不超过 9 个: 多了用户体验差

格式 (纯文本, 每行 1 个):
- 问题 1
- 问题 2
...

=== 用户 query ===
{query}

=== 搜索结果 (前 {num_results} 条) ===
{results_text}

输出 (只要问题列表, 不要其他):"""

# ==================== 全局 ====================

PROMPTS = {
    'timeline': TIMELINE_PROMPT,
    'comparison': COMPARISON_PROMPT,
    'related': RELATED_PROMPT,
}

MODES_DOC = {
    'timeline': '时间线: 按时间倒序列出 3-7 个关键节点',
    'comparison': '多角度对比: 列出支持/反对/中立 3 个角度',
    'related': '相关问题深挖: 6-9 个 followup 问题',
}

_CACHE_DIR = os.path.expanduser("~/.star-search-cache/discover")
os.makedirs(_CACHE_DIR, exist_ok=True)


def _cache_key(query, mode, num):
    raw = f"{query}|{mode}|{num}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]


def _cache_get(key):
    path = os.path.join(_CACHE_DIR, f"{key}.json")
    if os.path.exists(path):
        try:
            with open(path) as f:
                d = json.load(f)
            if time.time() - d.get('ts', 0) < 1800:
                return d
        except Exception:
            pass
    return None


def _cache_put(key, data):
    data['ts'] = time.time()
    path = os.path.join(_CACHE_DIR, f"{key}.json")
    try:
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


def _read_llm_config():
    base = os.environ.get('LLM_BASE_URL', 'https://api.<service-domain>/v1')
    key = os.environ.get('LLM_API_KEY', '')
    model = os.environ.get('LLM_MODEL', 'glm-4-flash')
    timeout = int(os.environ.get('LLM_TIMEOUT', '25'))
    env_path = '/home/ubuntu/star-search/.env'
    if os.path.exists(env_path):
        try:
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    k, v = k.strip(), v.strip().strip('"').strip("'")
                    if k == 'LLM_BASE_URL' and v:
                        base = v
                    elif k == 'LLM_API_KEY' and v:
                        key = v
                    elif k == 'LLM_MODEL' and v:
                        model = v
                    elif k == 'LLM_TIMEOUT' and v:
                        timeout = int(v)
        except Exception:
            pass
    return base.rstrip('/') + '/chat/completions', key, model, timeout


def discover_sync(query, mode='timeline', num_results=8):
    """v20.51 final: 独立线程跑 asyncio loop, 避免 uvicorn uvloop 冲突"""
    import urllib.request
    import threading
    import time as _time
    t0 = _time.time()
    result_box = [None]
    def _runner():
        try:
            import search as _search_mod
            loop = asyncio.new_event_loop()
            try:
                result_box[0] = loop.run_until_complete(
                    _search_mod.search_async(query, num=num_results, mode='auto')
                )
            finally:
                loop.close()
        except Exception as e:
            result_box[0] = ('error', str(e))
    t = threading.Thread(target=_runner, daemon=True)
    t.start()
    t.join(timeout=30)
    if t.is_alive():
        return {'error': 'search timeout', 'query': query, 'mode': mode, 'result': ''}
    r = result_box[0]
    if isinstance(r, tuple) and r[0] == 'error':
        return {'error': f'search error: {r[1]}', 'query': query, 'mode': mode, 'result': ''}
    results = r or []
    if not results:
        return {'error': 'no results', 'query': query, 'mode': mode, 'result': ''}

    # 格式化
    lines = []
    for i, rr in enumerate(results[:num_results], 1):
        title = rr.get('title', '')[:80]
        summary = rr.get('summary', '')[:200]
        lines.append(f'[{i}] {title}\n    {summary}')
    results_text = '\n\n'.join(lines)

    if mode not in PROMPTS:
        return {'error': f'invalid mode: {mode}', 'query': query, 'mode': mode, 'result': ''}
    prompt = PROMPTS[mode].format(query=query, num_results=num_results, results_text=results_text)

    # LLM
    llm_url, llm_key, llm_model, llm_timeout = _read_llm_config()
    try:
        req_data = {"model": llm_model, "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3, "max_tokens": 800}
        req = urllib.request.Request(llm_url, data=json.dumps(req_data).encode(),
            headers={"Authorization": f"Bearer {llm_key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=llm_timeout) as rr:
            data = json.loads(rr.read())
        llm_text = data['choices'][0]['message']['content'].strip()
    except Exception as e:
        llm_text = f'[LLM error: {e}]'

    return {
        'query': query, 'mode': mode, 'mode_doc': MODES_DOC.get(mode, ''),
        'result': llm_text, 'source_count': len(results), 'cached': False,
        'elapsed_ms': int((_time.time() - t0) * 1000),
    }
