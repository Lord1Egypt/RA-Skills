#!/usr/bin/env python3
"""
CapCut MCP Builder
Translates the clip list from build_payload.py into a sequence of
CapCut MCP tool calls to construct the final draft.

Replaces the old vectcut-api HTTP approach entirely.

Usage (called by Claude as part of the pipeline):
  from capcut_mcp_builder import build_capcut_draft
  result = build_capcut_draft(mcp_client, clips, video_path, original_width, original_height, srt_path, narration_dir)
"""

import os
from pathlib import Path


# ── Aspect ratio helpers ───────────────────────────────────────────────────────
def get_capcut_dimensions(original_width: int, original_height: int) -> tuple:
    """
    Return (width, height) for create_draft, preserving original aspect ratio.
    Normalizes to a standard resolution while keeping the exact ratio.
    """
    if not original_width or not original_height:
        return 1920, 1080  # safe default

    # Common output targets
    targets = [
        (1920, 1080),  # 16:9 landscape
        (1080, 1920),  # 9:16 portrait
        (1080, 1080),  # 1:1 square
        (2560, 1080),  # 21:9 ultrawide
        (1080, 1350),  # 4:5 Instagram
    ]

    input_ratio = original_width / original_height
    best = min(targets, key=lambda t: abs(t[0] / t[1] - input_ratio))

    # If no target is close enough, use the exact original dimensions
    best_ratio = best[0] / best[1]
    if abs(best_ratio - input_ratio) > 0.05:
        return original_width, original_height

    return best


# ── Main draft builder ─────────────────────────────────────────────────────────
def build_capcut_draft(
    mcp_client,              # MCP client instance from OpenClaw/Claude context
    clips: list,             # output of build_payload.build_clips()
    video_path: str,         # absolute path to source video
    original_width: int,
    original_height: int,
    srt_path: str = None,    # path to subtitles.srt (from narration_audio.generate_srt)
    narration_dir: str = None,  # dir containing clip_XXX_narration.mp3 files
    project_name: str = "Movie Clip Edit"
) -> dict:
    """
    Build a complete CapCut draft via MCP tool calls.

    Steps:
      1. create_draft  — set dimensions
      2. add_video     — one call per clip (with volume based on keep_original_audio)
      3. add_audio     — one call per silent clip that has a narration MP3
      4. add_text      — one call per silent clip for the on-screen narration card
      5. add_subtitle  — one call to attach the full SRT file
      6. save_draft    — finalize

    Returns the save_draft result dict.
    """
    video_path = str(Path(video_path).resolve())
    w, h = get_capcut_dimensions(original_width, original_height)

    print(f"\n[MCP] Starting CapCut draft: {w}x{h} | {len(clips)} clips")

    # ── Step 1: Create draft ───────────────────────────────────────────────────
    result = mcp_client.call_tool("create_draft", {"width": w, "height": h})
    if not result.get("success"):
        raise RuntimeError(f"create_draft failed: {result}")
    draft_id = result["result"]["draft_id"]
    print(f"[MCP] Draft created: {draft_id}")

    # ── Step 2: Add video clips ────────────────────────────────────────────────
    for clip in clips:
        # For koubo editing: apply internal micro-cuts by splitting into
        # sub-segments around each koubo_cut removal window
        sub_segments = _apply_koubo_cuts(clip)

        for seg in sub_segments:
            volume = 1.0 if clip.get("keep_original_audio", False) else 0.0
            result = mcp_client.call_tool("add_video", {
                "draft_id": draft_id,
                "video_url": video_path,
                "start": seg["start"],
                "end": seg["end"],
                "volume": volume
            })
            if not result.get("success"):
                print(f"[MCP] Warning: add_video failed for {clip['clip_id']} "
                      f"[{seg['start']:.2f}-{seg['end']:.2f}]: {result}")

    print(f"[MCP] Added {len(clips)} clips to timeline")

    # ── Step 3: Add narration audio for silent clips ───────────────────────────
    if narration_dir:
        narration_dir = Path(narration_dir)
        for clip in clips:
            if clip.get("type") != "silent":
                continue
            mp3_path = narration_dir / f"{clip['clip_id']}_narration.mp3"
            if mp3_path.exists():
                result = mcp_client.call_tool("add_audio", {
                    "draft_id": draft_id,
                    "audio_url": str(mp3_path),
                    "start": clip["start_time"],
                    "end": clip["end_time"],
                    "volume": 1.0
                })
                if result.get("success"):
                    print(f"[MCP] Narration audio added: {clip['clip_id']}")
                else:
                    print(f"[MCP] Warning: add_audio failed for {clip['clip_id']}: {result}")

    # ── Step 4: Add narration text cards for silent clips ─────────────────────
    for clip in clips:
        if clip.get("type") != "silent":
            continue
        narration = clip.get("narration_text")
        if not narration:
            continue

        result = mcp_client.call_tool("add_text", {
            "draft_id": draft_id,
            "text": narration,
            "start": clip["start_time"],
            "end": clip["end_time"],
            "font_size": 36,
            "font_color": "#FFFFFF",
            "shadow_enabled": True,
            "shadow_color": "#000000",
            "shadow_alpha": 0.8,
            "background_color": "#1E1E1E",
            "background_alpha": 0.6,
            "background_round_radius": 10
        })
        if result.get("success"):
            print(f"[MCP] Narration text card added: {clip['clip_id']} → '{narration[:40]}'")
        else:
            print(f"[MCP] Warning: add_text failed for {clip['clip_id']}: {result}")

    # ── Step 5: Add subtitle SRT ───────────────────────────────────────────────
    if srt_path and Path(srt_path).exists():
        result = mcp_client.call_tool("add_subtitle", {
            "draft_id": draft_id,
            "srt_path": str(Path(srt_path).resolve()),
            "font_style": "default",
            "position": "bottom"
        })
        if result.get("success"):
            print(f"[MCP] Subtitles added from: {srt_path}")
        else:
            print(f"[MCP] Warning: add_subtitle failed: {result}")

    # ── Step 6: Save draft ─────────────────────────────────────────────────────
    result = mcp_client.call_tool("save_draft", {"draft_id": draft_id})
    if not result.get("success"):
        raise RuntimeError(f"save_draft failed: {result}")

    print(f"\n[MCP] Draft saved successfully!")
    print(f"  draft_id  : {draft_id}")
    print(f"  draft_url : {result['result'].get('draft_url', 'N/A')}")

    return {
        "draft_id": draft_id,
        "draft_url": result["result"].get("draft_url"),
        "dimensions": f"{w}x{h}",
        "clip_count": len(clips),
        "success": True
    }


# ── Koubo micro-cut splitter ───────────────────────────────────────────────────
def _apply_koubo_cuts(clip: dict) -> list:
    """
    Split a clip into sub-segments by removing koubo_cut windows.

    Example:
      clip: start=0.0, end=10.0
      koubo_cuts: [{remove_start: 2.0, remove_end: 2.5},
                   {remove_start: 6.0, remove_end: 6.8}]
      result: [{start:0.0, end:2.0}, {start:2.5, end:6.0}, {start:6.8, end:10.0}]
    """
    cuts = clip.get("koubo_cuts", [])
    start = clip["start_time"]
    end = clip["end_time"]
    min_duration = 0.3  # skip sub-segments shorter than this

    if not cuts:
        return [{"start": start, "end": end}]

    # Sort cuts by start time
    cuts = sorted(cuts, key=lambda c: c["remove_start"])

    segments = []
    cursor = start

    for cut in cuts:
        rs = max(cut["remove_start"], cursor)
        re = min(cut["remove_end"], end)
        if rs > cursor and (rs - cursor) >= min_duration:
            segments.append({"start": cursor, "end": rs})
        cursor = re

    # Add final segment after last cut
    if end - cursor >= min_duration:
        segments.append({"start": cursor, "end": end})

    return segments if segments else [{"start": start, "end": end}]


# ── MCP call sequence preview (for user approval) ─────────────────────────────
def preview_mcp_calls(
    clips: list,
    video_path: str,
    original_width: int,
    original_height: int,
    srt_path: str = None,
    narration_dir: str = None
) -> str:
    """
    Generate a human-readable preview of the MCP tool calls that will be made.
    Show this to the user BEFORE actually executing, as part of Step 4 approval.
    """
    w, h = get_capcut_dimensions(original_width, original_height)
    lines = []
    lines.append(f"MCP Call Plan — {len(clips)} clips → {w}x{h} draft")
    lines.append("=" * 55)

    total_duration = sum(c["end_time"] - c["start_time"] for c in clips)
    dialogue = [c for c in clips if c.get("type") == "dialogue"]
    silent = [c for c in clips if c.get("type") == "silent"]

    lines.append(f"1. create_draft(width={w}, height={h})")
    lines.append("")

    call_n = 2
    for clip in clips:
        subs = _apply_koubo_cuts(clip)
        vol = 1.0 if clip.get("keep_original_audio") else 0.0
        speaker = clip.get("speaker_name") or "—"
        for sub in subs:
            lines.append(
                f"{call_n}. add_video(start={sub['start']:.1f}, end={sub['end']:.1f}, "
                f"volume={vol})  [{clip['clip_id']} {clip.get('type','?')} | {speaker}]"
            )
            call_n += 1

    lines.append("")
    if narration_dir:
        for clip in [c for c in clips if c.get("type") == "silent"]:
            mp3 = Path(narration_dir) / f"{clip['clip_id']}_narration.mp3"
            if mp3.exists():
                lines.append(
                    f"{call_n}. add_audio({clip['clip_id']}_narration.mp3, "
                    f"start={clip['start_time']:.1f}, end={clip['end_time']:.1f})"
                )
                call_n += 1

    lines.append("")
    for clip in [c for c in clips if c.get("type") == "silent" and c.get("narration_text")]:
        lines.append(
            f"{call_n}. add_text('{clip['narration_text'][:35]}...', "
            f"start={clip['start_time']:.1f}, end={clip['end_time']:.1f})"
        )
        call_n += 1

    lines.append("")
    if srt_path:
        lines.append(f"{call_n}. add_subtitle(subtitles.srt, position=bottom)")
        call_n += 1

    lines.append(f"{call_n}. save_draft()")
    lines.append("")
    lines.append(f"Summary: {len(dialogue)} dialogue + {len(silent)} silent clips")
    lines.append(f"Total duration: {total_duration:.1f}s / 90s max")
    lines.append(f"Total MCP calls: {call_n}")

    return "\n".join(lines)


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_clips = [
        {
            "clip_id": "clip_001", "type": "dialogue",
            "start_time": 0.0, "end_time": 4.2,
            "keep_original_audio": True,
            "speaker_name": "Alex",
            "narration_text": None,
            "koubo_cuts": [
                {"remove_start": 1.1, "remove_end": 1.5, "reason": "filler: 'um'"}
            ]
        },
        {
            "clip_id": "clip_002", "type": "silent",
            "start_time": 4.2, "end_time": 6.2,
            "keep_original_audio": False,
            "speaker_name": None,
            "narration_text": "[Alex walks to the whiteboard]",
            "koubo_cuts": []
        },
        {
            "clip_id": "clip_003", "type": "dialogue",
            "start_time": 9.8, "end_time": 14.5,
            "keep_original_audio": True,
            "speaker_name": "Sarah",
            "narration_text": None,
            "koubo_cuts": []
        }
    ]

    print(preview_mcp_calls(
        clips=test_clips,
        video_path="/movies/DarkKnight.mp4",
        original_width=2560,
        original_height=1080,
        srt_path="subtitles.srt",
        narration_dir="/tmp/narrations"
    ))

    print("\nKoubo cut test:")
    for sub in _apply_koubo_cuts(test_clips[0]):
        print(f"  sub-segment: {sub['start']:.2f}s → {sub['end']:.2f}s")
