#!/usr/bin/env python3
"""实战 63 multi_search (2026-06-16) - 多路并行搜索
- 调 super_brain.analyze_query 拿推荐引擎
- 并行 (asyncio.gather) 跑 2-3 个引擎
- 合并去重 (按 url + title jaccard)
- 保留 best N (按 score 排序)

设计:
- multi_search(query, top=10, use_brain=True) -> {results, brain_info, engines_used, elapsed_ms}
- backward compat: search() 仍支持单引擎
"""
import os
import sys
import time
import asyncio
import json
from typing import List, Dict, Optional
from pathlib import Path
from urllib.parse import urlparse

# 加入 scripts 目录
sys.path.insert(0, '/home/ubuntu/star-search/scripts')
sys.path.insert(0, os.path.dirname(__file__))

# 动态 import search (避免循环)
def _get_search_module():
    import search
    return search

# 引擎 → search engine 名字 映射
# 实战 74: 引擎白名单 (HTTP 引擎优先, playwright 引擎降级)
# playwright 引擎 (baidu/sogou/360/weixin) 需要 playwright 库, 没装时不可用
# 我们优先用 HTTP 引擎 (bing_cn/csdn/cnblogs/github/eastmoney/sina_finance/toutiao/zhihu)
HTTP_ENGINES = ['bing_cn', 'csdn', 'cnblogs', 'github', 'eastmoney', 'sina_finance', 'toutiao', 'zhihu', 'bing_www']

ENGINE_MAP = {
    'bing_cn': 'bing_cn',
    'bing_www': 'bing_www',
    'baidu': 'bing_www',  # 降级: 用 bing 搜 site:baidu
    'sogou': 'bing_www',  # 降级
    '360': 'bing_www',    # 降级
    'weixin': 'bing_www', # 降级
    'csdn': 'csdn',
    'cnblogs': 'cnblogs',
    'github': 'github',
    'eastmoney': 'eastmoney',
    'sina_finance': 'sina_finance',
    'taobao': 'bing_www',  # 降级
    'toutiao': 'toutiao',
    'zhihu': 'zhihu',
}


def _domain(url: str) -> str:
    try:
        d = urlparse(url).netloc.lower()
        if d.startswith('www.'):
            d = d[4:]
        return d
    except Exception:
        return ''


def _dedup_by_url(results: List[Dict]) -> List[Dict]:
    """实战 63: 按 url domain + 标题前缀去重"""
    seen_domains = set()
    seen_titles = set()
    out = []
    for r in results:
        u = r.get('url', '')
        d = _domain(u)
        title = (r.get('title', '') or '').strip()[:30]
        # 1) 完全相同 url
        if u in [x.get('url', '') for x in out]:
            continue
        # 2) 相同 domain + 相似标题 (前 20 字符)
        title_key = title[:20]
        if d and title_key:
            key = (d, title_key)
            if key in seen_domains:
                continue
            seen_domains.add(key)
        seen_titles.add(title)
        out.append(r)
    return out


async def _search_one(s, query: str, engine: str, num: int) -> List[Dict]:
    """实战 63: 跑一个引擎 (超快速失败)"""
    try:
        results = await asyncio.wait_for(
            s.search_async(query, engine=engine, num=num, mode='quick', force_refresh=False),
            timeout=15
        )
        return results or []
    except Exception as e:
        return [{'error': str(e), 'engine': engine}]


async def multi_search(query: str, top: int = 10, use_brain: bool = True,
                       max_engines: int = 3, max_retries: int = 3) -> Dict:
    """实战 63: 多路并行搜索
    1) super_brain.analyze_query → 推荐引擎
    2) 跑原 query + brain 拼的 1-2 变体, 每个用 2-3 引擎
    3) asyncio.gather 并行
    4) 合并去重

    实战 65: 智能重搜
    - 1 轮 < 3 条有效 → 自动触发重搜
    - 最多 3 轮
    - 重搜策略: 换引擎 / 拆词 / 放宽
    """
    t0 = time.time()
    rounds = []  # 实战 65: 记录每轮
    current_query = query
    current_top = top
    all_engines_used = []
    all_results = []
    brain_info = None

    for round_idx in range(max_retries):
        round_t0 = time.time()
        s = _get_search_module()

        # 1) 智能分析
        engines = ['bing_cn']  # 始终保留 fallback
        if use_brain:
            try:
                import super_brain as brain
                if brain_info is None:
                    brain_info = brain.analyze_query(current_query, use_cache=True)
                brain_engines = brain_info.get('search_engines', [])
                for be in brain_engines:
                    if be in ENGINE_MAP:
                        real_engine = ENGINE_MAP[be]
                        if real_engine not in engines and real_engine not in all_engines_used:
                            engines.append(real_engine)
                            if len(engines) >= max_engines:
                                break
            except Exception as e:
                if brain_info is None:
                    brain_info = {'error': str(e)}

        # 实战 65: 第 2 轮换不同引擎 (排除已用)
        if round_idx == 1:
            backup_engines = ['baidu', 'sogou', 'csdn', 'cnblogs', 'github', 'toutiao', 'zhihu']
            for be in backup_engines:
                if be in ENGINE_MAP and ENGINE_MAP[be] not in engines and ENGINE_MAP[be] not in all_engines_used:
                    engines.append(ENGINE_MAP[be])
                    if len(engines) >= max_engines:
                        break
        # 2) query 变体
        variants = [current_query]
        if brain_info and brain_info.get('pinyin') and brain_info.get('entity'):
            # 用拼音作为第二变体
            entity = brain_info['entity']
            if entity in current_query and brain_info['pinyin'] != entity:
                py_variant = current_query.replace(entity, brain_info['pinyin'].lower())
                variants.append(py_variant)

        # 实战 75: 智能搜索策略 (entity 类型 → site: 限制)
        try:
            import intent_strategy as _strat
            strat = _strat.strategy_for_query(current_query, brain_info)
            if strat and strat.get('rewrite_query'):
                variants.append(strat['rewrite_query'])
        except Exception:
            pass

        # 实战 65: 第 3 轮 - 拆词重写
        if round_idx >= 2 and brain_info and brain_info.get('entity'):
            entity = brain_info['entity']
            # 拆词: entity 拆成单字 + 用 query_rewrite 加同义词
            if len(entity) >= 2:
                for i in range(1, len(entity)):
                    parts = entity[:i] + ' ' + entity[i:]
                    variants.append(current_query.replace(entity, parts))
            # 简化: 去 "网址"/"官网" 等修饰词
            for suffix in [' 网址', ' 官网', ' 是什么', ' 怎么样']:
                if current_query.endswith(suffix):
                    variants.append(current_query[:-len(suffix)])

        variants = list(dict.fromkeys(variants))[:4]  # 去重 + 限 4

        # 3) 并行搜索
        tasks = []
        for v in variants:
            for e in engines:
                tasks.append(_search_one(s, v, e, current_top))

        all_results_raw = await asyncio.gather(*tasks, return_exceptions=True)

        # 4) 展平
        round_results = []
        round_engines = []
        for i, res in enumerate(all_results_raw):
            if isinstance(res, Exception):
                continue
            for r in res:
                if 'error' in r and 'url' not in r:
                    continue
                round_results.append(r)
            if res and isinstance(res, list) and res:
                eng = res[0].get('engine', '?')
                if eng not in round_engines:
                    round_engines.append(eng)
                if eng not in all_engines_used:
                    all_engines_used.append(eng)

        # 5) 注入 source
        for r in round_results:
            if not r.get('source') and r.get('url'):
                r['source'] = _domain(r['url'])

        # 6) 累加
        all_results.extend(round_results)

        # 记录本轮
        rounds.append({
            'round': round_idx + 1,
            'query': current_query,
            'variants': variants,
            'engines': engines,
            'engines_used': round_engines,
            'raw_count': len(round_results),
            'elapsed_ms': int((time.time() - round_t0) * 1000),
        })

        # 实战 65: 判断是否需要重搜
        # 计算"有效"结果数: 有 title + url + snippet 都不空
        effective = [r for r in round_results
                     if r.get('title') and r.get('url') and (r.get('snippet') or r.get('desc') or r.get('content'))]
        if len(effective) >= 3:
            # 已经够, 不再重搜
            break
        if round_idx >= max_retries - 1:
            # 最后一轮
            break
        # 触发下一轮: 用 query_rewrite 生成变体 query
        try:
            import query_rewrite as qr
            rewrites = qr.rewrite_query(current_query, use_llm=False)
            for r in rewrites[1:]:  # 跳过原 query
                if r != current_query and r not in [round.get('query') for round in rounds]:
                    current_query = r
                    break
        except Exception:
            pass

    # 7) 去重
    deduped = _dedup_by_url(all_results)

    # 8) 排序
    entity = (brain_info or {}).get('entity', '').lower() if brain_info else ''
    py = (brain_info or {}).get('pinyin', '').lower() if brain_info else ''

    def _score(r):
        base = r.get('score', 0) or 0
        title = (r.get('title', '') or '').lower()
        url = r.get('url', '') or ''
        bonus = 0
        if entity and (entity in title or entity.lower() in title):
            bonus += 50
        if py and (py in url or py in title):
            bonus += 30
        if entity and (entity in url.lower() or entity.replace(' ', '') in url.lower()):
            bonus += 20
        return base + bonus

    deduped.sort(key=_score, reverse=True)
    final = deduped[:top]

    return {
        'query': query,
        'variants': rounds[0].get('variants', []) if rounds else [],
        'engines': rounds[0].get('engines', []) if rounds else [],
        'engines_used': all_engines_used,
        'results': final,
        'count': len(final),
        'brain_info': brain_info,
        'rounds': rounds,  # 实战 65
        'retries': len(rounds) - 1,  # 实战 65
        'elapsed_ms': int((time.time() - t0) * 1000),
    }


# CLI 测试
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: multi_search.py <query> [top]")
        sys.exit(1)
    q = sys.argv[1]
    top = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    result = asyncio.run(multi_search(q, top=top))
    print(f"query: {result['query']}")
    print(f"variants: {result['variants']}")
    print(f"engines: {result['engines']}")
    print(f"elapsed: {result['elapsed_ms']}ms")
    print(f"count: {result['count']}")
    if result.get('brain_info'):
        bi = result['brain_info']
        print(f"brain: entity={bi.get('entity')} intent={bi.get('intent')} category={bi.get('category')}")
    print('results:')
    for i, r in enumerate(result['results'][:5], 1):
        print(f"  [{i}] {r.get('title', '?')[:60]}")
        print(f"      url: {r.get('url', '?')[:80]}")
        print(f"      source: {r.get('source', '?')}")
        print(f"      engine: {r.get('engine', '?')} score: {r.get('score', 0)}")
