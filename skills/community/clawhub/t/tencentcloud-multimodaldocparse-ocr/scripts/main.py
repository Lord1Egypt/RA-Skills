#!/usr/bin/env python3
"""
腾讯云多模态解析（文档版）(MultimodalDocParse) 调用脚本

支持对 PDF/Word/PPT/Excel/Markdown/TXT/图片/WPS 等多格式文档进行智能解析，
返回结构化结果包（zip）下载地址，zip 包含 *.md、*.json 和 images 文件夹。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --file-url "https://example.com/doc.pdf"
    python main.py --file-url "https://example.com/report.docx" \
                   --file-type 2 --result-type 9 --enable-sub-img true
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

# 结果包下载链接有效期（分钟）。
# 官方 API 文档标注 30 分钟；实测签名 q-sign-time 跨度为 24 小时。
# 时效由服务端决定，这里按官方口径保守输出，仍建议调用时用 --download 立即落盘。
RESULT_URL_EXPIRY_MINUTES = 30

# API 允许的枚举值
ALLOWED_FILE_TYPES = {0, 1, 2, 3, 4, 5, 6, 7, 8}
ALLOWED_RESULT_TYPES = {1, 2, 3, 9}
ALLOWED_TASK_TYPES = {0, 1, 2, 3, 4}
PAGE_RANGE_PATTERN = re.compile(r"^\d{1,4}-\d{1,4}$")
MAX_PAGE_RANGE_SPAN = 300

# URL 扩展名 -> FileType 映射（API 文档枚举值）
EXTENSION_TO_FILE_TYPE = {
    ".pdf": 1,
    ".doc": 2, ".docx": 2,
    ".ppt": 3, ".pptx": 3,
    ".xls": 4, ".xlsx": 4,
    ".md": 5, ".markdown": 5,
    ".txt": 6,
    ".png": 7, ".jpg": 7, ".jpeg": 7,
    ".bmp": 7, ".gif": 7, ".webp": 7, ".tiff": 7, ".tif": 7,
    ".wps": 8,
}

# 各类型文件大小限制（字节，API 硬性约束）
FILE_SIZE_LIMITS = {
    1: 150 * 1024 * 1024,  # PDF
    2: 150 * 1024 * 1024,  # Word
    3: 150 * 1024 * 1024,  # PPT
    4: 10 * 1024 * 1024,   # Excel
    6: 10 * 1024 * 1024,   # TXT
    7: 70 * 1024 * 1024,   # 图片
}


def validate_env() -> tuple:
    """校验并返回腾讯云API密钥。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print(
            "错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY",
            file=sys.stderr,
        )
        sys.exit(1)
    return secret_id, secret_key


def validate_file_url(url: str) -> str:
    """校验 FileUrl 格式，必须为 http(s) 开头。"""
    if not re.match(r"^https?://", url, re.IGNORECASE):
        print(
            f"错误: --file-url 必须是 http(s) 开头的URL，当前: {url}",
            file=sys.stderr,
        )
        sys.exit(1)
    return url


def infer_file_type(url: str):
    """从 URL 扩展名推断 FileType，失败返回 None。"""
    path = urllib.parse.urlparse(url).path
    _, ext = os.path.splitext(path)
    return EXTENSION_TO_FILE_TYPE.get(ext.lower())


def validate_page_range(page_range: str) -> str:
    """校验页码范围格式。"""
    if not PAGE_RANGE_PATTERN.match(page_range):
        print(
            f"错误: --page-range 格式错误，应为 '开始页-结束页'，例如 1-10，当前: {page_range}",
            file=sys.stderr,
        )
        sys.exit(1)
    start, end = page_range.split("-", 1)
    start_i, end_i = int(start), int(end)
    if start_i < 1 or end_i < start_i:
        print(
            f"错误: --page-range 起始页必须 >= 1，且结束页 >= 起始页，当前: {page_range}",
            file=sys.stderr,
        )
        sys.exit(1)
    if end_i - start_i + 1 > MAX_PAGE_RANGE_SPAN:
        print(
            f"错误: --page-range 单次调用最多支持 {MAX_PAGE_RANGE_SPAN} 页，"
            f"当前跨度 {end_i - start_i + 1} 页",
            file=sys.stderr,
        )
        sys.exit(1)
    return page_range


def download_result_zip(result_url: str, output_dir: str) -> str:
    """下载结果包 ZIP 到本地，返回保存路径。"""
    os.makedirs(output_dir, exist_ok=True)
    parsed = urllib.parse.urlparse(result_url)
    name = os.path.basename(parsed.path) or "multimodal_result.zip"
    if not name.lower().endswith(".zip"):
        name = "multimodal_result.zip"
    target = os.path.join(output_dir, name)
    try:
        with urllib.request.urlopen(result_url, timeout=120) as resp:
            data = resp.read()
        with open(target, "wb") as f:
            f.write(data)
        return target
    except Exception as e:
        print(f"结果包下载失败: {e}", file=sys.stderr)
        sys.exit(1)


def format_response(resp, downloaded_path: str = None) -> dict:
    """格式化 SDK 响应对象，输出最终 JSON。"""
    result = {
        "ResultUrl": resp.ResultUrl or "",
        "RequestId": resp.RequestId or "",
        "ExpiresIn": f"{RESULT_URL_EXPIRY_MINUTES}分钟",
    }
    if downloaded_path:
        result["downloaded_to"] = downloaded_path
    return result


def build_error_hint(code: str, args: argparse.Namespace) -> str:
    """针对特定错误码给出可执行的排查建议（基于线上实测）。"""
    if code == "FailedOperation.EngineRecognizeTimeout":
        lines = [
            "  引擎识别超时。本接口为同步调用，服务端约 30 秒硬超时，",
            "  超时即本次调用作废（仍会计费），且无异步任务可轮询。",
            "  建议按以下顺序收缩：",
            "    1) 关闭子图解析：去掉 --enable-sub-img true（实测这会显著拉长耗时）",
            "    2) 分批解析：用 --page-range 缩小范围，建议每批 <= 10 页",
        ]
        if not args.page_range:
            lines.append(
                "       （当前未指定 --page-range，默认解析整个文档）"
            )
        else:
            lines.append(f"       （当前 --page-range {args.page_range}）")
        lines.extend(
            [
                "    3) 换国内源：将文件放到腾讯云 COS 等国内存储再解析。",
                "       实测境外 URL（如 arxiv）即使本地测速快，服务端下载",
                "       仍可能拖慢整体耗时，触发超时。",
            ]
        )
        return "\n".join(lines)

    if code == "FailedOperation.DownLoadError":
        return "\n".join(
            [
                "  服务端无法下载该文件。请确认：",
                "    1) URL 公网可直连，无需登录/Cookie/Referer；",
                "    2) 服务端下载耗时不超过 3 秒（境外或慢速源易失败）；",
                "    3) URL 中若含中文或特殊字符，需先做 URL 编码。",
            ]
        )

    if code == "FailedOperation.UnOpenError":
        return "  多模态解析服务未开通。请前往腾讯云控制台开通「多模态解析」服务后重试。"

    if code == "LimitExceeded.TooLargeFileError":
        return "\n".join(
            [
                "  文件超出大小限制：PDF/Word/PPT 150MB、图片 70MB、Excel/TXT 10MB。",
                "  建议拆分文档后分批解析。",
            ]
        )

    return ""


def call_multimodal_doc_parse(args: argparse.Namespace) -> None:
    """调用腾讯云 MultimodalDocParse 接口。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
            TencentCloudSDKException,
        )
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.ocr.v20181119 import models, ocr_client
    except ImportError:
        print(
            "错误: 缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python",
            file=sys.stderr,
        )
        sys.exit(1)

    secret_id, secret_key = validate_env()
    file_url = validate_file_url(args.file_url)

    # 校验可选参数
    if args.result_type is not None and args.result_type not in ALLOWED_RESULT_TYPES:
        print(
            f"错误: --result-type 取值必须为 {sorted(ALLOWED_RESULT_TYPES)}",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.task_type is not None and args.task_type not in ALLOWED_TASK_TYPES:
        print(
            f"错误: --task-type 取值必须为 {sorted(ALLOWED_TASK_TYPES)}",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.file_type is not None and args.file_type not in ALLOWED_FILE_TYPES:
        print(
            f"错误: --file-type 取值必须为 {sorted(ALLOWED_FILE_TYPES)}",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.page_range is not None:
        args.page_range = validate_page_range(args.page_range)

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
    req = models.MultimodalDocParseRequest()
    req.FileUrl = file_url

    # FileType：用户显式 > 扩展名推断 > 不传（API 默认 1=PDF，有踩坑风险）
    if args.file_type is not None:
        req.FileType = args.file_type
    else:
        inferred = infer_file_type(file_url)
        if inferred is not None:
            req.FileType = inferred
        else:
            print(
                "警告: 无法从URL扩展名推断 FileType，将不传递该参数。"
                "API 默认 FileType=1 (PDF)，如解析其他类型请显式传入 --file-type。",
                file=sys.stderr,
            )

    if args.result_type is not None:
        req.ResultType = args.result_type

    if args.enable_sub_img is not None:
        req.EnableSubImg = args.enable_sub_img

    if args.page_range is not None:
        req.PageRange = args.page_range

    if args.task_type is not None:
        req.TaskType = args.task_type

    # 发起请求
    try:
        resp = client.MultimodalDocParse(req)
    except TencentCloudSDKException as e:
        print(f"API调用失败 [{e.code}]: {e.message}", file=sys.stderr)
        if e.requestId:
            print(f"RequestId: {e.requestId}", file=sys.stderr)
        hint = build_error_hint(e.code, args)
        if hint:
            print(f"\n排查建议:\n{hint}", file=sys.stderr)
        sys.exit(1)

    # 可选下载结果包
    downloaded_path = None
    if args.download and resp.ResultUrl:
        downloaded_path = download_result_zip(resp.ResultUrl, args.output_dir)

    result = format_response(resp, downloaded_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="腾讯云多模态解析（文档版）MultimodalDocParse 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 1. 解析 PDF 文档（自动从扩展名推断 FileType=1）
  python main.py --file-url "https://example.com/doc.pdf"

  # 2. 解析 Word 文档（按扩展名自动推断 FileType=2）
  python main.py --file-url "https://example.com/report.docx"

  # 3. 显式指定 FileType，规避扩展名推断不到的情况
  python main.py --file-url "https://example.com/contract" --file-type 2

  # 4. 多页 PDF 仅解析第 1-10 页（大文档务必分批，接口约 30 秒硬超时）
  python main.py --file-url "https://example.com/long.pdf" --page-range 1-10

  # 5. 输出 markdown 格式 + 自动下载结果包
  python main.py --file-url "https://example.com/paper.pdf" \\
                 --result-type 2 --download --output-dir ./results

  # 6. 任务类型：图片OCR识别（适用于扫描件）
  python main.py --file-url "https://example.com/scan.png" \\
                 --file-type 7 --task-type 1

  # 7. json+markdown+xml 三合一输出
  python main.py --file-url "https://example.com/full.pdf" --result-type 9
        """,
    )

    # 必填
    parser.add_argument(
        "--file-url",
        type=str,
        required=True,
        help=(
            "待解析文档的 URL 地址，支持 HTTP/HTTPS。"
            "文件下载时间不超过3秒，建议使用腾讯云COS/CDN 提升稳定性。"
        ),
    )

    # 可选参数
    parser.add_argument(
        "--file-type",
        type=int,
        default=None,
        choices=sorted(ALLOWED_FILE_TYPES),
        help=(
            "文件类型（推荐显式传）。0=未知 1=PDF 2=Word 3=PPT 4=Excel "
            "5=Markdown 6=TXT 7=图片 8=WPS；不传时按URL扩展名自动推断，"
            "无法推断则不传该参数（API 默认 1=PDF，有踩坑风险）"
        ),
    )
    parser.add_argument(
        "--result-type",
        type=int,
        default=None,
        choices=sorted(ALLOWED_RESULT_TYPES),
        help=(
            "输出格式（可选）。1=json 2=markdown 3=xml 9=json+markdown+xml（三合一）；"
            "不传则API默认 9"
        ),
    )
    parser.add_argument(
        "--enable-sub-img",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=None,
        help="是否开启子图解析（可选）。true/false，默认 false",
    )
    parser.add_argument(
        "--page-range",
        type=str,
        default=None,
        help=(
            "页码范围（可选），格式 '开始页-结束页'，单次最多 300 页。"
            "例如 1-10；仅对 PDF/Word/PPT 这类多页文档有效"
        ),
    )
    parser.add_argument(
        "--task-type",
        type=int,
        default=None,
        choices=sorted(ALLOWED_TASK_TYPES),
        help=(
            "任务类型（可选）。0=文档解析 1=图片OCR识别 2=切片文字识别 "
            "3=切片表格识别 4=切片代码识别；默认 0"
        ),
    )

    # 下载相关
    parser.add_argument(
        "--download",
        action="store_true",
        help="下载接口返回的 ZIP 结果包到本地（默认不下载；官方标注30分钟有效，实测24小时，建议立即下载）",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./multimodal_results",
        help="结果包下载目录，默认 ./multimodal_results",
    )

    # 通用
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
    call_multimodal_doc_parse(args)


if __name__ == "__main__":
    main()
