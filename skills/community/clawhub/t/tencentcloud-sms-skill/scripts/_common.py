#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 Skill 公共模块

提供所有脚本共用的功能：环境变量加载、依赖安装、凭证读取、客户端构建。
"""

import json
import os
import subprocess
import sys

# 复用 check_env.py 的环境变量加载逻辑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_env import _load_from_files  # noqa: E402

# 模块加载时自动从配置文件加载环境变量
_load_from_files()

DEFAULT_REGION = "ap-guangzhou"


def ensure_dependencies():
    """检测并自动安装 tencentcloud-sdk-python 依赖。"""
    try:
        import tencentcloud  # noqa: F401  # pylint: disable=unused-import
    except ImportError:
        print("[INFO] tencentcloud-sdk-python not found. Installing...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "tencentcloud-sdk-python", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] tencentcloud-sdk-python installed successfully.", file=sys.stderr)


def get_credentials():
    """从环境变量读取腾讯云 API 密钥，缺失时输出结构化错误并退出。"""
    from tencentcloud.common import credential

    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        missing = []
        if not secret_id:
            missing.append("TENCENTCLOUD_SECRET_ID")
        if not secret_key:
            missing.append("TENCENTCLOUD_SECRET_KEY")
        print(json.dumps({
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": "缺少腾讯云 API 密钥，请通过环境变量配置。",
            "missing": missing,
            "help": "前往 https://console.cloud.tencent.com/cam/capi 获取密钥",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def build_client(cred, region=None):
    """构建 SMS API 客户端。

    Args:
        cred: 腾讯云凭证对象
        region: 地域（默认 ap-guangzhou）
    """
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.sms.v20210111 import sms_client

    http_profile = HttpProfile()
    http_profile.endpoint = "sms.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return sms_client.SmsClient(cred, region or DEFAULT_REGION, client_profile)


def output_json(data):
    """将结果以 JSON 格式输出到 stdout。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def output_error(error_type, message, code=None):
    """输出结构化错误 JSON 并退出。"""
    err = {"error": error_type, "message": message}
    if code:
        err["code"] = code
    print(json.dumps(err, ensure_ascii=False, indent=2))
    sys.exit(1)



# 常见错误码的友好提示映射
FRIENDLY_ERROR_HINTS = {
    "FailedOperation.NotEnterpriseCertification": {
        "hint": "您的账号为个人认证，签名/模板增查 API 仅支持企业认证用户。",
        "actions": [
            "前往控制台手动操作: https://console.cloud.tencent.com/smsv2",
            "或升级为企业认证: https://console.cloud.tencent.com/developer/auth",
        ],
    },
    "AuthFailure.SecretIdNotFound": {
        "hint": "SecretId 不存在，请检查环境变量 TENCENTCLOUD_SECRET_ID 是否正确。",
        "actions": ["前往密钥管理确认: https://console.cloud.tencent.com/cam/capi"],
    },
    "AuthFailure.SignatureFailure": {
        "hint": "签名验证失败，请检查环境变量 TENCENTCLOUD_SECRET_KEY 是否正确。",
        "actions": ["前往密钥管理确认: https://console.cloud.tencent.com/cam/capi"],
    },
    "FailedOperation.InsufficientBalanceInSmsPackage": {
        "hint": "套餐包余量不足，请购买套餐包后重试。",
        "actions": ["购买套餐包: https://console.cloud.tencent.com/smsv2/package-manage/domestic"],
    },
    "InvalidParameterValue.SdkAppIdNotExist": {
        "hint": "应用 ID (SdkAppId) 不存在，请确认应用 ID 是否正确。",
        "actions": ["前往应用管理确认: https://console.cloud.tencent.com/smsv2/app-manage"],
    },
}


def handle_api_error(e):
    """统一处理 TencentCloudSDKException，提供友好错误提示。"""
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
        TencentCloudSDKException,
    )
    if isinstance(e, TencentCloudSDKException):
        code = e.code if hasattr(e, "code") else "UNKNOWN"
        err = {
            "error": "SMS_API_ERROR",
            "message": str(e),
            "code": code,
        }
        # 增加友好提示
        friendly = FRIENDLY_ERROR_HINTS.get(code)
        if friendly:
            err["hint"] = friendly["hint"]
            err["suggested_actions"] = friendly["actions"]
        print(json.dumps(err, ensure_ascii=False, indent=2))
        sys.exit(1)
    else:
        output_error("UNEXPECTED_ERROR", str(e))


def add_common_args(parser):
    """为 argparse 添加所有脚本共用的参数。"""
    parser.add_argument(
        "--region", default=DEFAULT_REGION,
        help=f"腾讯云地域，默认 {DEFAULT_REGION}",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="预览模式：仅验证参数并输出请求体，不实际调用 API",
    )
    return parser


# ───────────────────────── 按手机号拉取类脚本共用工具 ─────────────────────────
# 适用于 PullSmsSendStatusByPhoneNumber / PullSmsReplyStatusByPhoneNumber 等
# 「时间区间 + 单手机号 + 分页」结构相同的接口。

PULL_BY_PHONE_MAX_LIMIT = 100
PULL_BY_PHONE_DEFAULT_LOOKBACK_SECONDS = 24 * 3600


def parse_datetime_to_ts(value, field):
    """将 'YYYY-MM-DD HH:MM:SS' 转为本地 UNIX 秒，失败则结构化报错退出。"""
    import time
    from datetime import datetime
    try:
        return int(time.mktime(
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S").timetuple()
        ))
    except ValueError:
        output_error(
            "INVALID_PARAMETER",
            f"{field} 格式错误，需为 'YYYY-MM-DD HH:MM:SS'，实际值: {value}",
        )


def resolve_time_range(args, default_lookback_seconds=PULL_BY_PHONE_DEFAULT_LOOKBACK_SECONDS):
    """解析两组互斥时间参数，返回 (begin_ts, end_ts)。

    优先级：--begin-time/--end-time（UNIX 秒）> --begin-datetime/--end-datetime
    （本地时间字符串）> 默认最近 N 秒（默认 24 小时）。
    """
    import time

    has_int = args.begin_time is not None or args.end_time is not None
    has_str = args.begin_datetime is not None or args.end_datetime is not None
    if has_int and has_str:
        output_error(
            "INVALID_PARAMETER",
            "--begin-time/--end-time 与 --begin-datetime/--end-datetime 互斥，只能选择一组",
        )
    if has_int:
        if args.begin_time is None or args.end_time is None:
            output_error(
                "INVALID_PARAMETER",
                "--begin-time 与 --end-time 必须同时提供",
            )
        begin_ts, end_ts = int(args.begin_time), int(args.end_time)
    elif has_str:
        if args.begin_datetime is None or args.end_datetime is None:
            output_error(
                "INVALID_PARAMETER",
                "--begin-datetime 与 --end-datetime 必须同时提供",
            )
        begin_ts = parse_datetime_to_ts(args.begin_datetime, "--begin-datetime")
        end_ts = parse_datetime_to_ts(args.end_datetime, "--end-datetime")
    else:
        now = int(time.time())
        begin_ts, end_ts = now - default_lookback_seconds, now

    if end_ts < begin_ts:
        output_error(
            "INVALID_PARAMETER",
            f"EndTime ({end_ts}) 必须 >= BeginTime ({begin_ts})",
        )
    return begin_ts, end_ts


def validate_phone_number(value):
    """校验 --phone-number 为 E.164 格式。"""
    if not value or not value.startswith("+"):
        output_error(
            "INVALID_PARAMETER",
            f"--phone-number 必须为 E.164 格式（如 +8618501234444），实际值: {value}",
        )


def add_pull_by_phone_args(parser, max_limit=PULL_BY_PHONE_MAX_LIMIT):
    """为「按手机号拉取」类脚本统一添加：手机号 + 互斥时间 + 分页 参数。"""
    parser.add_argument("--sdk-app-id", required=True, help="短信 SdkAppId")
    parser.add_argument(
        "--phone-number", required=True,
        help="E.164 格式手机号，必须以 + 开头（如 +8618501234444）",
    )
    parser.add_argument("--begin-time", type=int, help="起始时间（UNIX 秒）")
    parser.add_argument("--end-time", type=int, help="结束时间（UNIX 秒）")
    parser.add_argument(
        "--begin-datetime",
        help="起始时间（'YYYY-MM-DD HH:MM:SS'，本地时区）",
    )
    parser.add_argument(
        "--end-datetime",
        help="结束时间（'YYYY-MM-DD HH:MM:SS'，本地时区）",
    )
    parser.add_argument(
        "--limit", type=int, default=max_limit,
        help=f"返回数量上限，默认 {max_limit}，最大 {max_limit}",
    )
    parser.add_argument("--offset", type=int, default=0, help="偏移量，默认 0")
    return parser


def build_pull_by_phone_params(args, max_limit=PULL_BY_PHONE_MAX_LIMIT):
    """构造「按手机号拉取」类接口的请求参数 dict。

    会自动校验手机号、解析时间窗、夹取 limit。
    """
    validate_phone_number(args.phone_number)
    begin_ts, end_ts = resolve_time_range(args)
    limit = max(1, min(args.limit, max_limit))
    return {
        "SmsSdkAppId": args.sdk_app_id,
        "PhoneNumber": args.phone_number,
        "BeginTime": begin_ts,
        "EndTime": end_ts,
        "Offset": args.offset,
        "Limit": limit,
    }


def run_pull_by_phone(args, api_name, request_cls, client_method_name):
    """执行「按手机号拉取」类接口的通用主流程。

    Args:
        args: argparse 解析结果（须包含 add_pull_by_phone_args + add_common_args 注入的字段）
        api_name: 用于 dry-run 输出的 API 名（如 "PullSmsSendStatusByPhoneNumber"）
        request_cls: SDK Request 类（如 models.PullSmsSendStatusByPhoneNumberRequest）
        client_method_name: client 上对应方法名（如 "PullSmsSendStatusByPhoneNumber"）
    """
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
        TencentCloudSDKException,
    )

    params = build_pull_by_phone_params(args)
    if args.dry_run:
        output_json({"dry_run": True, "api": api_name, "params": params})
        return

    cred = get_credentials()
    client = build_client(cred, region=args.region)
    try:
        req = request_cls()
        req.from_json_string(json.dumps(params))
        resp = getattr(client, client_method_name)(req)
        output_json(json.loads(resp.to_json_string()))
    except TencentCloudSDKException as e:
        handle_api_error(e)
    except Exception as e:  # pylint: disable=broad-except
        output_error("UNEXPECTED_ERROR", str(e))
