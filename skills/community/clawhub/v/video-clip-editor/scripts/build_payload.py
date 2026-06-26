#!/usr/bin/env python3
"""
build_payload.py
Core clip analysis:
  - Importance scoring (0.0-1.0) per dialogue segment
  - Koubo (jump-cut) filler/pause removal
  - Silent segment detection
  - Qwen-VL-Plus visual narration (with rule-based fallback)
  - 90-second budget enforcement
  - vectcut-api payload builder
"""
import base64
import json
import os
import re
import subprocess
import tempfile
from math import gcd
from pathlib import Path

# ── API Keys ───────────────────────────────────────────────────────────────────
# Set your keys here. env vars are used as fallback if left as None.
QWEN_API_KEY = None   # DashScope key for Qwen-VL-Plus, e.g. "sk-xxxxxxxxxxxx"
               # fallback: os.environ.get("QWEN_API_KEY")

# ── Constants ──────────────────────────────────────────────────────────────────
MAX_OUTPUT_SECONDS   = 90
MIN_SILENCE_GAP      = 1.5   # gap between Whisper segments to flag as silent
KOUBO_PAUSE_THRESH   = 0.5   # pause longer than this is cut within a sentence
MIN_CLIP_DURATION    = 0.8   # seconds
MAX_CLIP_DURATION    = 5.0   # seconds (per individual sub-cut)

FILLER_WORDS = {
    "um", "uh", "like", "you know", "so", "right", "okay",
    "well", "basically", "literally", "actually", "i mean",
    "kind of", "sort of"
}
HIGH_IMPORTANCE_WORDS = {
    "announced", "confirmed", "revealed", "breaking", "never", "always",
    "important", "critical", "secret", "truth", "finally", "shocked",
    "incredible", "amazing", "warning", "must", "key", "proven"
}


# ── Character map ──────────────────────────────────────────────────────────────
def build_character_map(characters: list) -> dict:
    return {c["id"]: c["name"] for c in (characters or [])}


# ── Importance scoring (0.0 – 1.0) ───────────────────────────────────────────
def score_segment(segment: dict) -> float:
    """
    Score a spoken segment for editorial importance.
    > 0.7 → keep full + preserve audio
    0.4-0.7 → trim with koubo cuts
    < 0.4 → drop or heavily cut
    """
    text = segment.get("text", "").lower()
    score = 0.4  # baseline

    # High-importance keywords
    hits = sum(1 for w in HIGH_IMPORTANCE_WORDS if w in text)
    score += min(hits * 0.1, 0.3)

    # Emotional punctuation
    if text.rstrip().endswith("!"):
        score += 0.15
    if text.rstrip().endswith("?"):
        score += 0.05

    # Duration sweet spot (3–8s feels most natural)
    dur = segment["end"] - segment["start"]
    if 3.0 <= dur <= 8.0:
        score += 0.1
    elif dur < 1.5:
        score -= 0.15  # too short, likely noise

    # Cap to 0.0 – 1.0
    return round(max(0.0, min(1.0, score)), 3)


# ── Silence detection ──────────────────────────────────────────────────────────
def detect_silent_segments(segments: list, video_duration: float = 0) -> list:
    enriched = []
    prev_end = 0.0

    for seg in segments:
        gap = seg["start"] - prev_end
        if gap > MIN_SILENCE_GAP:
            enriched.append({
                "id": f"silent_{len(enriched)}",
                "start": prev_end, "end": seg["start"],
                "text": "", "is_silent": True,
                "silent_duration": round(gap, 3),
                "speaker_id": None, "speaker_name": None
            })
        enriched.append({**seg, "is_silent": False})
        prev_end = seg["end"]

    if video_duration and video_duration - prev_end > MIN_SILENCE_GAP:
        enriched.append({
            "id": "silent_end",
            "start": prev_end, "end": video_duration,
            "text": "", "is_silent": True,
            "silent_duration": round(video_duration - prev_end, 3),
            "speaker_id": None, "speaker_name": None
        })
    return enriched


# ── Koubo (jump-cut) analysis ─────────────────────────────────────────────────
def apply_koubo_cuts(segment: dict) -> list:
    """Return list of micro-cuts to apply within the segment."""
    cuts = []
    text = segment.get("text", "").lower()
    words = text.split()
    if not words:
        return cuts

    seg_start = segment["start"]
    seg_dur = segment["end"] - seg_start
    time_per_word = seg_dur / len(words)
    cursor = seg_start

    for word in words:
        clean = re.sub(r"[^a-z ]", "", word).strip()
        if clean in FILLER_WORDS:
            cuts.append({
                "remove_start": round(cursor, 3),
                "remove_end": round(cursor + time_per_word * 1.2, 3),
                "reason": f"filler: '{clean}'"
            })
        cursor += time_per_word

    return cuts


# ── Qwen-VL-Plus visual narration ─────────────────────────────────────────────
# DashScope OpenAI-compatible endpoint
QWEN_VL_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_VL_MODEL    = "qwen-vl-plus"


def describe_frame_qwen(frame_path: str, context_before: str,
                         context_after: str, api_key: str) -> str:
    """
    Call Qwen-VL-Plus (DashScope) to describe a video frame.
    Uses the OpenAI-compatible API — no extra SDK needed beyond openai.
    Returns a 1-2 sentence narration string.
    """
    try:
        from openai import OpenAI
    except ImportError:
        import subprocess, sys
        subprocess.run([sys.executable, "-m", "pip", "install", "openai",
                        "--break-system-packages", "-q"], check=True)
        from openai import OpenAI

    with open(frame_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    client = OpenAI(api_key=api_key, base_url=QWEN_VL_BASE_URL)
    prompt = (
        f"Describe what is happening in this video frame in 1-2 sentences (max 15 words). "
        f"Context before this scene: \"{context_before[-80:]}\". "
        f"Context after: \"{context_after[:80]}\". "
        f"Be specific about visible actions, expressions, and objects."
    )
    response = client.chat.completions.create(
        model=QWEN_VL_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return response.choices[0].message.content.strip()


def extract_frame(video_path: str, timestamp: float, output_path: str):
    """Extract a single frame from the video at `timestamp` seconds."""
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(timestamp),
        "-i", video_path, "-vframes", "1",
        "-q:v", "2", output_path
    ], capture_output=True, check=True)


def generate_narration(silent_seg: dict, context_before: str, context_after: str,
                        video_path: str = None) -> str:
    """
    Generate narration for a silent segment.
    Uses Qwen-VL-Plus (global QWEN_API_KEY) if video_path is provided.
    Falls back to rule-based otherwise.
    """
    resolved_key = QWEN_API_KEY or os.environ.get('QWEN_API_KEY')
    if video_path and resolved_key:
        try:
            midpoint = (silent_seg["start"] + silent_seg["end"]) / 2
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                frame_path = tmp.name
            extract_frame(video_path, midpoint, frame_path)
            narration = describe_frame_qwen(frame_path, context_before,
                                            context_after, resolved_key)
            Path(frame_path).unlink(missing_ok=True)
            return narration
        except Exception as e:
            print(f"  Qwen-VL-Plus failed ({e}), falling back to rule-based.")

    # Rule-based fallback
    duration = silent_seg.get("silent_duration", 0)
    if duration < 3:
        last = context_before.strip().split()[-6:]
        return f"[Pause after: '{' '.join(last)}']" if last else "[Beat]"
    elif duration < 8:
        first = context_after.strip().split()[:6]
        return f"[Scene transition before: '{' '.join(first)}']" if first else "[Scene transition]"
    return "[Extended scene — describe the action on screen]"


# ── 90-second budget enforcement ──────────────────────────────────────────────
def enforce_budget(clips: list, max_seconds: float = MAX_OUTPUT_SECONDS) -> tuple:
    def priority(c):
        s = c.get("importance_score", 0.0)
        if c.get("keep_original_audio"):
            s += 0.2
        if c.get("type") == "dialogue":
            s += 0.1
        return s

    # Sort by score descending, then re-select in timeline order
    by_score = sorted(clips, key=priority, reverse=True)
    selected_ids = set()
    total = 0.0

    for clip in by_score:
        dur = clip["end_time"] - clip["start_time"]
        if total + dur <= max_seconds:
            selected_ids.add(clip["clip_id"])
            total += dur

    selected = sorted([c for c in clips if c["clip_id"] in selected_ids],
                      key=lambda c: c["start_time"])
    dropped = len(clips) - len(selected)
    return selected, round(total, 1), dropped


# ── Full clip builder ──────────────────────────────────────────────────────────
def build_clips(segments: list, characters: list = None,
                video_duration: float = 0, video_path: str = None) -> tuple:
    """
    Main function. Returns (selected_clips, total_duration, budget_status).
    Uses global QWEN_API_KEY for visual narration.
    """
    char_map = build_character_map(characters)
    enriched = detect_silent_segments(segments, video_duration)

    clips = []
    counter = 1
    prev_text = ""

    for i, seg in enumerate(enriched):
        next_text = enriched[i + 1]["text"] if i + 1 < len(enriched) else ""

        if seg["is_silent"]:
            narration = generate_narration(
                seg, prev_text, next_text, video_path
            )
            clips.append({
                "clip_id": f"clip_{counter:03d}",
                "start_time": round(seg["start"], 3),
                "end_time": round(seg["end"], 3),
                "duration": round(seg["end"] - seg["start"], 3),
                "type": "silent",
                "speaker_name": None,
                "importance_score": 0.3,
                "transcript": "",
                "keep_original_audio": False,
                "koubo_cuts": [],
                "narration_text": narration,
                "subtitles": []
            })
        else:
            speaker = char_map.get(seg.get("speaker_id", ""),
                                   seg.get("speaker_name") or "Unknown")
            score = score_segment(seg)
            koubo = apply_koubo_cuts(seg) if score >= 0.4 else []
            keep_audio = score > 0.7

            clips.append({
                "clip_id": f"clip_{counter:03d}",
                "start_time": round(seg["start"], 3),
                "end_time": round(seg["end"], 3),
                "duration": round(seg["end"] - seg["start"], 3),
                "type": "dialogue",
                "speaker_name": speaker,
                "importance_score": score,
                "transcript": seg["text"],
                "keep_original_audio": keep_audio,
                "koubo_cuts": koubo,
                "narration_text": None,
                "subtitles": [{
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"],
                    "speaker": speaker
                }]
            })
            prev_text = seg["text"]

        counter += 1

    selected, total, dropped = enforce_budget(clips)
    status = {
        "original_count": len(clips),
        "selected_count": len(selected),
        "dropped_count": dropped,
        "total_duration": total,
        "within_budget": total <= MAX_OUTPUT_SECONDS
    }
    return selected, total, status


# ── vectcut-api payload builder ────────────────────────────────────────────────
def clips_to_draft(video_path: str, clips: list,
                   original_width: int, original_height: int,
                   project_name: str = "Movie Clip Edit") -> dict:
    """
    Build the draft_content.json structure for manual import into CapCut.
    Save with: json.dump(draft, open('draft_content.json','w'), ensure_ascii=False, indent=2)
    """
    return {
        "project_name": project_name,
        "video_path": str(Path(video_path).resolve()),
        "aspect_ratio": {
            "width": original_width,
            "height": original_height,
            "mode": "preserve"
        },
        "editing_style": "koubo",
        "max_duration": MAX_OUTPUT_SECONDS,
        "clips": [{
            "clip_id": c["clip_id"],
            "start_time": c["start_time"],
            "end_time": c["end_time"],
            "type": c["type"],
            "speaker_name": c.get("speaker_name"),
            "keep_original_audio": c.get("keep_original_audio", False),
            "koubo_cuts": c.get("koubo_cuts", []),
            "narration_text": c.get("narration_text"),
            "subtitles": c.get("subtitles", [])
        } for c in clips],
        "options": {
            "subtitle_style": "default",
            "subtitle_position": "bottom",
            "font_size": 36,
            "transition": "none",
            "output_format": "draft_json"
        }
    }


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_segs = [
        {"id": 0, "start": 0.0,  "end": 4.5,
         "text": "Welcome back everyone, um, today we have a really important announcement."},
        {"id": 1, "start": 7.0,  "end": 13.0,
         "text": "Sarah has confirmed — we never expected numbers like this!"},
        {"id": 2, "start": 13.2, "end": 18.0,
         "text": "Let me basically, like, show you what I mean."},
        {"id": 3, "start": 26.0, "end": 30.0,
         "text": "This is the key breakthrough that shocked the industry."},
    ]
    chars = [
        {"id": "spk_0", "name": "Alex",  "role": "Host"},
        {"id": "spk_1", "name": "Sarah", "role": "Guest"}
    ]

    clips, total, status = build_clips(test_segs, chars, video_duration=32.0)

    print(f"Status : {status}")
    print(f"Total  : {total}s\n")
    for c in clips:
        icon = "🎙" if c["type"] == "dialogue" else "🔇"
        print(f"{icon} [{c['clip_id']}] {c['start_time']:.1f}–{c['end_time']:.1f}s  "
              f"score={c['importance_score']}  audio={c['keep_original_audio']}")
        if c["transcript"]:
            print(f"   text  : {c['transcript'][:70]}")
        if c["narration_text"]:
            print(f"   narr  : {c['narration_text']}")
        for cut in c.get("koubo_cuts", []):
            print(f"   ✂ {cut['reason']}")


# ── MP4 render ─────────────────────────────────────────────────────────────────
def render_output_video(clips: list, video_path: str, output_dir: str,
                         original_width: int, original_height: int) -> str:
    """
    Render final output_video.mp4 by:
      - Extracting each clip from source video
      - Overlaying narration audio (muting original) for narration clips
      - Keeping original audio for keep_original_audio=True clips
      - Concatenating everything into one MP4
      - Preserving original aspect ratio
    """
    import shutil
    tmp_dir = os.path.join(output_dir, "tmp_clips")
    os.makedirs(tmp_dir, exist_ok=True)
    clip_files = []

    for clip in clips:
        clip_path = os.path.join(tmp_dir, f"{clip['clip_id']}.mp4")
        duration  = clip["end_time"] - clip["start_time"]
        audio_path = clip.get("audio_path")

        if audio_path and Path(audio_path).exists():
            # Narration clip: overlay TTS audio, mute original
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(clip["start_time"]), "-t", str(duration),
                "-i", video_path,
                "-i", audio_path,
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "libx264", "-c:a", "aac",
                "-shortest", clip_path
            ]
        elif clip.get("keep_original_audio"):
            # Dialogue clip: keep original audio
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(clip["start_time"]), "-t", str(duration),
                "-i", video_path,
                "-c:v", "libx264", "-c:a", "aac",
                clip_path
            ]
        else:
            # Silent clip with no narration audio: mute
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(clip["start_time"]), "-t", str(duration),
                "-i", video_path,
                "-c:v", "libx264", "-an",
                clip_path
            ]

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            print(f"  Warning: clip {clip['clip_id']} render failed, skipping.")
            continue
        clip_files.append(clip_path)

    if not clip_files:
        raise RuntimeError("No clips rendered successfully.")

    # Concat list
    concat_path = os.path.join(tmp_dir, "concat.txt")
    with open(concat_path, "w") as f:
        for p in clip_files:
            f.write(f"file '{os.path.abspath(p)}'\n")

    output_path = os.path.join(output_dir, "output_video.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_path,
        "-vf", f"scale={original_width}:{original_height}"
                ":force_original_aspect_ratio=decrease"
                ":flags=lanczos",
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        output_path
    ], check=True)

    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"[render] Output video: {output_path}")
    return output_path


# ── LLM cinematic narration generator ─────────────────────────────────────────
def generate_cinematic_narration(
    event_description: str,
    stage: str,
    movie_name: str,
    characters: list = None,
    prev_narration: str = "",
    is_first: bool = False
) -> str:
    """
    Call Claude via Anthropic API to generate cinematic movie narration.
    Uses the gripping style: hook opening, tension-building, cliffhanger endings.

    Falls back to event_description if API call fails.
    """
    try:
        import urllib.request, json as _json

        char_str = "、".join(
            f"{c['name']}（{c.get('role','角色')}）"
            for c in (characters or [])
        ) or "未提供"

        hook_instruction = (
            "【重要】这是第一段旁白，必须以钩子句型开头，例如："
            "「眼前这个{角色}，只是做了个{小事}，才...」"
            if is_first else ""
        )

        prompt = f"""你是一位专业的电影解说文案写手，风格参考"木鱼水心"、"谷阿莫"、"电影最TOP"。

电影名称：{movie_name}
角色信息：{char_str}
当前情节事件：{event_description}
所处阶段：{stage}（起因/发展/高潮/结局）
上一段旁白：{prev_narration or "（无）"}
{hook_instruction}

要求：
1. 字数：20-35字，朗读时长约6-8秒
2. 风格：极具感染力，制造悬念，让观众迫切想看下去
3. 开头（仅第一段）：必须用钩子句型，如「眼前这个XX只是做了个XX，才...」
4. 中间段：用「随后」「然而」「就在此时」等转折词自然衔接
5. 结尾段：留悬念或给出有力总结
6. 禁止：平铺直叙、「我们看到」「画面中」「镜头转向」

只输出旁白文案，不要任何解释。"""

        payload = _json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = _json.loads(resp.read())
            return data["content"][0]["text"].strip()

    except Exception as e:
        print(f"  LLM narration failed ({e}), using event description as fallback.")
        return event_description


# ── Project name conflict detection ───────────────────────────────────────────
JIANYING_DRAFT_DIRS = [
    os.path.join(os.environ.get("LOCALAPPDATA", ""), 
                 "JianyingPro", "User Data", "Projects", "com.lveditor.draft"),
    os.path.expanduser(
        "~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"),
]

def resolve_project_name(base_name: str) -> str:
    """
    Check JianYing draft directory for name conflicts.
    Returns base_name if no conflict, or base_name(1) / base_name(2) / ... if taken.
    Notifies user if a rename occurs.
    """
    draft_dir = next((d for d in JIANYING_DRAFT_DIRS if os.path.isdir(d)), None)
    if not draft_dir:
        return base_name  # draft dir not found, proceed without checking

    existing = set(os.listdir(draft_dir))
    if base_name not in existing:
        return base_name

    i = 1
    while f"{base_name}({i})" in existing:
        i += 1
    resolved = f"{base_name}({i})"
    print(f"\n⚠️  草稿名称「{base_name}」已存在")
    print(f"   自动重命名为「{resolved}」以避免覆盖\n")
    return resolved


# ── Narration word budget calculator ──────────────────────────────────────────
CHARS_PER_MINUTE        = 200   # 1 min output video = 200 Chinese chars
TARGET_OUTPUT_SECS      = 60    # target output duration
DURATION_RANGE_SECS     = (45, 75)   # acceptable output range
IDEAL_CHARS_PER_SEGMENT = 25    # ~7.5s TTS per segment


def calculate_narration_budget(video_duration_seconds: float) -> dict:
    """
    Calculate narration word count budget.
    Output video always targets ~60 seconds (45–75s), regardless of source length.
    Rule: 1 minute output = 200 Chinese characters.
    """
    target_chars = CHARS_PER_MINUTE                                         # 200
    min_chars    = int(CHARS_PER_MINUTE * DURATION_RANGE_SECS[0] / 60)     # 150
    max_chars    = int(CHARS_PER_MINUTE * DURATION_RANGE_SECS[1] / 60)     # 250
    ideal_segs   = round(target_chars / IDEAL_CHARS_PER_SEGMENT)            # ~8

    return {
        "target_chars":         target_chars,
        "min_chars":            min_chars,
        "max_chars":            max_chars,
        "ideal_segment_count":  ideal_segs,
        "chars_per_segment":    IDEAL_CHARS_PER_SEGMENT,
        "target_output_secs":   TARGET_OUTPUT_SECS,
        "source_duration_secs": video_duration_seconds,
    }


def check_narration_budget(narrations: list, budget: dict) -> dict:
    """
    Count total chars across all narration segments and check against budget.
    Returns status dict with pass/fail and corrective action.
    """
    total_chars = sum(len(n.get("narration_text", "")) for n in narrations)
    status = "ok"
    action = None

    if total_chars < budget["min_chars"]:
        status = "too_short"
        action = f"expand: need {budget['min_chars'] - total_chars} more chars"
    elif total_chars > budget["max_chars"]:
        status = "too_long"
        action = f"trim: remove {total_chars - budget['max_chars']} chars"

    return {
        "total_chars":    total_chars,
        "target_chars":   budget["target_chars"],
        "min_chars":      budget["min_chars"],
        "max_chars":      budget["max_chars"],
        "status":         status,
        "action":         action,
        "within_budget":  status == "ok",
    }
