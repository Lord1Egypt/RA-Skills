#!/usr/bin/env python3
"""
腾讯云通用票据识别高级版(VatInvoiceOCR)调用脚本

支持增值税专用发票、增值税普通发票、增值税电子专票、增值税电子普票、
电子发票（普通发票）、电子发票（增值税专用发票）全字段的内容检测和识别。
需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image-url <url> [--is-pdf] [--pdf-page-number <int>]
    python main.py --image-base64 <base64_or_filepath> [--is-pdf] [--pdf-page-number <int>]
"""

import argparse
import base64
import json
import os
import sys

# SDK 最大图片/PDF限制 (10MB)
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024

# 发票头信息字段分类映射（用于格式化输出）
INVOICE_BASIC_FIELDS = {
    "发票代码", "发票号码", "打印发票代码", "打印发票号码", "开票日期",
    "发票名称", "发票类型", "校验码", "校验码备选", "校验码后六位备选",
    "发票号码备选", "机器编号", "密码区", "联次", "联次名称",
    "成品油标志", "是否代开", "是否收购", "是否有公司印章",
}

BUYER_FIELDS = {
    "购买方名称", "购买方识别号", "购买方地址、电话", "购买方开户行及账号",
}

SELLER_FIELDS = {
    "销售方名称", "销售方识别号", "销售方地址、电话", "销售方开户行及账号",
}

AMOUNT_FIELDS = {
    "合计金额", "合计税额", "价税合计(大写)", "小写金额", "税率", "税额",
    "车船税",
}

PERSON_FIELDS = {
    "开票人", "收款人", "复核",
}

OTHER_FIELDS = {
    "备注", "省", "市", "服务类型", "通行费标志", "发票消费类型",
    "货物或应税劳务、服务名称", "车牌号", "类型", "通行日期起", "通行日期止",
    "规格型号", "单位", "数量", "单价", "金额",
}

# 接口错误码含义映射
ERROR_CODE_MAP = {
    "FailedOperation.DownLoadError": "文件下载失败",
    "FailedOperation.EmptyImageError": "图片内容为空",
    "FailedOperation.ImageBlur": "图片模糊",
    "FailedOperation.ImageDecodeFailed": "图片解码失败",
    "FailedOperation.ImageNoText": "图片中未检测到文本",
    "FailedOperation.ImageSizeTooLarge": "图片尺寸过大，请确保编码后不超过10M，像素介于20-10000px",
    "FailedOperation.OcrFailed": "OCR识别失败",
    "FailedOperation.UnKnowError": "未知错误",
    "FailedOperation.UnOpenError": "服务未开通，请先在腾讯云控制台开通增值税发票识别服务",
    "InvalidParameter.EngineImageDecodeFailed": "引擎图片解码失败",
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
    加载 Base64 图片/PDF 内容。
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
            print(f"错误: 文件大小超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制", file=sys.stderr)
            sys.exit(1)
        encoded = base64.b64encode(raw).decode("utf-8")
        return encoded
    else:
        # 直接作为 Base64 字符串使用
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(f"错误: 图片/PDF大小超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print("错误: 提供的 ImageBase64 不是合法的 Base64 编码，也不是有效的文件路径", file=sys.stderr)
            sys.exit(1)
        return value


def classify_invoice_info(name: str) -> str:
    """根据字段名称判断所属分类。"""
    if name in INVOICE_BASIC_FIELDS:
        return "发票基本信息"
    if name in BUYER_FIELDS:
        return "购买方信息"
    if name in SELLER_FIELDS:
        return "销售方信息"
    if name in AMOUNT_FIELDS:
        return "金额信息"
    if name in PERSON_FIELDS:
        return "人员信息"
    return "其他信息"


def format_invoice_item(item: dict) -> dict:
    """格式化单个明细条目，只保留非空字段。"""
    field_map = [
        ("LineNo", "行号"),
        ("Name", "名称"),
        ("Spec", "规格型号"),
        ("Unit", "单位"),
        ("Quantity", "数量"),
        ("UnitPrice", "单价"),
        ("AmountWithoutTax", "不含税金额"),
        ("TaxRate", "税率"),
        ("TaxAmount", "税额"),
        ("TaxClassifyCode", "税收分类编码"),
        ("VehicleType", "运输工具类型"),
        ("VehicleBrand", "运输工具牌号"),
        ("DeparturePlace", "起始地"),
        ("ArrivalPlace", "到达地"),
        ("TransportItemsName", "运输货物名称"),
        ("ConstructionPlace", "建筑服务发生地"),
        ("ConstructionName", "建筑项目名称"),
    ]
    formatted = {}
    for eng_key, chn_key in field_map:
        val = item.get(eng_key)
        if val is not None and val != "":
            formatted[chn_key] = val
    return formatted


def format_response(resp_json: dict) -> dict:
    """格式化响应结果为结构化的中文输出。"""
    output = {}

    # 解析发票头信息（VatInvoiceInfos）
    vat_infos = resp_json.get("VatInvoiceInfos") or []
    categories = {}
    for info in vat_infos:
        name = info.get("Name", "")
        value = info.get("Value", "")
        if not name:
            continue
        category = classify_invoice_info(name)
        if category not in categories:
            categories[category] = {}
        categories[category][name] = value

    # 按固定顺序输出分类
    category_order = ["发票基本信息", "购买方信息", "销售方信息", "金额信息", "人员信息", "其他信息"]
    for cat in category_order:
        if cat in categories:
            output[cat] = categories[cat]

    # 解析明细条目（Items）
    items = resp_json.get("Items") or []
    if items:
        output["明细条目"] = [format_invoice_item(item) for item in items]

    # PDF页数
    pdf_page_size = resp_json.get("PdfPageSize")
    if pdf_page_size is not None and pdf_page_size > 0:
        if "其他信息" not in output:
            output["其他信息"] = {}
        output["其他信息"]["PDF总页数"] = pdf_page_size

    # 旋转角度
    angle = resp_json.get("Angle")
    if angle is not None:
        if "其他信息" not in output:
            output["其他信息"] = {}
        output["其他信息"]["旋转角度"] = angle

    # RequestId
    output["RequestId"] = resp_json.get("RequestId", "")

    return output


def call_vat_invoice_ocr(args: argparse.Namespace) -> None:
    """调用腾讯云 VatInvoiceOCR 接口。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
        from tencentcloud.ocr.v20181119 import ocr_client, models
    except ImportError:
        print(
            "错误: 缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python",
            file=sys.stderr,
        )
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
    req = models.VatInvoiceOCRRequest()

    if args.image_url:
        req.ImageUrl = args.image_url
    elif args.image_base64:
        req.ImageBase64 = load_image_base64(args.image_base64)
    else:
        print("错误: 必须提供 --image-url 或 --image-base64 之一", file=sys.stderr)
        sys.exit(1)

    if args.is_pdf:
        req.IsPdf = True

    if args.pdf_page_number is not None:
        if args.pdf_page_number < 1:
            print("错误: PdfPageNumber 必须 >= 1", file=sys.stderr)
            sys.exit(1)
        req.PdfPageNumber = args.pdf_page_number

    # 发起请求
    try:
        resp = client.VatInvoiceOCR(req)
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
        # 原始JSON输出模式
        print(json.dumps(resp_json, ensure_ascii=False, indent=2))
    else:
        result = format_response(resp_json)
        print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="腾讯云通用票据识别高级版(VatInvoiceOCR)调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 通过URL识别发票
  python main.py --image-url "https://example.com/invoice.jpg"

  # 通过文件路径(自动Base64编码)识别
  python main.py --image-base64 ./invoice.jpg

  # 识别PDF格式发票
  python main.py --image-base64 ./invoice.pdf --is-pdf

  # 识别PDF发票的指定页码
  python main.py --image-base64 ./invoice.pdf --is-pdf --pdf-page-number 2

  # 输出原始JSON响应
  python main.py --image-url "https://example.com/invoice.jpg" --raw
        """,
    )

    # 图片输入（二选一）
    img_group = parser.add_mutually_exclusive_group(required=True)
    img_group.add_argument(
        "--image-url",
        type=str,
        help="图片/PDF的URL地址",
    )
    img_group.add_argument(
        "--image-base64",
        type=str,
        help="图片/PDF的Base64字符串，或文件路径（自动编码）",
    )

    # 可选参数
    parser.add_argument(
        "--is-pdf",
        action="store_true",
        default=False,
        help="是否开启PDF识别，默认false",
    )
    parser.add_argument(
        "--pdf-page-number",
        type=int,
        default=None,
        help="PDF页码，仅当--is-pdf开启时有效，默认1，必须>=1",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        default=False,
        help="输出原始JSON响应（不做格式化处理）",
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
    call_vat_invoice_ocr(args)


if __name__ == "__main__":
    main()
