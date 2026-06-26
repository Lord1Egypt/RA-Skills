#!/usr/bin/env python3
"""
plot_researcher.py
Step 0: Search movie plot online via multi-search-engine tool,
        parse into timeline events, and rewrite as narration script.

Called by Claude as part of the pipeline — not a standalone CLI.
All functions return structured data for downstream use.
"""

import re
import json

# ── Narration transition words ─────────────────────────────────────────────────
TRANSITIONS = {
    "opening":     ["故事开始于", "一切的起点是", "影片伊始，"],
    "development": ["随后，", "紧接着，", "与此同时，", "就在这时，"],
    "climax":      ["然而，", "就在此刻，", "危机悄然降临——", "命运的转折点出现了，"],
    "resolution":  ["最终，", "就此，", "故事的结局是，", "尘埃落定，"],
    "neutral":     ["随后，", "然而，", "与此同时，", "不久后，", "就在此时，"]
}

# ── Search query builder ───────────────────────────────────────────────────────
def build_search_queries(movie_name: str) -> list:
    """
    Return a list of search queries to send to multi-search-engine.
    Covers: plot summary, scene timestamps, key events.
    """
    return [
        f"{movie_name} 剧情详细介绍 起因发展高潮结局",
        f"{movie_name} 电影剧情时间线 精彩片段时间点",
        f"{movie_name} plot summary timeline key scenes",
        f"{movie_name} 电影解说 分段剧情",
    ]


# ── Plot parser ────────────────────────────────────────────────────────────────
def parse_plot_to_events(raw_plot: str, movie_duration_minutes: float = None) -> list:
    """
    Parse raw plot text (from search results) into structured timeline events.

    Returns list of:
    {
        "event_id": "evt_001",
        "stage": "opening|development|climax|resolution",
        "video_timestamp": "01:15:00",   # HH:MM:SS or MM:SS from search result
        "video_seconds": 4500,           # converted to seconds
        "description": "陆金强带人找到废车场监听室，拿陆永瑜弑父视频要挟",
        "raw_text": "..."
    }
    """
    events = []
    counter = 1

    # Try to extract timestamp-prefixed lines (e.g. "01:15:00 陆金强...")
    timestamp_pattern = re.compile(
        r'(\d{1,3}:\d{2}(?::\d{2})?)\s*[：:]\s*(.+)'
    )

    lines = raw_plot.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        m = timestamp_pattern.match(line)
        if m:
            ts_str = m.group(1)
            desc = m.group(2).strip()
            seconds = _ts_to_seconds(ts_str)
            stage = _infer_stage(seconds, movie_duration_minutes)
            events.append({
                "event_id": f"evt_{counter:03d}",
                "stage": stage,
                "video_timestamp": ts_str,
                "video_seconds": seconds,
                "description": desc,
                "raw_text": line
            })
            counter += 1

    # If no timestamps found, split into 4 logical stages from prose
    if not events:
        events = _split_prose_to_stages(raw_plot, counter)

    return events


def _ts_to_seconds(ts: str) -> int:
    """Convert HH:MM:SS or MM:SS to total seconds."""
    parts = ts.strip().split(':')
    parts = [int(p) for p in parts]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return 0


def _infer_stage(seconds: int, total_seconds: float = None) -> str:
    """Infer narrative stage from timestamp position."""
    if not total_seconds:
        total_seconds = 7200  # assume 2h default
    ratio = seconds / total_seconds
    if ratio < 0.15:
        return "opening"
    elif ratio < 0.5:
        return "development"
    elif ratio < 0.85:
        return "climax"
    else:
        return "resolution"


def _split_prose_to_stages(text: str, start_counter: int) -> list:
    """Fallback: split prose plot into 4 equal stage segments."""
    sentences = re.split(r'[。！？.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    n = len(sentences)
    stages = ["opening", "development", "climax", "resolution"]
    chunk = max(1, n // 4)
    events = []
    counter = start_counter

    for i, stage in enumerate(stages):
        chunk_sents = sentences[i * chunk: (i + 1) * chunk]
        if not chunk_sents:
            continue
        events.append({
            "event_id": f"evt_{counter:03d}",
            "stage": stage,
            "video_timestamp": None,
            "video_seconds": None,
            "description": "。".join(chunk_sents),
            "raw_text": "。".join(chunk_sents)
        })
        counter += 1

    return events


# ── Narration script writer ────────────────────────────────────────────────────
def events_to_narration(events: list, movie_name: str = "") -> list:
    """
    Rewrite each event description into a narration sentence with
    appropriate transition words.

    Returns list of:
    {
        "narration_id": "nar_001",
        "event_id": "evt_001",
        "stage": "opening",
        "video_timestamp": "01:15:00",
        "video_seconds": 4500,
        "narration_text": "故事开始于一场意外——陆金强带人找到废车场...",
        "estimated_tts_seconds": None  # filled in by tts_generator.py
    }
    """
    import random
    narrations = []
    stage_counts = {}

    for i, evt in enumerate(events):
        stage = evt.get("stage", "neutral")
        count = stage_counts.get(stage, 0)
        stage_counts[stage] = count + 1

        # Pick transition word
        pool = TRANSITIONS.get(stage, TRANSITIONS["neutral"])
        # Use first transition for stage's first event, rotate after
        transition = pool[count % len(pool)]

        desc = evt["description"].strip()
        # Remove leading transitions already in desc
        for t in ["随后", "然而", "就在", "最终", "紧接着", "与此同时"]:
            if desc.startswith(t):
                desc = desc[len(t):].lstrip("，,、")
                break

        # Compose narration sentence
        narration = f"{transition}{desc}"
        if not narration.endswith(("。", "！", "？", "…", "——")):
            narration += "。"

        narrations.append({
            "narration_id": f"nar_{i+1:03d}",
            "event_id": evt["event_id"],
            "stage": stage,
            "video_timestamp": evt.get("video_timestamp"),
            "video_seconds": evt.get("video_seconds"),
            "narration_text": narration,
            "estimated_tts_seconds": None  # set after TTS generation
        })

    return narrations


# ── Duration estimator (before TTS) ───────────────────────────────────────────
def estimate_tts_duration(text: str, chars_per_second: float = 5.5) -> float:
    """
    Rough estimate of TTS audio duration before actually generating it.
    Chinese: ~5.5 chars/sec at normal speed.
    """
    clean = re.sub(r'[^\u4e00-\u9fff\w]', '', text)
    return round(len(clean) / chars_per_second, 2)


def add_duration_estimates(narrations: list) -> list:
    """Add estimated_tts_seconds to each narration item."""
    for n in narrations:
        n["estimated_tts_seconds"] = estimate_tts_duration(n["narration_text"])
    return narrations


# ── Total duration check (target 3–5 min) ─────────────────────────────────────
def check_total_duration(narrations: list) -> dict:
    """
    Check if total estimated TTS duration is within 3–5 minutes.
    Returns status and recommendation.
    """
    total = sum(n.get("estimated_tts_seconds", 0) for n in narrations)
    target_min, target_max = 180, 300  # 3–5 minutes

    return {
        "total_seconds": round(total, 1),
        "total_display": f"{int(total//60)}:{int(total%60):02d}",
        "within_target": target_min <= total <= target_max,
        "recommendation": (
            "✅ 时长合适" if target_min <= total <= target_max
            else f"⚠️ 偏{'短' if total < target_min else '长'}，建议{'增加' if total < target_min else '精简'}段落"
        )
    }


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Simulate parsed plot with timestamps
    sample_plot = """
01:00:00：陆永瑜发现父亲陆建业贪污受贿的证据，愤而举报
01:15:00：陆金强带人找到废车场监听室，拿陆永瑜弑父视频要挟
01:35:00：陆永瑜被迫签下认罪书，案件陷入僵局
01:50:00：律师张远发现监控录像存在剪辑痕迹，真相浮出水面
02:05:00：法庭上陆金强的伪证被当庭揭穿，陆永瑜无罪释放
"""
    events = parse_plot_to_events(sample_plot, movie_duration_minutes=120)
    narrations = events_to_narration(events, movie_name="误判")
    narrations = add_duration_estimates(narrations)
    status = check_total_duration(narrations)

    print(f"共 {len(narrations)} 段旁白  |  预估总时长: {status['total_display']}  |  {status['recommendation']}\n")
    for n in narrations:
        print(f"[{n['narration_id']}] {n['video_timestamp']}  ~{n['estimated_tts_seconds']}s")
        print(f"  {n['narration_text']}\n")

    print("Search queries:")
    for q in build_search_queries("误判"):
        print(f"  - {q}")
