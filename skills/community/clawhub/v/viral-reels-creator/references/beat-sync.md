# Beat-Synced Editing Reference

Sync video cuts to music beats for the single most powerful viral editing technique.
Beat-synced reels consistently outperform non-synced content by 2–4x on engagement.

---

## Core Concept

Every music track has:
- **BPM** (beats per minute) — determines cut frequency
- **Downbeats** — primary beats (1-2-3-4) — best for major cuts
- **Upbeats** — off-beats — good for quick flash cuts
- **Drop / Chorus** — highest energy section — save your best shot here

---

## Step 1: Get Beat Timestamps

### Method A: Use beat-detect.py (Automatic — Recommended)

```bash
# Requires: pip install librosa soundfile
python scripts/beat-detect.py music.mp3
# Output: beat_timestamps.txt with one timestamp per line
# Example output:
# 0.512
# 1.024
# 1.536
# 2.048 (drop detected here)
```

### Method B: Calculate from BPM (Manual)

If you know the BPM, calculate beat timestamps:

```python
bpm = 128  # beats per minute
offset = 0.2  # seconds until first beat (listen and measure)
beat_interval = 60 / bpm  # seconds between beats

beats = []
t = offset
while t < 30:  # for a 30s reel
    beats.append(round(t, 3))
    t += beat_interval

print(beats)
# [0.2, 0.669, 1.138, 1.607, 2.076, ...]
```

**Common BPMs and their beat intervals:**
| BPM | Beat interval | Cuts per 30s reel |
|-----|---------------|-------------------|
| 80  | 0.75s         | 40 cuts           |
| 100 | 0.60s         | 50 cuts           |
| 120 | 0.50s         | 60 cuts           |
| 128 | 0.469s        | 64 cuts           |
| 140 | 0.429s        | 70 cuts           |
| 160 | 0.375s        | 80 cuts           |

### Method C: ffmpeg Volume Peak Detection

Detect loud beats purely via audio analysis (no Python needed):

```bash
# Extract volume over time — peaks correspond to beats
ffmpeg -i music.mp3 -af "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level" \
  -f null - 2>&1 | grep "RMS_level" | head -60

# Better: use silencedetect inverted (loud sections)
ffmpeg -i music.mp3 -af "silencedetect=noise=-25dB:d=0.1" -f null - 2>&1 | grep "silence_"
```

---

## Step 2: Build Cut List from Beats

Given beat timestamps, assign each clip a duration matching beat multiples:

```python
# Example: 4 clips synced to beats at BPM=120 (0.5s per beat)
# Cut on every 2 beats (1 second per clip)

beat_timestamps = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
clips = ["clip1.mp4", "clip2.mp4", "clip3.mp4", "clip4.mp4", "clip5.mp4"]

# Assign clips to beat pairs
cut_plan = []
for i, clip in enumerate(clips):
    if i * 2 + 1 < len(beat_timestamps):
        start_beat = beat_timestamps[i * 2]
        end_beat = beat_timestamps[i * 2 + 2] if i * 2 + 2 < len(beat_timestamps) else beat_timestamps[-1] + 0.5
        cut_plan.append({
            "clip": clip,
            "reel_start": start_beat,
            "duration": end_beat - start_beat
        })

for cut in cut_plan:
    print(f"{cut['clip']} → play from {cut['reel_start']:.3f}s for {cut['duration']:.3f}s")
```

---

## Step 3: Assemble Beat-Synced Reel

### Single-Clip Beat Cuts

Cut a single long clip at beat timestamps:

```bash
# Given beats at: 0, 0.5, 1.0, 1.5, 2.0 (for first 2s)
# Cut on every 2 beats from different parts of source:

ffmpeg -i source.mp4 -i music.mp3 -filter_complex "
  [0:v]trim=10:11,setpts=PTS-STARTPTS[s1];
  [0:v]trim=25:26,setpts=PTS-STARTPTS[s2];
  [0:v]trim=40:41,setpts=PTS-STARTPTS[s3];
  [0:v]trim=55:56,setpts=PTS-STARTPTS[s4];
  [s1][s2][s3][s4]concat=n=4:v=1:a=0[v];
  [1:a]atrim=0:4,asetpts=PTS-STARTPTS[a]
" -map "[v]" -map "[a]" OUTPUT_FLAGS beat_reel.mp4
```

### Multi-Clip Beat Assembly (Python Generator)

```python
import subprocess
import json

# Your cut plan: (source_file, source_start, duration)
cut_plan = [
    ("clip1.mp4", 5.0,  0.5),   # beat 1
    ("clip2.mp4", 12.0, 0.5),   # beat 2
    ("clip3.mp4", 3.0,  1.0),   # beats 3-4 (hold for 2 beats)
    ("clip4.mp4", 18.5, 0.5),   # beat 5
    ("clip5.mp4", 7.2,  1.0),   # beats 6-7
    ("clip6.mp4", 22.0, 0.5),   # beat 8
]
music_file = "music.mp3"
output_file = "/mnt/user-data/outputs/beat_reel.mp4"

# Build ffmpeg command
inputs = [f"-i {src}" for src, _, _ in cut_plan] + [f"-i {music_file}"]
n_clips = len(cut_plan)

fc_parts = []
for i, (src, start, dur) in enumerate(cut_plan):
    fc_parts.append(f"[{i}:v]trim={start}:{start+dur},setpts=PTS-STARTPTS[v{i}];")

concat_inputs = "".join(f"[v{i}]" for i in range(n_clips))
fc_parts.append(f"{concat_inputs}concat=n={n_clips}:v=1:a=0[vout];")

total_dur = sum(dur for _, _, dur in cut_plan)
fc_parts.append(f"[{n_clips}:a]atrim=0:{total_dur},asetpts=PTS-STARTPTS[aout]")

fc = "\n".join(fc_parts)
cmd = (
    f"ffmpeg {' '.join(inputs)} "
    f'-filter_complex "{fc}" '
    f"-map [vout] -map [aout] "
    f"-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 "
    f"-c:a aac -ar 44100 -ac 2 -movflags +faststart {output_file}"
)
subprocess.run(cmd, shell=True)
```

---

## Step 4: Flash Cuts on Beat Drops

At the drop or chorus, add flash cuts (white/black frames on each beat):

```bash
# White flash on beat at t=8.0 and t=8.5 (the drop)
ffmpeg -i video.mp4 -filter_complex "
  fade=t=in:st=0:d=0.5,
  geq=r='if(between(t,8.0,8.05),255,r(X,Y))':g='if(between(t,8.0,8.05),255,g(X,Y))':b='if(between(t,8.0,8.05),255,b(X,Y))',
  geq=r='if(between(t,8.5,8.55),255,r(X,Y))':g='if(between(t,8.5,8.55),255,g(X,Y))':b='if(between(t,8.5,8.55),255,b(X,Y))'
" OUTPUT_FLAGS drop_flash.mp4
```

---

## Step 5: Zoom Pulse on Beat

Add a zoom pulse effect timed to each beat (very popular in Reels):

```bash
# Zoom pulse every 0.5s (120 BPM) — subtle zoom in-out
ffmpeg -i video.mp4 -filter_complex "
  zoompan=z='1+0.05*abs(sin(PI*t*2))':
    x='iw/2-(iw/zoom/2)':
    y='ih/2-(ih/zoom/2)':
    d=1:s=1080x1920:fps=30
" OUTPUT_FLAGS zoom_pulse.mp4
```

---

## Beat-to-Visual Sync Cheat Sheet

| Beat element          | Visual technique                   | ffmpeg approach          |
|-----------------------|------------------------------------|--------------------------|
| Every beat            | Hard cut to new clip               | concat with trim         |
| Every 2 beats         | Cut + quick zoom                   | concat + zoompan         |
| Every 4 beats         | Scene change with transition       | xfade transition         |
| Beat drop             | White flash + color grade change   | geq flash + eq change    |
| Build-up              | Slow zoom in, tension building     | zoompan zoom in          |
| Chorus                | Fast cuts, high saturation         | rapid concat + eq        |
| Outro/fade            | Blur out + fade to black           | avgblur + fade           |

---

## Advanced: Tempo Change / BPM Ramp

Speed-ramp to match a BPM change (e.g., drop goes from 100 to 130 BPM):

```bash
# Video speed increases 1.3x to match faster BPM after drop
ffmpeg -i video.mp4 -filter_complex "
  [0:v]trim=0:15,setpts=PTS-STARTPTS[pre];
  [0:v]trim=15:30,setpts=0.77*PTS[post];
  [pre][post]concat=n=2:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS tempo_ramp.mp4
```

---

## Quick Reference: Common Music Beat Patterns

```
4/4 time (most pop/EDM):  |1  2  3  4 | = cut on 1 and 3
Trap (hi-hat):            |1.0 1.5 2.0 2.5| = cut every 0.5 beats
Drill (slow):             |1   .   2   .  | = cut every beat
Latin (clave):            |1  .  2  .  3  | = 3/2 feel, cut on 1 and 3
```
