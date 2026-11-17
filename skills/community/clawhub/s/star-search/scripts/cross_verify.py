#!/usr/bin/env python3
"""v20.70 多源交叉验证 (2026-06-16)
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


# 来源可信度 (基于v20.70 经验值)
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

# v20.95: E-E-A-T 权威性词典 (Experience/Expertise/Authoritativeness/Trust)
SOURCE_AUTHORITY = {
    # 政府/官方 (1.0)
    'gov.cn': 1.0, 'miit.gov.cn': 1.0, 'beijing.gov.cn': 1.0, 'shanghai.gov.cn': 1.0,
    'people.com.cn': 0.95, 'xinhuanet.com': 0.95, 'xinhua.org': 0.95,
    # 教育/学术 (0.95)
    'edu.cn': 0.95, 'ac.cn': 0.95, 'cas.cn': 0.95, 'acm.org': 0.95, 'ieee.org': 0.95,
    'arxiv.org': 0.95, 'scholar.google.com': 0.95, 'researchgate.net': 0.9,
    'cnki.net': 0.9, 'wanfangdata.com.cn': 0.9,
    # 知名百科 (0.85)
    'wikipedia.org': 0.85, 'baike.baidu.com': 0.75, 'zh.wikipedia.org': 0.85,
    # 财经媒体 (0.8)
    'eastmoney.com': 0.85, 'sina.com.cn': 0.8, 'qq.com': 0.75, '163.com': 0.75,
    'sohu.com': 0.7, 'ifeng.com': 0.75, 'caixin.com': 0.9, 'yicai.com': 0.9,
    'stcn.com': 0.8, 'cnstock.com': 0.8, '21jingji.com': 0.8, 'cls.cn': 0.8,
    'wallstreetcn.com': 0.85, 'xueqiu.com': 0.75, 'jiuyangongshe.com': 0.8,
    # 商业媒体 (0.7)
    '36kr.com': 0.7, 'huxiu.com': 0.7, 'pingwest.com': 0.7, 'geekpark.net': 0.7,
    'csdn.net': 0.65, 'jianshu.com': 0.55, 'zhihu.com': 0.6, 'weibo.com': 0.55,
    # 商业平台 (0.7)
    'jd.com': 0.7, 'taobao.com': 0.65, 'tmall.com': 0.7, 'pdd.com': 0.6,
    'amap.com': 0.75, 'dianping.com': 0.7, 'meituan.com': 0.7,
    # 社交/UGC (0.5)
    'douban.com': 0.55, 'bilibili.com': 0.6, 'douyin.com': 0.55, 'kuaishou.com': 0.55,
    'tieba.baidu.com': 0.5, 'weibo.cn': 0.55,
    # 个人博客 (0.4)
    'cnblogs.com': 0.55, 'oschina.net': 0.6, 'segmentfault.com': 0.6, 'infoq.cn': 0.7,
    'wordpress.com': 0.4, 'blogspot.com': 0.4, 'hexo.io': 0.4,
}

# v20.95: 时间衰减函数 (近 30 天 1.0, 1 年内 0.8, 3 年内 0.6, 更老 0.4)
def get_time_decay(date_str: str) -> float:
    """根据发布日期返回时间衰减系数 0-1
    - 近 30 天: 1.0 (新)
    - 30-180 天: 0.9
    - 180-365 天: 0.8
    - 1-2 年: 0.65
    - 2-3 年: 0.5
    - 3+ 年: 0.4
    """
    if not date_str:
        return 0.6  # 无日期默认中等
    from datetime import datetime, timezone
    try:
        # 处理多种日期格式
        d = None
        for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
            try:
                d = datetime.strptime(date_str[:19], fmt)
                break
            except ValueError:
                continue
        if not d:
            return 0.6
        # 当前时间 (修正: 6/19)
        now = datetime(2026, 6, 19)
        days_old = (now - d).days
        if days_old <= 30: return 1.0
        if days_old <= 180: return 0.9
        if days_old <= 365: return 0.8
        if days_old <= 730: return 0.65
        if days_old <= 1095: return 0.5
        return 0.4
    except Exception:
        return 0.6

# v20.95: 语言匹配 (中文 query + 中文 url 加分)
def get_language_bonus(url: str, query: str = '') -> float:
    """中文 query + 中文 url 1.0, 否则 0.85"""
    if not url or not query:
        return 0.9
    has_chinese = bool(__import__('re').search(r'[\u4e00-\u9fff]', query))
    if not has_chinese:
        return 1.0  # 英文 query, 任何 url 都 OK
    # 中文 query
    d = _get_domain(url)
    if d.endswith('.cn') or 'baidu' in d or 'zhihu' in d or 'weibo' in d or 'sina' in d or 'qq' in d or 'sohu' in d or '163' in d or 'bilibili' in d:
        return 1.0
    return 0.85  # 英文 url 服务中文 query 略降



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


def get_source_credibility(url: str, date_str: str = '', query: str = '') -> float:
    """v20.70+95: 来源可信度 4 维评分 (0-1)
    - domain 基础 (SOURCE_CREDIBILITY 30+)
    - authority 权威性 (SOURCE_AUTHORITY 50+ E-E-A-T)
    - time_decay 时间衰减 (近 30 天 1.0 → 3+ 年 0.4)
    - language 语言匹配 (中文 query + 中文 url 1.0)
    加权: domain 30% + authority 30% + time 25% + lang 15%
    """
    if not url:
        return 0.5
    d = _get_domain(url)
    parts = d.split('.')

    # 1) domain 基础分
    domain_score = 0.5
    if d in SOURCE_CREDIBILITY:
        domain_score = SOURCE_CREDIBILITY[d]
    else:
        for k in (2, 3):
            if k <= len(parts):
                parent = '.'.join(parts[-k:])
                if parent in SOURCE_CREDIBILITY:
                    domain_score = SOURCE_CREDIBILITY[parent]
                    break
        if 'gov' in d or 'edu.cn' in d:
            domain_score = 0.9
        elif 'blog' in d or 'wordpress' in d:
            domain_score = 0.45
        elif 'csdn' in d or 'cnblogs' in d:
            domain_score = 0.6
        elif 'wiki' in d or 'baike' in d:
            domain_score = 0.85

    # 2) authority 权威性
    auth_score = domain_score
    if d in SOURCE_AUTHORITY:
        auth_score = SOURCE_AUTHORITY[d]
    else:
        for k in (2, 3):
            if k <= len(parts):
                parent = '.'.join(parts[-k:])
                if parent in SOURCE_AUTHORITY:
                    auth_score = SOURCE_AUTHORITY[parent]
                    break

    # 3) time_decay
    time_score = 0.6
    if date_str:
        from datetime import datetime
        try:
            d_obj = None
            ds = date_str[:19] if len(date_str) > 19 else date_str
            for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
                try:
                    d_obj = datetime.strptime(ds, fmt)
                    break
                except ValueError:
                    continue
            if d_obj:
                # 当前时间 (v20.95: 2026-06-19)
                now = datetime(2026, 6, 19)
                days_old = (now - d_obj).days
                if days_old <= 30: time_score = 1.0
                elif days_old <= 180: time_score = 0.9
                elif days_old <= 365: time_score = 0.8
                elif days_old <= 730: time_score = 0.65
                elif days_old <= 1095: time_score = 0.5
                else: time_score = 0.4
        except Exception:
            pass

    # 4) language
    lang_score = 0.9
    if query:
        import re
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', query))
        if not has_chinese:
            lang_score = 1.0
        else:
            if d.endswith('.cn') or any(k in d for k in ('baidu', 'zhihu', 'weibo', 'sina', 'qq.com', 'sohu', '163.com', 'bilibili', 'douban', 'eastmoney', 'csdn', 'cnblogs', 'cnki', 'sohu', 'toutiao')):
                lang_score = 1.0
            else:
                lang_score = 0.85

    # 加权平均
    final = domain_score * 0.30 + auth_score * 0.30 + time_score * 0.25 + lang_score * 0.15
    return round(final, 3)


def extract_facts(results: List[Dict]) -> Dict[str, List[Tuple[str, str, float]]]:
    """v20.70: 从结果中提取事实
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
        date_str = r.get('date', '') or ''
        query_str = ''
        credibility = get_source_credibility(url, date_str, query_str)

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
    """v20.70: 交叉验证 + 可信度评分
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
    """v20.70: 单一 URL 可信度"""
    return get_source_credibility(url)


def annotate_results_with_credibility(results: List[Dict]) -> List[Dict]:
    """v20.70: 给每条结果加 credibility 字段"""
    out = []
    for r in results:
        rr = dict(r)
        url = r.get('url', '')
        rr['credibility'] = get_source_credibility(url)
        out.append(rr)
    return out


def format_cross_verify_for_prompt(cv: Dict, max_facts: int = 5) -> str:
    """v20.70: 把交叉验证结果格式化成 LLM prompt 文本"""
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
