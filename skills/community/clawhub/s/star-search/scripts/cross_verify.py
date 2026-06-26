#!/usr/bin/env python3
"""实战 70 多源交叉验证 (2026-06-16)
- 同一事实 (实体/数字) 在 N 源出现 → 置信度 +30*N
- 来源可信度: 官网(w=1.0) / 百科(w=0.85) / 财经媒体(w=0.75) / 知乎(w=0.6) / 个人博客(w=0.4)
- 答案层标注: "3 源一致"/"2 源一致"/"X 说..."
"""
import os
import re
import json
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from urllib.parse import urlparse


# 来源可信度 (基于实战 70 经验值)
SOURCE_CREDIBILITY = {
    # 官方 (1.0)
    'jiuyangongshe.com': 1.0,
    'apple.com': 1.0,
    'huawei.com': 1.0,
    'byd.com': 1.0,
    'bydglobal.com': 1.0,
    'microsoft.com': 1.0,
    'openai.com': 1.0,
    'github.com': 1.0,
    'python.org': 1.0,
    'rust-lang.org': 1.0,
    'weixin.qq.com': 1.0,
    'weibo.com': 1.0,
    'zhihu.com': 1.0,
    'bilibili.com': 1.0,
    'douyin.com': 1.0,
    'tiktok.com': 1.0,
    'xueqiu.com': 0.95,  # 雪球
    '10jqka.com.cn': 0.95,  # 同花顺
    'eastmoney.com': 0.95,
    'sina.com.cn': 0.9,  # 新浪
    'qq.com': 0.9,
    'csdn.net': 0.85,  # CSDN (技术)
    'cnblogs.com': 0.85,
    'anthropic.com': 1.0,
    'docs.pythonlang.cn': 0.95,  # Python 中文文档
    'consumer.huawei.com': 1.0,
    'vmall.com': 0.9,  # 华为商城

    # 百科/聚合 (0.85)
    'baike.baidu.com': 0.85,
    'wikipedia.org': 0.95,
    'zhuanlan.zhihu.com': 0.7,  # 知乎专栏
    'baike.baidu.com': 0.85,

    # 财经媒体 (0.75)
    'cls.cn': 0.8,  # 财联社
    'yicai.com': 0.85,  # 第一财经
    'caixin.com': 0.9,  # 财新
    'stcn.com': 0.8,  # 证券时报
    'cnstock.com': 0.8,  # 中国证券网
    'thepaper.cn': 0.8,  # 澎湃
    'sohu.com': 0.6,  # 搜狐
    '163.com': 0.6,  # 网易
    'ifeng.com': 0.6,  # 凤凰

    # 工具/下载 (0.3)
    'pcsoft.com.cn': 0.3,  # PC 下载站
    'crsky.com': 0.3,
    'onlinedown.net': 0.3,
}


def _get_domain(url: str) -> str:
    if not url:
        return ''
    try:
        d = urlparse(url).netloc.lower()
        if d.startswith('www.'):
            d = d[4:]
        # 取主域 (例: docs.pythonlang.cn → pythonlang.cn)
        parts = d.split('.')
        if len(parts) >= 2:
            # 保留 .com/.cn/.org/.com.cn 等
            if parts[-1] in ('cn', 'com', 'org', 'net', 'io', 'cc'):
                if len(parts) >= 3 and parts[-2] in ('com', 'co', 'gov', 'net', 'org'):
                    return '.'.join(parts[-3:])
                return '.'.join(parts[-2:])
            return d
        return d
    except Exception:
        return ''


def get_source_credibility(url: str) -> float:
    """实战 70: 来源可信度 (0-1)"""
    if not url:
        return 0.5
    d = _get_domain(url)

    # 精确匹配
    if d in SOURCE_CREDIBILITY:
        return SOURCE_CREDIBILITY[d]

    # 子域匹配 (例: m.baidu.com → baidu.com)
    parts = d.split('.')
    if len(parts) > 2:
        parent = '.'.join(parts[-2:])
        if parent in SOURCE_CREDIBILITY:
            return SOURCE_CREDIBILITY[parent]
        parent3 = '.'.join(parts[-3:])
        if parent3 in SOURCE_CREDIBILITY:
            return SOURCE_CREDIBILITY[parent3]

    # 启发式
    if 'gov' in d or 'edu.cn' in d:
        return 0.9
    if 'blog' in d or 'wordpress' in d or 'csdn.net' in d:
        return 0.6
    if 'wiki' in d or 'baike' in d:
        return 0.85

    return 0.5  # 默认 0.5


def extract_facts(results: List[Dict]) -> Dict[str, List[Tuple[str, str, float]]]:
    """实战 70: 从结果中提取事实
    - 数字 (价格/年份/比例)
    - URL (官方网址)
    - 实体名 (标题里的核心词)
    返回: {fact_type: [(fact, source_domain, credibility)]}
    """
    facts = defaultdict(list)
    for r in results:
        title = r.get('title', '') or ''
        summary = r.get('summary', '') or r.get('snippet', '') or ''
        url = r.get('url', '') or ''
        domain = _get_domain(url)
        credibility = get_source_credibility(url)

        # 1) 数字
        nums = re.findall(r'\d+(?:\.\d+)?%?|\d{2,}', title + ' ' + summary[:300])
        for n in set(nums):
            if len(n) >= 2:  # 过滤太短
                facts['numbers'].append((n, domain, credibility))

        # 2) URL (官方网址)
        urls = re.findall(r'(?:https?://)?(?:www\.)?([a-zA-Z0-9][a-zA-Z0-9-]{0,61}\.(?:com|cn|org|net|io|cc|com\.cn|co))(?:/[^\s]*)?', summary)
        for u in set(urls):
            facts['urls'].append((u, domain, credibility))

        # 3) 标题实体 (简化: 取 title 第一个非空连续 2-10 字)
        for t in re.findall(r'[\u4e00-\u9fa5]{2,10}', title):
            if len(t) >= 2 and not t.isdigit():
                facts['titles'].append((t, domain, credibility))

    return facts


def cross_verify(results: List[Dict]) -> Dict:
    """实战 70: 交叉验证 + 可信度评分
    返回: {
        'facts': {fact_type: {fact: {sources: [...], cross_verified: N, avg_credibility: 0.0}}},
        'top_facts': [按 cross_verified + credibility 排序的 top 5 事实],
        'consensus_score': 0-100 总体一致度
    }
    """
    raw_facts = extract_facts(results)

    # 统计每个 fact 在多少不同源出现
    fact_summary = {}
    for ftype, flist in raw_facts.items():
        fact_summary[ftype] = {}
        for fact, source, cred in flist:
            if fact not in fact_summary[ftype]:
                fact_summary[ftype][fact] = {'sources': set(), 'credibilities': []}
            fact_summary[ftype][fact]['sources'].add(source)
            fact_summary[ftype][fact]['credibilities'].append(cred)

    # 计算 cross_verified + avg_credibility
    for ftype, fdict in fact_summary.items():
        for fact, info in fdict.items():
            info['cross_verified'] = len(info['sources'])
            info['avg_credibility'] = round(sum(info['credibilities']) / len(info['credibilities']), 2)
            info['sources'] = sorted(info['sources'])

    # 排序 top facts
    top_facts = []
    for ftype, fdict in fact_summary.items():
        for fact, info in fdict.items():
            # 分数 = cross_verified * 20 + avg_credibility * 30
            score = info['cross_verified'] * 20 + info['avg_credibility'] * 30
            top_facts.append({
                'type': ftype,
                'fact': fact,
                'score': round(score, 1),
                'cross_verified': info['cross_verified'],
                'avg_credibility': info['avg_credibility'],
                'sources': info['sources'][:5],
            })
    top_facts.sort(key=lambda x: x['score'], reverse=True)
    top_facts = top_facts[:10]

    # 总体一致度: 看 cross_verified >= 2 的比例
    if fact_summary:
        total = sum(len(f) for f in fact_summary.values())
        verified = sum(1 for fdict in fact_summary.values()
                      for info in fdict.values() if info['cross_verified'] >= 2)
        consensus = round(verified / max(total, 1) * 100, 1)
    else:
        consensus = 0.0

    return {
        'facts': {k: v for k, v in fact_summary.items()},
        'top_facts': top_facts,
        'consensus_score': consensus,
        'source_count': len(set(r.get('source', _get_domain(r.get('url', ''))) for r in results)),
    }


def get_credibility_for_url(url: str) -> float:
    """实战 70: 单一 URL 可信度"""
    return get_source_credibility(url)


def annotate_results_with_credibility(results: List[Dict]) -> List[Dict]:
    """实战 70: 给每条结果加 credibility 字段"""
    out = []
    for r in results:
        rr = dict(r)
        url = r.get('url', '')
        rr['credibility'] = get_source_credibility(url)
        out.append(rr)
    return out


def format_cross_verify_for_prompt(cv: Dict, max_facts: int = 5) -> str:
    """实战 70: 把交叉验证结果格式化成 LLM prompt 文本"""
    lines = []

    # 总体一致度
    lines.append(f"【多源交叉验证结果】")
    lines.append(f"总体一致度: {cv.get('consensus_score', 0)}/100")
    lines.append(f"覆盖源数: {cv.get('source_count', 0)}")
    lines.append("")

    # Top facts
    top = cv.get('top_facts', [])[:max_facts]
    if top:
        lines.append("【已验证事实 (按可信度排序)】")
        for i, f in enumerate(top, 1):
            lines.append(f"  {i}. {f['type']}: {f['fact'][:50]}")
            lines.append(f"     - 跨源数: {f['cross_verified']} 源")
            lines.append(f"     - 平均可信度: {f['avg_credibility']}")
            lines.append(f"     - 来源: {', '.join(f['sources'][:3])}")
        lines.append("")

    return "\n".join(lines)
