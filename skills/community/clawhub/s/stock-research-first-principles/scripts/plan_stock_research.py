#!/usr/bin/env python3
"""Generate an offline bilingual evidence-first stock-research plan."""

from __future__ import annotations

import argparse
from datetime import date


MODES = ("single_stock", "multi_compare", "sector_basket", "thesis_review")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbols", nargs="+", required=True)
    parser.add_argument("--market", required=True)
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--question", default="Assess evidence, valuation, and risk.")
    parser.add_argument("--review-date", default=str(date.today()))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    symbols = ", ".join(symbol.upper() for symbol in args.symbols)
    lines = [
        "# Evidence-first research plan / 证据优先研究计划",
        "",
        f"- Mode / 模式: {args.mode}",
        f"- Symbols / 标的: {symbols}",
        f"- Market / 市场: {args.market}",
        f"- Question / 问题: {args.question}",
        f"- Review date / 复盘日期: {args.review_date}",
        "- Direct trading action / 直接交易动作: 0",
        "",
        "## Evidence checklist / 证据清单",
        "",
        "- [ ] Dated primary sources and retrieval times / 带日期的一手来源和获取时间",
        "- [ ] Normalized financial and operating history / 标准化财务和经营历史",
        "- [ ] Guidance, consensus, and assumption reconciliation / 指引、一致预期和假设核对",
        "- [ ] Direct positive and negative evidence / 直接正面和负面证据",
        "- [ ] Valuation method, assumptions, range, and downside / 估值方法、假设、区间和下行情景",
        "- [ ] Falsifiable thesis, trigger, and invalidation / 可证伪论点、触发条件和失效条件",
        "- [ ] Research-only disclaimer / 仅研究免责声明",
        "",
        "## Completion gate / 完成门禁",
        "",
        "Do not finalize when evidence is stale, valuation is absent, source conflicts are unresolved, or execution fields appear. / 证据陈旧、缺少估值、来源冲突未解决或出现执行字段时，不得完成研究。",
    ]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
