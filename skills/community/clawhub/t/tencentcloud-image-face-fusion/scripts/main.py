# -*- coding: utf-8 -*-

import base64
import json
import os
import subprocess
import sys


def ensure_dependencies():
    try:
        import tencentcloud  # noqa: F401
    except ImportError:
        print("[INFO] tencentcloud-sdk-python not found. Installing...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "tencentcloud-sdk-python", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] tencentcloud-sdk-python installed successfully.", file=sys.stderr)


ensure_dependencies()

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.facefusion.v20220927 import facefusion_client, models


def get_credentials():
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": (
                "Tencent Cloud API credentials not found in environment variables. "
                "Please set TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY."
            ),
            "guide": {
                "step1": "开通人脸融合服务: https://console.cloud.tencent.com/facefusion",
                "step2": "获取 API 密钥: https://console.cloud.tencent.com/cam/capi",
                "step3_linux": 'export TENCENTCLOUD_SECRET_ID="your_id" && export TENCENTCLOUD_SECRET_KEY="your_key"',
                "step3_windows": '$env:TENCENTCLOUD_SECRET_ID="your_id"; $env:TENCENTCLOUD_SECRET_KEY="your_key"',
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    token = os.getenv("TENCENTCLOUD_TOKEN")
    if token:
        return credential.Credential(secret_id, secret_key, token)
    return credential.Credential(secret_id, secret_key)


def build_facefusion_client(cred):
    http_profile = HttpProfile()
    http_profile.endpoint = "facefusion.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return facefusion_client.FacefusionClient(cred, "ap-guangzhou", client_profile)


def resolve_image_input(value):
    """将输入值解析为 URL 或 base64 编码数据。

    返回 dict: {"url": ...} 或 {"base64": ...}
    """
    if value.startswith("http://") or value.startswith("https://"):
        return {"url": value}
    elif os.path.isfile(value):
        with open(value, "rb") as f:
            raw_data = f.read()
        b64 = base64.b64encode(raw_data).decode("utf-8")
        return {"base64": b64}
    else:
        # 尝试作为 base64 字符串
        if len(value) > 100 and "/" not in value and "\\" not in value:
            return {"base64": value}
        else:
            print(json.dumps({
                "error": "INVALID_INPUT",
                "message": f"Input '{value}' is neither a valid URL nor an existing file path.",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)


def parse_args():
    """解析命令行参数。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Tencent Cloud FuseFaceUltra CLI - 图片人脸融合（专业版）"
    )
    parser.add_argument(
        "--model", required=True,
        help="素材模板图片：URL、本地文件路径或 base64 字符串"
    )
    parser.add_argument(
        "--face", required=True,
        help="用户人脸图片：URL、本地文件路径或 base64 字符串"
    )
    parser.add_argument(
        "--swap-model-type", type=int, default=1, choices=[1, 2, 3, 4, 5, 6],
        help="融合模型类型（1-6），默认1。1:泛娱乐；2:影视自然；3:影视高清自然；4:影视高清高相似度；5:影视高清闭眼友好；6:影视高清极高相似度"
    )
    parser.add_argument(
        "--logo-add", type=int, default=1, choices=[0, 1],
        help="是否添加AI合成标识（0:不添加, 1:添加），默认1"
    )

    args = parser.parse_args()
    return args


def call_fuse_face_ultra(client, args):
    """调用 FuseFaceUltra API。"""
    # 解析素材模板图片
    model_input = resolve_image_input(args.model)
    # 解析用户人脸图片
    face_input = resolve_image_input(args.face)

    params = {
        "RspImgType": "url",
        "SwapModelType": args.swap_model_type,
        "LogoAdd": args.logo_add,
    }

    # 设置素材模板图片
    if "url" in model_input:
        params["ModelUrl"] = model_input["url"]
    else:
        params["ModelImage"] = model_input["base64"]

    # 构建 MergeInfos（用户人脸信息）
    merge_info = {}
    if "url" in face_input:
        merge_info["Url"] = face_input["url"]
    else:
        merge_info["Image"] = face_input["base64"]

    params["MergeInfos"] = [merge_info]

    req = models.FuseFaceUltraRequest()
    req.from_json_string(json.dumps(params))
    resp = client.FuseFaceUltra(req)
    return json.loads(resp.to_json_string())


def main():
    args = parse_args()
    cred = get_credentials()
    client = build_facefusion_client(cred)

    try:
        response = call_fuse_face_ultra(client, args)

        result = {}
        result["FusedImage"] = response.get("FusedImage")

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except TencentCloudSDKException as err:
        error_result = {
            "error": "FUSE_FACE_ULTRA_API_ERROR",
            "code": err.code if hasattr(err, "code") else "UNKNOWN",
            "message": str(err),
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)

    except Exception as err:
        error_result = {
            "error": "UNEXPECTED_ERROR",
            "message": str(err),
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
