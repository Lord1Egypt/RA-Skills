#!/usr/bin/env python3
"""备料脚本: 探测视频元信息 + 抽帧 + 长视频场景拆条。

用法:
    python3 extract_frames.py <video> [-f frames输出目录] [--interval 2] [--split]

行为:
- 默认: 探测时长/分辨率/编码, 按间隔抽帧到 <outdir>/f_XX.jpg。
- 时长>180s 时抽帧间隔自动放宽到 5s(可用 --interval 覆盖)。
- --split: 场景切点检测拆条(scene>0.4), 输出 segments/ 与 segframes/, 段名按序号+时长。
- 依赖 ffmpeg/ffprobe (macOS: brew install ffmpeg, 或 pip install imageio-ffmpeg 取内置二进制)。
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def find_bin(name: str) -> str:
    p = shutil.which(name)
    if p:
        return p
    try:
        import imageio_ffmpeg  # pip install imageio-ffmpeg
        if name == "ffmpeg":
            return imageio_ffmpeg.get_ffmpeg_exe()
        if name == "ffprobe":
            cand = Path(imageio_ffmpeg.get_ffmpeg_exe()).parent / "ffprobe"
            if cand.exists():
                return str(cand)
    except ImportError:
        pass
    print(f"[错误] 缺少 {name}。安装: brew install ffmpeg 或 pip install imageio-ffmpeg", file=sys.stderr)
    sys.exit(3)


def probe(video: Path) -> dict:
    ffprobe = find_bin("ffprobe")
    cmd = [ffprobe, "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", str(video)]
    info = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    fmt = info.get("format", {})
    vstream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    dur = float(fmt.get("duration", 0) or 0)
    return {
        "duration": dur,
        "duration_hms": f"{int(dur // 60)}:{int(dur % 60):02d}",
        "width": vstream.get("width"),
        "height": vstream.get("height"),
        "codec": vstream.get("codec_name"),
        "fps": vstream.get("r_frame_rate"),
        "size_mb": round(video.stat().st_size / 1e6, 1),
    }


def extract_frames(video: Path, out_dir: Path, interval: float) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_bin("ffmpeg")
    cmd = [ffmpeg, "-y", "-i", str(video), "-vf", f"fps=1/{interval},scale=640:-2",
           "-q:v", "3", str(out_dir / "f_%02d.jpg")]
    subprocess.run(cmd, check=True, capture_output=True)
    n = len(list(out_dir.glob("f_*.jpg")))
    return n


def split_scenes(video: Path, work_dir: Path) -> list:
    seg_dir = work_dir / "segments"
    frame_dir = work_dir / "segframes"
    seg_dir.mkdir(parents=True, exist_ok=True)
    frame_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_bin("ffmpeg")

    # 1) 场景切点检测
    detect = [ffmpeg, "-i", str(video), "-vf",
              "select='gt(scene,0.4)',showinfo", "-f", "null", "-"]
    r = subprocess.run(detect, capture_output=True, text=True)
    cuts = []
    for line in r.stderr.splitlines():
        if "pts_time:" in line and "showinfo" in line:
            t = float(line.split("pts_time:")[1].split()[0])
            if t > 1.0:  # 忽略开头1s内的切点
                cuts.append(round(t, 1))
    cuts = sorted(set(cuts))

    # 2) 按切点拆段
    dur = probe(video)["duration"]
    bounds = [0.0] + cuts + [dur]
    segments = []
    for i in range(len(bounds) - 1):
        s, e = bounds[i], bounds[i + 1]
        if e - s < 10:  # <10s 的碎片并入说明, 不单独成段
            continue
        name = f"seg{i + 1:02d}_{int(s // 60)}m{int(s % 60):02d}_{int(e - s)}s.mp4"
        seg_path = seg_dir / name
        cmd = ["ffmpeg", "-y", "-ss", str(s), "-to", str(e), "-i", str(video),
               "-c", "copy", str(seg_path)]
        subprocess.run(cmd, check=True, capture_output=True)
        # 3) 段抽帧: 首帧+中点帧
        for tag, at in (("a", s + 0.5), ("b", (s + e) / 2)):
            cmd = ["ffmpeg", "-y", "-ss", str(at), "-i", str(video),
                   "-frames:v", "1", "-q:v", "3",
                   str(frame_dir / f"{seg_path.stem}_{tag}.jpg")]
            subprocess.run(cmd, check=True, capture_output=True)
        segments.append({"name": name, "start": s, "end": e, "dur": round(e - s, 1)})
    return segments


def main():
    ap = argparse.ArgumentParser(description="视频抽帧与场景拆条")
    ap.add_argument("video", help="视频文件路径")
    ap.add_argument("-f", "--frames-dir", default=None, help="帧图输出目录(默认 <video目录>/frames)")
    ap.add_argument("--interval", type=float, default=None, help="抽帧间隔秒(默认2s, >3分钟自动5s)")
    ap.add_argument("--split", action="store_true", help="启用场景拆条(segments/ + segframes/)")
    args = ap.parse_args()

    video = Path(args.video).expanduser()
    if not video.exists():
        print(f"[错误] 文件不存在: {video}", file=sys.stderr)
        sys.exit(1)

    work_dir = video.parent
    info = probe(video)
    print("== 元信息 ==")
    print(json.dumps(info, ensure_ascii=False, indent=2))

    interval = args.interval or (5.0 if info["duration"] > 180 else 2.0)
    frames_dir = Path(args.frames_dir) if args.frames_dir else work_dir / "frames"
    n = extract_frames(video, frames_dir, interval)
    print(f"\n== 抽帧 ==  间隔 {interval}s, 共 {n} 帧 -> {frames_dir}")

    if args.split:
        segs = split_scenes(video, work_dir)
        print(f"\n== 拆条 ==  共 {len(segs)} 段 -> {work_dir / 'segments'}")
        for s in segs:
            print(f"  {s['name']}  start={s['start']}s dur={s['dur']}s")
        (work_dir / "segments_index.json").write_text(
            json.dumps(segs, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"索引: {work_dir / 'segments_index.json'}")


if __name__ == "__main__":
    main()
