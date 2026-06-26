"""
CLI 入口 — 统一命令行接口。
"""
from __future__ import annotations

import argparse
import sys

from .analyzers import analyze_multi, analyze_portfolio, analyze_single


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="stock-brief",
        description="A 股实时分析与操作建议生成器（三模式：portfolio/single/multi）",
        epilog="完整文档: https://github.com/your-username/stock-realtime-brief",
    )
    parser.add_argument(
        "--mode",
        choices=["portfolio", "single", "multi", "auto"],
        default="auto",
        help="分析模式（默认 auto，根据输入自判）",
    )
    parser.add_argument("--portfolio", help="portfolio.json 路径（模式 P）")
    parser.add_argument("--code", help="股票代码（模式 S）")
    parser.add_argument(
        "--codes",
        help="股票代码列表，逗号分隔（模式 M）",
    )
    parser.add_argument(
        "--skip-announce",
        action="store_true",
        help="跳过公告拉取（提速，仅模式 P 有效）",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.2.0",
    )

    args = parser.parse_args(argv)

    # 模式判定
    mode = args.mode
    if mode == "auto":
        if args.portfolio:
            mode = "portfolio"
        elif args.code:
            mode = "single"
        elif args.codes:
            n = len([c for c in args.codes.split(",") if c.strip()])
            mode = "single" if n == 1 else "multi"
        else:
            # 尝试找默认 portfolio
            from .portfolio import resolve_portfolio_path
            if resolve_portfolio_path():
                mode = "portfolio"
            else:
                parser.error("需要提供 --portfolio / --code / --codes 之一")

    # 执行
    try:
        if mode == "portfolio":
            result = analyze_portfolio(args.portfolio, skip_announce=args.skip_announce)
        elif mode == "single":
            code = args.code or args.codes.split(",")[0].strip()
            result = analyze_single(code)
        elif mode == "multi":
            codes = [c.strip() for c in args.codes.split(",") if c.strip()]
            result = analyze_multi(codes)
        else:
            parser.error(f"未知模式: {mode}")
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"分析失败: {e}", file=sys.stderr)
        return 2

    print(result.markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
