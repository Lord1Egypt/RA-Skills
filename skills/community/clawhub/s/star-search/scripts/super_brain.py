#!/usr/bin/env python3
"""v20.62 super_brain.py (2026-06-16) - AI 智能层
- query 进来先过 LLM: 实体识别 + 意图分类 + 关键词补全
- 缓存常见 query (省 LLM 调用)
- 后期给 query_rewrite.py / search / answer.py 用

设计:
- query → super_brain.analyze(query) → {entity, intent, keywords, pinyin, ...}
- search 用 intent 选引擎
- answer 用 entity 强约束 (必须包含 entity 官方信息)
"""
import os
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Optional

LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.<service-domain>/v1')
LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
LLM_MODEL = os.environ.get('LLM_MODEL', 'DeepSeek-V4-Flash')
LLM_TIMEOUT = int(os.environ.get('LLM_TIMEOUT', '8'))

_env_path = Path('/home/ubuntu/star-search/.env')
if _env_path.exists():
    try:
        with open(_env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, _, v = line.partition('=')
                    k, v = k.strip(), v.strip()
                    if k == 'LLM_BASE_URL' and v:
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

CACHE_FILE = Path('/home/ubuntu/star-search/brain_cache.json')
CACHE_TTL = 86400 * 7  # 7 天


def _load_cache() -> Dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        if time.time() - CACHE_FILE.stat().st_mtime > CACHE_TTL:
            return {}
        with open(CACHE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(data: Dict):
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


def _cache_get(key: str) -> Optional[Dict]:
    return _load_cache().get(key)


def _cache_set(key: str, value: Dict):
    data = _load_cache()
    data[key] = value
    _save_cache(data)


def _call_llm(prompt: str, max_tokens: int = 300) -> Optional[str]:
    """v20.62: 调 LLM (OpenAI 兼容)"""
    if not LLM_API_KEY:
        return None
    body = json.dumps({
        'model': LLM_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': 0.2,
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
    except Exception:
        return None


def analyze_query(query: str, use_cache: bool = True, context: str = '', **kwargs) -> Dict:
    """v20.62: AI 智能分析 query
    返回: {
        'entity': 主体词 (如 '韭研公社', '比亚迪', 'Python'),
        'intent': 意图 (navigation/info/transaction/comparison/news),
        'category': 类别 (finance/tech/general/shopping/social/...),
        'keywords': 关键词列表,
        'pinyin': 拼音 (entity 是中文时),
        'search_engines': 推荐引擎列表,
        'expected_info': 期望的答案信息 (网址/股价/教程/...)
    }
    """
    # 1) 缓存 (key 包含 query 长度避免短串冲突)
    cache_key = hashlib.md5(f"{len(query)}|{query.lower()}".encode('utf-8')).hexdigest()[:16]
    if use_cache:
        cached = _cache_get(cache_key)
        if cached:
            cached['from_cache'] = True
            return cached

    # 2) 调 LLM 分析
    prompt = f"""你是一个搜索意图分析助手。分析用户 query 并输出 JSON。

【intent 严格定义】
- navigation: 用户明确找官网/网址/官方入口 (含"官网/网址/官方"或"百度一下X/给我搜X")
- info: 用户查一般信息/介绍/百科/教程/原理/学术
- transaction: 用户想购买/比价 (含"价格/多少钱/优惠/折扣/购买/入手/购入")
- comparison: 用户对比多个对象 (含"vs/X和Y哪个好/X和Y区别/对比")
- news: 用户要最新资讯 (含"新闻/头条/进展/动态/最新消息")

【关键边界】
- "X 是什么/介绍/教程/原理" → info
- "X 官网/网址/百度一下X/给我搜X" → navigation
- "X 价格/多少钱/优惠" → transaction
- "X vs Y/对比/区别/哪个好" → comparison
- "X 新闻/进展/动态" → news
- 单纯"X" (公司/品牌/产品名) → info (查百科)

【示例】
Q: "华为官网" → {{"entity":"华为","intent":"navigation"}}
Q: "Python vs Rust" → {{"entity":"Python, Rust","intent":"comparison"}}
Q: "茅台 股价 多少" → {{"entity":"茅台","intent":"transaction"}}
Q: "今天 AI 新闻" → {{"entity":"AI","intent":"news"}}
Q: "Python 教程" → {{"entity":"Python","intent":"info"}}
Q: "比亚迪" → {{"entity":"比亚迪","intent":"info"}}

用户 query: {query}

请分析:
1. entity: 主体词 (专有名词/人名/产品名/品牌名/网站名)
2. intent: 搜索意图 (navigation 找官网 / info 查信息 / transaction 交易/购买 / comparison 对比 / news 资讯)
3. category: 类别 (finance 金融/tech 科技/general 通用/shopping 购物/social 社交/education 教育/medical 医疗/entertainment 娱乐/other 其他)
4. keywords: 核心关键词列表 (3-5 个)
5. pinyin: 主体词的拼音 (中文时返回, 英文返回 null)
6. search_engines: 推荐搜索引擎 (从 [bing_cn, baidu, sogou, 360, csdn, cnblogs, weixin, github, eastmoney, sina_finance, taobao] 中选 2-4 个)
7. expected_info: 用户期望看到什么信息 (网址/股价/教程/对比/新闻/...)

请严格按以下 JSON 格式返回 (不要其他说明):
{{
  "entity": "...",
  "intent": "...",
  "category": "...",
  "keywords": ["...", "..."],
  "pinyin": "...",
  "search_engines": ["...", "..."],
  "expected_info": "..."
}}"""

    content = _call_llm(prompt, max_tokens=300)
    if not content:
        # LLM 失败时降级: 用旧 query_rewrite 简单版本
        from query_rewrite import simple_pinyin
        return {
            'entity': query.split()[0] if query.split() else query,
            'intent': 'info',
            'category': 'general',
            'keywords': query.split(),
            'pinyin': simple_pinyin(query),
            'search_engines': ['bing_cn'],
            'expected_info': '通用信息',
            'from_llm': False,
        }

    # 3) 解析 JSON
    try:
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()
        result = json.loads(content)
        result['from_llm'] = True
    except Exception:
        # 解析失败
        from query_rewrite import simple_pinyin
        result = {
            'entity': query.split()[0] if query.split() else query,
            'intent': 'info',
            'category': 'general',
            'keywords': query.split(),
            'pinyin': simple_pinyin(query),
            'search_engines': ['bing_cn'],
            'expected_info': '通用信息',
            'from_llm': False,
            'raw_llm_response': content,
        }

    # 4) 缓存
    if use_cache and result.get('from_llm'):
        _cache_set(cache_key, result)

    return result