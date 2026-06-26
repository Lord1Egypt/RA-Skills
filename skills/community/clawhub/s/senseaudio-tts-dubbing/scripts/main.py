#!/usr/bin/env python3
"""
SenseAudio TTS - 统一命令行工具

功能：
    - auth-check    检查 API Key 是否配置正确
    - list-voices   输出内置常用音色
    - synth         非流式文本转语音
    - synth-stream  流式文本转语音（SSE）

环境变量：
    SENSEAUDIO_API_KEY   必填
    SENSEAUDIO_API_BASE  可选，默认 https://api.senseaudio.cn
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


def ensure_python_package(import_name: str, pip_name: Optional[str] = None) -> None:
    pip_name = pip_name or import_name
    try:
        importlib.import_module(import_name)
        return
    except ImportError:
        print(f"缺少 {pip_name}，正在自动安装...", file=sys.stderr)

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pip_name],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"自动安装 {pip_name} 失败，请手动执行: {sys.executable} -m pip install {pip_name}\n"
            f"stderr:\n{result.stderr.strip()}"
        )

    try:
        importlib.import_module(import_name)
    except ImportError as exc:
        raise RuntimeError(f"已安装 {pip_name}，但仍无法导入 {import_name}。") from exc


ensure_python_package("requests")
import requests

DEFAULT_API_BASE = "https://api.senseaudio.cn"
DEFAULT_API_PATH = "/v1/t2a_v2"
DEFAULT_MODEL = "senseaudio-tts-1.5-260319"
DEFAULT_VOICE_ID = "male_0004_a"
DEFAULT_FORMAT = "mp3"
DEFAULT_SAMPLE_RATE = 32000
DEFAULT_BITRATE = 128000
DEFAULT_CHANNEL = 1
DEFAULT_SPEED = 1.0
DEFAULT_VOL = 1.0
DEFAULT_PITCH = 0
MAX_TEXT_LENGTH = 10000
OUTPUT_DIR = Path("./outputs")

BUILTIN_VOICES: List[Dict[str, str]] = [
    {"voice_id": "child_0001_a", "name": "可爱萌娃", "style": "开心"},
    {"voice_id": "child_0001_b", "name": "可爱萌娃", "style": "平稳"},
    {"voice_id": "male_0004_a", "name": "儒雅道长", "style": "平稳"},
    {"voice_id": "male_0018_a", "name": "沙哑青年", "style": "深情"},
    {"voice_id": "male_0027_a", "name": "亢奋主播", "style": "热情介绍"},
    {"voice_id": "male_0023_a", "name": "撒娇青年", "style": "平稳"},
    {"voice_id": "male_0019_a", "name": "孔武青年", "style": "平稳"},
    {"voice_id": "female_0033_a", "name": "嗲嗲台妹", "style": "平稳"},
    {"voice_id": "female_0006_a", "name": "温柔御姐", "style": "深情"},
    {"voice_id": "female_0027_a", "name": "魅力姐姐", "style": "平稳"},
    {"voice_id": "female_0008_c", "name": "气质学姐", "style": "平稳"},
    {"voice_id": "female_0035_a", "name": "知心少女", "style": "内容剖析"},
]


class APIError(Exception):
    pass


@dataclass
class SynthesisResult:
    output_path: Path
    meta_path: Optional[Path]
    response_json: Dict[str, Any]


class SenseAudioClient:
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        self.api_key = (api_key or os.getenv("SENSEAUDIO_API_KEY", "")).strip()
        self.api_base = (api_base or os.getenv("SENSEAUDIO_API_BASE", DEFAULT_API_BASE)).rstrip("/")
        self.api_url = f"{self.api_base}{DEFAULT_API_PATH}"

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    @property
    def headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise APIError(_missing_key_message())
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, payload: Dict[str, Any], stream: bool = False, timeout: int = 120) -> requests.Response:
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                stream=stream,
                timeout=timeout,
            )
        except requests.exceptions.RequestException as exc:
            raise APIError(f"请求 SenseAudio 接口失败: {exc}") from exc

        if response.status_code in (401, 403):
            raise APIError(
                "认证失败：当前 SENSEAUDIO_API_KEY 无效、已过期，或当前账号无权限调用该音色/接口。\n\n"
                + _missing_key_message(show_exports=False)
            )
        if response.status_code == 429:
            raise APIError("请求过于频繁（HTTP 429），请稍后重试。")
        if response.status_code >= 400:
            preview = response.text[:500]
            raise APIError(f"HTTP {response.status_code}: {preview}")
        return response

    def auth_check(self) -> Dict[str, Any]:
        payload = {
            "model": DEFAULT_MODEL,
            "text": "认证检查",
            "stream": False,
            "voice_setting": {"voice_id": DEFAULT_VOICE_ID},
            "audio_setting": {"format": "mp3", "sample_rate": 16000, "channel": 1},
        }
        response = self._post(payload, stream=False, timeout=60)
        data = response.json()
        ensure_success_response(data)
        return data

    def synthesize(
        self,
        *,
        text: str,
        voice_id: str,
        output_format: str,
        sample_rate: int,
        bitrate: int,
        channel: int,
        speed: float,
        vol: float,
        pitch: int,
        output: Optional[str] = None,
        save_meta: bool = False,
    ) -> SynthesisResult:
        validate_text(text)
        validate_params(
            speed=speed,
            vol=vol,
            pitch=pitch,
            output_format=output_format,
            sample_rate=sample_rate,
            bitrate=bitrate,
            channel=channel,
        )

        payload = {
            "model": DEFAULT_MODEL,
            "text": text,
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": vol,
                "pitch": pitch,
            },
            "audio_setting": {
                "format": output_format,
                "sample_rate": sample_rate,
                "bitrate": bitrate,
                "channel": channel,
            },
        }
        response = self._post(payload, stream=False, timeout=180)
        result = response.json()
        ensure_success_response(result)

        audio_hex = ((result.get("data") or {}).get("audio") or "").strip()
        if not audio_hex:
            raise APIError("接口返回成功，但 data.audio 为空，未拿到可写入的音频数据。")
        try:
            audio_bytes = bytes.fromhex(audio_hex)
        except ValueError as exc:
            raise APIError("接口返回的 data.audio 不是合法的 hex 编码，无法解码音频。") from exc

        output_path = prepare_output_path(output, output_format, prefix="tts")
        output_path.write_bytes(audio_bytes)
        meta_path = None
        if save_meta:
            meta_path = save_metadata(output_path, result, text=text, voice_id=voice_id)
        return SynthesisResult(output_path=output_path, meta_path=meta_path, response_json=result)

    def synthesize_stream(
        self,
        *,
        text: str,
        voice_id: str,
        output_format: str,
        sample_rate: int,
        bitrate: int,
        channel: int,
        speed: float,
        vol: float,
        pitch: int,
        output: Optional[str] = None,
        save_meta: bool = False,
    ) -> SynthesisResult:
        validate_text(text)
        validate_params(
            speed=speed,
            vol=vol,
            pitch=pitch,
            output_format=output_format,
            sample_rate=sample_rate,
            bitrate=bitrate,
            channel=channel,
        )

        payload = {
            "model": DEFAULT_MODEL,
            "text": text,
            "stream": True,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": vol,
                "pitch": pitch,
            },
            "audio_setting": {
                "format": output_format,
                "sample_rate": sample_rate,
                "bitrate": bitrate,
                "channel": channel,
            },
        }
        response = self._post(payload, stream=True, timeout=300)

        chunks: List[bytes] = []
        last_obj: Dict[str, Any] = {}
        saw_any = False

        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if not line.startswith("data:"):
                continue
            payload_str = line[5:].strip()
            if payload_str == "[DONE]":
                break
            try:
                obj = json.loads(payload_str)
            except json.JSONDecodeError:
                continue
            last_obj = obj
            data = obj.get("data") or {}
            audio_hex = (data.get("audio") or "").strip()
            if audio_hex:
                saw_any = True
                try:
                    chunks.append(bytes.fromhex(audio_hex))
                except ValueError as exc:
                    raise APIError("流式返回中出现非法 hex 音频块，无法继续解码。") from exc

        if not saw_any:
            if last_obj:
                raise APIError(_format_base_resp_error(last_obj))
            raise APIError("流式请求未收到任何音频数据。")

        audio_bytes = b"".join(chunks)
        output_path = prepare_output_path(output, output_format, prefix="tts_stream")
        output_path.write_bytes(audio_bytes)
        meta_path = None
        if save_meta:
            meta_path = save_metadata(output_path, last_obj, text=text, voice_id=voice_id)
        return SynthesisResult(output_path=output_path, meta_path=meta_path, response_json=last_obj)


def _missing_key_message(show_exports: bool = True) -> str:
    lines = [
        "未检测到 SENSEAUDIO_API_KEY。",
        "",
        "请先完成以下步骤：",
        "1. 登录 SenseAudio 控制台。",
        "2. 进入“接口密钥 / API Key”页面。",
        "3. 点击“新增 API Key”，复制并安全保存该密钥。",
    ]
    if show_exports:
        lines.extend(
            [
                "4. 在终端执行：",
                "",
                '   export SENSEAUDIO_API_KEY="你的API Key"',
                '   export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"',
                "",
                "5. 运行以下命令验证配置：",
                "",
                "   python3 scripts/main.py auth-check",
            ]
        )
    return "\n".join(lines)


def _format_base_resp_error(result: Dict[str, Any]) -> str:
    base_resp = result.get("base_resp") or {}
    status_code = base_resp.get("status_code", "unknown")
    status_msg = base_resp.get("status_msg") or base_resp.get("status_message") or "unknown error"
    return f"SenseAudio 接口返回错误: status_code={status_code}, status_msg={status_msg}"


def validate_text(text: str) -> None:
    if not text or not text.strip():
        raise APIError("text 为空，请提供待合成文本。")
    if len(text) > MAX_TEXT_LENGTH:
        raise APIError(f"文本长度超过 {MAX_TEXT_LENGTH} 字符，请缩短文本或做分段合成。")


def validate_params(*, speed: float, vol: float, pitch: int, output_format: str,
                    sample_rate: int, bitrate: int, channel: int) -> None:
    if not (0.5 <= speed <= 2.0):
        raise APIError("speed 必须位于 [0.5, 2.0]。")
    if not (0 <= vol <= 10):
        raise APIError("vol 必须位于 [0, 10]。")
    if not (-12 <= pitch <= 12):
        raise APIError("pitch 必须位于 [-12, 12]。")
    if output_format not in {"mp3", "wav", "pcm", "flac"}:
        raise APIError("format 仅支持 mp3 / wav / pcm / flac。")
    if sample_rate not in {8000, 16000, 22050, 24000, 32000, 44100}:
        raise APIError("sample_rate 仅支持 8000/16000/22050/24000/32000/44100。")
    if bitrate not in {32000, 64000, 128000, 256000}:
        raise APIError("bitrate 仅支持 32000/64000/128000/256000。")
    if channel not in {1, 2}:
        raise APIError("channel 仅支持 1 或 2。")


def ensure_success_response(result: Dict[str, Any]) -> None:
    base_resp = result.get("base_resp") or {}
    status_code = base_resp.get("status_code")
    if status_code not in (0, None):
        raise APIError(_format_base_resp_error(result))


def prepare_output_path(output: Optional[str], ext: str, prefix: str) -> Path:
    if output:
        output_path = Path(output).expanduser()
        if output_path.suffix.lower() != f".{ext}":
            output_path = output_path.with_suffix(f".{ext}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUTPUT_DIR / f"{prefix}_{timestamp}.{ext}"


def save_metadata(output_path: Path, result: Dict[str, Any], *, text: str, voice_id: str) -> Path:
    meta = {
        "output_file": str(output_path),
        "voice_id": voice_id,
        "text_length": len(text),
        "response": result,
    }
    meta_path = output_path.with_suffix(output_path.suffix + ".json")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta_path


def print_result(result: SynthesisResult) -> None:
    print(f"✅ 音频已生成: {result.output_path}")
    if result.meta_path:
        print(f"📝 元信息已保存: {result.meta_path}")


def cmd_auth_check(_: argparse.Namespace) -> None:
    client = SenseAudioClient()
    if not client.configured:
        print(_missing_key_message())
        sys.exit(1)
    result = client.auth_check()
    print("✅ API Key 配置有效。")
    print(json.dumps(result.get("base_resp", {}), ensure_ascii=False, indent=2))


def cmd_list_voices(_: argparse.Namespace) -> None:
    print(json.dumps(BUILTIN_VOICES, ensure_ascii=False, indent=2))


def build_common_kwargs(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "text": args.text,
        "voice_id": args.voice_id,
        "output_format": args.format,
        "sample_rate": args.sample_rate,
        "bitrate": args.bitrate,
        "channel": args.channel,
        "speed": args.speed,
        "vol": args.vol,
        "pitch": args.pitch,
        "output": args.output,
        "save_meta": args.save_meta,
    }


def cmd_synth(args: argparse.Namespace) -> None:
    client = SenseAudioClient()
    if not client.configured:
        print(_missing_key_message())
        sys.exit(1)
    result = client.synthesize(**build_common_kwargs(args))
    print_result(result)


def cmd_synth_stream(args: argparse.Namespace) -> None:
    client = SenseAudioClient()
    if not client.configured:
        print(_missing_key_message())
        sys.exit(1)
    result = client.synthesize_stream(**build_common_kwargs(args))
    print_result(result)


def add_common_synth_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text", "-t", required=True, help="待合成文本")
    parser.add_argument("--voice-id", default=DEFAULT_VOICE_ID, help=f"音色 ID，默认 {DEFAULT_VOICE_ID}")
    parser.add_argument("--format", default=DEFAULT_FORMAT, choices=["mp3", "wav", "pcm", "flac"], help="输出格式")
    parser.add_argument("--sample-rate", type=int, default=DEFAULT_SAMPLE_RATE, help="采样率")
    parser.add_argument("--bitrate", type=int, default=DEFAULT_BITRATE, help="比特率，仅 mp3 生效")
    parser.add_argument("--channel", type=int, default=DEFAULT_CHANNEL, choices=[1, 2], help="声道数")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED, help="语速 [0.5, 2.0]")
    parser.add_argument("--vol", type=float, default=DEFAULT_VOL, help="音量 [0, 10]")
    parser.add_argument("--pitch", type=int, default=DEFAULT_PITCH, help="音调 [-12, 12]")
    parser.add_argument("--output", "-o", help="输出文件路径；若不指定则默认写入 ./outputs/")
    parser.add_argument("--save-meta", action="store_true", help="额外保存元信息 JSON（默认不保存）")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SenseAudio TTS - 统一命令行工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("auth-check", help="检查 API Key 是否可用")
    subparsers.add_parser("list-voices", help="列出内置常用音色")

    synth_parser = subparsers.add_parser("synth", help="非流式文本转语音")
    add_common_synth_args(synth_parser)

    stream_parser = subparsers.add_parser("synth-stream", help="流式文本转语音")
    add_common_synth_args(stream_parser)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "auth-check":
            cmd_auth_check(args)
        elif args.command == "list-voices":
            cmd_list_voices(args)
        elif args.command == "synth":
            cmd_synth(args)
        elif args.command == "synth-stream":
            cmd_synth_stream(args)
        else:
            parser.print_help()
    except APIError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已取消。", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:
        print(f"未预期错误: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
