"""scripts/score.py - SBA 打分 + 可选 rerank(B2) + source_prefs(B8)（§5.9 / §7）。"""

import datetime
import re
from typing import Any, Dict

DEFAULT_CRED = {
    "gov": 0.95,
    "media": 0.85,
    "academic": 0.9,
    "vendor": 0.7,
    "forum": 0.4,
    "selfmedia": 0.35,
    "unknown": 0.5,
}
DEFAULT_BIAS = {
    "gov": 0.1,
    "media": 0.2,
    "academic": 0.1,
    "vendor": 0.3,
    "forum": 0.6,
    "selfmedia": 0.7,
    "unknown": 0.5,
}
from common import load_config, tokenize

# freshness 窗口 → 以「年」为单位的参考半径（用于时效性线性衰减）
_FRESH_YEARS = {
    "近1月": 1 / 12,
    "近3月": 0.25,
    "近6月": 0.5,
    "近1年": 1.0,
    "近3年": 3.0,
    "近5年": 5.0,
}
_YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def _load_cred() -> Dict[str, float]:
    cfg = load_config()
    return cfg.get("credibility_table", DEFAULT_CRED)


def _lexical_overlap(snippet: str, q: str) -> float:
    sw = tokenize(snippet)
    qw = tokenize(q)
    if not qw:
        return 0.5
    return len(sw & qw) / len(qw)


def _recency(published: str, freshness: str = None) -> float:
    """时效性评分（P1-4 实装）：抽年份 → 按 freshness 窗口做线性衰减。

    - 无 published：0.5（未知，不高不低）
    - 有内容但抽不到年份：0.6（略高于未知）
    - 有年份：age = 当前年 - 发表年
        * freshness 命中窗口 W：窗口内满分，超出按超出比例线性降到 0.1 下限
          rec = 1.0 - (age / W) * 0.8
        * 无明确窗口（中/全部）：温和全局衰减，近 5 年仍有参考价值
          rec = 1.0 / (1.0 + age * 0.12)
    零依赖、纯标准库，无外部依赖。
    """
    if not published:
        return 0.5
    ym = _YEAR_RE.search(published)
    if not ym:
        return 0.6
    year = int(ym.group(0))
    now = datetime.date.today().year
    age = max(0, now - year)
    win = _FRESH_YEARS.get((freshness or "中"))
    if win:
        rec = 1.0 - (age / win) * 0.8
        return round(max(0.1, min(1.0, rec)), 3)
    rec = 1.0 / (1.0 + age * 0.12)
    return round(max(0.2, min(1.0, rec)), 3)


def _authority(source_type: str, credibility_table: Dict[str, float] = None) -> float:
    # 与 SBA 的 credibility 共用同一份权威度数值（统一真相源，消除 _authority 硬编码与 DEFAULT_CRED 分叉，S3）
    tbl = credibility_table or DEFAULT_CRED
    return tbl.get(source_type, 0.5)


def score_source(
    s: Dict[str, Any], q: str, credibility_table: Dict[str, float] = None, freshness: str = None
) -> Dict[str, Any]:
    cred_tbl = credibility_table or _load_cred()
    st = s.get("source_type", "unknown")
    cred = cred_tbl.get(st, 0.5)
    rel = _lexical_overlap(s.get("snippet", ""), q)
    rec = _recency(s.get("published"), freshness)
    auth = _authority(st, cred_tbl)
    bias = DEFAULT_BIAS.get(st, 0.5)
    weighted = 0.35 * cred + 0.30 * rel + 0.15 * rec + 0.15 * auth + 0.05 * (1 - bias)
    return {
        "url": s.get("url"),
        "credibility": cred,
        "relevance": rel,
        "recency": rec,
        "authority": auth,
        "bias": bias,
        "weighted": round(weighted, 4),
    }
