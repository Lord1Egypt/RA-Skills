# -*- coding: utf-8 -*-
"""音画对齐互相关实测——唇动曲线 × 音频能量包络，求最优滞后。
用法: python3 measure_sync.py --video seg.mp4 --wav tts.wav
输出 JSON: {"lip_start","audio_start","lag","delay"}  delay=compose 应注入偏移(秒)
原理: H3 段内唇动与它消费的音频同源；把 wav 前置静音计入后，互相关峰值即真实对齐点。
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")


def lip_curve(video, fps=24):
    tmp = tempfile.mkdtemp(prefix="sync_")
    subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-i", video, "-vf", "scale=480:-1",
                    "-f", "image2", os.path.join(tmp, "f%04d.png")], check=True)
    fs = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
    frames = [np.asarray(Image.open(os.path.join(tmp, f)).convert("L"), dtype=np.float32)
              for f in fs]
    curve = []
    for i in range(1, len(frames)):
        a, b = frames[i - 1], frames[i]
        h, w = a.shape
        box_a = a[int(h * 0.40):int(h * 0.80), int(w * 0.35):int(w * 0.65)]
        box_b = b[int(h * 0.40):int(h * 0.80), int(w * 0.35):int(w * 0.65)]
        curve.append(float(np.abs(box_a - box_b).mean()))
    return np.array(curve), fps, len(frames)


def audio_env(wav, fps=24):
    w = wave.open(wav)
    sr, n = w.getframerate(), w.getnframes()
    data = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    if data.ndim > 1:
        data = data.mean(axis=1)
    win = max(1, int(sr / fps))
    env = [float(np.sqrt((data[i:i + win] ** 2).mean())) for i in range(0, len(data) - win, win)]
    return np.array(env)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--wav", required=True)
    args = ap.parse_args()

    curve, fps, nframes = lip_curve(args.video)
    env = audio_env(args.wav, fps)
    # 归一化后互相关（音频可能短于视频段）
    c = (curve - curve.mean()) / (curve.std() + 1e-6)
    e = (env - env.mean()) / (env.std() + 1e-6)
    n = min(len(c), len(e))
    best_lag, best_score = 0, -2.0
    for lag in range(0, max(1, len(c) - len(e) + 1) if len(e) < len(c) else 1):
        pass
    # 通用互相关：e 在 c 上滑动
    scores = []
    for lag in range(0, max(1, len(c) - len(e) + 1)):
        seg = c[lag:lag + len(e)]
        if len(seg) < len(e):
            break
        scores.append((float((seg * e).mean()), lag))
    if scores:
        best_score, best_lag = max(scores)
    delay = round(best_lag / fps, 3)
    print(json.dumps({"lip_frames": len(curve) + 1, "env_frames": len(env),
                      "best_corr": round(best_score, 3), "delay": delay}))


if __name__ == "__main__":
    main()
