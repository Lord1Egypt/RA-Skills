#!/usr/bin/env python3
"""
TSW No-LTX Pipeline
====================
Quote → edge-tts audio → Pexels stock clips → MoviePy assembly → YouTube upload

No external video generation API needed. Fully self-contained.
"""

import os, sys, json, random, time, requests, subprocess, logging
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/projects/content/vanyan_video_factory')

# ── Config ──────────────────────────────────────────────────────────────────
QUOTE_LIBRARY   = "/root/.openclaw/workspace/projects/content/tsw_quote_library.json"
OUTPUT_DIR      = "/root/tsw_videos/noltx_output"
AUDIO_DIR       = "/root/tsw_videos/noltx_audio"
CLIP_CACHE_DIR  = "/root/tsw_videos/clip_library"
LOG_FILE        = "/root/.openclaw/workspace/agents/tsw/cron.log"
YT_UPLOADER     = "/root/.openclaw/workspace/projects/content/yt_uploader.py"
PEXELS_KEY      = "z4qzlGqn6cZzDpEzt6vsrLfxPXXVrGfDRJ7n3bB7xReXA53drnG0b3BD"

for d in [OUTPUT_DIR, AUDIO_DIR]:
    os.makedirs(d, exist_ok=True)

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [TSW-NOLTX] %(message)s",
    handlers=[logging.StreamHandler(),
              logging.FileHandler(LOG_FILE, mode='a')])
log = logging.getLogger("TSW")


def ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


# ── Stage 1: Pick a quote ────────────────────────────────────────────────────
def pick_quote():
    try:
        with open(QUOTE_LIBRARY) as f:
            library = json.load(f)
    except Exception as e:
        log.error(f"Quote library load failed: {e}")
        return None, None

    niche = random.choice(list(library.keys()))
    quotes = library.get(niche, [])
    if not quotes:
        return None, None

    quote_obj = random.choice(quotes)
    if isinstance(quote_obj, dict):
        author = quote_obj.get("author", "Unknown")
        text   = quote_obj.get("quote", quote_obj.get("text", ""))
    else:
        parts = str(quote_obj).split(" - ", 1)
        author = parts[0] if len(parts) > 1 else "Unknown"
        text   = parts[1] if len(parts) > 1 else parts[0]

    return niche, {"author": author, "text": text}


# ── Stage 2: Generate TTS ────────────────────────────────────────────────────
def generate_tts(text, author, audio_path):
    import asyncio, edge_tts

    script = f"{text}... — {author}."

    async def _gen():
        comm = edge_tts.Communicate(script, "en-US-GuyNeural", rate="-5%")
        await comm.save(audio_path)

    asyncio.run(_gen())
    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
        log.info(f"TTS generated: {os.path.getsize(audio_path)//1024}KB")
        return audio_path
    log.error("TTS failed or empty output")
    return None


# ── Stage 3: Get Pexels clips ────────────────────────────────────────────────
NICHE_QUERIES = {
    "sports_quotes":       ["sport athlete running", "basketball action", "soccer goal"],
    "motivational":        ["sunrise motivation", "mountain summit", "running success"],
    "business_quotes":     ["business office success", "entrepreneur laptop", "money finance"],
    "film_tv_quotes":      ["cinema film reel", "movie theater", "dramatic scene"],
    "wisdom_philosophy":   ["nature peaceful meditation", "stars galaxy", "ocean waves calm"],
    "political":           ["government building", "american flag", "crowd protest"],
    "science_tech":        ["technology futuristic", "circuit board", "space science"],
}

def get_pexels_clips(niche, count=3):
    queries = NICHE_QUERIES.get(niche, ["inspiration motivation success"])
    query   = random.choice(queries)
    clips   = []

    # Check cache first
    cache_dir = os.path.join(CLIP_CACHE_DIR, niche)
    if os.path.exists(cache_dir):
        cached = [os.path.join(cache_dir, f) for f in os.listdir(cache_dir) if f.endswith('.mp4')]
        if len(cached) >= count:
            random.shuffle(cached)
            log.info(f"Using {count} cached clips for niche: {niche}")
            return cached[:count]

    # Fetch from Pexels
    try:
        r = requests.get("https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_KEY},
            params={"query": query, "per_page": count + 2,
                    "orientation": "portrait", "size": "medium"},
            timeout=15)
        if r.status_code != 200:
            log.warning(f"Pexels {r.status_code} for '{query}'")
            # Fall back to any cached clips
            for cat_dir in os.listdir(CLIP_CACHE_DIR):
                cat_path = os.path.join(CLIP_CACHE_DIR, cat_dir)
                if os.path.isdir(cat_path):
                    files = [os.path.join(cat_path, f) for f in os.listdir(cat_path) if f.endswith('.mp4')]
                    clips.extend(files)
            random.shuffle(clips)
            return clips[:count]

        videos = r.json().get("videos", [])
        os.makedirs(os.path.join(CLIP_CACHE_DIR, niche), exist_ok=True)

        for vid in videos[:count]:
            # Pick best vertical file
            files = [vf for vf in vid.get("video_files", [])
                     if vf.get("height", 0) >= 720]
            files.sort(key=lambda x: x.get("height", 0))
            if not files:
                files = vid.get("video_files", [])
            if not files:
                continue
            vf = files[0]

            fpath = os.path.join(CLIP_CACHE_DIR, niche, f"pexels_{vid['id']}.mp4")
            if not os.path.exists(fpath):
                dl = requests.get(vf["link"], timeout=60, stream=True)
                with open(fpath, 'wb') as fp:
                    for chunk in dl.iter_content(32768):
                        fp.write(chunk)
                log.info(f"Downloaded clip: pexels_{vid['id']}.mp4")
            clips.append(fpath)
        return clips

    except Exception as e:
        log.error(f"Pexels fetch failed: {e}")
        return []


# ── Stage 4: Assemble video ──────────────────────────────────────────────────
def assemble_video(audio_path, clip_paths, quote_text, author, output_path):
    try:
        from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, ColorClip
        import numpy as np

        audio    = AudioFileClip(audio_path)
        duration = audio.duration

        # Build background from clips
        segments = []
        seg_dur  = duration / max(len(clip_paths), 1)
        for cp in clip_paths:
            try:
                c = VideoFileClip(cp).without_audio()
                # Crop to vertical 9:16
                if c.w / c.h > 9/16:
                    new_w = int(c.h * 9/16)
                    x1 = (c.w - new_w) // 2
                    c = c.cropped(x1=x1, y1=0, x2=x1+new_w, y2=c.h)
                c = c.resized((1080, 1920))
                c = c.subclipped(0, min(seg_dur, c.duration))
                c = c.with_duration(seg_dur)
                segments.append(c)
            except Exception as e:
                log.warning(f"Clip error {cp}: {e}")

        if not segments:
            log.error("No valid clips for assembly")
            return None

        bg = concatenate_videoclips(segments, method="compose")
        bg = bg.with_duration(duration)

        # Quote text overlay
        lines = []
        words  = quote_text.split()
        line   = []
        for w in words:
            line.append(w)
            if len(' '.join(line)) > 30:
                lines.append(' '.join(line))
                line = []
        if line:
            lines.append(' '.join(line))
        display_text = '\n'.join(lines) + f'\n\n— {author}'

        try:
            txt = TextClip(
                text=display_text,
                font_size=55,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                method='caption',
                size=(960, None),
                text_align='center',
            ).with_position('center').with_duration(duration)
            final = CompositeVideoClip([bg, txt])
        except Exception as e:
            log.warning(f"TextClip failed ({e}), using bg only")
            final = bg

        final = final.with_audio(audio)
        final.write_videofile(output_path, fps=30, codec='libx264',
                              audio_codec='aac', logger=None)
        log.info(f"Video assembled: {os.path.getsize(output_path)//1024//1024}MB")
        return output_path

    except Exception as e:
        log.error(f"Assembly failed: {e}")
        return None


# ── Stage 5: Upload to YouTube ───────────────────────────────────────────────
def upload_to_youtube(video_path, title, description):
    try:
        result = subprocess.run(
            ["python3", YT_UPLOADER, video_path, title, description],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            log.info(f"YouTube upload: {result.stdout.strip()[:200]}")
            return True
        else:
            log.warning(f"YouTube upload failed: {result.stderr.strip()[:200]}")
            return False
    except Exception as e:
        log.error(f"Upload error: {e}")
        return False


# ── Main ─────────────────────────────────────────────────────────────────────
def run():
    log.info("=" * 70)
    log.info("TSW NO-LTX PIPELINE START")
    log.info("=" * 70)

    # Stage 1: Pick quote
    niche, quote = pick_quote()
    if not quote:
        log.error("No quote available")
        return False

    log.info(f"Quote: {quote['author']} — {quote['text'][:60]}...")
    log.info(f"Niche: {niche}")

    slug      = f"tsw_{int(time.time())}"
    audio_path  = os.path.join(AUDIO_DIR, f"{slug}.mp3")
    output_path = os.path.join(OUTPUT_DIR, f"{slug}.mp4")

    # Stage 2: TTS
    log.info("Stage 2: Generating TTS audio...")
    if not generate_tts(quote['text'], quote['author'], audio_path):
        log.error("❌ TTS failed")
        return False

    # Stage 3: Get clips
    log.info("Stage 3: Fetching Pexels clips...")
    clips = get_pexels_clips(niche, count=4)
    if not clips:
        log.error("❌ No clips available")
        return False
    log.info(f"Got {len(clips)} clips")

    # Stage 4: Assemble
    log.info("Stage 4: Assembling video...")
    if not assemble_video(audio_path, clips, quote['text'], quote['author'], output_path):
        log.error("❌ Assembly failed")
        return False

    # Stage 5: Upload
    title = f'"{quote["text"][:60]}..." — {quote["author"]} #shorts #quotes #{niche}'
    desc  = f'{quote["text"]}\n\n— {quote["author"]}\n\n#quotes #motivation #shorts'
    log.info("Stage 5: Uploading to YouTube...")
    uploaded = upload_to_youtube(output_path, title, desc)

    if uploaded:
        log.info("✅ TSW pipeline complete — video uploaded!")
    else:
        log.info(f"✅ Video ready at {output_path} (upload failed — video saved)")

    return True


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
