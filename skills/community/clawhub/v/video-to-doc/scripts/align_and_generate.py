#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对齐截图和语音，生成文档内容（优化版）

使用提炼后的语音内容生成规范的操作步骤

用法:
    python align_and_generate.py <提炼后的JSON> <截图目录> <输出文件>
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


def load_json(file_path: str) -> dict:
    """加载 JSON 文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_frames(frames_dir: str) -> list:
    """
    获取截图列表
    
    Returns:
        [(文件名, 时间戳), ...]
    """
    frames = []
    
    # 尝试多种排序方式
    frame_files = list(Path(frames_dir).glob("*.jpg")) + \
                  list(Path(frames_dir).glob("*.png")) + \
                  list(Path(frames_dir).glob("*.jpeg"))
    
    frame_files = sorted(frame_files)
    
    for i, f in enumerate(frame_files):
        # 时间戳按序号估算（每6秒一帧）
        timestamp = i * 6
        frames.append((f.name, timestamp))
    
    return frames


def match_frame_to_segment(timestamp: float, frames: list, tolerance: int = 5) -> str:
    """
    根据时间戳匹配截图
    
    Args:
        timestamp: 语音片段开始时间
        frames: 截图列表 [(文件名, 时间戳), ...]
        tolerance: 容差（秒）
    
    Returns:
        匹配的图片文件名
    """
    for frame_name, frame_time in frames:
        if abs(frame_time - timestamp) <= tolerance:
            return frame_name
    
    # 找最近的
    if frames:
        closest = min(frames, key=lambda x: abs(x[1] - timestamp))
        return closest[0]
    
    return ""


def generate_steps_from_refined(refined_file: str, frames_dir: str, output_file: str) -> Dict:
    """
    从提炼后的语音生成操作步骤
    
    Args:
        refined_file: 提炼后的 JSON 文件
        frames_dir: 截图目录
        output_file: 输出文件
    """
    refined = load_json(refined_file)
    segments = refined.get("segments", [])
    frames = get_frames(frames_dir)
    
    steps = []
    for i, seg in enumerate(segments):
        # 匹配截图
        frame_name = match_frame_to_segment(seg["start"], frames)
        
        step = {
            "step_num": i + 1,
            "title": seg.get("title", f"步骤{i+1}"),
            "image_path": frame_name,
            "timestamp": seg.get("start", 0),
            "description": seg.get("description", ""),
            "voice_original": seg.get("voice_original", "")
        }
        steps.append(step)
    
    # 生成文档结构
    result = {
        "title": "操作指南",
        "overview": f"本文档共 {len(steps)} 个操作步骤，请按顺序执行。",
        "steps": steps,
        "notes": [
            "请按步骤顺序操作",
            "如有疑问请参考原视频教程",
            "界面元素名称以文档中标注的「」符号为准"
        ]
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"生成完成: {output_file}")
    print(f"共 {len(steps)} 个步骤")
    return result


def generate_steps_from_frames_and_transcript(
    frames_analysis_file: str,
    transcript_file: str,
    output_file: str
) -> Dict:
    """
    从截图分析和语音转录生成步骤（旧版兼容）
    
    Args:
        frames_analysis_file: 截图分析文件
        transcript_file: 语音转录文件
        output_file: 输出文件
    """
    frames_data = load_json(frames_analysis_file)
    transcript_data = load_json(transcript_file)
    
    frames = frames_data.get("frames", [])
    segments = transcript_data.get("segments", [])
    
    steps = []
    
    # 匹配逻辑：按时间顺序交错合并
    frame_idx = 0
    for seg in segments:
        seg_start = seg.get("start", 0)
        
        # 找到最接近的截图
        while frame_idx < len(frames):
            frame = frames[frame_idx]
            frame_time = frame.get("timestamp", 0)
            
            if frame_time >= seg_start - 3:  # 截图时间在语音前3秒内
                break
            frame_idx += 1
        
        if frame_idx >= len(frames):
            break
        
        frame = frames[frame_idx]
        
        step = {
            "step_num": len(steps) + 1,
            "title": frame.get("action_hint", f"步骤{len(steps)+1}"),
            "image_path": frame.get("image_path", ""),
            "timestamp": frame_time,
            "voice_text": seg.get("text", ""),
            "description": frame.get("action_hint", ""),
            "ui_elements": frame.get("ui_elements", [])
        }
        steps.append(step)
        frame_idx += 1
    
    result = {
        "title": "操作指南",
        "overview": f"本文档共 {len(steps)} 个操作步骤",
        "steps": steps,
        "notes": ["请按步骤顺序操作"]
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  # 新版（推荐）：使用提炼后的JSON")
        print("  python align_and_generate.py <提炼后的JSON> <截图目录> <输出文件>")
        print("")
        print("  # 旧版兼容：使用截图分析和语音转录")
        print("  python align_and_generate.py <截图分析文件> <语音转录文件> <输出文件> [video_name]")
        sys.exit(1)
    
    arg1 = sys.argv[1]
    
    if len(sys.argv) == 4:
        # 新版用法：refined_json frames_dir output
        refined_file = arg1
        frames_dir = sys.argv[2]
        output_file = sys.argv[3]
        generate_steps_from_refined(refined_file, frames_dir, output_file)
    else:
        # 旧版用法：frames_analysis transcript output video_name
        frames_analysis_file = arg1
        transcript_file = sys.argv[2]
        output_file = sys.argv[3]
        video_name = sys.argv[4] if len(sys.argv) > 4 else "操作指南"
        generate_steps_from_frames_and_transcript(
            frames_analysis_file, transcript_file, output_file
        )


if __name__ == "__main__":
    main()
