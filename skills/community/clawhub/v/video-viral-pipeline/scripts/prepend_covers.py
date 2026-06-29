#!/usr/bin/env python3
"""
把 <output_dir>/封面/<name>.jpg 作为 1.5 秒封面帧，拼到 <output_dir>/<name>.mp4 开头(替换原片)。
用法: python3 prepend_covers.py --config clips.json [--seconds 1.5]
"""
import argparse, json, os, subprocess, sys

def find_ffmpeg(cfg):
    for c in (cfg.get("ffmpeg"), "/usr/local/opt/ffmpeg-full/bin/ffmpeg",
              "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg", "ffmpeg"):
        if c and subprocess.run([c,"-version"],capture_output=True).returncode==0:
            return c
    sys.exit("找不到 ffmpeg")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--config",required=True)
    ap.add_argument("--seconds",type=float,default=1.5); a=ap.parse_args()
    cfg=json.load(open(a.config,encoding="utf-8")); FF=find_ffmpeg(cfg)
    OUT=os.path.expanduser(cfg["output_dir"]); COVER=os.path.join(OUT,"封面")
    D=a.seconds
    for i,clip in enumerate(cfg["clips"],1):
        name=clip["name"]; clip_mp4=os.path.join(OUT,f"{name}.mp4"); cover=os.path.join(COVER,f"{name}.jpg")
        if not (os.path.exists(clip_mp4) and os.path.exists(cover)):
            print(f"[{i}] 跳过 {name}(缺片或缺封面)"); continue
        tmp=os.path.join(OUT,f".{name}.tmp.mp4")
        vf=(f"[0:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[cv];"
            f"[1:v]fps=30,format=yuv420p,setsar=1[mv];[cv][mv]concat=n=2:v=1:a=0[outv];"
            f"anullsrc=cl=stereo:r=48000,atrim=0:{D},asetpts=PTS-STARTPTS[ca];"
            f"[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[ca][a1]concat=n=2:v=0:a=1[outa]")
        cmd=[FF,"-y","-loop","1","-t",f"{D}","-i",cover,"-i",clip_mp4,
             "-filter_complex",vf,"-map","[outv]","-map","[outa]",
             "-c:v","libx264","-preset","veryfast","-crf","23","-c:a","aac","-b:a","128k",
             "-movflags","+faststart",tmp]
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode: print(f"[{i}] ❌ {name}\n{r.stderr[-400:]}")
        else: os.replace(tmp,clip_mp4); print(f"[{i}] ✅ {name} 已加封面帧")
    print("=== 封面帧完成 ===")

if __name__=="__main__":
    main()
