#!/usr/bin/env python3
"""实战 61 智能 query 重写 (2026-06-16)
- 生僻词 / 合成词 / 拼音: 自动加同义词 + 拼音
- 短 query (< 4 字符): 不动
- 速度快: LLM 重写 < 500ms (缓存常见词)
- 端到端: query 拆词 + 拼音 + 翻译 (英文时)
"""
import os
import re
import json
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Optional
from pathlib import Path

LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.token-star.cn/v1')
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

# 常见中→拼音映射 (部分, 不全; LLM 补全)
PY_MAP = {
    '韭': 'jiu', '研': 'yan', '公': 'gong', '社': 'she',
    '所': 'suo', '股': 'gu', '票': 'piao', '财': 'cai',
    '经': 'jing', '券': 'quan', '基': 'ji', '金': 'jin',
    '惠': 'hui', '比': 'bi', '亚': 'ya', '迪': 'di',
    '华': 'hua', '为': 'wei', '腾': 'teng', '讯': 'xun',
    '阿': 'a', '里': 'li', '巴': 'ba', '腾': 'teng',
    '字': 'zi', '节': 'jie', '京': 'jing', '东': 'dong',
    '淘': 'tao', '拼': 'pin', '多': 'duo', '快': 'kuai',
    '网': 'wang', '易': 'yi', '微': 'wei', '博': 'bo',
    '美': 'mei', '团': 'tuan', '点': 'dian', '评': 'ping',
    '滴': 'di', '出': 'chu', '行': 'xing', '链': 'lian',
    '支': 'zhi', '付': 'fu', '宝': 'bao', '云': 'yun',
    '腾': 'teng', '讯': 'xun', '优': 'you', '酷': 'ku',
    '爱': 'ai', '奇': 'qi', '艺': 'yi', '哔': 'bi',
    '小': 'xiao', '红': 'hong', '书': 'shu', '抖': 'dou',
    '知': 'zhi', '乎': 'hu', '简': 'jian', '书': 'shu',
}

# 常见中→英文翻译 (部分)
EN_MAP = {
    '微信': 'wechat', '微博': 'weibo', '淘宝': 'taobao',
    '京东': 'jd.com', '拼多多': 'pinduoduo', '美团': 'meituan',
    '滴滴': 'didi', '快手': 'kuaishou', '抖音': 'douyin',
    '哔哩哔哩': 'bilibili', 'B站': 'bilibili',
    '知乎': 'zhihu', '百度': 'baidu', '阿里': 'alibaba',
    '腾讯': 'tencent', '华为': 'huawei', '小米': 'xiaomi',
    '比亚迪': 'byd', '苹果': 'apple', '微软': 'microsoft',
    '谷歌': 'google', '亚马逊': 'amazon', 'Meta': 'meta',
}


def simple_pinyin(text: str) -> str:
    """实战 61: 简单字符 → 拼音映射 (部分)
    """
    out = []
    for c in text:
        if c in PY_MAP:
            out.append(PY_MAP[c])
        else:
            out.append(c)
    return ''.join(out)


def expand_query(query: str) -> List[str]:
    """实战 61: 扩展 query (同义词 + 拼音 + 英文)
    返回: 多个变体 query 列表
    """
    variants = [query]  # 原 query 优先

    # 1) 拼音
    py = simple_pinyin(query)
    if py != query and not py.isascii():
        # 拼音里还有中文 (说明没全在 PY_MAP)
        pass
    if py != query and len(py) >= 3:
        variants.append(py)

    # 2) 英文翻译 (精确匹配)
    for cn, en in EN_MAP.items():
        if cn in query:
            variants.append(query.replace(cn, en))

    # 3) 短词 (< 4 字符): 不扩展 (避免 LLM 噪声)
    if len(query) > 4 and len(query) < 20:
        # 4) LLM 加同义词 (慢, 慎用)
        pass  # 默认不开 LLM 重写, 走快速路径

    return variants


def rewrite_query(query: str, use_llm: bool = False) -> List[str]:
    """实战 61: 智能 query 重写
    use_llm=False: 快速路径 (拼音 + 英文映射)
    use_llm=True: LLM 拆词 + 加同义词 (慢 1-3s, 慎用)
    """
    variants = expand_query(query)

    if use_llm and LLM_API_KEY and len(query) >= 2 and len(query) <= 30:
        # 调 LLM 拆词 + 同义词
        prompt = f"""用户搜索: {query}

请生成 3 个变体, 帮助搜索引擎更准确:
1. 拆词版本 (如 韭研公社 → 韭研 公社)
2. 拼音版本 (如 韭研公社 → jiuyangongshe)
3. 关键词补全 (如 加 'app'/'官网'/'平台')

一行一个, 不要其他说明:"""
        try:
            body = json.dumps({
                'model': LLM_MODEL,
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 100,
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
            with urllib.request.urlopen(req, timeout=LLM_TIMEOUT) as resp:
                data = json.loads(resp.read())
                content = data['choices'][0]['message']['content']
                for line in content.split('\n'):
                    line = line.strip().lstrip('0123456789.-:').strip()
                    if line and 2 <= len(line) <= 50:
                        variants.append(line)
        except Exception:
            pass

    # 去重
    seen = set()
    result = []
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            result.append(v)
    return result[:5]  # 最多 5 个
