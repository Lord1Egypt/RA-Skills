from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from price_utils import parse_price_kr

SUPPORTED_MARKETS = ("danggeun", "bunjang", "joonggonara")
MARKET_LABELS = {
    "danggeun": "당근마켓",
    "bunjang": "번개장터",
    "joonggonara": "중고나라",
}


@dataclass
class ListingItem:
    market: str
    article_id: str
    title: str
    price_text: str
    link: str
    query: str
    thumbnail: str | None = None
    seller: str | None = None
    location: str | None = None
    price_numeric: int | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def parse_price(self) -> int:
        if self.price_numeric is None:
            self.price_numeric = parse_price_kr(self.price_text)
        return self.price_numeric

    def article_key(self) -> str:
        return f"{self.market}:{self.article_id}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "market": self.market,
            "market_label": MARKET_LABELS.get(self.market, self.market),
            "article_id": self.article_id,
            "article_key": self.article_key(),
            "title": self.title,
            "price_text": self.price_text,
            "price_numeric": self.parse_price(),
            "link": self.link,
            "query": self.query,
            "thumbnail": self.thumbnail,
            "seller": self.seller,
            "location": self.location,
            "meta": self.meta,
        }


@dataclass
class SearchIntent:
    raw_query: str
    keyword: str
    include_terms: list[str]
    exclude_terms: list[str]
    markets: list[str]
    min_price: int | None = None
    max_price: int | None = None
    location: str | None = None
    limit: int = 12

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_query": self.raw_query,
            "keyword": self.keyword,
            "include_terms": self.include_terms,
            "exclude_terms": self.exclude_terms,
            "markets": self.markets,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "location": self.location,
            "limit": self.limit,
        }
