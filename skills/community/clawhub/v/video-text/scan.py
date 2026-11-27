"""核 v2 —— 一条片子，画面上到底有什么，说清楚

v1 只做了「读字」。v2 加三样真正有用的东西：

  一、分区。水印/台标通常在角上，字幕通常在下方。按区域统计，
      比把所有字混成一张清单有用得多。
  二、重复检测。同一句话在多帧反复出现 = 固定层（水印、台标、常驻标题）；
      只出现一次 = 内容层。这两类要分开，因为它们该不该在、能不能删，答案不同。
  三、字幕导出。逐帧 OCR 变成 SRT。这是最实际的用途：
      你没字幕轨的片子，也能拿到一份。

用法：
    python analysis/check.py 片.mp4                       # 概览
    python analysis/check.py 片.mp4 --srt out/字幕.srt     # 导出字幕
    python analysis/check.py 片.mp4 --report out/核.md     # 出报告
    python analysis/check.py 片.mp4 --step 0.5 --json x.json

区域（按画面高度百分比）：
    顶部 0-18%      底部 78-100%     中间 18-78%

判断规则：
    固定层 = 出现帧数 / 总帧数 >= 0.6
    内容层 = 其余
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

import numpy as np

def _find_tool(name):
    """找 ffmpeg / ffprobe：先看环境变量，再看同目录，最后看 PATH。"""
    import shutil
    env = os.environ.get('FFMPEG_DIR')
    if env:
        p = os.path.join(env, name + ('.exe' if os.name == 'nt' else ''))
        if os.path.exists(p):
            return p
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, name + ('.exe' if os.name == 'nt' else ''))
    if os.path.exists(p):
        return p
    found = shutil.which(name)
    if found:
        return found
    # 兜底：默认位置
    return os.path.join(r'C:\Users\0\Documents\deepseek-harness\default-workspace\tools',
                        name + '.exe')


FF = _find_tool('ffmpeg')
FP = _find_tool('ffprobe')

TOP, BOT = 0.18, 0.78          # 区域分界
FIXED_RATIO = 0.6              # 出现超过 60% 的帧 → 固定层
MIN_CONF = 0.55
# 只由这些字符组成的，多半是噪声（单个标点、单个字母）
NOISE = re.compile(r'^[\W_]{0,2}$')


def probe(path: str) -> dict:
    out = subprocess.run(
        [FP, '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=width,height,duration',
         '-show_entries', 'format=duration', '-of', 'json', path],
        capture_output=True, text=True, check=False).stdout
    try:
        j = json.loads(out)
    except Exception:
        return {}
    st = (j.get('streams') or [{}])[0]
    dur = float((j.get('format') or {}).get('duration') or st.get('duration') or 0)
    return {'w': st.get('width'), 'h': st.get('height'), 'dur': dur}


def grab(path, t, w, h):
    r = subprocess.run(
        [FF, '-v', 'error', '-ss', f'{t:.2f}', '-i', path,
         '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
        capture_output=True, check=False)
    if len(r.stdout) != w * h * 3:
        return None
    return np.frombuffer(r.stdout, np.uint8).reshape(h, w, 3)


def zone_of(y: int, h: int) -> str:
    r = y / max(h, 1)
    if r < TOP:
        return '顶部'
    if r >= BOT:
        return '底部'
    return '中间'


def ocr(engine, img, h):
    res, _ = engine(img)
    if not res:
        return []
    out = []
    for box, txt, conf in res:
        if conf < MIN_CONF:
            continue
        txt = txt.strip()
        if not txt or NOISE.match(txt):
            continue
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        cy = int(sum(ys) / len(ys))
        out.append({
            'text': txt,
            'conf': round(float(conf), 3),
            'zone': zone_of(cy, h),
            'y': cy,
            'x': int(sum(xs) / len(xs)),
            'h': int(max(ys) - min(ys)),
        })
    return out


def scan(src, step):
    info = probe(src)
    w, h, dur = info.get('w'), info.get('h'), info.get('dur') or 0
    if not (w and h):
        return None
    scale = min(1.0, 1280.0 / w)
    ow, oh = int(w * scale) // 2 * 2, int(h * scale) // 2 * 2
    from rapidocr_onnxruntime import RapidOCR
    engine = RapidOCR()
    import cv2

    frames, t = [], 0.0
    while t <= dur + 1e-6:
        img = grab(src, t, w, h)
        if img is not None:
            if scale < 1.0:
                img = cv2.resize(img, (ow, oh), interpolation=cv2.INTER_AREA)
            frames.append({'t': round(t, 2), 'texts': ocr(engine, img, oh)})
        t += step
    return {'src': src, 'w': w, 'h': h, 'dur': dur, 'step': step, 'frames': frames}


def classify(frames):
    """把一句话按出现帧数分成固定层 / 内容层"""
    n = len(frames)
    seen = {}
    for f in frames:
        for r in f['texts']:
            k = r['text']
            d = seen.setdefault(k, {'text': k, 'frames': 0, 'zones': {}, 'maxconf': 0.0,
                                    'times': []})
            d['frames'] += 1
            d['zones'][r['zone']] = d['zones'].get(r['zone'], 0) + 1
            d['maxconf'] = max(d['maxconf'], r['conf'])
            d['times'].append(f['t'])
    fixed, content = [], []
    for d in seen.values():
        d['ratio'] = d['frames'] / max(n, 1)
        d['main_zone'] = max(d['zones'], key=d['zones'].get)
        (fixed if d['ratio'] >= FIXED_RATIO else content).append(d)
    fixed.sort(key=lambda d: -d['ratio'])
    content.sort(key=lambda d: -d['frames'])
    return fixed, content


def to_srt(frames, path, min_conf=0.6):
    """逐帧 OCR → SRT。只取底部区域，且只保留连续出现的行"""
    lines = []
    for i, f in enumerate(frames):
        t0 = f['t']
        t1 = frames[i + 1]['t'] if i + 1 < len(frames) else t0 + 1.0
        txts = [r['text'] for r in f['texts'] if r['zone'] == '底部' and r['conf'] >= min_conf]
        if not txts:
            continue
        joined = ' '.join(txts)
        if lines and lines[-1][2] == joined:
            lines[-1][1] = t1
        else:
            lines.append([t0, t1, joined])

    def ts(x):
        hh = int(x // 3600); mm = int(x % 3600 // 60)
        ss = int(x % 60); ms = int((x - int(x)) * 1000)
        return f'{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}'

    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        for i, (a, b, t) in enumerate(lines, 1):
            fh.write(f'{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n')
    return len(lines)


def report(res, fixed, content, path):
    f = res['frames']
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    L = []
    L.append(f"# 核：{os.path.basename(res['src'])}\n")
    L.append(f"```\n{res['w']}x{res['h']}   {res['dur']:.1f} 秒   "
             f"每 {res['step']:g} 秒一帧   共 {len(f)} 帧\n```\n")

    L.append('## 一、固定层（多帧重复出现 — 水印/台标/常驻标题）\n')
    L.append('这些东西一直在画面上，不是内容，是来源的印记。\n')
    L.append('| 出现比例 | 区域 | 文字 |')
    L.append('|---:|---|---|')
    for d in fixed[:15]:
        L.append(f"| {d['ratio']*100:.0f}% | {d['main_zone']} | `{d['text'][:40]}` |")

    L.append('\n## 二、内容层（只出现几次 — 真在变的东西）\n')
    if content:
        L.append('| 次数 | 区域 | 文字 |')
        L.append('|---:|---|---|')
        for d in content[:25]:
            L.append(f"| {d['frames']} | {d['main_zone']} | `{d['text'][:40]}` |")
    else:
        L.append('（没有）\n')

    # 每帧密度
    L.append('\n## 三、逐帧文字量\n')
    L.append('```')
    for fr in f:
        bar = '█' * min(len(fr['texts']), 40)
        top = ' | '.join(r['text'] for r in fr['texts'][:3])[:56]
        L.append(f"{fr['t']:6.1f}s {len(fr['texts']):2d} {bar:<40} {top}")
    L.append('```')
    open(path, 'w', encoding='utf-8').write('\n'.join(L))
    return path


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    src = a[0]
    if not os.path.exists(src):
        print('没有这个文件:', src); return
    step = float(a[a.index('--step') + 1]) if '--step' in a else 1.0
    srt = a[a.index('--srt') + 1] if '--srt' in a else None
    rep = a[a.index('--report') + 1] if '--report' in a else None
    jout = a[a.index('--json') + 1] if '--json' in a else None

    print(f'扫描: {os.path.basename(src)}')
    res = scan(src, step)
    if not res:
        print('读不出来'); return
    print(f'  {res["w"]}x{res["h"]}  {res["dur"]:.1f}s  {len(res["frames"])} 帧')

    fixed, content = classify(res['frames'])
    print(f'\n固定层 {len(fixed)} 条（多帧重复，多半是水印/台标）:')
    for d in fixed[:8]:
        print(f'  {d["ratio"]*100:3.0f}%  [{d["main_zone"]}]  {d["text"][:44]}')
    print(f'\n内容层 {len(content)} 条（只出现几次）')

    if srt:
        n = to_srt(res['frames'], srt)
        print(f'\n字幕 {n} 段 → {srt}')
    if rep:
        report(res, fixed, content, rep)
        print(f'报告 → {rep}')
    if jout:
        os.makedirs(os.path.dirname(jout) or '.', exist_ok=True)
        json.dump(res, open(jout, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'JSON → {jout}')


if __name__ == '__main__':
    main()
