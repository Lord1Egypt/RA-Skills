#!/usr/bin/env python3
"""
腾讯云人脸比对 (CompareFace) 调用脚本

对两张图片中的人脸进行相似度比较，返回人脸相似度分数。
基于腾讯云人脸识别（IAI）服务，可用于判断两张人脸是否为同一人。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image-a ./face_a.jpg --image-b ./face_b.jpg
    python main.py --url-a "https://example.com/face_a.jpg" --url-b "https://example.com/face_b.jpg"
    python main.py --image-a ./face_a.jpg --url-b "https://example.com/face_b.jpg"
    python main.py --image-a "<base64_a>" --image-b "<base64_b>" --face-model-version 3.0
"""

import argparse
import json
import os
import sys
import base64

# 图片大小限制：Base64 编码后不可超过 5MB
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
# 建议大小
RECOMMENDED_IMAGE_SIZE_BYTES = 3 * 1024 * 1024

# 支持的图片扩展名
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

# 3.0版本相似度阈值说明
SCORE_DESC_V3 = [
    (60, "高度相似，十万分之一误识率，高度确信为同一人（3.0版本）"),
    (50, "较高相似，万分之一误识率，可认定为同一人（3.0版本）"),
    (40, "疑似相似，千分之一误识率，疑似同一人（3.0版本）"),
    (0,  "相似度较低，可能不是同一人（3.0版本）"),
]

# 2.0版本相似度阈值说明
SCORE_DESC_V2 = [
    (90, "高度相似，十万分之一误识率，高度确信为同一人（2.0版本）"),
    (80, "较高相似，万分之一误识率，可认定为同一人（2.0版本）"),
    (70, "疑似相似，千分之一误识率，疑似同一人（2.0版本）"),
    (0,  "相似度较低，可能不是同一人（2.0版本）"),
]


def validate_env() -> tuple:
    """校验并返回腾讯云API密钥。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    return secret_id, secret_key


def load_image_base64(value: str, label: str = "图片") -> str:
    """
    加载图片 Base64 内容。
    如果 value 是一个存在的文件路径，则读取文件内容并转为 Base64；
    否则直接视为 Base64 字符串。

    :param value: Base64 字符串或本地文件路径
    :param label: 图片标识（用于错误提示）
    :return: Base64 编码字符串
    """
    if os.path.isfile(value):
        ext = os.path.splitext(value)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            print(
                f"错误: {label} 文件格式不支持（{ext}），仅支持 PNG、JPG、JPEG、BMP",
                file=sys.stderr,
            )
            sys.exit(1)

        with open(value, "rb") as f:
            raw = f.read()

        # 检查文件内容是否本身就是 Base64 文本
        try:
            raw_str = raw.decode("utf-8").strip()
            decoded = base64.b64decode(raw_str, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(
                    f"错误: {label} Base64解码后大小({len(decoded) / (1024 * 1024):.1f}MB)超过最大限制(5MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
            if len(decoded) > RECOMMENDED_IMAGE_SIZE_BYTES:
                print(
                    f"警告: {label} Base64解码后大小({len(decoded) / (1024 * 1024):.1f}MB)超过建议上限(3MB)",
                    file=sys.stderr,
                )
            return raw_str
        except SystemExit:
            raise
        except Exception:
            pass

        # 将二进制文件编码为 Base64
        if len(raw) > MAX_IMAGE_SIZE_BYTES:
            print(
                f"错误: {label} 文件大小({len(raw) / (1024 * 1024):.1f}MB)超过最大限制(5MB)",
                file=sys.stderr,
            )
            sys.exit(1)
        if len(raw) > RECOMMENDED_IMAGE_SIZE_BYTES:
            print(
                f"警告: {label} 文件大小({len(raw) / (1024 * 1024):.1f}MB)超过建议上限(3MB)",
                file=sys.stderr,
            )
        return base64.b64encode(raw).decode("utf-8")
    else:
        # 直接作为 Base64 字符串使用，验证合法性
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(
                    f"错误: {label} 大小({len(decoded) / (1024 * 1024):.1f}MB)超过最大限制(5MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
            if len(decoded) > RECOMMENDED_IMAGE_SIZE_BYTES:
                print(
                    f"警告: {label} 大小({len(decoded) / (1024 * 1024):.1f}MB)超过建议上限(3MB)",
                    file=sys.stderr,
                )
        except SystemExit:
            raise
        except Exception:
            print(
                f"错误: {label} 提供的内容不是合法的 Base64 编码，也不是有效的文件路径",
                file=sys.stderr,
            )
            sys.exit(1)
        return value


def get_score_desc(score: float, model_version: str) -> tuple:
    """
    根据相似度分数和模型版本，返回分数描述和是否同一人的判断。

    :param score: 相似度分数
    :param model_version: 算法模型版本
    :return: (描述字符串, 是否同一人)
    """
    thresholds = SCORE_DESC_V3 if model_version == "3.0" else SCORE_DESC_V2
    same_threshold = 50 if model_version == "3.0" else 80

    desc = thresholds[-1][1]
    for threshold, description in thresholds:
        if score >= threshold:
            desc = description
            break

    is_same = score >= same_threshold
    return desc, is_same


def call_compare_face(args: argparse.Namespace) -> None:
    """调用腾讯云 CompareFace 接口。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
            TencentCloudSDKException,
        )
        from tencentcloud.iai.v20200303 import iai_client, models
    except ImportError:
        print(
            "错误: 缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python",
            file=sys.stderr,
        )
        sys.exit(1)

    secret_id, secret_key = validate_env()

    # 校验输入参数：A图片和B图片各需提供至少一种
    if not args.url_a and not args.image_a:
        print("错误: 必须提供 --image-a 或 --url-a 中的至少一个", file=sys.stderr)
        sys.exit(1)
    if not args.url_b and not args.image_b:
        print("错误: 必须提供 --image-b 或 --url-b 中的至少一个", file=sys.stderr)
        sys.exit(1)

    # 构建客户端
    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "iai.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = iai_client.IaiClient(cred, "ap-guangzhou", client_profile)

    # 构建请求参数
    params = {}

    # 处理 A 图片：URL 优先级高于 Base64
    if args.url_a:
        params["UrlA"] = args.url_a
    elif args.image_a:
        params["ImageA"] = load_image_base64(args.image_a, "A图片")

    # 处理 B 图片：URL 优先级高于 Base64
    if args.url_b:
        params["UrlB"] = args.url_b
    elif args.image_b:
        params["ImageB"] = load_image_base64(args.image_b, "B图片")

    # 可选参数
    if args.face_model_version:
        params["FaceModelVersion"] = args.face_model_version
    if args.quality_control is not None:
        params["QualityControl"] = args.quality_control
    if args.need_rotate_detection is not None:
        params["NeedRotateDetection"] = args.need_rotate_detection

    # 构建请求
    req = models.CompareFaceRequest()
    req.from_json_string(json.dumps(params))

    # 发起请求
    try:
        resp = client.CompareFace(req)
    except TencentCloudSDKException as e:
        print(f"API调用失败 [{e.code}]: {e.message}", file=sys.stderr)
        if e.requestId:
            print(f"RequestId: {e.requestId}", file=sys.stderr)
        sys.exit(1)

    # 解析响应
    resp_json = json.loads(resp.to_json_string())

    # 格式化输出
    result = {}
    score = resp_json.get("Score", 0)
    model_ver = resp_json.get("FaceModelVersion", args.face_model_version or "3.0")

    result["Score"] = score
    score_desc, is_same = get_score_desc(score, model_ver)
    result["ScoreDesc"] = score_desc
    result["IsSamePerson"] = is_same
    result["FaceModelVersion"] = model_ver
    result["RequestId"] = resp_json.get("RequestId", "")

    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="腾讯云人脸比对 (CompareFace) 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 传入两张本地图片文件（自动转Base64）
  python main.py --image-a ./face_a.jpg --image-b ./face_b.jpg

  # 传入图片URL
  python main.py --url-a "https://example.com/face_a.jpg" --url-b "https://example.com/face_b.jpg"

  # 混合使用（A用本地文件，B用URL）
  python main.py --image-a ./face_a.jpg --url-b "https://example.com/face_b.jpg"

  # 指定算法版本和质量控制
  python main.py --image-a ./face_a.jpg --image-b ./face_b.jpg --face-model-version 3.0 --quality-control 2

  # 传入Base64字符串
  python main.py --image-a "<base64_string_a>" --image-b "<base64_string_b>"
        """,
    )

    # A 图片参数（二选一）
    group_a = parser.add_argument_group("A图片输入（--image-a 和 --url-a 二选一）")
    group_a.add_argument(
        "--image-a",
        type=str,
        default=None,
        help="A图片: 本地文件路径（自动转Base64）或Base64字符串",
    )
    group_a.add_argument(
        "--url-a",
        type=str,
        default=None,
        help="A图片的URL地址，优先级高于 --image-a",
    )

    # B 图片参数（二选一）
    group_b = parser.add_argument_group("B图片输入（--image-b 和 --url-b 二选一）")
    group_b.add_argument(
        "--image-b",
        type=str,
        default=None,
        help="B图片: 本地文件路径（自动转Base64）或Base64字符串",
    )
    group_b.add_argument(
        "--url-b",
        type=str,
        default=None,
        help="B图片的URL地址，优先级高于 --image-b",
    )

    # 可选参数
    parser.add_argument(
        "--face-model-version",
        type=str,
        default=None,
        choices=["2.0", "3.0"],
        help="算法模型版本: '2.0' 或 '3.0'，默认 '3.0'",
    )
    parser.add_argument(
        "--quality-control",
        type=int,
        default=None,
        choices=[0, 1, 2, 3, 4],
        help="图片质量控制: 0(不控制)/1(低)/2(一般)/3(较高)/4(很高)，默认0",
    )
    parser.add_argument(
        "--need-rotate-detection",
        type=int,
        default=None,
        choices=[0, 1],
        help="是否开启旋转识别: 0(不开启)/1(开启)，默认0",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    call_compare_face(args)


if __name__ == "__main__":
    main()
