#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给成片加音效 + BGM（后期混音）

用法：
  python3 mix_audio.py \
    --video 05-成片/第01集-raw.mp4 \
    --manifest 02-配音/第01集/配音表.json \
    --sfx-dir 03-素材/音效 \
    --bgm 03-素材/BGM/bgm_loop.wav \
    --out 05-成片/第01集-混音.mp4

逻辑：
  1. 从视频里抽出人声轨（48kHz 立体声）
  2. 按 配音表.json 的 duration 累加，算出每句开始时间
  3. 把该句的 sfx 音效放到开始时间
  4. BGM 循环铺满全片，音量压到 0.12
  5. 混音后替换视频音轨（视频流直接 copy，不重编码）
"""

import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SFX_MAP = {
    "闹钟": "闹钟.wav",
    "开门声": "开门.wav",
    "开门": "开门.wav",
    "咚": "咚.wav",
    "乌鸦": "乌鸦.wav",
    "灵魂出窍": "灵魂出窍.wav",
    "叮": "叮.wav",
    "脚步": "脚步.wav",
}


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        n = w.getnframes()
        ch = w.getnchannels()
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        data = data.reshape(-1, 2)
    else:
        data = np.stack([data, data], axis=1)
    return data, sr


def write_wav(path, data, sr):
    data = np.clip(data, -1.0, 1.0)
    pcm = (data * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"命令失败：{' '.join(cmd)}\n{r.stderr}")


def main():
    ap = argparse.ArgumentParser(description="成片加音效 + BGM")
    ap.add_argument("--video", required=True, help="输入成片（含人声）")
    ap.add_argument("--out", required=True, help="输出成片")
    ap.add_argument("--manifest", required=True, help="配音表.json")
    ap.add_argument("--sfx-dir", default="03-素材/音效", help="音效目录")
    ap.add_argument("--bgm", default="", help="BGM 循环文件（wav）")
    ap.add_argument("--bgm-volume", type=float, default=0.12)
    ap.add_argument("--sfx-volume", type=float, default=0.45)
    ap.add_argument("--no-bgm", action="store_true")
    args = ap.parse_args()

    video = Path(args.video)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8-sig"))
    sfx_dir = Path(args.sfx_dir)

    tmp = Path(tempfile.mkdtemp(prefix="shadiao_mix_"))
    voice_wav = tmp / "voice.wav"
    mixed_wav = tmp / "mixed.wav"

    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "2", "-ar", "48000", "-f", "wav", str(voice_wav)])
    voice, sr = read_wav(voice_wav)
    total = len(voice)
    print(f">> 人声：{total / sr:.2f}s / {sr}Hz")

    # 句首时间
    cursor = 0.0
    placements = []
    for line in manifest.get("lines", []):
        dur = float(line.get("duration", 0)) / 1000.0
        sfx = (line.get("sfx") or "").strip()
        if sfx:
            placements.append((cursor, sfx, line.get("seq")))
        cursor += dur
    print(f">> 台词总时长：{cursor:.2f}s / 音效 {len(placements)} 个")

    # 混音
    mix = voice.copy()

    # BGM
    if not args.no_bgm and args.bgm:
        bgm_path = Path(args.bgm)
        if bgm_path.is_file():
            bgm, bsr = read_wav(bgm_path)
            if bsr != sr:
                print(f"  ! BGM 采样率 {bsr} != {sr}，跳过", file=sys.stderr)
            else:
                reps = math.ceil(total / len(bgm))
                bed = np.tile(bgm, (reps, 1))[:total]
                mix += bed * args.bgm_volume
                print(f">> BGM：{bgm_path.name} ×{reps}，音量 {args.bgm_volume}")
        else:
            print(f"  ! BGM 不存在：{bgm_path}", file=sys.stderr)

    # SFX（支持 脚步+咚 这种多音效）
    placed = 0
    for start, sfx, seq in placements:
        parts = [p.strip() for p in re.split(r"[+＋]", sfx) if p.strip()]
        for part in parts:
            name = None
            for key, filename in SFX_MAP.items():
                if key in part:
                    name = filename
                    break
            if not name:
                print(f"  ! 第 {seq} 句音效「{part}」没有映射，跳过", file=sys.stderr)
                continue
            path = sfx_dir / name
            if not path.is_file():
                print(f"  ! 音效不存在：{path}", file=sys.stderr)
                continue
            sig, ssr = read_wav(path)
            if ssr != sr:
                print(f"  ! 音效 {name} 采样率不对，跳过", file=sys.stderr)
                continue
            pos = max(0, int(round((start - 0.02) * sr)))
            end = min(total, pos + len(sig))
            if end > pos:
                mix[pos:end] += sig[: end - pos] * args.sfx_volume
                placed += 1
                print(f"   + {start:6.2f}s  第{seq}句  {part} → {name}")

    # 防削波
    peak = float(np.max(np.abs(mix)))
    if peak > 0.98:
        mix = mix / peak * 0.98
        print(f">> 峰值 {peak:.2f}，已压到 0.98")

    write_wav(mixed_wav, mix, sr)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-i", str(video), "-i", str(mixed_wav),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(args.out),
    ])
    print(f">> 完成：{args.out}（音效 {placed}/{len(placements)}）")


if __name__ == "__main__":
    main()
