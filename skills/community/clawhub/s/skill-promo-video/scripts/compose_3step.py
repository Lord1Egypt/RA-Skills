# -*- coding: utf-8 -*-
"""三步式合成模板——skill-promo-video
Step1 视频链（xfade+水印overlay+ASS字幕）→ Step2 音轨（BGM+旁白adelay）→ Step3 合并。
用法（全部必填）：
  python3 compose_3step.py --segs segs.json --narr narr.json --subs-map subs.json \
      --tts-dir tts/ --bgm bgm.mp3 --watermark wm.png --ass subs.ass --out final.mp4
  segs.json: [["png"|"vid", 路径, png段时长秒(vid 忽略)], ...]
  narr.json: [{"t0","t1","id"}, ...]（秒；id 对应 tts-dir 下 <id>.wav 与 subs-map 键）
  subs.json: {"<id>": "字幕文本"}
纪律：输出每次全新唯一名；中间产物唯一临时目录；字幕结束=所在段尾（防溢出下一段）。
"""
import json, subprocess, sys, argparse

sys.stdout.reconfigure(encoding="utf-8")

def probe_dur(p):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    assert r, f"missing/empty {p}"
    return round(float(r), 3)

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segs", required=True)
    ap.add_argument("--narr", required=True)
    ap.add_argument("--subs-map", required=True, help="json: {id: 字幕文本}")
    ap.add_argument("--tts-dir", required=True)
    ap.add_argument("--bgm", required=True)
    ap.add_argument("--watermark", required=True)
    ap.add_argument("--ass", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--fade", type=float, default=0.5)
    ap.add_argument("--tmp-dir", default="", help="中间产物目录（默认唯一临时目录，防旧文件假命中）")
    a = ap.parse_args()
    FADE, FPS = a.fade, a.fps
    import tempfile, os as _osmod
    tmpd = a.tmp_dir or tempfile.mkdtemp(prefix="spv_compose_")
    _osmod.makedirs(tmpd, exist_ok=True)

    segs = json.load(open(a.segs))
    narr = json.load(open(a.narr))
    submap = json.load(open(a.subs_map, encoding="utf-8"))

    # ── 时长表 ──
    durs, inputs = [], []
    for kind, src, dur in segs:
        if kind == "png":
            durs.append(dur); inputs += ["-loop", "1", "-framerate", str(FPS), "-t", str(dur + FADE), "-i", src]
        else:
            durs.append(probe_dur(src)); inputs += ["-i", src]
    offsets, off = [], 0.0
    for du in durs[:-1]:
        off += du - FADE; offsets.append(round(off, 3))
    total = round(off + durs[-1], 2)

    # ── ASS 字幕 ──
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "",
           "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV",
           "Style: Sub,Noto Sans CJK SC,44,&H00FFFFFF,&H00101820,&H80000000,1,3,1,2,80,80,96", "",
           "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for t0, t1, vid in narr:
        ass.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Sub,,0,0,0,,{submap[vid].replace(',', '，')}")
    open(a.ass, "w", encoding="utf-8").write("\n".join(ass))

    # ── Step1 视频链 ──
    n_seg = len(segs)
    cmd = ["ffmpeg", "-y"] + inputs + ["-i", a.watermark]
    parts = []
    for k in range(n_seg):
        kind = segs[k][0]
        fit = ("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" if kind == "vid"
               else "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2")
        parts.append(f"[{k}:v]fps={FPS},{fit},setsar=1,format=yuv420p[kn{k}]")
    cur = "kn0"
    for k in range(1, n_seg):
        parts.append(f"[{cur}][kn{k}]xfade=transition=fade:duration={FADE}:offset={offsets[k-1]:.3f}[vx{k}]")
        cur = f"vx{k}"
    parts.append(f"[{n_seg}:v]scale=420:-1[wmk]")
    parts.append(f"[{cur}][wmk]overlay=x=W-w-26:y=26:format=auto[vw]")
    parts.append(f"[vw]subtitles={a.ass}:fontsdir=/usr/share/fonts/opentype/noto[vf]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vf]",
            "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-r", str(FPS),
            "-t", f"{total:.2f}", os.path.join(tmpd, "video.mp4")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("STEP1 FAIL:", r.stderr[-1200:]); sys.exit(1)
    print("step1 video ok", total)

    # ── Step2 音轨 ──
    acmd = ["ffmpeg", "-y", "-i", a.bgm]
    aparts = [f"[0:a]aresample=48000,volume=0.14,atrim=0:{total:.2f}[bgmn]"]
    mix = "[bgmn]"
    for j, (t0, _t1, vid) in enumerate(narr):
        wav = f"{a.tts_dir}/{vid}.wav"
        assert os.path.getmtime(wav) > time.time() - 86400, f"⛔ {wav} mtime 陈旧（假 OK 嫌疑）"
        acmd += ["-i", wav]
        ms = int(t0 * 1000)
        aparts.append(f"[{j+1}:a]aresample=48000,adelay={ms}|{ms}[a{j}]")
        mix += f"[a{j}]"
    aparts.append(f"{mix}amix=inputs={len(narr)+1}:normalize=0:duration=longest,"
                  f"afade=t=in:d=1.2,afade=t=out:st={total-3:.2f}:d=2.8,"
                  f"aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    acmd += ["-filter_complex", ";".join(aparts), "-map", "[aout]",
             "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.2f}", os.path.join(tmpd, "audio.m4a")]
    import os as _os, time as _t
    r = subprocess.run(acmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("STEP2 FAIL:", r.stderr[-1200:]); sys.exit(1)
    print("step2 audio ok")

    # ── Step3 合并 ──
    r = subprocess.run(["ffmpeg", "-y", "-i", os.path.join(tmpd, "video.mp4"), "-i", os.path.join(tmpd, "audio.m4a"),
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                        "-movflags", "+faststart", a.out], capture_output=True, text=True)
    if r.returncode != 0:
        print("STEP3 FAIL:", r.stderr[-800:]); sys.exit(1)
    print("FINAL OK:", a.out, probe_dur(a.out))

if __name__ == "__main__":
    import os, time
    main()
