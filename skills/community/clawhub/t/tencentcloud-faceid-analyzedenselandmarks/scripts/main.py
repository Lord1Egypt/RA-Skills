#!/usr/bin/env python3
"""
腾讯云稠密人脸关键点 (AnalyzeDenseLandmarks) 调用脚本

对请求图片进行五官定位，计算构成人脸轮廓的关键点，包括眉毛、眼睛、鼻子、
嘴巴、下巴、脸型轮廓、中轴线等。最多返回 5 张人脸的稠密关键点信息。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image ./face.jpg                         # 本地图片（自动转 Base64）
    python main.py --url "https://example.com/face.jpg"      # 图片 URL
    python main.py --image ./face.jpg --mode 1               # 只检测面积最大的人脸
    python main.py --image ./face.jpg --need-rotate-detection 1  # 开启旋转识别
"""

import argparse
import base64
import json
import os
import sys

# 图片大小限制：Base64 编码后不超过 5MB
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024

# 支持的图片扩展名
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


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
    加载图片 Base64 内容。
    如果 value 是存在的文件路径，则读取文件并转为 Base64；
    否则直接视为 Base64 字符串。
    使用标准 Base64 编码方式（带=补位），符合 RFC4648 规范。

    :param value: 本地文件路径或 Base64 字符串
    :return: Base64 编码字符串
    """
    if os.path.isfile(value):
        ext = os.path.splitext(value)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            print(
                f"警告: 文件扩展名 '{ext}' 可能不受支持，支持的格式: {', '.join(sorted(IMAGE_EXTENSIONS))}",
                file=sys.stderr,
            )
        with open(value, "rb") as f:
            raw = f.read()
        # 尝试判断文件内容是否已经是 Base64 文本
        try:
            raw_str = raw.decode("utf-8").strip()
            decoded = base64.b64decode(raw_str, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(
                    f"错误: 图片 Base64 解码后大小 ({len(decoded) / (1024 * 1024):.1f}MB) 超过最大限制 (5MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
            return raw_str
        except SystemExit:
            raise
        except Exception:
            pass
        # 将二进制文件编码为 Base64
        if len(raw) > MAX_IMAGE_SIZE_BYTES:
            print(
                f"错误: 图片文件大小 ({len(raw) / (1024 * 1024):.1f}MB) 超过最大限制 (5MB)",
                file=sys.stderr,
            )
            sys.exit(1)
        encoded = base64.b64encode(raw).decode("utf-8")
        print(f"已加载本地图片: {value} ({len(raw) / 1024:.1f}KB -> Base64 {len(encoded) / 1024:.1f}KB)", file=sys.stderr)
        return encoded
    else:
        # 直接作为 Base64 字符串使用
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(
                    f"错误: 图片大小 ({len(decoded) / (1024 * 1024):.1f}MB) 超过最大限制 (5MB)",
                    file=sys.stderr,
                )
                sys.exit(1)
        except SystemExit:
            raise
        except Exception:
            print(
                "错误: 提供的内容不是合法的 Base64 编码，也不是有效的文件路径",
                file=sys.stderr,
            )
            sys.exit(1)
        return value


def format_point_list(points: list) -> list:
    """将关键点列表格式化为简洁的 [X, Y] 列表。"""
    if not points:
        return []
    return [{"X": p.get("X"), "Y": p.get("Y")} for p in points]


def format_response(resp_json: dict) -> dict:
    """格式化响应结果，整理稠密关键点数据结构。"""
    output = {
        "ImageWidth": resp_json.get("ImageWidth"),
        "ImageHeight": resp_json.get("ImageHeight"),
        "FaceModelVersion": resp_json.get("FaceModelVersion"),
        "RequestId": resp_json.get("RequestId"),
    }

    dense_face_shapes = resp_json.get("DenseFaceShapeSet", [])
    output["FaceCount"] = len(dense_face_shapes)
    output["DenseFaceShapeSet"] = []

    for face in dense_face_shapes:
        face_info = {
            "FaceRect": {
                "X": face.get("X"),
                "Y": face.get("Y"),
                "Width": face.get("Width"),
                "Height": face.get("Height"),
            },
            "LeftEye": format_point_list(face.get("LeftEye", [])),
            "RightEye": format_point_list(face.get("RightEye", [])),
            "LeftEyeBrow": format_point_list(face.get("LeftEyeBrow", [])),
            "RightEyeBrow": format_point_list(face.get("RightEyeBrow", [])),
            "MouthOutside": format_point_list(face.get("MouthOutside", [])),
            "MouthInside": format_point_list(face.get("MouthInside", [])),
            "Nose": format_point_list(face.get("Nose", [])),
            "LeftPupil": format_point_list(face.get("LeftPupil", [])),
            "RightPupil": format_point_list(face.get("RightPupil", [])),
            "CentralAxis": format_point_list(face.get("CentralAxis", [])),
            "Chin": format_point_list(face.get("Chin", [])),
            "LeftEyeBags": format_point_list(face.get("LeftEyeBags", [])),
            "RightEyeBags": format_point_list(face.get("RightEyeBags", [])),
            "Forehead": format_point_list(face.get("Forehead", [])),
        }
        # 统计各部位关键点数量
        face_info["KeypointCounts"] = {
            part: len(face_info[part])
            for part in [
                "LeftEye", "RightEye", "LeftEyeBrow", "RightEyeBrow",
                "MouthOutside", "MouthInside", "Nose",
                "LeftPupil", "RightPupil", "CentralAxis",
                "Chin", "LeftEyeBags", "RightEyeBags", "Forehead",
            ]
        }
        face_info["TotalKeypoints"] = sum(face_info["KeypointCounts"].values())
        output["DenseFaceShapeSet"].append(face_info)

    return output


def call_analyze_dense_landmarks(args: argparse.Namespace) -> None:
    """调用腾讯云 AnalyzeDenseLandmarks 接口。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
        from tencentcloud.iai.v20200303 import iai_client, models
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
    http_profile.endpoint = "iai.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    region = args.region if args.region else "ap-guangzhou"
    client = iai_client.IaiClient(cred, region, client_profile)

    # 构建请求参数
    params = {
        "Mode": args.mode,
        "FaceModelVersion": "3.0",
        "NeedRotateDetection": args.need_rotate_detection,
    }

    # 处理图片输入：URL 优先，其次 Base64
    if args.url:
        params["Url"] = args.url
        print(f"使用图片 URL: {args.url}", file=sys.stderr)
    elif args.image:
        params["Image"] = load_image_base64(args.image)
    else:
        print("错误: 请提供 --image（本地文件或Base64）或 --url（图片URL）", file=sys.stderr)
        sys.exit(1)

    # 构建请求
    req = models.AnalyzeDenseLandmarksRequest()
    req.from_json_string(json.dumps(params))

    # 发起请求
    try:
        resp = client.AnalyzeDenseLandmarks(req)
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
        description="腾讯云稠密人脸关键点 (AnalyzeDenseLandmarks) 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 传入本地图片文件（自动转 Base64）
  python main.py --image ./face.jpg

  # 传入图片 URL
  python main.py --url "https://example.com/face.jpg"

  # 只检测面积最大的人脸
  python main.py --image ./face.jpg --mode 1

  # 开启旋转识别
  python main.py --image ./face.jpg --need-rotate-detection 1
        """,
    )

    # 图片输入（二选一）
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--image",
        type=str,
        help="本地图片文件路径（自动转 Base64）或 Base64 字符串",
    )
    input_group.add_argument(
        "--url",
        type=str,
        help="图片 URL（与 --image 二选一，都提供时优先使用 URL）",
    )

    # 可选参数
    parser.add_argument(
        "--mode",
        type=int,
        default=0,
        choices=[0, 1],
        help="检测模式: 0(检测所有人脸) / 1(仅检测面积最大的人脸)，默认 0",
    )
    parser.add_argument(
        "--need-rotate-detection",
        type=int,
        default=0,
        choices=[0, 1],
        dest="need_rotate_detection",
        help="是否开启图片旋转识别: 0(不开启) / 1(开启)，默认 0",
    )
    parser.add_argument(
        "--region",
        type=str,
        default="ap-guangzhou",
        help="腾讯云地域，默认 ap-guangzhou",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # 校验至少提供了一种输入
    if not args.image and not args.url:
        parser.error("请提供 --image（本地文件或Base64）或 --url（图片URL）中的至少一个")

    call_analyze_dense_landmarks(args)


if __name__ == "__main__":
    main()
