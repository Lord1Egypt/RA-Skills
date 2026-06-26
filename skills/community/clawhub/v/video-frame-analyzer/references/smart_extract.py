# -*- coding: utf-8 -*-
# @Author   : AI漫剧花大叔 (AI Drama Uncle Hua)
# @Copyright: © 2026 AI漫剧花大叔。保留所有权利。
# @GitHub   : https://github.com/shijin-ai
# @License  : MIT-0
# @Desc     : 智能关键帧提取器 - 按场景变化自动选帧

#!/usr/bin/env python3
"""
智能关键帧提取器 - 按场景变化自动选帧，非固定间隔
适用于：AI漫剧/短剧视频分析，提取最具叙事价值的帧

依赖：pip install opencv-python
"""

import cv2
import os
import sys

def extract_smart_frames(video_path, output_dir, max_frames=15, scene_threshold=25.0):
    """
    智能提取关键帧：基于场景变化检测 + 时间均匀采样

    参数:
        video_path: 视频文件路径
        output_dir: 输出目录
        max_frames: 最大提取帧数（默认15，覆盖单集短剧完整剧情）
        scene_threshold: 场景变化阈值（0-100，越大越严格）
    返回:
        提取的帧文件列表
    """
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0

    print(f"视频信息: {total_frames}帧, {fps:.2f}fps, 时长{duration:.1f}秒")

    # 策略1: 场景变化检测（核心）
    scene_changes = []
    prev_frame = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if prev_frame is not None:
            # 计算帧间差异（简化版直方图对比）
            diff = cv2.absdiff(prev_frame, frame)
            mean_diff = diff.mean()

            if mean_diff > scene_threshold:
                scene_changes.append(frame_idx)
                print(f"  场景变化 @ 帧{frame_idx} ({frame_idx/fps:.1f}s)")

        prev_frame = frame.copy()
        frame_idx += 1

    cap.release()

    # 策略2: 时间均匀采样（保底，确保覆盖全片）
    time_samples = []
    if duration > 0:
        segments = 5  # 分成5段
        for i in range(segments):
            t = duration * (i + 0.5) / segments
            time_samples.append(int(t * fps))

    # 策略3: 合并去重，按优先级排序
    selected = set()

    # 先加入场景变化帧
    for idx in scene_changes:
        selected.add(idx)

    # 补充时间采样帧
    for idx in time_samples:
        # 避免太接近已有帧
        if all(abs(idx - s) > fps * 2 for s in selected):  # 至少间隔2秒
            selected.add(idx)

    # 如果还不够，均匀补充
    if len(selected) < max_frames:
        step = total_frames // max_frames
        for i in range(max_frames):
            idx = i * step
            if all(abs(idx - s) > fps * 1.5 for s in selected):
                selected.add(idx)

    # 排序并截断
    selected = sorted(selected)[:max_frames]

    # 提取帧
    cap = cv2.VideoCapture(video_path)
    extracted = []

    for i, frame_idx in enumerate(selected):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            timestamp = frame_idx / fps
            filename = f"smart_{i:04d}_t{int(timestamp):04d}s.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            extracted.append({
                'file': filepath,
                'frame': frame_idx,
                'time': timestamp,
                'is_scene_change': frame_idx in scene_changes
            })
            print(f"  ✓ 提取: {filename} @ {timestamp:.1f}s")

    cap.release()

    print(f"\n完成: 提取{len(extracted)}帧 -> {output_dir}")
    return extracted


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python smart_extract.py <视频路径> [输出目录] [最大帧数]")
        print("示例: python smart_extract.py video.mp4 frames/ 15")
        sys.exit(1)

    video = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "smart_frames"
    max_f = int(sys.argv[3]) if len(sys.argv) > 3 else 15

    extract_smart_frames(video, out_dir, max_f)
