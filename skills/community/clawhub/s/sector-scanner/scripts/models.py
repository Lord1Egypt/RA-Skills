from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class StockDefinition:
    code: str
    name: str


@dataclass(frozen=True)
class SectorDefinition:
    id: str
    name: str
    emoji: str
    stocks: list[StockDefinition]


@dataclass
class StockQuote:
    code: str
    name: str
    price: float
    previous_close: float
    open_price: float
    high: float
    low: float
    volume: float
    amount: float
    pct_chg: float
    source: str = "tdx"


@dataclass
class Bar:
    open: float
    close: float
    high: float
    low: float
    volume: float
    amount: float = 0.0


@dataclass
class StockScore:
    code: str
    name: str
    price: float
    pct_chg: float
    score: float
    flow_label: str
    flow_level: int
    volume_ratio: float
    details: list[str] = field(default_factory=list)


@dataclass
class SectorScanResult:
    id: str
    name: str
    emoji: str
    average_score: float
    heat_label: str
    flow_label: str
    flow_level: int
    red_count: int
    total_count: int
    up_ratio: float
    avg_pct_chg: float
    stocks: list[StockScore]
    scanned_at: datetime
    source: str
    errors: list[str] = field(default_factory=list)

    @property
    def top_stocks(self) -> list[StockScore]:
        return sorted(self.stocks, key=lambda item: item.score, reverse=True)[:3]

    def to_row(self, rank: int) -> list[Any]:
        return [
            rank,
            self.name,
            f"{self.average_score:.1f}",
            self.heat_label,
            f"{self.red_count}/{self.total_count}",
            f"{self.avg_pct_chg:+.2f}%",
            self.flow_label,
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "emoji": self.emoji,
            "average_score": self.average_score,
            "heat_label": self.heat_label,
            "flow_label": self.flow_label,
            "flow_level": self.flow_level,
            "red_count": self.red_count,
            "total_count": self.total_count,
            "up_ratio": round(self.up_ratio, 4),
            "avg_pct_chg": self.avg_pct_chg,
            "stocks": [
                {
                    "code": s.code,
                    "name": s.name,
                    "price": s.price,
                    "pct_chg": s.pct_chg,
                    "score": s.score,
                    "flow_label": s.flow_label,
                    "flow_level": s.flow_level,
                    "volume_ratio": s.volume_ratio,
                    "details": s.details,
                }
                for s in self.stocks
            ],
            "scanned_at": self.scanned_at.isoformat(),
            "source": self.source,
            "errors": self.errors,
        }
