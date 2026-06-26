# First Run Guidance

## Goal

If the user is running the pipeline for the first time, guide them through minimum configuration **and local media-tool prerequisites** before any production attempt.

## Ask in this order

### Step 0: Auto-detect pipeline mode + route policy
Read `runtime.pipelineMode` first:
- `minimax_full`: full upstream+downstream pipeline
- `vidu_simple`: lightweight direct video pipeline
- `seedance_simple`: lightweight direct video pipeline

If missing, default to `minimax_full`.

Then route by input capability (not by hardcoded vendor):
- 纯文字: `text -> video`
- 图+文字: `image+text -> video` (prefer direct first_frame binding)
- 纯文字且要先看首图: route to `text -> image` first

Use `runtime.routing` priority fields when present:
- `videoPriorityImageText`
- `videoPriorityTextOnly`
- `imagePriorityTextOnly`

### Step 1: Local media tools
First confirm whether the runtime can access:
- `ffmpeg`
- `ffprobe`

Resolution order should be portable:
1. explicit command arguments like `--ffmpeg` / `--ffprobe`
2. shared config values such as `runtime.ffmpeg` / `runtime.ffprobe`
3. environment variables such as `FFMPEG_PATH` / `FFPROBE_PATH`
4. binaries available from PATH

Do not rely on one machine’s fixed absolute path.

Without these tools, local mixing / final packaging should not be claimed as runnable.

### Step 2: Mode-specific model config

For `minimax_full` ask for:
- upstream Seedance: 厂商 / 接口地址 / 模型名 / API Key
- downstream video: use either single block `downstream.waoo.video` or multi-map `downstream.waoo.videos.*`
- downstream image: use either single block `downstream.waoo.image` or multi-map `downstream.waoo.images.*` (optional when user already provides reference image)
- downstream TTS: optional for initial video generation

For `vidu_simple` / `seedance_simple` ask for:
- downstream video: single block or multi-map as above

Then ask TTS only if user wants spoken voice in final output.

If user asks for subtitle auto-alignment, ask ASR config in this order:
1. `volc_asr_auc` (recommended): `X-Api-Key` + resource `volc.seedasr.auc`
2. `volc_vc`: `appid` + `token` (resource `vc.async.default`)
3. fallback: local `faster-whisper`

Optional operator overrides at runtime:
- `--video-vendor <seedance|vidu|minimax>`
- `--image-vendor <seedance|minimax>`

Adapter note:
- `vidu_simple` has built-in direct-video adapters for `minimax` / `vidu` / `seedance`
- if vendor is anything else, return clear unsupported-vendor guidance

### Step 2.5: Seedance strict-script profile (recommended)

When user asks “按剧本锁定” or fidelity is more important than speed, switch to Seedance full-doc-style request body:

- use `content` with:
  - one `text` block (strict panel prompt + subtitle semantics)
  - one `image_url` block with `role=first_frame` (anchor character/scene continuity)
- set explicit fields:
  - `duration` (panel-level clip length)
  - `resolution`
  - `generate_audio=true`
  - `camera_fixed=true`
  - `draft=false`
  - stable `seed`
  - `return_last_frame=true` for continuity chaining

Hard guard:
- do **not** mix `first_frame/last_frame` with `reference_image` in one request body (provider will reject with `InvalidParameter`).

Practical policy:
- script-fidelity run: prefer panelized `5s + 5s` and then merge
- quick preview run: text-only video is allowed but must be labeled as low-fidelity preview

### Step 3: Ambience policy
Ask whether to:
- 优先本地环境音素材
- or use AI ambience

If AI ambience is used, ask for:
- 厂商
- 接口地址
- 模型名
- API Key

## Guidance style

- keep the questionnaire short
- avoid technical jargon like `provider`
- explain missing pieces plainly
- do not dump all possible fields at once unless the user asks for a full template

## Minimum run-ready config

For `minimax_full`:
- upstream Seedance config
- downstream video config (single block or videos map)
- downstream image config only when no reference image is supplied
- locally available `ffmpeg` and `ffprobe` for mix/export stages

For `vidu_simple` / `seedance_simple`:
- downstream video config (single block or videos map)
- (optional) downstream TTS when narration is required
- locally available `ffmpeg` and `ffprobe` for mix/export stages

Ambience can remain optional depending on workflow stage.

For auto subtitle-alignment runs, at least one ASR route should be runnable:
- `volc_asr_auc` key route (`X-Api-Key` + `volc.seedasr.auc`)
- or `volc_vc` appid/token route (`vc.async.default`)
- or local `faster-whisper`
