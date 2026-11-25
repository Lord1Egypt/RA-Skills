# -*- coding: utf-8 -*-
"""TTS 批量 + 强校验——skill-promo-video
用法：python3 tts_batch.py --narr <tts.json> --out-dir <dir>
tts.json: [{"id","tts"}...]；文本自动去「？」（IndexTTS2 静默失败坑）。
⛔ 完成后校验：每个 wav 存在且 mtime 新鲜；任一失败=整批不可信（GPU OOM 假 OK 教训）。
"""
import json, subprocess, sys, os, time, argparse

sys.stdout.reconfigure(encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narr", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--medtts", default=os.path.expanduser("~/.local/bin/medtts"))
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    segs = json.load(open(a.narr, encoding="utf-8"))
    t0 = time.time()
    fails = []
    for seg in segs:
        wav = os.path.join(a.out_dir, seg["id"] + ".wav")
        txt = seg["tts"].replace("？", "。").replace("?", "。")  # pitfalls #17：问号静默失败
        r = subprocess.run(["bash", a.medtts, txt, wav],
                           capture_output=True, text=True, timeout=300)
        # pitfalls #2：rc=0 不可信，验文件+mtime+size
        if (not os.path.exists(wav)) or os.path.getmtime(wav) < t0 or os.path.getsize(wav) < 1000:
            fails.append(seg["id"])
            print(seg["id"], "FAIL（无输出/mtime 陈旧——疑 GPU OOM，先清显存重跑）",
                  (r.stderr or "")[-120:])
        else:
            print(seg["id"], "OK", os.path.getsize(wav), "B")
    print("BATCH", "ALL OK" if not fails else f"FAILED: {fails}")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
