#!/usr/bin/env python3
"""
腾讯云行驶证识别(VehicleLicenseOCR)调用脚本

支持行驶证主页和副页所有字段的自动定位与识别，支持复印件、翻拍告警功能。
需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image-url <url> [--card-side FRONT|BACK|DOUBLE]
    python main.py --image-base64 <base64_or_filepath> [--card-side FRONT|BACK|DOUBLE]
    python main.py --image-url <url> --tractor-card-side FRONT|BACK
"""

import argparse
import json
import os
import sys
import base64

# SDK 最大图片限制 (7MB)
MAX_IMAGE_SIZE_BYTES = 7 * 1024 * 1024

# CardSide 合法值
VALID_CARD_SIDES = {"FRONT", "BACK", "DOUBLE"}

# TractorCardSide 合法值
VALID_TRACTOR_CARD_SIDES = {"FRONT", "BACK"}

# 告警码含义映射
WARN_CODE_MAP = {
    -9102: "复印件告警",
    -9103: "翻拍件告警",
    -9104: "反光告警",
    -9105: "模糊告警",
    -9106: "边框不完整告警",
}

# 告警消息标识映射
WARN_MSG_MAP = {
    -9102: "WARN_DRIVER_LICENSE_COPY_CARD",
    -9103: "WARN_DRIVER_LICENSE_SCREENED_CARD",
    -9104: "WARN_DRIVER_LICENSE_REFLECTION",
    -9105: "WARN_DRIVER_LICENSE_BLUR",
    -9106: "WARN_DRIVER_LICENSE_BORDER_INCOMPLETE",
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


def parse_warn_infos(warn_codes: list, warn_msgs: list) -> list:
    """解析告警码列表并附加中文描述。"""
    if not warn_codes:
        return []
    result = []
    for i, code in enumerate(warn_codes):
        code_int = int(code) if not isinstance(code, int) else code
        msg = warn_msgs[i] if warn_msgs and i < len(warn_msgs) else WARN_MSG_MAP.get(code_int, "")
        result.append({
            "code": code_int,
            "message": WARN_CODE_MAP.get(code_int, "未知告警"),
            "identifier": msg,
        })
    return result


def format_front_info(front_info: dict) -> dict:
    """格式化行驶证主页识别结果。"""
    if not front_info:
        return {}

    fields = [
        ("PlateNo", "号牌号码"),
        ("VehicleType", "车辆类型"),
        ("Owner", "所有人"),
        ("Address", "住址"),
        ("UseCharacter", "使用性质"),
        ("Model", "品牌型号"),
        ("Vin", "车辆识别代号"),
        ("EngineNo", "发动机号码"),
        ("RegisterDate", "注册日期"),
        ("IssueDate", "发证日期"),
        ("Seal", "印章"),
    ]
    # 电子行驶证附加字段
    electronic_fields = [
        ("StateElectronic", "状态(电子行驶证)"),
        ("InspectionValidityTimeElectronic", "检验有效期(电子行驶证)"),
        ("GenerationTimeElectronic", "生成时间(电子行驶证)"),
    ]

    output = {}
    for key, label in fields:
        val = front_info.get(key)
        if val is not None and val != "":
            output[key] = val

    # 仅在电子行驶证时输出附加字段
    for key, label in electronic_fields:
        val = front_info.get(key)
        if val is not None and val != "":
            output[key] = val

    return output


def format_back_info(back_info: dict) -> dict:
    """格式化行驶证副页识别结果。"""
    if not back_info:
        return {}

    fields = [
        ("PlateNo", "号牌号码"),
        ("FileNo", "档案编号"),
        ("AllowNum", "核定人数"),
        ("TotalMass", "总质量"),
        ("CurbWeight", "整备质量"),
        ("LoadQuality", "核定载质量"),
        ("ExternalSize", "外廓尺寸"),
        ("Marks", "备注"),
        ("Record", "检验记录"),
        ("TotalQuasiMass", "准牵引总质量"),
        ("SubPageCode", "副页编码"),
        ("FuelType", "燃料种类"),
    ]
    # 电子行驶证附加字段
    electronic_fields = [
        ("AddressElectronic", "住址(电子行驶证)"),
        ("IssueAuthorityElectronic", "发证机关(电子行驶证)"),
        ("CarBodyColor", "车身颜色(电子行驶证)"),
    ]

    output = {}
    for key, label in fields:
        val = back_info.get(key)
        if val is not None:
            output[key] = val

    for key, label in electronic_fields:
        val = back_info.get(key)
        if val is not None and val != "":
            output[key] = val

    return output


def format_tractor_back_info(tractor_info: dict) -> dict:
    """格式化拖拉机行驶证副页识别结果。"""
    if not tractor_info:
        return {}

    fields = [
        ("PlateNo", "号牌号码"),
        ("AllowNum", "准乘人数"),
        ("CombineHarvesterQuality", "联合收割机质量"),
        ("TractorMinUsageWeight", "拖拉机最小使用质量"),
        ("TractorMaxAllowLoadCapacity", "拖拉机最大允许载质量"),
        ("ExternalSize", "外廓尺寸"),
        ("Record", "检验记录"),
        ("VehicleType", "类型"),
        ("Address", "住址"),
    ]

    output = {}
    for key, label in fields:
        val = tractor_info.get(key)
        if val is not None and val != "":
            output[key] = val

    return output


def format_response(resp_json: dict) -> dict:
    """格式化完整的API响应结果。"""
    output = {}

    # 主页信息
    if resp_json.get("FrontInfo"):
        output["FrontInfo"] = format_front_info(resp_json["FrontInfo"])

    # 副页信息
    if resp_json.get("BackInfo"):
        output["BackInfo"] = format_back_info(resp_json["BackInfo"])

    # 拖拉机行驶证副页信息
    if resp_json.get("TractorBackInfo"):
        output["TractorBackInfo"] = format_tractor_back_info(resp_json["TractorBackInfo"])

    # 行驶证类型
    if resp_json.get("VehicleLicenseType"):
        output["VehicleLicenseType"] = resp_json["VehicleLicenseType"]

    # 告警信息
    warn_codes = resp_json.get("RecognizeWarnCode", [])
    warn_msgs = resp_json.get("RecognizeWarnMsg", [])
    if warn_codes:
        output["RecognizeWarnCode"] = warn_codes
        output["RecognizeWarnMsg"] = warn_msgs
        output["Warnings"] = parse_warn_infos(warn_codes, warn_msgs)

    # 请求ID
    if resp_json.get("RequestId"):
        output["RequestId"] = resp_json["RequestId"]

    return output


def call_vehicle_license_ocr(args: argparse.Namespace) -> None:
    """调用腾讯云 VehicleLicenseOCR 接口。"""
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
    req = models.VehicleLicenseOCRRequest()

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

    if args.tractor_card_side:
        tractor_side = args.tractor_card_side.upper()
        if tractor_side not in VALID_TRACTOR_CARD_SIDES:
            print(f"错误: TractorCardSide 仅支持 {', '.join(sorted(VALID_TRACTOR_CARD_SIDES))}", file=sys.stderr)
            sys.exit(1)
        req.TractorCardSide = tractor_side

    # 发起请求
    try:
        resp = client.VehicleLicenseOCR(req)
    except TencentCloudSDKException as e:
        print(f"API调用失败 [{e.code}]: {e.message}", file=sys.stderr)
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
        description="腾讯云行驶证识别(VehicleLicenseOCR)调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 通过URL识别行驶证主页
  python main.py --image-url "https://example.com/vehicle_license.jpg" --card-side FRONT

  # 通过URL识别行驶证副页
  python main.py --image-url "https://example.com/vehicle_license_back.jpg" --card-side BACK

  # 识别行驶证主副双面
  python main.py --image-url "https://example.com/vehicle_license.jpg" --card-side DOUBLE

  # 通过文件路径(自动Base64编码)识别
  python main.py --image-base64 ./vehicle_license.jpg

  # 识别拖拉机行驶证副页
  python main.py --image-url "https://example.com/tractor.jpg" --tractor-card-side BACK
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
        choices=["FRONT", "BACK", "DOUBLE"],
        default=None,
        help="行驶证正副面: FRONT(主页正面) / BACK(副页正面) / DOUBLE(主副双面)，默认FRONT",
    )
    parser.add_argument(
        "--tractor-card-side",
        type=str,
        choices=["FRONT", "BACK"],
        default=None,
        help="拖拉机行驶证: FRONT(主页正面) / BACK(副页正面)",
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
    call_vehicle_license_ocr(args)


if __name__ == "__main__":
    main()
