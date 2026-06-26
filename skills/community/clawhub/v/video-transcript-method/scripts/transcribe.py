#!/usr/bin/env python3
"""
Bilibili视频音频转录脚本
使用OpenAI Whisper模型将音频文件转录为带时间戳的文字稿

用法:
    python3 transcribe.py --input <audio_file> --output <output_file> [--model-size <size>]

参数:
    --input       输入音频文件路径（必需）
    --output      输出文字稿文件路径（必需）
    --model-size  Whisper模型大小（默认: medium）
                  可选: tiny, base, small, medium, large
"""

import argparse
import ssl
import sys

# 绕过SSL证书验证问题（macOS常见）
ssl._create_default_https_context = ssl._create_unverified_context

import whisper


def format_timestamp(seconds: float) -> str:
    """将秒数格式化为 [MM:SS] 时间戳"""
    minutes, secs = divmod(int(seconds), 60)
    return f"[{minutes:02d}:{secs:02d}]"


def transcribe_audio(input_path: str, output_path: str, model_size: str = "medium"):
    """
    使用Whisper转录音频文件并保存为文字稿

    Args:
        input_path: 输入音频文件路径
        output_path: 输出文字稿文件路径
        model_size: Whisper模型大小
    """
    print(f"正在加载Whisper {model_size}模型...")
    model = whisper.load_model(model_size)

    print(f"正在转录音频: {input_path}")
    result = model.transcribe(input_path, language="zh", verbose=False)

    # 写入带时间戳的文字稿
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in result["segments"]:
            start = seg["start"]
            text = seg["text"].strip()
            if text:
                timestamp = format_timestamp(start)
                f.write(f"{timestamp} {text}\n")

    # 统计信息
    total_segments = len([s for s in result["segments"] if s["text"].strip()])
    duration = result["segments"][-1]["end"] if result["segments"] else 0
    minutes, secs = divmod(int(duration), 60)

    print(f"转录完成！")
    print(f"  音频时长: {minutes:02d}:{secs:02d}")
    print(f"  有效片段: {total_segments}")
    print(f"  输出文件: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="B站视频音频转录工具")
    parser.add_argument("--input", required=True, help="输入音频文件路径")
    parser.add_argument("--output", required=True, help="输出文字稿文件路径")
    parser.add_argument(
        "--model-size",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper模型大小（默认: medium）",
    )
    args = parser.parse_args()

    transcribe_audio(args.input, args.output, args.model_size)


if __name__ == "__main__":
    main()
