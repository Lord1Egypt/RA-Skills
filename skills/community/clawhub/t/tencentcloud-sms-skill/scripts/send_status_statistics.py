#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 — 发送短信统计 (SendStatusStatistics)

按 yyyymmddhh 时间区间统计提交侧数据：
- FeeCount         : 计费条数
- RequestCount     : 提交量
- RequestSuccessCount : 提交成功量

与 CallbackStatusStatistics 区别：
- 本接口统计「提交侧」数据；CallbackStatusStatistics 统计「运营商回执侧」结果分布。
- 本接口 SDK 注释未声明 32 天硬限制，脚本仅校验 EndTime >= BeginTime。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python send_status_statistics.py --sdk-app-id "1400006666" \\
        --begin-time "2025010100" --end-time "2025013123"
"""

import argparse
import json
import os
import sys
from datetime import datetime

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


def parse_yyyymmddhh(value, field):
    """校验 yyyymmddhh 格式并返回 datetime 对象。"""
    if not value or len(value) != 10 or not value.isdigit():
        output_error(
            "INVALID_PARAMETER",
            f"{field} 格式错误，需为 yyyymmddhh（如 2025010100），实际值: {value}",
        )
    try:
        return datetime.strptime(value, "%Y%m%d%H")
    except ValueError:
        output_error(
            "INVALID_PARAMETER",
            f"{field} 不是合法日期时间: {value}",
        )


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云短信 — 发送短信统计 (SendStatusStatistics)"
    )
    parser.add_argument("--sdk-app-id", required=True, help="短信 SdkAppId")
    parser.add_argument(
        "--begin-time", required=True,
        help="起始时间，格式 yyyymmddhh（如 2025010100）",
    )
    parser.add_argument(
        "--end-time", required=True,
        help="结束时间，格式 yyyymmddhh（如 2025013123），需 >= BeginTime",
    )
    add_common_args(parser)
    return parser


def main():
    args = build_parser().parse_args()

    begin_dt = parse_yyyymmddhh(args.begin_time, "--begin-time")
    end_dt = parse_yyyymmddhh(args.end_time, "--end-time")
    if end_dt < begin_dt:
        output_error(
            "INVALID_PARAMETER",
            f"--end-time ({args.end_time}) 必须 >= --begin-time ({args.begin_time})",
        )

    params = {
        "SmsSdkAppId": args.sdk_app_id,
        "BeginTime": args.begin_time,
        "EndTime": args.end_time,
        "Limit": 0,
        "Offset": 0,
    }

    if args.dry_run:
        output_json({
            "dry_run": True,
            "api": "SendStatusStatistics",
            "params": params,
        })
        return

    cred = get_credentials()
    client = build_client(cred, region=args.region)

    try:
        req = models.SendStatusStatisticsRequest()
        req.from_json_string(json.dumps(params))
        resp = client.SendStatusStatistics(req)
        output_json(json.loads(resp.to_json_string()))
    except TencentCloudSDKException as e:
        from _common import handle_api_error
        handle_api_error(e)
    except Exception as e:  # pylint: disable=broad-except
        output_error("UNEXPECTED_ERROR", str(e))


if __name__ == "__main__":
    main()
