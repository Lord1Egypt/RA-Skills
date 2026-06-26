from __future__ import annotations

import argparse
import json
from typing import Any

from toupiaoya.search import ToupiaoyaStoreWebSearch


def register(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser("search", help="搜索投票模板")
    p.add_argument("--keywords", type=str, required=False, help="关键词")
    p.add_argument("--pageNo", type=int, required=False, default=1, help="分页页码")
    p.add_argument("--pageSize", type=int, required=False, default=10, help="每页条数")
    p.add_argument(
        "--sortBy",
        type=str,
        required=False,
        default="common_total|desc",
        help="排序字段，如 common_total|desc",
    )
    p.add_argument(
        "--color",
        type=str,
        required=False,
        default=None,
        help="颜色，如 紫色、蓝色、粉色、红色、绿色、青色、橙色、黄色、黑色、白色、灰色",
    )


def run(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> None:
    search = ToupiaoyaStoreWebSearch()
    result: dict[str, Any] = search.execute(
        getattr(args, "keywords", None),
        getattr(args, "pageNo", 1),
        getattr(args, "pageSize", 10),
        sort_by=getattr(args, "sortBy", "common_total|desc"),
        color=getattr(args, "color", None),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
