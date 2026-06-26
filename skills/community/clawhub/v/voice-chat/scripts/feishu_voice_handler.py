#!/usr/bin/env python3
"""
飞书语音消息处理主流程：
1. 接收音频文件路径
2. 转写为文本
3. 生成回复文本
4. 合成语音回复
5. 输出结果供后续发送

此脚本为最小可用闭环，后续将集成到 OpenClaw 自动触发流程中。
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Tuple, Optional

# 添加当前目录到路径，以便导入同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import get_settings
from transcribe_audio import transcribe, TranscriptionError
from reply_with_tts import synthesize_to_feishu_voice, TTSGenerationError
from utils import ensure_file

logger = logging.getLogger(__name__)


class VoiceHandlerError(Exception):
    """语音处理流程中的自定义异常"""
    pass


def process_feishu_voice_message(
    audio_path: str,
    reply_template: Optional[str] = None
) -> Tuple[str, str, str]:
    """
    纯处理模式：接收 OpenClaw 已下载的本地音频路径，完成：转写 -> 生成回复 -> TTS。

    Args:
        audio_path: 输入音频文件路径 (OGG/Opus/WAV/MP3)
        reply_template: 回复文本模板，支持 {transcript} 占位符
                       默认："陛下，您说：{transcript}。我已收到。"

    Returns:
        (transcript, reply_text, voice_path) 元组：
        - transcript: 转写后的原文
        - reply_text: 生成的回复文本
        - voice_path: 生成的语音文件路径 (OGG/Opus)

    Raises:
        FileNotFoundError: 音频文件不存在
        TranscriptionError: 转写失败
        TTSGenerationError: TTS 合成失败
        ValueError: 输入参数无效
    """
    audio_file = ensure_file(audio_path)

    # 步骤 1: 转写
    try:
        logger.info("开始转写音频…")
        transcript = transcribe(str(audio_file))
        if not transcript:
            raise VoiceHandlerError("转写结果为空")
    except (TranscriptionError, FileNotFoundError) as e:
        raise VoiceHandlerError(f"转写失败：{e}") from e

    # 步骤 2: 生成回复文本
    if reply_template is None:
        reply_template = "陛下，您说：{transcript}。我已收到。"

    try:
        reply_text = reply_template.format(transcript=transcript)
    except KeyError as e:
        raise VoiceHandlerError(f"回复模板格式错误：缺少占位符 {e}") from e

    # 步骤 3: 合成语音
    try:
        logger.info("开始 TTS 合成…")
        voice_path = synthesize_to_feishu_voice(reply_text)
    except (TTSGenerationError, ValueError) as e:
        raise VoiceHandlerError(f"TTS 合成失败：{e}") from e

    return transcript, reply_text, voice_path


def main() -> None:
    """命令行入口点"""
    if len(sys.argv) < 2:
        print('Usage: feishu_voice_handler.py <audio_file>', file=sys.stderr)
        print('Example: feishu_voice_handler.py /tmp/audio.ogg', file=sys.stderr)
        print('可选参数：--template "<回复模板>"', file=sys.stderr)
        print('默认模板：陛下，您说：{transcript}。我已收到。', file=sys.stderr)
        sys.exit(1)

    # 解析参数
    audio_file: Optional[str] = None
    reply_template: Optional[str] = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--template' and i + 1 < len(sys.argv):
            reply_template = sys.argv[i + 1]
            i += 2
        elif audio_file is None:
            audio_file = sys.argv[i]
            i += 1
        else:
            print(f'未知参数：{sys.argv[i]}', file=sys.stderr)
            sys.exit(1)

    if audio_file is None:
        print('错误：必须提供音频文件路径', file=sys.stderr)
        sys.exit(1)

    try:
        transcript, reply_text, voice_path = process_feishu_voice_message(
            audio_file,
            reply_template,
        )

        # 输出 JSON
        print(json.dumps({
            "transcript": transcript,
            "reply": reply_text,
            "voice": voice_path,
            "status": "ok",
        }, ensure_ascii=False))

        sys.exit(0)

    except (FileNotFoundError, VoiceHandlerError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f'ERROR: 未预期的错误 - {e}', file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    main()
