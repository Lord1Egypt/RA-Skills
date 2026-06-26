#!/usr/bin/env python3
"""
Telegram 语音消息处理模块（纯处理模式）：
- process_telegram_voice_message: 接收本地音频路径，转写 → 生成回复 → TTS

说明：
- 不再直接访问 Telegram Bot API；下载与发送由 OpenClaw 负责
- 输入可以是 OGG/Opus/WAV/MP3 等，内部会转换为 Vosk 需要的 WAV 进行识别
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import requests

# 导入本项目模块
from config import get_settings
from transcribe_audio import transcribe, TranscriptionError
from reply_with_tts import synthesize_to_feishu_voice, TTSGenerationError
from utils import ensure_file

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE = "https://api.telegram.org"


class TelegramError(Exception):
    pass


def _bot_url(token: str, method: str) -> str:
    return f"{TELEGRAM_API_BASE}/bot{token}/{method}"


def download_telegram_voice(file_id: str, output_dir: Optional[str] = None) -> str:
    """
    已废弃：本项目已改为 OpenClaw Skill，不再直接访问 Telegram Bot API。
    由 OpenClaw 负责下载媒体到本地，并将音频文件路径传入处理函数。
    此函数仅保留以维持向后兼容，始终抛出异常提示调用方改用纯处理接口。
    """
    raise TelegramError("下载逻辑已移除：请让 OpenClaw 下载语音并传入本地文件路径")


def send_telegram_voice(audio_path: str, caption: Optional[str] = None, chat_id: Optional[str] = None) -> dict:
    """
    已废弃：发送逻辑由 OpenClaw 的 `message` 工具负责。
    本模块不再直接调用 Telegram Bot API。请在 OpenClaw 流程中发送语音。
    """
    raise TelegramError("发送逻辑已移除：请使用 OpenClaw 的 message 工具发送语音")


def process_telegram_voice_message(
    audio_path: str,
    reply_template: Optional[str] = None
) -> Tuple[str, str, str]:
    """
    纯处理模式：接收 OpenClaw 已下载的本地音频路径，完成：转写 -> 生成回复 -> TTS。
    返回 (transcript, reply_text, voice_path)。
    """
    audio_path = ensure_file(audio_path)

    # 转写
    try:
        transcript = transcribe(audio_path)
        if not transcript:
            raise TelegramError("转写结果为空")
    except (TranscriptionError, FileNotFoundError) as e:
        raise TelegramError(f"转写失败：{e}") from e

    # 回复文本
    if reply_template is None:
        reply_template = "陛下，您说：{transcript}。我已收到。"
    try:
        reply_text = reply_template.format(transcript=transcript)
    except KeyError as e:
        raise TelegramError(f"回复模板格式错误：缺少占位符 {e}") from e

    # TTS 合成（生成 OGG/Opus）
    try:
        voice_path = synthesize_to_feishu_voice(reply_text)
    except (TTSGenerationError, ValueError) as e:
        raise TelegramError(f"TTS 合成失败：{e}") from e

    return transcript, reply_text, voice_path


def main() -> None:
    import argparse
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    parser = argparse.ArgumentParser(description="处理 Telegram 语音消息闭环")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # 下载子命令
    p_dl = sub.add_parser("download", help="通过 file_id 下载 Telegram 语音到本地")
    p_dl.add_argument("file_id", help="Telegram voice.file_id")
    p_dl.add_argument("--out-dir", default=None, help="输出目录")

    # 发送子命令
    p_send = sub.add_parser("send", help="发送本地 OGG 语音到 Telegram")
    p_send.add_argument("audio_path", help="本地 OGG/Opus 文件路径")
    p_send.add_argument("--caption", default=None, help="文字说明")
    p_send.add_argument("--chat-id", default=None, help="目标 chat_id，默认 TELEGRAM_CHAT_ID")

    # 闭环处理
    p_proc = sub.add_parser("process", help="通过 file_id 完整处理并回传")
    p_proc.add_argument("file_id", help="Telegram voice.file_id")
    p_proc.add_argument("--template", default=None, help="回复模板，默认 '陛下，您说：{transcript}。我已收到。'")
    p_proc.add_argument("--send", action="store_true", help="生成后自动回传语音")

    args = parser.parse_args()

    try:
        if args.cmd == "download":
            out = download_telegram_voice(args.file_id, output_dir=args.out_dir)
            print(out)

        elif args.cmd == "send":
            resp = send_telegram_voice(args.audio_path, caption=args.caption, chat_id=args.chat_id)
            print(json.dumps(resp, ensure_ascii=False))

        elif args.cmd == "process":
            transcript, reply, voice = process_telegram_voice_message(args.file_id, reply_template=args.template)
            result = {"transcript": transcript, "reply": reply, "voice": voice}
            print(json.dumps(result, ensure_ascii=False))
            if args.send:
                resp = send_telegram_voice(voice, caption=reply)
                print(json.dumps({"send_result": resp}, ensure_ascii=False))

    except TelegramError as e:
        print(f"ERROR: {e}", file=os.sys.stderr)
        raise SystemExit(2)
    except Exception as e:
        print(f"ERROR: 未预期的错误 - {e}", file=os.sys.stderr)
        raise SystemExit(3)


if __name__ == "__main__":
    main()
