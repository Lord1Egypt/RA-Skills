from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CognitiveProfile:
    """Unified cognitive style model.

    Merges digital_twin.CognitiveStyle (continuous 0-1 values) and
    personality_analyzer cognitive/reasoning style (discrete categories).

    Both representations are kept because they serve different purposes:
    - Continuous values: for similarity computation and trend tracking
    - Discrete categories: for human-readable reports and personality profiles
    """

    reflective_depth: float = 0.5
    intuition_bias: float = 0.5
    risk_tolerance: float = 0.5
    complexity_preference: float = 0.5

    @property
    def cognitive_style(self) -> str:
        return "abstract" if self.complexity_preference > 0.5 else "concrete"

    @property
    def reasoning_style(self) -> str:
        return "intuitive" if self.intuition_bias > 0.5 else "logical"

    @property
    def decision_style(self) -> str:
        if self.intuition_bias > 0.65:
            return "intuitive"
        if self.intuition_bias < 0.35:
            return "analytical"
        return "mixed"

    @property
    def risk_profile(self) -> str:
        if self.risk_tolerance > 0.65:
            return "aggressive"
        if self.risk_tolerance < 0.35:
            return "conservative"
        return "moderate"

    update_source: str = "unknown"
    confidence: float = 0.5
    last_updated: float = 0.0

    @classmethod
    def from_digital_twin(cls, dt_style) -> 'CognitiveProfile':
        if isinstance(dt_style, dict):
            return cls(
                reflective_depth=dt_style.get('reflective_depth', 0.5),
                intuition_bias=dt_style.get('intuition_bias', 0.5),
                risk_tolerance=dt_style.get('risk_tolerance', 0.5),
                complexity_preference=dt_style.get('complexity_preference', 0.5),
                update_source=dt_style.get('update_source', 'digital_twin'),
            )
        return cls(
            reflective_depth=getattr(dt_style, 'reflective_depth', 0.5),
            intuition_bias=getattr(dt_style, 'intuition_bias', 0.5),
            risk_tolerance=getattr(dt_style, 'risk_tolerance', 0.5),
            complexity_preference=getattr(dt_style, 'complexity_preference', 0.5),
            update_source=getattr(dt_style, 'update_source', 'digital_twin'),
        )

    @classmethod
    def from_personality(cls, cognitive_style: str, reasoning_style: str) -> 'CognitiveProfile':
        return cls(
            complexity_preference=0.7 if cognitive_style == "abstract" else 0.3,
            intuition_bias=0.7 if reasoning_style == "intuitive" else 0.3,
            update_source="personality_analyzer",
        )

    def merge(self, other: 'CognitiveProfile', weight: float = 0.5) -> 'CognitiveProfile':
        return CognitiveProfile(
            reflective_depth=self.reflective_depth * (1 - weight) + other.reflective_depth * weight,
            intuition_bias=self.intuition_bias * (1 - weight) + other.intuition_bias * weight,
            risk_tolerance=self.risk_tolerance * (1 - weight) + other.risk_tolerance * weight,
            complexity_preference=self.complexity_preference * (1 - weight) + other.complexity_preference * weight,
            update_source="merged",
            confidence=max(self.confidence, other.confidence),
        )
