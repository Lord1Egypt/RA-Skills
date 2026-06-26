#!/usr/bin/env python3
"""
Whisper GPU 音频转字幕脚本
支持 Intel XPU / NVIDIA CUDA / AMD ROCm / Apple Metal 四种 GPU 加速
自动检测设备，适配最优运行配置
"""
import whisper
import os
import sys
import torch
import argparse


def detect_device():
    """自动检测可用 GPU 设备，按优先级返回 (device, fp16)"""
    if hasattr(torch, 'xpu') and torch.xpu.is_available():
        return "xpu", False  # Intel XPU 不支持 FP16
    elif torch.cuda.is_available():
        return "cuda", True  # NVIDIA CUDA 支持 FP16
    elif hasattr(torch, 'hip') and torch.hip.is_available():
        return "hip", True   # AMD ROCm 支持 FP16
    elif hasattr(torch, 'backends') and torch.backends.mps.is_available():
        return "mps", True   # Apple Metal 支持 FP16
    else:
        return "cpu", False  # CPU 不支持 FP16


def get_device_name(device):
    """获取设备名称"""
    try:
        if device == "xpu":
            return f"Intel XPU: {torch.xpu.get_device_name(0)}"
        elif device == "cuda":
            return f"NVIDIA CUDA: {torch.cuda.get_device_name(0)}"
        elif device == "hip":
            return f"AMD ROCm: {torch.hip.get_device_name(0)}"
        elif device == "mps":
            return "Apple Metal (M系列芯片)"
        else:
            return "CPU"
    except Exception:
        return device.upper()


def format_timestamp(seconds):
    """将秒数转换为 SRT 时间戳格式 HH:MM:SS,mmm"""
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)
    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000
    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000
    secs = milliseconds // 1_000
    milliseconds -= secs * 1_000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def transcribe(audio_file, model_name="turbo", language="zh", output_dir=None):
    """转录音频文件并保存为 SRT"""
    # 检查音频文件是否存在
    if not os.path.exists(audio_file):
        print(f"❌ 错误：文件不存在: {audio_file}")
        sys.exit(1)

    # 检测设备
    device, fp16 = detect_device()
    device_name = get_device_name(device)
    print(f"✅ 使用设备: {device_name}")
    print(f"   FP16 模式: {fp16}")

    # 确定输出目录
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(audio_file))
    os.makedirs(output_dir, exist_ok=True)

    print(f"📂 音频文件: {audio_file}")
    print(f"🤖 加载模型: {model_name} ...")

    # 加载模型
    try:
        model = whisper.load_model(model_name, device=device)
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        sys.exit(1)

    print(f"🎙️  开始转录（语言: {language}）...")

    # 转录
    try:
        result = model.transcribe(audio_file, language=language, fp16=fp16)
    except Exception as e:
        print(f"❌ 转录失败: {e}")
        sys.exit(1)

    # 生成 SRT 内容
    srt_content = ""
    for i, segment in enumerate(result["segments"], start=1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"

    # 输出文件路径
    basename = os.path.splitext(os.path.basename(audio_file))[0]
    output_file = os.path.join(output_dir, f"{basename}.srt")

    # 写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt_content)

    print(f"✅ 转录完成！")
    print(f"📄 SRT 文件: {output_file}")
    print(f"📊 共 {len(result['segments'])} 个字幕段")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisper GPU 音频转字幕")
    parser.add_argument("audio", help="音频文件路径")
    parser.add_argument("--model", default="turbo", help="Whisper 模型 (默认: turbo)")
    parser.add_argument("--language", default="zh", help="音频语言 (默认: zh 中文)")
    parser.add_argument("--output_dir", default=None, help="输出目录 (默认: 与音频同目录)")
    args = parser.parse_args()

    transcribe(
        audio_file=args.audio,
        model_name=args.model,
        language=args.language,
        output_dir=args.output_dir
    )
