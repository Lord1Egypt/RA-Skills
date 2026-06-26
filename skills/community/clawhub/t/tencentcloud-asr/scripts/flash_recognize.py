# -*- coding: utf-8 -*-
"""
录音文件识别极速版 (Flash ASR)
同步接口，支持 ≤100MB / ≤2h 音频，极速返回结果。
使用 HMAC-SHA1 签名直接调用 asr.cloud.tencent.com。
"""

import base64
import hashlib
import hmac
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request


def ensure_dependencies():
    """Ensure requests is available (for streaming upload)."""
    try:
        import requests  # noqa: F401
    except ImportError:
        print("[INFO] requests not found. Installing...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "requests", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] requests installed successfully.", file=sys.stderr)


ensure_dependencies()

import requests  # noqa: E402


SUPPORTED_FORMATS = {"wav", "pcm", "ogg-opus", "speex", "silk", "mp3", "m4a", "aac", "amr"}

FORMAT_EXT_MAP = {
    ".wav": "wav", ".pcm": "pcm", ".ogg": "ogg-opus", ".opus": "ogg-opus",
    ".speex": "speex", ".silk": "silk", ".mp3": "mp3", ".m4a": "m4a",
    ".aac": "aac", ".amr": "amr",
}


def guess_format(path_or_url):
    lower = path_or_url.lower().split("?")[0]
    for ext, fmt in FORMAT_EXT_MAP.items():
        if lower.endswith(ext):
            return fmt
    return "wav"


def get_credentials():
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")
    appid = os.getenv("TENCENTCLOUD_APPID")

    if not secret_id or not secret_key or not appid:
        missing = []
        if not secret_id:
            missing.append("SecretId")
        if not secret_key:
            missing.append("SecretKey")
        if not appid:
            missing.append("AppId")
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": "Missing Tencent Cloud credentials required for Flash ASR.",
            "missing_credentials": missing,
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    return appid, secret_id, secret_key


def generate_signature(secret_key, appid, secret_id, params):
    """Generate HMAC-SHA1 signature for Flash ASR API."""
    # Sort params by key
    sorted_params = sorted(params.items())
    query_string = urllib.parse.urlencode(sorted_params)
    url = f"asr.cloud.tencent.com/asr/flash/v1/{appid}?{query_string}"
    sign_str = f"POST{url}"
    hmac_hash = hmac.new(
        secret_key.encode("utf-8"),
        sign_str.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    return base64.b64encode(hmac_hash).decode("utf-8")


def download_url(url):
    """Download audio from URL and return bytes."""
    print(f"[INFO] Downloading audio from URL...", file=sys.stderr)
    resp = requests.get(url, timeout=300)
    resp.raise_for_status()
    print(f"[INFO] Downloaded {len(resp.content)} bytes.", file=sys.stderr)
    return resp.content


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Tencent Cloud Flash ASR (录音文件识别极速版)"
    )
    parser.add_argument("input", nargs="?", help="Audio file path or URL")
    parser.add_argument("--engine", default="16k_zh", help="Engine type (default: 16k_zh)")
    parser.add_argument(
        "--format", dest="voice_format", default=None,
        help=f"Audio format (default: auto-detect). Supported: {', '.join(sorted(SUPPORTED_FORMATS))}",
    )
    parser.add_argument("--word-info", type=int, default=0, choices=[0, 1, 2, 3],
                        help="Word-level timestamps: 0=off, 1=on, 2=with punctuation, 3=subtitle mode (default: 0)")
    parser.add_argument("--speaker-diarization", type=int, default=0, choices=[0, 1],
                        help="Speaker diarization: 0=off, 1=on (default: 0)")
    parser.add_argument("--first-channel-only", type=int, default=1, choices=[0, 1],
                        help="Only recognize first channel: 0=all, 1=first only (default: 1)")

    args = parser.parse_args()

    if not args.input:
        print(json.dumps({
            "error": "NO_INPUT",
            "message": "No audio input provided.",
            "usage": {
                "file": 'python3 flash_recognize.py /path/to/audio.wav',
                "url": 'python3 flash_recognize.py "https://example.com/audio.wav"',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Determine format
    voice_format = args.voice_format or guess_format(args.input)
    if voice_format not in SUPPORTED_FORMATS:
        print(json.dumps({
            "error": "UNSUPPORTED_FORMAT",
            "message": f"Format '{voice_format}' not supported. Supported: {', '.join(sorted(SUPPORTED_FORMATS))}",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return args, voice_format


def call_flash_asr(appid, secret_id, secret_key, audio_data, engine, voice_format, word_info, speaker_diarization, first_channel_only):
    """Call Flash ASR API with audio binary data."""
    timestamp = int(time.time())

    params = {
        "engine_type": engine,
        "voice_format": voice_format,
        "timestamp": str(timestamp),
        "secretid": secret_id,
        "word_info": str(word_info),
        "speaker_diarization": str(speaker_diarization),
        "first_channel_only": str(first_channel_only),
        "filter_dirty": "0",
        "filter_modal": "0",
        "filter_punc": "0",
        "convert_num_mode": "1",
    }

    signature = generate_signature(secret_key, appid, secret_id, params)

    sorted_params = sorted(params.items())
    query_string = urllib.parse.urlencode(sorted_params)
    url = f"https://asr.cloud.tencent.com/asr/flash/v1/{appid}?{query_string}"

    headers = {
        "Host": "asr.cloud.tencent.com",
        "Authorization": signature,
        "Content-Type": "application/octet-stream",
        "Content-Length": str(len(audio_data)),
    }

    resp = requests.post(url, data=audio_data, headers=headers, timeout=600)
    resp.raise_for_status()
    return resp.json()


def main():
    args, voice_format = parse_args()
    appid, secret_id, secret_key = get_credentials()

    # Load audio data
    input_value = args.input
    if input_value.startswith("http://") or input_value.startswith("https://"):
        audio_data = download_url(input_value)
    elif os.path.isfile(input_value):
        with open(input_value, "rb") as f:
            audio_data = f.read()
    else:
        print(json.dumps({
            "error": "INVALID_INPUT",
            "message": f"Input '{input_value}' is neither a valid URL nor an existing file.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Check size limit (100MB)
    if len(audio_data) > 100 * 1024 * 1024:
        print(json.dumps({
            "error": "FILE_TOO_LARGE",
            "message": (
                f"Audio file is {len(audio_data)} bytes, exceeds the 100MB Flash ASR limit. "
                "Normalize and split the file, then recognize each segment with flash_recognize.py. "
                "Use file_recognize.py rec only when async URL mode is explicitly required."
            ),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        response = call_flash_asr(
            appid, secret_id, secret_key, audio_data,
            args.engine, voice_format, args.word_info,
            args.speaker_diarization, args.first_channel_only,
        )

        if response.get("code", -1) != 0:
            print(json.dumps({
                "error": "FLASH_ASR_ERROR",
                "code": response.get("code"),
                "message": response.get("message", "Unknown error"),
                "request_id": response.get("request_id", ""),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        # Build output
        result = {
            # Flash ASR returns audio_duration in milliseconds; normalize to seconds
            # so all local ASR scripts expose a consistent audio_duration unit.
            "audio_duration": response.get("audio_duration", 0) / 1000.0,
            "request_id": response.get("request_id", ""),
        }

        flash_result = response.get("flash_result", [])
        if flash_result:
            # Combine all channel texts
            full_text = "\n".join(ch.get("text", "") for ch in flash_result)
            result["result"] = full_text
            result["channels"] = []
            for ch in flash_result:
                channel_info = {
                    "channel_id": ch.get("channel_id", 0),
                    "text": ch.get("text", ""),
                }
                if ch.get("sentence_list"):
                    channel_info["sentence_list"] = ch["sentence_list"]
                result["channels"].append(channel_info)
        else:
            result["result"] = ""

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except requests.exceptions.RequestException as err:
        print(json.dumps({
            "error": "NETWORK_ERROR",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as err:
        print(json.dumps({
            "error": "UNEXPECTED_ERROR",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
