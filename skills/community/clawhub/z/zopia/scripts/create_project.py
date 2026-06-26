#!/usr/bin/env python3
"""创建 Zopia 项目。

用法:
    python create_project.py [项目名称]

返回:
    {baseId, baseName, episodeId, projectUrl}
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import build_project_url, create_project, print_json


def main() -> None:
    parser = argparse.ArgumentParser(description="创建 Zopia 项目")
    parser.add_argument("name", nargs="?", default=None, help="项目名称（可选）")
    args = parser.parse_args()

    result = create_project(args.name)
    base_id = result.get("baseId", "")
    result["projectUrl"] = build_project_url(base_id)
    print_json(result)


if __name__ == "__main__":
    main()
