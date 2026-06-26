#!/usr/bin/env python3
"""
腾讯云 AI 人脸防护盾 (DetectAIFakeFaces) 调用脚本

基于多模态的 AI 大模型算法，提供对人脸图片、视频的防攻击检测能力，
可针对性有效识别高仿真的 AIGC 换脸、高清翻拍、批量黑产攻击、水印等攻击痕迹。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --face-input ./face.jpg                           # 本地图片(自动识别类型并Base64编码)
    python main.py --face-input ./face_video.mp4                     # 本地视频(自动识别类型并Base64编码)
    python main.py --face-input-type 1 --face-input <base64_string>  # 手动指定类型 + Base64字符串
    python main.py --face-input-type 2 --face-input <base64_string>  # 手动指定类型 + Base64字符串
"""

import argparse
import json
import os
import sys
import base64

# 图片大小限制：建议不超过 3MB，最大不可超过 10MB
MAX_IMAGE_RECOMMENDED_BYTES = 3 * 1024 * 1024
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
# 视频大小限制：建议不超过 8MB，最大不可超过 10MB
MAX_VIDEO_RECOMMENDED_BYTES = 8 * 1024 * 1024
MAX_VIDEO_SIZE_BYTES = 10 * 1024 * 1024

# 支持的图片扩展名（仅支持 jpg、png 格式）
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
# 支持的视频扩展名（仅支持 mp4、avi、flv 格式）
VIDEO_EXTENSIONS = {".mp4", ".avi", ".flv"}

# FaceInputType 合法值及其说明
VALID_FACE_INPUT_TYPES = {
    1: "图片Base64",
    2: "视频Base64",
}

# 风险等级说明
RISK_LEVEL_MAP = {
    "Low": "低风险 - 正常人脸",
    "Mid": "中风险 - 存在一定攻击嫌疑",
    "High": "高风险 - 极有可能为攻击行为",
}


def validate_env() -> tuple:
    """校验并返回腾讯云API密钥。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    return secret_id, secret_key


def infer_face_input_type(filepath: str) -> int:
    """
    根据文件扩展名自动推断 FaceInputType。

    :param filepath: 文件路径
    :return: 1(图片) 或 2(视频)，无法识别时返回 0
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        return 1
    if ext in VIDEO_EXTENSIONS:
        return 2
    return 0


def load_base64_content(
    value: str, max_size: int, recommended_size: int, content_type: str = "图片"
) -> str:
    """
    加载 Base64 内容。
    如果 value 是一个存在的文件路径，则读取文件内容作为 Base64；
    否则直接视为 Base64 字符串。
    使用标准 Base64 编码方式（带=补位），符合 RFC4648 规范。

    :param value: Base64 字符串或文件路径
    :param max_size: 最大允许的原始数据大小（字节）
    :param recommended_size: 建议的原始数据大小上限（字节）
    :param content_type: 内容类型描述（用于错误提示）
    :return: Base64 编码字符串
    """
    if os.path.isfile(value):
        with open(value, "rb") as f:
            raw = f.read()
        # 如果文件内容本身就是 Base64 文本（如 txt 文件），直接使用
        try:
            raw_str = raw.decode("utf-8").strip()
            decoded = base64.b64decode(raw_str, validate=True)
            if len(decoded) > max_size:
                print(
                    f"错误: {content_type} Base64解码后大小({len(decoded) / (1024 * 1024):.1f}MB)超过最大限制({max_size // (1024 * 1024)}MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
            if len(decoded) > recommended_size:
                print(
                    f"警告: {content_type} Base64解码后大小({len(decoded) / (1024 * 1024):.1f}MB)超过建议上限({recommended_size // (1024 * 1024)}MB)，建议压缩后再使用",
                    file=sys.stderr,
                )
            return raw_str
        except SystemExit:
            raise
        except Exception:
            pass
        # 否则将二进制文件编码为 Base64
        if len(raw) > max_size:
            print(
                f"错误: {content_type}文件大小({len(raw) / (1024 * 1024):.1f}MB)超过最大限制({max_size // (1024 * 1024)}MB)",
                file=sys.stderr,
            )
            sys.exit(1)
        if len(raw) > recommended_size:
            print(
                f"警告: {content_type}文件大小({len(raw) / (1024 * 1024):.1f}MB)超过建议上限({recommended_size // (1024 * 1024)}MB)，建议压缩后再使用",
                file=sys.stderr,
            )
        encoded = base64.b64encode(raw).decode("utf-8")
        return encoded
    else:
        # 直接作为 Base64 字符串使用
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) > max_size:
                print(
                    f"错误: {content_type}大小({len(decoded) / (1024 * 1024):.1f}MB)超过最大限制({max_size // (1024 * 1024)}MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
            if len(decoded) > recommended_size:
                print(
                    f"警告: {content_type}大小({len(decoded) / (1024 * 1024):.1f}MB)超过建议上限({recommended_size // (1024 * 1024)}MB)，建议压缩后再使用",
                    file=sys.stderr,
                )
        except SystemExit:
            raise
        except Exception:
            print(
                f"错误: 提供的内容不是合法的 Base64 编码，也不是有效的文件路径",
                file=sys.stderr,
            )
            sys.exit(1)
        return value


def format_response(resp_json: dict) -> dict:
    """格式化响应结果，增加风险等级的中文描述。"""
    output = {}

    # 核心字段
    if "AttackRiskLevel" in resp_json:
        output["AttackRiskLevel"] = resp_json["AttackRiskLevel"]
        output["AttackRiskLevelDesc"] = RISK_LEVEL_MAP.get(
            resp_json["AttackRiskLevel"], "未知风险等级"
        )

    # 攻击风险详情
    if "AttackRiskDetailInfos" in resp_json and resp_json["AttackRiskDetailInfos"]:
        output["AttackRiskDetailInfos"] = resp_json["AttackRiskDetailInfos"]

    # 人脸详情信息
    if "FaceDetailInfos" in resp_json and resp_json["FaceDetailInfos"]:
        output["FaceDetailInfos"] = resp_json["FaceDetailInfos"]

    # RequestId
    if "RequestId" in resp_json:
        output["RequestId"] = resp_json["RequestId"]

    return output


def call_detect_ai_fake_faces(args: argparse.Namespace) -> None:
    """调用腾讯云 DetectAIFakeFaces 接口。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
            TencentCloudSDKException,
        )
        from tencentcloud.faceid.v20180301 import faceid_client, models
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
    http_profile.endpoint = "faceid.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    region = args.region if args.region else ""
    client = faceid_client.FaceidClient(cred, region, client_profile)

    # 处理 FaceInputType：如果未指定，则根据文件扩展名自动推断
    face_input_type = args.face_input_type
    face_input = args.face_input

    if face_input_type is None:
        # 未指定类型，尝试自动推断
        if os.path.isfile(face_input):
            face_input_type = infer_face_input_type(face_input)
            if face_input_type == 0:
                print(
                    f"错误: 无法根据文件扩展名自动识别类型，请通过 --face-input-type 手动指定。"
                    f"\n支持的图片格式: {', '.join(sorted(IMAGE_EXTENSIONS))}"
                    f"\n支持的视频格式: {', '.join(sorted(VIDEO_EXTENSIONS))}",
                    file=sys.stderr,
                )
                sys.exit(1)
            print(f"自动识别文件类型: {VALID_FACE_INPUT_TYPES[face_input_type]}", file=sys.stderr)
        else:
            print(
                "错误: 未指定 --face-input-type，且输入不是有效的文件路径，无法自动推断类型。"
                "\n请通过 --face-input-type 指定输入类型: 1(图片Base64) / 2(视频Base64)",
                file=sys.stderr,
            )
            sys.exit(1)

    # 校验 FaceInputType
    if face_input_type not in VALID_FACE_INPUT_TYPES:
        print(
            f"错误: FaceInputType 仅支持 {', '.join(f'{k}({v})' for k, v in VALID_FACE_INPUT_TYPES.items())}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 处理 FaceInput：如果是本地文件路径，自动转为 Base64
    if face_input_type == 1:
        face_input = load_base64_content(
            face_input, MAX_IMAGE_SIZE_BYTES, MAX_IMAGE_RECOMMENDED_BYTES, "图片"
        )
    elif face_input_type == 2:
        face_input = load_base64_content(
            face_input, MAX_VIDEO_SIZE_BYTES, MAX_VIDEO_RECOMMENDED_BYTES, "视频"
        )

    # 构建请求
    req = models.DetectAIFakeFacesRequest()
    params = {
        "FaceInput": face_input,
        "FaceInputType": face_input_type,
    }
    req.from_json_string(json.dumps(params))

    # 发起请求
    try:
        resp = client.DetectAIFakeFaces(req)
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
        description="腾讯云 AI 人脸防护盾 (DetectAIFakeFaces) 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 传入本地图片文件(自动识别类型并Base64编码)
  python main.py --face-input ./face.jpg

  # 传入本地视频文件(自动识别类型并Base64编码)
  python main.py --face-input ./face_video.mp4

  # 手动指定类型 + Base64字符串
  python main.py --face-input-type 1 --face-input "<base64_string>"

  # 手动指定类型 + 文件路径
  python main.py --face-input-type 2 --face-input ./face_video.mp4
        """,
    )

    # 必填参数
    parser.add_argument(
        "--face-input",
        type=str,
        required=True,
        help="人脸输入内容: 本地图片/视频文件路径(自动转Base64)或Base64字符串",
    )

    # 可选参数
    parser.add_argument(
        "--face-input-type",
        type=int,
        default=None,
        choices=[1, 2],
        help="输入类型: 1(图片Base64) / 2(视频Base64)。传入本地文件时可省略，自动根据扩展名识别",
    )

    # 可选参数
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="腾讯云地域，默认为空(该接口不需要传递此参数)",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    call_detect_ai_fake_faces(args)


if __name__ == "__main__":
    main()
