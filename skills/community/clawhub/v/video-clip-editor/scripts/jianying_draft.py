#!/usr/bin/env python3
"""
jianying_draft.py
Generates JianYing Pro (剪映专业版) importable draft files:
  - draft_meta_info.json
  - draft_content.json

Spec:
  - draft_version : "10.8.0"
  - Resolution    : 1920x1080, fps 30
  - Time unit     : milliseconds (13-digit)
  - Media paths   : Windows D:/... format
  - Subtitles     : JianYing XML <font color="#FFFFFF"><size=60>text</size></font>
  - All IDs       : uuid4, unique, non-repeating
  - JSON          : strict, no trailing commas
"""

import json
import os
import time
import uuid
from pathlib import Path


# ── Helpers ────────────────────────────────────────────────────────────────────
def new_id() -> str:
    """Generate a unique ID (no hyphens, uppercase — JianYing style)."""
    return str(uuid.uuid4()).replace("-", "").upper()


def ms(seconds: float) -> int:
    """Convert seconds to integer milliseconds."""
    return int(round(seconds * 1000))


def to_win_path(path: str) -> str:
    """
    Convert any path to Windows D:/... format for JianYing file_Path fields.
    If already Windows-style, normalise separators.
    """
    p = str(Path(path).resolve())
    # Convert Linux/macOS absolute paths to Windows-style for the draft
    if p.startswith("/"):
        # Best effort: map /home/... or /mnt/... to D:/...
        p = "D:/" + p.lstrip("/").replace("/", "\\")
    else:
        p = p.replace("/", "\\")
    return p


def subtitle_xml(text: str) -> str:
    """Wrap narration text in JianYing subtitle XML format."""
    return f'<font color="#FFFFFF"><size=60>{text}</size></font>'


def unix_now() -> int:
    return int(time.time())


# ── draft_meta_info.json ───────────────────────────────────────────────────────
def build_meta(project_name: str, output_dir: str,
               total_duration_ms: int, draft_uuid: str) -> dict:
    now = unix_now()
    return {
        "cloud_package_attributes": "",
        "create_time": now,
        "draft_cloud_last_action_download": False,
        "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "",
        "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "",
        "draft_cover": "",
        "draft_deeplink_url": "",
        "draft_enterprise_info": {
            "draft_enterprise_extra": "",
            "draft_enterprise_id": "",
            "draft_enterprise_name": ""
        },
        "draft_fold_path": "",
        "draft_id": draft_uuid,
        "draft_is_ai_packaging_used": False,
        "draft_is_ai_shorts_used": False,
        "draft_is_ai_translate_used": False,
        "draft_is_article_video_used": False,
        "draft_is_from_deeplink": False,
        "draft_is_invisible": False,
        "draft_materials": [],
        "draft_name": project_name,
        "draft_need_rename": False,
        "draft_new_version": "",
        "draft_removable_storage_device": "",
        "draft_root_path": to_win_path(output_dir),
        "draft_timeline_materials_size_": 0,
        "draft_type": "",
        "tm_draft_create": now,
        "tm_draft_modified": now,
        "tm_duration": total_duration_ms
    }


# ── Material builders ──────────────────────────────────────────────────────────
def video_material(clip: dict, output_dir: str) -> dict:
    mp4_path = os.path.join(output_dir, f"{clip['clip_id']}.mp4")
    duration = ms(clip["mp3_duration"])
    return {
        "audio_fade": None,
        "cartoon_path": "",
        "category_id": "",
        "category_name": "",
        "check_flag": 63487,
        "crop": {
            "lower_left_x": 0.0, "lower_left_y": 1.0,
            "lower_right_x": 1.0, "lower_right_y": 1.0,
            "upper_left_x": 0.0, "upper_left_y": 0.0,
            "upper_right_x": 1.0, "upper_right_y": 0.0
        },
        "crop_ratio": "free",
        "crop_scale": 1.0,
        "duration": duration,
        "extra_type_option": 0,
        "file_Path": to_win_path(mp4_path),
        "formula_id": "",
        "id": clip["_mat_video_id"],
        "import_time": unix_now(),
        "import_time_ms": unix_now() * 1000,
        "item_source": 1,
        "md5": "",
        "metetype": "video",
        "roughcut_time_range": {"duration": -1, "start": -1},
        "sub_time_range": {"duration": -1, "start": -1},
        "type": "video",
        "video_algorithm": {
            "algorithms": [], "deflicker": None, "motion_blur_config": None,
            "noise_reduction": None, "path": "", "quality_enhance": None,
            "time_range": None
        },
        "width": 1920,
        "height": 1080
    }


def audio_material(clip: dict, output_dir: str) -> dict:
    mp3_path = os.path.join(output_dir, f"narration_{clip['clip_id']}.mp3")
    duration = ms(clip["mp3_duration"])
    return {
        "app_id": 0,
        "category_id": "",
        "category_name": "local",
        "check_flag": 63487,
        "duration": duration,
        "effect_id": "",
        "file_Path": to_win_path(mp3_path),
        "formula_id": "",
        "id": clip["_mat_audio_id"],
        "import_time": unix_now(),
        "import_time_ms": unix_now() * 1000,
        "item_source": 1,
        "md5": "",
        "metetype": "music",
        "name": f"narration_{clip['clip_id']}",
        "roughcut_time_range": {"duration": -1, "start": -1},
        "sub_time_range": {"duration": -1, "start": -1},
        "type": "extract_music"
    }


def text_material(clip: dict) -> dict:
    xml = subtitle_xml(clip.get("narration_text") or clip.get("transcript", ""))
    return {
        "add_type": 0,
        "alignment": 1,
        "background_alpha": 0.0,
        "background_color": "",
        "background_height": 0.08,
        "background_horizontal_offset": 0.0,
        "background_round_radius": 0.0,
        "background_style": 0,
        "background_vertical_offset": 0.0,
        "background_width": 0.14,
        "bold_width": 0.0,
        "border_alpha": 1.0,
        "border_color": "#000000",
        "border_width": 0.08,
        "content": xml,
        "fixed_height": -1.0,
        "fixed_width": -1.0,
        "font_category_id": "",
        "font_category_name": "",
        "font_id": "",
        "font_name": "",
        "font_path": "",
        "font_resource_id": "",
        "font_size": 60.0,
        "font_source_platform": 0,
        "font_time_range": {"duration": 0, "start": 0},
        "font_title": "",
        "font_url": "",
        "fonts": [],
        "force_apply_line_max_width": False,
        "global_alpha": 1.0,
        "group_id": "",
        "has_shadow": True,
        "id": clip["_mat_text_id"],
        "initial_scale": 1.0,
        "is_rich_text": False,
        "italic": False,
        "italic_degree": 0,
        "letter_spacing": 0.0,
        "line_feed": 1,
        "line_max_width": 0.82,
        "line_spacing": 0.02,
        "multi_language_current": "none",
        "name": "",
        "original_size": [],
        "preset_id": "",
        "recognize_task_id": "",
        "recognize_type": 0,
        "relevance_segment": [],
        "shadow_alpha": 0.9,
        "shadow_angle": -45.0,
        "shadow_color": "#000000",
        "shadow_distance": 8.0,
        "shadow_point": {"x": 0.6364, "y": -0.6364},
        "shadow_smoothing": 0.45,
        "shape_clip_x": False,
        "shape_clip_y": False,
        "style_name": "",
        "sub_type": 0,
        "text_alpha": 1.0,
        "text_color": "#FFFFFF",
        "text_curve": None,
        "text_preset_resource_id": "",
        "text_size": 60,
        "text_to_audio_ids": [],
        "tts_auto_update": False,
        "type": "text",
        "typesetting": 0,
        "underline": False,
        "underline_offset": 0.22,
        "underline_width": 0.05,
        "use_effect_default_color": True,
        "words": {"end_time": [], "start_time": [], "text": []}
    }


# ── Segment builders ──────────────────────────────────────────────────────────
def video_segment(clip: dict, timeline_start_ms: int) -> dict:
    dur   = ms(clip["mp3_duration"])
    src_s = ms(clip["start_time"])
    vol   = 1.0 if clip.get("keep_original_audio") else 0.0
    return {
        "cartoon": False,
        "clip": {
            "alpha": 1.0,
            "flip": {"horizontal": False, "vertical": False},
            "rotation": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "transform": {"x": 0.0, "y": 0.0}
        },
        "common_keyframes": [],
        "enable_adjust": True,
        "enable_color_correct_adjust": False,
        "enable_color_wheels": False,
        "enable_lut": False,
        "enable_smart_color_adjust": False,
        "extra_material_refs": [],
        "group_id": "",
        "hdr_settings": None,
        "id": new_id(),
        "intensifies_audio": False,
        "is_placeholder": False,
        "is_tone_modify": False,
        "keyframe_refs": [],
        "last_nonzero_volume": 1.0,
        "material_id": clip["_mat_video_id"],
        "render_index": 0,
        "responsive_layout": {
            "enable": False, "horizontal_pos_layout": 0,
            "size_layout": 0, "target_follow": "",
            "vertical_pos_layout": 0
        },
        "reverse": False,
        "source_timerange": {"duration": dur, "start": src_s},
        "speed": 1.0,
        "target_timerange": {"duration": dur, "start": timeline_start_ms},
        "template_id": "",
        "template_scene": "default",
        "track_attribute": 0,
        "track_render_index": 0,
        "uniform_scale": {"on": True, "value": 1.0},
        "visible": True,
        "volume": vol
    }


def audio_segment(clip: dict, timeline_start_ms: int) -> dict:
    dur = ms(clip["mp3_duration"])
    return {
        "app_id": 0,
        "category_id": "",
        "category_name": "local",
        "check_flag": 63487,
        "duration": dur,
        "effect_id": "",
        "id": new_id(),
        "intensifies_path": "",
        "is_ai_clone_tone": False,
        "is_text_edit_overdub": False,
        "is_unified_beauty_mode": False,
        "local_material_id": clip["_mat_audio_id"],
        "material_id": clip["_mat_audio_id"],
        "material_name": f"narration_{clip['clip_id']}",
        "render_index": 0,
        "source_timerange": {"duration": dur, "start": 0},
        "speed": 1.0,
        "target_timerange": {"duration": dur, "start": timeline_start_ms},
        "type": "extract_music",
        "volume": 1.0
    }


def text_segment(clip: dict, timeline_start_ms: int) -> dict:
    dur = ms(clip["mp3_duration"])
    xml = subtitle_xml(clip.get("narration_text") or clip.get("transcript", ""))
    return {
        "content": xml,
        "id": new_id(),
        "is_style_definition_segment": False,
        "keyframe_refs": [],
        "material_id": clip["_mat_text_id"],
        "render_index": 0,
        "target_timerange": {"duration": dur, "start": timeline_start_ms},
        "track_attribute": 0,
        "track_render_index": 0,
        "visible": True,
        "z_index": 0
    }


# ── Main generator ─────────────────────────────────────────────────────────────
def generate_jianying_draft(
    project_name: str,
    clips: list,
    output_dir: str,
    original_width: int = 1920,
    original_height: int = 1080
) -> tuple:
    """
    Generate draft_meta_info.json and draft_content.json for JianYing Pro.

    Each clip must have:
      clip_id, start_time, mp3_duration, narration_text (or transcript),
      keep_original_audio (bool)

    Returns: (meta_dict, content_dict)
    """
    output_dir = str(Path(output_dir).resolve())
    draft_uuid = new_id()

    # Pre-assign material IDs to each clip (stable, used in both materials + segments)
    for clip in clips:
        clip["_mat_video_id"] = new_id()
        clip["_mat_audio_id"] = new_id()
        clip["_mat_text_id"]  = new_id()

    # Build materials
    video_mats = [video_material(c, output_dir) for c in clips]
    audio_mats = [audio_material(c, output_dir) for c in clips
                  if not c.get("keep_original_audio")]
    text_mats  = [text_material(c) for c in clips
                  if c.get("narration_text") or c.get("transcript")]

    # Build segments (walk clips in order, accumulate timeline cursor)
    cursor_ms = 0
    video_segs, audio_segs, text_segs = [], [], []

    for clip in clips:
        dur = ms(clip["mp3_duration"])

        video_segs.append(video_segment(clip, cursor_ms))

        if not clip.get("keep_original_audio"):
            audio_segs.append(audio_segment(clip, cursor_ms))

        txt = clip.get("narration_text") or clip.get("transcript", "")
        if txt:
            text_segs.append(text_segment(clip, cursor_ms))

        cursor_ms += dur

    total_ms = cursor_ms

    # Assemble draft_content.json
    content = {
        "canvas_config": {
            "height": original_height,
            "ratio": "original",
            "width": original_width
        },
        "color_space": 0,
        "config": {
            "adjust_max_index": 1,
            "attachment_info": [],
            "combination_max_index": 1,
            "export_range": None,
            "extract_audio_last_index": 1,
            "lyrics_recognition_id": "",
            "lyrics_sync": True,
            "lyrics_taskinfo": [],
            "maintrack_adsorb": True,
            "material_save_mode": 0,
            "multi_language_current": "none",
            "multi_language_list": [],
            "multi_language_main": "none",
            "multi_language_mode": "none",
            "original_sound_last_index": 1,
            "record_audio_last_index": 1,
            "sticker_max_index": 1,
            "subtitle_recognition_id": "",
            "subtitle_sync": True,
            "subtitle_taskinfo": [],
            "system_font_list": [],
            "video_mute": False,
            "zoom_info_params": None
        },
        "cover": "",
        "create_time": 0,
        "duration": total_ms,
        "extra_info": None,
        "fps": 30.0,
        "free_render_index_mode_on": False,
        "group_container": None,
        "id": draft_uuid,
        "keyframe_graph_list": [],
        "keyframes": {
            "adjusts": [], "audios": [], "effects": [], "filters": [],
            "handwrites": [], "stickers": [], "texts": [], "videos": []
        },
        "lyrics_effects_size_": 0,
        "materials": {
            "audios": audio_mats,
            "videos": video_mats,
            "texts":  text_mats
        },
        "mutable_config": None,
        "name": project_name,
        "new_version": "10.8.0",
        "platform": {
            "app_id": 3704,
            "app_source": "lv",
            "app_version": "5.9.0",
            "device_id": "",
            "hard_disk_id": "",
            "mac_id": "",
            "os": "windows",
            "os_version": ""
        },
        "relationships": [],
        "render_index_track_mode_on": False,
        "retouch_cover": None,
        "source": "default",
        "static_cover_image_path": "",
        "time_marks": None,
        "tracks": [
            {
                "attribute": 0,
                "flag": 0,
                "id": new_id(),
                "is_default_name": True,
                "name": "",
                "segments": video_segs,
                "type": "video"
            },
            {
                "attribute": 0,
                "flag": 0,
                "id": new_id(),
                "is_default_name": True,
                "name": "",
                "segments": audio_segs,
                "type": "audio"
            },
            {
                "attribute": 0,
                "flag": 0,
                "id": new_id(),
                "is_default_name": True,
                "name": "",
                "segments": text_segs,
                "type": "text"
            }
        ],
        "update_time": 0,
        "version": 360000
    }

    meta = build_meta(project_name, output_dir, total_ms, draft_uuid)
    return meta, content


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_clips = [
        {
            "clip_id": "clip_001",
            "start_time": 200.0,
            "mp3_duration": 6.34,
            "narration_text": "眼前这个陆永瑜，只是举报了父亲的贪腐行为，才发现自己已经踏入了一个无法回头的深渊...",
            "keep_original_audio": False
        },
        {
            "clip_id": "clip_002",
            "start_time": 1125.0,
            "mp3_duration": 5.81,
            "narration_text": "随后，陆金强拿出了那段视频——弑父的证据，一字一句，把他逼入了死角。",
            "keep_original_audio": False
        },
        {
            "clip_id": "clip_003",
            "start_time": 4350.0,
            "mp3_duration": 6.10,
            "narration_text": "就在此时，律师张远当庭播放未剪辑原版监控，陆金强的谎言彻底崩塌。",
            "keep_original_audio": False
        }
    ]

    meta, content = generate_jianying_draft(
        project_name    = "误判",
        clips           = test_clips,
        output_dir      = "/tmp/jianying_test",
        original_width  = 1920,
        original_height = 1080
    )

    import json, os
    os.makedirs("/tmp/jianying_test", exist_ok=True)
    with open("/tmp/jianying_test/draft_meta_info.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    with open("/tmp/jianying_test/draft_content.json", "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"draft_meta_info.json  {os.path.getsize('/tmp/jianying_test/draft_meta_info.json')} bytes")
    print(f"draft_content.json    {os.path.getsize('/tmp/jianying_test/draft_content.json')} bytes")
    print(f"Total duration        {content['duration']}ms  ({content['duration']/1000:.1f}s)")
    print(f"Video tracks          {len(content['tracks'][0]['segments'])} segments")
    print(f"Audio tracks          {len(content['tracks'][1]['segments'])} segments")
    print(f"Text tracks           {len(content['tracks'][2]['segments'])} segments")
    print()

    # Validate: check all IDs are unique
    all_ids = []
    for mat_type in content["materials"].values():
        all_ids += [m["id"] for m in mat_type]
    for track in content["tracks"]:
        all_ids += [track["id"]]
        all_ids += [s["id"] for s in track["segments"]]
    all_ids.append(content["id"])

    dupes = [x for x in all_ids if all_ids.count(x) > 1]
    if dupes:
        print(f"DUPLICATE IDs FOUND: {dupes}")
    else:
        print(f"ID uniqueness check: PASS ({len(all_ids)} unique IDs)")

    # Validate: check subtitle XML format
    for seg in content["tracks"][2]["segments"]:
        assert seg["content"].startswith("<font color="), f"Bad XML: {seg['content']}"
    print("Subtitle XML check: PASS")
