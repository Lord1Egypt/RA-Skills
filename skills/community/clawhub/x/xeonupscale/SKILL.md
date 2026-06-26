---
name: xeonupscale
description: "ffmpeg lanczos video upscale skill. Resizes a video to a higher resolution (e.g. 480p→540p, 480p→1080p) using libx264 + lanczos scaler. Bundles a static ffmpeg from BtbN/FFmpeg-Builds so no system ffmpeg is needed. Use for: video upscale, video resize, change resolution, scale video, lanczos, upscaling, 视频放大, 视频缩放, 视频升分辨率, 480p to 1080p, bilinear/bicubic alternative."
allowed-tools: Bash(./upscale.sh *), Bash(bash upscale.sh *), Bash(./ffmpeg/ffmpeg *)
metadata:
  openclaw:
    requires:
      bins: [bash, curl, tar]
---

# xeonupscale

Video upscale via `ffmpeg ... -vf scale=W:H:flags=lanczos` + `libx264 -crf 18`.
Static ffmpeg binary lives in `./ffmpeg/ffmpeg` after install (no apt needed).

Source: `/home/node/.openclaw/workspace/skills/xeonupscale/`
GitHub: <https://github.com/Wray151/xeonupscale>

## TL;DR
```bash
cd /home/node/.openclaw/workspace/skills/xeonupscale
./upscale.sh in.mp4 540p                       # → in_960x540.mp4
./upscale.sh in.mp4 1080p out.mp4
./upscale.sh in.mp4 1920x1080                  # 自定义分辨率
```

"syntax OK": `540p` / `720p` / `1080p` / `1440p` / `2160p|4k`，或直接 `WxH`。
