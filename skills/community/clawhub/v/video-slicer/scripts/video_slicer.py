#!/usr/bin/env python3
"""
Video Slicer — 视频智能切片工具（一键版）
================================================

用法:
  python3 video_slicer.py <视频文件> [输出目录] [选项]

示例:
  # 基础用法（采样帧 + 短视频自动转写）
  python3 video_slicer.py ~/Downloads/演讲视频.mp4 ./output

  # 指定时间范围转写长视频中的一部分
  python3 video_slicer.py 长视频.mp4 ./output --start 00:40:00 --end 01:07:00

  # 仅采样关键帧，不做转写
  python3 video_slicer.py 视频.mp4 ./output --frames-only

工作流:
  Phase 1: 获取视频信息 → 均匀采样关键帧
  Phase 2: 提取目标音频 → Whisper 智能转写（中文+MPS加速）
  Phase 3: 输出结构化数据(JSON) → 供 Agent 规划切割方案
  Phase 4: （可选）执行 ffmpeg 批量切割

输出:
  output/
  ├── frames/           关键帧图片（jpg）
  ├── transcript/       转写结果（json + txt + aac）
  └── output/           切割后的短视频片段（mp4）

作者: Bill (米赋教育)
版本: 1.2.0 | 兼容模型: glm-5v-turbo / GPT-4o / Claude 3.5 Sonnet
"""

import os
import sys
import json
import subprocess
import ssl
import certifi
import shutil
import argparse
from datetime import timedelta


# ======================== 全局配置 ========================
DEFAULT_CONFIG = {
    "sample_interval": 300,      # 采样间隔(秒)，默认5分钟
    "min_clip": 180,             # 最短切片时长(秒) = 3分钟
    "max_clip": 480,             # 最长切片时长(秒) = 8分钟
    "whisper_model": "base",     # Whisper 模型: tiny/base/small/medium
    "crf": 18,                   # 视频质量 (0-51, 越小越好, 推荐17-23)
    "audio_bitrate": "128k",     # 音频码率
}


def time_to_seconds(time_str):
    """
    将时间字符串转换为秒数。
    支持格式: "HH:MM:SS", "MM:SS", 或纯数字(秒)

    参数:
        time_str (str): 时间字符串
    返回:
        int: 总秒数
    """
    if isinstance(time_str, (int, float)):
        return int(time_str)

    parts = str(time_str).strip().split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    else:
        return int(parts[0])


def seconds_to_hms(total_sec):
    """
    将秒数转换为 HH:MM:SS 格式。

    参数:
        total_sec (int/float): 总秒数
    返回:
        str: 格式化的时间字符串
    """
    total_sec = int(total_sec)
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


# ============================================================
#                    Phase 1: 视频信息 & 帧采样
# ============================================================

def get_video_info(video_path):
    """
    获取视频基本信息：时长、分辨率、编码格式等。

    参数:
        video_path (str): 视频文件绝对路径
    返回:
        dict: 包含 duration(秒), path, resolution, codec 的字典
    异常:
        Exception: 无法读取视频时抛出
    """
    import re

    result = subprocess.run(
        ["ffmpeg", "-i", video_path],
        capture_output=True, text=True
    )
    stderr = result.stderr

    # 解析时长
    dur_match = re.search(r'Duration:\s*(\d{2}):(\d{2}):(\d{2})', stderr)
    if not dur_match:
        raise Exception(f"无法从视频获取时长信息: {video_path}")

    h, m, s = map(int, dur_match.groups())
    duration_sec = h * 3600 + m * 60 + s

    # 解析视频流信息
    codec_match = re.search(r'Stream.*Video:\s*(\w+).*?(\d+x\d+)', stderr)
    resolution = codec_match.group(2) if codec_match else "未知"
    codec = codec_match.group(1) if codec_match else "未知"

    return {
        "duration": duration_sec,
        "path": os.path.abspath(video_path),
        "filename": os.path.basename(video_path),
        "resolution": resolution,
        "codec": codec,
        "duration_hms": seconds_to_hms(duration_sec),
        "size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 1),
    }


def sample_frames(video_path, out_dir, duration, interval=None):
    """
    在均匀时间间隔上采样视频关键帧。

    参数:
        video_path (str): 视频文件路径
        out_dir (str): 输出根目录
        duration (int): 视频总时长（秒）
        interval (int|None): 采样间隔（秒），默认使用配置值 300
    返回:
        dict: {"dir": 帧目录路径, "count": 采样帧数量, "files": 文件名列表}
    """
    interval = interval or DEFAULT_CONFIG["sample_interval"]
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    # 生成采样时间点列表
    times = list(range(0, int(duration) + 1, interval))
    if times and times[-1] != int(duration):
        times.append(int(duration))

    files = []
    for t in times:
        ts = seconds_to_hms(t)
        safe_ts = ts.replace(":", "_")  # 文件名安全格式
        out_path = os.path.join(frames_dir, f"frame_{safe_ts}.jpg")

        if not os.path.exists(out_path):
            proc = subprocess.run([
                "ffmpeg", "-y",
                "-ss", ts,
                "-i", video_path,
                "-frames:v", "1",
                "-q:v", "2",
                out_path
            ], capture_output=True, timeout=30)

            if proc.returncode != 0:
                continue  # 跳过失败的帧（通常是超出视频长度）

        files.append(f"frame_{safe_ts}.jpg")

    return {
        "dir": os.path.abspath(frames_dir),
        "count": len(files),
        "files": files,
    }


def sample_frames_fine(video_path, out_dir, start_sec, end_sec, interval=120):
    """
    在指定区间进行精细关键帧采样。

    参数:
        video_path (str): 视频文件路径
        out_dir (str): 输出目录
        start_sec (int): 区间起始（秒）
        end_sec (int): 区间结束（秒）
        interval (int): 采样间隔（秒），默认 120（2分钟）
    返回:
        dict: 同 sample_frames()
    """
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    files = []
    t = start_sec
    while t <= end_sec:
        ts = seconds_to_hms(t)
        safe_ts = ts.replace(":", "_")
        label = "fine"
        out_path = os.path.join(frames_dir, f"{label}_{safe_ts}.jpg")

        if not os.path.exists(out_path):
            subprocess.run([
                "ffmpeg", "-y",
                "-ss", ts,
                "-i", video_path,
                "-frames:v", "1",
                "-q:v", "2",
                out_path
            ], capture_output=True, timeout=30)

        files.append(f"{label}_{safe_ts}.jpg")
        t += interval

    return {"dir": os.path.abspath(frames_dir), "count": len(files), "files": files}


# ============================================================
#                 Phase 2: 音频提取 + Whisper 转写
# ============================================================

def transcribe_segment(video_path, out_dir, start_sec, end_sec,
                        model_name=None, initial_prompt=""):
    """
    从视频中提取指定区间的音频并执行 Whisper 转写。

    核心优化：先提取音频再转写，比直接喂视频快 ~10 倍。

    参数:
        video_path (str): 视频文件路径
        out_dir (str): 输出目录
        start_sec (int/float): 起始时间（秒）
        end_sec (int/float): 结束时间（秒）
        model_name (str|None): Whisper 模型名，默认 base
        initial_prompt (str): 领域关键词提示（提高准确率）
    返回:
        str|None: 成功返回 speech.json 的绝对路径，失败返回 None
    """
    model_name = model_name or DEFAULT_CONFIG["whisper_model"]

    try:
        import torch
        import whisper
        from opencc import OpenCC
    except ImportError as e:
        print(json.dumps({
            "status": "error",
            "error": f"缺少依赖库: {e}",
            "fix": "请运行: pip install openai-whisper opencc-python-reimplemented torch"
        }, ensure_ascii=False))
        return None

    # === macOS SSL 修复 ===
    ssl._create_default_https_context = lambda: ssl.create_default_context(
        cafile=certifi.where()
    )
    os.environ['SSL_CERT_FILE'] = certifi.where()

    # === 准备输出目录 ===
    transcript_dir = os.path.join(out_dir, "transcript")
    os.makedirs(transcript_dir, exist_ok=True)

    audio_path = os.path.join(transcript_dir, "segment.aac")
    ts_start = seconds_to_hms(start_sec)
    ts_end = seconds_to_hms(end_sec)
    duration = end_sec - start_sec

    # === Step 1: 提取音频 ===
    print(f"[1/3] 提取音频: {ts_start} ~ {ts_end} ({duration}秒)", file=sys.stderr)
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-ss", ts_start,
        "-to", ts_end,
        "-vn", "-acodec", "copy",
        audio_path
    ], capture_output=True, text=True)

    if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 10000:
        error_msg = result.stderr[-500:] if result.stderr else "未知错误"
        print(json.dumps({
            "status": "error",
            "error": f"音频提取失败或文件过小",
            "details": error_msg.strip()[:300]
        }, ensure_ascii=False), file=sys.stderr)
        return None

    audio_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"      音频大小: {audio_mb:.1f} MB", file=sys.stderr)

    # === Step 2: Whisper 转写 ===
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"[2/3] 加载模型 ({model_name}, device={device})...", file=sys.stderr)

    try:
        model = whisper.load_model(model_name, device=device)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": f"Whisper 模型加载失败: {e}"
        }, ensure_ascii=False), file=sys.stderr)
        return None

    print(f"[3/3] 转写中...", file=sys.stderr)
    try:
        whisper_result = model.transcribe(
            audio_path,
            language="zh",
            verbose=False,
            initial_prompt=initial_prompt,
            word_timestamps=False
        )
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": f"Whisper 转写过程出错: {e}"
        }, ensure_ascii=False), file=sys.stderr)
        return None

    # === Step 3: 后处理（繁简转换 + 时间戳校正）===
    cc = OpenCC('t2s')
    segments = []
    for seg in whisper_result["segments"]:
        text_clean = cc.convert(seg["text"].strip())
        if not text_clean:
            continue
        segments.append({
            "id": len(segments) + 1,
            "start": round(seg["start"] + start_sec, 1),
            "end": round(seg["end"] + start_sec, 1),
            "text": text_clean,
            "logprob": round(seg.get("avg_logprob", 0), 2),
        })

    # === 保存结果 ===
    json_path = os.path.join(transcript_dir, "speech.json")
    txt_path = os.path.join(transcript_dir, "speech.txt")

    output_data = {
        "meta": {
            "source_video": os.path.abspath(video_path),
            "audio_segment": f"{ts_start} ~ {ts_end}",
            "audio_duration_sec": round(duration, 1),
            "whisper_model": model_name,
            "device": device,
            "total_segments": len(segments),
            "generated_at": __import__("datetime").datetime.now().isoformat(),
        },
        "segments": segments,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        for seg in segments:
            sh, sm = divmod(int(seg["start"]), 60)
            eh, em = divmod(int(seg["end"]), 60)
            f.write(f"[{sh:02d}:{sm:02d} -> {eh:02d}:{em:02d}] {seg['text']}\n")

    # 输出结构化 JSON 结果到 stdout（供 Agent 解析）
    result_obj = {
        "status": "success",
        "json_path": os.path.abspath(json_path),
        "txt_path": os.path.abspath(txt_path),
        "audio_path": os.path.abspath(audio_path),
        "segment_count": len(segments),
        "duration_min": round((segments[-1]["end"] - segments[0]["end"]) / 60, 1) if segments else 0,
        "model": model_name,
        "device": device,
    }
    print(json.dumps(result_obj, ensure_ascii=False, indent=2))

    return json_path


# ============================================================
#                  Phase 4: 批量切割执行
# ============================================================

def cut_clips(video_path, out_dir, clips_plan, crf=None, audio_bitrate=None):
    """
    按 clips_plan 方案批量切割视频片段。

    参数:
        video_path (str): 源视频路径
        out_dir (str): 输出目录
        clips_plan (list[dict]): 切片计划列表，每项包含:
            - "start" (str): 起始时间 "HH:MM:SS"
            - "end" (str): 结束时间 "HH:MM:SS"
            - "title" (str): 切片标题（用于文件名）
        crf (int|None): 视频质量参数，默认使用配置值 18
        audio_bitrate (str|None): 音频码率，默认 "128k"
    返回:
        list[dict]: 切片结果列表 [{"file": path, "size_mb": float, "title": str}]
    """
    crf = crf or DEFAULT_CONFIG["crf"]
    audio_bitrate = audio_bitrate or DEFAULT_CONFIG["audio_bitrate"]

    output_dir = os.path.join(out_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    results = []
    total = len(clips_plan)

    for i, clip in enumerate(clips_plan, 1):
        start = clip.get("start")
        end = clip.get("end")
        title = clip.get("title", f"clip{i}")
        # 清理文件名中的非法字符
        safe_title = "".join(c for c in title if c.isalnum() or c in ("_", "-", " "))
        filename = f"clip{i}_{safe_title}.mp4"
        out_path = os.path.join(output_dir, filename)

        dur_sec = time_to_seconds(end) - time_to_seconds(start)
        print(f"[{i}/{total}] {title} ({start} -> {end}, ~{dur_sec // 60}min{dur_sec % 60}s)", file=sys.stderr)

        proc = subprocess.run([
            "ffmpeg", "-y",
            "-ss", start,
            "-to", end,
            "-i", video_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", str(crf),
            "-c:a", "aac",
            "-b:a", audio_bitrate,
            "-movflags", "+faststart",
            out_path
        ], capture_output=True, timeout=600)

        if proc.returncode == 0 and os.path.exists(out_path):
            size_mb = os.path.getsize(out_path) / (1024 * 1024)
            results.append({
                "file": os.path.abspath(out_path),
                "size_mb": round(size_mb, 1),
                "title": title,
                "status": "ok",
            })
            print(f"      OK: {filename} ({size_mb:.1f} MB)", file=sys.stderr)
        else:
            results.append({
                "file": out_path,
                "size_mb": 0,
                "title": title,
                "status": "failed",
                "error": (proc.stderr[-300:] if proc.stderr else "Unknown error").decode('utf-8', errors='replace') if isinstance(proc.stderr, bytes) else str(proc.stderr)[-300:] if proc.stderr else "Unknown error",
            })
            print(f"      FAIL: {filename}", file=sys.stderr)

    # 最终汇总输出（JSON）
    summary = {
        "status": "done",
        "total_clips": total,
        "succeeded": sum(1 for r in results if r["status"] == "ok"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "output_dir": os.path.abspath(output_dir),
        "clips": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"[完成] {summary['succeeded']}/{total} 个切片成功", file=sys.stderr)
    print(f"[目录] {summary['output_dir']}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    return results


# ============================================================
#                      CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Video Slicer — 视频智能切片工具 v1.2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 video_slicer.py 视频.mp4 ./output
  python3 video_slicer.py 视频.mp4 ./output --start 00:40 --end 01:07
  python3 video_slicer.py 视频.mp4 ./output --frames-only
  python3 video_slicer.py 视频.mp4 ./output --model small
        """,
    )

    parser.add_argument("video", help="源视频文件路径")
    parser.add_argument("outdir", nargs=".", default="./video_slicer_output",
                        help="输出目录（默认: ./video_slicer_output）")
    parser.add_argument("--start", type=str, default=None,
                        help="转写起始时间 (格式: HH:MM:SS 或 MM:SS)")
    parser.add_argument("--end", type=str, default=None,
                        help="转写结束时间 (格式: HH:MM:SS 或 MM:SS)")
    parser.add_argument("--model", type=str, default=None,
                        choices=["tiny", "base", "small", "medium"],
                        help=f'Whisper 模型 (默认: {DEFAULT_CONFIG["whisper_model"]})')
    parser.add_argument("--prompt", type=str, default="",
                        help="领域关键词提示（提高转写准确率）")
    parser.add_argument("--frames-only", action="store_true",
                        help="仅采样关键帧，跳过转写步骤")
    parser.add_argument("--interval", type=int, default=None,
                        help="帧采样间隔（秒，默认: 300）")
    parser.add_argument("--crf", type=int, default=None,
                        help=f'视频 CRF 质量 (默认: {DEFAULT_CONFIG["crf"]}, 范围 0-51)')
    parser.add_argument("--fine-start", type=int, default=None,
                        help="精细采样起始位置（秒）")
    parser.add_argument("--fine-end", type=int, default=None,
                        help="精细采样结束位置（秒）")

    args = parser.parse_args()

    video_path = os.path.expanduser(args.video)
    out_dir = args.outdir

    # ====== 验证输入 ======
    if not os.path.exists(video_path):
        print(json.dumps({"status": "error", "error": f"视频文件不存在: {video_path}"}))
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)

    # 应用命令行覆盖的配置
    if args.model:
        DEFAULT_CONFIG["whisper_model"] = args.model
    if args.crf is not None:
        DEFAULT_CONFIG["crf"] = args.crf

    print("=" * 55, file=sys.stderr)
    print("  Video Slicer v1.2.0 — 视频智能切片工具", file=sys.stderr)
    print("=" * 55, file=sys.stderr)

    # ====== Step 1: 获取视频信息 ======
    print(f"\n[Step 1] 分析视频...", file=sys.stderr)
    try:
        info = get_video_info(video_path)
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(1)

    print(f"  文件:   {info['filename']}", file=sys.stderr)
    print(f"  时长:   {info['duration_hms']} ({info['duration']}秒)", file=sys.stderr)
    print(f"  分辨率: {info['resolution']} | 编码: {info['codec']} | 大小: {info['size_mb']}MB", file=sys.stderr)

    # ====== Step 2: 采样关键帧 ======
    print(f"\n[Step 2] 采样关键帧 (每{args.interval or DEFAULT_CONFIG['sample_interval']}秒)...", file=sys.stderr)
    frame_result = sample_frames(video_path, out_dir, info["duration"], args.interval)
    print(f"  完成: {frame_result['count']} 帧 -> {frame_result['dir']}", file=sys.stderr)

    # 可选：精细采样
    if args.fine_start is not None and args.fine_end is not None:
        print(f"\n[Step 2b] 精细采样 ({args.fine_start}-{args.fine_end}秒)...", file=sys.stderr)
        fine_result = sample_frames_fine(
            video_path, out_dir, args.fine_start, args.fine_end
        )
        print(f"  完成: {fine_result['count']} 帧", file=sys.stderr)

    # ====== Step 3: 转写（除非仅采帧模式）=====
    if not args.frames_only:
        if args.start and args.end:
            # 用户指定了时间范围
            start_sec = time_to_seconds(args.start)
            end_sec = time_to_seconds(args.end)
            print(f"\n[Step 3] 转写目标段落: {args.start} ~ {args.end} ...", file=sys.stderr)
            transcribe_segment(
                video_path, out_dir, start_sec, end_sec,
                model_name=args.model,
                initial_prompt=args.prompt
            )
        elif info["duration"] <= 1800:
            # 短视频（<=30min）：自动全量转写
            print(f"\n[Step 3] 视频较短({info['duration']}s<1800s)，全量转写...", file=sys.stderr)
            transcribe_segment(
                video_path, out_dir, 0, info["duration"],
                model_name=args.model,
                initial_prompt=args.prompt
            )
        else:
            # 长视频（>30min）：提示用户手动指定
            print(f"""
{'='*55}
  视频较长 ({info['duration']//60}分{info['duration']%60}秒)，建议手动指定转写范围。

  帧目录: {frame_result['dir']}
  请查看关键帧后，运行:

  python3 {__file__} "{video_path}" "{out_dir}" \\
      --start HH:MM:SS --end HH:MM:SS \\
      --prompt "关键词提示"

  或在 Python 中调用:
  from video_slicer import transcribe_segment
  transcribe_segment("{video_path}", "{out_dir}", 2400, 4020)
{'='*55}
""", file=sys.stderr)

    # ====== 完成 ======
    print(f"\n[OK] 工作目录: {os.path.abspath(out_dir)}", file=sys.stderr)


if __name__ == "__main__":
    main()
