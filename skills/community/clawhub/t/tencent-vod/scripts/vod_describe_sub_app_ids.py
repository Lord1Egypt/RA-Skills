#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 子应用列表查询脚本
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vod_auto_upgrade import check_sdk_version


# 软依赖：vod_load_env 用于在凭证缺失时从 ~/.env 等 dotenv 文件兜底加载
try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

check_sdk_version()

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("错误：请先安装腾讯云 SDK: pip install tencentcloud-sdk-python")
    sys.exit(1)


DEFAULT_REGION = "ap-guangzhou"
MAX_LIMIT = 200


def get_credential():
    """获取腾讯云认证信息。若环境变量缺失则尝试从 dotenv 文件自动加载。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        # 兜底：尝试从 ~/.env 等 dotenv 文件加载
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] 环境变量未设置，尝试从 dotenv 文件自动加载...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from vod_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print("错误：请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
            sys.exit(1)

    return credential.Credential(secret_id, secret_key)


def get_client(region=DEFAULT_REGION):
    """获取 VOD 客户端"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


def normalize_tags(tag_args):
    """解析标签参数 KEY=VALUE 为接口所需结构"""
    if not tag_args:
        return []

    tags = []
    for raw_tag in tag_args:
        if "=" not in raw_tag:
            print(f"错误：标签参数格式错误：{raw_tag}，请使用 KEY=VALUE 格式")
            sys.exit(1)

        tag_key, tag_value = raw_tag.split("=", 1)
        tag_key = tag_key.strip()
        tag_value = tag_value.strip()

        if not tag_key:
            print(f"错误：标签键不能为空：{raw_tag}")
            sys.exit(1)

        tags.append({
            "TagKey": tag_key,
            "TagValue": tag_value,
        })

    return tags


def validate_args(args):
    """校验分页参数"""
    if args.offset is not None and args.offset < 0:
        print("错误：--offset 不能小于 0")
        sys.exit(1)

    if args.limit is not None and not 1 <= args.limit <= MAX_LIMIT:
        print(f"错误：--limit 必须在 1 到 {MAX_LIMIT} 之间")
        sys.exit(1)


def build_request_payload(args):
    """构造请求参数"""
    validate_args(args)

    payload = {}

    if args.name:
        payload["Name"] = args.name

    tags = normalize_tags(args.tag)
    if tags:
        payload["Tags"] = tags

    if args.offset is not None:
        payload["Offset"] = args.offset

    if args.limit is not None:
        payload["Limit"] = args.limit

    return payload


def build_request(args):
    """构造 SDK 请求对象"""
    payload = build_request_payload(args)
    req = models.DescribeSubAppIdsRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    return req, payload


def format_tags(tags):
    """格式化标签输出"""
    if not tags:
        return "无"
    return ", ".join(
        f"{tag.get('TagKey', '')}={tag.get('TagValue', '')}"
        for tag in tags
    )


def format_regions(regions):
    """格式化地域输出"""
    if not regions:
        return "无"
    return ", ".join(regions)


def print_human_readable(result, printer=print):
    """输出易读格式结果"""
    total_count = result.get("TotalCount", 0)
    sub_app_list = result.get("SubAppIdInfoSet", [])
    request_id = result.get("RequestId", "N/A")

    printer("查询完成!")
    printer(f"本次返回应用数: {len(sub_app_list)}")
    printer(f"应用总数: {total_count}")
    printer(f"RequestId: {request_id}")

    if not sub_app_list:
        printer("未查询到符合条件的子应用。")
        return

    for index, item in enumerate(sub_app_list, start=1):
        printer(f"\n[{index}] SubAppId: {item.get('SubAppId', 'N/A')}")
        printer(f"  名称: {item.get('SubAppIdName') or item.get('Name') or 'N/A'}")
        printer(f"  简介: {item.get('Description') or 'N/A'}")
        printer(f"  状态: {item.get('Status') or 'N/A'}")
        printer(f"  模式: {item.get('Mode') or 'N/A'}")
        printer(f"  创建时间: {item.get('CreateTime') or 'N/A'}")
        printer(f"  存储地域: {format_regions(item.get('StorageRegions'))}")
        printer(f"  标签: {format_tags(item.get('Tags'))}")


def describe_sub_app_ids(args, client=None, printer=print):
    """查询子应用列表"""
    req, payload = build_request(args)

    if args.dry_run:
        printer("[DRY RUN] 请求参数:")
        printer(json.dumps(payload, indent=2, ensure_ascii=False))
        return payload

    if client is None:
        client = get_client(args.region)

    try:
        resp = client.DescribeSubAppIds(req)
        result = json.loads(resp.to_json_string())

        if args.json:
            printer(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_human_readable(result, printer=printer)

        return result
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        printer(f"查询失败: {e}")
        sys.exit(1)


def create_parser():
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        description="VOD 子应用列表查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查询所有子应用
  python vod_describe_sub_app_ids.py

  # 按应用名称查询
  python vod_describe_sub_app_ids.py --name MyAppName

  # 按标签查询
  python vod_describe_sub_app_ids.py --tag env=prod --tag team=media

  # 分页查询并输出 JSON
  python vod_describe_sub_app_ids.py --offset 0 --limit 20 --json
        """,
    )

    parser.add_argument("--name", help="按应用名称过滤")
    parser.add_argument(
        "--tag",
        action="append",
        help="按标签过滤，格式 KEY=VALUE，可重复传入",
    )
    parser.add_argument("--offset", type=int, help="分页起始偏移量，默认 0")
    parser.add_argument("--limit", type=int, help="分页返回数量，范围 1-200")
    parser.add_argument("--region", default=DEFAULT_REGION, help="地域")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--dry-run", action="store_true", help="预览请求参数")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    describe_sub_app_ids(args)


if __name__ == "__main__":
    main()
