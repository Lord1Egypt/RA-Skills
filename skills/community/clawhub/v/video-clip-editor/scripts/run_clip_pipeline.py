#!/usr/bin/env python3
"""
Full video clip pipeline.
Usage: python run_clip_pipeline.py --video ./movie.mp4 --vectcut-key YOUR_KEY
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path


# ── Dependency check ──────────────────────────────────────────────────────────
def check_dependencies(whisper_mode: str):
    missing = []
    try:
        import anthropic
    except ImportError:
        missing.append("anthropic")
    try:
        import requests
    except ImportError:
        missing.append("requests")
    if whisper_mode == "local":
        try:
            import whisper
        except ImportError:
            missing.append("openai-whisper")
    else:
        try:
            from openai import OpenAI
        except ImportError:
            missing.append("openai")

    if missing:
        print(f"Missing dependencies. Install with: pip install {' '.join(missing)} --break-system-packages")
        sys.exit(1)


# ── Step 1: Whisper transcription ─────────────────────────────────────────────
def transcribe_local(video_path: str, model_size: str = "medium", language: str = None) -> list:
    """Transcribe using a local Whisper model."""
    import whisper

    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    print(f"Transcribing: {video_path}")
    options = {"verbose": False, "word_timestamps": False}
    if language:
        options["language"] = language

    result = model.transcribe(video_path, **options)

    segments = [
        {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
        for s in result["segments"]
        if s["text"].strip()
    ]
    print(f"Transcription complete — {len(segments)} segments found.")
    return segments


def transcribe_api(video_path: str, api_key: str, language: str = None) -> list:
    """Transcribe using the OpenAI Whisper API."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    print(f"Calling OpenAI Whisper API: {video_path}")

    kwargs = {"model": "whisper-1", "response_format": "verbose_json",
              "timestamp_granularities": ["segment"]}
    if language:
        kwargs["language"] = language

    with open(video_path, "rb") as f:
        transcript = client.audio.transcriptions.create(file=f, **kwargs)

    segments = [
        {"start": s.start, "end": s.end, "text": s.text.strip()}
        for s in transcript.segments
        if s.text.strip()
    ]
    print(f"Transcription complete — {len(segments)} segments found.")
    return segments


# ── Step 2: Claude highlight identification ───────────────────────────────────
def identify_highlights(segments: list, highlight_count: int = 5,
                         clip_duration: int = 60, content_type: str = "general") -> list:
    """Use Claude to identify the best highlight clips."""
    import anthropic

    client = anthropic.Anthropic()

    transcript_text = "\n".join([
        f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}"
        for seg in segments
    ])

    total_duration = segments[-1]["end"] if segments else 0

    prompt = f"""You are a professional short-video editor. Your job is to identify the best clips from a longer video for standalone social media sharing.

Video duration: {total_duration:.0f}s ({total_duration/60:.1f} min)
Content type: {content_type}

Full transcript with timestamps:
{transcript_text}

Identify the {highlight_count} best clips for standalone sharing. Each clip should be approximately {clip_duration} seconds.

Selection criteria:
1. Emotional impact — tension, conflict, turning points, humor
2. Information density — key insights, quotable moments
3. Narrative completeness — a clear beginning and end, not abrupt
4. Shareability — the first line hooks the viewer immediately
5. Variety — clips should cover different content

Return ONLY valid JSON in this exact format, no markdown or extra text:
{{"highlights": [{{"start": 0.0, "end": 60.0, "title": "Clip title", "reason": "Why this clip was selected", "hook": "Opening hook line", "energy_level": "high"}}]}}

energy_level options: high / medium / low"""

    print(f"Claude is analyzing content to find {highlight_count} highlights...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip().replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    highlights = result["highlights"]

    print(f"Found {len(highlights)} highlights:")
    for i, h in enumerate(highlights, 1):
        print(f"  {i}. [{h['start']:.0f}s–{h['end']:.0f}s] {h['title']} — {h['reason']}")

    return highlights


# ── Step 3: vectcut-api draft generation ──────────────────────────────────────
def generate_draft(video_source: str, highlights: list, api_key: str,
                   style: str = "viral", ratio: str = "9:16") -> str:
    """Call vectcut-api to generate a CapCut draft. Returns draft_id."""
    import requests

    clips = [
        {
            "index": i,
            "source_start": round(h["start"], 3),
            "source_end": round(h["end"], 3),
            "title": h.get("title", f"Clip {i+1}"),
            "caption": h.get("hook", ""),
            "energy_level": h.get("energy_level", "medium"),
        }
        for i, h in enumerate(highlights)
    ]

    payload = {
        "video_source": video_source,
        "clips": clips,
        "template": {
            "style": style,
            "ratio": ratio,
            "resolution": "1080p",
            "caption_style": "subtitle_center",
            "transition": "fade",
            "bgm": "auto",
            "color_grade": "cinematic",
        },
        "export": {
            "format": "jianying_draft",
            "include_captions": True,
            "auto_color_grade": True,
            "generate_cover": True,
        }
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    print(f"Submitting vectcut-api job (style: {style}, ratio: {ratio})...")
    resp = requests.post("https://api.vectcut.com/v1/drafts/generate",
                         json=payload, headers=headers, timeout=30)
    resp.raise_for_status()

    draft_id = resp.json()["draft_id"]
    print(f"Job submitted. draft_id: {draft_id}")
    return draft_id


def poll_and_download(draft_id: str, api_key: str, output_path: str) -> str:
    """Poll for completion and download the draft."""
    import requests

    headers = {"Authorization": f"Bearer {api_key}"}
    print("Waiting for generation to complete...")

    for _ in range(72):  # up to 6 minutes
        resp = requests.get(f"https://api.vectcut.com/v1/drafts/{draft_id}/status",
                            headers=headers, timeout=10)
        status = resp.json()
        state = status.get("state", "unknown")
        progress = status.get("progress", 0)

        if state == "completed":
            print(f"\nGeneration complete!")
            dl_resp = requests.get(status["download_url"], stream=True, timeout=120)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                for chunk in dl_resp.iter_content(8192):
                    f.write(chunk)
            print(f"Draft saved: {output_path}")
            return output_path
        elif state == "failed":
            raise RuntimeError(f"Generation failed: {status.get('error', 'unknown error')}")
        else:
            print(f"\r  Progress: {progress}%  ", end="", flush=True)
            time.sleep(5)

    raise TimeoutError(f"Timed out. Query draft_id manually: {draft_id}")


# ── Timeline HTML preview ──────────────────────────────────────────────────────
def generate_timeline_html(highlights: list, total_duration: float, output_path: str):
    """Generate a visual timeline HTML preview."""
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
              "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"]

    bars = ""
    for i, h in enumerate(highlights):
        left = (h["start"] / total_duration) * 100
        width = ((h["end"] - h["start"]) / total_duration) * 100
        color = colors[i % len(colors)]
        title = h.get("title", f"Clip {i+1}")
        start_fmt = f"{int(h['start']//60)}:{int(h['start']%60):02d}"
        end_fmt = f"{int(h['end']//60)}:{int(h['end']%60):02d}"
        bars += (f'<div class="clip" style="left:{left:.1f}%;width:{width:.1f}%;'
                 f'background:{color};" title="{title}: {start_fmt} - {end_fmt}">'
                 f'<span>{i+1}</span></div>')

    clips_list = "".join([
        f'<div class="clip-item">'
        f'<span class="num" style="background:{colors[i%len(colors)]}">{i+1}</span>'
        f'<div><strong>{h.get("title","")}</strong>'
        f'<small>{int(h["start"]//60)}:{int(h["start"]%60):02d} – '
        f'{int(h["end"]//60)}:{int(h["end"]%60):02d} '
        f'({int(h["end"]-h["start"])}s)</small>'
        f'<p>{h.get("hook","")}</p></div></div>'
        for i, h in enumerate(highlights)
    ])

    total_min = int(total_duration // 60)
    total_sec = int(total_duration % 60)

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>Clip Timeline Preview</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #0f0f0f; color: #eee; }}
  h1 {{ color: #fff; font-size: 1.4em; }}
  .timeline-wrap {{ background: #1a1a1a; border-radius: 12px; padding: 20px; margin: 20px 0; }}
  .timeline {{ position: relative; height: 60px; background: #2a2a2a; border-radius: 8px; overflow: hidden; }}
  .clip {{ position: absolute; top: 8px; height: 44px; border-radius: 6px; opacity: 0.9; display: flex; align-items: center; justify-content: center; cursor: pointer; }}
  .clip:hover {{ opacity: 1; box-shadow: 0 0 0 2px white; }}
  .clip span {{ color: #000; font-weight: 700; font-size: 14px; }}
  .time-labels {{ display: flex; justify-content: space-between; color: #666; font-size: 12px; margin-top: 6px; }}
  .clips-list {{ display: flex; flex-direction: column; gap: 12px; margin-top: 20px; }}
  .clip-item {{ display: flex; gap: 12px; align-items: flex-start; background: #1a1a1a; padding: 14px; border-radius: 10px; }}
  .num {{ min-width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #000; font-size: 13px; }}
  .clip-item strong {{ display: block; margin-bottom: 2px; }}
  .clip-item small {{ color: #888; font-size: 12px; display: block; margin-bottom: 4px; }}
  .clip-item p {{ margin: 0; font-size: 13px; color: #aaa; font-style: italic; }}
</style></head>
<body>
<h1>Video Clip Timeline Preview</h1>
<p style="color:#888">Total: {total_min}m {total_sec}s | {len(highlights)} clips</p>
<div class="timeline-wrap">
  <div class="timeline">{bars}</div>
  <div class="time-labels">
    <span>0:00</span>
    <span>{int(total_duration//4//60)}:{int(total_duration//4%60):02d}</span>
    <span>{int(total_duration//2//60)}:{int(total_duration//2%60):02d}</span>
    <span>{int(total_duration*3//4//60)}:{int(total_duration*3//4%60):02d}</span>
    <span>{total_min}:{total_sec:02d}</span>
  </div>
</div>
<div class="clips-list">{clips_list}</div>
</body></html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Timeline preview saved: {output_path}")


# ── Main entry point ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Video clip pipeline")
    parser.add_argument("--video", required=True, help="Input video file path")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--highlights", type=int, default=5, help="Number of clips to extract")
    parser.add_argument("--duration", type=int, default=60, help="Target duration per clip (seconds)")
    parser.add_argument("--style", default="viral",
                        choices=["viral", "cinematic", "vlog", "interview"],
                        help="CapCut template style")
    parser.add_argument("--ratio", default="9:16", choices=["9:16", "16:9", "1:1"],
                        help="Output aspect ratio")
    parser.add_argument("--language", default=None, help="Transcription language code (e.g. en, zh, ja)")
    parser.add_argument("--content-type", default="general",
                        help="Content type hint (e.g. interview, documentary, standup)")
    parser.add_argument("--whisper-mode", default="local", choices=["local", "api"],
                        help="Whisper mode: local model or OpenAI API")
    parser.add_argument("--whisper-model", default="medium",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Local Whisper model size")
    parser.add_argument("--openai-key", default=os.environ.get("OPENAI_API_KEY"),
                        help="OpenAI API key (required for api mode)")
    parser.add_argument("--vectcut-key", default=os.environ.get("VECTCUT_API_KEY"),
                        help="vectcut API key")
    parser.add_argument("--skip-vectcut", action="store_true",
                        help="Skip vectcut — output highlights.json only")
    args = parser.parse_args()

    check_dependencies(args.whisper_mode)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"Video Clip Pipeline")
    print(f"{'='*50}")
    print(f"Input : {args.video}")
    print(f"Clips : {args.highlights} x ~{args.duration}s | Style: {args.style}")
    print(f"{'='*50}\n")

    # Step 1: Transcription (skip if cached)
    transcript_path = output_dir / "transcript.json"
    if transcript_path.exists():
        print(f"Found cached transcript, skipping transcription: {transcript_path}")
        with open(transcript_path) as f:
            segments = json.load(f)
    else:
        if args.whisper_mode == "local":
            segments = transcribe_local(args.video, args.whisper_model, args.language)
        else:
            if not args.openai_key:
                print("Error: --openai-key or OPENAI_API_KEY required for api mode.")
                sys.exit(1)
            segments = transcribe_api(args.video, args.openai_key, args.language)

        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        print(f"Transcript saved: {transcript_path}")

    if not segments:
        print("Error: transcript is empty. Check the video file.")
        sys.exit(1)

    # Step 2: Identify highlights
    highlights = identify_highlights(
        segments,
        highlight_count=args.highlights,
        clip_duration=args.duration,
        content_type=args.content_type
    )

    highlights_path = output_dir / "highlights.json"
    with open(highlights_path, "w", encoding="utf-8") as f:
        json.dump(highlights, f, ensure_ascii=False, indent=2)
    print(f"Highlights saved: {highlights_path}")

    total_duration = segments[-1]["end"] if segments else 0
    generate_timeline_html(highlights, total_duration, str(output_dir / "timeline_preview.html"))

    # Step 3: vectcut-api
    if args.skip_vectcut:
        print("\nSkipping vectcut. Pipeline complete.")
    elif not args.vectcut_key:
        print("\nNo --vectcut-key provided. Skipping draft generation.")
        print("highlights.json is ready — you can call vectcut-api manually.")
    else:
        draft_id = generate_draft(
            video_source=str(Path(args.video).absolute()),
            highlights=highlights,
            api_key=args.vectcut_key,
            style=args.style,
            ratio=args.ratio
        )
        draft_path = str(output_dir / "jianying_draft.zip")
        poll_and_download(draft_id, args.vectcut_key, draft_path)
        print(f"\nUnzip {draft_path} and use 'Import Draft' in CapCut to open it.")

    print(f"\n{'='*50}")
    print(f"Done! Output directory: {output_dir}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
