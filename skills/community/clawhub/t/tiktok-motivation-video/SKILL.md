---
name: tiktok-motivation-video
description: >
  Full AI pipeline to create dark motivational TikTok/Reels videos using REAL video footage.
  Generates script (Claude), voiceover (ElevenLabs), searches real dark/cinematic video clips
  from Pexels API (no AI image generation), adds animated text overlays (MoviePy), color grading
  (FFmpeg), and exports final 1080x1920 MP4. Use this skill for: motivation video, dark aesthetic
  TikTok, pixel motivation reel, AI motivation video with voice, vuongmilano style video.
compatibility:
  required_apis:
    - Anthropic Claude API
    - ElevenLabs API
    - Pexels API (free real video footage — pexels.com/api)
    - FFmpeg
  python_packages: requests, Pillow, moviepy, pydub, numpy
---

# TikTok Dark-Motivation Video Skill

30-90 second vertical (9:16) dark motivational video — @vuongmilano style.

Pipeline: Script (Claude) + Voice (ElevenLabs) + Real Video (Pexels API) + Text (MoviePy) + Grade (FFmpeg)

IMPORTANT: All visuals come from Pexels API (real filmed stock footage).
Do NOT use FAL.ai, Replicate, or any AI image generator. Pexels only.

---

## Step 0 - Gather Inputs

- TOPIC: e.g. "discipline", "loneliness", "becoming your best self"
- TONE: dark & stoic | dark & aggressive | dark & poetic  (default: dark & stoic)
- DURATION: 30 | 60 | 90 seconds  (default: 60)
- VISUAL_THEME: dark city rain | lone warrior | dark nature | minimal shadow  (default: dark city rain)
- VOICE_ID: ElevenLabs voice  (default: Adam = pNInz6obpgDQGcFmaJgB)
- LANGUAGE: English | Vietnamese | bilingual

---

## Step 1 - Generate Script (Claude API)

System prompt produces JSON with lines, timings, AND Pexels search queries.

SYSTEM PROMPT:
  You are a master motivational content writer for dark aesthetic TikTok videos.
  Style like @vuongmilano: short, punchy, deep philosophical lines.
  Dark, cinematic, poetic. Speaks to the isolated, driven person who wants to level up.
  Rules: 8-15 lines max. Each line max 8 words. No filler. Every word hits hard.
  Build tension then release with power. End with one unforgettable closer.
  Add [PAUSE] markers for dramatic silence.
  Return ONLY valid JSON (no markdown fences):
  {
    "title": "...",
    "lines": [
      {"id": 1, "text": "...", "duration_ms": 3000, "pause_after_ms": 500},
      {"id": 2, "text": "[PAUSE]", "duration_ms": 1200, "pause_after_ms": 0}
    ],
    "total_duration_ms": 60000,
    "hashtags": ["#darkmotivation", "#discipline", "#fyp"],
    "pexels_search_queries": ["dark city rain night", "lone person walking", "shadow dramatic"]
  }

```python
import json, requests

def generate_script(topic, tone, duration, api_key):
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "system": SCRIPT_SYSTEM,
            "messages": [{"role": "user", "content": f"Topic: {topic}\nTone: {tone}\nDuration: {duration}s"}]
        }
    )
    raw = r.json()["content"][0]["text"]
    return json.loads(raw.replace("```json","").replace("```","").strip())
```

---

## Step 2 - Generate Voiceover (ElevenLabs)

Voice settings for dark motivation style:
  stability: 0.75, similarity_boost: 0.85, style: 0.30, use_speaker_boost: True
  model_id: eleven_multilingual_v2

Top voices:
  Adam   pNInz6obpgDQGcFmaJgB  deep, authoritative
  Antoni ErXwobaYiN019PkySvjV  warm, intense
  Josh   TxGEqnHWrfWFTfGW9XjX  cinematic, dramatic

```python
from pydub import AudioSegment
import io

def generate_voiceover(script, voice_id, api_key, out="voice.mp3"):
    segs = []
    for line in script["lines"]:
        if line["text"] == "[PAUSE]":
            segs.append(AudioSegment.silent(duration=line["duration_ms"]))
            continue
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            json={"text": line["text"], "model_id": "eleven_multilingual_v2",
                  "voice_settings": {"stability":0.75,"similarity_boost":0.85,"style":0.30,"use_speaker_boost":True}}
        )
        segs.append(AudioSegment.from_mp3(io.BytesIO(r.content)))
        if line.get("pause_after_ms", 0) > 0:
            segs.append(AudioSegment.silent(duration=line["pause_after_ms"]))
    final = sum(segs)
    final.export(out, format="mp3")
    return out, len(final)
```

---

## Step 3 - Fetch Real Video Clips (Pexels API)

Free API key at: https://www.pexels.com/api/

Default queries by theme:
```python
THEME_QUERIES = {
    "dark city rain":  ["dark city rain night", "rain street cinematic", "dark alley bokeh", "night city slow motion"],
    "lone warrior":    ["lone person silhouette night", "person walking alone dark", "shadow warrior", "lone figure darkness"],
    "dark nature":     ["dark forest fog cinematic", "storm clouds dramatic", "night mountain silhouette", "dark ocean storm"],
    "minimal shadow":  ["shadow dark minimal", "dark room single light", "dramatic low key lighting", "black shadow person"],
}
```

```python
import os

def fetch_video_clips(theme, duration, pexels_key, output_dir="clips", script=None):
    os.makedirs(output_dir, exist_ok=True)

    # Use Claude-generated queries if available, else use theme defaults
    queries = (script or {}).get("pexels_search_queries") or THEME_QUERIES.get(theme, THEME_QUERIES["dark city rain"])
    needed = max(3, duration // 15)
    collected = []

    for query in queries:
        if len(collected) >= needed:
            break
        print(f"  Pexels: searching '{query}'")
        r = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": pexels_key},
            params={"query": query, "per_page": 5, "orientation": "portrait", "size": "medium"}
        )
        for video in r.json().get("videos", []):
            if len(collected) >= needed:
                break
            # Pick best MP4 file >= 720px wide
            files = sorted(video.get("video_files", []), key=lambda f: f.get("width", 0), reverse=True)
            url = next((f["link"] for f in files if f.get("width",0)>=720 and "mp4" in f.get("file_type","")), None)
            if not url:
                continue
            path = os.path.join(output_dir, f"clip_{len(collected):02d}.mp4")
            with open(path, "wb") as f:
                for chunk in requests.get(url, stream=True, timeout=60).iter_content(8192):
                    f.write(chunk)
            collected.append({
                "path": path,
                "duration": video.get("duration", 10),
                "photographer": video.get("user", {}).get("name", "Pexels")
            })
            print(f"  Downloaded clip {len(collected)}/{needed}")

    if not collected:
        raise RuntimeError("No clips fetched. Check PEXELS_API_KEY.")
    return collected
```

Pexels notes:
- Free: 200 req/hour, 20,000/month
- orientation=portrait returns vertical-friendly clips
- Attribution required in TikTok caption: "Video footage via Pexels"
- Best keywords: dark, night, shadow, rain, fog, cinematic, dramatic, silhouette, alone

---

## Step 4 - Compose Video (MoviePy)

Crop all clips to 1080x1920 vertical. Layer dark overlay. Sync text to voice timing.

Font: Download Bebas Neue from fonts.google.com -> save as fonts/BebasNeue-Regular.ttf

```python
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ColorClip, TextClip,
    concatenate_videoclips, CompositeVideoClip, CompositeAudioClip
)

def crop_to_vertical(clip, w=1080, h=1920):
    clip = clip.resize(height=h)
    if clip.w < w:
        clip = clip.resize(width=w)
    return clip.crop(x_center=clip.w/2, width=w).resize((w, h))

def compose_video(clips_info, audio_path, script, out="output.mp4", bg_music_path=None):
    audio = AudioFileClip(audio_path)
    total_dur = audio.duration

    # Assemble background from Pexels clips
    pool = clips_info * 4
    parts, remaining = [], total_dur
    for info in pool:
        if remaining <= 0: break
        try:
            c = crop_to_vertical(VideoFileClip(info["path"], audio=False))
            dur = min(c.duration - 0.3, remaining)
            if dur <= 0: continue
            parts.append(c.subclip(0, dur))
            remaining -= dur
        except: continue
    if not parts:
        raise RuntimeError("No clips could be loaded")
    bg = concatenate_videoclips(parts, method="compose").set_duration(total_dur)

    # Dark overlay - essential for mood
    dark = ColorClip((1080,1920), color=(0,0,0)).set_opacity(0.55).set_duration(total_dur)

    # Text synced to script timing
    texts = []
    t = 0.0
    for line in script["lines"]:
        if line["text"] == "[PAUSE]":
            t += line["duration_ms"] / 1000
            continue
        dur = line["duration_ms"] / 1000
        try:
            clip = TextClip(line["text"], fontsize=78, font="fonts/BebasNeue-Regular.ttf",
                            color="white", stroke_color="black", stroke_width=3,
                            size=(900, None), method="caption")
        except:
            clip = TextClip(line["text"], fontsize=78, color="white",
                            stroke_color="black", stroke_width=3, size=(900,None), method="caption")
        texts.append(clip.set_duration(dur).crossfadein(0.25).crossfadeout(0.25).set_start(t).set_position("center"))
        t += dur + line.get("pause_after_ms", 0) / 1000

    if bg_music_path and os.path.exists(bg_music_path):
        mus = AudioFileClip(bg_music_path).volumex(0.08).set_duration(total_dur)
        final_audio = CompositeAudioClip([audio, mus])
    else:
        final_audio = audio

    CompositeVideoClip([bg, dark] + texts).set_audio(final_audio).write_videofile(
        out, fps=30, codec="libx264", audio_codec="aac", bitrate="8000k", threads=4, preset="fast"
    )
    return out
```

---

## Step 5 - Color Grade (FFmpeg)

```bash
ffmpeg -y -i output.mp4 \
  -vf "curves=blue='0/0.05 1/1.1',eq=contrast=1.15:brightness=-0.04:saturation=0.60,vignette=PI/4,noise=alls=6:allf=t+u" \
  -c:v libx264 -crf 17 -c:a copy final_video.mp4
```

Filters: blue tint shadow + darker contrast + vignette edges + film grain

---

## Master Pipeline

```python
import os, subprocess

def create_motivation_video(
    topic, tone="dark & stoic", duration=60,
    visual_theme="dark city rain", voice_id="pNInz6obpgDQGcFmaJgB",
    output="motivation_video.mp4", bg_music_path=None
):
    ak = os.getenv("ANTHROPIC_API_KEY")
    ek = os.getenv("ELEVENLABS_API_KEY")
    pk = os.getenv("PEXELS_API_KEY")

    print("[1/5] Script..."); script = generate_script(topic, tone, duration, ak)
    print("[2/5] Voice...");  audio, _ = generate_voiceover(script, voice_id, ek)
    print("[3/5] Pexels..."); clips = fetch_video_clips(visual_theme, duration, pk, script=script)
    print("[4/5] Compose..."); raw = compose_video(clips, audio, script, "raw.mp4", bg_music_path)
    print("[5/5] Grade...")
    subprocess.run([
        "ffmpeg","-y","-i",raw,"-vf",
        "curves=blue='0/0.05 1/1.1',eq=contrast=1.15:brightness=-0.04:saturation=0.60,vignette=PI/4",
        "-c:v","libx264","-crf","17","-c:a","copy", output
    ], check=True)
    print(f"\nDone: {output}")
    print(f"Tags: {' '.join(script['hashtags'])}")
    print("Caption: Video footage via Pexels")
    return output, script
```

---

## Setup

```bash
pip install requests Pillow moviepy pydub numpy
# macOS: brew install ffmpeg
# Ubuntu: apt install ffmpeg -y
# Font: fonts.google.com/specimen/Bebas+Neue -> fonts/BebasNeue-Regular.ttf

# .env
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=...
PEXELS_API_KEY=...       # free at pexels.com/api
```

## CLI

```bash
python scripts/pipeline_full.py --topic "discipline" --duration 60 --theme "dark city rain"
```

## Troubleshooting

  No Pexels results   -> Broaden queries; verify API key
  Landscape clips     -> crop_to_vertical() handles automatically
  Text desynced       -> Check timing uses /1000 (ms to seconds)
  Voice monotone      -> Lower stability 0.5, raise style 0.5
  Font error          -> Use full absolute path to .ttf file
  FFmpeg missing      -> brew install ffmpeg or apt install ffmpeg

## Best Pexels Keywords for Dark Motivation

  Discipline:  dark city rain, shadow silhouette night, person walking alone
  Loneliness:  lone figure fog, empty dark room, solitude night
  Rising up:   mountain storm clearing, dark dawn sky, fog path
  Villain arc: dramatic low key shadow, dark smoke motion, moody portrait
  Hustle:      night city timelapse, urban rain bokeh, dark street light

## References

  references/pexels_search_guide.md  - Full query list by mood
  references/elevenlabs_voices.md    - Voice catalog
  scripts/pipeline_full.py           - Complete runnable script
