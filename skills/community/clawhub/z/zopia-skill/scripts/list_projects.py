#!/usr/bin/env python3
"""列出 Zopia 项目。

用法:
    python list_projects.py
    python list_projects.py --page 2 --page-size 20

返回:
    {data: [...], page, pageSize, hasMore}
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import build_project_url, list_projects, print_json


def main() -> None:
    parser = argparse.ArgumentParser(description="列出 Zopia 项目")
    parser.add_argument("--page", type=int, default=1, help="页码（默认 1）")
    parser.add_argument("--page-size", type=int, default=12, help="每页数量（默认 12，最大 50）")
    args = parser.parse_args()

    result = list_projects(args.page, args.page_size)
    for item in result.get("data", []):
        item["projectUrl"] = build_project_url(item.get("id", ""))
    print_json(result)


if __name__ == "__main__":
    main()
