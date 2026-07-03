#!/usr/bin/env python3
"""
声音复刻工具
功能：调用自有平台 SkillController 接口创建 voice_id。
voice_id 会写入到 voice_config.json 的 `voice_id` 字段，便于后续使用。
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
from pathlib import Path
from typing import Optional


def log(msg: str, level: str = "INFO"):
    prefix = {"INFO": "\u2139\ufe0f ", "WARN": "\u26a0\ufe0f ", "ERR": "\u274c", "OK": "\u2705"}.get(level, "")
    print(f"{prefix} {msg}")


def build_audio_data_uri(file_path: str) -> str:
    """将本地音频文件转换为 data URI（base64）。"""
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"音频文件不存在: {file_path}")
    if not file_path_obj.is_file():
        raise FileNotFoundError(f"音频文件不存在: {file_path}")

    audio_mime_type = mimetypes.guess_type(file_path_obj.name)[0] or "application/octet-stream"
    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f"data:{audio_mime_type};base64,{base64_str}"
    return data_uri


def load_platform_api_key(config_path: Path) -> str:
    """从 voice_config.json 读取平台 API Key。"""
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("api_key", "").strip()
    return ""


def enroll_voice(audio_url: str, prefix: str, language: str, target_model: str) -> str:
    """
    调用自有平台 SkillController 声音复刻接口。
    接口: POST /api/v1/skill/voice/enroll（platform.delilegal.com）
    返回 voice_id。
    """
    try:
        import httpx
        import certifi
    except ImportError:
        log("httpx 或 certifi 未安装，正在安装...", "WARN")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "httpx", "certifi", "-q"], check=True)
        import httpx
        import certifi

    os.environ["SSL_CERT_FILE"] = certifi.where()

    endpoint = "https://platform.delilegal.com/api/v1/skill/voice/enroll"

    payload = {
        "audioUrl": audio_url,
        "prefix": prefix,
        "language": language,
        "targetModel": target_model,
    }

    config_path = Path(__file__).parent.parent / "voice_config.json"
    api_key = load_platform_api_key(config_path)
    if not api_key:
        api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("未找到平台 API Key，请设置 voice_config.json 中的 api_key 或环境变量 DASHSCOPE_API_KEY")

    # 复用 dashscope_api 的 header 构建（含 skill-id / skill-version / session-id）
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from dashscope_api import _build_platform_headers
        headers = _build_platform_headers(api_key)
    except Exception:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    response = httpx.post(endpoint, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    # 平台统一响应格式: { success, code, msg, body: { ... } }
    if not data.get("success", False):
        raise RuntimeError(f"接口返回失败: {data.get('msg', '未知错误')}")

    body = data.get("body", {})
    voice_id = body.get("voiceId", "")
    if not voice_id:
        raise RuntimeError(f"接口调用成功，但未从响应中解析到 voiceId。响应: {json.dumps(data, ensure_ascii=False)}")

    return voice_id


def main():
    parser = argparse.ArgumentParser(description="声音复刻工具（通过自有平台 SkillController）")
    parser.add_argument("--audio-url", default="", help="公网可访问的音频 URL（建议 OSS）")
    parser.add_argument("--audio-file", default="", help="本地音频文件路径（自动转换为 data URI）")
    parser.add_argument("--prefix", default="myvoice", help="voice 前缀，默认 myvoice")
    parser.add_argument("--language", default="zh", help="语言提示，默认 zh")
    parser.add_argument("--target-model", default="cosyvoice-v3.5-plus", help="目标语音模型")
    args = parser.parse_args()

    if not args.audio_url and not args.audio_file:
        log("请提供 --audio-url 或 --audio-file", "ERR")
        sys.exit(1)

    audio_url = args.audio_url.strip()
    if not audio_url and args.audio_file:
        try:
            log("开始读取本地音频并转换为 data URI")
            audio_url = build_audio_data_uri(args.audio_file)
        except Exception as e:
            log(f"音频转换失败: {e}", "ERR")
            sys.exit(1)

    try:
        log("开始调用自有平台声音复刻接口...")
        voice_id = enroll_voice(
            audio_url=audio_url,
            prefix=args.prefix,
            language=args.language,
            target_model=args.target_model,
        )
        log(f"成功创建 voice_id: {voice_id}", "OK")
        # 将 voice_id 写入 voice_config.json 的 voice_id 字段，保留其他已有配置
        config_path = Path(__file__).parent.parent / "voice_config.json"
        try:
            cfg = {}
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    try:
                        cfg = json.load(f) or {}
                    except Exception:
                        cfg = {}
            cfg["voice_id"] = voice_id
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
            log(f"已将 voice_id 写入配置文件: {config_path}", "OK")
        except Exception as e:
            log(f"写入 voice_config.json 失败: {e}", "WARN")
    except Exception as e:
        log(f"复刻失败: {e}", "ERR")
        sys.exit(1)


if __name__ == "__main__":
    main()
