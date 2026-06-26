# Configuration Reference

All configuration lives in `config/project.json` (copied from `config/project-template.json`, renamed to `project.json.template` during project init).

## video

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | number | 1920 | Video width in pixels |
| `height` | number | 1080 | Video height in pixels |
| `fps` | number | 30 | Frames per second |
| `codec` | string | "h264" | Video codec |
| `crf` | number | 18 | Quality (lower = better, 18 = high quality) |
| `concurrency` | number | 4 | Render thread concurrency |

## paths

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `audioDir` | string | "public/audio" | TTS audio output directory |
| `buildDir` | string | "build" | Build output directory |
| `defaultContent` | string | "content/subtitles.json" | Default content file |

## tts

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `engine` | string | "edge" | Default TTS engine: `edge` / `qwen` |
| `speedRate` | number | 1.25 | Global speech speed multiplier (1.0 = normal) |

### tts.pythonEnv

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | string | "conda" | Environment type: `conda` / `venv` |
| `conda.name` | string | "base" | Conda environment name |
| `venv.path` | string | ".venv" | Path to venv directory |

### tts.edge

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `voice` | string | "zh-CN-YunyangNeural" | Edge TTS voice name |
| `rate` | string | "+0%" | Per-engine rate override ("+0%" uses global speedRate) |
| `volume` | string | "+0%" | Volume adjustment |

### tts.qwen

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | "mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-bf16" | MLX model ID |
| `voice` | string | "vivian" | Voice preset |
| `lang_code` | string | "zh" | Language code |
| `speed` | number | 1.0 | Model-level speed (multiplied by global speedRate) |
| `temperature` | number | 0.3 | Generation temperature |
| `tokens_per_char` | number | 4 | Token estimation: tokens per character |
| `min_max_tokens` | number | 180 | Minimum max_tokens floor (~15s audio) |
| `max_max_tokens` | number | 2400 | Maximum max_tokens ceiling (~200s audio) |
| `short_text_threshold` | number | 200 | Chars threshold for single-chunk vs sentence-split |
| `sentence_gap_sec` | number | 0.15 | Silence gap between sentences (seconds) |
| `silence_threshold` | number | 0.005 | Silence trimming threshold (relative to peak) |
| `chars_per_second` | number | 4.0 | Expected speech rate for hallucination detection |
| `hallucination_headroom` | number | 2.0 | Max audio duration = expected × headroom |

Available Qwen voices: `serena`, `vivian`, `uncle_fu`, `ryan`, `aiden`, `ono_anna`, `sohee`, `eric`, `dylan`

## subtitle

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | true | Enable subtitles |
| `style` | string | "bottom" | Position: `tiktok` / `bottom` / `center` |
| `displayMode` | string | "sentence" | `sentence` = one at a time, `full` = all text |
| `fontSize` | number | 28 | Font size in pixels |
| `fontFamily` | string | "PingFang SC, Noto Sans SC, sans-serif" | Font family |
| `color` | string | "#FFFFFF" | Text color |
| `highlightColor` | string | "#39E508" | Highlight color |
| `strokeColor` | string | "#000000" | Text stroke color |
| `strokeWidth` | number | 1 | Stroke width |
| `combineTokensWithinMs` | number | 1200 | Token combine threshold |
| `marginBottom` | number | 50 | Bottom margin |
| `fadeDurationSec` | number | 0.3 | Fade transition duration |
| `backgroundColor` | string | "rgba(0, 0, 0, 0.5)" | Subtitle background |
| `maxWidth` | string | "90%" | Max width |
| `padding` | string | "8px 20px" | Padding |
| `borderRadius` | number | 6 | Border radius |

## animation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `transition` | string | "fade" | Transition: `fade` / `slide` / `wipe` / `none` |
| `transitionDurationFrames` | number | 15 | Transition duration in frames |
| `entranceSpring.damping` | number | 200 | Spring damping for entrance animations |
| `paddingFrames` | number | 15 | Extra frames before/after each slide |
| `textEntryDelay` | number | 10 | Delay (frames) before body text appears |

## theme

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backgroundColor` | string | "#0a0a0a" | Slide background color |
| `primaryColor` | string | "#3b82f6" | Title / accent color |
| `secondaryColor` | string | "#8b5cf6" | Secondary accent |
| `textColor` | string | "#ffffff" | Body text color |
| `titleFontSize` | number | 64 | Title font size |
| `bodyFontSize` | number | 36 | Body text font size |
| `fontFamily` | string | "PingFang SC, Noto Sans SC, sans-serif" | Font family |
| `slidePadding` | number | 80 | Slide padding |
| `bodyMaxWidth` | number | 1200 | Max width for body text |
| `decorLineWidth` | number | 200 | Decorative line width |
| `backgroundImageOpacity` | number | 0.3 | Background image opacity |

## bgm (Background Music)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | false | Enable background music |
| `file` | string | "bgm/background.mp3" | Path to BGM file (relative to `public/`) |
| `volume` | number | 0.15 | BGM volume (0.0-1.0, recommended 0.1-0.2) |
| `loop` | boolean | true | Loop BGM for the entire video |

## speakers (Multi-Speaker)

Maps speaker names to TTS voice IDs. Used by `subtitles.json` → `speaker` field.

```json
"speakers": {
  "default": "zh-CN-YunyangNeural",
  "narrator": "zh-CN-YunyangNeural",
  "female": "zh-CN-XiaoxiaoNeural",
  "expert": "zh-CN-YunxiNeural"
}
```

Common Edge TTS Chinese voices:
- `zh-CN-YunyangNeural` — Male, warm, professional
- `zh-CN-YunxiNeural` — Male, young, energetic
- `zh-CN-XiaoxiaoNeural` — Female, warm, natural
- `zh-CN-XiaoyiNeural` — Female, young, lively

## Content Script Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | Unique slide ID (format: `slide_XX`) |
| `title` | string | ✅ | Slide title (displayed in scene) |
| `text` | string | ✅ | Narration text (converted to TTS audio) |
| `speaker` | string | ✅ | Speaker name (maps to `config.speakers`) |
| `type` | string | ❌ | `"intro"` / `"outro"` / `"content"` (default) |
| `notes` | string | ❌ | Internal notes (not rendered) |
