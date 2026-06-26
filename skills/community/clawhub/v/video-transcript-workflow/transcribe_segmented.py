#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分段转录脚本
将长视频分段转录，避免长时间运行被系统终止

用法：
    python transcribe_segmented.py <视频文件> [模型大小] [语言] [分段分钟数]
"""

import sys
import os
import json
import time
from pathlib import Path

# Windows 控制台 UTF-8 编码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    
    # 添加 NVIDIA CUDA DLL 路径
    nvidia_paths = [
        os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "cublas", "bin"),
        os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "cudnn", "bin"),
    ]
    for nvidia_path in nvidia_paths:
        if os.path.exists(nvidia_path):
            os.add_dll_directory(nvidia_path)
            os.environ["PATH"] = nvidia_path + os.pathsep + os.environ.get("PATH", "")


def get_video_duration(file_path):
    """获取视频时长（秒）"""
    try:
        from faster_whisper import WhisperModel
        # 临时加载模型获取时长
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, info = model.transcribe(file_path, language="zh")
        _ = list(segments)  # 消费生成器
        return info.duration
    except Exception as e:
        print(f"无法获取视频时长: {e}")
        return None


def transcribe_segment(file_path, model_size, language, start_time, end_time, segment_index, output_dir):
    """转录视频的一个片段"""
    from faster_whisper import WhisperModel
    
    print(f"\n{'='*50}")
    print(f"📹 片段 {segment_index}: {start_time/60:.1f}分 - {end_time/60:.1f}分")
    print(f"{'='*50}")
    
    # 加载模型
    print("⏳ 加载模型...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print("✅ 模型加载完成")
    
    # 转录指定时间段
    segment_file = os.path.join(output_dir, f"segment_{segment_index:03d}.txt")
    all_text = []
    
    print(f"🔄 开始转录...")
    start = time.time()
    
    try:
        segments, info = model.transcribe(
            file_path,
            language=None if language == "auto" else language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        segment_count = 0
        for seg in segments:
            # 只保留在时间范围内的片段
            if seg.start >= end_time:
                break
            if seg.end >= start_time:
                # 调整时间码
                adjusted_start = max(0, seg.start - start_time)
                text = seg.text.strip()
                if text:
                    mins = int(adjusted_start // 60)
                    secs = int(adjusted_start % 60)
                    timestamp = f"[{mins:02d}:{secs:02d}]"
                    line = f"{timestamp} {text}"
                    all_text.append(line)
                    print(line)
                    segment_count += 1
        
        elapsed = time.time() - start
        print(f"\n✅ 片段 {segment_index} 完成！共 {segment_count} 个片段，用时 {elapsed:.1f}秒")
        
        # 保存片段文件
        with open(segment_file, "w", encoding="utf-8") as f:
            f.write(f"# 片段 {segment_index}: {start_time/60:.1f}分 - {end_time/60:.1f}分\n\n")
            f.write("\n".join(all_text))
        
        return all_text, segment_count
        
    except Exception as e:
        print(f"❌ 片段 {segment_index} 转录失败: {e}")
        return [], 0


def transcribe_full(file_path, model_size, language, output_dir):
    """完整转录（不分段）"""
    from faster_whisper import WhisperModel
    
    print(f"\n{'='*50}")
    print(f"📹 完整转录")
    print(f"{'='*50}")
    
    # 加载模型
    print("⏳ 加载模型...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print("✅ 模型加载完成")
    
    # 转录
    segment_file = os.path.join(output_dir, "full_transcript.txt")
    all_text = []
    
    print(f"🔄 开始转录...")
    start = time.time()
    
    try:
        segments, info = model.transcribe(
            file_path,
            language=None if language == "auto" else language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        print(f"📊 音频时长: {info.duration:.1f}秒 ({info.duration/60:.1f}分钟)")
        print(f"🌐 检测语言: {info.language}")
        print()
        
        segment_count = 0
        last_save_count = 0
        
        for seg in segments:
            segment_count += 1
            mins = int(seg.start // 60)
            secs = int(seg.start % 60)
            timestamp = f"[{mins:02d}:{secs:02d}]"
            text = seg.text.strip()
            if text:
                line = f"{timestamp} {text}"
                all_text.append(line)
                print(line)
            
            # 每 500 个片段保存一次进度
            if segment_count - last_save_count >= 500:
                save_progress(output_dir, all_text, segment_count, info.duration)
                last_save_count = segment_count
                print(f"\n💾 已保存进度: {segment_count} 片段\n")
        
        elapsed = time.time() - start
        print(f"\n✅ 转录完成！共 {segment_count} 个片段，用时 {elapsed/60:.1f}分钟")
        
        # 保存完整文件
        with open(segment_file, "w", encoding="utf-8") as f:
            f.write(f"# 完整转录\n\n")
            f.write(f"> 音频时长: {info.duration:.1f}秒 ({info.duration/60:.1f}分钟)\n")
            f.write(f"> 转录模型: {model_size}\n")
            f.write(f"> 片段数量: {segment_count}\n\n")
            f.write("-" * 50 + "\n\n")
            f.write("\n".join(all_text))
        
        return all_text, segment_count, info.duration
        
    except Exception as e:
        print(f"❌ 转录失败: {e}")
        # 保存已转录内容
        if all_text:
            save_progress(output_dir, all_text, segment_count, 0)
        raise


def save_progress(output_dir, text_lines, segment_count, total_duration):
    """保存进度"""
    progress_file = os.path.join(output_dir, "progress.json")
    transcript_file = os.path.join(output_dir, "transcript_progress.txt")
    
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump({
            "segment_count": segment_count,
            "total_duration": total_duration,
            "lines_count": len(text_lines),
            "timestamp": time.time()
        }, f, indent=2)
    
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write("\n".join(text_lines))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n❌ 错误：请指定视频文件路径")
        print("💡 示例：python transcribe_segmented.py video.mp4 base zh 20")
        sys.exit(1)
    
    file_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    language = sys.argv[3] if len(sys.argv) > 3 else "zh"
    segment_minutes = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    # 创建输出目录
    file_name = Path(file_path).stem
    output_dir = os.path.join(Path(file_path).parent, f"{file_name}_转录输出")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 文件: {file_path}")
    print(f"🤖 模型: {model_size}")
    print(f"🌐 语言: {language}")
    print(f"📂 输出目录: {output_dir}")
    print()
    
    # 使用完整转录（带进度保存）
    transcribe_full(file_path, model_size, language, output_dir)


if __name__ == "__main__":
    main()