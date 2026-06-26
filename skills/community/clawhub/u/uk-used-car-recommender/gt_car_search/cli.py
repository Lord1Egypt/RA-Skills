"""gt-car-search installable CLI entrypoint."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from scripts.cars.scraper import run_car_search
from scripts.cars.urls import (
    BODY_TYPES,
    COLOUR_OPTIONS,
    DOOR_OPTIONS,
    ENGINE_SIZE_OPTIONS,
    FUEL_TYPES,
    MILEAGE_OPTIONS,
    MPG_OPTIONS,
    SEAT_OPTIONS,
    SELLER_TYPE_OPTIONS,
    SORT_OPTIONS,
    TRANSMISSION_TYPES,
    YEAR_OPTIONS,
    build_car_search_url,
)

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def _output(data: dict[str, Any], exit_code: int = 0) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def _load_mock_file(path: str | None) -> str | None:
    if not path:
        return None
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = (Path(__file__).resolve().parent.parent / path).resolve()
    return file_path.read_text(encoding="utf-8")


# ── 子命令处理函数 ────────────────────────────────────────────────────────────

def cmd_search(args: argparse.Namespace) -> None:
    seller_types = args.seller_type if args.seller_type else None
    search_url = build_car_search_url(
        keyword=args.keyword or "",
        search_location=args.location,
        sort=args.sort,
        distance=args.distance,
        min_price=args.min_price,
        max_price=args.max_price,
        make=args.make,
        model=args.model,
        fuel_type=args.fuel_type,
        transmission=args.transmission,
        body_type=args.body_type,
        mileage=args.mileage,
        year=args.year,
        engine_size=args.engine_size,
        colour=args.colour,
        doors=args.doors,
        seats=args.seats,
        avg_mpg=args.avg_mpg,
        seller_types=seller_types,
    )
    mock_html = _load_mock_file(args.mock_file)
    result = run_car_search(
        search_url=search_url,
        limit=args.limit,
        sort=args.sort,
        mock_html=mock_html,
        timeout=args.timeout,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_build_url(args: argparse.Namespace) -> None:
    seller_types = args.seller_type if args.seller_type else None
    url = build_car_search_url(
        keyword=args.keyword or "",
        search_location=args.location,
        sort=args.sort,
        distance=args.distance,
        min_price=args.min_price,
        max_price=args.max_price,
        make=args.make,
        model=args.model,
        fuel_type=args.fuel_type,
        transmission=args.transmission,
        body_type=args.body_type,
        mileage=args.mileage,
        year=args.year,
        engine_size=args.engine_size,
        colour=args.colour,
        doors=args.doors,
        seats=args.seats,
        avg_mpg=args.avg_mpg,
        seller_types=seller_types,
    )
    _output({"ok": True, "search_url": url})


def cmd_list_options(_args: argparse.Namespace) -> None:
    _output({
        "ok": True,
        "options": {
            "sort": SORT_OPTIONS,
            "fuel_type": FUEL_TYPES,
            "transmission": TRANSMISSION_TYPES,
            "body_type": BODY_TYPES,
            "mileage": MILEAGE_OPTIONS,
            "year": YEAR_OPTIONS,
            "engine_size": ENGINE_SIZE_OPTIONS,
            "colour": COLOUR_OPTIONS,
            "doors": DOOR_OPTIONS,
            "seats": SEAT_OPTIONS,
            "avg_mpg": MPG_OPTIONS,
            "seller_type": SELLER_TYPE_OPTIONS,
        },
    })


# ── 共用参数构建器 ────────────────────────────────────────────────────────────

def _add_filter_args(sub: argparse.ArgumentParser) -> None:
    """将所有搜索筛选参数添加到子命令解析器。"""
    sub.add_argument("--keyword", "-k", default="", help="搜索关键词（如车型名称）")
    sub.add_argument(
        "--location", "-l", default="uk",
        help="搜索地点，如 'uk'、'London'、'Manchester'（默认: uk）",
    )
    sub.add_argument("--distance", type=int, default=None, help="搜索半径（英里）")
    sub.add_argument("--min-price", type=int, default=None, help="最低价格（英镑）")
    sub.add_argument("--max-price", type=int, default=None, help="最高价格（英镑）")
    sub.add_argument(
        "--make", default=None,
        help="品牌，如 toyota、ford、bmw、volkswagen",
    )
    sub.add_argument(
        "--model", default=None,
        help="车型，如 yaris、focus、3-series",
    )
    sub.add_argument(
        "--fuel-type", choices=FUEL_TYPES, default=None,
        metavar=f"{{{','.join(FUEL_TYPES)}}}",
        help="燃油类型",
    )
    sub.add_argument(
        "--transmission", choices=TRANSMISSION_TYPES, default=None,
        metavar=f"{{{','.join(TRANSMISSION_TYPES)}}}",
        help="变速箱类型",
    )
    sub.add_argument(
        "--body-type", choices=BODY_TYPES, default=None,
        metavar=f"{{{','.join(BODY_TYPES)}}}",
        help="车身类型",
    )
    sub.add_argument(
        "--mileage", choices=MILEAGE_OPTIONS, default=None,
        metavar=f"{{{','.join(MILEAGE_OPTIONS)}}}",
        help="里程上限",
    )
    sub.add_argument(
        "--year", choices=YEAR_OPTIONS, default=None,
        metavar=f"{{{','.join(YEAR_OPTIONS)}}}",
        help="车龄（注册年限），如 up_to_5 表示 5 年以内",
    )
    sub.add_argument(
        "--engine-size", choices=ENGINE_SIZE_OPTIONS, default=None,
        metavar=f"{{{','.join(ENGINE_SIZE_OPTIONS)}}}",
        help="发动机排量",
    )
    sub.add_argument(
        "--colour", choices=COLOUR_OPTIONS, default=None,
        metavar=f"{{{','.join(COLOUR_OPTIONS)}}}",
        help="车身颜色",
    )
    sub.add_argument(
        "--doors", type=int, choices=DOOR_OPTIONS, default=None,
        help="车门数量（2/3/4/5）",
    )
    sub.add_argument(
        "--seats", type=int, choices=SEAT_OPTIONS, default=None,
        help=f"座位数（{'/'.join(str(s) for s in SEAT_OPTIONS)}）",
    )
    sub.add_argument(
        "--avg-mpg", choices=MPG_OPTIONS, default=None,
        metavar=f"{{{','.join(MPG_OPTIONS)}}}",
        help="平均油耗下限（MPG）：over_30≈9.4L/100km、over_40≈7.1L/100km、over_50≈5.6L/100km、over_60≈4.7L/100km",
    )
    sub.add_argument(
        "--seller-type", choices=SELLER_TYPE_OPTIONS, action="append", default=None,
        metavar=f"{{{','.join(SELLER_TYPE_OPTIONS)}}}",
        help="卖家类型，可多次指定（trade / private）",
    )
    sub.add_argument(
        "--sort", choices=SORT_OPTIONS, default=None,
        metavar=f"{{{','.join(SORT_OPTIONS)}}}",
        help="排序方式",
    )


# ── 解析器构建 ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gt-car-search",
        description="Gumtree 二手车搜索 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 搜索伦敦附近 5000 英镑以内的丰田汽车
  gt-car-search search --make toyota --max-price 5000 --location London --sort date

  # 搜索手动挡柴油 SUV，5 年以内，3 万英里以内
  gt-car-search search --fuel-type diesel --transmission manual --body-type suv --year up_to_5 --mileage up_to_30000

  # 仅构建搜索 URL 不发起请求
  gt-car-search build-url --make bmw --model 3-series --year up_to_3

  # 查看所有可选参数值
  gt-car-search list-options
""",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── search 子命令 ──────────────────────────────────────────────────────────
    sub_search = subparsers.add_parser(
        "search",
        help="搜索 Gumtree 二手车并返回帖子信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
输出字段说明（每条 item）:
  listing_id      帖子 ID
  title           标题
  description     描述摘要
  price           标价（原始值）
  price_pennies   标价（便士）
  location        所在地
  url             帖子链接
  age             发布时长
  is_trade        是否为商家卖家
  category        分类名称
  promotions      推广标签列表
  number_of_images  图片数量
  is_delivery     是否支持配送
  is_gbg_verified 是否通过 GBG 认证
""",
    )
    _add_filter_args(sub_search)
    sub_search.add_argument("--limit", type=int, default=10, help="返回结果数量（默认: 10）")
    sub_search.add_argument("--timeout", type=int, default=30, help="请求超时秒数（默认: 30）")
    sub_search.add_argument(
        "--mock-file",
        default=None,
        help="使用本地 HTML 文件替代网络请求（用于测试）",
    )
    sub_search.set_defaults(func=cmd_search)

    # ── build-url 子命令 ───────────────────────────────────────────────────────
    sub_url = subparsers.add_parser(
        "build-url",
        help="根据参数构建搜索 URL（不发起请求）",
    )
    _add_filter_args(sub_url)
    sub_url.set_defaults(func=cmd_build_url)

    # ── list-options 子命令 ────────────────────────────────────────────────────
    sub_opts = subparsers.add_parser(
        "list-options",
        help="列出所有筛选参数的可选值",
    )
    sub_opts.set_defaults(func=cmd_list_options)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as exc:  # pragma: no cover
        _output({"ok": False, "error": f"未知错误: {exc}"}, exit_code=2)


if __name__ == "__main__":
    main()
