---
name: video-clip-editor
description: "Video clip editing skill for automatically analyzing video content and generating CapCut draft templates. Uses local Whisper for speech transcription, Qwen-VL-Plus for visual scene description, and edge-tts for narration audio. Intelligently splits by dialogue/keywords/highlights, applies koubo jump-cut editing, and outputs draft_content.json ready to import into CapCut. Use this skill whenever the user mentions: video editing, clip, CapCut draft, highlight extraction, subtitle editing, keyword clipping, movie clip, narration, scene description, or uploads a video and asks to edit it."
license: MIT
---

# Video Clip Editor Skill

## Strict Output Contract

Every run MUST produce exactly these 4 files in `video_clipper_output/`:

```
video_clipper_output/
├── narration_XXX.mp3      ← 配音音频，每段独立文件，时间戳对齐
├── subtitles.srt          ← 字幕，时间轴与 mp3 严格对应
├── clip_XXX.mp4           ← 视频切片，每段独立文件
└── draft_content.json     ← 剪映草稿文件
```

**不允许缺少任何一个。每个 mp3/mp4 的时间轴必须与 srt 中对应条目精确匹配。**

---

## Two Operating Modes

### Mode A — Movie Narration (电影解说)
User provides movie name + video file → LLM generates cinematic narration.

### Mode B — Interview / Dialogue (剪口播)
User provides video with real speech → Whisper transcribes → koubo jump-cut editing.

---

## Overall Workflow

```
[Step 0]  Collect inputs (movie name / characters / voice)
    ↓
[Step 1]  ffprobe → original aspect ratio + video duration
    ↓
[Step 2]  Mode A: search movie plot online → LLM generates narration script
          Mode B: Whisper transcription → koubo clip analysis
    ↓
[Step 3]  Show clip plan → wait for user approval
    ↓
[Step 4]  Generate narration_XXX.mp3  (one per clip, edge-tts)
          Measure ACTUAL mp3 duration via ffprobe
    ↓
[Step 5]  Generate clip_XXX.mp4       (one per clip, ffmpeg)
          clip duration = mp3 duration (exact match)
    ↓
[Step 6]  Generate subtitles.srt      (timestamps from mp3 durations)
    ↓
[Step 7]  Generate draft_content.json (JianYing/CapCut importable)
    ↓
[Step 8]  Show final output message
```

---

## Step 0: Collect Inputs

Ask before starting:

**Mode A:**
> "请提供：① 电影名称 ② 视频文件完整路径 ③ 片中主要角色（如：主角陆永瑜，反派陆金强） ④ 旁白语音（默认：zh-CN-XiaoxiaoNeural）"

**Mode B:**
> "请提供：① 视频文件路径 ② 说话人名称（如：主持人Alex，嘉宾Sarah，可跳过） ③ 旁白语音（默认：zh-CN-XiaoxiaoNeural）"

```python
movie_name  = "误判"
video_path  = "C:\\Movies\\误判.mp4"
characters  = [{"name": "陆永瑜", "role": "主角"}, {"name": "陆金强", "role": "反派"}]
tts_voice   = "zh-CN-XiaoxiaoNeural"
output_dir  = "video_clipper_output"
```

### Project Name Conflict Detection (草稿名冲突处理)

Before generating any files, check if a project with the same name already exists
in the JianYing draft directory. If it does, append `(1)`, `(2)`, `(3)` etc. to avoid overwriting.

```python
import os, re

JIANYING_DRAFT_DIRS = [
    # Windows
    os.path.expandvars(r"%LOCALAPPDATA%\JianyingPro\User Data\Projects\com.lveditor.draft"),
    # macOS
    os.path.expanduser("~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"),
]

def resolve_project_name(base_name: str) -> str:
    """
    Check JianYing draft directory for name conflicts.
    Returns base_name if no conflict, or base_name(1) / base_name(2) / ... if taken.
    """
    draft_dir = next((d for d in JIANYING_DRAFT_DIRS if os.path.isdir(d)), None)
    if not draft_dir:
        return base_name  # can't check, proceed with original name

    existing = set(os.listdir(draft_dir))

    if base_name not in existing:
        return base_name

    # Find next available suffix
    i = 1
    while f"{base_name}({i})" in existing:
        i += 1
    resolved = f"{base_name}({i})"

    # Notify user
    print(f"⚠️  草稿名称「{base_name}」已存在，自动重命名为「{resolved}」以避免覆盖。")
    return resolved

# Call at the start, before generating any files
project_name = resolve_project_name(movie_name)
output_dir   = f"video_clipper_output_{project_name}"
```

Tell the user before proceeding:
```
⚠️ 检测到剪映草稿「误判」已存在
   本次项目将命名为「误判(1)」，输出到 video_clipper_output_误判(1)/
   继续？(是 / 自定义名称)
```

---

## Step 1: Probe Video + Calculate Narration Budget

```bash
# Get width, height, duration
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration \
  -of json <video_path>
```

Store: `original_width`, `original_height`, `video_duration_seconds`.

### Narration Word Budget (字数预算)

**Core rule: 1 minute of output video = 200 Chinese characters of narration**

```python
CHARS_PER_MINUTE  = 200          # 1 min output = 200 chars
TARGET_DURATION_S = 60           # target output: ~60 seconds
DURATION_RANGE    = (45, 75)     # acceptable range: 45s – 75s

def calculate_narration_budget(video_duration_seconds: float) -> dict:
    """
    Calculate how many characters and segments to generate.
    Output video is always capped to ~60 seconds (±15s), regardless of source length.
    """
    target_chars  = CHARS_PER_MINUTE                # 200 chars → ~60s output
    min_chars     = int(CHARS_PER_MINUTE * DURATION_RANGE[0] / 60)   # 150 chars → 45s
    max_chars     = int(CHARS_PER_MINUTE * DURATION_RANGE[1] / 60)   # 250 chars → 75s

    # Typical segment: 25 chars → ~7.5s each
    ideal_segment_chars  = 25
    ideal_segment_count  = round(target_chars / ideal_segment_chars)   # ~8 segments

    return {
        "target_chars":         target_chars,    # 200
        "min_chars":            min_chars,        # 150
        "max_chars":            max_chars,        # 250
        "ideal_segment_count":  ideal_segment_count,  # ~8
        "chars_per_segment":    ideal_segment_chars,  # 25
        "target_output_secs":   TARGET_DURATION_S,    # 60
        "source_duration_secs": video_duration_seconds
    }

budget = calculate_narration_budget(video_duration_seconds)
```

**Tell user the budget before searching:**
```
📐 旁白字数预算
   源视频时长  ：X 分 X 秒
   目标输出时长：约 60 秒（可接受范围：45–75 秒）
   旁白总字数  ：约 200 字（150–250 字区间）
   预计片段数  ：约 8 段，每段约 25 字
```

**Enforcement during narration generation:**
- Each segment: aim for `chars_per_segment` (25 chars), hard max 35 chars
- After all segments written: count total chars
  - < 150 chars → expand existing segments or add 1–2 more
  - \> 250 chars → trim or merge lowest-importance segments
- Final output video duration MUST land in 45–75s range

---

## Step 2: Build Clip List

### Mode A — Online Search for Precise Scene Timestamps

**Search strategy — run ALL queries, then synthesize:**

```python
def build_search_queries(movie_name: str) -> list:
    return [
        f"{movie_name} 剧情详解 起因发展高潮结局 时间点",
        f"{movie_name} 电影解说 精彩片段时间轴 几分几秒",
        f"{movie_name} 剧情时间线 关键场景 时间戳",
        f"{movie_name} plot breakdown scene timestamps minutes",
        f"{movie_name} 完整剧情 开头结尾 高潮在第几分钟",
    ]
```

**Parse search results into events with PRECISE timestamps:**

Each event MUST have a specific `video_timestamp` (not a vague range).
If search results give ranges like "第30–40分钟", take the midpoint (35:00).
If no timestamp is found for an event, mark `timestamp_confidence: "estimated"`.

```json
[
  {
    "event_id":            "evt_001",
    "stage":               "起因",
    "video_timestamp":     "00:03:20",
    "video_seconds":       200,
    "timestamp_confidence":"exact",
    "description":         "陆永瑜在父亲书房发现账本，意识到父亲长期贪腐"
  },
  {
    "event_id":            "evt_002",
    "stage":               "发展",
    "video_timestamp":     "00:18:45",
    "video_seconds":       1125,
    "timestamp_confidence":"exact",
    "description":         "陆金强约见陆永瑜，暗示他撤回举报，遭到拒绝"
  },
  {
    "event_id":            "evt_003",
    "stage":               "发展",
    "video_timestamp":     "00:35:10",
    "video_seconds":       2110,
    "timestamp_confidence":"estimated",
    "description":         "律师张远接手案件，发现监控录像有剪辑痕迹"
  },
  {
    "event_id":            "evt_004",
    "stage":               "高潮",
    "video_timestamp":     "01:12:30",
    "video_seconds":       4350,
    "timestamp_confidence":"exact",
    "description":         "庭审现场，张远当庭播放未剪辑原版监控，陆金强伪证当场崩塌"
  },
  {
    "event_id":            "evt_005",
    "stage":               "结局",
    "video_timestamp":     "01:28:00",
    "video_seconds":       5280,
    "timestamp_confidence":"exact",
    "description":         "陆永瑜无罪释放，走出法院，与家人重逢"
  }
]
```

**Segment count must match `budget["ideal_segment_count"]` (≈8).**
If search only returns 4–5 events, expand by splitting long stages into sub-events.
If search returns 15+ events, merge adjacent same-stage events.

**Each clip duration = narration TTS duration (measured AFTER TTS generation in Step 4).**
Source video timestamp marks WHERE to cut, not HOW LONG to hold.

### Mode A — Narration Script via LLM

Generate narration for EACH event. Total char count must stay within budget (150–250 chars).
Then call LLM for each event:

**LLM Narration Prompt:**
```
你是专业电影解说文案写手，风格参考"木鱼水心"。

电影：{movie_name}
角色：{characters}
事件：{event_description}
阶段：{stage}（起因/发展/高潮/结局）
上段旁白：{prev_narration}
本段目标字数：{target_chars_this_segment} 字（全片总字数预算：{total_budget} 字，已用：{used_chars} 字，剩余：{remaining_chars} 字）

要求：
- 严格控制在 {target_chars_this_segment} 字左右（±3字），不得超过 35 字
- 第一段必须用钩子开头：「眼前这个{角色}，只是{做了件小事}，才...」
- 中间段用「随后」「然而」「就在此时」衔接
- 极具感染力，制造悬念
- 禁止平铺直叙，禁止「画面中」「镜头转向」

只输出旁白文案，不要解释。
```

Call via `build_payload.generate_cinematic_narration()`.

### Mode B — Whisper + Koubo Analysis

Run `scripts/whisper_transcribe.py` → detect silent gaps > 1.5s → score segments → apply koubo cuts → enforce 90s budget.

### Clip List Format (共用)

```python
clips = [
    {
        "clip_id":            "clip_001",
        "start_time":         0.0,       # seconds in source video
        "end_time":           6.3,       # seconds in source video
        "narration_text":     "眼前这个陆永瑜，只是举报了父亲的贪腐...",
        "keep_original_audio": False,    # True = keep source audio, no TTS
        "stage":              "起因",
        "speaker_name":       None,
    },
    ...
]
```

---

## Step 3: Approval Gate

**MANDATORY** — Show the FULL detailed clip plan BEFORE generating any files.
Include every clip with: index, source timestamp, stage, estimated duration, full narration text.

```
╔══════════════════════════════════════════════════════════════════════╗
║  📋 《误判(1)》剪辑方案预览  共 8 段 | 预估总时长：约 52 秒          ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ clip_001 ────────────────────────────────────────────────────────┐
│  阶段：起因                                                         │
│  源片段：00:02:15 → 00:02:22  (约 7s)                              │
│  旁白文案：                                                          │
│  「眼前这个陆永瑜，只是举报了父亲的贪腐行为，才发现自己              │
│    已经踏入了一个无法回头的深渊...」                                  │
│  音频：narration_clip_001.mp3 | 视频：clip_001.mp4                  │
└───────────────────────────────────────────────────────────────────┘

┌─ clip_002 ────────────────────────────────────────────────────────┐
│  阶段：发展                                                          │
│  源片段：00:18:40 → 00:18:46  (约 6s)                              │
│  旁白文案：                                                          │
│  「随后，陆金强悄悄接触了关键证人，一场精心设计的陷阱，              │
│    正在悄无声息地收紧。」                                             │
│  音频：narration_clip_002.mp3 | 视频：clip_002.mp4                  │
└───────────────────────────────────────────────────────────────────┘

┌─ clip_003 ────────────────────────────────────────────────────────┐
│  阶段：发展                                                          │
│  源片段：00:35:10 → 00:35:16  (约 6s)                              │
│  旁白文案：                                                          │
│  「然而，就在案件似乎尘埃落定之际，律师张远发现了一处细节——          │
│    这个细节，将让所有人的判断彻底崩塌。」                             │
│  音频：narration_clip_003.mp3 | 视频：clip_003.mp4                  │
└───────────────────────────────────────────────────────────────────┘

  ... （以此格式列出所有 N 个片段）

══════════════════════════════════════════════════════════════════════
  项目名称  ：误判(1)
  输出目录  ：video_clipper_output_误判(1)/
  视频比例  ：1920×1080（保持原始）
  旁白语音  ：zh-CN-XiaoxiaoNeural
  旁白总字数：213 字  ✅（目标 200 字，范围 150–250 字）
  预估时长  ：约 64 秒  ✅（目标 60 秒，范围 45–75 秒）
══════════════════════════════════════════════════════════════════════

确认开始生成？(是 / 修改某段文案 / 删除某段 / 全部重新生成)
```

**Rules for this display:**
- Show ALL clips, no truncation — even if there are 20+ clips
- Each clip box must contain: stage, source timestamp range, estimated duration, full narration text, output filenames
- Show project name WITH conflict suffix (e.g. `误判(1)`) so user sees the final name before committing
- Wait for explicit user approval before proceeding to Step 4

---

## Step 4: Generate narration_XXX.mp3

One MP3 per clip. Filename: `narration_clip_001.mp3`, `narration_clip_002.mp3`, ...

```python
import edge_tts, asyncio, subprocess

async def tts_one(text: str, path: str, voice: str):
    tts = edge_tts.Communicate(text.strip("[]"), voice=voice)
    await tts.save(path)

def get_mp3_duration(path: str) -> float:
    """Measure ACTUAL mp3 duration — used to set clip_XXX.mp4 length."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True
    )
    return float(result.stdout.strip())

# Generate + measure
for clip in clips:
    mp3_path = f"{output_dir}/narration_{clip['clip_id']}.mp3"
    asyncio.run(tts_one(clip["narration_text"], mp3_path, tts_voice))
    clip["mp3_path"]      = mp3_path
    clip["mp3_duration"]  = get_mp3_duration(mp3_path)  # ACTUAL seconds
    # Update end_time to match mp3 duration exactly
    clip["end_time"]      = clip["start_time"] + clip["mp3_duration"]
```

**After this step, `clip["mp3_duration"]` is the authoritative duration for all downstream steps.**

---

## Step 5: Generate clip_XXX.mp4

One MP4 per clip. Duration = `clip["mp3_duration"]` exactly.
Filename: `clip_001.mp4`, `clip_002.mp4`, ...

```python
import subprocess, os

def render_clip(clip: dict, video_path: str, output_dir: str,
                original_width: int, original_height: int):
    """
    Extract one clip from source video.
    - Duration locked to mp3_duration (exact match with narration audio)
    - Preserves original aspect ratio
    - Mutes source audio if narration overlay (keep_original_audio=False)
    - Keeps source audio if keep_original_audio=True
    """
    out_path = f"{output_dir}/{clip['clip_id']}.mp4"
    duration = clip["mp3_duration"]  # locked to mp3

    base_cmd = [
        "ffmpeg", "-y",
        "-ss", str(clip["start_time"]),
        "-t",  str(duration),
        "-i",  video_path,
    ]

    if not clip.get("keep_original_audio") and clip.get("mp3_path"):
        # Merge narration audio into clip
        cmd = base_cmd + [
            "-i", clip["mp3_path"],
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "fast",
            "-vf", f"scale={original_width}:{original_height}"
                    ":force_original_aspect_ratio=decrease:flags=lanczos",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", out_path
        ]
    elif clip.get("keep_original_audio"):
        # Keep source audio, no narration
        cmd = base_cmd + [
            "-c:v", "libx264", "-preset", "fast",
            "-vf", f"scale={original_width}:{original_height}"
                    ":force_original_aspect_ratio=decrease:flags=lanczos",
            "-c:a", "aac", "-b:a", "192k",
            out_path
        ]
    else:
        # Silent clip (no audio at all)
        cmd = base_cmd + [
            "-c:v", "libx264", "-preset", "fast",
            "-vf", f"scale={original_width}:{original_height}"
                    ":force_original_aspect_ratio=decrease:flags=lanczos",
            "-an", out_path
        ]

    subprocess.run(cmd, capture_output=True, check=True)
    clip["mp4_path"] = out_path
    print(f"  {clip['clip_id']}.mp4  {duration:.2f}s")
    return out_path
```

---

## Step 6: Generate subtitles.srt

Timestamps derived from `mp3_duration` — NOT from source video timestamps.
Each clip starts where the previous ended (sequential playback timeline).

```python
def generate_srt(clips: list, output_path: str):
    """
    Build SRT where each entry's timing matches the clip's position
    in the final concatenated video, not the source video.
    """
    def fmt(s: float) -> str:
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s%1)*1000):03d}"

    cursor = 0.0  # running position in output video timeline
    entries = []

    for i, clip in enumerate(clips, 1):
        duration = clip["mp3_duration"]
        start    = cursor
        end      = cursor + duration
        text     = clip.get("narration_text") or clip.get("transcript", "")
        speaker  = clip.get("speaker_name")
        label    = f"[{speaker}] {text}" if speaker else text

        entries.append(f"{i}\n{fmt(start)} --> {fmt(end)}\n{label}\n")
        cursor = end  # advance timeline

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(entries))
    print(f"SRT saved: {output_path}  ({len(entries)} entries)")
```

---

## Step 7: Generate JianYing Draft Files

**MUST output exactly 2 files** — both required for a valid importable draft:
1. `draft_meta_info.json`
2. `draft_content.json`

Call `scripts/jianying_draft.py` → `generate_jianying_draft()`.

---

### JianYing Draft Spec (剪映专业版导入规范)

| Field | Rule |
|-------|------|
| `draft_version` | Always `"10.8.0"` |
| Resolution | `1920 × 1080`, frame rate `30` |
| Time unit | **Milliseconds**, 13-digit timestamp |
| Media path | Windows-style: `D:/path/to/clip_001.mp4` |
| Subtitle format | JianYing XML: `<font color="#FFFFFF"><size=60>文字</size></font>` |
| All IDs | Unique, non-repeating (use `uuid4()`) |
| JSON | Strict — no trailing commas, no comments |

---

### draft_meta_info.json

```json
{
  "cloud_package_attributes": "",
  "create_time": 1700000000,
  "draft_cloud_last_action_download": false,
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
  "draft_id": "{uuid}",
  "draft_is_ai_packaging_used": false,
  "draft_is_ai_shorts_used": false,
  "draft_is_ai_translate_used": false,
  "draft_is_article_video_used": false,
  "draft_is_from_deeplink": false,
  "draft_is_invisible": false,
  "draft_materials": [],
  "draft_name": "{project_name}",
  "draft_need_rename": false,
  "draft_new_version": "",
  "draft_removable_storage_device": "",
  "draft_root_path": "{output_dir_abs_path}",
  "draft_timeline_materials_size_": 0,
  "draft_type": "",
  "tm_draft_create": 1700000000,
  "tm_draft_modified": 1700000000,
  "tm_duration": {total_duration_ms}
}
```

---

### draft_content.json Structure

```json
{
  "canvas_config": {
    "height": 1080,
    "ratio": "original",
    "width": 1920
  },
  "color_space": 0,
  "config": {
    "adjust_max_index": 1,
    "attachment_info": [],
    "combination_max_index": 1,
    "export_range": null,
    "extract_audio_last_index": 1,
    "lyrics_recognition_id": "",
    "lyrics_sync": true,
    "lyrics_taskinfo": [],
    "maintrack_adsorb": true,
    "material_save_mode": 0,
    "multi_language_current": "none",
    "multi_language_list": [],
    "multi_language_main": "none",
    "multi_language_mode": "none",
    "original_sound_last_index": 1,
    "record_audio_last_index": 1,
    "sticker_max_index": 1,
    "subtitle_recognition_id": "",
    "subtitle_sync": true,
    "subtitle_taskinfo": [],
    "system_font_list": [],
    "video_mute": false,
    "zoom_info_params": null
  },
  "cover": "",
  "create_time": 0,
  "duration": {total_duration_ms},
  "extra_info": null,
  "fps": 30.0,
  "free_render_index_mode_on": false,
  "group_container": null,
  "id": "{draft_uuid}",
  "keyframe_graph_list": [],
  "keyframes": { "adjusts": [], "audios": [], "effects": [], "filters": [],
                  "handwrites": [], "stickers": [], "texts": [], "videos": [] },
  "lyrics_effects_size_": 0,
  "materials": {
    "audios": [ ...narration_audio_materials... ],
    "videos": [ ...video_clip_materials... ],
    "texts":  [ ...subtitle_text_materials... ]
  },
  "mutable_config": null,
  "name": "{project_name}",
  "new_version": "10.8.0",
  "platform": { "app_id": 3704, "app_source": "lv", "app_version": "5.9.0",
                  "device_id": "", "hard_disk_id": "", "mac_id": "", "os": "windows",
                  "os_version": "" },
  "relationships": [],
  "render_index_track_mode_on": false,
  "retouch_cover": null,
  "source": "default",
  "static_cover_image_path": "",
  "time_marks": null,
  "tracks": [
    {
      "attribute": 0,
      "flag": 0,
      "id": "{track_video_uuid}",
      "is_default_name": true,
      "name": "",
      "segments": [ ...video_segments... ],
      "type": "video"
    },
    {
      "attribute": 0,
      "flag": 0,
      "id": "{track_audio_uuid}",
      "is_default_name": true,
      "name": "",
      "segments": [ ...audio_segments... ],
      "type": "audio"
    },
    {
      "attribute": 0,
      "flag": 0,
      "id": "{track_text_uuid}",
      "is_default_name": true,
      "name": "",
      "segments": [ ...text_segments... ],
      "type": "text"
    }
  ],
  "update_time": 0,
  "version": 360000
}
```

---

### Segment Templates

**Video segment:**
```json
{
  "cartoon": false,
  "clip": {
    "alpha": 1.0,
    "flip": { "horizontal": false, "vertical": false },
    "rotation": 0.0,
    "scale": { "x": 1.0, "y": 1.0 },
    "transform": { "x": 0.0, "y": 0.0 }
  },
  "common_keyframes": [],
  "enable_adjust": true,
  "enable_color_correct_adjust": false,
  "enable_color_wheels": false,
  "enable_lut": false,
  "enable_smart_color_adjust": false,
  "extra_material_refs": [],
  "group_id": "",
  "hdr_settings": null,
  "id": "{segment_uuid}",
  "intensifies_audio": false,
  "is_placeholder": false,
  "is_tone_modify": false,
  "keyframe_refs": [],
  "last_nonzero_volume": 1.0,
  "material_id": "{material_uuid}",
  "render_index": 0,
  "responsive_layout": { "enable": false, "horizontal_pos_layout": 0,
                          "size_layout": 0, "target_follow": "", "vertical_pos_layout": 0 },
  "reverse": false,
  "source_timerange": {
    "duration": {clip_duration_ms},
    "start": {clip_source_start_ms}
  },
  "speed": 1.0,
  "target_timerange": {
    "duration": {clip_duration_ms},
    "start": {timeline_start_ms}
  },
  "template_id": "",
  "template_scene": "default",
  "track_attribute": 0,
  "track_render_index": 0,
  "uniform_scale": { "on": true, "value": 1.0 },
  "visible": true,
  "volume": 0.0
}
```
Note: `volume: 0.0` for narration clips (audio replaced by TTS), `volume: 1.0` for keep_original_audio clips.

**Audio segment (narration TTS):**
```json
{
  "app_id": 0,
  "category_id": "",
  "category_name": "local",
  "check_flag": 63487,
  "duration": {mp3_duration_ms},
  "effect_id": "",
  "id": "{segment_uuid}",
  "intensifies_path": "",
  "is_ai_clone_tone": false,
  "is_text_edit_overdub": false,
  "is_unified_beauty_mode": false,
  "local_material_id": "{audio_material_uuid}",
  "material_id": "{audio_material_uuid}",
  "material_name": "narration_{clip_id}",
  "render_index": 0,
  "source_timerange": { "duration": {mp3_duration_ms}, "start": 0 },
  "speed": 1.0,
  "target_timerange": { "duration": {mp3_duration_ms}, "start": {timeline_start_ms} },
  "type": "extract_music",
  "volume": 1.0
}
```

**Text segment (subtitle):**
```json
{
  "content": "{subtitle_xml}",
  "id": "{segment_uuid}",
  "is_style_definition_segment": false,
  "keyframe_refs": [],
  "material_id": "{text_material_uuid}",
  "render_index": 0,
  "target_timerange": { "duration": {mp3_duration_ms}, "start": {timeline_start_ms} },
  "track_attribute": 0,
  "track_render_index": 0,
  "visible": true,
  "z_index": 0
}
```

**Subtitle XML format (字幕必须用剪映 XML 格式):**
```xml
<font color="#FFFFFF"><size=60>眼前这个陆永瑜，只是举报了父亲的贪腐行为</size></font>
```

---

### Material Templates

**Video material:**
```json
{
  "audio_fade": null,
  "cartoon_path": "",
  "category_id": "",
  "category_name": "",
  "check_flag": 63487,
  "crop": { "lower_left_x": 0.0, "lower_left_y": 1.0, "lower_right_x": 1.0,
             "lower_right_y": 1.0, "upper_left_x": 0.0, "upper_left_y": 0.0,
             "upper_right_x": 1.0, "upper_right_y": 0.0 },
  "crop_ratio": "free",
  "crop_scale": 1.0,
  "duration": {clip_duration_ms},
  "extra_type_option": 0,
  "file_Path": "D:/{output_dir}/{clip_id}.mp4",
  "formula_id": "",
  "id": "{material_uuid}",
  "import_time": 1700000000,
  "import_time_ms": 1700000000000,
  "item_source": 1,
  "md5": "",
  "metetype": "video",
  "roughcut_time_range": { "duration": -1, "start": -1 },
  "sub_time_range": { "duration": -1, "start": -1 },
  "type": "video",
  "video_algorithm": { "algorithms": [], "deflicker": null, "motion_blur_config": null,
                        "noise_reduction": null, "path": "", "quality_enhance": null,
                        "time_range": null },
  "width": 1920,
  "height": 1080
}
```

**Audio material:**
```json
{
  "app_id": 0,
  "category_id": "",
  "category_name": "local",
  "check_flag": 63487,
  "duration": {mp3_duration_ms},
  "effect_id": "",
  "file_Path": "D:/{output_dir}/narration_{clip_id}.mp3",
  "formula_id": "",
  "id": "{material_uuid}",
  "import_time": 1700000000,
  "import_time_ms": 1700000000000,
  "item_source": 1,
  "md5": "",
  "metetype": "music",
  "name": "narration_{clip_id}",
  "roughcut_time_range": { "duration": -1, "start": -1 },
  "sub_time_range": { "duration": -1, "start": -1 },
  "type": "extract_music"
}
```

**Text material:**
```json
{
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
  "content": "{subtitle_xml}",
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
  "font_time_range": { "duration": 0, "start": 0 },
  "font_title": "新标准黑",
  "font_url": "",
  "fonts": [],
  "force_apply_line_max_width": false,
  "global_alpha": 1.0,
  "group_id": "",
  "has_shadow": true,
  "id": "{material_uuid}",
  "initial_scale": 1.0,
  "is_rich_text": false,
  "italic": false,
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
  "shadow_point": { "x": 0.6364, "y": -0.6364 },
  "shadow_smoothing": 0.45,
  "shape_clip_x": false,
  "shape_clip_y": false,
  "style_name": "",
  "sub_type": 0,
  "text_alpha": 1.0,
  "text_color": "#FFFFFF",
  "text_curve": null,
  "text_preset_resource_id": "",
  "text_size": 60,
  "text_to_audio_ids": [],
  "tts_auto_update": false,
  "type": "text",
  "typesetting": 0,
  "underline": false,
  "underline_offset": 0.22,
  "underline_width": 0.05,
  "use_effect_default_color": true,
  "words": { "end_time": [], "start_time": [], "text": [] }
}
```

---

### Time Conversion Rules

```python
def ms(seconds: float) -> int:
    """Convert seconds to milliseconds (13-digit JianYing timestamp)."""
    return int(seconds * 1000)

# Timeline cursor — accumulates as clips are placed
cursor_ms = 0
for clip in clips:
    clip_duration_ms   = ms(clip["mp3_duration"])
    clip_source_start  = ms(clip["start_time"])     # position IN source video
    timeline_start     = cursor_ms                   # position IN output timeline
    cursor_ms         += clip_duration_ms            # advance cursor
```

---

### Python Generator Function

```python
from scripts.jianying_draft import generate_jianying_draft

meta, content = generate_jianying_draft(
    project_name    = project_name,        # already conflict-resolved
    clips           = clips,               # with mp3_duration + mp4_path + mp3_path
    output_dir      = output_dir,          # abs path, used in file_Path fields
    original_width  = 1920,
    original_height = 1080
)

import json, os
os.makedirs(output_dir, exist_ok=True)
with open(f"{output_dir}/draft_meta_info.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
with open(f"{output_dir}/draft_content.json", "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)
```

---

## Step 8: Final Output Message

```
✅ 生成完成！

📁 输出目录: video_clipper_output/

  配音文件 (narration_*.mp3):
    narration_clip_001.mp3   6.34s
    narration_clip_002.mp3   5.81s
    ... 共 N 个

  视频切片 (clip_*.mp4):
    clip_001.mp4   6.34s  ← 与 narration_clip_001.mp3 精确对齐
    clip_002.mp4   5.81s  ← 与 narration_clip_002.mp3 精确对齐
    ... 共 N 个

  字幕文件:
    subtitles.srt  (N 条，时间轴与 mp3 严格对应)

  剪映草稿:
    draft_content.json
```

**首次使用时，额外显示剪映草稿导入指引：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 剪映草稿导入方法（首次使用）

草稿目录：
  Windows: C:\Users\{用户名}\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft\
  macOS:   ~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/

步骤：
  1. 在草稿目录下新建一个文件夹（随意命名）
  2. 将 draft_content.json 放入该文件夹
  3. 打开剪映 → 首页 → 找到刚才的草稿 → 点击「继续编辑」
  4. clip_XXX.mp4 已含旁白音频，可直接在剪映时间轴使用
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

只在以下情况显示导入指引：
- 用户第一次运行（对话中无历史记录）
- 用户说"不知道怎么导入" / "草稿在哪"

---

## Timing Alignment Rules (CRITICAL)

```
mp3_duration  →  controls everything downstream
      │
      ├──► clip_XXX.mp4 duration  = mp3_duration  (ffmpeg -t flag)
      │
      ├──► subtitles.srt timing   = cumulative sum of mp3_durations
      │         clip_001: 00:00:00,000 → 00:00:06,340
      │         clip_002: 00:00:06,340 → 00:00:12,160
      │         clip_003: 00:00:12,160 → ...
      │
      └──► draft_content.json srt_start / srt_end  = same values
```

**Never use source video timestamps for srt. Always use mp3_duration.**

---

## API Keys

| Service | Key | Purpose |
|---------|-----|---------|
| Anthropic Claude | auto (OpenClaw) | LLM narration generation |
| Qwen-VL-Plus | `QWEN_API_KEY` env var | Silent scene description (Mode B) |
| edge-tts | no key needed | TTS narration MP3 |
| Whisper | local, no key | Speech transcription (Mode B) |

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| ffprobe / ffmpeg not found | `apt install ffmpeg` / `brew install ffmpeg` / ffmpeg.org |
| TTS fails for a clip | Retry once; if still fails, set `mp3_duration = estimated_seconds`, flag in report |
| ffmpeg clip render fails | Log and skip; include in report as failed clips |
| LLM narration API error | Fall back to raw event description; rewrite style manually |
| Whisper OOM (Mode B) | Switch to `base` model or chunk into 10-min segments |
| Qwen-VL-Plus error | Use rule-based fallback narration |

---

## Dependencies

```bash
pip install edge-tts openai openai-whisper --break-system-packages
# FFmpeg: https://ffmpeg.org/download.html
```

---

## Scripts

- `scripts/build_payload.py`     — clip analysis, LLM narration, render_output_video, clips_to_draft
- `scripts/narration_audio.py`   — edge-tts generation, SRT builder, report
- `scripts/whisper_transcribe.py`— Mode B speech transcription
- `scripts/run_clip_pipeline.py` — end-to-end CLI
