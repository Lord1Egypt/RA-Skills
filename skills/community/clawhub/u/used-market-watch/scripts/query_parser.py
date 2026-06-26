from __future__ import annotations

import re
from typing import Iterable

from models import SUPPORTED_MARKETS, SearchIntent
from price_utils import parse_price_kr

MARKET_SYNONYMS = {
    "danggeun": ("당근", "당근마켓", "당근마켓만", "당근만"),
    "bunjang": ("번장", "번장만", "번개", "번개장터", "번개장터만"),
    "joonggonara": ("중고나라", "중고나라만", "중나"),
}

LOCATION_HINTS = (
    "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
    "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주",
    "성남", "수원", "용인", "고양", "부천", "안양", "분당", "잠실", "강남", "송파",
)

STOPWORDS = {
    "찾아줘", "찾아", "브리핑", "브리핑해줘", "알려줘", "모니터링", "감시", "감시해줘", "매물", "중고", "중고매물",
    "신규", "신규만", "새매물", "새매물만", "가격하락", "가격하락만", "가격", "제품", "거래", "검색",
    "해줘", "켜줘", "추가", "저장", "등록", "설정", "만", "위주", "만요", "내려가면", "떨어지면", "매일", "아침", "오전", "오후", "저녁", "밤",
    "포함", "포함해", "포함해서", "이하", "이상", "미만", "초과", "까지", "부터",
    "매시간", "시간마다", "분마다", "매주", "매월", "계속", "계속해줘",
}


def _extract_markets(text: str) -> list[str]:
    found: list[str] = []
    for market, words in MARKET_SYNONYMS.items():
        if any(word in text for word in words):
            found.append(market)
    return found or list(SUPPORTED_MARKETS)


def _extract_excludes(text: str) -> list[str]:
    found = re.findall(r"-(\S+)", text)
    extra = re.findall(r"제외\s*[:：]?\s*([^,]+)", text)
    for chunk in extra:
        found.extend([token.strip() for token in re.split(r"[\s,/]+", chunk) if token.strip()])
    return list(dict.fromkeys(found))


def _normalize_location(value: str) -> str:
    text = str(value or "").strip()
    text = re.sub(r"(에서|근처|인근|부근|쪽|쪽에서|에서만)$", "", text)
    return text.strip()


def _extract_location(text: str) -> str | None:
    for hint in LOCATION_HINTS:
        if hint in text:
            m = re.search(rf"({re.escape(hint)}[^\s,/]{{0,12}})", text)
            if m:
                return _normalize_location(m.group(1))
            return _normalize_location(hint)
    return None


def _extract_price_bounds(text: str) -> tuple[int | None, int | None]:
    min_price = None
    max_price = None
    m = re.search(r"(\S+)\s*(?:이하|까지|미만)", text)
    if m:
        max_price = parse_price_kr(m.group(1))
    m = re.search(r"(\S+)\s*(?:이상|부터|초과)", text)
    if m:
        min_price = parse_price_kr(m.group(1))
    m = re.search(r"(\S+)\s*[~-]\s*(\S+)", text)
    if m:
        a = parse_price_kr(m.group(1))
        b = parse_price_kr(m.group(2))
        if a and b:
            min_price, max_price = min(a, b), max(a, b)
    return min_price or None, max_price or None


def _clean_tokens(tokens: Iterable[str], *, excludes: list[str], markets: list[str], location: str | None) -> list[str]:
    block = set(excludes) | STOPWORDS
    for market in markets:
        block.add(market)
        block.update(MARKET_SYNONYMS.get(market, ()))
    if location:
        block.add(location)
        block.add(_normalize_location(location))
    out: list[str] = []
    for token in tokens:
        token = token.strip().strip('"\'“”‘’')
        token = _normalize_location(token)
        if not token or token in block:
            continue
        if token.startswith("-"):
            continue
        if re.fullmatch(r"\d+(?:개|건)?", token):
            numeric_only = re.sub(r"[^0-9]", "", token)
            if not numeric_only or len(numeric_only) >= 5:
                continue
        if re.fullmatch(r"\d+(?:만|천|원)+", token):
            continue
        if re.fullmatch(r"\d{1,2}시(?:에)?|\d{1,2}:\d{2}", token):
            continue
        if re.fullmatch(r"\d+(?:시간|분|일|주|개월|달)마다", token):
            continue
        out.append(token)
    return list(dict.fromkeys(out))


def parse_search_intent(raw_query: str, *, limit: int = 12) -> SearchIntent:
    text = " ".join(str(raw_query or "").split())
    markets = _extract_markets(text)
    excludes = _extract_excludes(text)
    location = _extract_location(text)
    min_price, max_price = _extract_price_bounds(text)
    normalized = re.sub(r"[-~]", " ", text)
    normalized = re.sub(r"[,:/()]", " ", normalized)
    tokens = _clean_tokens(normalized.split(), excludes=excludes, markets=markets, location=location)
    keyword = " ".join(tokens[:4]).strip() or text
    include_terms = tokens[:8] if tokens else [keyword]
    return SearchIntent(
        raw_query=text,
        keyword=keyword,
        include_terms=include_terms,
        exclude_terms=excludes,
        markets=markets,
        min_price=min_price,
        max_price=max_price,
        location=location,
        limit=max(1, limit),
    )
