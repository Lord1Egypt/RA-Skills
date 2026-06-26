#!/usr/bin/env python3
"""
TTS 合成模块：将文本转换为飞书兼容的语音消息格式。
支持 Edge TTS (首选) 和 pyttsx3 (本地降级)。
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
import tempfile
from typing import Optional

from config import get_settings
from utils import ensure_ffmpeg_exists, resolve_edge_tts

# 日志
logger = logging.getLogger(__name__)

# 常量
TEMP_DIR = os.path.join("/tmp", "voice-chat")
os.makedirs(TEMP_DIR, exist_ok=True)

TEMP_MP3_PREFIX = "tts_temp_"
TEMP_MP3_SUFFIX = ".mp3"
TEMP_OGG_PREFIX = "voice_chat_"
TEMP_OGG_SUFFIX = ".ogg"


class TTSGenerationError(Exception):
    """TTS 生成过程中的自定义异常"""
    pass


def synthesize_with_edge_tts(text: str, mp3_path: str, voice: str) -> bool:
    """尝试使用 Edge TTS 生成语音。成功返回 True，失败返回 False。"""
    try:
        edge_tts_bin = resolve_edge_tts(get_settings().EDGE_TTS_BIN)
        if edge_tts_bin.startswith("python"):
            cmd = [sys.executable, "-m", "edge_tts", "--text", text, "--write-media", mp3_path, "--voice", voice]
        else:
            cmd = [edge_tts_bin, "--text", text, "--write-media", mp3_path, "--voice", voice]
        
        logger.info("尝试使用 Edge TTS...")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        
        if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
            logger.info("Edge TTS 成功。")
            return True
        else:
            logger.warning("Edge TTS 生成的文件为空。")
            return False
    except subprocess.TimeoutExpired:
        logger.warning("Edge TTS 超时。")
        return False
    except subprocess.CalledProcessError as e:
        logger.warning(f"Edge TTS 失败：{e.stderr.decode('utf-8', errors='ignore') if e.stderr else '未知错误'}")
        return False
    except Exception as e:
        logger.warning(f"Edge TTS 异常：{e}")
        return False


def synthesize_with_pyttsx3(text: str, mp3_path: str) -> bool:
    """尝试使用本地 pyttsx3 生成语音。成功返回 True，失败返回 False。"""
    try:
        import pyttsx3
        logger.info("降级使用本地 pyttsx3...")
        
        engine = pyttsx3.init()
        # 设置中文语音（如果可用）
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'zh' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.setProperty('rate', 180)  # 语速
        engine.setProperty('volume', 1.0)  # 音量
        
        # pyttsx3 直接输出到文件（部分版本支持）或先输出到 stdout 再保存
        # 这里使用 save_to_file 方法
        engine.save_to_file(text, mp3_path)
        engine.runAndWait()
        
        if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
            logger.info("pyttsx3 成功。")
            return True
        else:
            logger.warning("pyttsx3 生成的文件为空。")
            return False
    except ImportError:
        logger.error("pyttsx3 未安装。")
        return False
    except Exception as e:
        logger.error(f"pyttsx3 异常：{e}")
        return False


def synthesize_to_feishu_voice(text: str, voice: Optional[str] = None, output_dir: Optional[str] = None) -> str:
    """
    将文本合成为飞书兼容的 OGG/Opus 语音文件。
    策略：先尝试 Edge TTS，失败后自动降级到 pyttsx3。
    """
    settings = get_settings()
    voice = voice or settings.DEFAULT_VOICE
    text = text.strip()
    
    if not text:
        raise ValueError("合成文本不能为空")

    with tempfile.NamedTemporaryFile(prefix=TEMP_MP3_PREFIX, suffix=TEMP_MP3_SUFFIX, dir=TEMP_DIR, delete=False) as mp3_tmp:
        mp3_path = mp3_tmp.name
    with tempfile.NamedTemporaryFile(prefix=TEMP_OGG_PREFIX, suffix=TEMP_OGG_SUFFIX, dir=TEMP_DIR, delete=False) as ogg_tmp:
        ogg_path = ogg_tmp.name

    try:
        ensure_ffmpeg_exists()

        # 步骤 1: 尝试 Edge TTS
        mp3_success = False
        if not synthesize_with_edge_tts(text, mp3_path, voice):
            # 步骤 2: 降级到 pyttsx3
            if not synthesize_with_pyttsx3(text, mp3_path):
                raise TTSGenerationError("Edge TTS 和 pyttsx3 均失败，无法生成语音。")

        # 步骤 3: 使用 ffmpeg 转换为 OGG/Opus
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", mp3_path,
            "-c:a", "libopus", "-b:a", "64k",
            "-ar", "48000", "-ac", "1",
            "-application", "audio", "-frame_size", "60",
            "-f", "ogg",
            ogg_path
        ]
        logger.info("开始转码为 OGG/Opus (ffmpeg)...")
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=60)

        if not os.path.exists(ogg_path) or os.path.getsize(ogg_path) == 0:
            raise TTSGenerationError("ffmpeg 未生成有效输出文件。")

        # 清理临时 MP3
        try:
            os.remove(mp3_path)
        except OSError:
            pass

        logger.info(f"TTS 生成成功：{ogg_path}")
        return ogg_path

    except subprocess.TimeoutExpired:
        raise TTSGenerationError("TTS 生成或转码超时。")
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr.decode('utf-8', errors='ignore') if e.stderr else '未知错误'
        raise TTSGenerationError(f"TTS 转码失败：{stderr_msg}")
    except Exception as e:
        raise TTSGenerationError(f"TTS 生成失败：{e}")


def main():
    """命令行入口点"""
    if len(sys.argv) < 2:
        print("Usage: reply_with_tts.py <text> [--voice <voice_name>]", file=sys.stderr)
        sys.exit(1)

    text_parts = []
    voice = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--voice" and i + 1 < len(sys.argv):
            voice = sys.argv[i + 1]
            i += 2
        else:
            text_parts.append(sys.argv[i])
            i += 1
    text = " ".join(text_parts)

    try:
        voice_path = synthesize_to_feishu_voice(text, voice)
        print(voice_path)
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
