"""vkey-bid-standardizer.patterns

章节编号识别：
- parse_cn_num: 中文数字 → int（1-99，含 廿/卅/卌、两）
- match_pattern: 模式注册表匹配
- renumber_paragraph: 重编号核心
"""
import re
from typing import Optional, Tuple, List, Dict, Any


# ═══════════════════════════════════════════
#  中文数字解析
# ═══════════════════════════════════════════

_CN_DIG = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '两': 2,
    '廿': 20, '卅': 30, '卌': 40,
    '百': 100, '千': 1000,
}


def parse_cn_num(s: str) -> int:
    """中文数字 1-99 → int，支持 廿/卅/卌、两。

    Examples:
        '一' → 1, '十' → 10, '十一' → 11,
        '二十一' → 21, '九十九' → 99, '廿' → 20
        '' / 'xyz' → 0
    """
    if not s:
        return 0

    if len(s) == 1:
        v = _CN_DIG.get(s, 0)
        return v if v < 100 else 0

    n = 0
    if s[0] == '十':
        n = 10
        s = s[1:]
    else:
        ones = _CN_DIG.get(s[0], -1)
        if ones < 0 or ones >= 10:
            return 0
        if len(s) >= 2 and s[1] == '十':
            n = ones * 10
            s = s[2:]
        else:
            return 0

    if s:
        n += _CN_DIG.get(s[0], 0)
    return n


def parse_mixed_num(s: str) -> int:
    """混合数字（中/阿）→ int。'1' / '12' / '三' / '十一' / '21' 都支持。"""
    s = s.strip()
    if not s:
        return 0
    if s.isdigit():
        return int(s)
    return parse_cn_num(s)


# ═══════════════════════════════════════════
#  模式加载 + 匹配
# ═══════════════════════════════════════════

def load_patterns(profile: dict) -> Dict[str, List[dict]]:
    """从 profile 读模式注册表（profile['patterns']）。

    Returns:
        {h1: [...], h2: [...], h3: [...], h4: [...], h5: [...]}
    """
    return profile.get('patterns', {})


def match_pattern(rules: List[dict], text: str) -> Tuple[Optional[dict], Optional[re.Match], Optional[str]]:
    """按顺序尝试规则列表，返回 (matched_rule, match, title) 或 (None, None, None)。"""
    for rule in rules:
        try:
            m = re.match(rule['pattern'], text)
        except re.error:
            continue
        if not m:
            continue
        groups = list(m.groups())
        title = groups[-1].strip() if groups else text
        return rule, m, title
    return None, None, None


def resolve_number(rule: dict, m: re.Match) -> int:
    """根据规则的 cn_to_int / mixed_cn_int 标志解析第一个捕获组为整数。"""
    groups = list(m.groups())
    num_str = groups[0] if groups else ''

    if rule.get('cn_to_int'):
        return parse_cn_num(num_str)
    if rule.get('mixed_cn_int'):
        return parse_mixed_num(num_str)
    try:
        return int(num_str)
    except (ValueError, TypeError):
        return 0


def build_number(counters: List[int], level: int) -> str:
    """根据计数器和层级构建编号字符串。

    Args:
        counters: 5 个计数器 [chapter, section, subsection, subsubsection, subsubsubsection]
        level: 目标层级（1-5）
    """
    parts = counters[:level]
    return '.'.join(str(p) for p in parts)
