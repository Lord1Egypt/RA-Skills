#!/usr/bin/env python3
"""
腾讯云人脸检测 (DetectFace) 调用脚本

检测图片中的人脸位置，可选返回人脸属性信息（性别、年龄、表情等）和质量信息。
基于腾讯云人脸识别（IAI）服务，使用 iai SDK（v20200303）。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python main.py --image ./face.jpg                                         # 本地图片(自动转Base64)
    python main.py --url "https://example.com/face.jpg"                       # 图片URL
    python main.py --image ./face.jpg --need-face-attributes 1                # 开启属性检测
    python main.py --image ./face.jpg --need-quality-detection 1              # 开启质量检测
    python main.py --image ./face.jpg --max-face-num 5                        # 最多检测5张人脸
    python main.py --image "<base64_string>"                                  # 直接传Base64字符串
"""

import argparse
import json
import os
import sys
import base64

# 图片大小限制：Base64 编码后不可超过 5MB
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
MAX_IMAGE_RECOMMENDED_BYTES = 3 * 1024 * 1024

# 支持的图片扩展名
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

# 性别描述
GENDER_DESC = {
    True: "男性",
    False: "女性",
}

# 表情描述
EXPRESSION_DESC = {
    (0, 30): "严肃",
    (30, 70): "微笑",
    (70, 101): "大笑",
}


def validate_env() -> tuple:
    """校验并返回腾讯云API密钥。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    return secret_id, secret_key


def load_base64_image(value: str) -> str:
    """
    加载图片 Base64 内容。
    如果 value 是存在的文件路径，则读取文件并编码为 Base64；
    否则直接视为 Base64 字符串。
    使用标准 Base64 编码方式（带=补位），符合 RFC4648 规范。

    :param value: Base64 字符串或本地图片文件路径
    :return: Base64 编码字符串
    """
    if os.path.isfile(value):
        ext = os.path.splitext(value)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            print(
                f"警告: 文件扩展名 '{ext}' 不在支持列表 {sorted(IMAGE_EXTENSIONS)} 中，仍尝试上传",
                file=sys.stderr,
            )
        with open(value, "rb") as f:
            raw = f.read()
        # 检查是否已是 Base64 文本文件
        try:
            raw_str = raw.decode("utf-8").strip()
            decoded = base64.b64decode(raw_str, validate=True)
            _check_image_size(len(decoded))
            return raw_str
        except SystemExit:
            raise
        except Exception:
            pass
        # 将二进制图片编码为 Base64
        _check_image_size(len(raw))
        return base64.b64encode(raw).decode("utf-8")
    else:
        # 直接作为 Base64 字符串使用
        try:
            decoded = base64.b64decode(value, validate=True)
            _check_image_size(len(decoded))
        except SystemExit:
            raise
        except Exception:
            print(
                "错误: 提供的内容不是合法的 Base64 编码，也不是有效的文件路径",
                file=sys.stderr,
            )
            sys.exit(1)
        return value


def _check_image_size(size_bytes: int) -> None:
    """检查图片大小是否超限。"""
    if size_bytes > MAX_IMAGE_SIZE_BYTES:
        print(
            f"错误: 图片大小({size_bytes / (1024 * 1024):.1f}MB)超过最大限制({MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB)",
            file=sys.stderr,
        )
        sys.exit(1)
    if size_bytes > MAX_IMAGE_RECOMMENDED_BYTES:
        print(
            f"警告: 图片大小({size_bytes / (1024 * 1024):.1f}MB)超过建议上限({MAX_IMAGE_RECOMMENDED_BYTES // (1024 * 1024)}MB)，建议压缩后再使用",
            file=sys.stderr,
        )


def get_expression_desc(expression: int) -> str:
    """根据表情分值返回描述。"""
    for (low, high), desc in EXPRESSION_DESC.items():
        if low <= expression < high:
            return desc
    return "未知"


def format_face_attributes(attrs: dict) -> dict:
    """格式化人脸属性，添加中文描述。"""
    if not attrs:
        return attrs
    result = dict(attrs)
    # 性别描述
    if "Gender" in result:
        result["GenderDesc"] = "男性" if result["Gender"] > 50 else "女性"
        result["GenderScore"] = result.pop("Gender")
    # 表情描述
    if "Expression" in result:
        result["ExpressionDesc"] = get_expression_desc(result["Expression"])
    # 眼镜描述
    if "Glass" in result:
        result["GlassDesc"] = "戴眼镜" if result["Glass"] else "无眼镜"
    # 口罩描述
    if "Mask" in result:
        result["MaskDesc"] = "戴口罩" if result["Mask"] == 1 else "无口罩"
    return result


def format_response(resp_json: dict) -> dict:
    """格式化响应结果，增加可读性字段。"""
    output = {}

    # 图片尺寸
    if "ImageWidth" in resp_json:
        output["ImageWidth"] = resp_json["ImageWidth"]
    if "ImageHeight" in resp_json:
        output["ImageHeight"] = resp_json["ImageHeight"]

    # 算法版本
    if "FaceModelVersion" in resp_json:
        output["FaceModelVersion"] = resp_json["FaceModelVersion"]

    # 人脸列表
    face_infos = resp_json.get("FaceInfos") or []
    output["FaceCount"] = len(face_infos)
    output["FaceInfos"] = []

    for face in face_infos:
        face_item = {
            "X": face.get("X"),
            "Y": face.get("Y"),
            "Width": face.get("Width"),
            "Height": face.get("Height"),
        }
        # 属性信息
        attrs = face.get("FaceAttributesInfo")
        if attrs:
            face_item["FaceAttributesInfo"] = format_face_attributes(attrs)
        # 质量信息
        quality = face.get("FaceQualityInfo")
        if quality:
            face_item["FaceQualityInfo"] = quality

        output["FaceInfos"].append(face_item)

    # RequestId
    if "RequestId" in resp_json:
        output["RequestId"] = resp_json["RequestId"]

    return output


def call_detect_face(args: argparse.Namespace) -> None:
    """调用腾讯云 DetectFace 接口。"""
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

    # 校验必须提供 --image 或 --url 之一
    if not args.image and not args.url:
        print("错误: 必须提供 --image（图片文件路径或Base64）或 --url（图片URL）之一", file=sys.stderr)
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
    params = {}

    # 图片输入：URL 优先级高于 Image
    if args.url:
        params["Url"] = args.url
        print(f"使用图片URL: {args.url}", file=sys.stderr)
    else:
        print(f"加载图片: {args.image}", file=sys.stderr)
        params["Image"] = load_base64_image(args.image)
        print("图片Base64编码完成", file=sys.stderr)

    # 可选参数
    if args.max_face_num is not None:
        params["MaxFaceNum"] = args.max_face_num
    if args.min_face_size is not None:
        params["MinFaceSize"] = args.min_face_size
    if args.need_face_attributes is not None:
        params["NeedFaceAttributes"] = args.need_face_attributes
    if args.need_quality_detection is not None:
        params["NeedQualityDetection"] = args.need_quality_detection
    if args.face_model_version is not None:
        params["FaceModelVersion"] = args.face_model_version
    if args.need_rotate_detection is not None:
        params["NeedRotateDetection"] = args.need_rotate_detection

    # 构建请求
    req = models.DetectFaceRequest()
    req.from_json_string(json.dumps(params))

    # 发起请求
    print("正在调用 DetectFace 接口...", file=sys.stderr)
    try:
        resp = client.DetectFace(req)
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
        description="腾讯云人脸检测 (DetectFace) 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 传入本地图片文件（仅检测人脸位置）
  python main.py --image ./face.jpg

  # 传入图片 URL
  python main.py --url "https://example.com/face.jpg"

  # 开启人脸属性检测
  python main.py --image ./face.jpg --need-face-attributes 1

  # 开启质量检测
  python main.py --image ./face.jpg --need-quality-detection 1

  # 全功能检测：属性 + 质量 + 最多5张人脸
  python main.py --image ./face.jpg --need-face-attributes 1 --need-quality-detection 1 --max-face-num 5

  # 传入 Base64 字符串
  python main.py --image "<base64_string>"
        """,
    )

    # 图片输入（二选一）
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--image",
        type=str,
        default=None,
        help="图片输入: 本地图片文件路径(自动转Base64)或Base64字符串。与 --url 二选一，--url 优先级更高",
    )
    input_group.add_argument(
        "--url",
        type=str,
        default=None,
        help="图片的 URL 地址。与 --image 二选一，优先级高于 --image",
    )

    # 可选参数
    parser.add_argument(
        "--max-face-num",
        type=int,
        default=None,
        help="最多检测人脸数，默认 1，最大 120",
    )
    parser.add_argument(
        "--min-face-size",
        type=int,
        default=None,
        choices=[20, 34],
        help="人脸最小尺寸（像素），只支持 34 和 20，默认 34",
    )
    parser.add_argument(
        "--need-face-attributes",
        type=int,
        default=None,
        choices=[0, 1],
        help="是否返回人脸属性：0(不返回)/1(返回)，默认 0",
    )
    parser.add_argument(
        "--need-quality-detection",
        type=int,
        default=None,
        choices=[0, 1],
        help="是否开启质量检测：0(关闭)/1(开启)，默认 0",
    )
    parser.add_argument(
        "--face-model-version",
        type=str,
        default=None,
        choices=["2.0", "3.0"],
        help="算法模型版本：2.0/3.0，默认 3.0",
    )
    parser.add_argument(
        "--need-rotate-detection",
        type=int,
        default=None,
        choices=[0, 1],
        help="是否开启旋转识别：0(关闭)/1(开启)，默认 0",
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
    call_detect_face(args)


if __name__ == "__main__":
    main()
