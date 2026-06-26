#!/usr/bin/env python3
"""
腾讯云人脸静态活体检测（高精度版）(DetectLiveFaceAccurate) 调用脚本

对用户上传的静态图片进行防翻拍活体检测，判断是否为翻拍图片。
相比普通静态活体检测，高精度版增强了对高清屏幕、裁剪纸片、3D面具等攻击的防御能力。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image ./face.jpg                           # 本地图片文件(自动Base64编码)
    python main.py --url "http://example.com/face.jpg"          # 图片URL
    python main.py --image "<base64_string>"                    # 直接传入Base64字符串
    python main.py --image ./face.jpg --face-model-version 3.0  # 指定算法模型版本
"""

import argparse
import json
import os
import sys
import base64

# 图片大小限制：Base64编码后不可超过5MB
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
# 建议大小
RECOMMENDED_IMAGE_SIZE_BYTES = 3 * 1024 * 1024

# 支持的图片扩展名
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

# 推荐阈值
RECOMMENDED_THRESHOLD = 40

# 可选阈值列表
AVAILABLE_THRESHOLDS = [5, 10, 40, 70, 90]


def validate_env() -> tuple:
    """校验并返回腾讯云API密钥。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    return secret_id, secret_key


def load_base64_content(value: str) -> str:
    """
    加载图片Base64内容。
    如果 value 是一个存在的文件路径，则读取文件内容并转为 Base64；
    否则直接视为 Base64 字符串。
    使用标准 Base64 编码方式（带=补位），符合 RFC4648 规范。

    :param value: Base64 字符串或文件路径
    :return: Base64 编码字符串
    """
    if os.path.isfile(value):
        # 检查文件扩展名
        ext = os.path.splitext(value)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            print(
                f"警告: 文件扩展名 '{ext}' 可能不被支持。"
                f"支持的格式: {', '.join(sorted(IMAGE_EXTENSIONS))}",
                file=sys.stderr,
            )

        with open(value, "rb") as f:
            raw = f.read()

        # 如果文件内容本身就是 Base64 文本（如 txt 文件），直接使用
        try:
            raw_str = raw.decode("utf-8").strip()
            decoded = base64.b64decode(raw_str, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(
                    f"错误: 图片Base64解码后大小({len(decoded) / (1024 * 1024):.1f}MB)超过最大限制(5MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
            if len(decoded) > RECOMMENDED_IMAGE_SIZE_BYTES:
                print(
                    f"警告: 图片Base64解码后大小({len(decoded) / (1024 * 1024):.1f}MB)超过建议上限(3MB)，建议压缩后再使用",
                    file=sys.stderr,
                )
            return raw_str
        except SystemExit:
            raise
        except Exception:
            pass

        # 否则将二进制文件编码为 Base64
        if len(raw) > MAX_IMAGE_SIZE_BYTES:
            print(
                f"错误: 图片文件大小({len(raw) / (1024 * 1024):.1f}MB)超过最大限制(5MB)",
                file=sys.stderr,
            )
            sys.exit(1)
        if len(raw) > RECOMMENDED_IMAGE_SIZE_BYTES:
            print(
                f"警告: 图片文件大小({len(raw) / (1024 * 1024):.1f}MB)超过建议上限(3MB)，建议压缩后再使用",
                file=sys.stderr,
            )
        encoded = base64.b64encode(raw).decode("utf-8")
        print(f"已将本地文件转为Base64编码", file=sys.stderr)
        return encoded
    else:
        # 直接作为 Base64 字符串使用
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(
                    f"错误: 图片大小({len(decoded) / (1024 * 1024):.1f}MB)超过最大限制(5MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
            if len(decoded) > RECOMMENDED_IMAGE_SIZE_BYTES:
                print(
                    f"警告: 图片大小({len(decoded) / (1024 * 1024):.1f}MB)超过建议上限(3MB)，建议压缩后再使用",
                    file=sys.stderr,
                )
        except SystemExit:
            raise
        except Exception:
            print(
                "错误: 提供的内容不是合法的 Base64 编码，也不是有效的文件路径",
                file=sys.stderr,
            )
            sys.exit(1)
        return value


def judge_liveness(score: float, threshold: int = RECOMMENDED_THRESHOLD) -> tuple:
    """
    根据活体分数和阈值判断是否为真实人脸。

    :param score: 活体分数
    :param threshold: 判断阈值，默认推荐阈值40
    :return: (is_live: bool, desc: str)
    """
    is_live = score >= threshold
    if is_live:
        desc = f"活体分数{score:.1f}，高于阈值{threshold}，判断为真实人脸（非翻拍）"
    else:
        desc = f"活体分数{score:.1f}，低于阈值{threshold}，判断为翻拍图片"
    return is_live, desc


def format_response(resp_json: dict, threshold: int = RECOMMENDED_THRESHOLD) -> dict:
    """格式化响应结果，增加活体判断结论。"""
    output = {}

    # 活体分数
    if "Score" in resp_json:
        score = resp_json["Score"]
        output["Score"] = score
        is_live, score_desc = judge_liveness(score, threshold)
        output["ScoreDesc"] = score_desc
        output["IsLive"] = is_live

    # 算法模型版本
    if "FaceModelVersion" in resp_json:
        output["FaceModelVersion"] = resp_json["FaceModelVersion"]

    # RequestId
    if "RequestId" in resp_json:
        output["RequestId"] = resp_json["RequestId"]

    return output


def call_detect_live_face_accurate(args: argparse.Namespace) -> None:
    """调用腾讯云 DetectLiveFaceAccurate 接口。"""
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

    # 校验输入参数
    if not args.image and not args.url:
        print("错误: 必须提供 --image 或 --url 参数之一", file=sys.stderr)
        sys.exit(1)

    secret_id, secret_key = validate_env()

    # 构建客户端
    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "iai.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    region = args.region if args.region else ""
    client = iai_client.IaiClient(cred, region, client_profile)

    # 构建请求参数
    params = {}

    # 处理图片输入（URL优先于Image）
    if args.url:
        params["Url"] = args.url
        print(f"使用图片URL: {args.url}", file=sys.stderr)
    elif args.image:
        image_base64 = load_base64_content(args.image)
        params["Image"] = image_base64

    # 算法模型版本
    if args.face_model_version:
        params["FaceModelVersion"] = args.face_model_version

    # 构建请求
    req = models.DetectLiveFaceAccurateRequest()
    req.from_json_string(json.dumps(params))

    # 发起请求
    try:
        resp = client.DetectLiveFaceAccurate(req)
    except TencentCloudSDKException as e:
        print(f"API调用失败 [{e.code}]: {e.message}", file=sys.stderr)
        if e.requestId:
            print(f"RequestId: {e.requestId}", file=sys.stderr)
        sys.exit(1)

    # 解析并格式化输出
    resp_json = json.loads(resp.to_json_string())
    result = format_response(resp_json, threshold=args.threshold)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="腾讯云人脸静态活体检测（高精度版）(DetectLiveFaceAccurate) 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 传入本地图片文件(自动Base64编码)
  python main.py --image ./face.jpg

  # 传入图片URL
  python main.py --url "http://example.com/face.jpg"

  # 传入Base64字符串
  python main.py --image "<base64_string>"

  # 指定算法模型版本和判断阈值
  python main.py --image ./face.jpg --face-model-version 3.0 --threshold 70
        """,
    )

    # 图片输入（二选一）
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--image",
        type=str,
        help="图片输入: 本地图片文件路径(自动转Base64)或Base64字符串",
    )
    input_group.add_argument(
        "--url",
        type=str,
        help="图片URL地址（与 --image 二选一，若同时提供则URL优先）",
    )

    # 可选参数
    parser.add_argument(
        "--face-model-version",
        type=str,
        default="3.0",
        help="人脸识别算法模型版本，目前支持'3.0'（默认: 3.0）",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=RECOMMENDED_THRESHOLD,
        choices=AVAILABLE_THRESHOLDS,
        help=f"活体判断阈值，可选值: {AVAILABLE_THRESHOLDS}（默认推荐值: {RECOMMENDED_THRESHOLD}）",
    )

    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="腾讯云地域，默认为空",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    call_detect_live_face_accurate(args)


if __name__ == "__main__":
    main()
