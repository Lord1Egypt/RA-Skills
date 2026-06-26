#!/usr/bin/env python3
"""
合并截图分析和语音转录，生成文档内容
用法: python merge_and_generate.py <截图分析JSON> <语音转录JSON> <截图目录> <输出文件>
"""
import os
import sys
import json
from pathlib import Path

def load_json(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def match_voice_to_frame(timestamp: float, transcript_segments: list, window: int = 5) -> str:
    """根据时间戳匹配语音"""
    matched = []
    for seg in transcript_segments:
        if abs(seg.get("start", 0) - timestamp) <= window:
            matched.append(seg.get("text", ""))
    return " ".join(matched)

def generate_content(frames_analysis: dict, transcript: dict, frames_dir: str) -> dict:
    """
    合并截图分析和语音转录，生成文档内容
    
    Args:
        frames_analysis: {"frames": [{"timestamp": 0, "ui_elements": [...], "text_content": "..."}]}
        transcript: {"segments": [{"start": 0, "end": 2, "text": "..."}]}
        frames_dir: 截图目录
    
    Returns:
        文档内容结构
    """
    segments = transcript.get("segments", [])
    frames = frames_analysis.get("frames", [])
    
    steps = []
    for i, frame in enumerate(frames):
        timestamp = frame.get("timestamp", i * 6)
        
        # 匹配语音
        voice_text = match_voice_to_frame(timestamp, segments)
        
        # 从截图分析提取信息
        ui_elements = frame.get("ui_elements", [])
        text_content = frame.get("text_content", "")
        action_hint = frame.get("action_hint", "")
        
        # 生成标题：优先用 action_hint，否则用语音前10字
        if action_hint:
            title = action_hint[:15]
        elif voice_text:
            title = voice_text[:15].replace(" ", "")
        else:
            title = f"步骤{i+1}"
        
        # 生成描述
        if ui_elements:
            ui_text = "、".join([f"「{e.get('text', '')}」{e.get('type', '')}" for e in ui_elements[:3]])
            description = f"界面包含：{ui_text}"
            if voice_text:
                description += f"\n操作说明：{voice_text}"
        elif voice_text:
            description = voice_text
        else:
            description = "请参考截图进行操作"
        
        # 获取截图文件名
        frame_files = sorted(Path(frames_dir).glob("*.jpg"))
        frame_file = frame_files[i].name if i < len(frame_files) else f"frame_{i+1:03d}.jpg"
        
        steps.append({
            "step_num": i + 1,
            "title": title,
            "image_path": frame_file,
            "timestamp": timestamp,
            "description": description,
            "ui_elements": ui_elements,
            "voice_text": voice_text
        })
    
    return {
        "title": "操作指南",
        "overview": f"本文档共 {len(steps)} 个操作步骤，请按顺序执行。",
        "steps": steps,
        "notes": ["请按步骤顺序操作", "如有疑问请参考原视频教程"]
    }

def main():
    if len(sys.argv) < 5:
        print("用法: python merge_and_generate.py <截图分析JSON> <语音转录JSON> <截图目录> <输出文件>")
        sys.exit(1)
    
    frames_analysis_file = sys.argv[1]
    transcript_file = sys.argv[2]
    frames_dir = sys.argv[3]
    output_file = sys.argv[4]
    
    frames_analysis = load_json(frames_analysis_file)
    transcript = load_json(transcript_file)
    
    content = generate_content(frames_analysis, transcript, frames_dir)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f"内容生成完成: {output_file}")
    print(f"共 {len(content['steps'])} 个步骤")

if __name__ == "__main__":
    main()
