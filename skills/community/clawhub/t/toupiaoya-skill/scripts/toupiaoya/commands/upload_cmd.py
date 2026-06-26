from __future__ import annotations

import argparse
import json
import sys
from hashlib import md5
from pathlib import Path
from typing import Any, Mapping

import requests

try:
    from qcloud_cos.cos_exception import CosClientError, CosServiceError
except ImportError:

    class CosClientError(Exception):
        """占位：未安装 cos-python-sdk-v5 时仅占位类型，避免 isinstance 使用非法元组。"""

    class CosServiceError(Exception):
        """占位：未安装 cos-python-sdk-v5 时仅占位类型。"""

from toupiaoya.auth import resolve_token
from toupiaoya.constants import (
    BROWSER_CHROME_UA,
    DEFAULT_COS_BUCKET,
    DEFAULT_COS_PREFIX,
    DEFAULT_TIMEOUT,
    DEFAULT_MATERIAL_SOURCE,
)
from toupiaoya.cos_upload import build_object_key, fetch_cos_token, put_local_file
from toupiaoya.http import get
from toupiaoya.material_api import build_save_file_payload, save_material_file

_PASSPORT_USER_INFO_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "origin": "https://www.toupiaoya.com",
    "user-agent": BROWSER_CHROME_UA,
}


def fetch_user_info(access_token: str, *, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """GET /user/info，获取当前 token 对应用户信息。"""
    res = get(
        "https://passport.toupiaoya.com/user/info",
        access_token=access_token,
        extra_headers=dict(_PASSPORT_USER_INFO_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("user/info 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取用户信息失败"))
    return body


def extract_user_id_from_user_info(body: Mapping[str, Any]) -> str:
    """从 user/info 响应中提取 userId。"""
    obj = body.get("obj")
    if not isinstance(obj, dict):
        raise RuntimeError("user/info 返回缺少 obj")
    score_info = obj.get("userScoreInfo")
    if isinstance(score_info, dict):
        uid = str(score_info.get("userId") or "").strip()
        if uid:
            return uid
    members = obj.get("members")
    if isinstance(members, list):
        for member in members:
            if not isinstance(member, dict):
                continue
            uid = str(member.get("userId") or "").strip()
            if uid:
                return uid
    raise RuntimeError("user/info 未返回有效 userId")


def register(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "upload",
        help="COS 上传后登记到投票鸭素材库（token-upload → PutObject → saveFile）",
    )
    p.add_argument("--file", type=str, required=True, help="本地文件路径")
    p.add_argument("--bucket", type=str, default=DEFAULT_COS_BUCKET, help=f"业务 bucket 名（默认 {DEFAULT_COS_BUCKET}）")
    p.add_argument(
        "--prefix",
        type=str,
        default=DEFAULT_COS_PREFIX,
        help=f"与 token-upload 一致的 prefix（默认 {DEFAULT_COS_PREFIX!r}）",
    )
    p.add_argument(
        "--name",
        type=str,
        required=False,
        default=None,
        help="COS 对象名（prefix 下）；默认使用本地文件 basename",
    )
    p.add_argument(
        "--tmb-path",
        type=str,
        required=False,
        default=None,
        help="saveFile 的 tmbPath；默认与 COS path（key）相同",
    )
    p.add_argument(
        "--source",
        type=str,
        default=DEFAULT_MATERIAL_SOURCE,
        help=f"saveFile 的 source（默认 {DEFAULT_MATERIAL_SOURCE!r}）",
    )
    p.add_argument("--tag-id", type=int, default=-1, help="saveFile 的 tagId（默认 -1）")
    p.add_argument("--file-type", type=int, default=1, help="saveFile 的 fileType（默认 1，图片）")
    p.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )


def run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    _ = parser
    path = Path(args.file).expanduser()
    if not path.is_file():
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": f"文件不存在或不是普通文件: {path}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    token = resolve_token(getattr(args, "access_token", None))
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

    object_name = (args.name or path.name).strip()
    if not object_name:
        print(
            json.dumps({"success": False, "code": 400, "msg": "对象名不能为空"}, ensure_ascii=False, indent=2)
        )
        raise SystemExit(1)

    try:
        user_info = fetch_user_info(token)
        user_id = extract_user_id_from_user_info(user_info)
        ext = path.suffix.lstrip(".")
        hashed_name = md5(object_name.encode("utf-8")).hexdigest()
        filename = f"{hashed_name}.{ext}" if ext else hashed_name
        object_key = build_object_key(args.prefix, f"{user_id}/{filename}")
        inner = fetch_cos_token(
            token,
            bucket=args.bucket,
            prefix=args.prefix,
        )
        cos_result = put_local_file(inner, path, object_key)
    except ImportError as e:
        print(
            json.dumps(
                {"success": False, "code": 500, "msg": str(e)},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
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
                {"success": False, "code": 502, "msg": f"获取用户信息或 COS 凭证 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    except Exception as e:
        if isinstance(e, CosServiceError):
            detail = e.get_digest_msg() if hasattr(e, "get_digest_msg") else str(e)
            print(
                json.dumps(
                    {
                        "success": False,
                        "code": 502,
                        "msg": "COS 上传失败",
                        "detail": detail,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            raise SystemExit(1) from e
        if isinstance(e, CosClientError):
            print(
                json.dumps(
                    {"success": False, "code": 502, "msg": f"COS 客户端错误: {e}"},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            raise SystemExit(1) from e
        print(
            json.dumps(
                {"success": False, "code": 500, "msg": str(e)},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e

    try:
        save_payload = build_save_file_payload(
            cos_key=cos_result["key"],
            local_path=path,
            logical_bucket=args.bucket,
            source=args.source,
            tag_id=args.tag_id,
            file_type=args.file_type,
            tmb_path=args.tmb_path,
        )
        material_obj = save_material_file(token, save_payload)
    except RuntimeError as e:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 502,
                    "msg": str(e),
                    "cos": {k: cos_result.get(k) for k in ("bucket", "region", "key", "etag", "assetUrl")},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 502,
                    "msg": f"素材库 saveFile HTTP 失败: {e}",
                    "cos": {k: cos_result.get(k) for k in ("bucket", "region", "key", "etag", "assetUrl")},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e

    out = {
        "success": True,
        "code": 200,
        "msg": "ok",
        "cos": {k: cos_result.get(k) for k in ("bucket", "region", "key", "etag", "assetUrl")},
        "material": material_obj,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
