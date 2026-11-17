# -*- coding: utf-8 -*-
"""意群字幕重建（V01 验证 v5）：从真实配音时间轴生成「意群完整 + 尽可能短」的同步字幕。

三大原则：
1. 意群优先：只在 。！？；： 等意群边界断屏；意群超过单行容量才退而在逗号处切
   （优先逗号保意群，枚举逗号次之，兜底硬切避开《》）。
2. 声画同步：切换点对齐配音音轨中的真实静音停顿（能量检测），
   用「前向+后向语速约束窗口」保证每条字幕有足够展示时间、也给后面内容留时间。
3. 单行不超框：每屏 ≤ max-chars（默认 28，实测 28 字≈908px，1080 宽安全）。

为什么不能直接用原始 SRT 时间：配音阶段做过裁静音/变速/锚点重排，
原 SRT 的均分时间轴必然与配音错位（最大可差 6s 以上）。

配音计划 JSON（与 narrate_edge_tts.py 的 segments 对应）：
    [{"idx": 1, "start": 0.30, "file": "seg01.wav"}, ...]   # file 为 narration 工作目录下的文件名

用法：
    python build_subtitles.py --srt 脚本.srt --track 音轨.wav --plan plan.json \
        --out 同步字幕.srt [--total 95.9] [--max-chars 28]
"""
import argparse
import json
import os
import re

import numpy as np
import soundfile as sf


def parse_srt(path):
    txt = open(path, encoding="utf-8").read()
    segs = {}
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        segs[int(lines[0])] = "".join(lines[2:])
    return segs


def detect_regions(track, sr):
    """音轨能量检测语音活动区（20ms 窗，2% 峰值阈值），返回 [(start, end), ...] 秒。"""
    tr, sr = sf.read(track)
    win = int(0.02 * sr)
    n = len(tr) // win
    rms = np.sqrt(np.array([np.mean(tr[i*win:(i+1)*win]**2) for i in range(n)]))
    voiced = rms > rms.max() * 0.02
    raw, i = [], 0
    while i < n:
        if voiced[i]:
            j = i
            while j < n and voiced[j]:
                j += 1
            raw.append([i * 0.02, j * 0.02])
            i = j
        else:
            i += 1
    merged = []
    for r in raw:
        if merged and r[0] - merged[-1][1] < 0.05:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [r for r in merged if r[1] - r[0] >= 0.08]


def weak_split(p, max_chars, weak_cap):
    """意群超长时退一步切：优先逗号/冒号，再枚举逗号，兜底硬切（避开《》内部）。"""
    if len(p) <= max_chars:
        return [p]
    for cls in ("，：", "、"):
        cands = [i + 1 for i, ch in enumerate(p)
                 if ch in cls and 0 < i + 1 <= weak_cap and len(p) - (i + 1) <= max_chars]
        if cands:
            k = max(cands)
            return [p[:k]] + weak_split(p[k:], max_chars, weak_cap)
    k = max_chars
    in_book = any(ch == "《" for ch in p[:k]) and "》" not in p[:k]
    if in_book:
        close = p.find("》", k)
        k = close + 1 if close != -1 else len(p)
    return [p[:k]] + weak_split(p[k:], max_chars, weak_cap)


def split_cues(text, max_chars, weak_cap):
    """主切分：只在句末标点/冒号等意群边界断屏。"""
    parts = [p for p in re.findall(r"[^。！？；：]+[。！？；：]?", text) if p]
    cues = []
    for p in parts:
        cues.extend(weak_split(p, max_chars, weak_cap))
    return cues


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--track", required=True, help="混音后的配音音轨 wav")
    ap.add_argument("--plan", required=True, help="配音计划 JSON（idx/start/file）")
    ap.add_argument("--work", default=None, help="分段 wav 所在目录（默认取 plan 的 file 同级）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--total", type=float, default=95.9)
    ap.add_argument("--max-chars", type=int, default=28)
    ap.add_argument("--weak-cap", type=int, default=26)
    ap.add_argument("--pre", type=float, default=0.12, help="每段首条提前亮相")
    ap.add_argument("--tail", type=float, default=0.25, help="每段末条延后谢幕")
    ap.add_argument("--gap-min", type=float, default=0.15)
    ap.add_argument("--tol", type=float, default=1.2)
    ap.add_argument("--rate-fast", type=float, default=7.5)
    ap.add_argument("--rate-slow", type=float, default=3.4)
    ap.add_argument("--rate-typ", type=float, default=4.9)
    a = ap.parse_args()

    segs = parse_srt(a.srt)
    plan = json.load(open(a.plan, encoding="utf-8"))
    work = a.work or os.path.dirname(plan[0]["file"]) or "."
    regions = detect_regions(a.track, 24000)

    def gap_points(s0, s1):
        pts = []
        for x, y in zip(regions, regions[1:]):
            if y[0] - x[1] >= a.gap_min and x[1] > s0 - 0.15 and y[0] < s1 + 0.15:
                pts.append((x[1] + y[0]) / 2)
        return pts

    raw_entries = []
    for seg in plan:
        idx, start = int(seg["idx"]), float(seg["start"])
        d, _ = sf.read(os.path.join(work, seg["file"]))
        s0, s1 = start, start + len(d) / 24000
        cues = split_cues(segs[idx], a.max_chars, a.weak_cap)
        gaps = gap_points(s0, s1)
        n_cue = len(cues)

        suffix = [0] * (n_cue + 1)
        for k in range(n_cue - 2, -1, -1):
            suffix[k] = suffix[k + 1] + len(cues[k + 1])

        bounds, prev = [], s0
        for k in range(n_cue - 1):
            c = len(cues[k])
            lo = prev + c / a.rate_fast
            hi = s1 - suffix[k] / a.rate_fast
            if hi < lo:
                mid = (lo + hi) / 2
                lo = hi = mid
            target = min(max(prev + c / a.rate_typ, lo), hi)
            best, bd = None, a.tol
            for g in gaps:
                if lo <= g <= hi and abs(g - target) < bd:
                    best, bd = g, abs(g - target)
            b = best if best is not None else target
            bounds.append(b)
            prev = b

        for k, cue in enumerate(cues):
            cs = s0 - a.pre if k == 0 else bounds[k - 1]
            ce = bounds[k] if k < n_cue - 1 else s1 + a.tail
            raw_entries.append([cs, ce, cue, idx])

    raw_entries.sort(key=lambda e: e[0])
    entries = []
    for i, (cs, ce, tx, idx) in enumerate(raw_entries):
        cs = max(0.0, cs)
        if entries:
            cs = max(cs, entries[-1][1])
        nxt = raw_entries[i + 1][0] if i + 1 < len(raw_entries) else None
        lim = a.total if nxt is None else min(a.total, nxt)
        ce = min(ce, lim)
        if ce - cs < 0.5:
            ce = min(cs + 0.5, lim)
        entries.append((cs, ce, tx, idx))

    blocks = []
    for i, (cs, ce, tx, idx) in enumerate(entries, 1):
        blocks.append(f"{i}\n{fmt(cs)} --> {fmt(ce)}\n{tx}\n")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(blocks))

    mx = max(len(e[2]) for e in entries)
    mn = min(e[1] - e[0] for e in entries)
    ok = all(entries[i][1] <= entries[i + 1][0] + 0.001 for i in range(len(entries) - 1))
    ok = ok and all(0 <= cs < ce <= a.total + 0.001 for cs, ce, _, _ in entries)
    print(f"共 {len(entries)} 条字幕；最长 {mx} 字（上限 {a.max_chars}）；最短展示 {mn:.2f}s；"
          f"自检 {'通过' if ok and mx <= a.max_chars else '有问题'}")
    print("已写出:", a.out)
    for cs, ce, tx, idx in entries:
        print(f"  段{idx:02d} {fmt(cs)} --> {fmt(ce)} ({ce-cs:4.2f}s/{len(tx):2d}字) {tx}")


if __name__ == "__main__":
    main()
