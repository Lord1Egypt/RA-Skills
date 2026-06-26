from __future__ import annotations

import re

_FREE_KEYWORDS = ("무료나눔", "무료", "나눔", "무나")


def parse_price_kr(text: str | None) -> int:
    if text is None:
        return 0
    s = str(text).strip()
    if not s:
        return 0
    s = s.replace(" ", "")
    s_norm = s.lower().replace(",", "").replace("krw", "").replace("￦", "").replace("원", "")
    if not re.search(r"\d", s_norm):
        return 0 if any(k in s_norm for k in _FREE_KEYWORDS) else 0
    total = 0
    m_man = re.search(r"(\d+(?:\.\d+)?)만", s_norm)
    if m_man:
        total += int(float(m_man.group(1)) * 10000)
        rest = s_norm[m_man.end():]
        m_thousand = re.search(r"(\d+(?:\.\d+)?)천", rest)
        if m_thousand:
            total += int(float(m_thousand.group(1)) * 1000)
            return total
        m_tail = re.search(r"(\d+)", rest)
        if m_tail:
            tail = int(m_tail.group(1))
            total += tail * 1000 if tail < 1000 else tail
        return total
    m_thousand = re.search(r"(\d+(?:\.\d+)?)천", s_norm)
    if m_thousand:
        return int(float(m_thousand.group(1)) * 1000)
    digits = re.findall(r"\d+", s_norm)
    return int("".join(digits)) if digits else 0


def format_price_kr(amount: int | None) -> str:
    if not amount:
        return "가격문의"
    return f"{int(amount):,}원"
