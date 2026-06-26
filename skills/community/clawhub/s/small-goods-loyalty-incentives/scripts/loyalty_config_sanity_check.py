#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class LoyaltyConfig:
    """Minimal loyalty config model for sanity checks."""

    currency: str
    points_per_dollar: float
    point_monetary_value: float
    average_margin_pct: float
    max_reward_discount_pct_per_order: float
    min_order_value_for_redemption: float

    def effective_max_reward_pct(self) -> float:
        # Max discount fraction of order value if a member uses all allowed points
        return min(self.max_reward_discount_pct_per_order, 100.0)


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in {path}: {e}") from e


def parse_config(data: Dict[str, Any]) -> LoyaltyConfig:
    def get_required(key: str) -> Any:
        if key not in data:
            raise SystemExit(f"Missing required key in config: '{key}'")
        return data[key]

    return LoyaltyConfig(
        currency=str(get_required("currency")),
        points_per_dollar=float(get_required("points_per_dollar")),
        point_monetary_value=float(get_required("point_monetary_value")),
        average_margin_pct=float(get_required("average_margin_pct")),
        max_reward_discount_pct_per_order=float(
            get_required("max_reward_discount_pct_per_order")
        ),
        min_order_value_for_redemption=float(
            get_required("min_order_value_for_redemption")
        ),
    )


def analyze_config(cfg: LoyaltyConfig) -> List[str]:
    notes: List[str] = []

    if cfg.points_per_dollar <= 0:
        notes.append("❌ points_per_dollar must be > 0.")

    if cfg.point_monetary_value <= 0:
        notes.append("❌ point_monetary_value must be > 0.")

    # Reward cost as % of revenue per order if customer always redeems
    reward_cost_per_dollar = cfg.points_per_dollar * cfg.point_monetary_value
    reward_cost_pct = reward_cost_per_dollar * 100.0

    notes.append(
        f"ℹ️ Reward cost if fully redeemed every order: "
        f"{reward_cost_pct:.2f}% of revenue."
    )

    if reward_cost_pct > cfg.average_margin_pct:
        notes.append(
            "⚠️ Reward cost per order is higher than average margin. "
            "Consider lowering points_per_dollar or point_monetary_value."
        )
    elif reward_cost_pct > cfg.average_margin_pct * 0.7:
        notes.append(
            "⚠️ Reward cost per order is high relative to margin. "
            "Double-check you can sustain this with expected redemption rate."
        )
    else:
        notes.append(
            "✅ Reward cost per order is below average margin (assuming 100% redemption)."
        )

    if not (0.0 < cfg.max_reward_discount_pct_per_order <= 100.0):
        notes.append(
            "❌ max_reward_discount_pct_per_order must be between 0 and 100."
        )

    if cfg.min_order_value_for_redemption <= 0:
        notes.append("⚠️ min_order_value_for_redemption is <= 0; set a minimum to protect AOV.")

    if cfg.average_margin_pct < 10.0:
        notes.append(
            "⚠️ Average margin is low (<10%). Loyalty rewards should be conservative."
        )

    return notes


def format_report(cfg: LoyaltyConfig, notes: List[str]) -> str:
    lines: List[str] = []
    lines.append("# Loyalty config sanity check\n")
    lines.append(f"- Currency: {cfg.currency}")
    lines.append(f"- Points per {cfg.currency} 1: {cfg.points_per_dollar:.2f}")
    lines.append(f"- Point value: {cfg.point_monetary_value:.4f} {cfg.currency}")
    lines.append(f"- Average margin: {cfg.average_margin_pct:.2f}%")
    lines.append(
        f"- Max reward discount per order: {cfg.max_reward_discount_pct_per_order:.2f}%"
    )
    lines.append(
        f"- Min order value for redemption: {cfg.min_order_value_for_redemption:.2f} {cfg.currency}"
    )
    lines.append("")
    lines.append("## Findings")
    for note in notes:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Quick sanity check for a simple loyalty program config (points value vs margin, max discount, thresholds)."
    )
    p.add_argument("--config", required=True, help="Path to loyalty_config.json")
    p.add_argument(
        "--out",
        help="Optional path to write a markdown report. If omitted, prints to stdout.",
    )
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    cfg_path = Path(args.config).expanduser()
    data = read_json(cfg_path)
    cfg = parse_config(data)
    notes = analyze_config(cfg)
    report = format_report(cfg, notes)

    if args.out:
        out_path = Path(args.out).expanduser()
        out_path.write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()

