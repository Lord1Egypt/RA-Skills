#!/usr/bin/env python3
"""实战 58 Deep Research 简版 (2026-06-16)
- 3 步: 主 search + LLM 拆 3 子问题 + 3 子 search + LLM 综合
- 端到端 20-30s
- 端点: POST /v1/deep_research {query}
"""
import os
import json
import time
import asyncio
import urllib.request
import urllib.error
from typing import List, Dict, Optional
from pathlib import Path

LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.token-star.cn/v1')
LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
LLM_MODEL = os.environ.get('LLM_MODEL', 'DeepSeek-V4-Flash')
LLM_TIMEOUT = int(os.environ.get('LLM_TIMEOUT', '25'))

# 兼容从 /home/ubuntu/star-search/.env 读
_env_path = Path('/home/ubuntu/star-search/.env')
if _env_path.exists():
    try:
        with open(_env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, _, v = line.partition('=')
                    k = k.strip()
                    v = v.strip()
                    if k == 'LLM_BASE_URL' and v and LLM_BASE_URL == 'https://api.token-star.cn/v1':
                        LLM_BASE_URL = v
                    elif k == 'LLM_API_KEY' and v:
                        LLM_API_KEY = v
                    elif k == 'LLM_MODEL' and v:
                        LLM_MODEL = v
                    elif k == 'LLM_TIMEOUT' and v:
                        try:
                            LLM_TIMEOUT = int(v)
                        except: pass
    except Exception:
        pass

def _call_llm(messages: List[Dict], max_tokens: int = 800) -> Optional[str]:
    """同步 LLM 调用 (OpenAI 兼容)"""
    body = json.dumps({
        'model': LLM_MODEL,
        'messages': messages,
        'max_tokens': max_tokens,
        'temperature': 0.3,
    }).encode()
    req = urllib.request.Request(
        f'{LLM_BASE_URL}/chat/completions',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LLM_API_KEY}',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT) as resp:
            data = json.loads(resp.read())
            return data['choices'][0]['message']['content']
    except Exception as e:
        return f'LLM_ERROR: {e}'

def _run_search_subprocess(query: str, top: int = 5) -> List[Dict]:
    """独立进程跑 search (避免 event loop 冲突)"""
    env = dict(os.environ)
    env['PYTHONPATH'] = '/home/ubuntu/.local/lib/python3.10/site-packages'
    try:
        proc = subprocess.run(
            ['/usr/bin/python3', '/home/ubuntu/star-search/scripts/search_runner.py',
             json.dumps({'query': query, 'top': top})],
            capture_output=True, text=True, timeout=30, env=env
        )
        last = proc.stdout.strip().split('\n')[-1] if proc.stdout.strip() else '{}'
        out = json.loads(last)
        return out.get('results', [])
    except Exception as e:
        return [{'title': 'search error', 'summary': str(e), 'url': ''}]

import subprocess

def decompose_to_subqueries(query: str, main_results: List[Dict]) -> List[str]:
    """实战 58: LLM 拆 3 个子问题
    返回: list of str (3 子问题)
    """
    # 准备上下文: 主 query + top 3 结果标题
    context = '\n'.join([
        f"- [{i+1}] {r.get('title', '?')}: {(r.get('summary', '') or '')[:80]}"
        for i, r in enumerate(main_results[:3])
    ])
    prompt = f"""你是一个研究助手。用户主问题: {query}

已有初步搜索结果:
{context}

请基于已有结果, 拆出 3 个深入研究的子问题 (子问题应该更具体、更深入)。
每个子问题一行, 不要编号, 不要其他说明。

子问题:"""
    content = _call_llm([
        {'role': 'user', 'content': prompt}
    ], max_tokens=200)
    if not content or 'LLM_ERROR' in str(content):
        # fallback: 用 query 本身 + 一些变体
        return [f'{query} 详细', f'{query} 对比', f'{query} 最新进展']
    # 解析: 3 行
    sub_queries = [line.strip().lstrip('0123456789.。- ').strip()
                   for line in content.split('\n') if line.strip()]
    sub_queries = [q for q in sub_queries if len(q) > 4][:3]
    while len(sub_queries) < 3:
        sub_queries.append(f'{query} 补充 {len(sub_queries)+1}')
    return sub_queries[:3]

def synthesize_report(query: str, main_results: List[Dict], sub_queries: List[str],
                     sub_results_list: List[List[Dict]]) -> Dict:
    """实战 58: LLM 综合所有结果
    返回: {summary, key_points, sources}
    """
    # 拼所有结果 + 引用编号
    sources = []
    source_idx = 0
    sections = []
    sections.append('## 主问题搜索结果')
    for r in main_results[:5]:
        source_idx += 1
        sources.append({
            'index': source_idx,
            'title': r.get('title', ''),
            'url': r.get('url', ''),
            'summary': r.get('summary', '') or '',
        })
        sections.append(f"[{source_idx}] {r.get('title', '')}: {(r.get('summary', '') or '')[:120]}")
    for i, (sq, srs) in enumerate(zip(sub_queries, sub_results_list)):
        sections.append(f'\n## 子问题 {i+1}: {sq}')
        for r in srs[:3]:
            source_idx += 1
            sources.append({
                'index': source_idx,
                'title': r.get('title', ''),
                'url': r.get('url', ''),
                'summary': r.get('summary', '') or '',
            })
            sections.append(f"[{source_idx}] {r.get('title', '')}: {(r.get('summary', '') or '')[:120]}")

    context = '\n'.join(sections)
    prompt = f"""你是一个研究助手。基于以下搜索结果, 综合深度研究报告。

主问题: {query}

搜索结果 (含引用编号):
{context}

要求:
1. 200-400 字综合答案
2. 标注引用编号 (用 [N] 格式)
3. 列 3-5 个关键点
4. 客观中立, 跨源对比

请按这个 JSON 格式返回 (不要其他说明文字):
{{
  "summary": "综合答案 (200-400 字, 包含 [N] 引用)",
  "key_points": ["关键点1", "关键点2", "关键点3"]
}}"""
    content = _call_llm([
        {'role': 'user', 'content': prompt}
    ], max_tokens=1000)
    # 解析 JSON
    try:
        # 尝试提取 JSON 块
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()
        result = json.loads(content)
    except Exception:
        result = {
            'summary': content if content else 'LLM 综合失败',
            'key_points': [],
        }
    result['sources'] = sources
    result['sub_queries'] = sub_queries
    return result

def deep_research(query: str) -> Dict:
    """实战 58: 3 步 Deep Research
    Step 1: 主 search (top 5)
    Step 2: LLM 拆 3 子问题 + 3 子 search
    Step 3: LLM 综合报告
    """
    t0 = time.time()
    steps = []
    # Step 1: 主 search
    t1 = time.time()
    main_results = _run_search_subprocess(query, top=5)
    steps.append({
        'step': 1,
        'name': 'main_search',
        'query': query,
        'result_count': len(main_results),
        'elapsed_ms': int((time.time() - t1) * 1000),
    })
    if not main_results:
        return {'error': 'no main results', 'query': query, 'steps': steps}

    # Step 2: 拆子问题 + 子 search
    t2 = time.time()
    sub_queries = decompose_to_subqueries(query, main_results)
    sub_results_list = []
    for sq in sub_queries:
        srs = _run_search_subprocess(sq, top=3)
        sub_results_list.append(srs)
    steps.append({
        'step': 2,
        'name': 'sub_search',
        'sub_queries': sub_queries,
        'sub_result_counts': [len(srs) for srs in sub_results_list],
        'elapsed_ms': int((time.time() - t2) * 1000),
    })

    # Step 3: LLM 综合
    t3 = time.time()
    report = synthesize_report(query, main_results, sub_queries, sub_results_list)
    steps.append({
        'step': 3,
        'name': 'synthesize',
        'elapsed_ms': int((time.time() - t3) * 1000),
    })

    return {
        'query': query,
        'sub_queries': sub_queries,
        'main_result_count': len(main_results),
        'sub_result_counts': [len(srs) for srs in sub_results_list],
        'summary': report.get('summary', ''),
        'key_points': report.get('key_points', []),
        'sources': report.get('sources', []),
        'steps': steps,
        'elapsed_ms': int((time.time() - t0) * 1000),
    }
