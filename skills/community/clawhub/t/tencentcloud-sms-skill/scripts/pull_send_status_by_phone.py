#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 — 按手机号拉取下发状态 (PullSmsSendStatusByPhoneNumber)

按 UNIX 秒时间区间 + 单个 E.164 手机号拉取下发状态明细，
返回：UserReceiveTime（用户接收时间）、SerialNo、ReportStatus(SUCCESS/FAIL)、
Description、SessionContext 等。

时间窗口: 最多可拉取当前时间往前 7 天。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    # 默认最近 24 小时
    python pull_send_status_by_phone.py --sdk-app-id "1400006666" \\
        --phone-number "+8618501234444"

    # 指定 UNIX 秒时间区间
    python pull_send_status_by_phone.py --sdk-app-id "1400006666" \\
        --phone-number "+8618501234444" \\
        --begin-time 1715000000 --end-time 1715086400

    # 指定本地时间字符串
    python pull_send_status_by_phone.py --sdk-app-id "1400006666" \\
        --phone-number "+8618501234444" \\
        --begin-datetime "2025-05-01 00:00:00" \\
        --end-datetime   "2025-05-02 00:00:00"
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    ensure_dependencies,
    add_common_args,
    add_pull_by_phone_args,
    run_pull_by_phone,
)

ensure_dependencies()

from tencentcloud.sms.v20210111 import models  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云短信 — 按手机号拉取下发状态 (PullSmsSendStatusByPhoneNumber)"
    )
    add_pull_by_phone_args(parser)
    add_common_args(parser)
    return parser


def main():
    args = build_parser().parse_args()
    run_pull_by_phone(
        args,
        api_name="PullSmsSendStatusByPhoneNumber",
        request_cls=models.PullSmsSendStatusByPhoneNumberRequest,
        client_method_name="PullSmsSendStatusByPhoneNumber",
    )


if __name__ == "__main__":
    main()
