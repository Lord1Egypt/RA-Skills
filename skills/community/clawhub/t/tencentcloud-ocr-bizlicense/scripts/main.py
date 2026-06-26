#!/usr/bin/env python3
"""
腾讯云营业执照识别(BizLicenseOCR)调用脚本

支持快速精准识别营业执照上的字段，包括统一社会信用代码、公司名称、主体类型、
法定代表人、注册资本、组成形式、成立日期、营业期限和经营范围等字段。
需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image-url <url> [--enable-copy-warn] [--enable-period-complete]
    python main.py --image-base64 <base64_or_filepath> [--enable-business-certificate]
"""

import argparse
import json
import os
import sys
import base64

# SDK 最大图片限制 (7MB)
MAX_IMAGE_SIZE_BYTES = 7 * 1024 * 1024

# 告警码含义映射
WARN_CODE_MAP = {
    -9102: "黑白复印件告警",
    -9104: "翻拍件告警",
}

# 告警消息标识映射
WARN_MSG_MAP = {
    "WARN_COPY_CARD": "黑白复印件告警",
    "WARN_RESHOOT_CARD": "翻拍件告警",
}

# 错误码说明映射
ERROR_CODE_MAP = {
    "FailedOperation.DownLoadError": "文件下载失败",
    "FailedOperation.ImageDecodeFailed": "图片解码失败",
    "FailedOperation.NoBizLicense": "非营业执照",
    "FailedOperation.OcrFailed": "OCR识别失败",
    "FailedOperation.UnKnowError": "未知错误",
    "FailedOperation.UnOpenError": "服务未开通",
    "InvalidParameterValue.InvalidParameterValueLimit": "参数值错误",
    "LimitExceeded.TooLargeFileError": "文件内容太大",
    "ResourceUnavailable.InArrears": "账号已欠费",
    "ResourceUnavailable.ResourcePackageRunOut": "账号资源包耗尽",
    "ResourcesSoldOut.ChargeStatusException": "计费状态异常",
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
        if len(raw) > MAX_IMAGE_SIZE_BYTES:
            print(f"错误: 图片文件大小超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制", file=sys.stderr)
            sys.exit(1)
        encoded = base64.b64encode(raw).decode("utf-8")
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


def format_response(resp_json: dict) -> dict:
    """格式化响应结果，提取关键字段并附加告警信息中文描述。"""
    output = {}

    # 核心业务字段
    core_fields = [
        "RegNum", "Name", "Capital", "Person", "Address", "Business",
        "Type", "Period", "ComposingForm", "SetDate",
    ]
    # 扩展字段
    extra_fields = [
        "IsDuplication", "RegistrationDate", "Angle",
        "NationalEmblem", "QRCode", "Seal",
        "Title", "SerialNumber", "RegistrationAuthority",
        "Electronic", "Important",
    ]

    for field in core_fields + extra_fields:
        if field in resp_json and resp_json[field] is not None:
            output[field] = resp_json[field]

    # 处理告警码
    warn_codes = resp_json.get("RecognizeWarnCode") or []
    warn_msgs = resp_json.get("RecognizeWarnMsg") or []
    if warn_codes:
        warnings = []
        for i, code in enumerate(warn_codes):
            msg_id = warn_msgs[i] if i < len(warn_msgs) else ""
            warnings.append({
                "code": code,
                "message_id": msg_id,
                "description": WARN_CODE_MAP.get(code, WARN_MSG_MAP.get(msg_id, "未知告警")),
            })
        output["Warnings"] = warnings

    # 非营业执照的营业类证件识别结果
    biz_cert = resp_json.get("BusinessCertificate")
    if biz_cert:
        output["BusinessCertificate"] = biz_cert

    # 请求ID
    if "RequestId" in resp_json:
        output["RequestId"] = resp_json["RequestId"]

    return output


def call_biz_license_ocr(args: argparse.Namespace) -> None:
    """调用腾讯云 BizLicenseOCR 接口。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
        from tencentcloud.ocr.v20181119 import ocr_client, models
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
    req = models.BizLicenseOCRRequest()

    if args.image_url:
        req.ImageUrl = args.image_url
    elif args.image_base64:
        req.ImageBase64 = load_image_base64(args.image_base64)
    else:
        print("错误: 必须提供 --image-url 或 --image-base64 之一", file=sys.stderr)
        sys.exit(1)

    if args.enable_copy_warn:
        req.EnableCopyWarn = True

    if args.enable_period_complete is not None:
        req.EnablePeriodComplete = args.enable_period_complete

    if args.enable_business_certificate:
        req.EnableBusinessCertificate = True

    # 发起请求
    try:
        resp = client.BizLicenseOCR(req)
    except TencentCloudSDKException as e:
        error_desc = ERROR_CODE_MAP.get(e.code, "")
        error_hint = f" ({error_desc})" if error_desc else ""
        print(f"API调用失败 [{e.code}]{error_hint}: {e.message}", file=sys.stderr)
        if e.requestId:
            print(f"RequestId: {e.requestId}", file=sys.stderr)
        sys.exit(1)

    # 解析并格式化输出
    resp_json = json.loads(resp.to_json_string())
    result = format_response(resp_json)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="腾讯云营业执照识别(BizLicenseOCR)调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 通过URL识别营业执照
  python main.py --image-url "https://example.com/biz_license.jpg"

  # 通过文件路径(自动Base64编码)识别
  python main.py --image-base64 ./biz_license.jpg

  # 开启复印件/翻拍件告警
  python main.py --image-url "https://example.com/biz_license.jpg" --enable-copy-warn

  # 开启营业类证件识别（含非营业执照证件）
  python main.py --image-url "https://example.com/biz_license.jpg" --enable-business-certificate

  # 关闭有效期自动拼接
  python main.py --image-url "https://example.com/biz_license.jpg" --enable-period-complete false
        """,
    )

    # 图片输入（二选一）
    img_group = parser.add_mutually_exclusive_group(required=True)
    img_group.add_argument(
        "--image-url",
        type=str,
        help="图片URL地址（PNG/JPG/JPEG，不超过7M，下载时间不超过3秒）",
    )
    img_group.add_argument(
        "--image-base64",
        type=str,
        help="图片Base64字符串，或图片/Base64文本文件的路径",
    )

    # 可选参数
    parser.add_argument(
        "--enable-copy-warn",
        action="store_true",
        default=False,
        help="是否返回告警码（复印件/翻拍件告警），默认不开启",
    )
    parser.add_argument(
        "--enable-period-complete",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=None,
        help="是否返回自动拼接的有效期（默认true）",
    )
    parser.add_argument(
        "--enable-business-certificate",
        action="store_true",
        default=False,
        help="是否支持营业类证件识别（包括非营业执照证件），默认不开启",
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
    call_biz_license_ocr(args)


if __name__ == "__main__":
    main()
