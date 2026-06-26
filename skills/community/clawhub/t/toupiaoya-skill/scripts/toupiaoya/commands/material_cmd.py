from __future__ import annotations

import argparse
import json
import sys

import requests

from toupiaoya.auth import resolve_token
from toupiaoya.material_api import fetch_user_upload_list


def register(subparsers: argparse._SubParsersAction) -> None:
    material_parser = subparsers.add_parser("material", help="素材库相关命令")
    mat_sub = material_parser.add_subparsers(dest="material_command")

    list_p = mat_sub.add_parser("list", help="用户上传图片列表（fileType=1）")
    list_p.add_argument("--pageNo", type=int, default=1, help="页码，默认 1")
    list_p.add_argument("--pageSize", type=int, default=30, help="每页条数，默认 30")
    list_p.add_argument("--tagId", type=int, default=-1, help="标签 id，默认 -1")
    list_p.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )


def run_material(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    sub = getattr(args, "material_command", None)
    if sub != "list":
        parser.print_help()
        raise SystemExit(1)

    token_cli = getattr(args, "access_token", None)
    token = resolve_token(token_cli)
    if not token:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 401,
                    "msg": "缺少 X-Openclaw-Token：请先执行 `login` 或传 --access-token。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    try:
        data = fetch_user_upload_list(
            token,
            file_type=1,
            page_no=getattr(args, "pageNo", 1),
            page_size=getattr(args, "pageSize", 30),
            tag_id=getattr(args, "tagId", -1),
        )
    except RuntimeError as e:
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": str(e)},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"素材列表 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e

    print(json.dumps(data, ensure_ascii=False, indent=2))
