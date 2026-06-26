#!/usr/bin/env python3
"""
视频初审 - 主脚本
用法: python3 video_audit.py <视频路径> [--output <报告路径>] [--frame-interval <秒数>]
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

# 违禁词库路径
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BANNED_WORDS_FILE = os.path.join(SKILL_DIR, "refs", "banned_words.json")


def load_banned_words():
    """加载违禁词库"""
    if os.path.exists(BANNED_WORDS_FILE):
        with open(BANNED_WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"dirty_words": [], "limit_words": [], "sensitive_nations": []}


def extract_frames(video_path, output_dir, interval=2):
    """场景感知抽帧 + 均匀覆盖兜底"""
    os.makedirs(output_dir, exist_ok=True)

    # 优先使用场景感知抽帧（只抽有变化的帧）
    try:
        from scene_aware_sampler import scene_aware_extract
        frames_with_ts = scene_aware_extract(
            video_path, output_dir,
            min_interval=1.0, max_frames=80
        )
        if frames_with_ts and len(frames_with_ts) >= 5:
            # 返回 [(timestamp_str, frame_path), ...]
            return frames_with_ts
        elif frames_with_ts:
            print(f"场景感知抽帧数量不足({len(frames_with_ts)})，降级为均匀抽帧", file=sys.stderr)
    except Exception as e:
        print(f"场景感知抽帧失败，降级为均匀抽帧: {e}", file=sys.stderr)

    # 兜底：均匀抽帧
    output_pattern = os.path.join(output_dir, "frame_%04d.png")
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        output_pattern,
        "-y"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"抽帧失败: {result.stderr}", file=sys.stderr)
        return None
    frames = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
    # 转换为统一格式
    return [(str(i * interval), os.path.join(output_dir, f)) for i, f in enumerate(frames)]


def get_video_info(video_path):
    """获取视频基本信息"""
    cmd = ["ffprobe", "-v", "error",
           "-show_entries", "format=duration,size",
           "-show_entries", "stream=width,height,codec_name,r_frame_rate",
           "-of", "json", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def detect_visual_issues(frames_with_ts, video_info):
    """调用 image 工具逐帧检测视觉问题
    frames_with_ts: [(timestamp_str, frame_path), ...]
    """
    issues = []
    sys.path.insert(0, os.path.join(SKILL_DIR))
    try:
        from visual_checker import check_frame
    except ImportError:
        def check_frame(frame_path, frame_num, timestamp):
            return []

    for i, (ts_str, frame_path) in enumerate(frames_with_ts):
        # timestamp 格式转为 MM:SS
        ts_sec = float(ts_str)
        timestamp = f"00:{int(ts_sec)//60:02d}:{int(ts_sec)%60:02d}"
        frame_file = os.path.basename(frame_path)

        try:
            result = check_frame(frame_path, i, timestamp)
            for iss in result:
                iss["frame_file"] = frame_file
            issues.extend(result)
        except Exception as e:
            print(f"检测帧 {frame_file} 时出错: {e}", file=sys.stderr)
        time.sleep(0.3)

    return issues


def detect_subtitle_issues(video_path):
    """字幕转录 + 违禁词检测"""
    issues = []
    banned = load_banned_words()

    # 1. 提取 WAV
    wav_path = video_path + ".wav"
    cmd_convert = [
        "ffmpeg", "-i", video_path,
        "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
        wav_path, "-y"
    ]
    r = subprocess.run(cmd_convert, capture_output=True, text=True)
    if r.returncode != 0:
        return [{"type": "error", "desc": f"WAV转换失败: {r.stderr[:100]}"}]

    # 2. 调用 haoone-cli 转录
    # haoone-cli 需要设置安装路径，这里用绝对路径
    haoone_cli = "/Users/suran/Documents/haoone/haoone-cli"
    if os.path.exists(haoone_cli):
        cmd_transcribe = [haoone_cli, "transcribe", wav_path]
        r = subprocess.run(cmd_transcribe, capture_output=True, text=True, timeout=300)
        transcript = r.stdout if r.returncode == 0 else ""
    else:
        transcript = ""

    # 3. 违禁词检测
    detected_words = {"dirty": [], "limit": [], "nation": []}
    for w in banned.get("dirty_words", []):
        if w in transcript:
            detected_words["dirty"].append(w)
    for w in banned.get("limit_words", []):
        if w in transcript:
            detected_words["limit"].append(w)
    for w in banned.get("sensitive_nations", []):
        if w in transcript:
            detected_words["nation"].append(w)

    for w in detected_words["dirty"]:
        issues.append({"type": "subtitle", "category": "脏话",
                       "word": w, "timestamp": "（见字幕）"})
    for w in detected_words["limit"]:
        issues.append({"type": "subtitle", "category": "极限词",
                       "word": w, "timestamp": "（见字幕）"})
    for w in detected_words["nation"]:
        issues.append({"type": "subtitle", "category": "敏感国家名",
                       "word": w, "timestamp": "（见字幕）"})

    # 清理临时 WAV
    if os.path.exists(wav_path):
        os.remove(wav_path)

    return issues


def generate_report(video_path, video_info, visual_issues, subtitle_issues, output_path):
    """生成检测报告"""
    passed = len([i for i in visual_issues + subtitle_issues if "严重" in i.get("severity", "")]) == 0

    lines = []
    lines.append("━━━ 视频初审检测报告 ━━━")
    lines.append(f"文件：{os.path.basename(video_path)}")
    if video_info:
        dur = video_info.get("format", {}).get("duration", "N/A")
        size = video_info.get("format", {}).get("size", "N/A")
        streams = video_info.get("streams", [])
        width = height = fps = "N/A"
        for s in streams:
            if s.get("codec_type") == "video":
                width = s.get("width", "N/A")
                height = s.get("height", "N/A")
                fps = s.get("r_frame_rate", "N/A")
        lines.append(f"时长：{float(dur):.1f}秒 | 分辨率：{width}x{height} | 帧率：{fps}")
    else:
        lines.append("时长：无法获取")

    lines.append(f"通过：{'✅ 是' if passed else '❌ 否'}")
    total = len(visual_issues) + len(subtitle_issues)
    lines.append(f"问题数量：{total}")
    lines.append("")

    if visual_issues:
        lines.append("━━━ 视觉问题 ━━━")
        for idx, iss in enumerate(visual_issues, 1):
            sev = iss.get("severity", "轻微")
            icon = "❌" if sev == "严重" else "⚠️"
            cat = iss.get("category", "其他")
            desc = iss.get("desc", "")
            loc = iss.get("location", "")
            suggestion = iss.get("suggestion", "请审查")
            lines.append(f"{idx}. {icon} [{cat}] {desc} - {loc}")
            lines.append(f"   严重程度：{sev}")
            lines.append(f"   建议：{suggestion}")
            lines.append("")
    else:
        lines.append("━━━ 视觉问题 ━━━")
        lines.append("  无明显视觉问题")
        lines.append("")

    if subtitle_issues:
        lines.append("━━━ 字幕/台词问题 ━━━")
        for idx, iss in enumerate(subtitle_issues, 1):
            cat = iss.get("category", "")
            word = iss.get("word", "")
            ts = iss.get("timestamp", "")
            lines.append(f"{idx}. ❌ [{cat}] \"{word}\" - {ts}")
            lines.append("")
    else:
        lines.append("━━━ 字幕/台词问题 ━━━")
        lines.append("  无违禁词检出")
        lines.append("")

    severe_count = len([i for i in visual_issues + subtitle_issues if i.get("severity") == "严重"])
    minor_count = len([i for i in visual_issues + subtitle_issues if i.get("severity") == "轻微"])

    lines.append("━━━ 总结 ━━━")
    lines.append(f"综合判定：{'✅ 通过' if passed else '❌ 不通过'}")
    lines.append(f"严重问题：{severe_count}（需处理）")
    lines.append(f"轻微问题：{minor_count}（建议处理）")

    report_text = "\n".join(lines)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"报告已保存：{output_path}")
    else:
        print(report_text)

    return passed


def main():
    parser = argparse.ArgumentParser(description="视频初审检测")
    parser.add_argument("video", help="视频文件路径")
    parser.add_argument("--output", "-o", help="输出报告路径", default="")
    parser.add_argument("--frame-interval", "-fi", type=int, default=2,
                        help="抽帧间隔（秒），默认2秒")
    args = parser.parse_args()

    video_path = args.video
    if not os.path.exists(video_path):
        print(f"错误：文件不存在: {video_path}", file=sys.stderr)
        sys.exit(1)

    # 准备临时目录
    temp_dir = os.path.join("/tmp", f"audit_{int(time.time())}")
    os.makedirs(temp_dir, exist_ok=True)
    frames_dir = os.path.join(temp_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"正在检测：{video_path}")

    # 1. 获取视频信息
    print("获取视频信息...")
    video_info = get_video_info(video_path)

    # 2. 抽帧（场景感知）
    print("正在抽帧（场景感知模式）...")
    frames = extract_frames(video_path, frames_dir, args.frame_interval)
    if not frames:
        print("抽帧失败", file=sys.stderr)
        sys.exit(1)
    print(f"抽到 {len(frames)} 帧")

    # 3. 视觉检测
    print("正在进行视觉检测（场景感知抽帧）...")
    visual_issues = detect_visual_issues(frames, video_info)

    # 4. 字幕检测
    print("正在进行字幕/台词检测...")
    subtitle_issues = detect_subtitle_issues(video_path)

    # 5. 生成报告
    print("正在生成报告...")
    passed = generate_report(video_path, video_info, visual_issues, subtitle_issues, args.output)

    # 清理临时文件
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()