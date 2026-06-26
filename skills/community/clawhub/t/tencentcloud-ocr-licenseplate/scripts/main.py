#!/usr/bin/env python3
"""
腾讯云车牌识别(LicensePlateOCR)调用脚本

支持对中国大陆机动车车牌的自动定位和识别，返回地域编号和车牌号码与车牌颜色信息。
支持多车牌场景识别。
需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image-url <url>
    python main.py --image-base64 <base64_or_filepath>
"""

import argparse
import json
import os
import sys
import base64

# SDK 最大图片限制 (10MB)
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024

# 车牌颜色枚举
VALID_PLATE_COLORS = {"白", "黑", "蓝", "绿", "黄", "黄绿", "临牌", "喷漆", "其它"}

# 错误码含义映射
ERROR_CODE_MAP = {
    "FailedOperation.DownLoadError": "文件下载失败",
    "FailedOperation.ImageDecodeFailed": "图片解码失败",
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
    """格式化响应结果，提取关键信息并结构化输出。"""
    output = {}

    # 首选车牌号码
    if resp_json.get("Number"):
        output["Number"] = resp_json["Number"]

    # 置信度
    if resp_json.get("Confidence") is not None:
        output["Confidence"] = resp_json["Confidence"]

    # 车牌颜色
    if resp_json.get("Color"):
        output["Color"] = resp_json["Color"]

    # 车牌类别
    if resp_json.get("LicensePlateCategory"):
        output["LicensePlateCategory"] = resp_json["LicensePlateCategory"]

    # 像素坐标框
    rect = resp_json.get("Rect")
    if rect:
        output["Rect"] = rect

    # 全部车牌信息（多车牌场景）
    plate_infos = resp_json.get("LicensePlateInfos")
    if plate_infos:
        formatted_plates = []
        for plate in plate_infos:
            plate_info = {
                "Number": plate.get("Number", ""),
                "Confidence": plate.get("Confidence", 0),
                "Color": plate.get("Color", ""),
            }
            if plate.get("Rect"):
                plate_info["Rect"] = plate["Rect"]
            if plate.get("LicensePlateCategory"):
                plate_info["LicensePlateCategory"] = plate["LicensePlateCategory"]
            formatted_plates.append(plate_info)
        output["LicensePlateInfos"] = formatted_plates
        output["PlateCount"] = len(formatted_plates)

    # 请求ID
    if "RequestId" in resp_json:
        output["RequestId"] = resp_json["RequestId"]

    return output


def call_license_plate_ocr(args: argparse.Namespace) -> None:
    """调用腾讯云 LicensePlateOCR 接口。"""
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
    req = models.LicensePlateOCRRequest()

    if args.image_url:
        req.ImageUrl = args.image_url
    elif args.image_base64:
        req.ImageBase64 = load_image_base64(args.image_base64)
    else:
        print("错误: 必须提供 --image-url 或 --image-base64 之一", file=sys.stderr)
        sys.exit(1)

    # 发起请求
    try:
        resp = client.LicensePlateOCR(req)
    except TencentCloudSDKException as e:
        error_desc = ERROR_CODE_MAP.get(e.code, "")
        error_msg = f"API调用失败 [{e.code}]: {e.message}"
        if error_desc:
            error_msg += f" ({error_desc})"
        print(error_msg, file=sys.stderr)
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
        description="腾讯云车牌识别(LicensePlateOCR)调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 通过URL识别车牌
  python main.py --image-url "https://example.com/car.jpg"

  # 通过文件路径(自动Base64编码)识别
  python main.py --image-base64 ./car.jpg

  # 通过Base64文本文件识别
  python main.py --image-base64 ./base64.txt

  # 指定地域
  python main.py --image-url "https://example.com/car.jpg" --region ap-beijing
        """,
    )

    # 图片输入（二选一）
    img_group = parser.add_mutually_exclusive_group(required=True)
    img_group.add_argument(
        "--image-url",
        type=str,
        help="图片URL地址，建议存储于腾讯云COS",
    )
    img_group.add_argument(
        "--image-base64",
        type=str,
        help="图片Base64字符串，或图片/Base64文本文件的路径",
    )

    # 可选参数
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
    call_license_plate_ocr(args)


if __name__ == "__main__":
    main()
