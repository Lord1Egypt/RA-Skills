#!/usr/bin/env python3
"""
腾讯云身份证识别(IDCardOCR)调用脚本

支持中国大陆居民二代身份证正反面所有字段的识别。
需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image-url <url> [--card-side FRONT|BACK] [--config <json>]
    python main.py --image-base64 <base64_or_filepath> [--card-side FRONT|BACK] [--config <json>]
"""

import argparse
import base64
import json
import os
import sys

# SDK 最大图片限制 (10MB)
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024

# CardSide 合法值
VALID_CARD_SIDES = {"FRONT", "BACK"}

# CardWarnType 合法值
VALID_CARD_WARN_TYPES = {"Basic", "Advanced"}

# Config 中允许的开关字段
VALID_CONFIG_KEYS = {
    "CropIdCard", "CropPortrait", "CopyWarn", "BorderCheckWarn",
    "ReshootWarn", "DetectPsWarn", "TempIdWarn", "InvalidDateWarn",
    "Quality", "MultiCardDetect", "ReflectWarn",
}

# 告警码含义映射
WARN_CODE_MAP = {
    -9100: "有效日期不合法",
    -9101: "边框不完整",
    -9102: "复印件",
    -9103: "翻拍",
    -9104: "临时身份证",
    -9105: "框内遮挡",
    -9106: "PS痕迹",
    -9107: "反光",
    -9108: "复印件(仅黑白)",
    -9110: "电子身份证",
}


def validate_env() -> tuple:
    """校验并返回腾讯云API密钥。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    return secret_id, secret_key


def load_image_base64(value: str) -> str:
    """
    加载 Base64 图片内容。
    如果 value 是一个存在的文件路径，则读取文件内容作为 Base64；
    否则直接视为 Base64 字符串。
    """
    if os.path.isfile(value):
        with open(value, "rb") as f:
            raw = f.read()
        # 如果文件内容本身就是Base64文本(如txt文件)，直接使用
        try:
            raw_str = raw.decode("utf-8").strip()
            base64.b64decode(raw_str, validate=True)
            return raw_str
        except (UnicodeDecodeError, ValueError):
            pass
        # 否则将二进制文件编码为Base64
        encoded = base64.b64encode(raw).decode("utf-8")
        if len(raw) > MAX_IMAGE_SIZE_BYTES:
            print(f"错误: 图片文件大小超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制", file=sys.stderr)
            sys.exit(1)
        return encoded
    else:
        # 直接作为 Base64 字符串使用
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(f"错误: 图片大小超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print("错误: 提供的 ImageBase64 不是合法的 Base64 编码，也不是有效的文件路径", file=sys.stderr)
            sys.exit(1)
        return value


def validate_config(config_str: str) -> str:
    """校验 Config JSON 字符串格式和字段合法性。"""
    try:
        config_dict = json.loads(config_str)
    except json.JSONDecodeError as e:
        print(f"错误: Config 不是合法的 JSON 字符串: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(config_dict, dict):
        print("错误: Config 必须是 JSON 对象", file=sys.stderr)
        sys.exit(1)

    invalid_keys = set(config_dict.keys()) - VALID_CONFIG_KEYS
    if invalid_keys:
        print(f"警告: Config 中包含未知字段: {', '.join(sorted(invalid_keys))}", file=sys.stderr)

    for key, val in config_dict.items():
        if key in VALID_CONFIG_KEYS and not isinstance(val, bool):
            print(f"警告: Config 字段 '{key}' 建议使用 bool 类型", file=sys.stderr)

    return config_str


def parse_warn_infos(advanced_info) -> list:
    """
    Parse warning info from AdvancedInfo and attach Chinese descriptions.

    Args:
        advanced_info: AdvancedInfo string from SDK response object.
    """
    if not advanced_info:
        return []
    try:
        info = json.loads(advanced_info) if isinstance(advanced_info, str) else advanced_info
    except (json.JSONDecodeError, TypeError):
        return []

    warn_infos = info.get("WarnInfos", []) if isinstance(info, dict) else []
    result = []
    for code in warn_infos:
        code_int = int(code) if not isinstance(code, int) else code
        result.append({
            "code": code_int,
            "message": WARN_CODE_MAP.get(code_int, "未知告警"),
        })
    return result


def format_response(resp) -> dict:
    """
    Format SDK response object, attach Chinese descriptions for warning codes.

    Args:
        resp: IDCardOCRResponse object from SDK.
    """
    output = {}

    # Front side fields (人像面)
    front_fields = ["Name", "Sex", "Nation", "Birth", "Address", "IdNum"]
    # Back side fields (国徽面)
    back_fields = ["Authority", "ValidDate"]
    # Common fields
    common_fields = ["AdvancedInfo", "RequestId"]

    for field in front_fields + back_fields + common_fields:
        val = getattr(resp, field, None)
        if val:
            output[field] = val

    # Parse warning info
    advanced_info = getattr(resp, "AdvancedInfo", None)
    if advanced_info:
        warnings = parse_warn_infos(advanced_info)
        if warnings:
            output["Warnings"] = warnings

    # Reflect detail info
    reflect_details = getattr(resp, "ReflectDetailInfos", None)
    if reflect_details:
        output["ReflectDetailInfos"] = [
            {"Position": item.Position, "Tag": item.Tag}
            for item in reflect_details
        ] if reflect_details else []

    return output


def call_idcard_ocr(args: argparse.Namespace) -> None:
    """调用腾讯云 IDCardOCR 接口。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
            TencentCloudSDKException,
        )
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.ocr.v20181119 import models, ocr_client
    except ImportError:
        print("错误: 缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python", file=sys.stderr)
        sys.exit(1)

    secret_id, secret_key = validate_env()

    # 构建客户端
    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "ocr.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client_profile.request_client = args.user_agent
    region = args.region if args.region else "ap-guangzhou"
    client = ocr_client.OcrClient(cred, region, client_profile)

    # 构建请求
    req = models.IDCardOCRRequest()

    if args.image_url:
        req.ImageUrl = args.image_url
    elif args.image_base64:
        req.ImageBase64 = load_image_base64(args.image_base64)
    else:
        print("错误: 必须提供 --image-url 或 --image-base64 之一", file=sys.stderr)
        sys.exit(1)

    if args.card_side:
        side = args.card_side.upper()
        if side not in VALID_CARD_SIDES:
            print(f"错误: CardSide 仅支持 {', '.join(sorted(VALID_CARD_SIDES))}", file=sys.stderr)
            sys.exit(1)
        req.CardSide = side

    if args.config:
        req.Config = validate_config(args.config)

    if args.enable_recognition_rectify is not None:
        req.EnableRecognitionRectify = args.enable_recognition_rectify

    if args.enable_reflect_detail is not None:
        req.EnableReflectDetail = args.enable_reflect_detail

    if args.card_warn_type:
        if args.card_warn_type not in VALID_CARD_WARN_TYPES:
            print(f"错误: CardWarnType 仅支持 {', '.join(sorted(VALID_CARD_WARN_TYPES))}", file=sys.stderr)
            sys.exit(1)
        req.CardWarnType = args.card_warn_type

    # Send request (using SDK high-level interface, type-safe with auto-deserialization)
    try:
        resp = client.IDCardOCR(req)
    except TencentCloudSDKException as e:
        print(f"API调用失败 [{e.code}]: {e.message}", file=sys.stderr)
        if e.requestId:
            print(f"RequestId: {e.requestId}", file=sys.stderr)
        sys.exit(1)

    # Format output
    result = format_response(resp)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="腾讯云身份证识别(IDCardOCR)调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础调用(--user-agent 默认为 Skills，可不传)
  python main.py --image-url "https://example.com/idcard.jpg" --card-side FRONT

  # 使用 Base64 文件调用
  python main.py --image-base64 ./idcard.jpg

  # 开启告警检测
  python main.py --image-url "https://example.com/idcard.jpg" \\
    --config '{"CopyWarn":true,"ReshootWarn":true,"DetectPsWarn":true}'

  # 使用进阶PS告警
  python main.py --image-url "https://example.com/idcard.jpg" --card-warn-type Advanced
        """,
    )

    # 图片输入（二选一）
    img_group = parser.add_mutually_exclusive_group(required=True)
    img_group.add_argument(
        "--image-url",
        type=str,
        help="图片URL地址",
    )
    img_group.add_argument(
        "--image-base64",
        type=str,
        help="图片Base64字符串，或图片/Base64文本文件的路径",
    )

    # 可选参数
    parser.add_argument(
        "--card-side",
        type=str,
        choices=["FRONT", "BACK"],
        default=None,
        help="身份证正反面: FRONT(人像面) / BACK(国徽面)，不指定则自动判断",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help='JSON字符串，配置开关，例如: \'{"CropIdCard":true,"CopyWarn":true}\'',
    )
    parser.add_argument(
        "--enable-recognition-rectify",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=None,
        help="是否开启身份证号/出生日期/性别的矫正补齐 (默认true)",
    )
    parser.add_argument(
        "--enable-reflect-detail",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=None,
        help="是否返回反光点覆盖区域详情 (默认false，需配合ReflectWarn)",
    )
    parser.add_argument(
        "--card-warn-type",
        type=str,
        choices=["Basic", "Advanced"],
        default=None,
        help="告警类型: Basic(默认) / Advanced(进阶PS告警)",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="腾讯云地域，默认 ap-guangzhou",
    )
    parser.add_argument(
        "--user-agent",
        type=str,
        default="Skills",
        help="客户端标识，用于统计调用来源，统一固定为 Skills",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    call_idcard_ocr(args)


if __name__ == "__main__":
    main()
