#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕后处理器
功能：从修改后的文字稿重新生成字幕和视频
"""

import sys
import os
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# 默认字幕样式配置
DEFAULT_SUBTITLE_STYLE = {
    "font": "Arial",           # 字体
    "fontsize": 24,            # 字号
    "primary_color": "&H00FFFFFF",  # 主颜色（白色）
    "outline_color": "&H00000000",  # 轮廓颜色（黑色）
    "back_color": "&H00000000",     # 背景颜色（透明）
    "bold": 0,                 # 粗体 (0/1)
    "italic": 0,               # 斜体 (0/1)
    "underline": 0,            # 下划线 (0/1)
    "strikeout": 0,            # 删除线 (0/1)
    "border_style": 4,         # 边框样式 (1=框，4=阴影)
    "outline": 2,              # 轮廓宽度
    "shadow": 0,               # 阴影
    "alignment": 2,            # 对齐 (2=中下，8=中上)
    "margin_l": 10,            # 左边距
    "margin_r": 10,            # 右边距
    "margin_v": 50,            # 垂直边距
    "alpha": "00",             # 透明度 (00=不透明，FF=全透明)
}


def load_subtitle_style(config_path: str = None) -> dict:
    """加载字幕样式配置"""
    style = DEFAULT_SUBTITLE_STYLE.copy()
    
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                custom_style = json.load(f)
                style.update(custom_style)
                print(f"[样式] 已加载自定义样式：{config_path}")
        except Exception as e:
            print(f"[样式] 加载配置失败：{e}，使用默认样式")
    
    return style


def save_subtitle_style(style: dict, config_path: str):
    """保存字幕样式配置"""
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(style, f, indent=2, ensure_ascii=False)
    print(f"[样式] 配置已保存：{config_path}")


def parse_transcript(transcript_path: str) -> list:
    """
    解析文字稿文件
    
    格式：[MM:SS - MM:SS] 文字内容
    或：[HH:MM:SS - HH:MM:SS] 文字内容
    """
    print(f"[解析] 读取文字稿：{transcript_path}")
    
    if not Path(transcript_path).exists():
        print(f"       ❌ 文件不存在")
        return []
    
    transcript_lines = []
    time_pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+)')
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('=') or line.startswith('音频') or line.startswith('识别') or line.startswith('模型'):
                continue
            
            match = time_pattern.match(line)
            if match:
                start_str = match.group(1)
                end_str = match.group(2)
                text = match.group(3).strip()
                
                # 转换为秒数
                start_sec = time_to_seconds(start_str)
                end_sec = time_to_seconds(end_str)
                
                transcript_lines.append({
                    "start": start_sec,
                    "end": end_sec,
                    "text": text
                })
    
    print(f"       ✅ 解析成功，共 {len(transcript_lines)} 段")
    return transcript_lines


def time_to_seconds(time_str: str) -> float:
    """将时间字符串转换为秒数"""
    parts = time_str.split(':')
    if len(parts) == 3:
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    return 0.0


def seconds_to_srt(seconds: float) -> str:
    """将秒数转换为 SRT 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt(transcript_lines: list, output_path: str) -> bool:
    """生成 SRT 字幕文件"""
    print(f"[字幕] 生成 SRT 字幕...")
    
    if not transcript_lines:
        print(f"       ❌ 没有内容")
        return False
    
    srt_content = ""
    
    for index, item in enumerate(transcript_lines, 1):
        start_srt = seconds_to_srt(item["start"])
        end_srt = seconds_to_srt(item["end"])
        text = item["text"].strip()
        
        srt_content += f"{index}\n"
        srt_content += f"{start_srt} --> {end_srt}\n"
        srt_content += f"{text}\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    print(f"       ✅ SRT 已保存：{output_path}")
    return True


def style_to_ass_string(style: dict) -> str:
    """将样式字典转换为 ASS 格式字符串"""
    return (
        f"FontName={style['font']},"
        f"FontSize={style['fontsize']},"
        f"PrimaryColour={style['primary_color']},"
        f"OutlineColour={style['outline_color']},"
        f"BackColour={style['back_color']},"
        f"Bold={style['bold']},"
        f"Italic={style['italic']},"
        f"Underline={style['underline']},"
        f"StrikeOut={style['strikeout']},"
        f"BorderStyle={style['border_style']},"
        f"Outline={style['outline']},"
        f"Shadow={style['shadow']},"
        f"Alignment={style['alignment']},"
        f"MarginL={style['margin_l']},"
        f"MarginR={style['margin_r']},"
        f"MarginV={style['margin_v']},"
        f"Alpha={style['alpha']}"
    )


def add_subtitles_to_video(video_path: str, subtitle_path: str, output_path: str, style: dict = None) -> bool:
    """将字幕烧录到视频（支持自定义样式）"""
    print(f"[合成] 将字幕烧录到视频...")
    
    if style is None:
        style = DEFAULT_SUBTITLE_STYLE
    
    # 使用相对路径（FFmpeg 兼容性更好）
    subtitle_rel = str(Path(subtitle_path))
    video_rel = str(Path(video_path))
    output_rel = str(Path(output_path))
    
    # 检查文件是否存在
    if not Path(video_rel).exists():
        print(f"       ❌ 视频文件不存在：{video_rel}")
        return False
    if not Path(subtitle_rel).exists():
        print(f"       ❌ 字幕文件不存在：{subtitle_rel}")
        return False
    
    # FFmpeg 在 Windows 上需要正斜杠
    subtitle_ffmpeg = subtitle_rel.replace("\\", "/")
    video_ffmpeg = video_rel.replace("\\", "/")
    output_ffmpeg = output_rel.replace("\\", "/")
    
    # 生成样式字符串 - ASS 格式中的特殊字符需要转义
    style_str = style_to_ass_string(style)
    # 转义特殊字符：& 需要变成 \& 等
    style_str_escaped = style_str.replace("\\", "\\\\").replace(":", "\\:").replace(",", "\\,").replace("'", "\\'")
    
    # FFmpeg 命令（使用 ASS 滤镜方式）- 样式字符串需要用单引号包裹
    vf_filter = f"subtitles='{subtitle_ffmpeg}':force_style='{style_str_escaped}'"
    
    print(f"       样式：{style['font']} {style['fontsize']}px, 对齐={style['alignment']}")
    
    cmd = [
        "ffmpeg", "-i", video_ffmpeg,
        "-vf", vf_filter,
        "-c:a", "copy",
        "-y",
        output_ffmpeg
    ]
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            timeout=600
        )
        # FFmpeg 有时返回码非 0 但实际成功了，检查输出文件是否存在
        if Path(output_path).exists() and Path(output_path).stat().st_size > 0:
            file_size = Path(output_path).stat().st_size / 1024 / 1024
            print(f"       ✅ 视频已生成：{output_path} ({file_size:.2f} MB)")
            return True
        elif result.returncode == 0:
            file_size = Path(output_path).stat().st_size / 1024 / 1024
            print(f"       ✅ 视频已生成：{output_path} ({file_size:.2f} MB)")
            return True
        else:
            stderr = result.stderr.decode('utf-8', errors='ignore') if result.stderr else '未知错误'
            # 查找错误行
            error_lines = []
            for line in stderr.split('\n'):
                if 'Error' in line or 'error' in line or 'Invalid' in line:
                    error_lines.append(line.strip())
            print(f"       ❌ 合成失败：{' | '.join(error_lines[:2])}")
            return False
    except Exception as e:
        print(f"       ❌ 错误：{e}")
        return False


def regenerate_from_transcript(transcript_path: str, video_path: str, output_dir: str, style_config: str = None) -> bool:
    """
    从修改后的文字稿重新生成字幕和视频
    
    Args:
        transcript_path: 修改后的文字稿路径
        video_path: 原始视频路径
        output_dir: 输出目录
        style_config: 样式配置文件路径（可选）
    """
    print("="*60)
    print("字幕后处理器 - 从文字稿重新生成")
    print("="*60)
    print()
    
    # 检查文件
    if not Path(transcript_path).exists():
        print(f"[ERROR] 文字稿不存在：{transcript_path}")
        return False
    
    if not Path(video_path).exists():
        print(f"[ERROR] 视频不存在：{video_path}")
        return False
    
    # 创建输出目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"regenerated_{timestamp}"
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"[输出] 目录：{output_path}")
    print()
    
    # 1. 解析文字稿
    transcript_lines = parse_transcript(transcript_path)
    if not transcript_lines:
        print("[ERROR] 无法解析文字稿")
        return False
    
    # 2. 生成 SRT
    srt_path = output_path / "subtitles.srt"
    if not generate_srt(transcript_lines, str(srt_path)):
        return False
    
    # 3. 加载样式配置
    style = load_subtitle_style(style_config)
    
    # 4. 生成带字幕的视频
    video_output = output_path / "video_with_subtitles.mp4"
    if not add_subtitles_to_video(video_path, str(srt_path), str(video_output), style):
        return False
    
    # 5. 复制文字稿到输出目录
    import shutil
    transcript_output = output_path / "transcript_modified.txt"
    shutil.copy(transcript_path, transcript_output)
    
    print()
    print("="*60)
    print("生成完成！")
    print("="*60)
    print()
    print("输出文件:")
    print(f"  ✅ subtitles: {srt_path}")
    print(f"  ✅ video: {video_output}")
    print(f"  ✅ transcript: {transcript_output}")
    print()
    
    return True


def create_style_template(output_path: str):
    """创建样式配置模板"""
    style = DEFAULT_SUBTITLE_STYLE.copy()
    style["description"] = "字幕样式配置 - 修改后保存为 subtitle_style.json"
    style["examples"] = {
        "white_text": {"primary_color": "&H00FFFFFF"},
        "yellow_text": {"primary_color": "&H0000FFFF"},
        "top_center": {"alignment": 8},
        "bottom_center": {"alignment": 2},
        "with_background": {"border_style": 1, "outline": 3},
        "with_shadow": {"border_style": 4, "shadow": 2},
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(style, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 样式模板已创建：{output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="字幕后处理器")
    parser.add_argument("--transcript", "-t", help="修改后的文字稿路径")
    parser.add_argument("--video", "-v", help="原始视频路径")
    parser.add_argument("--output", "-o", default="./regenerated", help="输出目录")
    parser.add_argument("--style", "-s", help="样式配置文件路径")
    parser.add_argument("--create-style-template", action="store_true", help="创建样式模板")
    
    args = parser.parse_args()
    
    if args.create_style_template:
        create_style_template("subtitle_style_template.json")
        return
    
    if not args.transcript or not args.video:
        print("用法：subtitle_processor.py -t <文字稿> -v <视频> [-o 输出目录] [-s 样式配置]")
        print("      subtitle_processor.py --create-style-template")
        sys.exit(1)
    
    success = regenerate_from_transcript(args.transcript, args.video, args.output, args.style)
    
    if success:
        print("✅ 重新生成成功！")
    else:
        print("❌ 重新生成失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
