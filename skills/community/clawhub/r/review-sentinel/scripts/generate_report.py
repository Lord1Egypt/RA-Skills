#!/usr/bin/env python3
"""
generate_report.py — Generate a reputation report from stored state.

Usage:
    python3 generate_report.py state/specsavers-broadway.json
    python3 generate_report.py state/specsavers-broadway.json --markdown --output report.md
"""

import sys
import json
from datetime import datetime


def load_state(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def generate_report(state: dict, as_markdown: bool = False) -> str:
    lines = []
    biz = state.get("businessName", "Unknown Business")
    rating = state.get("currentRating", "N/A")
    total = state.get("totalReviews", "N/A")
    breakdown = state.get("ratingBreakdown", {})
    reviews = state.get("recentReviews", [])
    history = state.get("history", [])
    fetched = state.get("lastFetched", "Unknown")
    
    if as_markdown:
        lines.append(f"# Reputation Report: {biz}")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    else:
        lines.append(f"REPUTATION REPORT: {biz}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Overview
    lines.append(f"## Overview" if as_markdown else "OVERVIEW")
    lines.append(f"- Rating: **{rating}** / 5.0" if as_markdown else f"  Rating: {rating} / 5.0")
    lines.append(f"- Total Reviews: **{total}**" if as_markdown else f"  Total Reviews: {total}")
    lines.append(f"- Last Updated: {fetched}\n")
    
    # Breakdown
    if breakdown:
        lines.append("## Rating Breakdown" if as_markdown else "RATING BREAKDOWN")
        total_count = sum(int(v) for v in breakdown.values()) or 1
        for stars in ["5", "4", "3", "2", "1"]:
            count = breakdown.get(stars, 0)
            pct = (count / total_count) * 100
            bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
            lines.append(f"  {stars}★ {bar} {count} ({pct:.0f}%)")
        lines.append("")
    
    # Trend
    if len(history) >= 2:
        lines.append("## Trend" if as_markdown else "TREND")
        first = history[0]
        last = history[-1]
        rating_delta = (last.get("rating", 0) or 0) - (first.get("rating", 0) or 0)
        review_delta = (last.get("totalReviews", 0) or 0) - (first.get("totalReviews", 0) or 0)
        direction = "📈 Improving" if rating_delta > 0 else "📉 Declining" if rating_delta < 0 else "➡️ Stable"
        lines.append(f"  Rating: {direction} ({rating_delta:+.2f} over {len(history)} snapshots)")
        lines.append(f"  New Reviews: +{review_delta}")
        lines.append("")
    
    # Recent negative reviews
    negatives = [r for r in reviews if r.get("rating") and r["rating"] <= 2]
    if negatives:
        lines.append("## ⚠️ Negative Reviews Requiring Attention" if as_markdown else "NEGATIVE REVIEWS")
        for r in negatives[:5]:
            author = r.get("author", "Anonymous")
            text = r.get("text", "")[:200]
            replied = "✅ Responded" if r.get("replied") else "❌ No response"
            lines.append(f"  [{r.get('rating', '?')}★] {author}: \"{text}\" — {replied}")
        lines.append("")
    
    # Positive highlights
    positives = [r for r in reviews if r.get("rating") and r["rating"] >= 4]
    if positives:
        lines.append("## 🌟 Positive Highlights" if as_markdown else "POSITIVE HIGHLIGHTS")
        for r in positives[:3]:
            author = r.get("author", "Anonymous")
            text = r.get("text", "")[:150]
            lines.append(f"  [{r.get('rating', '?')}★] {author}: \"{text}\"")
        lines.append("")
    
    # Recommendations
    lines.append("## Recommendations" if as_markdown else "RECOMMENDATIONS")
    
    if negatives:
        unresponded = [r for r in negatives if not r.get("replied")]
        if unresponded:
            lines.append(f"  1. Respond to {len(unresponded)} unaddressed negative review(s)")
    
    if breakdown:
        one_star_pct = (breakdown.get("1", 0) / total_count) * 100
        if one_star_pct > 10:
            lines.append(f"  2. 1-star reviews are {one_star_pct:.0f}% of total — investigate root causes")
    
    lines.append("  3. Encourage satisfied patients to leave reviews (ask after positive interactions)")
    lines.append("  4. Monitor competitor review trends for benchmarking")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    state = load_state(sys.argv[1])
    as_md = "--markdown" in sys.argv
    report = generate_report(state, as_markdown=as_md)
    
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    if output_path:
        with open(output_path, "w") as f:
            f.write(report)
        print(f"Report written to {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
