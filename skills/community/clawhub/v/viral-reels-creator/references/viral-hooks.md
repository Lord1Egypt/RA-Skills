# Viral Hooks & Content Strategy Reference

Science-backed strategies for creating high-retention, shareable Reels.
The first 3 seconds determine everything — use these formulas to stop the scroll.

---

## The Viral Reel Formula

```
[0–3s]  HOOK        — Stop the scroll. Create pattern interrupt.
[3–7s]  SETUP       — Establish context. Deliver the promise.
[7–20s] CONTENT     — Core value. Quick cuts. Keep energy high.
[20–25s] PAYOFF     — Punchline, reveal, result, or transformation.
[25–30s] CTA        — Tell viewer what to do next.
```

**Cut pacing by content type:**
| Type         | Avg cut every | Hook length |
|--------------|---------------|-------------|
| Dance/Music  | 0.5–1s        | 1s          |
| Tutorial     | 3–5s          | 2–3s        |
| Comedy/Skit  | 1–3s          | 2s          |
| Travel/Vlog  | 2–4s          | 3s          |
| Product      | 2–3s          | 2s          |
| Talking Head | 3–5s          | 3s          |

---

## Opening Hook Formulas (First 3 Seconds)

### Formula 1: Bold Statement
Open with a controversial or surprising claim in text overlay.

```
Text overlay at t=0–3s:
"I made $10,000 doing THIS"
"Nobody talks about this trick"
"Stop using X — do this instead"
"This changed my life in 30 days"
```

**ffmpeg implementation:**
```bash
drawtext=text='Nobody talks about this trick':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=64:fontcolor=white:
  borderw=4:bordercolor=black:
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,0,3)'
```

### Formula 2: Pattern Interrupt
Start mid-action or with something visually unusual. Begin at the most interesting frame — not the beginning of the clip.

**Technique:** Use `scene-detect.py` to find the highest-energy frame, then trim to start there.

```bash
# Start 8 seconds in where the action peaks
ffmpeg -ss 00:00:08 -i input.mp4 -t 00:00:25 OUTPUT_FLAGS hooked_clip.mp4
```

### Formula 3: Question Hook
Open with a question that creates a curiosity gap.

```
"What would you do if..."
"Did you know that..."
"Why does nobody talk about..."
"How do [successful people] actually..."
```

### Formula 4: Before/After Promise
Show the end result first, then cut back to the beginning.

```bash
# Clip structure: result (3s) → process (20s) → result again (5s)
ffmpeg -i result.mp4 -i process.mp4 -filter_complex "
  [0:v]trim=0:3,setpts=PTS-STARTPTS[intro];
  [1:v]trim=0:20,setpts=PTS-STARTPTS[body];
  [0:v]trim=0:5,setpts=PTS-STARTPTS[outro];
  [intro][body][outro]concat=n=3:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS before_after.mp4
```

### Formula 5: Jump Cut Energy Opening
3 fast cuts in the first 2 seconds to signal high energy.

```bash
ffmpeg -i clip.mp4 -filter_complex "
  [0:v]trim=0:0.5,setpts=PTS-STARTPTS[c1];
  [0:v]trim=5:5.5,setpts=PTS-STARTPTS[c2];
  [0:v]trim=10:10.5,setpts=PTS-STARTPTS[c3];
  [0:v]trim=0:30,setpts=PTS-STARTPTS[main];
  [c1][c2][c3][main]concat=n=4:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS energy_open.mp4
```

---

## Retention Hook Placement

Viewers drop off at predictable timestamps. Place retention hooks to fight churn:

| Timestamp | Action                                  |
|-----------|-----------------------------------------|
| 0–3s      | Pattern interrupt / bold opening        |
| 7s        | "But wait..." — new information reveal  |
| 12s       | Visual change: zoom, cut, color shift   |
| 20s       | "Here's the part nobody tells you..."   |
| 25s       | Payoff or transformation reveal         |
| 28–30s    | CTA + loop back to beginning            |

**Loop trick** — end video so it seamlessly loops back to start. Viewers rewatch without realizing:
```bash
# Add cross-fade loop: last 1s fades into first 1s
ffmpeg -i video.mp4 -filter_complex "
  [0:v]trim=0:1,setpts=PTS-STARTPTS,fade=t=in:st=0:d=1[intro];
  [0:v]trim=1:28,setpts=PTS-STARTPTS[body];
  [0:v]trim=28:30,setpts=PTS-STARTPTS,fade=t=out:st=1:d=1[outro];
  [intro][body][outro]concat=n=3:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS loopable.mp4
```

---

## Trending Reel Formats

### 1. Transformation / Glow-Up
Structure: Before state → Process montage → After reveal

```
Opening text: "30 day transformation — watch till end"
Clips: before (3s) | day 1-10 fast cuts | day 20-30 fast cuts | final reveal (5s)
Caption: "Would you try this?" (CTA)
```

### 2. Tutorial / How-To (Value Bomb)
Structure: Hook → Steps → Result

```
Opening text: "Do this in 60 seconds"
Format: Numbered steps with text overlay per step
Tip: Show hands / screen — never just talking head for tutorials
Audio: Upbeat, medium tempo background music
```

**Step counter text overlay:**
```bash
# Step 1 at t=2, Step 2 at t=8, Step 3 at t=14...
drawtext=text='Step 1':fontsize=48:fontcolor=yellow:borderw=3:bordercolor=black:x=80:y=200:enable='between(t,2,8)',
drawtext=text='Step 2':fontsize=48:fontcolor=yellow:borderw=3:bordercolor=black:x=80:y=200:enable='between(t,8,14)',
drawtext=text='Step 3':fontsize=48:fontcolor=yellow:borderw=3:bordercolor=black:x=80:y=200:enable='between(t,14,20)'
```

### 3. Day-in-My-Life / Vlog
Structure: Morning → Highlight moments → Night wrap-up

```
Pacing: 2–3s per clip, max 15 clips for 30s reel
Music: Match energy to time of day
Hook: "My 5am routine that changed everything"
```

### 4. Reaction / Commentary
Structure: Show clip → Cut to reaction face → Commentary

```
Layout: Main clip (60% screen) + reaction face PiP (40% bottom corner)
Time reaction face appears exactly as the moment hits
```

**PiP reaction layout:**
```bash
ffmpeg -i main_clip.mp4 -i reaction_face.mp4 -filter_complex "
  [0:v]scale=1080:1920[bg];
  [1:v]scale=400:-1,format=rgba,colorchannelmixer=aa=0.9[face];
  [bg][face]overlay=W-w-20:H-h-200:enable='between(t,5,15)'
" OUTPUT_FLAGS reaction.mp4
```

### 5. POV / Storytelling
Structure: Set up scenario in text → Play out → Twist ending

```
Opening text: "POV: You just found out..."
No talking — tell story through captions + visuals + music
End with unexpected twist or punchline
```

### 6. Listicle / Countdown
Structure: "5 things you didn't know about X" with numbered reveals

```
Text pattern: big number first, then reveal, then next number
Numbers animate in with pop scale or bounce (see animations.md)
Hook: Always start with #5 or tease #1 in first 3s
```

**Number reveal animation:**
```bash
drawtext=text='#5':fontsize=160:fontcolor=white:borderw=6:bordercolor=black:
  fontsize='if(between(t,0,0.3),160*(1+0.4*sin(PI*t/0.3)),160)':
  x=(w-tw)/2:y=(h-th)/2:enable='between(t,0,3)'
```

### 7. Satisfying / ASMR Process
Structure: Slow reveal of process + satisfying end result

```
Audio: No music, use raw satisfying sounds OR lo-fi ambient
Pacing: Slower than usual — let each satisfying moment breathe (3–5s/clip)
Hook: Show the end result first (most satisfying frame)
Color: High contrast, vivid saturation (use Clarendon or Cyberpunk grade)
```

---

## Caption / Text Hook Psychology

### Curiosity Gap Phrases
Use these in first-3-second text overlays:

```
"...and this is why it works"       (mid-sentence hook)
"What happened next shocked me"      (narrative tension)
"I wish I knew this sooner"          (regret-based hook)
"The secret that [authority] hides"  (conspiracy framing)
"Most people don't know this"        (exclusivity)
"Do NOT do this until you see this"  (urgency)
"I tested this for 30 days..."       (commitment signal)
```

### Text Hierarchy for Viral Impact
```
Line 1 (largest, 72px+): HOOK WORD — single powerful word or number
Line 2 (medium, 48px):   Main claim or context
Line 3 (small, 32px):    Supporting detail or CTA

Example:
"WAIT"           ← 90px, yellow, center
"This trick"     ← 56px, white, center
"saves 2 hours"  ← 40px, white@0.8, center
```

---

## Music Selection Guide

| Content Type       | BPM Range  | Genre Suggestion         |
|--------------------|------------|--------------------------|
| Dance/Energy       | 120–140    | Pop, EDM, Hip-hop        |
| Chill/Aesthetic    | 70–90      | Lo-fi, Indie, Ambient    |
| Tutorial           | 90–110     | Upbeat instrumental      |
| Comedy             | 100–120    | Meme audio, viral sounds |
| Transformation     | 80–100     | Cinematic, emotional     |
| Product showcase   | 100–120    | Modern pop, trap         |
| Travel/Adventure   | 100–120    | Indie pop, folk-pop      |

**Sync tip:** Always cut clips on beat. Use `beat-detect.py` (see scripts/) to extract beat timestamps, then use those as cut points.

---

## Viral Caption (Text Post) Strategy

Always include on-screen text — 85% of viewers watch without sound.

**3-line caption formula:**
```
[HOOK LINE — makes them stop]
[VALUE LINE — what they get from watching]
[ENGAGEMENT LINE — question, CTA, or poll]

Example:
"This editing trick went viral 🔥"
"Took me 5 minutes using only free tools"
"Save this for later — you'll need it"
```

---

## Engagement Trigger Overlays

Add these at strategic timestamps to boost comments and shares:

```bash
# "Save this!" reminder at 15s
drawtext=text='Save this for later!':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=40:fontcolor=yellow:borderw=3:bordercolor=black:
  x=(w-tw)/2:y=h-th-100:
  enable='between(t,14,16)'

# "Part 2?" poll at end (25–30s)
drawtext=text='Want Part 2? Comment below':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=44:fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:y=h-th-120:
  enable='between(t,25,30)'

# Arrow pointing to like button
drawtext=text='Like if this helped!':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=36:fontcolor=0x00FF88:borderw=2:bordercolor=black:
  x=(w-tw)/2:y=h-th-80:
  enable='between(t,28,30)'
```

---

## Finding Viral Moments in Raw Footage

Use `scripts/scene-detect.py` to:
1. Analyze raw footage for high-motion/high-energy scenes
2. Extract timestamps of most visually interesting frames
3. Auto-rank clips by "potential virality" (sharpness + motion + brightness)

Quick manual approach with ffmpeg scene detection:
```bash
# Find scene changes (output: timestamps where new scenes start)
ffmpeg -i raw_footage.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep "pts_time"

# Lower threshold (0.2) = more scene changes detected
# Higher threshold (0.4) = only major cuts
```

Extract the best 30s from a long video:
```bash
# Find the segment with the most scene changes (= highest energy)
ffprobe -v quiet -show_entries frame=pkt_pts_time,best_effort_timestamp_time \
  -select_streams v -of csv input.mp4 | head -100
```
