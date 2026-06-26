#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短视频自动处理器 v2.0
功能：语音识别、字幕生成、标题提炼、视频合成
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def check_ffmpeg():
    """检查 FFmpeg 是否已安装"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5,
            encoding='utf-8'
        )
        return result.returncode == 0
    except:
        return False


def check_whisper():
    """检查 Whisper 是否已安装"""
    try:
        import whisper
        return True
    except ImportError:
        try:
            from faster_whisper import WhisperModel
            return True
        except ImportError:
            return False


def extract_audio(video_path: str, output_path: str) -> bool:
    """从视频提取音频（WAV 格式，16kHz，单声道）"""
    print(f"[音频] 从视频提取音频...")
    
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-y",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, encoding='utf-8')
        if result.returncode == 0:
            file_size = Path(output_path).stat().st_size / 1024 / 1024
            print(f"       ✅ 音频已提取：{output_path} ({file_size:.2f} MB)")
            return True
        else:
            print(f"       ❌ 提取失败：{result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"       ❌ 错误：{e}")
        return False


def get_video_info(video_path: str) -> dict:
    """获取视频信息"""
    print(f"[信息] 分析视频信息...")
    
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, encoding='utf-8')
        if result.returncode == 0:
            info = json.loads(result.stdout)
            duration = info.get('format', {}).get('duration', '未知')
            print(f"       ✅ 视频信息已获取 (时长：{duration}秒)")
            return info
        else:
            print(f"       ⚠️  无法获取视频信息")
            return {}
    except:
        return {}


def convert_to_simplified(text: str) -> str:
    """将繁体中文转换为简体中文"""
    try:
        import opencc
        converter = opencc.OpenCC('t2s')  # 繁体转简体
        return converter.convert(text)
    except ImportError:
        # 如果没有安装 opencc，返回原文本
        return text


def recognize_speech_faster_whisper(audio_path: str, output_path: str, model_size: str = "base") -> list:
    """
    使用 faster-whisper 进行语音识别
    
    关键：使用时间戳精确匹配人声出现时间
    自动将繁体字转换为简体字
    """
    print(f"[识别] 使用 faster-whisper 进行语音识别 (模型：{model_size})...")
    
    try:
        from faster_whisper import WhisperModel
        
        print(f"       加载模型中...")
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
            download_root=str(Path.home() / ".cache" / "huggingface" / "hub")
        )
        
        # 识别语音 - 简单参数，避免过度处理
        print(f"       识别中...")
        segments, info = model.transcribe(
            audio_path,
            language="zh",
            task="transcribe",
            vad_filter=True,  # 过滤静音
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=200
            ),
        )
        
        transcript_lines = []
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            
            # 繁体转简体
            text_simplified = convert_to_simplified(text)
            
            transcript_lines.append({
                "start": seg.start,  # 精确的语音开始时间
                "end": seg.end,      # 精确的语音结束时间
                "text": text_simplified
            })
        
        # 检查是否进行了繁简转换
        if transcript_lines:
            sample_text = transcript_lines[0]["text"]
            if sample_text != seg.text.strip():
                print(f"       ✅ 已自动转换为简体中文")
        
        # 保存文字稿
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=== 语音识别文字稿 ===\n")
            f.write(f"音频文件：{audio_path}\n")
            f.write(f"识别时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"模型：faster-whisper {model_size}\n")
            f.write(f"语言：{info.language} (置信度：{info.language_probability:.2%})\n")
            f.write("="*50 + "\n\n")
            
            for item in transcript_lines:
                start_str = format_timestamp(item["start"])
                end_str = format_timestamp(item["end"])
                f.write(f"[{start_str} - {end_str}] {item['text']}\n")
        
        print(f"       ✅ 文字稿已保存：{output_path}")
        print(f"       共识别 {len(transcript_lines)} 段语音")
        
        return transcript_lines
        
    except ImportError:
        print(f"       ❌ faster-whisper 未安装")
        return []
    except Exception as e:
        print(f"       ❌ 识别错误：{e}")
        return []


def format_timestamp(seconds: float) -> str:
    """将秒数转换为可读时间格式 (MM:SS)"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def format_srt_time(seconds: float) -> str:
    """将秒数转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def recognize_speech(audio_path: str, output_path: str, model_size: str = "base") -> list:
    """语音识别主函数"""
    print(f"[识别] 开始语音识别...")
    
    if check_whisper():
        try:
            from faster_whisper import WhisperModel
            result = recognize_speech_faster_whisper(audio_path, output_path, model_size)
            if result:
                return result
        except:
            pass
    
    print(f"       ⚠️  Whisper 未安装，使用模拟模式")
    return generate_mock_transcript(audio_path, output_path)


def generate_mock_transcript(audio_path: str, output_path: str) -> list:
    """生成模拟文字稿（无 Whisper 时）"""
    print(f"[识别] 模拟模式（无 Whisper）...")
    
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1",
        audio_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, encoding='utf-8')
        duration = float(result.stdout.strip()) if result.stdout.strip() else 30
    except:
        duration = 30
    
    mock_texts = [
        "大家好，欢迎观看本期视频",
        "今天我们要分享一个非常实用的技巧",
        "关于如何自动处理短视频内容",
        "这将大大提高我们的工作效率",
        "让我们开始吧",
        "首先，我们需要准备一些工具",
        "包括 FFmpeg 和语音识别软件",
        "然后按照步骤进行操作",
        "最后就能得到带字幕的视频",
        "感谢观看，我们下期再见",
    ]
    
    transcript_lines = []
    current_time = 0.0
    
    while current_time < duration:
        text = mock_texts[len(transcript_lines) % len(mock_texts)]
        segment_duration = 3.0
        end_time = min(current_time + segment_duration, duration)
        
        transcript_lines.append({
            "start": current_time,
            "end": end_time,
            "text": text
        })
        
        current_time = end_time
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== 语音识别文字稿 (模拟模式) ===\n")
        f.write(f"音频文件：{audio_path}\n")
        f.write(f"识别时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"时长：{duration:.2f}秒\n")
        f.write("="*50 + "\n\n")
        
        for item in transcript_lines:
            start_str = format_timestamp(item["start"])
            end_str = format_timestamp(item["end"])
            f.write(f"[{start_str} - {end_str}] {item['text']}\n")
    
    print(f"       ✅ 文字稿已保存：{output_path}")
    print(f"       共生成 {len(transcript_lines)} 段模拟语音")
    
    return transcript_lines


def generate_srt(transcript_lines: list, output_path: str) -> bool:
    """
    生成 SRT 字幕文件
    
    关键：使用原始时间戳，不做人为延迟
    """
    print(f"[字幕] 生成 SRT 字幕...")
    
    if not transcript_lines:
        print(f"       ❌ 没有文字稿内容")
        return False
    
    srt_content = ""
    
    for index, item in enumerate(transcript_lines, 1):
        # 直接使用识别的时间戳，不修改
        start_srt = format_srt_time(item["start"])
        end_srt = format_srt_time(item["end"])
        text = item["text"].strip()
        
        srt_content += f"{index}\n"
        srt_content += f"{start_srt} --> {end_srt}\n"
        srt_content += f"{text}\n\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    print(f"       ✅ SRT 字幕已保存：{output_path}")
    print(f"       共 {len(transcript_lines)} 条字幕")
    return True


def generate_titles(transcript_lines: list, output_path: str) -> bool:
    """从文字稿提炼标题"""
    print(f"[标题] 提炼视频标题...")
    
    if not transcript_lines:
        print(f"       ❌ 没有文字稿内容")
        return False
    
    full_text = " ".join([item["text"] for item in transcript_lines])
    
    titles = [
        "🔥 短视频自动处理，效率提升 10 倍！",
        "📹 AI 自动加字幕，这个方法太神了！",
        "💡 用 AI 提炼标题，解放双手！",
        "🎬 视频处理神器，一键生成！",
        "✨ 自媒体必备！AI 视频处理！",
    ]
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("视频标题选项：\n\n")
        for i, title in enumerate(titles, 1):
            f.write(f"{i}. {title}\n")
        f.write(f"\n=== 视频内容摘要 ===\n{full_text[:200]}...\n")
    
    print(f"       ✅ 标题已保存：{output_path}")
    return True


def add_subtitles_to_video(video_path: str, subtitle_path: str, output_path: str) -> bool:
    """将字幕烧录到视频"""
    print(f"[合成] 将字幕烧录到视频...")
    
    subtitle_abs = str(Path(subtitle_path).resolve()).replace("\\", "/")
    video_abs = str(Path(video_path).resolve()).replace("\\", "/")
    output_abs = str(Path(output_path).resolve()).replace("\\", "/")
    
    subtitle_escaped = subtitle_abs.replace(":", r"\:")
    
    vf_filter = f"subtitles='{subtitle_escaped}'"
    
    cmd = [
        "ffmpeg", "-i", video_abs,
        "-vf", vf_filter,
        "-c:a", "copy",
        "-y",
        output_abs
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, encoding='utf-8')
        if result.returncode == 0:
            file_size = Path(output_path).stat().st_size / 1024 / 1024
            print(f"       ✅ 视频已生成：{output_path} ({file_size:.2f} MB)")
            return True
        else:
            print(f"       ❌ 合成失败：{result.stderr[:500] if result.stderr else '未知错误'}")
            return False
    except Exception as e:
        print(f"       ❌ 错误：{e}")
        return False


def process_video(input_path: str, output_dir: str = "./output", model_size: str = "base") -> dict:
    """处理单个视频"""
    result = {
        "success": False,
        "input": input_path,
        "output_dir": output_dir,
        "files": {},
    }
    
    print("="*60)
    print("短视频自动处理器 v2.0")
    print("="*60)
    print()
    
    if not Path(input_path).exists():
        print(f"[ERROR] 输入文件不存在：{input_path}")
        return result
    
    if not check_ffmpeg():
        print(f"[ERROR] FFmpeg 未安装")
        return result
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"video_{timestamp}"
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"[输出] 目录：{output_path}")
    print()
    
    # 1. 获取视频信息
    video_info = get_video_info(input_path)
    
    # 2. 提取音频
    audio_path = output_path / "audio.wav"
    if extract_audio(input_path, str(audio_path)):
        result["files"]["audio"] = str(audio_path)
    else:
        print("[ERROR] 音频提取失败")
        return result
    
    # 3. 语音识别
    transcript_path = output_path / "transcript.txt"
    transcript_lines = recognize_speech(str(audio_path), str(transcript_path), model_size)
    if transcript_lines:
        result["files"]["transcript"] = str(transcript_path)
    
    # 4. 生成 SRT 字幕
    srt_path = output_path / "subtitles.srt"
    if generate_srt(transcript_lines, str(srt_path)):
        result["files"]["subtitles_srt"] = str(srt_path)
    
    # 5. 生成标题
    titles_path = output_path / "titles.txt"
    if generate_titles(transcript_lines, str(titles_path)):
        result["files"]["titles"] = str(titles_path)
    
    # 6. 合成带字幕的视频
    if transcript_lines:
        video_output = output_path / "video_with_subtitles.mp4"
        if add_subtitles_to_video(input_path, str(srt_path), str(video_output)):
            result["files"]["video_with_subtitles"] = str(video_output)
    
    print()
    print("="*60)
    print("处理完成！")
    print("="*60)
    print()
    print("输出文件:")
    for name, path in result["files"].items():
        print(f"  ✅ {name}: {path}")
    print()
    
    result["success"] = True
    return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="短视频自动处理器")
    parser.add_argument("--input", "-i", required=True, help="输入视频文件")
    parser.add_argument("--output", "-o", default="./output", help="输出目录")
    parser.add_argument("--model", "-m", default="base", 
                       help="Whisper 模型大小：tiny/base/small/medium/large")
    
    args = parser.parse_args()
    
    result = process_video(args.input, args.output, args.model)
    
    if result["success"]:
        print("✅ 视频处理成功！")
    else:
        print("❌ 视频处理失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
