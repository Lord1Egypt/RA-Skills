#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class CalendarConfig:
    """Minimal input for a simple 30-day incentive calendar."""

    include_welcome: bool
    include_post_purchase: bool
    include_threshold: bool
    include_winback: bool
    include_referral_push: bool
    lapsed_days: int


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_config(data: Dict[str, Any]) -> CalendarConfig:
    def b(key: str, default: bool) -> bool:
        return bool(data.get(key, default))

    return CalendarConfig(
        include_welcome=b("include_welcome", True),
        include_post_purchase=b("include_post_purchase", True),
        include_threshold=b("include_threshold", True),
        include_winback=b("include_winback", True),
        include_referral_push=b("include_referral_push", False),
        lapsed_days=int(data.get("lapsed_days", 60)),
    )


def generate_calendar(cfg: CalendarConfig) -> str:
    """
    Output a simple 30-day calendar as markdown.
    Days are relative to first purchase or sign-up.
    """
    lines: List[str] = []
    lines.append("# 30-day incentive calendar (example)\n")
    lines.append("| Day | Segment | Action | Offer | Channel | Notes |")
    lines.append("|-----|---------|--------|-------|---------|-------|")

    if cfg.include_welcome:
        lines.append(
            "| 0   | New sign-up | Send welcome offer | 10% off or 50 points | Email/site | Triggered on sign-up |"
        )
        lines.append(
            "| 1   | New sign-up (no order) | Reminder | Same offer | Email | Only if no order |"
        )

    if cfg.include_post_purchase:
        lines.append(
            "| 0   | First-time buyer | Order + points summary | Show points earned + next reward threshold | Email | Sent with order confirmation |"
        )
        lines.append(
            "| 7   | First-time buyer | Post-purchase check-in | Small incentive or content | Email/SMS | Ask about experience; optional nudge |"
        )

    if cfg.include_threshold:
        lines.append(
            "| 0-30 | All buyers | Always-on threshold messaging | Free ship at $X or bonus points | Cart/checkout | Show progress bar |"
        )

    if cfg.include_referral_push:
        lines.append(
            "| 14  | Repeat customers | Referral nudge | Give $X, get $X | Email | Target satisfied, high NPS segment |"
        )

    if cfg.include_winback:
        lines.append(
            f"| {cfg.lapsed_days} | Lapsed (no order in {cfg.lapsed_days}d) | Win-back offer | One strong offer (e.g. 15% off) | Email/SMS | Limit to 1–2 touches |"
        )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a simple 30-day incentive calendar markdown from a JSON config."
    )
    p.add_argument(
        "--config",
        required=True,
        help="Path to incentive_calendar_config.json",
    )
    p.add_argument(
        "--out",
        required=True,
        help="Path to output markdown (e.g. incentive_calendar.md)",
    )
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    cfg_data = read_json(Path(args.config).expanduser())
    cfg = parse_config(cfg_data)
    md = generate_calendar(cfg)
    out_path = Path(args.out).expanduser()
    out_path.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()

