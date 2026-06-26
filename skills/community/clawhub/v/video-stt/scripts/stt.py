#!/usr/bin/env python3
"""
Video STT - Extract audio from video and transcribe using Whisper
使用 uv 管理虚拟环境
"""

import subprocess
import os
import sys
import json
import argparse
from pathlib import Path

# 使用 uv 运行
def run_with_uv(cmd: list):
    """使用 uv 运行命令"""
    return subprocess.run(["uv", "run", "python"] + cmd, check=True)

# 检查依赖
def check_dependencies():
    """检查必要的命令是否可用"""
    for cmd in ["yt-dlp", "ffmpeg"]:
        result = subprocess.run(["which", cmd], capture_output=True)
        if result.returncode != 0:
            print(f"Warning: {cmd} not found. Installing...")
            subprocess.run(["brew", "install", cmd], check=False)

# 下载音频
def download_audio(url: str, output_dir: Path) -> str:
    """从视频 URL 下载音频"""
    audio_file = output_dir / f"audio_{int(subprocess.run(['date', '+%s'], capture_output=True, text=True).stdout.strip())}.wav"
    
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "-o", str(audio_file.with_suffix(".%(ext)s")),
        "--extract-audio",
        "--audio-format", "wav",
        url
    ]
    
    print(f"Downloading audio from: {url}")
    subprocess.run(cmd, check=True, capture_output=True)
    
    # 找到实际下载的文件
    actual_file = max(output_dir.glob("audio_*.wav"), key=os.path.getmtime)
    return str(actual_file)

# 转录
def transcribe(audio_path: str, model: str = "base", output_path: str = None) -> dict:
    """使用 Whisper 转录音频"""
    try:
        import whisper
    except ImportError:
        print("Installing whisper...")
        subprocess.run(["uv", "pip", "install", "whisper"], check=True)
        import whisper
    
    print(f"Loading Whisper {model} model...")
    whisper_model = whisper.load_model(model)
    
    print("Transcribing...")
    result = whisper_model.transcribe(audio_path)
    
    return result

# 保存结果
def save_output(result: dict, output_path: str, format: str = "txt"):
    """保存转录结果"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == "json":
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
    elif format == "srt":
        with open(output_path, "w") as f:
            for i, segment in enumerate(result["segments"], 1):
                start = segment["start"]
                end = segment["end"]
                content = segment["text"]
                
                # SRT 时间格式
                def fmt_srt(t):
                    h = int(t // 3600)
                    m = int((t % 3600) // 60)
                    s = int(t % 60)
                    ms = int((t % 1) * 1000)
                    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                
                f.write(f"{i}\n")
                f.write(f"{fmt_srt(start)} --> {fmt_srt(end)}\n")
                f.write(f"{content}\n\n")
    else:
        # Plain text
        with open(output_path, "w") as f:
            f.write(result["text"])
    
    print(f"Saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Video STT - 转录视频音频")
    parser.add_argument("url", help="视频 URL")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-m", "--model", default="base", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper 模型 (默认: base)")
    parser.add_argument("-f", "--format", default="txt",
                        choices=["txt", "srt", "vtt", "json"],
                        help="输出格式 (默认: txt)")
    
    args = parser.parse_args()
    
    # 目录
    script_dir = Path(__file__).parent
    audio_dir = script_dir / "audio"
    output_dir = script_dir / "output"
    audio_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # 检查依赖
    check_dependencies()
    
    # 下载
    audio_path = download_audio(args.url, audio_dir)
    print(f"Audio: {audio_path}")
    
    # 转录
    result = transcribe(audio_path, args.model)
    
    # 输出
    if args.output:
        output_path = args.output
    else:
        output_path = output_dir / f"transcript.{args.format}"
    
    save_output(result, str(output_path), args.format)
    
    # 打印内容
    print("\n--- Transcript ---")
    print(result["text"])

if __name__ == "__main__":
    main()
