
# VoxFlow Video Skill

Generate short-form videos with AI: LLM writes the script, AI draws cards or scenes, TTS narrates, FFmpeg / Remotion renders the final MP4.

For article-to-card reels (Slice — 6 themes: paper / editorial / poster / Notion / brutalist / glass), switch to [slice.md](slice.md).

Five entry points — pick by what the user wants:

| Command | Output | Use when |
|---|---|---|
| `picstory` | Vertical/landscape MP4 with hand-drawn cards or cinematic scenes | "知识卡片视频", 小红书 / Twitter edu, sketchnote tutorials |
| `present` | 1080×1920 narrated card video, 5 visual schemes | Pitch decks, explainer reels, branded short-form |
| `explain` | MP4 explainer with title / bullets / summary scenes | "What is X?" tutorials, course intros |
| `slides` | Self-contained HTML deck with embedded TTS audio | Product launches, talks, share-as-link |
| `image` | Single PNG | One-off illustrations / thumbnails (Hunyuan TextToImage) |

## Prerequisites

- `npm install -g voxflow` and `voxflow login`
- `ffmpeg` installed (`brew install ffmpeg` / `sudo apt install ffmpeg`) — required for MP4 render
- For `present` / `explain` (Remotion-backed): the local plugin install includes `remotion-cards/`. If `present` says "Remotion not ready", run `npm install` inside the bundled `remotion-cards/` directory. For `explain`, you can skip local Remotion with `--cloud`.


## 🎴 picstory — knowledge-card video

LLM writes a structured script, AI draws one card per scene, TTS narrates, FFmpeg assembles. Best for 小红书 / Twitter edu / TikTok.

### Quick start

```bash
# Default: Chinese, sketchnote style, portrait, 5 scenes
voxflow picstory --topic "AI Agent 入门指南"

# 2-scene quick test (no full video render)
voxflow picstory --topic "AI 入门" --scenes 2 --image-only

# English landscape video
voxflow picstory --topic "How React Hooks Work" --language en --ratio landscape --style photo
```

Output: `picstory-<timestamp>.mp4` + `.json` (script).

### Card-type styles (structured heading + key points)

| `--style` | Look | Best for |
|---|---|---|
| `sketchnote` *(default)* | Colorful hand-drawn bullet journal | Knowledge sharing, tutorials |
| `neon_noir` | Cyberpunk dark with neon glow | Tech, startup |
| `minimal_3d` | Soft 3D clay on pastel gradients | 小红书 lifestyle |
| `chalkboard` | White chalk on dark green | Science, academic |

### Scene-type styles (free-form illustration)

| `--style` | Look | Best for |
|---|---|---|
| `photo` | Cinematic / photo-real | Storytelling, travel |
| `manga_panel` | Japanese manga ink linework | Drama, step-by-step guides |
| `vintage_newspaper` | 1940s broadsheet | History, factual stories |

### Ratios

| `--ratio` | Pixels | Platform |
|---|---|---|
| `portrait` *(default)* | 1080×1920 | 小红书, TikTok, Reels, 抖音 |
| `landscape` | 1920×1080 | YouTube, B站 |
| `square` | 1080×1080 | Instagram, Twitter |

### Script-model presets (`--script-model`)

| Preset | Provider | Strength |
|---|---|---|
| omitted | server config | Balanced default (gpt-4o-mini) |
| `gemini-flash` | OpenRouter | Multilingual, good Chinese |
| `deepseek` | DeepSeek | Cheapest, excellent Chinese |
| `hunyuan` | 腾讯混元 | Chinese-native |
| `moonshot` | Moonshot | Chinese long context |

> Server enforces an allowlist — only the preset names above work; arbitrary model IDs are rejected.

### Image quality (`--quality`)

Image generation is the only meaningful cost (~$0.005-0.08 per image). LLM script (~2K tokens) is negligible.

| `--quality` | Provider | Strength | 5-image cost |
|---|---|---|---|
| `fast` *(default)* | OpenRouter Gemini Flash | Cheapest, balanced | ~$0.025 |
| `hd` | OpenRouter Gemini Pro | Higher detail | mid |
| `ultra` | OpenRouter gpt-5.4-image-2 | Best overall, ~16× cost | ~$0.40 |
| `fast-aiberm` | Aiberm Gemini Flash | Cheap Aiberm tier | low |
| `hd-aiberm` | Aiberm Gemini Pro | **Strongest Chinese text rendering** — best for 小红书 cards with Chinese headers | mid |

Use `fast` for iteration; `hd-aiberm` when cards must contain accurate Chinese characters; `ultra` for hero exports.

### Full options

| Flag | Default | Description |
|---|---|---|
| `--topic <text>` | required (or `--text`) | Story topic |
| `--text <content>` | — | Paste full article instead of a topic |
| `--style <name>` | `sketchnote` | See styles above |
| `--ratio <name>` | `portrait` | `portrait` \| `landscape` \| `square` |
| `--language <code>` | `zh` | `zh` \| `en` \| `ja` \| `ko` \| ... |
| `--scenes <n>` | `5` | 2–10. Use `2` for quick tests. |
| `--script-model <preset>` | server default | See presets above |
| `--quality <tier>` | `fast` | See table above |
| `--voice <id>` | default | TTS voice from `voxflow voices` |
| `--speed <n>` | `1.0` | TTS speed 0.5–2.0 |
| `--bgm <file>` | — | Background music (mp3/wav) mixed under narration |
| `--bgm-volume <n>` | `0.1` | BGM volume 0–1 |
| `--fade <n>` | `0.4` | Per-scene fade in/out seconds (`0` to disable) |
| `--image-only` | false | Save images + audio without final video render |
| `--output-dir <dir>` | — | Directory for all outputs |
| `--output <path>` | auto | Final MP4 path |

### Quota cost

| Operation | Quota |
|---|---|
| LLM script | 100 |
| TTS / scene | 50 |
| Image / scene | 500 |
| **2-scene test** | **~1,200** |
| **5-scene full** | **~2,850** |

Free tier (10K/month) ≈ 3 full picstory videos.

### Pipeline

```
Topic / Text
  ├─[1] LLM script → { title, scenes: [{ heading, keyPoints, narration }] }
  ├─[2] TTS per scene → PCM audio
  ├─[3] Image per scene (parallel) → JPEG via /api/image/generate
  └─[4] FFmpeg: image + WAV → Ken Burns zoompan MP4 → concat → +BGM → final.mp4
```

### Troubleshooting

| Problem | Fix |
|---|---|
| `ffmpeg not found` | `brew install ffmpeg` (mac) / `sudo apt install ffmpeg` |
| `Image generation failed` | Retry; if stuck on `hd`, drop to `--quality fast` |
| Render too slow | Ken Burns is CPU-heavy. Use `--scenes 2 --image-only` to validate content first. |
| `model_not_allowed` | Use a `--script-model` preset name, not a raw model ID |
| Chinese text mangled in cards | Switch to `--quality hd-aiberm` |


## 📑 present — narrated card video (Remotion local)

Text or URL → LLM cards → TTS → Remotion render. 1080×1920, 5 visual schemes.

```bash
voxflow present --text "Claude Code 是一个 AI 编程工具" --style aurora
voxflow present --url https://example.com/article --style noir
voxflow present --text "2025 AI 芯片格局" --web-search --style neon
voxflow present --cards pre-generated.json --no-audio
```

| Flag | Default | Notes |
|---|---|---|
| `--text` / `--url` / `--cards` | one required | input source |
| `--style` | `aurora` | `noir` \| `neon` \| `editorial` \| `aurora` \| `brutalist` |
| `--voice <id>` | `v-female-R2s4N9qJ` | TTS voice |
| `--speed <n>` | `1.0` | 0.5–2.0 |
| `--no-audio` | false | Silent video only |
| `--web-search` | false | Augment LLM with up-to-date web facts |
| `--output <path>` | `./present-<ts>.mp4` | `.mp4` or `.wav` |

> If `present` reports "Remotion not ready", run `npm install` inside the bundled `remotion-cards/` directory to set up the local renderer.


## 🧠 explain — AI explainer video

Title / bullets / summary scene flow. Best for "What is X?" tutorials.

```bash
voxflow explain --topic "What is React?"
voxflow explain --topic demo --output demo.mp4         # built-in demo (no API call)
voxflow explain --topic "区块链入门" --style chalkboard --voice v-male-Bk7vD3xP
voxflow explain --topic "Machine Learning" --audio-only
voxflow explain --topic "AI Agent 入门" --cloud         # render on server
```

| Flag | Default | Notes |
|---|---|---|
| `--topic <text>` | required | Use `demo` for built-in demo script |
| `--style` | `modern` | `modern` \| `playful` \| `corporate` \| `chalkboard` |
| `--language` | `en` | `en` \| `zh` \| `ja` \| `ko` \| ... |
| `--voice <id>` | `v-female-R2s4N9qJ` | |
| `--scenes <n>` | `5` | 3–12 |
| `--audio-only` | false | Skip render, output WAV only |
| `--cloud` | false | Use cloud Remotion instead of local |
| `--output <path>` | `./explain-<ts>.mp4` | |


## 📊 slides — HTML presentation with TTS

Generates a self-contained HTML deck with embedded base64 audio per slide. Open in any browser, no server needed.

```bash
voxflow slides "AI in Healthcare"
voxflow slides "Q4 Revenue Report" --template report --theme paper
voxflow slides "React Tutorial" --template tutorial --model balanced
voxflow slides "Startup Pitch" --template pitch --theme ocean --no-audio
```

| Flag | Default | Notes |
|---|---|---|
| `--text <text>` (or positional) | required | Topic |
| `--template` | `free` | `product` \| `report` \| `tutorial` \| `pitch` \| `free` |
| `--theme` | `midnight` | `midnight` \| `paper` \| `ember` \| `forest` \| `ocean` |
| `--model` | `swift` | `swift` \| `balanced` \| `pro` \| `creative` |
| `--voice <id>` | `v-female-R2s4N9qJ` | |
| `--no-audio` | false | Skip TTS, slides only |
| `--output <path>` | `./slides-<ts>.html` | |

10 layouts: `hero`, `title-bullets`, `two-column`, `three-cards`, `image-left`, `image-right`, `quote`, `timeline`, `stats`, `section`. Templates auto-pick a layout sequence.


## 🖼 image — single Hunyuan illustration

Synchronous text → image (PNG). Useful for thumbnails or one-off art.

```bash
voxflow image "a sleeping cat in a sunlit window" --resolution 1024:1024 -o cat.png
```

Resolutions: `768:768`, `768:1024`, `1024:768`, `1024:1024`, `720:1280`, `1280:720`, `768:1280`, `1280:768`, `1080:1920`, `1920:1080`.

Prompt max 1000 chars. Output: local PNG + COS URL.


## Pick-the-right-tool checklist

```
"小红书风格知识卡片"           → picstory
"AI 短视频 + caption"          → picstory --style sketchnote
"explainer / What is X?"        → explain
"branded short with my text"    → present
"already have cards/script"     → present --cards
"shareable HTML deck w/ audio"  → slides
"single illustration"           → image
```

## Rules

1. **Search voices** with `voxflow voices` before passing `--voice`. Never guess IDs.
2. **Check quota** before video calls (`voxflow status`): picstory ≈ 3K, present/explain ≈ 500–2K.
3. **Test cheap first**: `picstory --scenes 2 --image-only` validates the script before paying for full render.
4. After render finishes, auto-play: `open output.mp4` (macOS).
