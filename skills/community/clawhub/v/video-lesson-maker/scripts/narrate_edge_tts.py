# -*- coding: utf-8 -*-
"""edge-tts 云希配音管线（V01 验证通过）。

流程：按 SRT 逐段合成中文解说 → 裁静音 → 按画面事件锚点混入音轨 → 与无声成片混音。
- 默认音色 zh-CN-YunxiNeural（云希，男声·阳光青年，普通话标准、断句自然、不夸张）
- rate：相对变速百分比，正值=加速、负值=减速；场景节奏偏慢时用 +8~15% 微加速卡点
- 每段之间做 40ms 淡入淡出防爆音；自动检查重叠

配置 JSON 字段：
    video     无声成片路径（画面锚点依据，也作为混音底）
    srt       字幕脚本路径（按段号取文本）
    work      工作目录（分段 mp3/wav 与合成音轨）
    output    输出的配音成片路径
    total     成片总时长（秒）
    voice     音色，默认 zh-CN-YunxiNeural
    sr        采样率，默认 24000
    segments [{idx, start, rate}]  idx=SRT 段号；start=该段混入秒（对齐画面事件）；
                                   rate=相对变速%（0=原速）

用法：
    python narrate_edge_tts.py --config plan.json
依赖：edge-tts、soundfile、numpy、ffmpeg（系统或已配置路径）。
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
    """edge-tts 合成（网络抖动重试）。注意：--rate 正值=加速。"""
    r = f"{rate:+d}%"
    for attempt in range(retries):
        try:
            subprocess.run([sys.executable, "-m", "edge_tts", "--voice", voice,
                            "--rate", r, "--text", text, "--write-media", out_mp3],
                           check=True, capture_output=True, timeout=120)
            if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1000:
                return
        except Exception:
            pass
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"合成失败: {text[:20]} rate={r}")


def to_wav_trim(mp3, wav, sr):
    """mp3→wav 并裁掉首尾静音（-45dB 阈值）。"""
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", mp3,
                    "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,"
                           "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse",
                    "-ar", str(sr), "-ac", "1", wav], check=True, capture_output=True, timeout=120)


def run(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    video, srt, work = cfg["video"], cfg["srt"], cfg["work"]
    out_video = cfg["output"]
    voice = cfg.get("voice", "zh-CN-YunxiNeural")
    sr = int(cfg.get("sr", 24000))
    total = float(cfg.get("total", 0))
    os.makedirs(work, exist_ok=True)
    segs = parse_srt(srt)

    # 1) 合成 + 裁剪 + 测时长
    clips = []
    for seg in cfg["segments"]:
        idx, start, rate = int(seg["idx"]), float(seg["start"]), int(seg.get("rate", 0))
        tag = f"seg{idx:02d}" + (f"_r{rate}" if rate else "")
        mp3 = os.path.join(work, tag + ".mp3")
        wav = os.path.join(work, tag + ".wav")
        if not (os.path.exists(mp3) and os.path.getsize(mp3) > 1000):
            synth(segs[idx], mp3, voice, rate)
        if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(mp3):
            to_wav_trim(mp3, wav, sr)
        d, _ = sf.read(wav)
        dur = len(d) / sr
        clips.append((start, d.astype(np.float32), idx, dur))
        print(f"seg{idx:02d} rate={rate:+3d}%  {start:6.2f} -> {start+dur:6.2f}  ({dur:5.2f}s)  {segs[idx][:20]}...")

    # 2) 重叠检查
    clips.sort()
    for (s1, _, i1, d1), (s2, _, i2, _) in zip(clips, clips[1:]):
        if s1 + d1 > s2 + 0.02:
            print(f"  !! seg{i1:02d} 与 seg{i2:02d} 重叠 {s1+d1-s2:.2f}s")

    # 3) 组装音轨（淡入淡出防爆音）
    if not total:
        total = max(s + d for s, _, _, d in clips) + 0.5
    track = np.zeros(int(total * sr) + sr, dtype=np.float32)
    for start, clip, idx, dur in clips:
        i0 = int(start * sr)
        n = min(len(clip), len(track) - i0)
        seg = clip[:n].copy()
        f = min(int(0.04 * sr), n // 2)
        if f > 0:
            seg[:f] *= np.linspace(0, 1, f)
            seg[-f:] *= np.linspace(1, 0, f)
        track[i0:i0 + n] += seg

    audio_wav = os.path.join(work, "narration-track.wav")
    sf.write(audio_wav, track, sr)
    print("音轨:", audio_wav, f"{len(track)/sr:.1f}s")

    # 4) 混音（视频流 copy，不二次编码）
    subprocess.run([FFMPEG, "-y", "-loglevel", "error",
                    "-i", video, "-i", audio_wav,
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", out_video], check=True, timeout=300)
    print("成片:", out_video, f"{os.path.getsize(out_video)/1e6:.1f}MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="配音计划 JSON")
    a = ap.parse_args()
    run(a.config)
