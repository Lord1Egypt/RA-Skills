#!/usr/bin/env python3
"""
mlx-qwen3-asr CLI 转写脚本（Apple Silicon MLX 版本）
用法: python3 transcribe.py -f <音频文件路径>
输出: 纯文本到 stdout（OpenClaw 读取这个）
"""

import argparse
import os
import sys
import subprocess
import tempfile
import warnings
warnings.filterwarnings("ignore")

# 需要 ffmpeg 转换的格式
CONVERT_EXTS = {".silk", ".slk", ".amr", ".ogg", ".opus", ".webm", ".m4a", ".mp4", ".aac"}


def convert_to_wav(input_path: str) -> str:
    """用 ffmpeg 转换为 16kHz 单声道 WAV"""
    wav_path = tempfile.mktemp(suffix=".wav")
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", input_path,
             "-ar", "16000", "-ac", "1", "-f", "wav", wav_path],
            capture_output=True, timeout=60
        )
        if result.returncode == 0 and os.path.exists(wav_path):
            return wav_path
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return ""


def main():
    parser = argparse.ArgumentParser(description="mlx-qwen3-asr 语音转文字")
    parser.add_argument("-f", "--file", required=True, help="音频文件路径")
    parser.add_argument(
        "--model",
        default=os.environ.get("MLX_ASR_MODEL", "Qwen/Qwen3-ASR-0.6B"),
        help="ASR 模型 (默认: Qwen/Qwen3-ASR-0.6B)"
    )
    args = parser.parse_args()

    # 检查文件
    if not os.path.isfile(args.file):
        print(f"错误: 文件不存在 - {args.file}", file=sys.stderr)
        sys.exit(1)

    if os.path.getsize(args.file) == 0:
        print("错误: 文件为空", file=sys.stderr)
        sys.exit(1)

    # 判断是否需要格式转换
    ext = os.path.splitext(args.file)[1].lower()
    converted_path = ""
    audio_path = args.file

    if ext in CONVERT_EXTS:
        converted_path = convert_to_wav(args.file)
        if converted_path:
            audio_path = converted_path

    try:
        # ====== 使用 mlx-qwen3-asr 转录 ======
        from mlx_qwen3_asr import transcribe

        result = transcribe(audio_path, model=args.model)

        # 提取文本
        if isinstance(result, dict):
            text = result.get("text", "").strip()
        elif hasattr(result, "text"):
            text = result.text.strip()
        else:
            text = str(result).strip()

        if not text:
            text = "[无法识别语音内容]"

        # 输出纯文本到 stdout（OpenClaw 要求）
        print(text)

    except Exception as e:
        print(f"转录错误: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # 清理临时文件
        if converted_path and os.path.exists(converted_path):
            try:
                os.unlink(converted_path)
            except OSError:
                pass


if __name__ == "__main__":
    main()
