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
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.asr.v20190614 import models, asr_client


def get_credentials():
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        missing = []
        if not secret_id:
            missing.append("SecretId")
        if not secret_key:
            missing.append("SecretKey")
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": "Missing Tencent Cloud credentials required for ASR.",
            "missing_credentials": missing,
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    token = os.getenv("TENCENTCLOUD_TOKEN")
    if token:
        return credential.Credential(secret_id, secret_key, token)
    return credential.Credential(secret_id, secret_key)


def build_asr_client(cred):
    http_profile = HttpProfile()
    http_profile.endpoint = "asr.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return asr_client.AsrClient(cred, "", client_profile)


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
    """Parse command-line arguments and return (input_data, engine, voice_format, word_info)."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Tencent Cloud ASR SentenceRecognition CLI"
    )
    parser.add_argument("input", nargs="?", help="Audio URL or file path")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--engine", default="16k_zh", help="Engine type (default: 16k_zh)")
    parser.add_argument(
        "--format", dest="voice_format", default=None,
        help=f"Audio format: {', '.join(sorted(SUPPORTED_FORMATS))} (auto-detected from extension if omitted)",
    )
    parser.add_argument("--word-info", type=int, default=0, choices=[0, 1, 2], help="Word-level timestamps: 0=off, 1=on, 2=with punctuation (default: 0)")

    args = parser.parse_args()

    # Determine input data
    input_data = {}

    if args.stdin:
        raw = sys.stdin.read().strip()
        data = json.loads(raw)
        if "audio_url" in data:
            input_data = {"audio_url": data["audio_url"]}
        elif "audio_file" in data:
            input_data = {"audio_file": data["audio_file"]}
        else:
            print(json.dumps({
                "error": "INVALID_STDIN",
                "message": "stdin JSON must contain one of: audio_url, audio_file",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
    elif args.input:
        value = args.input
        if value.startswith("http://") or value.startswith("https://"):
            input_data = {"audio_url": value}
        elif os.path.isfile(value):
            input_data = {"audio_file": value}
        else:
            print(json.dumps({
                "error": "INVALID_INPUT",
                "message": (
                    f"Input '{value}' is neither a valid URL nor an existing file path. "
                    "Raw Base64 audio input is not supported."
                ),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        print(json.dumps({
            "error": "NO_INPUT",
            "message": "No audio input provided. Please supply a URL or file path.",
            "usage": {
                "url": 'python sentence_recognize.py "https://example.com/audio.wav"',
                "file": "python sentence_recognize.py /path/to/audio.wav",
                "stdin_url": 'echo \'{"audio_url":"https://..."}\' | python sentence_recognize.py --stdin',
                "stdin_file": 'echo \'{"audio_file":"/path/to/audio.wav"}\' | python sentence_recognize.py --stdin',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Determine voice format
    voice_format = args.voice_format
    if not voice_format:
        source = (
            input_data.get("audio_url")
            or input_data.get("audio_file")
            or ""
        )
        voice_format = guess_format(source) if source else "wav"

    if voice_format not in SUPPORTED_FORMATS:
        print(json.dumps({
            "error": "UNSUPPORTED_FORMAT",
            "message": f"Audio format '{voice_format}' is not supported. Supported: {', '.join(sorted(SUPPORTED_FORMATS))}",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return input_data, args.engine, voice_format, args.word_info


def call_asr(client, input_data, engine, voice_format, word_info):
    """Call the SentenceRecognition API."""
    req = models.SentenceRecognitionRequest()
    params = {
        "EngSerViceType": engine,
        "VoiceFormat": voice_format,
        "WordInfo": word_info,
    }

    if "audio_url" in input_data:
        params["SourceType"] = 0
        params["Url"] = input_data["audio_url"]
    elif "audio_file" in input_data:
        file_path = input_data["audio_file"]
        with open(file_path, "rb") as f:
            raw_data = f.read()
        audio_b64 = base64.b64encode(raw_data).decode("utf-8")
        params["SourceType"] = 1
        params["Data"] = audio_b64
        params["DataLen"] = len(raw_data)
    else:
        raise ValueError("No valid audio input found.")

    req.from_json_string(json.dumps(params))
    resp = client.SentenceRecognition(req)
    return json.loads(resp.to_json_string())


def main():
    input_data, engine, voice_format, word_info = parse_args()
    cred = get_credentials()
    client = build_asr_client(cred)

    try:
        response = call_asr(client, input_data, engine, voice_format, word_info)

        result = {
            "result": response.get("Result", ""),
            # SentenceRecognition returns AudioDuration in milliseconds; normalize to seconds
            # so all local ASR scripts expose a consistent audio_duration unit.
            "audio_duration": response.get("AudioDuration", 0) / 1000.0,
        }

        word_list = response.get("WordList")
        if word_list:
            result["word_size"] = response.get("WordSize", len(word_list))
            result["word_list"] = word_list

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
