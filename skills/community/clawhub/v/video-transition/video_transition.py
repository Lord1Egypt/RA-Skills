# -*- coding: utf-8 -*-
"""
Video Transition Module
视频转场效果工具

使用 ffmpeg xfade 滤镜实现多种转场效果
"""

import subprocess
import os
import json
from typing import List, Optional, Tuple
from pathlib import Path


# 支持的转场效果
TRANSITIONS = {
    "fade": "淡入淡出",
    "slideleft": "左滑",
    "slideright": "右滑",
    "slideup": "上滑",
    "slidedown": "下滑",
    "circleopen": "圆形展开",
    "circleclose": "圆形关闭",
    "wipeleft": "左擦除",
    "wiperight": "右擦除",
    "wipeup": "上擦除",
    "wipedown": "下擦除",
    "distance": "距离渐变",
    "pixelize": "像素化",
    "diagtl": "左上对角线",
    "diagtr": "右上对角线",
    "diagbl": "左下对角线",
    "diagbr": "右下对角线",
    "hlslice": "水平切片",
    "vrslice": "垂直切片",
    "dissolve": "溶解",
    "radial": "径向",
    "smoothleft": "平滑左滑",
    "smoothright": "平滑右滑",
    "smoothup": "平滑上滑",
    "smoothdown": "平滑下滑",
    "rectcrop": "矩形裁剪",
    "circlecrop": "圆形裁剪",
}


def get_video_duration(video_path: str) -> float:
    """获取视频时长"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        raise ValueError(f"无法获取视频时长: {video_path}")


def get_video_info(video_path: str) -> dict:
    """获取视频详细信息"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=width,height,r_frame_rate,codec_name",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def add_fade_to_video(
    video_path: str,
    output_path: str,
    fade_in: float = 0.3,
    fade_out: float = 0.3
) -> str:
    """
    为视频添加淡入淡出效果
    
    Args:
        video_path: 输入视频路径
        output_path: 输出视频路径
        fade_in: 淡入时长（秒）
        fade_out: 淡出时长（秒）
    
    Returns:
        输出视频路径
    """
    duration = get_video_duration(video_path)
    
    vf = f"fade=t=in:st=0:d={fade_in},fade=t=out:st={duration-fade_out}:d={fade_out}"
    af = f"afade=t=in:st=0:d={fade_in},afade=t=out:st={duration-fade_out}:d={fade_out}"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True, encoding='utf-8', errors='replace')
    return output_path


def apply_transition(
    video1: str,
    video2: str,
    output: str,
    transition: str = "fade",
    duration: float = 0.5,
    offset: Optional[float] = None
) -> str:
    """
    在两个视频之间应用转场效果
    
    Args:
        video1: 第一个视频路径
        video2: 第二个视频路径
        output: 输出视频路径
        transition: 转场类型（fade, slideleft, slideright 等）
        duration: 转场时长（秒）
        offset: 转场起始时间（秒），默认为 video1 结束前 duration 秒
    
    Returns:
        输出视频路径
    """
    duration1 = get_video_duration(video1)
    
    if offset is None:
        offset = duration1 - duration
    
    if transition not in TRANSITIONS:
        print(f"警告: 未知转场类型 '{transition}'，使用 'fade'")
        transition = "fade"
    
    filter_complex = f"""
[0:v][1:v]xfade=transition={transition}:duration={duration}:offset={offset}[outv];
[0:a][1:a]acrossfade=d={duration}[outa]
"""
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video1,
        "-i", video2,
        "-filter_complex", filter_complex.strip(),
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264", "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        output
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    
    if result.returncode != 0:
        raise RuntimeError(f"转场失败: {result.stderr}")
    
    return output


def concat_with_transitions(
    video_paths: List[str],
    output_path: str,
    transition_duration: float = 0.5,
    transitions: Optional[List[str]] = None,
    auto_fade: bool = True,
    fade_in: float = 0.3,
    fade_out: float = 0.3
) -> str:
    """
    合并多个视频并添加转场效果
    
    Args:
        video_paths: 视频路径列表
        output_path: 输出视频路径
        transition_duration: 转场时长（秒）
        transitions: 转场类型列表，默认循环使用所有类型
        auto_fade: 是否自动为每个片段添加淡入淡出
        fade_in: 淡入时长（秒）
        fade_out: 淡出时长（秒）
    
    Returns:
        输出视频路径
    """
    if len(video_paths) < 2:
        raise ValueError("至少需要 2 个视频片段")
    
    # 获取所有视频时长
    durations = [get_video_duration(v) for v in video_paths]
    
    # 默认转场类型列表
    if transitions is None:
        transitions = ["fade", "slideleft", "slideright", "slideup", "slidedown",
                      "circleopen", "wipeleft", "wiperight"]
    
    # 构建 xfade 滤镜链
    filter_parts = []
    
    # 计算每个转场的 offset
    # offset = 前面所有视频时长之和 - 前面转场数量 * 转场时长
    offsets = []
    cumulative = 0
    for i in range(len(video_paths) - 1):
        cumulative += durations[i]
        offset = cumulative - (i + 1) * transition_duration
        offsets.append(offset)
    
    # 第一个转场
    trans0 = transitions[0 % len(transitions)]
    filter_parts.append(
        f"[0:v][1:v]xfade=transition={trans0}:duration={transition_duration}:offset={offsets[0]}[v01];"
        f"[0:a][1:a]acrossfade=d={transition_duration}[a01]"
    )
    
    # 后续转场
    for i in range(2, len(video_paths)):
        prev_v = f"v0{i-1}" if i > 2 else "v01"
        prev_a = f"a0{i-1}" if i > 2 else "a01"
        curr_v = f"v0{i}"
        curr_a = f"a0{i}"
        trans = transitions[i % len(transitions)]
        
        filter_parts.append(
            f"[{prev_v}][{i}:v]xfade=transition={trans}:duration={transition_duration}:offset={offsets[i-1]}[{curr_v}];"
            f"[{prev_a}][{i}:a]acrossfade=d={transition_duration}[{curr_a}]"
        )
    
    final_v = f"v0{len(video_paths)-1}" if len(video_paths) > 2 else "v01"
    final_a = f"a0{len(video_paths)-1}" if len(video_paths) > 2 else "a01"
    
    filter_complex = ";".join(filter_parts)
    
    # 构建 ffmpeg 命令
    inputs = []
    for path in video_paths:
        inputs.extend(["-i", path])
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", f"[{final_v}]",
        "-map", f"[{final_a}]",
        "-c:v", "libx264", "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    print(f"合并 {len(video_paths)} 个视频片段...")
    print(f"转场时长: {transition_duration}s")
    print(f"转场效果: {len(set(transitions[:len(video_paths)-1]))} 种")
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    
    if result.returncode != 0:
        print(f"xfade 失败: {result.stderr[:500]}")
        # 备用方案：简单 concat
        print("使用简单合并...")
        concat_simple(video_paths, output_path)
    
    return output_path


def concat_simple(video_paths: List[str], output_path: str) -> str:
    """简单合并视频（无转场）"""
    list_file = os.path.join(os.path.dirname(output_path), "video_list.txt")
    with open(list_file, 'w', encoding='utf-8') as f:
        for path in video_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264", "-c:a", "aac",
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True, encoding='utf-8', errors='replace')
    os.remove(list_file)
    return output_path


def add_fade_to_clips(
    input_dir: str,
    output_dir: str,
    fade_in: float = 0.3,
    fade_out: float = 0.3,
    extensions: Tuple[str, ...] = (".mp4", ".mov", ".avi", ".mkv")
) -> List[str]:
    """
    批量为视频片段添加淡入淡出
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        fade_in: 淡入时长（秒）
        fade_out: 淡出时长（秒）
        extensions: 支持的视频格式
    
    Returns:
        处理后的视频路径列表
    """
    os.makedirs(output_dir, exist_ok=True)
    output_paths = []
    
    for file in Path(input_dir).iterdir():
        if file.suffix.lower() in extensions:
            output_path = os.path.join(output_dir, file.name)
            print(f"处理: {file.name}")
            add_fade_to_video(str(file), output_path, fade_in, fade_out)
            output_paths.append(output_path)
    
    return output_paths


# 列出所有支持的转场效果
def list_transitions() -> dict:
    """列出所有支持的转场效果"""
    return TRANSITIONS.copy()


if __name__ == "__main__":
    print("支持的转场效果：")
    for name, desc in TRANSITIONS.items():
        print(f"  {name}: {desc}")
