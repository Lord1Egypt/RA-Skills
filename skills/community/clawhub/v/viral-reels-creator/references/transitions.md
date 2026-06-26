# Transitions Reference — 12+ Video Transitions

All transitions work between two clips. Each assumes:
- **clip1**: first video (outgoing)
- **clip2**: second video (incoming)
- **OVERLAP**: duration of transition in seconds (typically 0.5–1.5s)
- Both clips are pre-normalized to 1080×1920, 30fps, same codec

---

## Pre-Normalization (run for every clip first)

```bash
ffmpeg -i clipN.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 norm_clipN.mp4
```

---

## Transition 1: Cross Dissolve (Fade)

```bash
OVERLAP=1
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=5,setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1];
  [v0]fade=t=out:st=4:d=${OVERLAP}[v0f];
  [v1]fade=t=in:st=0:d=${OVERLAP}[v1f];
  [v0f][v1f]overlay=enable='gte(t,4)'[v];
  [0:a]atrim=duration=5,asetpts=PTS-STARTPTS,afade=t=out:st=4:d=${OVERLAP}[a0];
  [1:a]atrim=duration=5,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=${OVERLAP}[a1];
  [a0][a1]acrossfade=d=${OVERLAP}[a]
" -map "[v]" -map "[a]" OUTPUT_FLAGS output.mp4
```

---

## Transition 2: Dip to Black

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=5,setpts=PTS-STARTPTS,fade=t=out:st=4:d=0.5[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.5[v1];
  [v0][v1]concat=n=2:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 3: Dip to White

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=5,setpts=PTS-STARTPTS,fade=t=out:st=4:d=0.5:color=white[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.5:color=white[v1];
  [v0][v1]concat=n=2:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 4: Wipe Left

```bash
OVERLAP=1
DUR1=5
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=${DUR1},setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1];
  [v0][v1]overlay=x='if(between(t,${DUR1}-${OVERLAP},${DUR1}),W-W*(t-(${DUR1}-${OVERLAP}))/${OVERLAP},W)':y=0[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 5: Wipe Right

```bash
OVERLAP=1
DUR1=5
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=${DUR1},setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1];
  [v0][v1]overlay=x='if(between(t,${DUR1}-${OVERLAP},${DUR1}),-W+W*(t-(${DUR1}-${OVERLAP}))/${OVERLAP},-W)':y=0[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 6: Wipe Up

```bash
OVERLAP=1
DUR1=5
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=${DUR1},setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1];
  [v0][v1]overlay=x=0:y='if(between(t,${DUR1}-${OVERLAP},${DUR1}),H-H*(t-(${DUR1}-${OVERLAP}))/${OVERLAP},H)':shortest=1[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 7: Wipe Down

```bash
OVERLAP=1
DUR1=5
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=${DUR1},setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1];
  [v0][v1]overlay=x=0:y='if(between(t,${DUR1}-${OVERLAP},${DUR1}),-H+H*(t-(${DUR1}-${OVERLAP}))/${OVERLAP},-H)':shortest=1[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 8: Zoom In Transition

```bash
OVERLAP=1
DUR1=5
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=${DUR1},setpts=PTS-STARTPTS,
    zoompan=z='if(between(on,(${DUR1}-${OVERLAP})*30,${DUR1}*30),min(zoom+0.02,2.0),1.0)':
    x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,
    fade=t=out:st=$((DUR1-OVERLAP)):d=${OVERLAP}[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS,fade=t=in:st=0:d=${OVERLAP}[v1];
  [v0][v1]overlay=enable='gte(t,$((DUR1-OVERLAP)))'[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 9: Zoom Out Transition

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=5,setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1];
  [v0][v1]xfade=transition=smoothup:duration=1:offset=4[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 10: Spin / Rotate

```bash
OVERLAP=0.8
DUR1=5
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=${DUR1},setpts=PTS-STARTPTS,
    rotate='if(between(t,${DUR1}-${OVERLAP},${DUR1}),2*PI*(t-${DUR1}+${OVERLAP})/${OVERLAP},0):c=black:ow=1080:oh=1920',
    fade=t=out:st=$((DUR1-1)):d=${OVERLAP}[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.3[v1];
  [v0][v1]concat=n=2:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 11: Glitch Cut

```bash
DUR1=5
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=${DUR1},setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1raw];
  [v1raw]split=3[v1r][v1g][v1b];
  [v1r]lutrgb=g=0:b=0,crop=w=iw-8:h=ih:x=8:y=0,pad=iw+8:ih:0:0[red];
  [v1g]lutrgb=r=0:b=0[green];
  [v1b]lutrgb=r=0:g=0,crop=w=iw-8:h=ih:x=0:y=0,pad=iw+8:ih:8:0[blue];
  [green][red]blend=all_mode=addition[rg];
  [rg][blue]blend=all_mode=addition,trim=duration=0.15,setpts=PTS-STARTPTS[glitch];
  [1:v]trim=start=0.15,setpts=PTS-STARTPTS[v1clean];
  [v0][glitch][v1clean]concat=n=3:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Transition 12: Blur Dissolve

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=5,setpts=PTS-STARTPTS,
    avgblur='if(gt(t,4),ceil(30*(t-4)),0)':planes=0xF,
    fade=t=out:st=4.5:d=0.5[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS,
    avgblur='if(lt(t,1),ceil(30*(1-t)),0)':planes=0xF,
    fade=t=in:st=0:d=0.5[v1];
  [v0][v1]concat=n=2:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Using xfade (ffmpeg 4.3+) — Built-in Transitions

```bash
# Available xfade transitions:
# fade, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright,
# slideup, slidedown, circlecrop, rectcrop, distance, fadeblack,
# fadewhite, radial, smoothleft, smoothright, smoothup, smoothdown,
# circleopen, circleclose, vertopen, vertclose, horzopen, horzclose,
# dissolve, pixelize, diagtl, diagtr, diagbl, diagbr, hlslice, hrslice,
# vuslice, vdslice, squeezeh, squeezev, zoomin, fadegrays, wipetl,
# wipetr, wipebl, wipebr, coverleft, coverright, coverup, coverdown,
# revealup, revealdown, revealleft, revealright

ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]trim=duration=5,setpts=PTS-STARTPTS[v0];
  [1:v]trim=duration=5,setpts=PTS-STARTPTS[v1];
  [v0][v1]xfade=transition=circleopen:duration=1:offset=4[v]
" -map "[v]" OUTPUT_FLAGS output.mp4
```

---

## Multi-Clip Transition Pipeline (3+ clips)

```python
import subprocess

clips = ["clip1.mp4", "clip2.mp4", "clip3.mp4", "clip4.mp4"]
transition = "fade"
trans_dur = 1
clip_dur = 5

inputs = " ".join(f"-i {c}" for c in clips)
fc_parts = []

for i, clip in enumerate(clips):
    fc_parts.append(f"[{i}:v]trim=duration={clip_dur},setpts=PTS-STARTPTS[v{i}];")

prev = "v0"
for i in range(1, len(clips)):
    offset = clip_dur - trans_dur
    out = f"xf{i}" if i < len(clips) - 1 else "vout"
    fc_parts.append(f"[{prev}][v{i}]xfade=transition={transition}:duration={trans_dur}:offset={offset}[{out}];")
    prev = out

fc = "\n".join(fc_parts).rstrip(";")
cmd = f'ffmpeg {inputs} -filter_complex "{fc}" -map "[vout]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -movflags +faststart output.mp4'
subprocess.run(cmd, shell=True)
```

---

## Transition Selection Guide

| Mood / Content     | Recommended Transitions              |
|--------------------|--------------------------------------|
| Professional       | Cross Dissolve, Dip to Black         |
| Energetic / Fun    | Wipe, Slide, Glitch Cut             |
| Cinematic          | Dip to Black, Blur Dissolve, Zoom   |
| Travel / Vlog      | Cross Dissolve, Zoom, Spin          |
| Music / Dance      | Glitch Cut, Hard Cut, Flash (white) |
| Tutorial           | Wipe Left, Slide Up                 |
| Storytelling       | Dip to Black, Blur Dissolve         |
