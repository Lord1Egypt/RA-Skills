#!/usr/bin/env python3
"""
把一条长视频(已烧好字幕的成片)按 clips 配置切成多条 9:16 竖屏爆款片段，
每条顶部烧一个中文钩子大标题，背景用模糊填充。

用法:
    python3 render_clips.py --config clips.json

clips.json 结构见 examples/clips.example.json。
依赖: ffmpeg(需带 libass/freetype，macOS 上用 ffmpeg-full)。
"""
import argparse, json, os, subprocess, sys

def sec(ts):
    ts = ts.replace("，", ",")
    h, m, r = ts.split(":")
    s, ms = (r.split(",") + ["0"])[:2]
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def find_ffmpeg(cfg):
    for c in (cfg.get("ffmpeg"), "/usr/local/opt/ffmpeg-full/bin/ffmpeg",
              "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg", "ffmpeg"):
        if not c:
            continue
        try:
            subprocess.run([c, "-version"], capture_output=True, check=True)
            # 验证带 libass
            out = subprocess.run([c, "-hide_banner", "-version"], capture_output=True, text=True).stdout
            return c
        except Exception:
            continue
    sys.exit("找不到可用的 ffmpeg")

def find_font(cfg):
    import glob
    if cfg.get("font") and os.path.exists(cfg["font"]):
        return cfg["font"]
    for pat in ("/System/Library/AssetsV2/**/Yuanti.ttc",
                "/System/Library/Fonts/**/PingFang.ttc",
                "/System/Library/Fonts/STHeiti*.ttc"):
        hits = glob.glob(pat, recursive=True)
        if hits:
            return hits[0]
    return "/System/Library/Fonts/STHeiti Medium.ttc"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    FF = find_ffmpeg(cfg)
    FONT = find_font(cfg)
    SRC = os.path.expanduser(cfg["source_video"])          # 已烧字幕成片
    OUT = os.path.expanduser(cfg["output_dir"])
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, ".hooks"); os.makedirs(tmp, exist_ok=True)

    for i, clip in enumerate(cfg["clips"], 1):
        start = sec(clip["start"]); dur = round(sec(clip["end"]) - start, 3)
        hook = clip["hook"].replace("\\n", "\n")
        hookfile = os.path.join(tmp, f"hook_{i:02d}.txt")
        open(hookfile, "w", encoding="utf-8").write(hook)
        out = os.path.join(OUT, f"{clip['name']}.mp4")
        vf = (
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=22[bgb];"
            "[fg]scale=1080:-2[fg2];"
            "[bgb][fg2]overlay=(W-w)/2:(H-h)/2[v1];"
            f"[v1]drawtext=fontfile='{FONT}':textfile='{hookfile}':fontsize=66:fontcolor=white:"
            "borderw=5:bordercolor=black@0.85:line_spacing=14:x=(w-text_w)/2:y=210[vout]"
        )
        cmd = [FF, "-y", "-ss", f"{start}", "-i", SRC, "-t", f"{dur}",
               "-filter_complex", vf, "-map", "[vout]", "-map", "0:a:0",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
               "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            print(f"[{i}] ❌ {clip['name']}\n{r.stderr[-600:]}")
        else:
            print(f"[{i}] ✅ {clip['name']}.mp4  ({dur:.0f}s)")
    print("=== 切片完成 ===")

if __name__ == "__main__":
    main()
