#!/usr/bin/env python3
"""
按 clips 配置给每条片段生成一张 9:16 封面图(取干净无字幕源帧 + 暗化 + 大标题 + 系列标签)。
输出到 <output_dir>/封面/<name>.jpg

用法: python3 render_covers.py --config clips.json
"""
import argparse, json, os, subprocess, sys, glob

def sec(ts):
    ts = ts.replace("，", ",")
    h, m, r = ts.split(":"); s, ms = (r.split(",") + ["0"])[:2]
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

def find_ffmpeg(cfg):
    for c in (cfg.get("ffmpeg"), "/usr/local/opt/ffmpeg-full/bin/ffmpeg",
              "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg", "ffmpeg"):
        if c and subprocess.run([c,"-version"],capture_output=True).returncode==0:
            return c
    sys.exit("找不到 ffmpeg")

def find_font(cfg):
    if cfg.get("font") and os.path.exists(cfg["font"]): return cfg["font"]
    for pat in ("/System/Library/AssetsV2/**/Yuanti.ttc","/System/Library/Fonts/**/PingFang.ttc"):
        h=glob.glob(pat,recursive=True)
        if h: return h[0]
    return "/System/Library/Fonts/STHeiti Medium.ttc"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--config",required=True); a=ap.parse_args()
    cfg=json.load(open(a.config,encoding="utf-8"))
    FF=find_ffmpeg(cfg); FONT=find_font(cfg)
    CLEAN=os.path.expanduser(cfg.get("clean_video") or cfg["source_video"])  # 优先无字幕源
    OUT=os.path.expanduser(cfg["output_dir"]); COVER=os.path.join(OUT,"封面"); os.makedirs(COVER,exist_ok=True)
    tmp=os.path.join(OUT,".covertxt"); os.makedirs(tmp,exist_ok=True)
    tag=cfg.get("series_tag","")
    tagfile=os.path.join(tmp,"tag.txt"); open(tagfile,"w",encoding="utf-8").write(tag)

    for i,clip in enumerate(cfg["clips"],1):
        title=clip.get("cover_title", clip["hook"]).replace("\\n","\n")
        frac=float(clip.get("cover_frac",0.45))
        t=sec(clip["start"])+(sec(clip["end"])-sec(clip["start"]))*frac
        tf=os.path.join(tmp,f"title_{i:02d}.txt"); open(tf,"w",encoding="utf-8").write(title)
        out=os.path.join(COVER,f"{clip['name']}.jpg")
        vf=("[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=24,eq=brightness=-0.06[bgb];"
            "[fg]scale=1080:-2[fg2];[bgb][fg2]overlay=(W-w)/2:(H-h)/2[base];"
            "[base]drawbox=x=0:y=1240:w=1080:h=680:color=black@0.55:t=fill[band];"
            f"[band]drawtext=fontfile='{FONT}':textfile='{tagfile}':fontsize=40:fontcolor=white@0.9:"
            "borderw=3:bordercolor=black@0.7:x=(w-text_w)/2:y=70[tag];"
            "[tag]drawbox=x=(iw-150)/2:y=1360:w=150:h=10:color=yellow@0.95:t=fill[bar];")
        vf+=(f"[bar]drawtext=fontfile='{FONT}':textfile='{tf}':fontsize=108:fontcolor=white:"
             "borderw=6:bordercolor=black@0.85:line_spacing=20:x=(w-text_w)/2:y=1420[vout]")
        cmd=[FF,"-y","-ss",f"{t}","-i",CLEAN,"-frames:v","1","-filter_complex",vf,"-map","[vout]","-q:v","2",out]
        r=subprocess.run(cmd,capture_output=True,text=True)
        print(f"[{i}] {'✅' if r.returncode==0 else '❌ '+r.stderr[-300:]} {clip['name']}.jpg")
    print("=== 封面完成 ===")

if __name__=="__main__":
    main()
