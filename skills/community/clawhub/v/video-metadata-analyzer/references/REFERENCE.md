# Video Metadata Analyzer — Full Technical Reference

> Complete parameter reference, output schemas, standalone usage, and error handling details.
> This file is loaded on demand when the agent needs deep technical details.

> ⚠️ **Privacy:** Modes marked 🌐 send data to external endpoints. See [SKILL.md Privacy Notice](../SKILL.md) for details.

## Complete Parameter Reference

### `run.sh` — Main Orchestrator

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--video PATH` | **Yes** | — | Input video file path |
| `--output DIR` | **Yes** | — | Output directory (auto-created) |
| `--max-frames N` | No | `15` | Max frames per 4-minute segment |
| `--keep-frames` | No | `false` | Keep frame images (auto-cleaned by default) |
| `--transcribe MODE` | No | `agent-direct` | Audio mode: `local` / `cloud` 🌐 / `agent-direct` / `audio-llm` 🌐 |
| `--whisper-model MODEL` | No | `base` | Local Whisper model size (tiny/base/small/medium/large) |
| `--whisper-api-key KEY` | No | — | Cloud Whisper API key (`--transcribe cloud`) |
| `--whisper-api-base URL` | No | — | Cloud Whisper API base URL (`--transcribe cloud`) |
| `--whisper-api-model MODEL` | No | `whisper-1` | Cloud Whisper model name |
| `--vision-llm-key KEY` | No | — | Vision LLM API key. Omit = preprocess-only (placeholder observations) |
| `--vision-llm-base URL` | No | — | Vision LLM API base URL |
| `--vision-llm-model MODEL` | No | — | Vision LLM model (must support `image_url` in chat completions) |
| `--audio-llm-key KEY` | No | — | Audio LLM API key (`--transcribe audio-llm`) |
| `--audio-llm-base URL` | No | — | Audio LLM API base URL |
| `--audio-llm-model MODEL` | No | — | Audio LLM model (must support `input_audio` in chat completions) |
| `--synthesize-method METHOD` | No | — | `api` / `agent` / `manual`. Omit = observe only (no metadata.json) |
| `--analyze-llm-key KEY` | No | — | Synthesize LLM API key (required for `api` method) |
| `--analyze-llm-base URL` | No | — | Synthesize LLM API base URL |
| `--analyze-llm-model MODEL` | No | — | Synthesize LLM model name |

**Note:** `--interval` is deprecated and ignored. Interval is auto-calculated per segment.

### Timeout Protection

`run.sh` wraps itself with `exec timeout $VA_TIMEOUT` on first invocation (default 3600s = 1 hour). Override via environment:

```bash
VA_TIMEOUT=7200 bash scripts/run.sh --video input.mp4 --output /tmp/out ...
```

The timeout covers the entire pipeline (frame extraction + LLM analysis + synthesis).

### Fallback / Degradation

- `--transcribe` omitted → defaults to `agent-direct`
- `--transcribe audio-llm` but missing key/base/model → falls back to `agent-direct` + warning
- `--transcribe cloud` but missing `--whisper-api-key` → falls back to `agent-direct` + warning
- `--synthesize-method api` but missing `--analyze-llm-key/base/model` → skips synthesis entirely + warning
- No `--vision-llm-key` → preprocess-only mode (extracts frames, outputs placeholder observations)

---

## `common.py` — Shared Utilities

Three functions used across all scripts. No external dependencies.

### `http_request_with_retry(req, ctx=None, timeout=180, max_retries=3, label="API")`

HTTP request with exponential backoff. Retries on:
- HTTP 5xx errors
- ConnectionError / TimeoutError / OSError

Wait: `2^attempt` seconds (2s, 4s for attempts 2 and 3).

### `get_media_duration(path) → float`

Returns audio/video file duration in seconds via `ffprobe`.

### `parse_json_from_llm(content, expect_array=False) → dict | list | None`

Extracts JSON from LLM output:
- Handles bare JSON and ` ```json ... ``` ` wrapped output
- `expect_array=True` → tries to extract array first
- Returns `None` on any parse failure

---

## `visual.py` — Frame Extraction + Visual Observation

### Frame Extraction Strategy

| Video Length | Segments | Interval | Frames/seg | API Calls |
|-------------|----------|----------|-----------|-----------|
| ≤ 4 min | 1 | adaptive (`duration/max_frames`) | ≤ 15 | 1 |
| 8 min | 2 | 16s (full) / adaptive (tail) | ≤ 15 | 2 parallel |
| 30 min | 8 | 16s | ≤ 15 | up to 4 parallel |
| 2 hours | 30 | 16s | ≤ 15 | up to 4 parallel |

**Constants:** `SEGMENT_SECONDS = 240` (4 min), `MAX_FRAMES_PER_SEGMENT = 20` (code limit, default `--max-frames 15`).

**Parallel processing:** `ThreadPoolExecutor(max_workers=min(segments, 4))` for long videos.

**Frame compression:** Frames >200KB auto-resized to max 1280px width, JPEG quality 85. Pillow preferred; ffmpeg fallback if Pillow unavailable.

### Observation Prompt Fields

| Field | Type | Description |
|-------|------|-------------|
| `frame` | string | Filename (e.g. `frame_001.jpg`) |
| `objects` | string[] | Key entities (people, devices, UI elements). **Source of truth for `desc`** |
| `desc` | string | ~100 char Chinese paragraph, 5W1H (Who/What/When/Where/Why/How). Who must use `objects` names |
| `texts` | string | All readable text, comma-separated. Empty string if none |
| `actions` | string[] | Events/actions happening in frame |
| `style` | string | Style tags (科技感/教程/日常/娱乐/卡通/纪录片 etc.) |
| `cover_candidate` | boolean | `true` if high info density + clear text + visual impact |

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--video` | Yes | — | Input video file |
| `--output-dir` | Yes | — | Output directory |
| `--max-frames` | No | `15` | Max frames per 4-min segment |
| `--keep-frames` | No | `false` | Keep frame images |
| `--vision-llm-key` | No | — | Vision LLM API key |
| `--vision-llm-base` | No | — | Vision LLM API base URL |
| `--vision-llm-model` | No | — | Vision LLM model (must support `image_url`) |

### Standalone Usage

```bash
# Full mode with vision LLM
python3 scripts/visual.py --video input.mp4 --output-dir /tmp/out \
  --vision-llm-key KEY --vision-llm-base URL --vision-llm-model MODEL

# Preprocess-only (extract frames, no API calls)
python3 scripts/visual.py --video input.mp4 --output-dir /tmp/out --keep-frames
```

---

## `transcribe.py` — Audio Extraction + Transcription

### Four Transcription Modes

| Mode | How it works | Requirements | Output |
|------|-------------|-------------|--------|
| `audio-llm` | Sends audio via `input_audio` in chat completions to multimodal LLM | `--audio-llm-key/base/model` | Structured JSON (transcript + speakers + key_points + tone) |
| `cloud` | OpenAI-compatible `/audio/transcriptions` endpoint | `--whisper-api-key` + `--whisper-api-base` | Plain text transcript |
| `local` | Local Whisper model | `pip install openai-whisper` | Plain text transcript |
| `agent-direct` | Extracts audio to WAV only. Agent reads it directly. | ffmpeg only | Empty transcript + `audio_file` path |

### Audio Processing Pipeline (audio-llm mode)

```
Video → ffmpeg extract MP3 (64kbps mono)
  → size check: base64 estimate > 10MB?
    → YES: split_audio() → chunks with 2s overlap
         → transcribe each chunk via _call_audio_llm_single()
         → merge_transcripts() dedup overlap
         → _extract_structured_from_text() → final structured JSON
    → NO: _call_audio_llm_single() directly → structured JSON
```

### Audio Prompt Fields (audio-llm mode)

| Field | Type | Description |
|-------|------|-------------|
| `transcript` | string | Complete transcription (Chinese, original sentence breaks preserved). If no speech, write a short note like "（无语音内容，仅包含背景音乐和游戏音效）" |
| `speakers` | string[] | Speaker identification (e.g. `["主讲"]`). Empty array if no speech |
| `key_points` | string[] | 3-8 key information points from speech. If no speech, describe audio features (BGM, SFX, clicks, etc.) |
| `tone` | string | Voice style (平稳/激动/正式/随意/幽默). If no speech: "无语音（纯音效/音乐）" |

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--video` | Yes | Input video file |
| `--output` | Yes | Output JSON path |
| `--mode` | Yes | One of: `local`, `cloud`, `agent-direct`, `audio-llm` |
| `--whisper-model` | No | Local Whisper model size (default: `base`) |
| `--api-key` | Conditional | Cloud Whisper API key (`cloud` mode) |
| `--api-base` | Conditional | Cloud Whisper API base URL (`cloud` mode) |
| `--audio-llm-key` | Conditional | Audio LLM API key (`audio-llm mode`) |
| `--audio-llm-base` | Conditional | Audio LLM API base URL (`audio-llm mode`) |
| `--audio-llm-model` | Conditional | Audio LLM model (`audio-llm mode`) |

### Standalone Usage

```bash
# Audio-LLM mode (recommended)
python3 scripts/transcribe.py --video input.mp4 --output obs.json \
  --mode audio-llm \
  --audio-llm-key KEY --audio-llm-base URL --audio-llm-model mimo-v2.5

# Cloud Whisper
python3 scripts/transcribe.py --video input.mp4 --output obs.json \
  --mode cloud --whisper-api-key KEY --whisper-api-base URL

# Local Whisper
python3 scripts/transcribe.py --video input.mp4 --output obs.json \
  --mode local --whisper-model base

# Agent-direct (extract only)
python3 scripts/transcribe.py --video input.mp4 --output obs.json \
  --mode agent-direct
```

---

## `analyze.py` — Metadata Synthesis

### Three Synthesis Methods

| Method | How it works | Output |
|--------|-------------|--------|
| `api` 🌐 | Calls external LLM via `--api-key/base/model`. 3× JSON parse retry. Falls back to heuristic `synthesize_agent()` on total failure | `metadata.json` (JSON) |
| `agent` | Writes system prompt + observations as Markdown. Agent reads it and generates metadata itself | `metadata.json` (Markdown prompt; Agent writes actual JSON) |
| `manual` | Converts observations to human-readable Markdown | `metadata.json` (Markdown) |

### Synthesis Prompt Design (api/agent modes)

**System prompt** frames the LLM as "资深 B 站内容运营":

- **Title**: Like a real creator would write. Informative, distinctive. 严禁 AI clichés (深入浅出, 全面解析, 带你了解)
- **Intro**: Helps viewers decide "is this video for me?". Natural language, not summary — preview
- **Tags**: From content, specific to video's domain, no generic tags
- **Category**: Must match Bilibili's actual category tree
- **Cover suggestion**: Which frame + why (info density / visual impact / text clarity)

Title examples in prompt:
- ✅ `"用 AI Agent 自动审查代码缺陷，我把自家项目翻了个底朝天"`
- ✅ `"ESP32 心率监测器：20 块钱的方案也能跑"`
- ❌ `"AI Agent 技术分享"` — 空泛

### Heuristic Fallback: `synthesize_agent()`

When `api` method fails all retries, falls back to rule-based generation:
- **Title**: First `key_point` (≤80 chars) → first sentence of transcript → first frame desc
- **Intro**: key_points (bulleted) + transcript excerpt (≤500 chars)
- **Tags**: From style + objects + key_points (regex: 2-6 char Chinese/English words)
- **Category**: Keyword matching (科技/游戏/音乐 + sub-categories)
- **Cover**: First frame with `cover_candidate: true`, auto-generated reason
- **Declaration**: Keyword detection (AI生成 → "含AI生成内容", else "内容无需标注")

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--observations-visual` | Yes | Path to observations_visual.json |
| `--observations-audio` | Yes | Path to observations_audio.json |
| `--output` | Yes | Output file path |
| `--method` | No | `api` / `agent` / `manual` (default: `manual`) |
| `--api-key` | For `api` | LLM API key |
| `--api-base` | For `api` | LLM API base URL |
| `--model` | For `api` | LLM model name |

### Standalone Usage

```bash
# API mode
python3 scripts/analyze.py \
  --observations-visual obs_v.json --observations-audio obs_a.json \
  --output metadata.json --method api \
  --api-key KEY --api-base URL --model gpt-5.5

# Agent mode
python3 scripts/analyze.py \
  --observations-visual obs_v.json --observations-audio obs_a.json \
  --output metadata.json --method agent

# Manual mode
python3 scripts/analyze.py \
  --observations-visual obs_v.json --observations-audio obs_a.json \
  --output metadata.md --method manual
```

---

## Output Schemas

### `observations_visual.json`

JSON array, one object per frame, sorted by (segment_index, frame_number):

```json
[
  {
    "frame": "frame_001.jpg",
    "objects": ["研究员", "实验设备"],
    "desc": "深色科技界面中，研究员正在调试大型实验设备...",
    "texts": "实验参数,2026-05",
    "actions": ["调试设备参数"],
    "style": "科技感/深色系",
    "cover_candidate": true,
    "segment": 0,
    "segment_start": 0.0
  }
]
```

On parse failure after all retries, placeholder entries are generated:
```json
{
  "frame": "frame_001.jpg",
  "objects": [],
  "desc": "(LLM output unparseable) <first 200 chars>",
  "texts": "",
  "actions": [],
  "style": "",
  "cover_candidate": false,
  "segment": 0,
  "segment_start": 0.0,
  "parse_failed": true
}
```

### `observations_audio.json`

```json
{
  "transcript": "大家好，这是一个测试视频...",
  "speakers": ["主讲"],
  "key_points": ["这是一个测试视频", "用于验证转写功能"],
  "tone": "平稳"
}
```

For `agent-direct` mode, includes `audio_file` path:
```json
{
  "transcript": "",
  "audio_file": "/path/to/transcript.wav",
  "speakers": [],
  "key_points": [],
  "tone": ""
}
```

### `metadata.json`

```json
{
  "title": "80字以内，像 UP 主写的标题",
  "intro": "2000字以内，给观众看的视频介绍",
  "tags": ["标签1", "标签2"],
  "category": "B站一级分区（2026-05 type2 平铺，共30个）",
  "cover_suggestion": {
    "primary": "frame_001.jpg",
    "reason": "为什么这帧适合做封面",
    "secondary": "frame_010.jpg"
  },
  "declaration": "内容无需标注",
  "copyright_claim": false,
  "watermark": true,
  "author_marks": []
}
```

**Field reference:**
- `title` (string, ≤80 chars): Human-readable title
- `intro` (string, ≤2000 chars): Natural language video introduction
- `tags` (string[], ≤10, each ≤20 chars): Content-specific tags
- `category` (string): Bilibili type2 flat category, one of: 影视 | 娱乐 | 音乐 | 舞蹈 | 动画 | 绘画 | 鬼畜 | 游戏 | 资讯 | 知识 | 人工智能 | 科技数码 | 汽车 | 时尚美妆 | 家装房产 | 户外潮流 | 健身 | 体育运动 | 手工 | 美食 | 小剧场 | 旅游出行 | 三农 | 动物 | 亲子 | 健康 | 情感 | vlog | 生活兴趣 | 生活经验
- `cover_suggestion.primary` (string): Recommended frame filename
- `cover_suggestion.reason` (string): Why this frame works
- `cover_suggestion.secondary` (string): Backup frame filename
- `declaration` (string): One of: `"内容无需标注"` | `"含AI生成内容"` | `"含虚构演绎内容"` | `"内容含营销信息"` | `"个人观点，仅供参考"` | `"内容为转载"`
- `copyright_claim` (boolean): Whether to check "自制". Default `false`
- `watermark` (boolean): Whether to enable B站 original watermark. Default `true`
- `author_marks` (string[]): Optional multi-select author declarations. Each must be one of the 6 standard B站 author marks, or empty array

---

## Error Handling: Three-Layer Defense

### Layer 1: HTTP Retry

`http_request_with_retry()` applied to all API calls:
- 3 retries with exponential backoff (2s, 4s) on 5xx / connection errors
- Applied to: vision LLM, audio LLM, Whisper API, synthesize LLM

### Layer 2: JSON Parse Retry

Multi-round JSON parsing with error feedback:

| Script | Function | Attempts | Mechanism |
|--------|----------|----------|-----------|
| `visual.py` | `observe_segment()` | 1 initial + 2 retries | Error message + previous output sent back to LLM |
| `transcribe.py` | `_call_audio_llm_single()` | 3 attempts | Same |
| `transcribe.py` | `_extract_structured_from_text()` | 3 attempts | Same |
| `analyze.py` | `synthesize_api()` | 3 attempts | Same |

Each retry sends the parse error + previous LLM output as a follow-up message.

### Layer 3: Graceful Degradation

| Script | On total failure |
|--------|-----------------|
| `visual.py` | Placeholder entries: `{objects:[], desc:"(LLM output unparseable)", parse_failed:true}` |
| `transcribe.py` | Raw LLM text preserved: `{transcript: "<raw>", speakers:[], key_points:[], tone:""}` |
| `analyze.py` | Falls back to `synthesize_agent()` heuristic |
| `run.sh` | Missing credentials → auto falls back to `agent-direct` |

---

## Complete Usage Examples

### Full pipeline (recommended)

```bash
bash scripts/run.sh \
  --video my_video.mp4 --output /tmp/va-out \
  --transcribe audio-llm \
  --audio-llm-key KEY --audio-llm-base https://api.example.com/v1 --audio-llm-model mimo-v2.5 \
  --vision-llm-key KEY --vision-llm-base https://api.example.com/v1 --vision-llm-model mimo-v2.5 \
  --max-frames 15 \
  --synthesize-method api \
  --analyze-llm-key KEY --analyze-llm-base https://api.example.com/v1 --analyze-llm-model gpt-5.5
```

### Agent-direct mode (no external API)

```bash
bash scripts/run.sh \
  --video my_video.mp4 --output /tmp/va-out \
  --keep-frames
# Agent reads frames and audio file directly, generates observations and metadata
```

### Observe only, synthesize later

```bash
# Step 1: observe only
bash scripts/run.sh \
  --video my_video.mp4 --output /tmp/va-out \
  --transcribe audio-llm \
  --audio-llm-key KEY --audio-llm-base URL --audio-llm-model MODEL \
  --vision-llm-key KEY --vision-llm-base URL --vision-llm-model MODEL

# Step 2: synthesize separately (can use different model)
python3 scripts/analyze.py \
  --observations-visual /tmp/va-out/observations_visual.json \
  --observations-audio /tmp/va-out/observations_audio.json \
  --output /tmp/va-out/metadata.json --method agent
```

### Mixed: API vision + local Whisper

```bash
bash scripts/run.sh \
  --video my_video.mp4 --output /tmp/va-out \
  --transcribe local --whisper-model small \
  --vision-llm-key KEY --vision-llm-base URL --vision-llm-model MODEL \
  --synthesize-method api \
  --analyze-llm-key KEY --analyze-llm-base URL --analyze-llm-model MODEL
```

### Same key for all three LLMs

If your provider supports vision + audio + text in one model:

```bash
bash scripts/run.sh \
  --video my_video.mp4 --output /tmp/va-out \
  --transcribe audio-llm \
  --audio-llm-key KEY --audio-llm-base URL --audio-llm-model mimo-v2.5 \
  --vision-llm-key KEY --vision-llm-base URL --vision-llm-model mimo-v2.5 \
  --synthesize-method api \
  --analyze-llm-key KEY --analyze-llm-base URL --analyze-llm-model mimo-v2.5
```
