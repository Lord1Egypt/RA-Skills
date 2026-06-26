# -*- coding: utf-8 -*-
# @Author   : AI漫剧花大叔 (AI Drama Uncle Hua)
# @Copyright: © 2026 AI漫剧花大叔。保留所有权利。
# @GitHub   : https://github.com/shijin-ai
# @License  : MIT-0
# @Desc     : 保底帧提取器 - 固定间隔提取（当 smart_extract.py 不可用时）

import os
import sys
try:
    # moviepy 2.x API
    from moviepy import VideoFileClip
except ImportError:
    # moviepy 1.x API
    from moviepy.editor import VideoFileClip
from PIL import Image

def extract_frames(video_path, output_dir, interval=3):
    """
    从视频中按固定间隔提取帧（保底方案，当 smart_extract.py 不可用時使用）

    参数:
        video_path: 视频文件路径
        output_dir: 输出目录
        interval: 提取间隔（秒），默认3秒一帧（高频采样）
    """
    print(f"正在加载视频: {video_path}")

    try:
        clip = VideoFileClip(video_path)
    except Exception as e:
        print(f"加载视频失败: {e}")
        return

    duration = clip.duration
    print(f"视频时长: {duration:.2f} 秒 ({duration/60:.2f} 分钟)")

    os.makedirs(output_dir, exist_ok=True)

    frame_count = 0
    for t in range(0, int(duration), interval):
        try:
            frame = clip.get_frame(t)
            img = Image.fromarray(frame)
            output_path = os.path.join(output_dir, f"frame_{frame_count:04d}_t{t:04d}s.jpg")
            img.save(output_path, "JPEG", quality=85)
            print(f"已保存: {output_path}")
            frame_count += 1
        except Exception as e:
            print(f"提取 {t}秒 帧失败: {e}")

    # 也提取最后一帧
    try:
        frame = clip.get_frame(duration - 1)
        img = Image.fromarray(frame)
        output_path = os.path.join(output_dir, f"frame_{frame_count:04d}_end.jpg")
        img.save(output_path, "JPEG", quality=85)
        print(f"已保存结尾帧: {output_path}")
        frame_count += 1
    except Exception as e:
        print(f"提取结尾帧失败: {e}")

    clip.close()
    print(f"\n总共提取了 {frame_count} 帧到 {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_frames.py <视频路径> [输出目录] [间隔秒数]")
        print("示例: python extract_frames.py video.mp4 frames/ 3")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "video_frames"
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    extract_frames(video_path, output_dir, interval)
