# -*- coding: utf-8 -*-
"""QC 闸门编排——skill-promo-video v2

六道闸（按 SOP 顺序）：
  text    文字稳定性：talking 卡段首/尾帧文字区像素差（漂移超标=引擎把卡面文字画花了）
  lips    口型运动：三帧嘴部区域方差（运动量过低=没在说话/静态）
  hands   手部抽帧：2 帧手部区 3x 放大裁片（供逐指清点——多指/并指一票否决，人工/judge 复核）
  av      音画对齐：段表×旁白表一致性（旁白不得长于所在卡段）
  asr     听写闸门：调外部 FunASR 闸门命令（--gate-cmd 模板，可选）
  narr    旁白数字口径闸：成数词族/口语百分点/tts 读法展开与 % 直读（10-22 立规，
          根治「一成六」类缺陷——正本 narr_audit.py，exit 1 即拦截发车）

用法：
  python3 qc_gates.py text --video s03.mp4 --prefix s03
  python3 qc_gates.py lips --video s03.mp4
  python3 qc_gates.py hands --video s03.mp4 --out-dir qc_hands/
  python3 qc_gates.py av --segs segs.json --narr narr.json
  python3 qc_gates.py asr --video final.mp4 --gate-cmd "python3 /path/delivery_gate.py --media {media} --require {require}"
"""
import argparse, json, os, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")


def sh(cmd, timeout=60):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def dur(p):
    r = sh(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", p])
    return float(r.stdout.strip())


def grab(video, t, prefix):
    tmpd = tempfile.mkdtemp(prefix="spv_qc_")
    out = os.path.join(tmpd, prefix + ".png")
    r = sh(["ffmpeg", "-y", "-ss", "%.2f" % t, "-i", video, "-frames:v", "1", out])
    assert r.returncode == 0, r.stderr[-200:]
    return out


def region_diff(a_path, b_path, box):
    """PIL 裁区差值比（0~1，越高越漂移）。"""
    from PIL import Image, ImageChops
    ia, ib = Image.open(a_path).convert("L"), Image.open(b_path).convert("L")
    w, h = ia.size
    box = (int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h))
    da, db = ia.crop(box), ib.crop(box)
    if da.size != db.size:
        db = db.resize(da.size)
    diff = ImageChops.difference(da, db)
    hist = diff.histogram()
    total = sum(hist)
    changed = sum(hist[16:])  # 像素差>16 视为变化
    return changed / max(1, total)


def cmd_text(a):
    d = dur(a.video)
    f1 = grab(a.video, d * 0.02, "first")
    f2 = grab(a.video, d * 0.98, "last")
    ratio = region_diff(f1, f2, (0.45, 0.05, 0.98, 0.92))  # 右侧卷面文字区（card 版式）
    verdict = "PASS" if ratio <= a.threshold else "FAIL"
    print("TEXT-STABILITY %.4f (阈值 %.3f) -> %s" % (ratio, a.threshold, verdict))
    sys.exit(0 if verdict == "PASS" else 1)


def cmd_lips(a):
    """帧间差分：相邻采样帧嘴部区域平均像素差（运动特异，抗纹理干扰）。"""
    d = dur(a.video)
    import numpy as np
    from PIL import Image
    crops = []
    for i, pct in enumerate((0.15, 0.4, 0.65, 0.9)):
        f = grab(a.video, d * pct, "l%d" % i)
        im = Image.open(f).convert("L")
        w, h = im.size
        box = ((0.10, 0.10, 0.55, 0.55) if a.crop == "card" else (0.38, 0.52, 0.62, 0.78))
        crops.append(np.asarray(im.crop((int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3]))), dtype=np.int16))
    diffs = [float(np.abs(crops[i + 1] - crops[i]).mean()) for i in range(len(crops) - 1)]
    motion = max(diffs)
    verdict = "PASS" if motion >= a.min_spread else "FAIL"
    print("LIP-MOTION max-frame-diff=%.1f (最低 %.1f) diffs=%s -> %s" % (motion, a.min_spread, ["%.1f" % x for x in diffs], verdict))
    sys.exit(0 if verdict == "PASS" else 1)


def cmd_hands(a):
    d = dur(a.video)
    os.makedirs(a.out_dir, exist_ok=True)
    outs = []
    from PIL import Image
    for i, pct in enumerate((0.3, 0.7)):
        f = grab(a.video, d * pct, "h%d" % i)
        im = Image.open(f)
        w, h = im.size
        crop = im.crop((int(w * 0.25), int(h * 0.55), int(w * 0.75), h))
        crop = crop.resize((crop.width * 3, crop.height * 3))
        p = os.path.join(a.out_dir, "%s_hand_%d.png" % (a.prefix, i))
        crop.save(p)
        outs.append(p)
    print("HAND CROPS（逐指清点：每只手五指，多指/并指=一票否决）:")
    for p in outs:
        print("  " + p)


def cmd_av(a):
    """音画对齐：每条旁白窗口必须完整落在其对应段内（字幕边界=段尾纪律）。"""
    segs = json.load(open(a.segs))
    narr = json.load(open(a.narr))
    FADE = 0.5
    spans, t = [], 0.0
    for k, (kind, src, d) in enumerate(segs):
        real = dur(src) if kind == "vid" else float(d)
        spans.append((t, t + real, src))
        t += real - (FADE if k < len(segs) - 1 else 0)
    problems = []
    for n in narr:
        if n["t1"] - n["t0"] <= 0:
            problems.append(n["id"] + ": 零长度窗口"); continue
        span = next((sp for sp in spans if n["id"] in os.path.basename(sp[2])), None)
        if span is None:
            problems.append(n["id"] + ": 段表中找不到对应段（id 须为段文件名子串）"); continue
        if n["t0"] < span[0] - 0.01 or n["t1"] > span[1] + 0.01:
            problems.append("%s: 窗口[%.2f,%.2f] 越出段[%.2f,%.2f]" % (n["id"], n["t0"], n["t1"], span[0], span[1]))
    print("AV-CHECK segments=%d narrations=%d -> %s" % (len(segs), len(narr), "PASS" if not problems else problems))
    sys.exit(1 if problems else 0)


def cmd_asr(a):
    assert a.gate_cmd, "--gate-cmd 必填（外部 FunASR 闸门命令模板，{media} {require} 占位）"
    cmd = a.gate_cmd.format(media=a.video, require=a.require or "")
    r = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=600)
    print(r.stdout[-1500:])
    if r.returncode != 0:
        print("ASR GATE FAIL"); sys.exit(1)
    print("ASR GATE PASS")


def cmd_narr(a):
    from narr_audit import audit
    rc = 0
    for p in a.tts:
        rc |= audit(p)
    sys.exit(rc)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="gate", required=True)

    p = sub.add_parser("text"); p.add_argument("--video", required=True)
    p.add_argument("--threshold", type=float, default=0.055); p.set_defaults(fn=cmd_text)

    p = sub.add_parser("lips"); p.add_argument("--video", required=True)
    p.add_argument("--min-spread", type=float, default=6.0)
    p.add_argument("--crop", choices=["card", "talker"], default="talker",
                   help="card=人物在左/中左（面部区 x10-55%,y10-55%）；talker=人物居中（x38-62%,y52-78%）")
    p.set_defaults(fn=cmd_lips)

    p = sub.add_parser("hands"); p.add_argument("--video", required=True)
    p.add_argument("--out-dir", required=True); p.add_argument("--prefix", default="seg")
    p.set_defaults(fn=cmd_hands)

    p = sub.add_parser("av"); p.add_argument("--segs", required=True)
    p.add_argument("--narr", required=True); p.set_defaults(fn=cmd_av)

    p = sub.add_parser("narr"); p.add_argument("--tts", nargs="+", required=True); p.set_defaults(fn=cmd_narr)

    p = sub.add_parser("asr"); p.add_argument("--video", required=True)
    p.add_argument("--gate-cmd", default="", help="外部听写闸门命令模板（经 shell 执行；{media} {require} 占位）")
    p.add_argument("--require", default="")
    p.set_defaults(fn=cmd_asr)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
