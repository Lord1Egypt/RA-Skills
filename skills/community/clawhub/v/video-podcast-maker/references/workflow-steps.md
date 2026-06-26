# Video Podcast Maker — Workflow Steps Reference

> **When to load:** Claude loads this file during workflow execution for detailed step instructions.

---

## Pre-workflow: Design Reference (Optional)

When the user provides a reference video/image with their video creation request:

1. Run extraction: `python3 learn_design.py <input>`
2. Read extracted frames using the Read tool (Claude Vision)
3. Analyze against design-guide.md component vocabulary
4. Present design analysis report to user
5. User confirms/adjusts extracted attributes
6. Apply as session overrides for this video (do NOT save to library unless user asks)

---

## Startup: Load User Preferences

**Agent behavior:** Auto-execute before Step 1, no user interaction needed.

1. Check if `user_prefs.json` exists in `${CLAUDE_SKILL_DIR}`
2. If not, copy from `${CLAUDE_SKILL_DIR}/user_prefs.template.json`
3. Read preferences, **check version and migrate if needed**, then apply in subsequent steps

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"
PREFS_FILE="$SKILL_DIR/user_prefs.json"
TEMPLATE_FILE="$SKILL_DIR/user_prefs.template.json"

if [ ! -f "$PREFS_FILE" ]; then
  cp "$TEMPLATE_FILE" "$PREFS_FILE"
  echo "✓ Created default preferences"
fi
```

### Preference Migration

After loading `user_prefs.json`, check the `version` field and migrate if outdated:

| From | To | Migration |
|------|----|-----------|
| `1.0` | `1.1` | Add top-level `topic_patterns`, `style_profiles`, `design_references`, `learning_history` |
| `1.1` | `1.2` | Convert `tts.voice` (string) → `tts.voices` (per-backend object, preserving user's voice for azure/edge); Add `bgm` preferences (volume, track, tracks library) |
| `1.2` | `1.3` | Add `platform: "bilibili"`, `language: "zh-CN"`, `cta`, `subtitle` fields; expand `progressBar` from boolean to `{ enabled: <old_value>, height: 6, fontSize: 18, activeColor: "auto", position: "bottom" }`; add `content.chapters: true` |

**Migration rules:**
- Preserve all existing user values — never overwrite what the user has customized
- Only add missing fields with defaults from `user_prefs.template.json`
- When migrating `tts.voice` → `tts.voices`: use the old voice value for `azure` and `edge`, use defaults for `doubao` and `cosyvoice`
- v1.3 → v1.4: No structural changes. Platform enum now accepts `"xiaohongshu"`. Update `version` to `"1.4"`.
- v1.4 → v1.5: No structural changes. Platform enum now accepts `"douyin"`. Update `version` to `"1.5"`.
- v1.5 → v1.6: No structural changes. Platform enum now accepts `"weixin-channels"`. Update `version` to `"1.6"`.
- After migration, update `version` to `"1.6"` and save the file
- Print: `"✓ Migrated preferences from v{old} to v1.6"`

4. At Step 1 start, inform user of active preferences (if customized):

```
"Based on your preferences:
 - Platform: [platform] | Language: [language]
 - TTS: [tts.backend] / [tts.voices[backend]]
 - Speech rate: [tts.rate]
 - BGM: [bgm.track] at volume [bgm.volume]
 - Subtitles: [enabled/disabled] | CTA: [cta.type]

Say 'set platform youtube' or 'set language en-US' to change.
Say 'show preferences' to see all details."
```

---

## Step 1: Define Topic Direction

**Auto mode:** Infer all decisions from the user's topic description. Use sensible defaults (audience: general, style: educational intro, tone: professional-casual, duration: medium 3-7min). Save directly to `videos/{name}/topic_definition.md`.

**Interactive mode:** Confirm each item (use `brainstorming` skill if available, otherwise ask directly):
1. **Target audience**: developers / general / students / professionals
2. **Video style**: educational intro / deep analysis / news brief / hands-on tutorial
3. **Content scope**: background / technical principles / usage / comparison
4. **Tone**: serious / casual / fast-paced
5. **Duration**: short (1-3min) / medium (3-7min) / long (7-15min)

Save to `videos/{name}/topic_definition.md`

---

## Step 2: Research Topic

Use WebSearch and WebFetch. Save to `videos/{name}/topic_research.md`.

---

## Step 3: Design Video Sections

Design 5-7 sections:
- Hero/Intro (15-25s)
- Core concepts (30-45s each)
- Demo/Examples (30-60s)
- Comparison/Analysis (30-45s)
- Summary (20-30s)

### Content Density Selection

Assign each section a density tier:

| Tier | Items | Best For |
|------|-------|----------|
| **Impact** | 1 | Hook, hero, CTA, brand moment — largest text |
| **Standard** | 2-3 | Features, comparison, demo |
| **Compact** | 4-6 | Feature grid, ecosystem |
| **Dense** | 6+ | Data tables, detailed comparisons — smallest text |

### Topic Type Detection

> **Planned feature.** Currently, topic-specific styles are applied manually via `user_prefs.json` under `topic_patterns`. Auto-detection from keywords is not yet implemented.

### Title Position

**Auto mode:** Use `top-center` (default).
**Interactive mode:** Ask user: top-center (recommended) / top-left / full-center.

**Rule:** Keep title position consistent within a single video.

---

## Step 4: Write Narration Script

**Preference application:** Adjust script style from `user_prefs.content`:
- `tone: professional` → formal language
- `tone: casual` → conversational, interjections ok
- `verbosity: concise` → 50-80 chars per paragraph
- `verbosity: detailed` → 100-150 chars per paragraph
- `heroOpening` (if set) → use as fixed hero opening line
- `outroClosing` (if set) → use as fixed outro closing line

Create `videos/{name}/podcast.txt` with section markers:

```text
[SECTION:hero]
{heroOpening}（话题引入）...

[SECTION:features]
它有以下功能...

[SECTION:demo]
让我演示一下...

[SECTION:summary]
总结一下，xxx是目前最xxx的xxx。

[SECTION:references]
本期视频参考了官方文档和技术博客。

[SECTION:outro]
{outroClosing}
```

**Numbers MUST use Chinese pronunciation** for correct TTS:

| Type | Wrong | Correct |
|------|-------|---------|
| Integer | 29, 3999 | 二十九，三千九百九十九 |
| Decimal | 1.2, 3.5 | 一点二，三点五 |
| Percentage | 15%, -10% | 百分之十五，负百分之十 |
| Date | 2025-01-15 | 二零二五年一月十五日 |
| Large number | 6144 | 六千一百四十四 |
| English units | 128GB | 一百二十八G |

**Section notes**:
- **hero**: MUST start with `content.heroOpening` if set in user_prefs, followed by the topic hook
- **summary**: Pure content summary, no interaction prompts
- **references** (optional): One sentence about sources
- **outro**: MUST use `content.outroClosing` if set in user_prefs. Fallback: platform-specific CTA
- Empty `[SECTION:xxx]` = silent section

### Script Template Selection

Copy the script template based on `language`:
- `zh-CN` → `${CLAUDE_SKILL_DIR}/templates/podcast_zh.txt`
- `en-US` → `${CLAUDE_SKILL_DIR}/templates/podcast_en.txt`

### Outro Text by Platform + Language

| Platform | zh-CN | en-US |
|----------|-------|-------|
| bilibili | "一键三连！评论区留言，下期再见！" | "Like, coin, and favorite! Leave a comment, see you next time!" |
| youtube | "点赞订阅转发！评论区留言，下期再见！" | "Like, subscribe, and share! Leave a comment, see you next time!" |
| xiaohongshu | "点赞收藏加关注，评论区见！" | "Like, save & follow! See you in comments!" |
| douyin | "点赞关注，评论区见！" | "Like & follow! See you in comments!" |
| weixin-channels | "点赞关注，转发给朋友！" | "Like, follow & share with friends!" |

### Duration Estimation (Dry Run)

After writing `podcast.txt`, automatically run:

```bash
python3 ${CLAUDE_SKILL_DIR}/generate_tts.py --input videos/{name}/podcast.txt --output-dir videos/{name} --dry-run
```

Report estimated duration. If >12min or <3min, suggest adjustments.

---

## Step 5: Collect Media Assets

**Auto mode:** Skip media collection (text-only animated sections). Proceed to Step 6.
**Interactive mode:** Ask per-section media source (skip / local file / screenshot / web search / AI generated).

If user mentioned AI images, screenshots, or specific assets in initial request, collect those regardless of mode.

Save assets to `videos/{name}/media/`, generate `media_manifest.json`.

**Available sources:**
- **Unsplash** / **Pexels** / **Pixabay** — free images
- **unDraw** — open-source SVG illustrations
- **Simple Icons** — brand SVG icons
- **Playwright** — web screenshots
- **imagen skill** — AI-generated images

---

## Step 6: Generate Publish Info (Part 1)

Based on `podcast.txt`, generate `publish_info.md`:
- Title (number + topic + hook)
- Tags (10, including product names / domain terms / trending tags)
- Description (100-200 chars)

---

## Step 7: Generate Video Thumbnail

**Auto mode:** Generate Remotion thumbnails (16:9 + 4:3).
**Interactive mode:** Ask user: Remotion-generated / AI (imagen skill) / both.

**MUST generate both aspect ratios**: 16:9 (playback page) and 4:3 (feed/activity), both required. 9:16 only when generating vertical video.

**Thumbnail design rules** (see `references/design-guide.md` for full spec):
- Centered layout, title ≥120px bold, icons ≥120px — as large as text length allows
- Text + icons should fill most of the canvas, minimize empty space
- Must be legible at 300px feed size — use text-stroke or contrast overlay

```bash
npx remotion still src/remotion/index.ts Thumbnail16x9 videos/{name}/thumbnail_remotion_16x9.png --public-dir videos/{name}/
npx remotion still src/remotion/index.ts Thumbnail4x3 videos/{name}/thumbnail_remotion_4x3.png --public-dir videos/{name}/
# Optional: vertical thumbnail (only if rendering vertical video)
npx remotion still src/remotion/index.ts Thumbnail9x16 videos/{name}/thumbnail_remotion_9x16.png --public-dir videos/{name}/
```

**xiaohongshu:** Generate 3:4 thumbnail (replaces 4:3):
```bash
npx remotion still src/remotion/index.ts Thumbnail3x4 videos/{name}/thumbnail_remotion_3x4.png --public-dir videos/{name}/
```

---

## Step 8: Generate TTS Audio

**Preference application:** Read backend/rate/voice from `user_prefs.tts`.

**Agent MUST** extract `tts.backend` from `user_prefs.json` and pass it via `TTS_BACKEND` env var. The script does NOT read user_prefs.json directly — it defaults to `edge` if no env var is set.

```bash
# Primary command — ALWAYS pass TTS_BACKEND from user_prefs
TTS_BACKEND=$(python3 -c "import json; print(json.load(open('${CLAUDE_SKILL_DIR}/user_prefs.json'))['global']['tts']['backend'])") \
  python3 ${CLAUDE_SKILL_DIR}/generate_tts.py --input videos/{name}/podcast.txt --output-dir videos/{name}

# Resume from breakpoint
TTS_BACKEND=$(python3 -c "import json; print(json.load(open('${CLAUDE_SKILL_DIR}/user_prefs.json'))['global']['tts']['backend'])") \
  python3 ${CLAUDE_SKILL_DIR}/generate_tts.py --input videos/{name}/podcast.txt --output-dir videos/{name} --resume

# Dry run (estimate duration)
python3 ${CLAUDE_SKILL_DIR}/generate_tts.py --input videos/{name}/podcast.txt --output-dir videos/{name} --dry-run
```

Backend selection via env: `TTS_BACKEND=azure|cosyvoice|edge`, rate via `TTS_RATE="+5%"`.

### Voice Selection by Language

If user has not customized `tts.voices`, use language-appropriate defaults:

| Language | Azure | Edge | Doubao | CosyVoice |
|----------|-------|------|--------|-----------|
| zh-CN | zh-CN-XiaoxiaoNeural | zh-CN-XiaoxiaoNeural | BV001_streaming | longxiaochun |
| en-US | en-US-JennyNeural | en-US-JennyNeural | BV700_streaming | longlaoshu_v2 |

Set the voice via environment variable before running TTS:

```bash
# Example for en-US with Edge TTS
EDGE_TTS_VOICE="en-US-JennyNeural" python3 ${CLAUDE_SKILL_DIR}/generate_tts.py --input videos/{name}/podcast.txt --output-dir videos/{name}
```

### Phoneme Correction (SSML)

Three tiers (highest to lowest priority):

**1. Inline annotation** (highest) — in podcast.txt:
```text
每个执行器[zhí xíng qì]都有自己的上下文窗口
```

**2. Project dictionary** — in `videos/{name}/phonemes.json`:
```json
{ "执行器": "zhí xíng qì", "重做": "chóng zuò" }
```

**3. Global dictionary** — `phonemes.json` in skill root (shared across all projects)

**Outputs**: `podcast_audio.wav`, `podcast_audio.srt`, `timing.json`

**timing.json `label` field**: Each section gets a human-readable label from the first line of content (before first punctuation, max 10 chars). Example: `[SECTION:hero]` with "大家好，欢迎来到本期视频" → `label: "大家好"`. Silent sections use section name as label.

---

## Step 9: Create Remotion Composition + Studio Preview

**Claude MUST read `references/design-guide.md` before this step.**

**Preference application:** From `user_prefs.visual` override `defaultVideoProps`:
- `typography.*` × `scalePreference` → apply font scaling
- `theme: dark` → swap backgroundColor/textColor
- `primaryColor`, `accentColor` → direct override

All Remotion commands use `--public-dir videos/{name}/` so assets are read directly from the video directory (no copying needed).

### Style Profile Integration

Before choosing visual design, check in order:
1. Session-specified style profile? → Load `user_prefs.json` style_profiles[name], apply props_override
2. No profile? → Check design_references index for tag matches against detected topic
3. Found matches? → Suggest: "Your reference library has N references matching '{topic}'. Apply style '{profile_name}'?"
4. Nothing matches? → Fall back to global + topic_patterns (existing behavior)

Priority chain: Root.tsx defaults < global < topic_patterns[type] < style_profiles[name] < current instructions

### Standard Video Template

Use `${CLAUDE_SKILL_DIR}/templates/Video.tsx` as starting point.

**Shared infrastructure** — copy only if not already present:
```bash
[ ! -f src/remotion/Root.tsx ] && cp ${CLAUDE_SKILL_DIR}/templates/Root.tsx src/remotion/
[ ! -d src/remotion/components ] && cp -r ${CLAUDE_SKILL_DIR}/templates/components src/remotion/components
```

**Per-video composition** — NEVER overwrite `Video.tsx`. Create a unique file:
```bash
cp ${CLAUDE_SKILL_DIR}/templates/Video.tsx src/remotion/{PascalCaseName}Video.tsx
```

Register in `Root.tsx`. Each video gets its own composition file.

**Naming convention:**
| Video name | Composition file | Composition ID |
|------------|-----------------|----------------|
| `ai-agents` | `AiAgentsVideo.tsx` | `AiAgents` |
| `reference-manager` | `ReferenceManagerVideo.tsx` | `ReferenceManager` |

Components are modular:
```tsx
import { ComparisonCard, CodeBlock, FeatureGrid, MediaSection } from "./components";
```

### Component Selection Guide

Choose components based on section content type:

| Content Type | Recommended Component | Draw-On Effect |
|---|---|---|
| Process / pipeline steps | `FlowChart` | SVG arrow connectors draw progressively |
| History / milestones | `Timeline` | SVG nodes + connectors animate in sequence |
| Architecture / system diagram | `DiagramReveal` | Nodes + edges draw on with curve/elbow/straight |
| Comparison / vs | `ComparisonCard` | Entrance animation |
| Data / metrics | `DataBar`, `StatCounter`, `MetricsRow` | Bar fill + counter animations |
| Code / terminal | `CodeBlock` | Entrance animation |
| Key quote | `QuoteBlock` | Entrance animation |
| Feature list / grid | `FeatureGrid`, `IconCard` | Staggered entrance |
| Images / screenshots | `MediaSection`, `MediaGrid` | Entrance animation |
| After Effects animation | `LottieAnimation` | Frame-accurate Lottie playback |

**Audio visualization** — add `AudioWaveform` as a persistent overlay in the video:
```tsx
// Inside Video component, after Scale4K but before Audio elements:
<AudioWaveform props={props} position="bottom" mode="bars" barCount={32} height={40} opacity={0.25} />
```
Three modes: `"bars"` (spectrum), `"wave"` (filled area), `"dots"` (pulsing circles).

**Diagram architecture** — use `DiagramReveal` for system/architecture diagrams:
```tsx
<DiagramReveal
  props={props}
  nodes={[
    { id: "a", label: "Input", x: 100, y: 80 },
    { id: "b", label: "Process", x: 400, y: 80 },
    { id: "c", label: "Output", x: 700, y: 80 },
  ]}
  edges={[
    { from: "a", to: "b", style: "curve" },
    { from: "b", to: "c", style: "curve" },
  ]}
  width={900} height={200}
/>
```

**Lottie animations** — place JSON files in `videos/{name}/animations/`:
```tsx
<LottieAnimation src="animations/brain.json" width={200} height={200} loop />
```

### Section Transitions

Template uses `@remotion/transitions` `TransitionSeries`.

| Property | Default | Description |
|----------|---------|-------------|
| `transitionType` | `fade` | fade / slide / wipe / none |
| `transitionDuration` | `15` (0.5s) | Frames |

Install dependencies:
```bash
npm install @remotion/transitions @remotion/paths @remotion/shapes @remotion/media-utils @remotion/lottie lottie-web
```

### Key Architecture

| Point | Description |
|-------|-------------|
| **ChapterProgressBar** | Must be **outside** `scale(2)` container |
| **Chapter width** | Use `flex: ch.duration_frames` for proportional width |
| **Progress indicator** | White progress bar within current chapter |
| **4K scaling** | Content area uses `scale(2)` from 1920×1080 to 3840×2160 |

### Triple-Click Outro

**Auto mode:** Use pre-made MP4 animation (white for light, black for dark theme).
**Interactive mode:** Ask: pre-made MP4 (recommended) / Remotion code-generated.

```bash
cp ${CLAUDE_SKILL_DIR}/assets/bilibili-triple-white.mp4 videos/{name}/media/
```

```tsx
import { OffthreadVideo, staticFile } from "remotion";
<OffthreadVideo src={staticFile("media/bilibili-triple-white.mp4")} />
```

**Xiaohongshu:** No pre-made animation — use text-based CTA. The outro section renders the CTA text ("点赞收藏加关注，评论区见！") as an animated text overlay, similar to YouTube's text CTA mode.

**Douyin:** Text-only CTA (no animation). Douyin content is vertical shorts only — the CTA text ("点赞关注，评论区见！") is rendered as simple end text, not animated.

**WeChat Channels:** Text-only CTA (no animation). WeChat Channels content is vertical shorts only — the CTA text ("点赞关注，转发给朋友！") is rendered as simple end text, not animated.

### Preview & Quality Gate (Mandatory Stop)

Remotion Studio is **always launched** — both auto and interactive modes. This is the primary review step.

**Kill any existing Studio instance first** to avoid serving stale assets from a previous project:

```bash
lsof -ti:3000 | xargs kill -9 2>/dev/null
npx remotion studio src/remotion/index.ts --public-dir videos/{name}/
```

1. Launch `remotion studio` (real-time preview, hot reload)
2. Ask user: "Studio is running at http://localhost:3000. Please review the video preview."
3. **Review loop** — user reviews, requests changes, Claude applies them, Studio hot reloads:
   - Layout/animation tweaks → edit components, Studio auto-refreshes
   - Script/content changes → edit `podcast.txt`, may need re-TTS (Step 8)
   - Pronunciation fixes → re-run TTS (Step 8)
4. **Exit condition**: User explicitly says "render 4K" / "render final version" / "looks good, render" → proceed to Step 10
5. Do NOT proceed to Step 10 until the user confirms.

---

### Visual QA (Automated, part of Step 9)

> **Planned feature.** Automated still rendering and multimodal inspection is not yet implemented. Currently, visual quality is verified manually via Remotion Studio preview. Claude may offer to render section stills for manual inspection if requested.

---

## Step 10: Render 4K Video

> **Prerequisite:** User has reviewed in Remotion Studio (Step 9) and explicitly requested final render.

### 4K Render

```bash
npx remotion render src/remotion/index.ts CompositionId videos/{name}/output.mp4 --video-bitrate 16M --public-dir videos/{name}/
```

**Verify 4K:**
```bash
ffprobe -v quiet -show_entries stream=width,height -of csv=p=0 videos/{name}/output.mp4
# Expected: 3840,2160
```

### Optional: Vertical Highlight Clip (9:16)

```bash
npx remotion render src/remotion/index.ts MyVideoVertical videos/{name}/output_vertical.mp4 --video-bitrate 16M --public-dir videos/{name}/
npx remotion still src/remotion/index.ts Thumbnail9x16 videos/{name}/thumbnail_remotion_9x16.png --public-dir videos/{name}/
```

The vertical composition reuses Video.tsx with `orientation: "vertical"`. All components auto-adapt.

**Platform-specific video format notes:**
- **xiaohongshu**: Primarily short-form vertical content. Long-form horizontal video is optional.
- **douyin**: Vertical shorts only (9:16). No horizontal long-form video generated. Uses existing `generate_shorts.py` pipeline.
- **weixin-channels**: Vertical shorts only (9:16). No horizontal long-form video generated. Uses existing `generate_shorts.py` pipeline.

---

## Step 11: Mix with Background Music

### BGM Selection

**Auto mode:** Select BGM based on topic type:
- Tech/coding/tutorial → `snow-stevekaldes-piano-397491.mp3` (calm)
- Product review/news/upbeat → `perfect-beauty-191271.mp3` (positive)
- User provided custom BGM → use their file

**Interactive mode:** Ask user to choose or provide their own.

```bash
# Default: auto-selected track
cp ${CLAUDE_SKILL_DIR}/assets/{selected-track}.mp3 videos/{name}/bgm.mp3

# Or user's custom BGM
cp /path/to/user-bgm.mp3 videos/{name}/bgm.mp3
```

### Mix

BGM volume priority: `user_prefs.tts.bgmVolume` > topic-pattern default > `0.05` fallback.

```bash
# BGM_VOL from user_prefs.tts.bgmVolume (default 0.05)
ffmpeg -y \
  -i videos/{name}/output.mp4 \
  -stream_loop -1 -i videos/{name}/bgm.mp3 \
  -filter_complex "[0:a]volume=1.0[a1];[1:a]volume=${BGM_VOL:-0.05}[a2];[a1][a2]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" \
  -c:v copy -c:a aac -b:a 192k \
  videos/{name}/video_with_bgm.mp4
```

> **More BGM options and volume tuning:** See `references/troubleshooting.md`.

---

## Step 12: Add Subtitles

> **Preferred approach: Remotion-native subtitles (no FFmpeg re-encode needed)**
>
> The `Video.tsx` template already includes `<Subtitles src={staticFile("podcast_audio.srt")} />`.
> This renders SRT subtitles inside Remotion using React/CSS — positioned at the bottom of the 4K frame,
> with text outline, font, and style matching the project theme. No FFmpeg subtitle pass is needed.
>
> **When to skip this step:** If the video was rendered with the standard `Video.tsx` template
> (which includes `<Subtitles>`), Step 12 is a no-op — just copy `video_with_bgm.mp4` as `final_video.mp4`.
>
> **When FFmpeg subtitles may still be needed:** Legacy videos rendered without the `Subtitles` component,
> or special subtitle styling not achievable in CSS (e.g., karaoke effects).

**Auto mode:** Skip subtitles — copy `video_with_bgm.mp4` as `final_video.mp4`.
**Interactive mode:** Ask user: "Add burned-in subtitles? (Usually not needed — Remotion renders subtitles natively)"

### Subtitle Preferences

Read `subtitle` preferences. If `subtitle.enabled == false`, skip subtitle burning (copy video_with_bgm.mp4 as final_video.mp4).

If FFmpeg subtitle burn is explicitly requested (legacy/special cases only):

Resolve `fontName: "auto"` by `language`:
- zh-CN → `PingFang SC`
- en-US → `Arial`

```bash
# Alignment=2: bottom-center. MarginV uses ASS PlayResY (default 288), NOT video pixels.
# MarginV=6 ≈ 6/288 = ~2% from bottom edge, good for all resolutions.
# WARNING: Only burn from video_with_bgm.mp4, NEVER from final_video.mp4 (avoids double-burn).
ffmpeg -y -i videos/{name}/video_with_bgm.mp4 \
  -vf "subtitles=videos/{name}/podcast_audio.srt:force_style='FontName=PingFang SC,FontSize=20,PrimaryColour=&H00333333,OutlineColour=&H00FFFFFF,Bold=0,Outline=2,Shadow=0,Alignment=2,MarginV=6'" \
  -c:v libx264 -crf 18 -preset slow -s 3840x2160 \
  -c:a copy videos/{name}/final_video.mp4
```

If skipping (default for Remotion-native subtitle videos):
```bash
cp videos/{name}/video_with_bgm.mp4 videos/{name}/final_video.mp4
```

---

## Step 13: Complete Publish Info (Part 2)

Generate Bilibili chapters from `timing.json`:

```
00:00 Opening
00:23 Features
00:55 Demo
01:20 Summary
```

Format: `MM:SS Chapter Title`, each gap ≥5s.

### Publish Info Format by Platform

**Agent behavior:** Generate publish info matching `platform` preference.

**bilibili format:**
- 标题公式、标签、简介
- 章节时间戳 (if `content.chapters == true`)

**youtube format:**
- SEO-optimized title (<70 chars)
- Keyword-rich description with timestamps
- Tags and hashtags (#tag1 #tag2)
- Chapters (if `content.chapters == true`, first line must be `0:00`)

**xiaohongshu format:**
- 标题（≤20字）— short, punchy, emoji-friendly
- 正文（200-500字）— 种草/knowledge-sharing style with emoji
- 话题标签 5-10 个，格式 `#话题#`（双井号）
- 无章节时间戳（小红书不支持）

**douyin format:**
- 文案（100-200字）— casual, emoji-friendly, conversational tone
- 话题标签 3-8 个，格式 `#话题`（单井号）
- 无章节时间戳
- Note: Douyin is shorts-only — no horizontal long-form video

**weixin-channels format:**
- 文案（100-300字）— knowledge-sharing style, suitable for forwarding
- 话题标签 3-8 个，格式 `#话题`（单井号）
- 无章节时间戳
- Note: WeChat Channels is shorts-only — no horizontal long-form video

---

## Step 14: Verify Output & Cleanup

### 14.1 Verification

```bash
VIDEO_DIR="videos/{name}"
echo "=== File Check ==="
for f in podcast.txt podcast_audio.wav podcast_audio.srt timing.json output.mp4 final_video.mp4; do
  [ -f "$VIDEO_DIR/$f" ] && echo "✓ $f" || echo "✗ $f missing"
done

echo "=== Technical Specs ==="
RES=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$VIDEO_DIR/final_video.mp4")
[ "$RES" = "3840,2160" ] && echo "✓ Resolution: 3840x2160 (4K)" || echo "✗ Resolution: $RES (not 4K)"
DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO_DIR/final_video.mp4" | cut -d. -f1)
echo "✓ Duration: ${DUR}s"
SIZE=$(ls -lh "$VIDEO_DIR/final_video.mp4" | awk '{print $5}')
echo "✓ File size: $SIZE"
```

### 14.2 Cleanup

**Both modes:** Only clean TTS temp files (part_*.wav, concat_list.txt) automatically. **NEVER delete output.mp4 or video_with_bgm.mp4** until the user has reviewed final_video.mp4 and explicitly confirmed it's acceptable. These files are needed to re-do BGM/subtitle steps without a full re-render (~8 min).

```bash
VIDEO_DIR="videos/{name}"
# Safe to auto-clean: TTS intermediate files only
rm -f "$VIDEO_DIR"/part_*.wav "$VIDEO_DIR"/concat_list.txt
echo "✓ TTS temp files cleaned"
echo ""
echo "Kept (delete manually after confirming final_video.mp4):"
echo "  output.mp4 — clean render without BGM/subtitles"
echo "  video_with_bgm.mp4 — render with BGM, no subtitles"
```

### 14.3 Final Report

```
=== Video Complete ===
✓ File: final_video.mp4
✓ Resolution: 3840x2160 (4K)
✓ Duration: XXs
✓ Size: XXX MB
✓ Thumbnails: thumbnail_remotion_16x9.png, thumbnail_remotion_4x3.png
✓ Publish info: publish_info.md
✓ Temp files cleaned
```

---

## Step 15: Generate Vertical Shorts (Optional)

**When:** After long-form video is complete (Step 14). Optional step.

**Agent behavior:** Offer to generate vertical shorts. If user agrees, run automatically.

### Generate shorts from sections

```bash
python3 generate_shorts.py --input-dir videos/{name}/ --title "视频标题"
```

This produces `videos/{name}/shorts/{section_name}/` for each qualifying section (>20s, not hero/outro) with:
- `short_audio.wav` — extracted audio slice
- `short_timing.json` — timing for intro (3s) + content + CTA (3s)
- `short_info.json` — composition metadata
- `register_snippet.tsx` — Root.tsx registration code

### Create short compositions

For each generated short:
1. Copy `templates/ShortVideo.tsx` as `src/remotion/{SectionName}ShortVideo.tsx`
2. Replace `SectionContent` placeholder with the actual section component from the long-form video
3. Update `SHORT_CONFIG` with values from `short_info.json`
4. Register composition in `Root.tsx` using `register_snippet.tsx`
5. Ensure `short_audio.wav` is in the short's directory (used via `--public-dir`)

### Render shorts

```bash
npx remotion render src/remotion/index.ts {CompId} videos/{name}/shorts/{section}/short.mp4 --video-bitrate 16M --public-dir videos/{name}/
```

Each short is a standalone 9:16 4K video (2160×3840) with:
- 3-second intro title card
- Section content (vertical layout, all components auto-adapt)
- 3-second CTA card ("关注看完整版")
