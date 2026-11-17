#!/usr/bin/env python3
"""
transcribe.py — 视频语音转文字工具

将视频文件转为文字稿，使用 OpenAI Whisper 进行语音识别。

Usage:
    python3 transcribe.py <video_path> [video_path2 ...] [options]

Options:
    --model <model>       Whisper 模型 (默认: base)
                          可选: tiny, base, small, medium, large, turbo
    --language <lang>     语言代码 (默认: 自动检测)
                          例如: zh, en, ja
    --output-dir <dir>    输出目录 (默认: 视频所在目录)
    --device <device>     计算设备 (默认: auto, 自动选择最佳设备)
                          可选: cpu, mps (Apple Silicon), cuda (NVIDIA)
    --strip-silence       裁剪静音段落（默认开启，减少无效音频长度）
    --no-strip-silence    关闭静音裁剪
    --speed <factor>      音频变速系数 (默认: 1.0, 推荐 1.0-1.5)
                          1.3 ≈ 快 23%, 对精度影响极小

支持的模型耗时参考 (CPU, 中文):
  - tiny:   ~实时0.5x (最快, 精度较低)
  - base:   ~实时的1x   (推荐日常使用)
  - small:  ~实时的2x   (精度较好)
  - medium: ~实时的4x   (精度很好)
  - large:  ~实时的8x   (精度最高, 很慢)
  - turbo:  ~实时的4x   (推荐长视频, 精度接近large)
"""

import argparse
import os
import sys
import time
import json
import shutil
import subprocess


def detect_ffmpeg():
    """检查 ffmpeg 是否可用"""
    if shutil.which("ffmpeg") is None:
        print("错误: 未找到 ffmpeg。请先安装: brew install ffmpeg")
        sys.exit(1)


def get_video_duration(video_path):
    """获取视频时长(分钟)"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
             video_path],
            capture_output=True, text=True, timeout=30
        )
        duration_sec = float(result.stdout.strip())
        return duration_sec / 60.0
    except Exception:
        return None


def extract_audio(video_path, audio_path, strip_silence=True, speed=1.0):
    """从视频中提取音频，支持静音裁剪和变速"""
    print(f"  🎵 提取音频: {os.path.basename(video_path)}")

    # 构建音频滤镜链
    filter_parts = []

    if strip_silence:
        # 裁剪首尾静音 + 中间 >0.5s 的停顿
        # 使用 reverse 两次分别裁剪开头和结尾的静音
        filter_parts.append(
            "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:"
            "detection=peak,aformat=dblp,areverse,"
            "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:"
            "detection=peak,aformat=dblp,areverse"
        )

    if speed != 1.0:
        # atempo 保持音调的同时变速，范围 0.5-2.0
        clamped = max(0.5, min(2.0, speed))
        filter_parts.append(f"atempo={clamped}")

    filter_str = ",".join(filter_parts) if filter_parts else None

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",           # 不处理视频
        "-acodec", "pcm_s16le",  # PCM 16-bit
        "-ar", "16000",  # 16kHz 采样率 (whisper 最佳)
        "-ac", "1",      # 单声道
    ]

    if filter_str:
        cmd.extend(["-af", filter_str])
        if strip_silence:
            print(f"    🔇 裁剪静音段落 — 减少无效音频时长")
        if speed != 1.0:
            print(f"    ⏩ 变速: {speed}x — 减少转写时长约 {(1 - 1/speed)*100:.0f}%")

    cmd.append(audio_path)

    original_size = os.path.getsize(video_path) if os.path.exists(video_path) else 0
    start = time.time()

    result = subprocess.run(cmd, capture_output=True, text=True)

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  ❌ 音频提取失败: {result.stderr}")
        return False

    # 报告压缩效果
    output_size = os.path.getsize(audio_path) if os.path.exists(audio_path) else 0
    if original_size > 0 and output_size > 0:
        ratio = output_size / original_size
        print(f"    💾 音频 {original_size/1024/1024:.0f}MB → {output_size/1024/1024:.0f}MB ({ratio*100:.0f}%)")

    print(f"    ⏱  ffmpeg 耗时: {elapsed:.1f}秒")
    return True


def transcribe(audio_path, model, language=None, device="cpu"):
    """使用 whisper 进行语音识别"""
    import whisper

    print(f"  🤖 加载模型: {model} (设备: {device})")
    start = time.time()

    whisper_model = whisper.load_model(model, device=device)

    transcribe_opts = {"verbose": False}
    if language:
        transcribe_opts["language"] = language

    print(f"  📝 开始转写... (这可能需要一段时间)")
    result = whisper_model.transcribe(audio_path, **transcribe_opts)

    elapsed = time.time() - start
    print(f"  ✅ 转写完成! 耗时: {elapsed:.0f}秒 ({elapsed/60:.1f}分钟)")
    return result


def write_output(result, output_path):
    """写入转写结果到文件"""
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in result.get("segments", []):
            start_ts = seg["start"]
            end_ts = seg["end"]
            text = seg["text"].strip()
            # 格式: [MM:SS -> MM:SS] 文本
            f.write(f"[{format_time(start_ts)} -> {format_time(end_ts)}] {text}\n")

    print(f"  💾 输出文件: {output_path}")


def format_time(seconds):
    """将秒数格式化为 MM:SS"""
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def process_video(video_path, model, language, output_dir, device,
                  strip_silence=True, speed=1.0):
    """处理单个视频文件"""
    if not os.path.exists(video_path):
        print(f"  ❌ 文件不存在: {video_path}")
        return False

    if not video_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm',
                                         '.flv', '.wmv', '.m4v', '.mp3', '.wav',
                                         '.m4a', '.flac', '.aac', '.ogg')):
        print(f"  ⚠️  跳过不支持的文件: {video_path}")
        return False

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{base_name}_audio.wav")
    output_txt = os.path.join(output_dir, f"{base_name}.txt")

    # 如果输出已存在，跳过
    if os.path.exists(output_txt):
        print(f"  ⏭️  已存在: {base_name}.txt，跳过")
        return True

    print(f"\n{'='*60}")
    print(f"🎬 处理: {os.path.basename(video_path)}")

    # 检查视频时长
    duration = get_video_duration(video_path)
    if duration:
        print(f"⏱️  时长: {duration:.1f}分钟")
        if duration > 120:
            print(f"⚠️  视频较长(>2小时)，建议只处理此单个文件以确保质量")
        # 建议开启加速
        if duration > 30 and not strip_silence and speed == 1.0:
            print(f"💡 建议: 长视频可加 --strip-silence 和 --speed 1.3 加速转写")

    # 提取音频（含静音裁剪 + 变速）
    if not extract_audio(video_path, audio_path, strip_silence, speed):
        return False

    # 转写
    try:
        result = transcribe(audio_path, model, language, device)
    except Exception as e:
        print(f"  ❌ 转写失败: {e}")
        return False
    finally:
        # 清理临时音频文件
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"  🧹 临时音频已清理")

    # 写入输出
    write_output(result, output_txt)

    return True


def main():
    parser = argparse.ArgumentParser(description="视频语音转文字工具")
    parser.add_argument("videos", nargs="+", help="视频文件路径")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "tiny.en", "base", "base.en",
                                 "small", "small.en", "medium", "medium.en",
                                 "large", "turbo"],
                        help="Whisper 模型 (默认: base)")
    parser.add_argument("--language", default=None,
                        help="语言代码 (默认: 自动检测)")
    parser.add_argument("--output-dir", default=None,
                        help="输出目录 (默认: 视频所在目录)")
    parser.add_argument("--device", default="auto",
                        help="计算设备 (默认: auto, 自动选择最佳设备; 可选: cpu, mps, cuda)")
    parser.add_argument("--strip-silence", action="store_true", default=True,
                        help="裁剪静音段落（默认开启）")
    parser.add_argument("--no-strip-silence", action="store_false", dest="strip_silence",
                        help="关闭静音裁剪")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="音频变速系数 (默认: 1.0, 推荐 1.0-1.5)")
    parser.add_argument("--max-files", type=int, default=3,
                        help="同时处理最大文件数 (默认: 3)")

    args = parser.parse_args()

    # 检查 ffmpeg
    detect_ffmpeg()

    # 自动检测最佳设备
    device = args.device
    if device == "auto":
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                print("🚀 检测到 NVIDIA GPU，使用 CUDA 加速")
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                device = "mps"
                print("🚀 检测到 Apple Silicon (MPS)，使用 GPU 加速")
            else:
                device = "cpu"
                print("💻 未检测到 GPU 加速，使用 CPU 模式")
        except ImportError:
            device = "cpu"
            print("💻 torch 版本不支持设备检测，使用 CPU 模式")
    elif device == "mps":
        print("🚀 手动指定 MPS (Apple Silicon GPU)")
    elif device == "cuda":
        print("🚀 手动指定 CUDA (NVIDIA GPU)")
    else:
        print(f"💻 使用 CPU 模式")

    videos = args.videos

    if "turbo" in str(args.model).lower():
        print("⚡ 使用 turbo 模型，兼顾速度与精度")

    # 限制处理数量
    if len(videos) > args.max_files:
        print(f"⚠️  一次最多处理 {args.max_files} 个文件，已截取前 {args.max_files} 个")
        videos = videos[:args.max_files]

    # 检查是否有超长视频
    for v in videos:
        dur = get_video_duration(v)
        if dur and dur > 120:
            print(f"\n⚠️  '{os.path.basename(v)}' 时长 {dur:.0f}分钟 (>2小时)")
            print(f"   建议只处理此单个文件。如需继续请移除其他文件或确认。")
            if len(videos) > 1:
                print(f"   仅处理此文件，忽略其他 {len(videos)-1} 个")
                videos = [v]
            break

    success = 0
    fail = 0

    for video in videos:
        # 确定输出目录
        out_dir = args.output_dir or os.path.dirname(os.path.abspath(video))
        ok = process_video(video, args.model, args.language, out_dir, device,
                          args.strip_silence, args.speed)
        if ok:
            success += 1
        else:
            fail += 1

    print(f"\n{'='*60}")
    print(f"📊 处理完成: {success} 成功, {fail} 失败")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
