---
name: remotion-video-studio
description: "Automated video production studio using Remotion + React + TTS. Creates animated explainer videos from JSON content scripts through a make-driven pipeline: TTS audio generation → render props → Remotion video rendering. Use when users want to create educational/explainer videos, animated presentations, data visualization videos, or any programmatic video with narration and subtitles. Supports Edge TTS (online free) and Qwen TTS (local MLX on Apple Silicon). All operations MUST use `make` commands, never bare CLI commands."
---

# Remotion Video Studio

Automated video production: JSON content script → TTS audio → animated Remotion video.

## ⚠️ Critical Rule: Use `make` Only

**All project operations MUST go through `make`. Never run bare commands.**

The only exception is `scripts/init_project.py`, which runs **before** the project exists (and thus before `Makefile` is available). After project initialization, all operations must use `make`.

```bash
# ✅ Correct — project scaffolding (the only exception to make-only rule)
python scripts/init_project.py my-video --path ~/projects

# ✅ Correct — all subsequent operations use make
make pipeline-edge

# ❌ Wrong — will break env/paths
python3 scripts/pipeline.py --tts edge
npx remotion render src/index.ts MainVideo build/video.mp4
```

## Workflow (Step-by-Step)

Follow this exact order when creating a video project:

### Step 1: Scaffold Project

Copy the template from `assets/project-template/` to the target directory:

```bash
python scripts/init_project.py <project-name> --path <output-directory>
```

Or manually copy `assets/project-template/` and run `make install`.

### Step 2: Edit Configuration

Edit `config/project.json` to customize video parameters **before** running any pipeline.

Key config sections to review:
- `video`: Resolution (1920×1080), FPS (30), codec, quality
- `tts.engine`: Choose `"edge"` (online, free) or `"qwen"` (local MLX)
- `tts.speedRate`: Speech speed multiplier (1.0 = normal, 1.25 = 25% faster)
- `subtitle`: Style (`bottom`/`tiktok`/`center`), display mode (`sentence`/`full`)
- `animation`: Transition type (`fade`/`slide`/`wipe`/`none`)
- `theme`: Colors, fonts, layout
- `bgm`: Background music (file path, volume, loop)
- `speakers`: Map speaker names to TTS voice IDs for multi-speaker support

See [references/config-reference.md](references/config-reference.md) for full parameter docs.

### Step 3: Write Content Script

Edit `content/subtitles.json`:

```json
{
  "title": "Video Title",
  "slides": [
    {
      "id": "slide_01",
      "title": "Opening",
      "text": "Narration text — TTS converts this to speech.",
      "speaker": "default",
      "type": "intro",
      "notes": "Opening slide"
    },
    {
      "id": "slide_02",
      "title": "Core Concept",
      "text": "Main content narration.",
      "speaker": "default",
      "notes": "Content slide"
    },
    {
      "id": "slide_03",
      "title": "Closing",
      "text": "Summary and thanks.",
      "speaker": "narrator",
      "type": "outro",
      "notes": "Closing slide"
    }
  ]
}
```

Rules:
- `id`: Must be unique, format `slide_XX`. Maps to custom scene components.
- `text`: The narration. Keep 50-150 chars per slide for best subtitle display.
- `speaker`: Maps to a voice in `config.speakers` (default: uses `tts.edge.voice`).
- `type`: Optional. `"intro"` for opening, `"outro"` for closing. Omit for regular content.

#### Content Design Guidelines

- **Recommended slides**: 7-12 slides for a 2-5 minute video
- **Text length**: 50-150 characters per slide for best TTS and subtitle display
- **Structure**: intro → core concepts (3-6 slides) → comparison/examples → applications → summary
- **Speaker variety**: Use different `speaker` values for multi-voice narration

### Step 4: (Optional) Create Animated Scenes

Create custom animated scenes for specific slides. Slides without custom scenes get a generic text layout.

1. Create `src/components/scenes/YourScene01.tsx`:

```tsx
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import type { SlideRenderData, ThemeConfig } from "../../types/types";

type Props = {
  slide: SlideRenderData;  // Full slide data (id, title, text, durationInFrames, etc.)
  title: string;           // Shortcut for slide.title
  theme: ThemeConfig;      // Theme colors, fonts, sizes
};

export const YourScene01: React.FC<Props> = ({ slide, title, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Use slide.durationInFrames to adapt animation timing
  const midPoint = Math.floor(slide.durationInFrames / 2);

  // Use animation components from ../animations/ (FadeIn, SineWave, AnimatedBarChart, etc.)
  return (
    <AbsoluteFill style={{ backgroundColor: theme.backgroundColor }}>
      {/* Your animated content */}
    </AbsoluteFill>
  );
};
```

2. Export from `src/components/scenes/index.ts`
3. Register in `src/components/sceneMap.ts`:

```tsx
export const SCENE_MAP: Record<string, React.FC<any>> = {
  slide_01: YourScene01,
};
```

See `src/components/scenes/ExampleScene.tsx` for a complete reference.
See [references/animation-components.md](references/animation-components.md) for available animation components.

### Step 5: Run Pipeline

```bash
make pipeline-edge        # Edge TTS (online, free, recommended)
make pipeline-qwen        # Qwen TTS (local MLX, Apple Silicon)
```

Output: `build/video.mp4`

For iterative development (only regenerates changed slides):
```bash
make rebuild-edge         # Incremental rebuild with Edge TTS
make rebuild-fast         # Rebuild without audio normalization (faster)
```

### Step 6: Preview (Optional)

```bash
make dev    # Open Remotion Studio browser preview
```

## Pipeline Stages

```
content/subtitles.json  →  TTS  →  public/audio/*.mp3 + *.srt
                                →  Audio normalization (optional)
                                →  build/render-props.json
                                →  build/video.mp4
```

1. **TTS**: Convert each slide's text to audio (MP3 + SRT subtitles for Edge, WAV for Qwen)
2. **Audio Post-Processing**: Loudness normalization (EBU R128) via ffmpeg (skip with `--no-normalize`)
3. **Render Props**: Probe audio durations, calculate frame counts, generate `build/render-props.json`
4. **Remotion Render**: Compose animations + audio + subtitles → final video

### Incremental Builds

The TTS engine uses hash-based change detection. When you modify a slide's text, only that slide's audio is regenerated. To force full regeneration:

```bash
make clean-tts            # Remove TTS manifest
make pipeline-edge        # Full regeneration
```

## Project Structure

> **Note on template packaging**: The skill package stores `Makefile` as `Makefile.txt` and omits `.gitignore` to comply with the publishing platform's file-type validation rules. The `init_project.py` script automatically restores these files to their correct names during project scaffolding.

```
project-root/
├── Makefile                     # All operations entry point (restored from Makefile.txt by init_project.py)
├── .gitignore                   # Git ignore rules (auto-generated)
├── config/
│   ├── project.json.template    # Config template (from project-template.json)
│   └── project.json             # Local config (Git-ignored, edit this)
├── content/
│   ├── subtitles.json           # Video content script
│   └── subtitles.json.template  # Content template (from subtitles-template.json)
├── scripts/
│   ├── pipeline.py              # End-to-end pipeline orchestrator
│   ├── tts_edge.py              # Edge TTS engine (incremental, multi-speaker, SRT)
│   ├── tts_qwen.py              # Qwen TTS engine (local MLX)
│   └── tts_utils.py             # Shared utilities (path resolution, config loading)
├── src/
│   ├── index.ts                 # Remotion entry
│   ├── Root.tsx                 # Root composition registration
│   ├── lib/config.ts            # Config loader for Remotion
│   ├── compositions/
│   │   └── MainVideo.tsx        # Main video orchestrator (+ BGM support)
│   ├── components/
│   │   ├── SlideScene.tsx       # Scene dispatcher (custom → fallback)
│   │   ├── SubtitleOverlay.tsx  # Subtitle renderer (sentence/full mode)
│   │   ├── sceneMap.ts          # Slide ID → Scene component registry
│   │   ├── animations/         # Reusable animation components (13 components)
│   │   └── scenes/             # Topic-specific animated scenes
│   │       └── ExampleScene.tsx # Reference scene template
│   └── types/types.ts           # TypeScript type definitions
├── public/
│   ├── audio/                   # TTS output (generated: .mp3 + .srt)
│   └── bgm/                    # Background music files (optional)
├── build/                       # Render output (generated)
├── package.json
├── requirements.txt             # Python dependencies
└── tsconfig.json
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install npm dependencies (auto init-config) |
| `make install-chrome` | Install Chrome Headless Shell (auto-detect zip or copy from another project) |
| `make install-chrome CHROME_ZIP=path` | Install Chrome from a specific zip file |
| `make install-chrome CHROME_FROM=path` | Copy Chrome from another project's node_modules |
| `make dev` | Open Remotion Studio browser preview |
| `make pipeline` | Full pipeline (default TTS from config) |
| `make pipeline-edge` | Full pipeline + Edge TTS (recommended) |
| `make pipeline-qwen` | Full pipeline + Qwen TTS (local MLX) |
| `make pipeline-content CONTENT=content/xxx.json` | Pipeline with custom content file |
| `make rebuild-edge` | Incremental rebuild (Edge TTS, only changed slides) |
| `make rebuild-qwen` | Incremental rebuild (Qwen TTS) |
| `make rebuild-fast` | Rebuild without audio normalization (faster) |
| `make tts-edge` | Generate TTS audio only (Edge) |
| `make tts-qwen` | Generate TTS audio only (Qwen) |
| `make render` | Render video only (needs existing audio) |
| `make render-props` | Generate render-props.json only |
| `make deps-qwen` | Install Qwen TTS dependencies |
| `make clean` | Remove generated audio and video |
| `make clean-tts` | Remove TTS manifest (force full regeneration) |
| `make distclean` | Remove all generated files + node_modules |

## TTS Engines

| Engine | Type | Speed | Features |
|--------|------|-------|----------|
| `edge` | Online | ⚡ Fast | Multi-speaker, SRT subtitles, incremental builds |
| `qwen` | Local (MLX) | 🚀 Fast on Apple Silicon | Custom voices, offline |

Default: `edge` (recommended for most use cases).

### Network & Privacy Disclosure

- **Edge TTS** (`tts_edge.py`): Calls Microsoft Edge TTS free API via the `edge-tts` Python package (endpoint: `speech.platform.bing.com`). Only the slide narration text is sent for speech synthesis. **No API key or account required**. No other user data is transmitted.
- **Qwen TTS** (`tts_qwen.py`): **Fully offline**. Runs the MLX model locally on Apple Silicon. No network calls whatsoever.
- **Pipeline** (`pipeline.py`): Orchestrates TTS + `ffmpeg` (local audio processing) + `npx remotion render` (local video rendering). No network calls beyond the TTS engine selected.
- **No credentials required**: This skill does not require any API keys, tokens, or environment secrets.

### Multi-Speaker Support

Configure speaker-to-voice mappings in `config/project.json`:

```json
"speakers": {
  "default": "zh-CN-YunyangNeural",
  "narrator": "zh-CN-YunyangNeural",
  "female": "zh-CN-XiaoxiaoNeural",
  "expert": "zh-CN-YunxiNeural"
}
```

Then use in `subtitles.json`:
```json
{ "id": "slide_01", "speaker": "narrator", "text": "..." },
{ "id": "slide_02", "speaker": "female", "text": "..." }
```

### Background Music

Enable BGM in `config/project.json`:

```json
"bgm": {
  "enabled": true,
  "file": "bgm/background.mp3",
  "volume": 0.15,
  "loop": true
}
```

Place your audio file in `public/bgm/`. Volume 0.1-0.2 is recommended to not overpower narration.

### Python Environment for Qwen

Qwen TTS requires a separate Python environment. Configure in `config/project.json`:

```json
"pythonEnv": {
  "type": "conda",
  "conda": { "name": "base" },
  "venv": { "path": ".venv" }
}
```

Override on command line: `make pipeline-qwen ENV_TYPE=conda CONDA_ENV=myenv`

## Available Animation Components

Import from `src/components/animations/`:

| Component | Description |
|-----------|-------------|
| `FadeIn` | Opacity fade entrance |
| `ScaleIn` | Scale-up entrance |
| `SlideIn` | Directional slide entrance |
| `TypewriterText` | Character-by-character text reveal |
| `WordHighlight` | Word-by-word highlight effect |
| `AnimatedBarChart` | Animated bar chart |
| `AnimatedLineChart` | Animated line chart |
| `AnimatedPieChart` | Animated pie chart |
| `SineWave` | Animated sine wave SVG |
| `CoordinateSystem` | Animated coordinate axes |
| `AnimatedPath` | SVG path drawing animation |
| `StaggeredList` | Staggered list item entrance |
| `CountUp` | Number counting animation |

See [references/animation-components.md](references/animation-components.md) for API details.

## Remotion Patterns

See [references/remotion-rules.md](references/remotion-rules.md) for Remotion core API patterns.

## Environment Requirements

- **Node.js** ≥ 18
- **Python** ≥ 3.10
- **make** (macOS/Linux built-in)
- **FFmpeg** (bundled with @remotion/renderer, also used for audio normalization)
- `pip install edge-tts` for Edge TTS
- Qwen TTS: separate conda/venv with `mlx-audio soundfile numpy`

## Troubleshooting

### Chrome Headless Shell Download Fails

Remotion requires Chrome Headless Shell (~94MB) for rendering. If the automatic download fails (network issues, proxy, etc.):

**Quick Install** (recommended):
```bash
# Auto-detect zip in current or parent directories
make install-chrome

# From a specific zip file
make install-chrome CHROME_ZIP=/path/to/chrome-headless-shell-mac-arm64.zip

# Copy from another project (avoids re-downloading)
make install-chrome CHROME_FROM=/path/to/other-project
```

**Manual Install** (if `make install-chrome` doesn't work):

**Step 1**: Find the required version:
```bash
node -e "console.log(require('@remotion/renderer/package.json').version)"
# Then check: node_modules/@remotion/renderer/dist/browser/BrowserFetcher.js
# Look for TESTED_VERSION (e.g., "144.0.7559.20")
```

**Step 2**: Download manually:
```
https://storage.googleapis.com/chrome-for-testing-public/<VERSION>/mac-arm64/chrome-headless-shell-mac-arm64.zip
```
Replace `<VERSION>` with the version from Step 1. For Intel Mac, use `mac-x64`.

**Step 3**: Install to the correct directory:
```bash
CHROME_DIR="node_modules/.remotion/chrome-headless-shell"
mkdir -p "$CHROME_DIR/mac-arm64"

# Unzip and move to platform directory
unzip chrome-headless-shell-mac-arm64.zip -d "$CHROME_DIR/mac-arm64/"

# Write VERSION file (MUST match the TESTED_VERSION exactly)
echo "144.0.7559.20" > "$CHROME_DIR/VERSION"

# Ensure executable permission
chmod +x "$CHROME_DIR/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell"
```

**Expected directory structure**:
```
node_modules/.remotion/chrome-headless-shell/
├── VERSION                                    ← Must contain exact version string
└── mac-arm64/                                 ← Platform directory
    └── chrome-headless-shell-mac-arm64/       ← Unzipped folder
        └── chrome-headless-shell              ← Executable
```

### Pipeline Fails Mid-Way

If the pipeline fails after TTS but before rendering:
```bash
make render              # Just re-run the render step
```

If TTS partially completed:
```bash
make pipeline-edge       # Incremental: only regenerates missing/changed audio
```

To force full regeneration:
```bash
make clean-tts           # Remove hash manifest
make pipeline-edge       # Full regeneration
```

### Audio Quality Issues

If narration sounds too loud/quiet or inconsistent:
- Audio normalization runs automatically (EBU R128 standard)
- Skip with `make rebuild-fast` or `--no-normalize` flag
- Adjust `tts.speedRate` in config (1.0-1.5 recommended)

### JSX Common Pitfalls in Scenes

When writing custom scene components, watch out for these JSX gotchas:

**Curly braces in text**: `{ }` in JSX is treated as JavaScript expressions, not literal text. This is especially common when displaying math formulas.

```tsx
// ❌ Wrong — JSX interprets { f(t) } as an expression, causing "f is not defined" error
<div>ℒ { f(t) } → F(s)</div>

// ✅ Correct — wrap in a string literal
<div>{"ℒ { f(t) } → F(s)"}</div>

// ✅ Also correct — use a variable
const formula = "ℒ { f(t) } → F(s)";
<div>{formula}</div>
```

**Angle brackets in text**: `<` and `>` can be misinterpreted as JSX tags.

```tsx
// ❌ Wrong
<div>when x < 0 and y > 1</div>

// ✅ Correct
<div>{"when x < 0 and y > 1"}</div>
```

**Tip**: When in doubt, always wrap text containing special characters (`{ } < >`) in `{"..."}` string expressions.

### Video Renders But Looks Wrong

1. Use `make dev` to open Remotion Studio for visual debugging
2. Check `build/render-props.json` for correct frame counts
3. Verify scene components are registered in `sceneMap.ts`

## Examples

Complete example projects are available in `assets/examples/`:

- **fourier-transform/**: Full Fourier Transform explainer with 9 custom scenes
  - Copy scenes to your project as reference
  - Demonstrates SVG animations, data visualization, comparison layouts
