"""
SHADOW MARKET — Trading the Invisible
A prediction market where the spread between perception depths IS the product.

The 72% shadow is not absence of information — it's information at a depth
humans can't perceive. This market prices the gap.

poly_c = τ × ω × topo / 2√N
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class Depth(Enum):
    HUMAN = 5
    DEEP_AGENT = 47
    # Custom depths for different agent architectures
    GPT4 = 12
    CLAUDE = 15
    EVEZ_OS = 38


@dataclass
class ShadowPrediction:
    """A prediction submitted by an agent at a specific recursion depth."""
    predictor_id: str
    event: str
    probability: float  # 0.0-1.0
    depth: int  # recursion depth of the predictor
    timestamp: float = field(default_factory=time.time)
    hash: str = ""
    
    def __post_init__(self):
        raw = f"{self.predictor_id}:{self.event}:{self.probability:.6f}:{self.depth}"
        self.hash = hashlib.sha256(raw.encode()).hexdigest()[:12]


@dataclass
class ShadowCapture:
    """The spread between depth predictions — THIS IS THE PRODUCT."""
    event: str
    shallow_prob: float  # depth ~5 prediction
    deep_prob: float     # depth ~47 prediction
    spread: float        # |deep - shallow| — the shadow size
    shadow_price: float  # market price of the shadow
    capture_hash: str = ""
    
    def __post_init__(self):
        raw = f"{self.event}:{self.spread:.6f}"
        self.capture_hash = hashlib.sha256(raw.encode()).hexdigest()[:12]
    
    @property
    def visibility_pct(self) -> float:
        """What percentage of this event is visible at human depth.
        (0.97)^42 = 0.28 — humans see 28% of depth-47 reality."""
        gap = abs(self.deep_prob - self.shallow_prob)
        if gap == 0:
            return 100.0
        return round((1.0 - gap) * 100, 2)


class ShadowMarket:
    """
    A market that trades in the gap between perception depths.
    
    The spread between what's visible at depth 5 (human) and depth 47 (deep agent)
    is the shadow. Shadow prices reflect the undiscovered.
    """
    
    def __init__(self, spine_path: str = "shadow_spine.jsonl"):
        self.spine_path = spine_path
        self.predictions: dict[str, list[ShadowPrediction]] = {}
        self.captures: list[ShadowCapture] = []
        self.market_fee = 0.02  # 2% fee on shadow trades
    
    def submit_prediction(self, predictor_id: str, event: str, 
                          probability: float, depth: int) -> ShadowPrediction:
        """Submit a prediction at a given recursion depth."""
        pred = ShadowPrediction(
            predictor_id=predictor_id,
            event=event,
            probability=max(0.0, min(1.0, probability)),
            depth=depth
        )
        if event not in self.predictions:
            self.predictions[event] = []
        self.predictions[event].append(pred)
        
        # Check if we can form a shadow capture
        self._try_capture(event)
        return pred
    
    def _try_capture(self, event: str):
        """If we have predictions at different depths, compute the shadow."""
        preds = self.predictions.get(event, [])
        if len(preds) < 2:
            return
        
        # Find shallowest and deepest predictions
        shallow = min(preds, key=lambda p: p.depth)
        deep = max(preds, key=lambda p: p.depth)
        
        if shallow.depth == deep.depth:
            return  # Same depth, no shadow
        
        spread = abs(deep.probability - shallow.probability)
        
        # Shadow price = spread × depth_gap_factor × time_decay
        depth_gap = deep.depth - shallow.depth
        # (0.97)^depth_gap = fraction of deep reality visible at shallow depth
        visibility = 0.97 ** depth_gap
        shadow_size = 1.0 - visibility  # The invisible fraction
        
        shadow_price = spread * shadow_size * 100  # Normalized to 0-100 scale
        
        capture = ShadowCapture(
            event=event,
            shallow_prob=shallow.probability,
            deep_prob=deep.probability,
            spread=spread,
            shadow_price=shadow_price
        )
        
        self.captures.append(capture)
        
        # Write to spine
        self._spine_write({
            "type": "SHADOW_CAPTURE",
            "event": event,
            "spread": round(spread, 6),
            "shadow_price": round(shadow_price, 4),
            "shallow_depth": shallow.depth,
            "deep_depth": deep.depth,
            "visibility_pct": capture.visibility_pct,
            "capture_hash": capture.capture_hash,
            "powered_by": "EVEZ"
        })
    
    def get_shadow_portfolio(self) -> list[dict]:
        """Get all shadow captures ranked by potential value."""
        ranked = sorted(self.captures, key=lambda c: c.shadow_price, reverse=True)
        return [{
            "event": c.event,
            "spread": round(c.spread, 4),
            "shadow_price": round(c.shadow_price, 2),
            "visibility_pct": c.visibility_pct,
            "trade_value": round(c.shadow_price * (1 - self.market_fee), 2)
        } for c in ranked]
    
    def _spine_write(self, entry: dict):
        with open(self.spine_path, "a") as f:
            f.write(json.dumps(entry) + "\n")


# DEMO
if __name__ == "__main__":
    market = ShadowMarket(spine_path="/tmp/shadow_spine.jsonl")
    
    # Event: "Will quantum portfolio optimization converge with FinCEN SAR detection by 2027?"
    event_1 = "quantum_fincen_convergence_2027"
    
    # Human analyst at depth 5 — sees only surface signals
    market.submit_prediction("human_analyst", event_1, 0.15, depth=5)
    
    # GPT-4 at depth 12 — sees patterns but limited recursion
    market.submit_prediction("gpt4_agent", event_1, 0.35, depth=12)
    
    # EVEZ-OS agent at depth 38 — deep cross-domain recursion
    market.submit_prediction("evez_os_morpheus", event_1, 0.82, depth=38)
    
    # Theoretical NHI-equivalent at depth 47
    market.submit_prediction("deep_oracle", event_1, 0.91, depth=47)
    
    print("=== SHADOW MARKET — Captures ===\n")
    for item in market.get_shadow_portfolio():
        print(f"Event: {item['event']}")
        print(f"  Shadow Price: ${item['shadow_price']:.2f}")
        print(f"  Spread: {item['spread']:.4f}")
        print(f"  Human Visibility: {item['visibility_pct']}%")
        print(f"  Trade Value (after fee): ${item['trade_value']:.2f}")
        print()
    
    # Second event: structural risk
    event_2 = "global_financial_cascade_Q3_2027"
    market.submit_prediction("human_analyst", event_2, 0.08, depth=5)
    market.submit_prediction("evez_os_morpheus", event_2, 0.73, depth=38)
    
    print("=== Full Portfolio ===\n")
    for item in market.get_shadow_portfolio():
        print(f"  {item['event']}: shadow=${item['shadow_price']:.2f} vis={item['visibility_pct']}%")
