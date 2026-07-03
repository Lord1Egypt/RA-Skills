#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 — 套餐包信息统计 (SmsPackagesStatistics)

查询指定时间段内创建的套餐包统计信息。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python packages_statistics.py --sdk-app-id "1400006666" \
        --begin-time "2025010100" --end-time "2025033123"
"""

import argparse
import json
import os
import sys
import time

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


def format_timestamp(ts):
    """将 Unix 时间戳转为可读时间字符串。"""
    if ts and ts > 0:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    return None


def format_packages(packages):
    """为套餐包信息增加可读的时间和用量描述。"""
    for pkg in packages:
        if "PackageCreateTime" in pkg:
            pkg["PackageCreateTimeStr"] = format_timestamp(pkg["PackageCreateTime"])
        if "PackageExpiredTime" in pkg:
            pkg["PackageExpiredTimeStr"] = format_timestamp(pkg["PackageExpiredTime"])
        if "PackageEffectiveTime" in pkg:
            pkg["PackageEffectiveTimeStr"] = format_timestamp(pkg["PackageEffectiveTime"])
        amount = pkg.get("PackageAmount", 0)
        usage = pkg.get("CurrentUsage", 0)
        pkg["RemainingAmount"] = amount - usage
        if amount > 0:
            pkg["UsagePercent"] = f"{usage / amount * 100:.1f}%"
    return packages


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云短信 — 套餐包信息统计 (SmsPackagesStatistics)"
    )
    parser.add_argument("--sdk-app-id", required=True, help="短信 SdkAppId")
    parser.add_argument("--begin-time", required=True, help="起始时间，格式 yyyymmddhh（如 2025010100）")
    parser.add_argument("--end-time", required=True, help="结束时间，格式 yyyymmddhh（如 2025033123）")
    parser.add_argument("--limit", type=int, default=100, help="返回数量上限，默认 100，最大 500")
    parser.add_argument("--offset", type=int, default=0, help="偏移量，默认 0")
    add_common_args(parser)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    params = {
        "SmsSdkAppId": args.sdk_app_id,
        "Limit": min(args.limit, 500),
        "Offset": args.offset,
        "BeginTime": args.begin_time,
        "EndTime": args.end_time,
    }

    if args.dry_run:
        output_json({"dry_run": True, "api": "SmsPackagesStatistics", "params": params})
        return

    cred = get_credentials()
    client = build_client(cred, region=args.region)

    try:
        req = models.SmsPackagesStatisticsRequest()
        req.from_json_string(json.dumps(params))
        resp = client.SmsPackagesStatistics(req)
        result = json.loads(resp.to_json_string())

        if "SmsPackagesStatisticsSet" in result:
            result["SmsPackagesStatisticsSet"] = format_packages(
                result["SmsPackagesStatisticsSet"]
            )

        output_json(result)
    except TencentCloudSDKException as e:
        from _common import handle_api_error
        handle_api_error(e)
    except Exception as e:  # pylint: disable=broad-except
        output_error("UNEXPECTED_ERROR", str(e))


if __name__ == "__main__":
    main()
