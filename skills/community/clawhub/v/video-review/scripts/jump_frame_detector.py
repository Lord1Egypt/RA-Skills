#!/usr/bin/env python3
"""
jump_frame_detector.py
视频初审 - 逐帧跳帧检测

对视频逐帧提取，与上一帧/下一帧分别做像素级相似度对比：
- 当前帧与上一帧 AND 下一帧的相似度都低于阈值 → 判定为跳帧
- 当前帧与上一帧 OR 下一帧的相似度 ≥ 阈值 → 无跳帧

用法：
  python3 jump_frame_detector.py -i /path/to/video.mp4
  python3 jump_frame_detector.py -i /path/to/video.mp4 --threshold 0.90
  python3 jump_frame_detector.py -i /path/to/video.mp4 --resize 128 --show-frames 10
"""

import argparse
import os
import subprocess
import sys
import tempfile
import json
from pathlib import Path
from PIL import Image
import numpy as np

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FPROBE = "/opt/homebrew/bin/ffprobe"


def run(cmd, timeout=600):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def get_video_info(mp4):
    """获取视频帧率、时长、总帧数"""
    ret, out, _ = run([
        FPROBE, "-v", "quiet", "-show_streams", "-select_streams", "v:0", mp4
    ])
    fps = 30.0
    if "r_frame_rate" in out:
        m = re.search(r"r_frame_rate=(\d+)/(\d+)", out)
        if m:
            fps = int(m.group(1)) / int(m.group(2))
    # 总帧数
    ret2, out2, _ = run([
        FPROBE, "-v", "quiet", "-select_streams", "v:0",
        "-count_packets", "-show_entries", "stream=nb_read_packets",
        "-of", "csv=p=0", mp4
    ])
    total_frames = int(out2.strip()) if out2.strip().isdigit() else None
    # 时长
    ret3, out3, _ = run([
        FPROBE, "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", mp4
    ])
    duration = float(out3.strip()) if out3.strip() else None
    return fps, duration, total_frames


import re


def extract_frames(mp4, output_dir, resize=128, max_frames=None):
    """提取所有帧（缩放到指定尺寸加速比较）"""
    os.makedirs(output_dir, exist_ok=True)

    fps, duration, total_frames = get_video_info(mp4)
    print(f"  📊 信息: {fps:.2f}fps, {duration:.1f}s, {total_frames}帧")

    limit_str = f",select=lt(n\\,{max_frames})" if max_frames else ""

    cmd = [
        FFMPEG, "-y", "-i", mp4,
        "-vf", f"scale=128:-1:flags=fast_bilinear{limit_str}",
        "-q:v", "5",
        "-vsync", "0",
        os.path.join(output_dir, "frame_%06d.jpg")
    ]
    ret, stdout, stderr = run(cmd, timeout=600)
    if ret != 0:
        print(f"  ❌ 帧提取失败: {stderr[-300:]}")
        return None, None, None

    frames = sorted(Path(output_dir).glob("frame_*.jpg"))
    print(f"  📸 提取到 {len(frames)} 帧 (缩放至 {resize}px)")
    return frames, fps, total_frames


def compute_similarity(img1_path, img2_path):
    """计算两张图的像素级相似度（归一化，绝对差值）"""
    try:
        img1 = Image.open(img1_path).convert("RGB")
        img2 = Image.open(img2_path).convert("RGB")

        # 缩小到更小尺寸加速
        small_size = (64, 64)
        img1_small = img1.resize(small_size, Image.BILINEAR)
        img2_small = img2.resize(small_size, Image.BILINEAR)

        arr1 = np.array(img1_small, dtype=np.float32)
        arr2 = np.array(img2_small, dtype=np.float32)

        # 归一化像素差异
        diff = np.abs(arr1 - arr2).mean()
        max_diff = 255.0
        similarity = 1.0 - (diff / max_diff)
        return float(similarity)
    except Exception as e:
        return None


def detect_jump_frames(frames_dir, threshold=0.80, output_json=None):
    """逐帧检测跳帧：当前帧与上一帧OR下一帧相似度 > threshold → 无跳帧"""
    frames = sorted(Path(frames_dir).glob("frame_*.jpg"))
    if len(frames) < 3:
        print(f"  ⚠️  帧数不足（{len(frames)}帧），无法做跳帧检测")
        return [], {}, threshold

    jump_frames = []
    details = []

    print(f"\n  🔍 逐帧检测中（共 {len(frames)} 帧，阈值 {threshold*100:.0f}%）...")

    for i, frame_path in enumerate(frames):
        # 跳过第一帧（没有上一帧）和最后一帧（没有下一帧）
        if i == 0 or i == len(frames) - 1:
            continue

        prev_frame = frames[i - 1]
        next_frame = frames[i + 1]

        sim_prev = compute_similarity(prev_frame, frame_path)
        sim_next = compute_similarity(next_frame, frame_path)

        if sim_prev is None or sim_next is None:
            continue

        # 逻辑：当前帧与上一帧 AND 下一帧相似度都 < threshold → 跳帧
        #       否则 → 无跳帧
        has_jump = sim_prev < threshold and sim_next < threshold

        frame_num = int(frame_path.stem.split("_")[1])

        if has_jump:
            jump_frames.append({
                "frame": frame_num,
                "sim_prev": round(sim_prev, 4),
                "sim_next": round(sim_next, 4),
                "sim_prev_pct": f"{sim_prev*100:.1f}%",
                "sim_next_pct": f"{sim_next*100:.1f}%"
            })

        details.append({
            "frame": frame_num,
            "sim_prev": round(sim_prev, 4),
            "sim_next": round(sim_next, 4),
            "has_jump": has_jump
        })

        # 进度提示
        if i % 500 == 0 and i > 0:
            print(f"    已检测 {i}/{len(frames)-2} 帧 ...", end="\r")

    print(f"    已检测 {len(frames)-2}/{len(frames)-2} 帧 ✓")

    result = {
        "threshold": threshold,
        "total_frames_checked": len(frames) - 2,
        "jump_frame_count": len(jump_frames),
        "jump_frames": jump_frames,
        "details": details
    }

    if output_json:
        with open(output_json, "w") as f:
            json.dump(result, f, indent=2)
        print(f"  📄 详细结果已保存: {output_json}")

    return jump_frames, result, threshold


def format_report(video_name, fps, jump_frames, result, threshold):
    """格式化输出报告"""
    total = result["total_frames_checked"]
    jump_count = len(jump_frames)
    ratio = jump_count / total if total > 0 else 0

    print(f"\n{'='*50}")
    print(f"📋 逐帧跳帧检测报告: {video_name}")
    print(f"{'='*50}")
    print(f"  🎬 帧率: {fps:.2f}fps | 检测帧数: {total}")
    print(f"  📊 相似度阈值: {threshold*100:.0f}%")
    print(f"  🖼️  跳帧数量: {jump_count}")

    if jump_count == 0:
        print(f"  ✅ 结论: 未检测到跳帧（与上一帧或下一帧相似度均正常）")
    else:
        print(f"  ❌ 结论: 检测到 {jump_count} 处跳帧")
        print(f"\n  跳帧帧号（相似度详情）:")
        for jf in jump_frames[:30]:
            print(f"    帧{jf['frame']:>6}: 与上一帧={jf['sim_prev_pct']}, 与下一帧={jf['sim_next_pct']}")
        if jump_count > 30:
            print(f"    ...还有 {jump_count - 30} 处")
        print(f"\n  ⚠️  跳帧比例: {ratio*100:.2f}% (>{5*threshold:.0f}% 需关注)")

    print(f"{'='*50}")
    return jump_count == 0, jump_count, ratio


def main():
    p = argparse.ArgumentParser(
        description="视频逐帧跳帧检测：当前帧与上一帧OR下一帧相似度 >80% → 无跳帧"
    )
    p.add_argument("-i", "--input", required=True, help="输入视频路径")
    p.add_argument("--threshold", type=float, default=0.90,
                   help="相似度阈值 (默认 0.90)")
    p.add_argument("--resize", type=int, default=128,
                   help="帧缩放尺寸，用于加速比较 (默认 128)")
    p.add_argument("--max-frames", type=int, default=None,
                   help="最多检测帧数（默认全部）")
    p.add_argument("--output-json", default=None,
                   help="输出详细JSON报告路径")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)

    video_name = os.path.basename(args.input)
    print(f"\n🎬 开始逐帧跳帧检测: {video_name}")
    print(f"  相似度阈值: {args.threshold*100:.0f}%")
    print(f"  缩放尺寸: {args.resize}px")

    # 临时目录
    with tempfile.TemporaryDirectory(prefix="jump_frame_") as tmp_dir:
        frames_dir = os.path.join(tmp_dir, "frames")
        os.makedirs(frames_dir, exist_ok=True)

        # 提取帧
        print(f"\n📸 提取帧...")
        frames, fps, total_frames = extract_frames(
            args.input, frames_dir,
            resize=args.resize,
            max_frames=args.max_frames
        )
        if frames is None:
            sys.exit(1)

        # 检测跳帧
        output_json = args.output_json or os.path.join(
            os.path.dirname(args.input) or ".", f"{video_name}_jump_frames.json"
        )
        jump_frames, result, threshold = detect_jump_frames(
            frames_dir, threshold=args.threshold, output_json=output_json
        )

        # 输出报告
        passed, jump_count, ratio = format_report(
            video_name, fps, jump_frames, result, threshold
        )

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()