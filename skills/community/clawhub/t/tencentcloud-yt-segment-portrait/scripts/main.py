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
from tencentcloud.bda.v20200324 import bda_client, models


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
                "step1": "开通人像分割服务: https://console.cloud.tencent.com/bda/segment-portrait-pic",
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


def build_bda_client(cred):
    http_profile = HttpProfile()
    http_profile.endpoint = "bda.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return bda_client.BdaClient(cred, "ap-guangzhou", client_profile)


SUPPORTED_FORMATS = {"wav", "pcm", "ogg-opus", "speex", "silk", "mp3", "m4a", "aac", "amr"}

FORMAT_EXT_MAP = {
    ".wav": "wav",
    ".pcm": "pcm",
    ".ogg": "ogg-opus",
    ".opus": "ogg-opus",
    ".speex": "speex",
    ".silk": "silk",
    ".mp3": "mp3",
    ".m4a": "m4a",
    ".aac": "aac",
    ".amr": "amr",
}


def guess_format(path_or_url):
    """Guess audio format from file extension."""
    lower = path_or_url.lower().split("?")[0]  # strip query params
    for ext, fmt in FORMAT_EXT_MAP.items():
        if lower.endswith(ext):
            return fmt
    return "wav"  # default


def parse_args():
    """Parse command-line arguments and return (input_data)."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Tencent Cloud bda SegmentPortraitPic CLI"
    )
    parser.add_argument("input", nargs="?", help="Picture URL, file path, or base64 string")

    args = parser.parse_args()

    # Determine input data
    input_data = {}

    if args.input:
        value = args.input
        if value.startswith("http://") or value.startswith("https://"):
            input_data = {"picture_url": value}
        elif os.path.isfile(value):
            input_data = {"picture_file": value}
        else:
            # Might be raw base64
            if len(value) > 100 and "/" not in value and "\\" not in value:
                input_data = {"audio_base64": value}
            else:
                print(json.dumps({
                    "error": "INVALID_INPUT",
                    "message": f"Input '{value}' is neither a valid URL nor an existing file path.",
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
    else:
        print(json.dumps({
            "error": "NO_INPUT",
            "message": "No audio input provided. Please supply a URL, file path, or Base64 string.",
            "usage": {
                "url": 'python main.py "https://example.com/audio.wav"',
                "file": "python main.py /path/to/example.png",
                "base64": 'python main.py --base64 "UklGR..."',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return input_data


def call_asr(client, input_data):
    """Call the SegmentPortraitPicRequest API."""
    req = models.SegmentPortraitPicRequest()
    params = {
        "RspImgType": "url"
    }

    if "picture_url" in input_data:
        params["Url"] = input_data["picture_url"]
    elif "picture_base64" in input_data:
        pic_b64 = input_data["picture_base64"]
        params["Image"] = pic_b64
    elif "picture_file" in input_data:
        file_path = input_data["picture_file"]
        with open(file_path, "rb") as f:
            raw_data = f.read()
        pic_b64 = base64.b64encode(raw_data).decode("utf-8")
        params["Image"] = pic_b64
    else:
        raise ValueError("No valid audio input found.")

    req.from_json_string(json.dumps(params))
    resp = client.SegmentPortraitPic(req)
    return json.loads(resp.to_json_string())


def main():
    input_data = parse_args()
    cred = get_credentials()
    client = build_bda_client(cred)

    try:
        response = call_asr(client, input_data)

        result = {}

        result["ResultMaskUrl"] = response.get("ResultMaskUrl")
        result["ResultImageUrl"] = response.get("ResultImageUrl")

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except TencentCloudSDKException as err:
        error_result = {
            "error": "ASR_API_ERROR",
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
