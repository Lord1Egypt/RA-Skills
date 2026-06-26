#!/usr/bin/env python3
"""
Video Shot Analyzer v1.0
上传视频 → 镜头切分 → 运镜识别 → AI 提示词生成
"""

import cv2
import numpy as np
import os
import sys
import json
import base64
import time
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from datetime import timedelta

# ─── 运镜类型定义 ───
CAMERA_MOVEMENTS_ZH = {
    "push_in":     {"zh": "推镜头",  "en": "Slow push in"},
    "pull_out":    {"zh": "拉镜头",  "en": "Pull back"},
    "pan_left":    {"zh": "左摇",    "en": "Pan left"},
    "pan_right":   {"zh": "右摇",    "en": "Pan right"},
    "tilt_up":     {"zh": "上摇",    "en": "Tilt up"},
    "tilt_down":   {"zh": "下摇",    "en": "Tilt down"},
    "truck_left":  {"zh": "左移",    "en": "Truck left"},
    "truck_right": {"zh": "右移",    "en": "Truck right"},
    "zoom_in":     {"zh": "变焦推近","en": "Zoom in"},
    "zoom_out":    {"zh": "变焦拉远","en": "Zoom out"},
    "static":      {"zh": "固定镜头","en": "Static shot"},
    "handheld":    {"zh": "手持",    "en": "Handheld camera"},
    "orbit":       {"zh": "环绕",    "en": "Orbit / Arc shot"},
    "dolly_zoom":  {"zh": "希区柯克变焦","en": "Dolly zoom" },
    "crane_up":    {"zh": "升降上升","en": "Crane up / Pedestal up"},
    "crane_down":  {"zh": "升降下降","en": "Crane down / Pedestal down"},
}

SHOT_SIZES_ZH = {
    "extreme_close_up": {"zh": "特写",     "en": "Extreme close-up"},
    "close_up":         {"zh": "近景",     "en": "Close-up"},
    "medium":           {"zh": "中景",     "en": "Medium shot"},
    "wide":             {"zh": "全景",     "en": "Wide shot"},
    "extreme_wide":     {"zh": "远景",     "en": "Extreme wide shot"},
}


def timestamp_to_str(seconds):
    """秒 → HH:MM:SS"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 10)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms}"


def detect_scenes(video_path, threshold=30.0):
    """基于像素差异检测镜头切分点"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] 无法打开视频: {video_path}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    print(f"📹 视频信息: {total_frames} 帧, {fps:.2f} fps, 时长 {duration:.1f}s")

    cut_times = [0.0]  # 第一个镜头从 0 开始
    prev_hist = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % max(1, int(fps / 5)) == 0:  # 每秒采 5 帧
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (256, 256))
            hist = cv2.calcHist([gray], [0], None, [64], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()

            if prev_hist is not None:
                score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                if score < (1 - threshold / 100):
                    cut_times.append(frame_idx / fps)

            prev_hist = hist
        frame_idx += 1

    cap.release()

    # 添加结束时间点
    cut_times.append(duration)

    # 去重合并太近的切分点（<1秒）
    merged = [cut_times[0]]
    for t in cut_times[1:]:
        if t - merged[-1] > 1.0:
            merged.append(t)
    merged[-1] = duration  # 最后一个就是总时长

    print(f"✂️ 检测到 {len(merged) - 1} 个镜头")
    return merged, fps, duration, total_frames


def extract_keyframes(video_path, start, end, max_frames=5):
    """从镜头中提取关键帧用于后续分析"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    start_frame = int(start * fps)
    end_frame = int(end * fps)

    frames = []
    interval = max(1, (end_frame - start_frame) // (max_frames + 1))

    for i in range(max_frames):
        target = start_frame + interval * (i + 1)
        target = min(target, total_frames - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target)
        ret, frame = cap.read()
        if ret:
            frames.append((target / fps, frame))

    cap.release()
    return frames


def analyze_camera_motion(video_path, start, end):
    """使用光流法分析镜头内的相机运动"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    start_frame = max(0, int(start * fps) - 1)
    end_frame = int(end * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return {"movement": "static", "confidence": 0, "details": {}}

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # 累积统计数据
    total_dx = 0    # 水平平移
    total_dy = 0    # 垂直平移
    total_scale = 0 # 缩放
    jitter_count = 0
    frame_count = 0
    direction_changes_x = 0
    direction_changes_y = 0
    prev_dx = 0
    prev_dy = 0

    # 采样帧（跳过一些帧提高速度）
    skip = max(1, int(fps / 10))
    sample_count = 0
    max_samples = 50

    while True:
        for _ in range(skip):
            ret = cap.grab()
            if not ret:
                break

        ret, curr_frame = cap.retrieve()
        if not ret:
            break

        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        # 使用稀疏光流 (Farneback 密集光流太重，用 Good Features + calcOpticalFlowPyrLK)
        prev_pts = cv2.goodFeaturesToTrack(
            prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=10, blockSize=5
        )

        if prev_pts is not None and len(prev_pts) >= 8:
            curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)

            if curr_pts is not None and status is not None:
                valid = status.flatten() == 1
                good_prev = prev_pts[valid]
                good_curr = curr_pts[valid]

                if len(good_prev) >= 4:
                    # 估计仿射变换
                    M, inliers = cv2.estimateAffinePartial2D(good_prev, good_curr)

                    if M is not None:
                        dx = M[0, 2]  # 平移 X
                        dy = M[1, 2]  # 平移 Y
                        scale_x = M[0, 0]
                        scale_y = M[1, 1]
                        rotation = np.arctan2(M[1, 0], M[0, 0])

                        avg_scale = (scale_x + scale_y) / 2

                        total_dx += dx
                        total_dy += dy
                        total_scale += (avg_scale - 1.0)
                        frame_count += 1

                        # 检测方向变化（手抖特征）
                        if np.sign(dx) != np.sign(prev_dx) and abs(dx) > 1:
                            direction_changes_x += 1
                        if np.sign(dy) != np.sign(prev_dy) and abs(dy) > 1:
                            direction_changes_y += 1
                        prev_dx = dx
                        prev_dy = dy

        prev_gray = curr_gray
        sample_count += 1
        if sample_count >= max_samples:
            break

    cap.release()

    if frame_count == 0:
        return {"movement": "static", "confidence": 0.5, "details": {}}

    # 平均运动
    avg_dx = total_dx / frame_count
    avg_dy = total_dy / frame_count
    avg_scale = total_scale / frame_count
    jitter_ratio = (direction_changes_x + direction_changes_y) / (frame_count * 2) if frame_count > 0 else 0

    # 累积运动量
    total_motion_x = abs(total_dx)
    total_motion_y = abs(total_dy)
    total_zoom = abs(total_scale * frame_count)

    # ─── 运镜分类 ───
    movement = "static"
    confidence = 0.0
    details = {}

    # 手持特征：高频方向变化
    is_handheld = jitter_ratio > 0.4 and (total_motion_x + total_motion_y) < 100

    if is_handheld:
        movement = "handheld"
        confidence = min(1.0, jitter_ratio * 1.5)
    elif total_zoom > 0.15 * frame_count:
        if avg_scale > 1:
            movement = "zoom_in"
            confidence = min(1.0, avg_scale * frame_count * 3)
        else:
            movement = "zoom_out"
            confidence = min(1.0, abs(avg_scale) * frame_count * 3)
    elif total_motion_x > 80 and total_motion_y < 40:
        if avg_dx > 0:
            movement = "truck_left"
            confidence = min(1.0, abs(avg_dx) / 10)
        else:
            movement = "truck_right"
            confidence = min(1.0, abs(avg_dx) / 10)
    elif total_motion_y > 80 and total_motion_x < 40:
        if avg_dy < 0:
            movement = "tilt_down"
            confidence = min(1.0, abs(avg_dy) / 10)
        else:
            movement = "tilt_up"
            confidence = min(1.0, abs(avg_dy) / 10)
    elif total_motion_x > 60 and total_motion_y > 60:
        # 对角线运动，可能是环绕
        movement = "orbit"
        confidence = 0.5
    elif total_motion_x > 30:
        if avg_dx < 0:
            movement = "push_in"
            confidence = min(1.0, abs(avg_dx) / 15)
        else:
            movement = "pull_out"
            confidence = min(1.0, abs(avg_dx) / 15)
    elif total_motion_y > 30:
        if avg_dy < 0:
            movement = "crane_up"
            confidence = min(1.0, abs(avg_dy) / 15)
        else:
            movement = "crane_down"
            confidence = min(1.0, abs(avg_dy) / 15)
    else:
        movement = "static"
        confidence = 0.7

    details = {
        "motion_x": round(total_dx, 2),
        "motion_y": round(total_dy, 2),
        "scale_change": round(avg_scale * 100, 2),
        "jitter": round(jitter_ratio, 3),
        "frames_analyzed": frame_count,
    }

    return {"movement": movement, "confidence": min(1.0, confidence), "details": details}


def frame_to_base64(frame):
    """将 OpenCV 帧编码为 base64 JPEG"""
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
    return base64.b64encode(buffer).decode('utf-8')


def save_thumbnails(video_path, shots, output_dir):
    """为每个镜头保存缩略图"""
    os.makedirs(output_dir, exist_ok=True)

    thumbnails = []
    for i, (start, end) in enumerate(zip(shots[:-1], shots[1:])):
        mid = (start + end) / 2
        cap = cv2.VideoCapture(video_path)
        frame_idx = int(mid * cap.get(cv2.CAP_PROP_FPS))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        cap.release()

        if ret:
            thumb_path = os.path.join(output_dir, f"shot_{i:03d}.jpg")
            resized = cv2.resize(frame, (480, 270))
            cv2.imwrite(thumb_path, resized)
            thumbnails.append(thumb_path)

    return thumbnails


def output_result(result_json_path):
    """输出格式化的中文结果"""
    with open(result_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("\n" + "=" * 60)
    print(f"🎬 运镜分析报告 - {data['filename']}")
    print(f"   时长: {data['duration']:.1f}s | 镜头数: {len(data['shots'])}")
    print("=" * 60)

    for i, shot in enumerate(data['shots']):
        mv = shot['movement']
        mv_info = CAMERA_MOVEMENTS_ZH.get(mv, CAMERA_MOVEMENTS_ZH['static'])
        
        print(f"\n── 📹 镜头 {i + 1} ──")
        print(f"   时间: {timestamp_to_str(shot['start'])} → {timestamp_to_str(shot['end'])}")
        print(f"   运镜: {mv_info['zh']} ({mv_info['en']})")
        print(f"   置信度: {shot['confidence']:.0%}")
        print(f"   AI 生成提示词:")
        print(f"   > {shot['ai_prompt']}")

        if shot.get('base64_thumbnail'):
            print(f"   📸 缩略图: [base64 JPEG, {len(shot['base64_thumbnail'])} bytes]")

    print("\n" + "=" * 60)


def analyze_video(video_path):
    """主分析流程"""
    video_path = str(video_path)
    if not os.path.exists(video_path):
        print(f"[ERROR] 文件不存在: {video_path}")
        sys.exit(1)

    filename = os.path.basename(video_path)
    base_name = Path(filename).stem
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", base_name)
    
    print(f"🔍 开始分析: {filename}")

    # 1. 镜头切分
    shots, fps, duration, total_frames = detect_scenes(video_path)

    # 2. 对每个镜头分析运镜
    shot_results = []
    thumbnails = []

    for i in range(len(shots) - 1):
        start = shots[i]
        end = shots[i + 1]
        shot_duration = end - start
        
        print(f"\n分析镜头 {i+1}/{len(shots)-1} ({timestamp_to_str(start)} → {timestamp_to_str(end)}, {shot_duration:.1f}s)...")

        # 运镜分析
        motion = analyze_camera_motion(video_path, start, end)
        movement = motion['movement']
        mv_info = CAMERA_MOVEMENTS_ZH.get(movement, CAMERA_MOVEMENTS_ZH['static'])
        
        # 提取关键帧（取第一帧作缩略图）
        keyframes = extract_keyframes(video_path, start, end, max_frames=3)

        # 缩略图
        thumb_b64 = None
        if keyframes:
            mid_idx = len(keyframes) // 2
            frame_ts, frame = keyframes[mid_idx]
            thumb_b64 = frame_to_base64(frame)

        # 生成 AI 提示词模板
        ai_prompt = f"{mv_info['en']}, {shot_duration:.0f} second clip"

        shot_result = {
            "index": i + 1,
            "start": round(start, 2),
            "end": round(end, 2),
            "duration": round(shot_duration, 2),
            "movement": movement,
            "movement_zh": mv_info["zh"],
            "movement_en": mv_info["en"],
            "confidence": motion['confidence'],
            "motion_details": motion['details'],
            "ai_prompt": ai_prompt,
            "base64_thumbnail": thumb_b64,
            "keyframes_count": len(keyframes),
        }
        shot_results.append(shot_result)

    # 3. 输出结果
    result = {
        "filename": filename,
        "duration": duration,
        "total_frames": total_frames,
        "fps": fps,
        "shot_count": len(shot_results),
        "shots": shot_results,
        "summary": {
            "movements": list(set(s['movement'] for s in shot_results)),
            "most_common": max(set(s['movement'] for s in shot_results), key=lambda m: sum(1 for s in shot_results if s['movement'] == m)) if shot_results else "static"
        }
    }

    # 保存 JSON
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "analysis.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 打印结果
    print("\n" + "=" * 60)
    print(f"🎬 运镜分析完成 - {filename}")
    print(f"   时长: {duration:.1f}s | 镜头数: {len(shot_results)}")
    print(f"   输出目录: {output_dir}")
    print("=" * 60)

    for shot in shot_results:
        print(f"\n── 📹 镜头 {shot['index']} ──")
        print(f"   时间: {timestamp_to_str(shot['start'])} → {timestamp_to_str(shot['end'])}")
        print(f"   运镜: {shot['movement_zh']} ({shot['movement_en']})")
        print(f"   置信度: {shot['confidence']:.0%}")
        print(f"   时长: {shot['duration']:.1f}s")
        print(f"   AI 提示词: {shot['ai_prompt']}")
        details = shot['motion_details']
        if details:
            print(f"   运动数据: X={details.get('motion_x', 0):+.0f}px, Y={details.get('motion_y', 0):+.0f}px, 缩放={details.get('scale_change', 0):+.2f}%, 抖动={details.get('jitter', 0):.1%}")

    return json_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: py analyzer.py <视频文件路径>")
        print("  支持: mp4, avi, mov, mkv, webm")
        sys.exit(1)

    video_path = sys.argv[1]
    json_path = analyze_video(video_path)
    print(f"\n✅ 分析结果已保存: {json_path}")
