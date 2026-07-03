#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 — 查询短信签名状态 (DescribeSmsSignList)

查询短信签名的审核状态。仅企业认证用户可调用此接口。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python describe_sign.py --sign-id-set 1110 1111 --international 0
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    ensure_dependencies,
    get_credentials,
    build_client,
    output_json,
    output_error,
    add_common_args,
)

ensure_dependencies()

from tencentcloud.common.exception.tencent_cloud_sdk_exception import (  # noqa: E402
    TencentCloudSDKException,
)
from tencentcloud.sms.v20210111 import models  # noqa: E402


STATUS_MAP = {
    0: "已通过",
    1: "待审核",
    2: "已拒绝",
}


def format_sign_status(sign_list):
    """格式化签名状态列表，增加可读状态描述。"""
    for sign in sign_list:
        status_code = sign.get("StatusCode")
        if status_code is not None:
            sign["StatusDesc"] = STATUS_MAP.get(status_code, f"未知({status_code})")
    return sign_list


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云短信 — 查询短信签名状态 (DescribeSmsSignList)"
    )
    parser.add_argument(
        "--sign-id-set", type=int, nargs="*", default=None,
        help="签名 ID 列表（空格分隔），不填则分页查询全部签名，最多 100 个",
    )
    parser.add_argument(
        "--international", type=int, required=True,
        choices=[0, 1],
        help="0=国内短信, 1=国际/港澳台短信",
    )
    parser.add_argument("--limit", type=int, default=10, help="返回数量上限，默认 10，最大 100（仅分页模式）")
    parser.add_argument("--offset", type=int, default=0, help="偏移量，默认 0（仅分页模式）")
    add_common_args(parser)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    params = {
        "International": args.international,
    }

    if args.sign_id_set:
        if len(args.sign_id_set) > 100:
            output_error("PARAM_ERROR", "签名 ID 数量不能超过 100 个")
        params["SignIdSet"] = args.sign_id_set
    else:
        # 分页查询全部签名
        params["Limit"] = min(args.limit, 100)
        params["Offset"] = args.offset

    if args.dry_run:
        output_json({"dry_run": True, "api": "DescribeSmsSignList", "params": params})
        return

    cred = get_credentials()
    client = build_client(cred, region=args.region)

    try:
        req = models.DescribeSmsSignListRequest()
        req.from_json_string(json.dumps(params))
        resp = client.DescribeSmsSignList(req)
        result = json.loads(resp.to_json_string())

        if "DescribeSignListStatusSet" in result:
            result["DescribeSignListStatusSet"] = format_sign_status(
                result["DescribeSignListStatusSet"]
            )

        output_json(result)
    except TencentCloudSDKException as e:
        from _common import handle_api_error
        handle_api_error(e)
    except Exception as e:  # pylint: disable=broad-except
        output_error("UNEXPECTED_ERROR", str(e))


if __name__ == "__main__":
    main()
