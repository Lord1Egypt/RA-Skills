#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 narration_plan.json 重新排布已合成的 segNN.wav → narration-track.wav。

为什么需要它
------------
`narrate_edge_tts.py` 会把音轨直接混流进成片，所以**音轨只在跑 TTS 时生成一次**。
一旦之后 SRT / 分段 / plan 发生变更（改文案、加句、拆幕），plan 里的 `start`
与磁盘上的 `narration-track.wav` 就会失配：

- 画面与字幕都按 **plan** 走 → 二者一致；
- 但听感按 **旧音轨** 走 → 观众听到的句子比画面早/晚，甚至整段缺失
  （实测：V03 的 seg29 根本没进旧音轨，末尾一段讲解完全没声音，
  而画面却老老实实为它画了 3 秒）。

本脚本只重排已有的 seg 片段，**不重新调 TTS**（秒级完成、零额外费用），
保证 `plan` / 音轨 / 字幕 / 画面四者共用同一只钟。

用法
----
  python rebuild_track.py --plan narration/narration_plan.json \\
      --work narration --out narration/narration-track.wav

  # 批量
  for d in V01_rubric V02_truth; do
    python rebuild_track.py --plan $d/narration/narration_plan.json \\
        --work $d/narration --out $d/narration/narration-track.wav
  done

自检输出会给出 `segs / speech_end / track`，请核对：
**成片无声时长 ≈ speech_end + 结尾凝视（1.0~1.5s）**。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, help="narration_plan.json")
    ap.add_argument("--work", default=None, help="segNN.wav 所在目录（默认 plan 同级）")
    ap.add_argument("--out", default=None, help="输出 wav（默认 work/narration-track.wav）")
    ap.add_argument("--sr", type=int, default=24000)
    ap.add_argument("--pad", type=float, default=0.6, help="末尾留白秒数")
    ap.add_argument("--fade", type=float, default=0.04, help="每段淡入淡出秒数（防爆音）")
    a = ap.parse_args()

    try:
        import soundfile as sf
    except ImportError:
        print("需要 soundfile：pip install soundfile", file=sys.stderr)
        return 2

    work = a.work or os.path.dirname(os.path.abspath(a.plan))
    out = a.out or os.path.join(work, "narration-track.wav")
    plan = json.load(open(a.plan, encoding="utf-8"))
    segs = sorted(plan["segments"], key=lambda s: s["idx"])

    clips = []
    for s in segs:
        p = os.path.join(work, "seg%02d.wav" % int(s["idx"]))
        if not os.path.exists(p):
            print("缺少分段音频：%s" % p, file=sys.stderr)
            return 3
        data, sr = sf.read(p)
        if sr != a.sr:
            print("采样率不一致：%s 为 %d（期望 %d）" % (p, sr, a.sr), file=sys.stderr)
            return 4
        if data.ndim > 1:
            data = data.mean(axis=1)
        clips.append((float(s["start"]), data.astype(np.float32), int(s["idx"])))

    speech_end = max(st + len(c) / a.sr for st, c, _ in clips)
    total = speech_end + a.pad
    track = np.zeros(int(total * a.sr) + a.sr, dtype=np.float32)

    overlaps = []
    for st, clip, idx in clips:
        i0 = int(st * a.sr)
        n = min(len(clip), len(track) - i0)
        if n <= 0:
            continue
        seg = clip[:n].copy()
        f = min(int(a.fade * a.sr), n // 2)
        if f > 0:
            seg[:f] *= np.linspace(0, 1, f)
            seg[-f:] *= np.linspace(1, 0, f)
        if np.abs(track[i0:i0 + n]).max() > 0.01 and np.abs(seg).max() > 0.01:
            overlaps.append(idx)
        track[i0:i0 + n] += seg

    sf.write(out, track, a.sr)
    print("音轨 %s：seg %d 段  语音结束 %.2fs  轨长 %.2fs%s"
          % (out, len(clips), speech_end, len(track) / a.sr,
             ("  !! 重叠段 %s" % overlaps) if overlaps else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
