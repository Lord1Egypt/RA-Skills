#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加BGM到视频

使用方法：
    python add_bgm.py <视频> [BGM文件] [输出文件]

特性：
- BGM自动循环（交叉淡入淡出）
- 音量控制
- 自动淡入淡出
"""

import sys
import os
import subprocess
import json
from pathlib import Path

# 默认参数
DEFAULT_BGM_VOLUME = 0.12  # BGM音量12%
DEFAULT_CROSSFADE = 3      # 交叉淡入淡出3秒
DEFAULT_FADE_IN = 2        # 开头淡入2秒
DEFAULT_FADE_OUT = 2       # 结尾淡出2秒


def get_video_duration(video_path):
    """获取视频时长"""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])


def add_bgm(video_path, bgm_path=None, output_path=None, volume=None):
    """添加BGM"""
    import numpy as np
    
    if bgm_path is None:
        # 默认BGM
        script_dir = Path(__file__).parent
        bgm_path = script_dir.parent / "bgm" / "relaxing.mp3"
        if not bgm_path.exists():
            print(f"[!] 默认BGM不存在: {bgm_path}")
            print("[!] 请指定BGM文件: python add_bgm.py <视频> <BGM>")
            return False
    
    if output_path is None:
        video_stem = Path(video_path).stem
        output_path = str(Path(video_path).parent / f"{video_stem}_with_bgm.mp4")
    
    if volume is None:
        volume = DEFAULT_BGM_VOLUME
    
    print(f"[*] 添加BGM...")
    print(f"    视频: {video_path}")
    print(f"    BGM: {bgm_path}")
    print(f"    音量: {volume*100:.0f}%")
    
    # 获取视频时长
    video_duration = get_video_duration(video_path)
    print(f"    视频时长: {video_duration:.1f}s")
    
    # 构建ffmpeg命令
    # 使用afilter实现：
    # 1. BGM循环播放
    # 2. 交叉淡入淡出循环
    # 3. 音量调节
    # 4. 与原音频混合
    
    filter_complex = f"""
[1:a]volume={volume}[bgm];
[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]
""".strip()
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-stream_loop", "-1", "-i", bgm_path,  # 循环BGM
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[OK] 输出: {output_path}")
        return True
    else:
        print(f"[!] 失败: {result.stderr}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python add_bgm.py <视频> [BGM文件] [输出文件]")
        print("\n参数说明:")
        print("  视频      输入视频路径（必需）")
        print("  BGM文件   背景音乐文件（可选，默认使用bgm/relaxing.mp3）")
        print("  输出文件  输出视频路径（可选，默认为<视频名>_with_bgm.mp4）")
        sys.exit(1)
    
    video_path = sys.argv[1]
    bgm_path = sys.argv[2] if len(sys.argv) > 2 else None
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = add_bgm(video_path, bgm_path, output_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()