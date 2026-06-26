# Command Reference — shellbot-creative-studio

Complete parameter documentation for every command.

---

## `image` — Generate Images

```
Usage: image --prompt "..." [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--prompt` | string | **required** | Text prompt describing the image |
| `--style` | enum | `photo` | `photo`, `digital_art`, `illustration` |
| `--size` | enum | `16:9` | Aspect ratio: `16:9`, `9:16`, `1:1`, `4:3` |
| `--resolution` | enum | `2k` | Output resolution: `1k`, `2k`, `4k` |
| `--provider` | enum | auto | `freepik`, `fal`, `nano-banana-2` |
| `--model` | string | auto | Model override (e.g., `mystic`, `flux-2`, `seedream-v4-5`) |
| `--reference` | URL | — | Reference image for style/structure guidance |
| `--count` | int | `1` | Number of images: 1-4 |
| `--output` | path | — | Save first image to this path |
| `--dry-run` | flag | — | Show command without executing |

**Provider priority:** Nano Banana 2 > Freepik Seedream v5 lite > fal Flux-2

**Freepik models:** `seedream-v5-lite` (default, fast + quality), `seedream-v4-5` (typography), `mystic` (ultra-photoreal, slower), `flux-2-klein` (sub-second), `flux-kontext-pro` (context-aware)

---

## `edit` — Edit/Transform Images

```
Usage: edit --input <url_or_path> --action <action> [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--input` | URL/path | **required** | Input image |
| `--action` | enum | **required** | See actions below |
| `--prompt` | string | — | Text guidance for the edit |
| `--mask` | URL | — | Mask image (required for `inpaint`) |
| `--reference` | URL | — | Reference image (for `style-transfer`) |
| `--scale` | int | `4` | Upscale factor: 2-16 (for `upscale`) |
| `--left/right/top/bottom` | int | `0` | Outpaint margins in px |
| `--provider` | enum | auto | `freepik`, `fal`, `nano-banana-2` |
| `--output` | path | — | Save result to this path |
| `--dry-run` | flag | — | Show command without executing |

**Actions:**

| Action | Description | Sync? | Providers |
|--------|-------------|-------|-----------|
| `upscale` | AI-enhanced resolution increase | async | freepik, fal |
| `remove-bg` | Remove background | **sync** | freepik only |
| `inpaint` | Edit masked region with prompt | async | freepik |
| `outpaint` | Expand canvas edges | async | freepik |
| `style-transfer` | Apply reference image style | async | freepik |
| `relight` | Change lighting | async | freepik |

---

## `video` — Generate Video Clips

```
Usage: video --prompt "..." [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--prompt` | string | **required** | Video description |
| `--image` | URL | — | Input image for image-to-video |
| `--duration` | int | `5` | Duration: 3-15 seconds |
| `--aspect` | enum | `16:9` | `16:9`, `9:16`, `1:1` |
| `--provider` | enum | auto | `freepik`, `fal` |
| `--model` | string | auto | Model override |
| `--output` | path | — | Save video to this path |
| `--dry-run` | flag | — | Show command without executing |

**Provider priority:** Freepik Kling v3 omni pro > fal Kling v2

**Freepik models:** `kling-v3-omni-pro` (best quality), `kling-v3-pro` (multi-shot), `runway-4-5` (T2V/I2V), `wan-v2-6` (T2V)

---

## `voice` — Text-to-Speech

```
Usage: voice --text "..." [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--text` | string | **required** | Text to speak (1-40000 chars) |
| `--voice` | string | `21m00Tcm4TlvDq8ikWAM` | ElevenLabs voice ID |
| `--speed` | float | `1.0` | Speaking speed: 0.7-1.2 |
| `--stability` | float | `0.5` | Voice stability: 0-1 |
| `--similarity` | float | `0.2` | Similarity boost: 0-1 |
| `--provider` | enum | auto | `freepik`, `elevenlabs` |
| `--output` | path | — | Save audio to this path (.mp3) |
| `--dry-run` | flag | — | Show command without executing |

**Common voice IDs:**
- `21m00Tcm4TlvDq8ikWAM` — Rachel (female, narration)
- `EXAVITQu4vr4xnSDxMaL` — Bella (female, soft)
- `ErXwobaYiN019PkySvjV` — Antoni (male, deep)
- `VR6AewLTigWG4xSOukaG` — Arnold (male, confident)

---

## `music` — Background Music

```
Usage: music --prompt "..." --duration <seconds> [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--prompt` | string | **required** | Music description |
| `--duration` | int | **required** | Length: 10-240 seconds |
| `--provider` | enum | auto | `freepik`, `elevenlabs` |
| `--output` | path | — | Save audio to this path (.mp3) |
| `--dry-run` | flag | — | Show command without executing |

---

## `sfx` — Sound Effects

```
Usage: sfx --prompt "..." --duration <seconds> [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--prompt` | string | **required** | Sound description (max 2500 chars) |
| `--duration` | float | **required** | Length: 0.5-22 seconds |
| `--loop` | flag | — | Make loop-friendly |
| `--influence` | float | `0.3` | Prompt influence: 0-1 |
| `--provider` | enum | auto | `freepik`, `elevenlabs` |
| `--output` | path | — | Save audio to this path (.mp3) |
| `--dry-run` | flag | — | Show command without executing |

---

## `remotion init` — Bootstrap Remotion Project

```
Usage: remotion init --template <name> [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--template` | enum | **required** | Template name (see below) |
| `--name` | string | from template | Custom composition ID |
| `--output` | path | `./remotion-project` | Target directory |
| `--include-rule-assets` | flag | — | Copy code snippets to src/rule-assets/ |
| `--no-install` | flag | — | Skip npm install |
| `--no-verify` | flag | — | Skip composition verification |
| `--list` | flag | — | List templates and exit |

**Templates:**

| Name | Description | Aspect | Use Case |
|------|-------------|--------|----------|
| `aida-classic-16x9` | AIDA product marketing | 1920x1080 | Product launch, paid ads |
| `cinematic-product-16x9` | Dramatic product launch | 1920x1080 | Premium launches |
| `saas-metrics-16x9` | B2B dashboard metrics | 1920x1080 | SaaS demos |
| `mobile-ugc-9x16` | Vertical social | 1080x1920 | Reels, TikTok, Stories |
| `blank-16x9` | Minimal starter | 1920x1080 | Custom projects |
| `explainer-16x9` | 5-scene how-it-works | 1920x1080 | Tutorials, explainers |

---

## `remotion render` — Render Video

```
Usage: remotion render --project <dir> [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--project` | path | **required** | Remotion project directory |
| `--composition` | string | auto-detected | Composition ID |
| `--output` | path | `out/<comp>.mp4` | Output file path |
| `--codec` | enum | `h264` | `h264`, `h265` |
| `--crf` | int | `18` | Quality (lower=better): 0-51 |
| `--dry-run` | flag | — | Show command without executing |

---

## `plan` — Creative Brief to Storyboard

```
Usage: plan --brief "..." [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--brief` | string | **required*** | Creative brief text or JSON |
| `--brief-file` | path | — | Path to brief JSON file |
| `--format` | enum | `product-marketing` | `product-marketing`, `explainer`, `social-ad` |
| `--duration` | int | `45` | Target seconds: 15-120 |
| `--aspect` | enum | `16:9` | `16:9`, `9:16` |
| `--fps` | int | `30` | `24`, `30`, `60` |
| `--framework` | enum | `general` | `aida` (AIDA-specific), `general` |
| `--output` | path | `./storyboard.json` | Output JSON path |
| `--dry-run` | flag | — | Show command without executing |

*Either `--brief` or `--brief-file` is required.

---

## `pipeline` — End-to-End Production

```
Usage: pipeline --brief "..." [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--brief` | string | **required*** | Creative brief |
| `--brief-file` | path | — | Path to brief JSON file |
| `--template` | enum | `aida-classic-16x9` | Remotion template |
| `--output-dir` | path | `./creative-output` | Output directory |
| `--framework` | enum | `general` | `aida`, `general` |
| `--duration` | int | `45` | Target seconds |
| `--aspect` | enum | `16:9` | `16:9`, `9:16` |
| `--fps` | int | `30` | Frames per second |
| `--skip-render` | flag | — | Stop before render (review first) |
| `--dry-run` | flag | — | Show all commands without executing |

**Pipeline steps:** plan > image > upscale > video > voice > music > remotion init > render

---

## `status` — Check Task Status

```
Usage: status [options]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--task-id` | string | — | Specific task ID to check |
| `--provider` | enum | auto | `freepik`, `fal` |
| `--all` | flag | — | Show all tracked tasks |

---

## `providers` — Provider Availability

```
Usage: providers
```

No parameters. Shows all providers, their availability (based on env vars), and capabilities.

**Environment variables checked:**
- `FREEPIK_API_KEY` — Freepik (image, edit, video, voice, music, sfx)
- `FAL_API_KEY` — fal.ai (image, edit, video)
- `GOOGLE_API_KEY` — Nano Banana 2 via Google (image, edit)
- `OPENROUTER_API_KEY` — Nano Banana 2 via OpenRouter (image, edit)
- `ELEVENLABS_API_KEY` — ElevenLabs (voice, music, sfx)
