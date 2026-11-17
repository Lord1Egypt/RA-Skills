#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配音预演 + 锚点计算（自包含版）。

把「写配音计划」这一步从"凭感觉估时长"改成"先合成再量真实时长"，彻底消除
narration 段间重叠 / 配音超出画面的问题（本项目 V09 踩过的大坑）。

流程：
  1. 解析 SRT，按段号取出每段解说文本；
  2. 用 edge-tts 逐段合成 mp3，ffmpeg 裁掉首尾静音 → wav；
  3. 测量每段真实时长；
  4. 段间留 --gap 秒间隙，累计算出每段混入锚点 start（秒）；
  5. 写出可直接交给 narrate_edge_tts.py 的 narration_plan.json。

关键约定：
  - zh-CN-YunxiNeural 常速实测约 5.2 字/秒；节奏偏慢的段可用 --rates 给正 rate 微加速。
  - 若配音总时长 > 无声成片时长，脚本会告警；此时应延长各幕 sceneDurationMs
    （重渲）或给若干段加正 rate，而不是事后硬拉音频（会吞字）。

用法：
  python prepare_narration.py --srt 脚本.srt --work ./narration \
      --video 无声.mp4 --output 配音版.mp4 --total 130.7 \
      [--voice zh-CN-YunxiNeural] [--gap 0.4] [--rates 1:0,2:8,3:-5] \
      [--plan-out narration/narration_plan.json]

依赖：edge-tts、soundfile、numpy，ffmpeg（系统或 FFMPEG_PATH 指定）。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

import numpy as np
import soundfile as sf

FFMPEG = os.environ.get("FFMPEG_PATH", "ffmpeg")


def parse_srt(path):
    txt = open(path, encoding="utf-8").read()
    segs = {}
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        segs[int(lines[0])] = "".join(lines[2:])
    return segs


def synth(text, out_mp3, voice, rate, retries=4):
    """edge-tts 合成（网络抖动重试）。--rate 正值=加速。"""
    r = f"{rate:+d}%"
    for attempt in range(retries):
        try:
            subprocess.run(
                [sys.executable, "-m", "edge_tts", "--voice", voice, "--rate", r,
                 "--text", text, "--write-media", out_mp3],
                check=True, capture_output=True, timeout=120,
            )
            if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1000:
                return
        except Exception:
            pass
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"合成失败: {text[:20]!r} rate={r}")


def trim(mp3, wav, sr):
    """mp3→wav 并裁掉首尾静音（-45dB 阈值）。"""
    subprocess.run(
        [FFMPEG, "-y", "-loglevel", "error", "-i", mp3,
         "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,"
                "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse",
         "-ar", str(sr), "-ac", "1", wav],
        check=True, capture_output=True, timeout=120,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True, help="字幕脚本(.srt)")
    ap.add_argument("--work", required=True, help="分段 wav 工作目录")
    ap.add_argument("--video", required=True, help="无声成片路径")
    ap.add_argument("--output", required=True, help="输出的配音成片路径")
    ap.add_argument("--total", type=float, required=True, help="无声成片总时长(秒)")
    ap.add_argument("--voice", default="zh-CN-YunxiNeural")
    ap.add_argument("--sr", type=int, default=24000)
    ap.add_argument("--gap", type=float, default=0.4, help="段间静音间隙(秒)")
    ap.add_argument("--rates", default="", help="idx:rate 映射, 如 1:0,2:8,3:-5")
    ap.add_argument("--plan-out", default=None, help="输出 plan(默认 work/narration_plan.json)")
    a = ap.parse_args()

    os.makedirs(a.work, exist_ok=True)
    segs = parse_srt(a.srt)
    rate_map = {}
    for kv in a.rates.split(","):
        kv = kv.strip()
        if not kv:
            continue
        idx, rt = kv.split(":")
        rate_map[int(idx)] = int(rt)

    idxs = sorted(segs.keys())
    durations = []
    for idx in idxs:
        mp3 = os.path.join(a.work, f"seg{idx:02d}.mp3")
        wav = os.path.join(a.work, f"seg{idx:02d}.wav")
        rate = rate_map.get(idx, 0)
        if not (os.path.exists(mp3) and os.path.getsize(mp3) > 1000):
            synth(segs[idx], mp3, a.voice, rate)
        if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(mp3):
            trim(mp3, wav, a.sr)
        d, _ = sf.read(wav)
        dur = len(d) / a.sr
        durations.append(dur)
        print(f"seg{idx:02d} rate={rate:+3d}%  {dur:6.2f}s  {segs[idx][:18]}...")

    # 累计锚点（段间留 gap 秒）
    anchors = []
    t = 0.0
    for i, idx in enumerate(idxs):
        anchors.append((idx, t, durations[i], rate_map.get(idx, 0)))
        t += durations[i] + a.gap
    last_end = t - a.gap
    print(f"配音总时长(含间隙): {last_end:.2f}s  无声成片: {a.total:.2f}s")
    if last_end > a.total + 0.01:
        print(f"[warn] 配音超出画面 {last_end - a.total:.2f}s！请延长各幕 sceneDurationMs 或给若干段加正 rate。")

    total_out = max(a.total, last_end + 0.5)
    plan = {
        "video": a.video,
        "srt": a.srt,
        "work": a.work,
        "output": a.output,
        "total": round(total_out, 2),
        "voice": a.voice,
        "sr": a.sr,
        "segments": [
            {"idx": idx, "start": round(s, 2), "rate": rt}
            for idx, s, _, rt in anchors
        ],
    }
    out_path = a.plan_out or os.path.join(a.work, "narration_plan.json")
    json.dump(plan, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"已写出 narration_plan.json -> {out_path}")


if __name__ == "__main__":
    main()
