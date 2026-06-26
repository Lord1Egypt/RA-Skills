"""
TikTok Dark Motivation Video - Full Pipeline (Pexels Edition)
Real stock footage from Pexels API — no AI image generation.

Usage:
  python pipeline_full.py --topic "discipline" --tone "dark & stoic" --duration 60 --theme "dark city rain"

Requirements:
  pip install requests Pillow moviepy pydub numpy
  brew install ffmpeg  (or apt install ffmpeg)
  Font: fonts/BebasNeue-Regular.ttf  (from fonts.google.com)

API Keys (set in .env or environment):
  ANTHROPIC_API_KEY
  ELEVENLABS_API_KEY
  PEXELS_API_KEY  (free at https://www.pexels.com/api/)
"""
import os, json, io, subprocess, argparse, requests, random
from pydub import AudioSegment
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ColorClip, TextClip,
    concatenate_videoclips, CompositeVideoClip, CompositeAudioClip
)

# ── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_KEY  = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
PEXELS_KEY     = os.getenv("PEXELS_API_KEY")

VIDEO_W, VIDEO_H = 1080, 1920
FPS = 30

VOICE_IDS = {
    "adam":   "pNInz6obpgDQGcFmaJgB",   # deep, authoritative
    "antoni": "ErXwobaYiN019PkySvjV",   # warm, intense
    "josh":   "TxGEqnHWrfWFTfGW9XjX",   # cinematic, dramatic
}

VOICE_SETTINGS = {
    "stability": 0.75,
    "similarity_boost": 0.85,
    "style": 0.30,
    "use_speaker_boost": True,
}

# Pexels search queries by visual theme
THEME_QUERIES = {
    "dark city rain": [
        "dark city rain night",
        "rain street cinematic night",
        "city lights bokeh rain",
        "dark alley rain noir",
    ],
    "lone warrior": [
        "lone person silhouette night",
        "person walking alone dark",
        "shadow warrior dark",
        "lone figure fog night",
    ],
    "dark nature": [
        "dark forest fog cinematic",
        "storm clouds dramatic sky",
        "night mountain silhouette",
        "dark ocean waves storm",
    ],
    "minimal shadow": [
        "shadow dark minimal",
        "dark room single light",
        "dramatic low key lighting portrait",
        "black shadow person cinematic",
    ],
}

SCRIPT_SYSTEM = """
You are a master motivational content writer for dark aesthetic TikTok videos.
Style like @vuongmilano: short, punchy, deep philosophical lines.
Dark, cinematic, poetic. Speaks to the isolated, driven person who wants to level up.

Rules:
- 8-15 lines maximum
- Each line max 8 words
- No filler words. Every word must hit hard.
- Lines build tension then release with power
- End with one unforgettable single-line closer
- Add [PAUSE] markers for dramatic silence

Return ONLY valid JSON (no markdown fences, no extra text):
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
"""

# ── STEP 1: SCRIPT ────────────────────────────────────────────────────────────

def generate_script(topic, tone, duration):
    print(f"  Topic: {topic} | Tone: {tone} | {duration}s")
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "system": SCRIPT_SYSTEM,
            "messages": [{"role": "user", "content": f"Topic: {topic}\nTone: {tone}\nDuration: {duration} seconds"}]
        }
    )
    r.raise_for_status()
    raw = r.json()["content"][0]["text"]
    script = json.loads(raw.replace("```json", "").replace("```", "").strip())
    print(f"  Title: {script['title']} | Lines: {len([l for l in script['lines'] if l['text'] != '[PAUSE]'])}")
    return script

# ── STEP 2: VOICEOVER ─────────────────────────────────────────────────────────

def generate_voiceover(script, voice_id, out_path="voice.mp3"):
    print(f"  Voice ID: {voice_id}")
    segments = []
    for line in script["lines"]:
        if line["text"] == "[PAUSE]":
            segments.append(AudioSegment.silent(duration=line["duration_ms"]))
            continue
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
            json={
                "text": line["text"],
                "model_id": "eleven_multilingual_v2",
                "voice_settings": VOICE_SETTINGS
            }
        )
        r.raise_for_status()
        segments.append(AudioSegment.from_mp3(io.BytesIO(r.content)))
        if line.get("pause_after_ms", 0) > 0:
            segments.append(AudioSegment.silent(duration=line["pause_after_ms"]))
    final = sum(segments)
    final.export(out_path, format="mp3")
    print(f"  Audio: {len(final)/1000:.1f}s saved")
    return out_path, len(final)

# ── STEP 3: PEXELS VIDEO FETCH ────────────────────────────────────────────────

def fetch_video_clips(theme, duration, output_dir="clips", script=None):
    """
    Search Pexels for real dark/cinematic video footage.
    Uses Claude-generated pexels_search_queries from script when available.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Prefer Claude's contextual queries over generic theme defaults
    queries = (script or {}).get("pexels_search_queries") or THEME_QUERIES.get(theme, THEME_QUERIES["dark city rain"])
    needed = max(3, duration // 15)
    collected = []

    for query in queries:
        if len(collected) >= needed:
            break
        print(f"  Pexels search: '{query}'")
        try:
            r = requests.get(
                "https://api.pexels.com/videos/search",
                headers={"Authorization": PEXELS_KEY},
                params={
                    "query": query,
                    "per_page": 6,
                    "orientation": "portrait",   # vertical preferred
                    "size": "medium",
                }
            )
            r.raise_for_status()
            videos = r.json().get("videos", [])
            random.shuffle(videos)   # variety across runs

            for video in videos:
                if len(collected) >= needed:
                    break
                # Select best quality MP4 >= 720px wide
                files = sorted(video.get("video_files", []), key=lambda f: f.get("width", 0), reverse=True)
                url = next(
                    (f["link"] for f in files if f.get("width", 0) >= 720 and "mp4" in f.get("file_type", "")),
                    files[0]["link"] if files else None
                )
                if not url:
                    continue

                clip_path = os.path.join(output_dir, f"clip_{len(collected):02d}.mp4")
                print(f"  Downloading {len(collected)+1}/{needed}: {video.get('duration','?')}s by {video.get('user',{}).get('name','?')}")

                # Stream download
                dl = requests.get(url, stream=True, timeout=90)
                dl.raise_for_status()
                with open(clip_path, "wb") as f:
                    for chunk in dl.iter_content(chunk_size=8192):
                        f.write(chunk)

                collected.append({
                    "path": clip_path,
                    "duration": video.get("duration", 10),
                    "pexels_id": video.get("id"),
                    "photographer": video.get("user", {}).get("name", "Pexels"),
                })

        except Exception as e:
            print(f"  Warning: '{query}' failed — {e}")
            continue

    if not collected:
        raise RuntimeError("No clips fetched from Pexels. Check PEXELS_API_KEY and network.")

    print(f"  Total clips: {len(collected)}")
    return collected

# ── STEP 4: COMPOSE ───────────────────────────────────────────────────────────

def crop_to_vertical(clip, w=VIDEO_W, h=VIDEO_H):
    """Scale and center-crop any clip to 9:16 vertical format."""
    clip = clip.resize(height=h)
    if clip.w < w:
        clip = clip.resize(width=w)
    return clip.crop(x_center=clip.w / 2, width=w).resize((w, h))


def compose_video(clips_info, audio_path, script, out="output.mp4", bg_music_path=None):
    print("  Loading audio...")
    audio = AudioFileClip(audio_path)
    total_dur = audio.duration

    # Build background from Pexels clips (loop pool if needed)
    print("  Preparing background...")
    pool = clips_info * 5
    parts, remaining = [], total_dur
    for info in pool:
        if remaining <= 0:
            break
        try:
            clip = VideoFileClip(info["path"], audio=False)
            clip = crop_to_vertical(clip)
            use_dur = min(clip.duration - 0.3, remaining)
            if use_dur <= 0.5:
                continue
            parts.append(clip.subclip(0, use_dur))
            remaining -= use_dur
        except Exception as e:
            print(f"  Skip clip: {e}")
    if not parts:
        raise RuntimeError("Could not load any video clips")
    bg = concatenate_videoclips(parts, method="compose").set_duration(total_dur)

    # Dark mood overlay — essential for the aesthetic
    dark = ColorClip((VIDEO_W, VIDEO_H), color=(0, 0, 0)).set_opacity(0.55).set_duration(total_dur)

    # Text overlays synced to script timing
    text_clips = []
    t = 0.0
    FONT_PATH = "fonts/BebasNeue-Regular.ttf"

    for line in script["lines"]:
        if line["text"] == "[PAUSE]":
            t += line["duration_ms"] / 1000
            continue
        dur = line["duration_ms"] / 1000
        kwargs = dict(fontsize=78, color="white", stroke_color="black", stroke_width=3,
                      size=(900, None), method="caption")
        try:
            clip = TextClip(line["text"], font=FONT_PATH, **kwargs)
        except Exception:
            clip = TextClip(line["text"], **kwargs)   # fallback: system font

        clip = (clip.set_duration(dur)
                    .crossfadein(0.25)
                    .crossfadeout(0.25)
                    .set_start(t)
                    .set_position("center"))
        text_clips.append(clip)
        t += dur + line.get("pause_after_ms", 0) / 1000

    # Ambient music (optional)
    if bg_music_path and os.path.exists(bg_music_path):
        mus = AudioFileClip(bg_music_path).volumex(0.08).set_duration(total_dur)
        final_audio = CompositeAudioClip([audio, mus])
    else:
        final_audio = audio

    print("  Rendering...")
    final = CompositeVideoClip([bg, dark] + text_clips).set_audio(final_audio)
    final.write_videofile(
        out, fps=FPS, codec="libx264", audio_codec="aac",
        bitrate="8000k", threads=4, preset="fast"
    )
    return out

# ── STEP 5: COLOR GRADE ───────────────────────────────────────────────────────

def color_grade(input_path, output_path):
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", (
            "curves=blue='0/0.05 1/1.1',"
            "eq=contrast=1.15:brightness=-0.04:saturation=0.60,"
            "vignette=PI/4,"
            "noise=alls=6:allf=t+u"
        ),
        "-c:v", "libx264", "-crf", "17",
        "-c:a", "copy",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FFmpeg warning (using ungraded): {result.stderr[-300:]}")
        import shutil; shutil.copy(input_path, output_path)
    return output_path

# ── MASTER PIPELINE ───────────────────────────────────────────────────────────

def create_motivation_video(
    topic, tone="dark & stoic", duration=60,
    visual_theme="dark city rain", voice="adam",
    output="motivation_video.mp4", bg_music_path=None
):
    voice_id = VOICE_IDS.get(voice.lower(), voice)
    print(f"\n{'='*50}")
    print(f"  DARK MOTIVATION VIDEO GENERATOR")
    print(f"  Topic: {topic} | {duration}s | {visual_theme}")
    print(f"{'='*50}\n")

    print("[1/5] Generating script (Claude)...")
    script = generate_script(topic, tone, duration)

    print("\n[2/5] Generating voiceover (ElevenLabs)...")
    audio_path, _ = generate_voiceover(script, voice_id)

    print("\n[3/5] Fetching real video clips (Pexels)...")
    clips = fetch_video_clips(visual_theme, duration, script=script)

    print("\n[4/5] Composing video (MoviePy)...")
    raw = compose_video(clips, audio_path, script, "raw_output.mp4", bg_music_path)

    print("\n[5/5] Color grading (FFmpeg)...")
    final = color_grade(raw, output)

    photographers = list(set(c["photographer"] for c in clips))
    print(f"\n{'='*50}")
    print(f"  DONE: {final}")
    print(f"  Hashtags : {' '.join(script['hashtags'])}")
    print(f"  Caption  : Video footage via Pexels ({', '.join(photographers)})")
    print(f"{'='*50}\n")
    return final, script

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create dark motivation TikTok video using Pexels footage")
    parser.add_argument("--topic",    default="silent discipline")
    parser.add_argument("--tone",     default="dark & stoic",
                        choices=["dark & stoic", "dark & aggressive", "dark & poetic"])
    parser.add_argument("--duration", type=int, default=60, choices=[30, 60, 90])
    parser.add_argument("--theme",    default="dark city rain",
                        choices=list(THEME_QUERIES.keys()))
    parser.add_argument("--voice",    default="adam", choices=list(VOICE_IDS.keys()))
    parser.add_argument("--output",   default="motivation_video.mp4")
    parser.add_argument("--music",    default=None, help="Optional background music path")
    args = parser.parse_args()

    create_motivation_video(
        topic=args.topic, tone=args.tone, duration=args.duration,
        visual_theme=args.theme, voice=args.voice,
        output=args.output, bg_music_path=args.music
    )
