#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给成片尾部加「黑屏字幕」结尾卡

为什么：
  沙雕短剧的收尾最好是「一句冷幽默 + 黑屏字幕」，而不是让角色站在那儿收场。
  这一步纯 ffmpeg 合成，不依赖 app。

用法：
  python3 add_endcard.py --video 第01集.mp4 --out 第01集-成片.mp4 \
      --line1 "本故事纯属虚构" \
      --line2 "如有雷同，说明你们日报也是这么写的" \
      --duration 2.4

  --opener  可选：在片头前加一张黑卡（标题/栏目名）
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile


def run(cmd):
    """跑外部命令的唯一入口：列表传参、不经过 shell。"""
    p = subprocess.run(list(cmd), capture_output=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", "ignore")[-3000:])
        raise SystemExit(f"外部命令失败：{' '.join(cmd[:6])}…")
    return p


def probe(path):
    """返回 (width, height, fps, duration)"""
    out = run([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1",
        path,
    ]).stdout.decode("utf-8", "ignore")
    kv = dict(
        line.split("=", 1) for line in out.strip().splitlines() if "=" in line
    )
    try:
        num, den = (kv.get("r_frame_rate", "30/1").split("/") + ["1"])[:2]
        fps = float(num) / float(den or 1)
    except (ValueError, ZeroDivisionError):
        fps = 30.0
    if not (fps > 0):
        fps = 30.0
    try:
        return int(kv["width"]), int(kv["height"]), fps, float(kv["duration"])
    except (KeyError, ValueError):
        raise SystemExit(f"✗ 读不出视频信息（宽高/时长）：{path}")


def ff_path(path):
    """filtergraph 里的路径：转义 \\ : ' , [ ] 会破坏参数解析的字符。"""
    s = str(path)
    for ch in ("\\", ":", "'", ",", "[", "]"):
        s = s.replace(ch, "\\" + ch)
    return s


def make_card(path, size, fps, duration, lines, font, tmpdir, bg="0x0b0b0b"):
    w, h = size
    # 字体名同样在 filtergraph 里，引号和换行会破坏解析
    font = str(font).replace("'", "").replace("\n", " ").strip() or "PingFang SC"
    filters = ["format=yuv420p"]
    for i, (t, fs, y, col, delay) in enumerate(lines):
        # 文案走 textfile：冒号、引号、花括号、百分号全都不用转义
        text_file = os.path.join(tmpdir, f"line{i}.txt")
        with open(text_file, "w", encoding="utf-8") as fh:
            fh.write(str(t).replace("\r", " ").replace("\n", " "))
        filters.append(
            f"drawtext=font='{font}':textfile='{ff_path(text_file)}':expansion=none"
            f":fontsize={fs}:fontcolor={col}:x=(w-text_w)/2:y={y}-text_h/2"
            f":enable='between(t,{delay},{duration})'"
        )
    vf = ",".join(filters)
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c={bg}:s={w}x{h}:r={fps}:d={duration}",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            path,
        ]
    )


def main():
    ap = argparse.ArgumentParser(description="黑屏字幕结尾卡")
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--line1", default="本故事纯属虚构")
    ap.add_argument("--line2", default="")
    ap.add_argument("--duration", type=float, default=2.4)
    ap.add_argument("--font", default="PingFang SC")
    ap.add_argument("--crf", default="20")
    args = ap.parse_args()

    if not re.fullmatch(r"\d{1,2}", str(args.crf)):
        ap.error(f"--crf 必须是 0–51 的整数，实际是 {args.crf}")
    if not (0.2 <= args.duration <= 15):
        ap.error(f"--duration 建议在 0.2–15 秒之间，实际是 {args.duration}")

    if not os.path.isfile(args.video):
        raise SystemExit(f"找不到视频：{args.video}")

    w, h, fps, _ = probe(args.video)
    tmp = tempfile.mkdtemp(prefix="endcard_")
    try:
        card = os.path.join(tmp, "card.mp4")

        # 主句在中间偏上，副句在其下；最后 0.4s 一起淡出靠 simple fade
        lines = [
            (args.line1, max(28, int(h * 0.030)), int(h * 0.46), "0xF2F2F2", 0),
        ]
        if args.line2:
            lines.append(
                (args.line2, max(20, int(h * 0.020)), int(h * 0.56), "0xA8A8A8", 0)
            )
        make_card(card, (w, h), fps, args.duration, lines, args.font, tmp)

        # 音轨补齐静音，直接 concat
        out = args.out
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-i", args.video,
                "-f", "lavfi", "-t", f"{args.duration}",
                "-i", f"anullsrc=channel_layout=stereo:sample_rate=48000",
                "-i", card,
                "-filter_complex",
                f"[0:v]scale={w}:{h},setsar=1[v0];[2:v]setsar=1[v1];"
                f"[0:a]aresample=48000[a0];[1:a]aresample=48000[a1];"
                f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
                out,
            ]
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f">> 已加结尾卡：{args.out}（+{args.duration:.1f}s）")


if __name__ == "__main__":
    main()
