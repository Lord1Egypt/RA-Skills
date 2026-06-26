"""Data models for item detail fetching and evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SellerInfo:
    name: str = ""
    rating: str = ""
    reviews_count: int = 0
    member_since: str = ""
    location: str = ""


@dataclass
class ItemDetail:
    title: str = ""
    price: str = ""
    price_numeric: float = 0.0
    currency: str = "USD"
    description: str = ""
    condition: str = ""
    images: list[str] = field(default_factory=list)
    seller: SellerInfo = field(default_factory=SellerInfo)
    posted_date: str = ""
    views: int = 0
    platform: str = ""
    source_url: str = ""
    platform_extras: dict = field(default_factory=dict)


@dataclass
class VisionConfig:
    """Configuration for the vision model used in image analysis."""
    model: str = ""
    api_base: str = ""
    api_key: str = ""
    max_images: int = 5
    timeout: int = 60

    @property
    def enabled(self) -> bool:
        return bool(self.model and self.api_base and self.api_key)


@dataclass
class EvalScores:
    seller_trust: float = 0.0
    listing_authenticity: float = 0.0
    image_quality: float = 0.0
    condition_value: float = 0.0
    price_competitiveness: float = 0.0
    risk_flags: float = 0.0
    overall: float = 0.0


@dataclass
class EvalResult:
    item: ItemDetail = field(default_factory=ItemDetail)
    scores: EvalScores = field(default_factory=EvalScores)
    flags: list[str] = field(default_factory=list)
    verdict: str = ""
    verdict_label: str = ""
    rationale: str = ""
    image_analysis: str = ""
