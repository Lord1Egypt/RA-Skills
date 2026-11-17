#!/usr/bin/env python3
"""
视频爆款拆解 pipeline（自动配置版）
首次运行自动建 venv + 装依赖 + 提供 ffmpeg，用户装完 skill 直接跑。
"""

import argparse
import json
import os
import re
import site
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = SKILL_DIR / ".venv"


def is_venv():
    return hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)


def in_target_venv():
    return VENV_DIR.exists() and Path(sys.executable).resolve().startswith(VENV_DIR.resolve())


def run(cmd):
    print("[run] " + " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def ensure_env():
    """首次运行时自动建 venv 并装依赖。装好后重启脚本走 venv 的 python。"""
    if in_target_venv():
        return

    print("=" * 50)
    print("[setup] 首次运行，自动配置环境（约 2-5 分钟，仅一次）")
    print("=" * 50)

    # 用当前 python 建 venv
    if not VENV_DIR.exists():
        print("[setup] 创建隔离 venv: {}".format(VENV_DIR))
        r = run([sys.executable, "-m", "venv", str(VENV_DIR)])
        if r.returncode != 0:
            print("[error] 建 venv 失败:")
            print(r.stderr[-500:] if r.stderr else "")
            sys.exit(1)

    venv_python = VENV_DIR / ("Scripts" / "python.exe" if os.name == "nt" else "bin" / "python")
    venv_pip = str(venv_python) + " -m pip"

    # 升级 pip
    print("[setup] 升级 pip ...")
    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip",
         "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])

    # 装依赖（用清华源加速）
    req_file = SKILL_DIR / "requirements.txt"
    print("[setup] 安装依赖（清华源）...")
    r = run([str(venv_python), "-m", "pip", "install", "-r", str(req_file),
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
    if r.returncode != 0:
        print("[error] 装依赖失败:")
        print(r.stderr[-1500:] if r.stderr else "")
        print("")
        print("[hint] 可手动执行:")
        print('  "{}" -m pip install -r "{}" -i https://pypi.tuna.tsinghua.edu.cn/simple'.format(
            venv_python, req_file))
        sys.exit(1)

    print("[setup] 环境就绪，重新启动 pipeline ...")
    print("=" * 50)
    # 用 venv 的 python 重启自己，带上原参数
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)


def is_url(s):
    """检测输入是否是 URL（http/https 开头）。"""
    return s.startswith(("http://", "https://"))


def download_with_yt_dlp(url, workdir):
    """用 yt-dlp 从分享链接下载视频到 workdir，返回本地文件路径。"""
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        print("[error] yt-dlp 未安装，无法处理链接")
        print("[hint] 重新运行本脚本会自动装 yt-dlp；或手动: pip install yt-dlp")
        sys.exit(1)

    ydl_opts = {
        "outtmpl": str(workdir / "source.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "quiet": False,
        "no_warnings": False,
    }
    print("[download] 从链接下载视频: {}".format(url))
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print("[error] yt-dlp 下载失败: {}".format(e))
        print("[hint] 检查链接是否有效；部分平台需要 cookie，可参考 yt-dlp 文档配置")
        sys.exit(1)

    candidates = [c for c in workdir.glob("source.*")
                  if c.suffix.lower() in (".mp4", ".webm", ".mkv", ".flv", ".avi", ".m4v")]
    if not candidates:
        print("[error] 下载完成但未找到视频文件")
        sys.exit(1)
    return candidates[0]


def get_ffmpeg():
    """优先用 imageio-ffmpeg 自带的 ffmpeg 二进制，回退系统 ffmpeg。"""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        # 回退系统 ffmpeg
        from shutil import which
        ff = which("ffmpeg")
        if ff:
            return ff
        print("[error] 找不到 ffmpeg。imageio-ffmpeg 未安装且系统 PATH 无 ffmpeg。")
        print("[hint] 重新运行本脚本会自动装 imageio-ffmpeg；或手动: pip install imageio-ffmpeg")
        sys.exit(1)


def get_ffprobe():
    """ffprobe 不在 imageio-ffmpeg 里，用 ffmpeg 推算或回退系统 ffprobe。"""
    from shutil import which
    fp = which("ffprobe")
    if fp:
        return fp
    # 没有 ffprobe 时，用 ffmpeg -i 解析时长
    return None


def get_video_duration(video, ffmpeg_bin):
    fp = get_ffprobe()
    if fp:
        cmd = [fp, "-v", "quiet", "-print_format", "json", "-show_format", str(video)]
        r = run(cmd)
        if r.returncode == 0:
            try:
                return float(json.loads(r.stdout)["format"]["duration"])
            except (KeyError, ValueError):
                pass
    # 回退：用 ffmpeg -i 抓 stderr 里的 Duration
    r = run([ffmpeg_bin, "-i", str(video)])
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", r.stderr or "")
    if m:
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    return 0.0


def extract_audio(video, workdir, ffmpeg_bin):
    audio = workdir / "audio.wav"
    cmd = [ffmpeg_bin, "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(audio)]
    r = run(cmd)
    if r.returncode != 0:
        print("[error] ffmpeg 抽音失败:")
        print(r.stderr[-800:] if r.stderr else "")
        sys.exit(1)
    return audio


def extract_frames(video, workdir, ffmpeg_bin, scene_threshold, fps):
    frames_dir = workdir / "frames"
    frames_dir.mkdir(exist_ok=True)
    for old in frames_dir.glob("frame_*.jpg"):
        old.unlink()

    frames = []

    if fps and fps > 0:
        cmd = [
            ffmpeg_bin, "-y", "-i", str(video),
            "-vf", "fps={}".format(fps),
            "-q:v", "2",
            str(frames_dir / "frame_%04d.jpg"),
        ]
        run(cmd)
        frame_files = sorted(frames_dir.glob("frame_*.jpg"))
        for i, f in enumerate(frame_files):
            frames.append((str(f.relative_to(workdir)), round(i / fps, 2)))
        return frames

    cmd = [
        ffmpeg_bin, "-y", "-i", str(video),
        "-vf", "select='gt(scene,{})',showinfo,scale=1280:-1".format(scene_threshold),
        "-vsync", "vfr",
        "-q:v", "2",
        str(frames_dir / "frame_%04d.jpg"),
    ]
    r = run(cmd)
    times = re.findall(r"pts_time:(\d+\.?\d*)", r.stderr or "")
    frame_files = sorted(frames_dir.glob("frame_*.jpg"))

    if not frame_files:
        print("[warn] 场景切换未抽到帧，回退到每秒一帧")
        return extract_frames(video, workdir, ffmpeg_bin, 0, 1)

    for i, f in enumerate(frame_files):
        t = float(times[i]) if i < len(times) else 0.0
        frames.append((str(f.relative_to(workdir)), round(t, 2)))
    return frames


def detect_device():
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


def transcribe(audio, model_size, device):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[error] faster-whisper 仍未安装，环境配置异常")
        sys.exit(1)

    compute_type = "int8" if device == "cpu" else "float16"
    print("[whisper] 加载模型 {} ({})，首次会下载约 {} ...".format(
        model_size, device, "~1.5GB" if model_size == "medium" else "~500MB"))
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    segments, info = model.transcribe(
        str(audio),
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500, "speech_pad_ms": 200},
    )

    result = [
        {"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}
        for s in segments
    ]
    return result, info


def ocr_frames(workdir, frames, use_gpu):
    try:
        import easyocr
    except ImportError:
        print("[warn] easyocr 未装，跳过 OCR")
        return {}

    print("[ocr] 加载模型（首次下载约 100MB）...")
    reader = easyocr.Reader(["ch_sim", "en"], gpu=use_gpu)
    results = {}
    for i, (frame_rel, _) in enumerate(frames):
        frame_path = workdir / frame_rel
        try:
            ocr_result = reader.readtext(str(frame_path))
            texts = [item[1] for item in ocr_result]
            results[frame_rel] = " ".join(texts).strip()
        except Exception as e:
            results[frame_rel] = ""
            print("[warn] OCR 失败 {}: {}".format(frame_rel, e))
        if (i + 1) % 5 == 0:
            print("[ocr] 进度 {}/{}".format(i + 1, len(frames)))
    return results


def align_timeline(segments, frames, ocr_results):
    timeline = []
    for seg in segments:
        seg_mid = (seg["start"] + seg["end"]) / 2
        best = None
        best_diff = float("inf")
        for frame_rel, t in frames:
            diff = abs(t - seg_mid)
            if diff < best_diff:
                best_diff = diff
                best = (frame_rel, t)
        timeline.append({
            "start": seg["start"],
            "end": seg["end"],
            "narration": seg["text"],
            "subtitle": ocr_results.get(best[0], "") if best else "",
            "frame": best[0] if best else None,
            "frame_time": round(best[1], 2) if best else seg["start"],
        })
    for frame_rel, t in frames:
        in_seg = any(s["start"] <= t <= s["end"] for s in segments)
        if not in_seg:
            timeline.append({
                "start": round(t, 2),
                "end": round(t + 1.0, 2),
                "narration": "",
                "subtitle": ocr_results.get(frame_rel, ""),
                "frame": frame_rel,
                "frame_time": round(t, 2),
            })
    timeline.sort(key=lambda x: x["start"])
    return timeline


def main():
    parser = argparse.ArgumentParser(description="视频爆款拆解 pipeline（自动配置环境）")
    parser.add_argument("--input", required=True,
                        help="视频文件路径或分享链接（抖音/B站/小红书/视频号/YouTube 等）")
    parser.add_argument("--workdir", required=True, help="工作目录")
    parser.add_argument("--model", default="medium",
                        choices=["tiny", "base", "small", "medium", "large-v3"])
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--ocr", dest="ocr", action="store_true", default=True)
    parser.add_argument("--no-ocr", dest="ocr", action="store_false")
    parser.add_argument("--scene-threshold", type=float, default=0.3)
    parser.add_argument("--fps", type=float, default=0,
                        help="固定抽帧 fps，0=仅场景切换检测")
    args = parser.parse_args()

    ensure_env()

    workdir = Path(args.workdir).resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    if is_url(args.input):
        video = download_with_yt_dlp(args.input, workdir)
    else:
        video = Path(args.input).resolve()
        if not video.exists():
            print("[error] 视频不存在: {}".format(video))
            sys.exit(1)

    ffmpeg_bin = get_ffmpeg()
    duration = get_video_duration(video, ffmpeg_bin)
    print("=" * 50)
    print("[video] {}".format(video.name))
    print("[video] 时长 {:.1f}s | ffmpeg: {}".format(duration, ffmpeg_bin))
    print("=" * 50)

    print("[1/5] 抽音轨 (16kHz wav)")
    audio = extract_audio(video, workdir, ffmpeg_bin)

    print("[2/5] 抽关键帧")
    frames = extract_frames(video, workdir, ffmpeg_bin, args.scene_threshold, args.fps)
    print("      抽取 {} 帧".format(len(frames)))

    device = detect_device() if args.device == "auto" else args.device
    print("[3/5] whisper 转录 (model={}, device={})".format(args.model, device))
    segments, info = transcribe(audio, args.model, device)
    print("      转录 {} 段, 语言={}".format(len(segments), info.language))

    ocr_results = {}
    if args.ocr and frames:
        print("[4/5] OCR 抓字幕")
        ocr_results = ocr_frames(workdir, frames, use_gpu=(device == "cuda"))
    else:
        print("[4/5] 跳过 OCR")

    print("[5/5] 时间戳对齐 + 输出 JSON")
    timeline = align_timeline(segments, frames, ocr_results)
    full_text = " ".join(s["text"] for s in segments)

    result = {
        "video": str(video),
        "duration": round(duration, 2),
        "model": args.model,
        "device": device,
        "language": info.language,
        "timeline": timeline,
        "full_text": full_text,
        "segments_count": len(segments),
        "frames_count": len(frames),
    }

    output = workdir / "analysis.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("")
    print("[done] 输出: {}".format(output))
    print("       时长 {:.1f}s | 段落 {} | 帧 {} | 时间线条目 {}".format(
        duration, len(segments), len(frames), len(timeline)))


if __name__ == "__main__":
    main()
