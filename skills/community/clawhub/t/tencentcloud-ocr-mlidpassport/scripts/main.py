#!/usr/bin/env python3
"""
腾讯云护照识别（多国多地区）(MLIDPassportOCR)调用脚本

支持中国大陆地区及中国港澳台地区、其他国家以及地区的护照识别。
识别字段包括护照ID、姓名、出生日期、性别、有效期、发行国、国籍、国家地区代码，
具备护照人像照片的裁剪功能和翻拍、复印件告警功能。
需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image-url <url> [--ret-image] [--region <region>]
    python main.py --image-base64 <base64_or_filepath> [--ret-image] [--region <region>]
"""

import argparse
import json
import os
import sys
import base64

# SDK 最大图片限制 (10MB)
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024

# 告警码含义映射（WarnCardInfos，仅国际站生效）
WARN_CODE_MAP = {
    -9101: "证件边框不完整告警",
    -9102: "证件复印件告警",
    -9103: "证件翻拍告警",
    -9104: "证件PS告警",
    -9107: "证件反光告警",
    -9108: "证件模糊告警",
    -9109: "告警能力未开通",
}

# 错误码中文描述映射
ERROR_CODE_MAP = {
    "FailedOperation.DownLoadError": "文件下载失败",
    "FailedOperation.FieldException": "字段值不符合预期",
    "FailedOperation.ImageDecodeFailed": "图片解码失败",
    "FailedOperation.InconsistencyBetweenMRZAndVRZ": "视读区信息与机读区信息不一致",
    "FailedOperation.NoPassport": "非护照",
    "FailedOperation.OcrFailed": "OCR识别失败",
    "FailedOperation.UnKnowError": "未知错误",
    "FailedOperation.UnOpenError": "服务未开通",
    "FailedOperation.WarningServiceFailed": "通用告警服务异常",
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


def parse_warn_infos(warn_codes: list) -> list:
    """解析告警码列表并附加中文描述。"""
    if not warn_codes:
        return []
    result = []
    for code in warn_codes:
        code_int = int(code) if not isinstance(code, int) else code
        result.append({
            "code": code_int,
            "message": WARN_CODE_MAP.get(code_int, "未知告警"),
        })
    return result


def format_passport_recognize_infos(infos: dict) -> dict:
    """格式化信息区(视读区)证件内容。"""
    if not infos:
        return {}

    fields = [
        ("Type", "证件类型"),
        ("IssuingCountry", "发行国家"),
        ("PassportID", "护照号码"),
        ("Surname", "姓"),
        ("GivenName", "名"),
        ("Name", "姓名"),
        ("Nationality", "国籍"),
        ("DateOfBirth", "出生日期"),
        ("Sex", "性别"),
        ("DateOfIssuance", "发行日期"),
        ("DateOfExpiration", "截止日期"),
        ("Signature", "持证人签名"),
        ("IssuePlace", "签发地点"),
        ("IssuingAuthority", "签发机关"),
    ]

    output = {}
    for key, _label in fields:
        val = infos.get(key)
        if val is not None and val != "":
            output[key] = val

    return output


def format_response(resp_json: dict) -> dict:
    """格式化完整的API响应结果。"""
    output = {}

    # 机读码区(MRZ)解析字段
    mrz_fields = [
        "ID", "Name", "Surname", "GivenName",
        "DateOfBirth", "Sex", "DateOfExpiration",
        "IssuingCountry", "Nationality", "Type",
        "CodeSet", "CodeCrc",
    ]

    for field in mrz_fields:
        val = resp_json.get(field)
        if val is not None and val != "":
            output[field] = val

    # 人像照片（仅在 RetImage=true 且有值时输出）
    image = resp_json.get("Image")
    if image and image != "":
        output["Image"] = image

    # 信息区(视读区)证件内容
    passport_infos = resp_json.get("PassportRecognizeInfos")
    if passport_infos:
        formatted_infos = format_passport_recognize_infos(passport_infos)
        if formatted_infos:
            output["PassportRecognizeInfos"] = formatted_infos

    # 卡证数量（仅曼谷地域返回）
    card_count = resp_json.get("CardCount")
    if card_count is not None:
        output["CardCount"] = card_count

    # 告警信息（WarnCardInfos，仅国际站生效）
    warn_codes = resp_json.get("WarnCardInfos", [])
    if warn_codes:
        output["WarnCardInfos"] = warn_codes
        output["Warnings"] = parse_warn_infos(warn_codes)

    # 请求ID
    if resp_json.get("RequestId"):
        output["RequestId"] = resp_json["RequestId"]

    return output


def call_mlidpassport_ocr(args: argparse.Namespace) -> None:
    """调用腾讯云 MLIDPassportOCR 接口。"""
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
    req = models.MLIDPassportOCRRequest()

    if args.image_url:
        req.ImageUrl = args.image_url
    elif args.image_base64:
        req.ImageBase64 = load_image_base64(args.image_base64)
    else:
        print("错误: 必须提供 --image-url 或 --image-base64 之一", file=sys.stderr)
        sys.exit(1)

    if args.ret_image:
        req.RetImage = True

    # 发起请求
    try:
        resp = client.MLIDPassportOCR(req)
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

    if args.raw:
        print(json.dumps(resp_json, ensure_ascii=False, indent=2))
    else:
        result = format_response(resp_json)
        print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="腾讯云护照识别（多国多地区）(MLIDPassportOCR)调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 通过URL识别护照
  python main.py --image-url "https://example.com/passport.jpg"

  # 通过URL识别护照并返回人像照片
  python main.py --image-url "https://example.com/passport.jpg" --ret-image

  # 通过文件路径(自动Base64编码)识别
  python main.py --image-base64 ./passport.jpg

  # 指定地域（如使用国际站获取告警信息）
  python main.py --image-url "https://example.com/passport.jpg" --region ap-bangkok

  # 输出原始API响应（不格式化）
  python main.py --image-url "https://example.com/passport.jpg" --raw
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
        "--ret-image",
        action="store_true",
        default=False,
        help="是否返回人像照片Base64 (默认不返回)",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="腾讯云地域，默认 ap-guangzhou",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        default=False,
        help="输出原始API响应（不进行格式化处理）",
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
    call_mlidpassport_ocr(args)


if __name__ == "__main__":
    main()
