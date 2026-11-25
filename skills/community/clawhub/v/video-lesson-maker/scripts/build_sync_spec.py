#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""音画同步标注生成器 v2（自研，项目「世校赛讲座视频」沉淀）。

根治「绘画 / 动画 / 文字讲解不同步」：让白板揭示时间轴与配音时间轴用同一只钟，
并且**每一句口播都精确驱动它对应的那块画面**（讲到哪、画到哪）。

v2 相比 v1 的关键变化
--------------------
1. **逐句节拍（beats）**：v1 只按「标题/左/右/结论」四拍粗切，一拍动辄覆盖
   五六句口播（最长 20s），整块内容在一次窗口里按位置硬画，必然「讲到哪画不到哪」。
   v2 改为 scenes.json 里显式声明每个节拍覆盖哪几句口播（lines）＋ 对应哪块
   画面（rects，可多块顺序画）＋ 可选指点手势（point 路径，只移动笔尖不落墨）。
   一句一画、多句一画都可以，语义映射由作者按画面内容决定。

2. **真实语音计时**：v1 用 plan 的段间隔推算时长，最后一段按 target 总时长
   补齐（假时长，最长 17.6s），导致末尾十几秒静音空画。v2 直接测量每个
   segNN.wav 的真实语音长度（--narration-dir），节拍时长 = 语音 + 少量收尾；
   幕与幕之间不再各自叠加凝视，成片总长 = 最后一句语音结束 + 结尾凝视，
   彻底消除「每幕 +0.6s 累积漂移」和「尾部空白」。

3. **节拍间留白**：每拍画到「本拍语音结束 + tail」即收笔，剩余时间是已完成
   画面的静止展示（渲染器 fill_static 天然支持），口播换句时画面已停稳。

用法
----
  python build_sync_spec.py \
      --srt Vxx.srt \
      --plan narration/narration_plan.json \
      --narration-dir narration \
      --scenes scenes.json \
      --out-dir . \
      --gaze 1000 --tail 250

scenes.json（v2 格式；rects 为 [x,y,w,h]，画布坐标）：
  [
    {
      "lines": [1, 4],
      "beats": [
        {"lines": [1],  "rects": [[0, 0, 1536, 190]]},
        {"lines": [2],  "rects": [[500, 180, 520, 290]]},
        {"lines": [3,4], "rects": [[0, 600, 1536, 264]]}
      ]
    }
  ]
  - lines：本幕覆盖的段号区间（仅作自检用，实际以 beats 为准）。
  - beats[].lines：本节拍对应的口播段号（须在本幕 lines 内）。
  - beats[].rects：本节拍依次画哪些区域；可用 {"rect":[...], "dur":毫秒}
    指定单块时长（未指定的均分剩余）。
  - beats[].point：[[x,y],...] 指点路径（画布坐标）——本拍只移动笔尖不落墨，
    用于总结/过渡句（如「用这五条逻辑重新审视你的项目」时笔尖沿三角描一遍）。

向后兼容：beats 缺失时回退到 v1 的 bodyBeats 粗切（不推荐）。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import wave

import numpy as np


# ── 真实语音时长测量 ──────────────────────────────────────────
def measure_speech_seconds(wav_path: str) -> float | None:
    """测量单个 segNN.wav 的真实语音长度（去首尾静音；20ms 窗、峰值 4% 阈值）。"""
    try:
        w = wave.open(wav_path, "rb")
    except (OSError, wave.Error):
        return None
    with w:
        n = w.getnframes()
        sr = w.getframerate()
        if n == 0 or sr == 0:
            return None
        audio = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
    win = max(1, int(sr * 0.02))
    nwin = len(audio) // win
    if nwin == 0:
        return None
    e = np.sqrt((audio[:nwin * win].reshape(nwin, win) ** 2).mean(axis=1))
    thr = max(float(e.max()) * 0.04, 50.0)
    voiced = e > thr
    if not voiced.any():
        return 0.0
    first = int(np.argmax(voiced)) * 0.02
    last = (len(voiced) - int(np.argmax(voiced[::-1]))) * 0.02
    return max(0.05, last - first)


def load_timeline(plan_path: str, narration_dir: str | None):
    """返回 (starts, speech)：starts[i]=段i+1在音轨中的起始秒；speech[i]=真实语音秒数。"""
    plan = json.load(open(plan_path, encoding="utf-8"))
    segs = sorted(plan["segments"], key=lambda s: s["idx"])
    total = float(plan["total"])
    starts: dict[int, float] = {}
    gap: dict[int, float] = {}
    for i, s in enumerate(segs):
        starts[s["idx"]] = float(s["start"])
        if i + 1 < len(segs):
            gap[s["idx"]] = float(segs[i + 1]["start"]) - float(s["start"])
        else:
            gap[s["idx"]] = max(0.3, total - float(s["start"]))
    speech: dict[int, float] = {}
    if narration_dir and os.path.isdir(narration_dir):
        for idx in starts:
            p = os.path.join(narration_dir, "seg%02d.wav" % idx)
            m = measure_speech_seconds(p)
            if m is not None:
                speech[idx] = m
    # 兜底：没测到的用 plan 间隔
    for idx in starts:
        speech.setdefault(idx, gap[idx])
    return starts, speech, gap


# ── spec 生成 ──────────────────────────────────────────
def _norm_rects(beat):
    """把 beats[].rects 规范成 [{"rect":..., "dur":None|int}, ...]。"""
    out = []
    for item in beat.get("rects", []):
        if isinstance(item, dict):
            out.append({"rect": item["rect"], "dur": item.get("dur")})
        else:
            out.append({"rect": item, "dur": None})
    return out


def build_one_scene(scene_idx, scene, starts, speech, tail_ms, hard_end, gaze_ms):
    """hard_end：本幕必须结束的绝对时刻（下一幕首句起始；末幕为 None）。"""
    beats = scene.get("beats")
    if not beats:
        raise ValueError("scenes.json 需要 v2 的 beats 字段（逐句节拍）")

    # 自检：beats 覆盖的段号必须落在本幕 lines 内
    lo, hi = scene["lines"]
    covered = sorted({ln for b in beats for ln in b["lines"]})
    for ln in covered:
        if not (lo <= ln <= hi):
            raise ValueError("第%d幕 beats 覆盖段 %d 越界（lines=%s）" % (scene_idx + 1, ln, scene["lines"]))
    missing = [ln for ln in range(lo, hi + 1) if ln not in covered]
    if missing:
        raise ValueError("第%d幕有口播段未被任何节拍覆盖: %s" % (scene_idx + 1, missing))

    scene_start = starts[covered[0]]
    last_speech_end = starts[covered[-1]] + speech[covered[-1]]

    # 每个节拍的窗口：[本拍首句起始, 本拍末句语音结束 + tail]
    # 硬约束：下一拍首句起始（口播下一句开讲时，本拍必须画完）；
    #         末拍再受 hard_end 约束（幕界处不留负间隔）
    beat_windows = []
    for bi, b in enumerate(beats):
        first, last = b["lines"][0], b["lines"][-1]
        end = starts[last] + speech[last] + tail_ms / 1000.0
        if bi + 1 < len(beats):
            end = min(end, starts[beats[bi + 1]["lines"][0]] - 0.05)
        elif hard_end is not None:
            end = min(end, hard_end - 0.05)
        beat_windows.append((starts[first] - scene_start, end - scene_start, b))

    regions = []
    prev_end = 0.0  # 上一拍窗口结束（幕内相对秒）
    for win_start, win_end, beat in beat_windows:
        dur_ms = max(120, int(round((win_end - win_start) * 1000)))
        rects = _norm_rects(beat)
        if beat.get("point"):
            # 指点拍：单区域 + point 路径（region 仅占位）
            p0 = beat["point"][0]
            lead = max(0, int(round((win_start - prev_end) * 1000)))
            regions.append({
                "x": int(p0[0]), "y": int(p0[1]), "width": 1, "height": 1,
                "dur": dur_ms, "lead": lead, "mode": "point", "path": beat["point"],
            })
            prev_end = win_end
            continue
        if not rects:
            prev_end = win_end
            continue
        fixed = sum(r["dur"] for r in rects if r["dur"])
        free = [r for r in rects if not r["dur"]]
        share = max(60, (dur_ms - fixed) // max(1, len(free))) if free else 0
        first = True
        for r in rects:
            d = r["dur"] if r["dur"] else share
            x, y, w, h = r["rect"]
            # 拍间空隙放在本拍第一块的 lead（口播停顿时画面静止）；
            # 拍内多块紧接画（lead=0），由渲染器抬笔衔接
            lead = max(0, int(round((win_start - prev_end) * 1000))) if first else 0
            regions.append({"x": x, "y": y, "width": w, "height": h,
                            "dur": int(d), "lead": lead})
            first = False
        prev_end = win_end

    # 幕时长：非末幕 = 到下一幕首句起始（音轨无缝衔接，零漂移）；
    # 末幕 = 最后一句语音结束 + 结尾凝视。
    if hard_end is not None:
        scene_duration_ms = int(round((hard_end - scene_start) * 1000))
    else:
        scene_duration_ms = int(round((last_speech_end + gaze_ms / 1000.0 - scene_start) * 1000))

    spec = {
        "canvas": {"width": 1536, "height": 864},
        "sceneDurationMs": scene_duration_ms,
        "regions": regions,
        "durationMs": 3000,
        "leadMs": 0,
        "gazeMs": 0,
    }
    return spec, scene_duration_ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--plan", required=True, help="narration_plan.json")
    ap.add_argument("--narration-dir", default=None,
                    help="旁音目录（含 segNN.wav），用于实测每句真实语音时长")
    ap.add_argument("--scenes", required=True, help="幕定义 JSON（v2 beats 格式）")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--gaze", type=float, default=1000, help="全片结尾凝视(ms)")
    ap.add_argument("--tail", type=float, default=250, help="每拍语音结束后的收尾时长(ms)")
    a = ap.parse_args()

    starts, speech, gap = load_timeline(a.plan, a.narration_dir)
    if os.path.exists(a.scenes):
        scenes = json.load(open(a.scenes, encoding="utf-8"))
    else:
        scenes = json.loads(a.scenes)

    os.makedirs(a.out_dir, exist_ok=True)
    # 预计算每幕的 hard_end（下一幕首句起始）
    first_lines = []
    for sc in scenes:
        lo, hi = sc["lines"]
        first_lines.append(lo)
    total_ms = 0
    for i, scene in enumerate(scenes):
        hard_end = starts[first_lines[i + 1]] if i + 1 < len(scenes) else None
        spec, sd = build_one_scene(i, scene, starts, speech, a.tail, hard_end, a.gaze)
        out = os.path.join(a.out_dir, "spec-01-%d.json" % (i + 1))
        json.dump(spec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        total_ms += sd
        print("spec-01-%d.json: 节拍元素 %d 个  幕时长 %dms  行 %s"
              % (i + 1, len(spec["regions"]), sd, scene["lines"]))
    print("汇总：%d 幕，预计成片 %.1fs（真实语音 %.1fs + 结尾凝视 %.1fs）"
          % (len(scenes), total_ms / 1000.0,
             max(starts[l] + speech[l] for l in speech) if speech else 0, a.gaze / 1000.0))


if __name__ == "__main__":
    main()
