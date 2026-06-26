# Implementation Notes

## Current Status

This skill is now structured as an execution policy, not just a loose workflow note.

Prompt-engineering overlays from Seedance 2.0 best practices are merged as a dedicated reference (`references/seedance-prompt-engineering.md`) and wired into SKILL phase `0.5` for pre-submit prompt hardening.

Current pieces include:
- SKILL.md rewritten around explicit execution phases
- references for runtime policy and model routing
- newly added references for checkpoints, clip states, audio, lipsync, and rhythm

## What changed in this refactor

### 1. From abstract layers to executable phases
The skill now frames work as:
1. 目标确认
2. 素材确认
3. 视频生成 / 获取
4. 单条完善
5. 多条拼接
6. 交付汇报

This is closer to how real episode work was actually executed.

### 2. Explicit user modes
The skill now distinguishes:
- 单条保交付模式
- 逐步确认模式
- 配额敏感直跑模式

This was missing before and became important in quota-constrained runs.

### 3. Optional lipsync policy
The skill now treats lipsync as an optional downstream stage.
It is no longer implicitly mixed into the main path.

### 4. Honest clip state language
The new clip-state contract reduces confusion between:
- raw clip
- ambience clip
- dialogue clip
- lipsync candidate
- final clip
- merged clip

## 2026-03-29 reality check after Lin Chong ep1 work

### Video execution learnings
- Official `MiniMax-Hailuo-2.3-Fast` worked for follow-up episode clips.
- `MiniMax` practical split in this workspace remained:
  - `video_generation` for base video
  - `t2a_v2` for voice/TTS
- In practice, `MiniMax` did **not** serve as a single-step strict lipsync final-video solution in this run.

### Lipsync learnings
- `Vidu lip-sync` is validated as a usable optional downstream step.
- A successful original-script run produced:
  - `work/video-engines/waoowaoo/work/video3-vidu/ep1-video3-vidu-lipsync-v1.mp4`
  - duration about `5.8s`
- This is strong enough to keep lipsync as an optional branch in the skill, but not strong enough to make it mandatory by default.

### Audio learnings
The biggest recurring source of confusion was not generation itself, but mismatched audio intent:
- mouth movement without real dialogue
- dialogue intent mixed with ambience-only decisions
- merged clips sounding like separate experiments

This refactor therefore promotes audio policy and rhythm policy to first-class references.

## 2026-04-01 capability routing + guided config upgrade

New behavior in `run-seedance-workflow.cjs`:
- capability-first routing instead of single hardcoded provider path
- supports provider maps:
  - `downstream.waoo.videos.*`
  - `downstream.waoo.images.*`
- keeps backward compatibility with legacy single blocks:
  - `downstream.waoo.video`
  - `downstream.waoo.image`

Routing policy details:
- `runtime.routing.videoPriorityImageText`
- `runtime.routing.videoPriorityTextOnly`
- `runtime.routing.imagePriorityTextOnly`
- optional runtime overrides:
  - `--video-vendor`
  - `--image-vendor`

Flow behavior:
- image+text defaults to direct `first_frame` binding after four-pack confirmation
- first-image generation stage is skipped when source image exists
- auto-continue can now auto-submit video and finish polling/download in one pass

Readiness/guidance improvements:
- guidance now includes routing summary and selected provider source
- vendor/endpoint mismatch check is conservative:
  - blocks obvious cross-vendor mixups
  - allows custom gateway endpoints when no conflicting hint is detected
- `tts` is no longer a hard blocker for initial video generation

## 2026-04-01 first-image strategy prompt + switch

User-facing guidance is now explicit right after four-pack generation:
- confirmation message now includes a visible strategy choice:
  - A `direct` (default, bind source image as `first_frame`)
  - B `img2img` (style-transfer / redraw first image)
- this removes hidden behavior and tells users how to switch in plain language.

Execution changes:
- `continue-seedance-flow.cjs` now accepts `--first-image-strategy direct|img2img`
- strategy can also be inferred from revision text keywords:
  - "图生图 / 转绘 / 风格化 / 换风格" -> `img2img`
  - "原图 / 保脸 / 一致" -> `direct`
- when strategy is `img2img`, direct-first-frame shortcut is disabled and flow continues through first-image generation.

Driver propagation:
- `run-seedance-workflow.cjs --action continue` now forwards `--first-image-strategy` to continue branches.
- outputs now include `firstImageStrategy` / `strategyPrompt` for easier UI messaging and debug traces.

Marketplace summary update:
- `SKILL.md` frontmatter `description` updated to concise Chinese with multi-vendor routing mention:
  - `Seedance / Vidu / MiniMax`

## 2026-04-02 Prompt pack overlay (P0)

新增前置提示词工程层，避免 freeform prompt 漂移：

- 新增脚本：`scripts/build-seedance-prompt-pack.cjs`
  - 输出结构化 prompt（目标/模式/镜头动作/时间节拍/负面约束）
  - 输出 assets mapping 与 timecoded beats
- 新增自测：`scripts/self-test-prompt-pack.cjs`
- `run-seedance-workflow.cjs --action start` 默认生成 `prompt-pack.result.json`
  - simple/full 两条启动路径都会透传：
    - `promptPack`
    - `promptPackStatus`
    - `promptPackError`
    - `artifacts.promptPackPath`
- 新增可选覆盖参数：
  - `--prompt-mode <text-only|first-last-frame|all-reference>`
  - `--prompt-style "..."`
  - `--prompt-camera "..."`
  - `--prompt-scenario <general|ecommerce|narrative|mv|tutorial>`
- Prompt pack 升级（v2）：
  - 场景模板库（general/ecommerce/narrative/mv/tutorial）
  - 负面约束分场景生成
  - workflow 输出 `promptQuality`（score/level/suggestions）用于快速质检
- 低分自动回退：
  - 默认开启 `--prompt-auto-fallback=true`
  - 默认阈值 `--prompt-min-score=80`
  - 当分数低于阈值时自动尝试其他 scenario 生成更优 prompt pack
  - 结果写入 `promptFallback`（triggered/applied/fromScore/toScore/attempts）

## 2026-04-01 ASR route clarification (Volc)

Subtitle-alignment path now has explicit dual-route guidance:

1) AUC route (`/api/v3/auc/bigmodel`)
- auth via `X-Api-Key`
- resource via `volc.seedasr.auc`
- suitable for utterance timestamp extraction from media URL

2) VC route (`/api/v1/vc/submit|query`)
- auth via `Authorization: Bearer; <token>` + `appid`
- requires resource grant `vc.async.default`

Operational rule:
- if one route reports grant mismatch, auto-fallback to the other route or local whisper
- do not keep retrying same unauthorized route

Structured hint policy (sub-script level, not preflight):
- `generate-tts.ts` returns `configuration-guidance` JSON when TTS config is missing
- `check-asr-config.ts` returns `configuration-guidance` JSON when ASR config is missing/incomplete
- `prepare-ambience.ts --mode ai` returns `configuration-guidance` JSON when ambience config is missing/incomplete

## 2026-03-30 workflow continuation fix

A continuation bug was fixed in `continue-after-first-image.cjs`:
- when state was `first-image-asset-confirm`, the driver previously called `prepare-approved-panel-context.cjs` without passing approved image file/url
- this caused `panel-context.approved.json` to lose the first image (`imageUrl` empty)
- downstream prepare step stayed blocked at `video-submit-prepared-blocked`

Now the script forwards:
- `--approved-image-file` from `state.firstImageAsset.imageFile`
- `--approved-image-url` from `state.firstImageAsset.imageUrl`

After this fix, the same sample state can reach `currentStage = video-submit-ready` with `prepareSubmit.ready = true`.

## Current implementation priority

User has paused further video generation because quota is exhausted.
The immediate priority is to continue skill packaging.

## Recommended next code steps

Base helper scripts are now present.

Recommended next steps:
1. run one portable end-to-end sample with real local files
2. unify remaining prompt/error wording across all scripts
3. optionally document one lipsync helper path after base pipeline scripts stabilize

## Driver self-test helper (new)

To quickly validate stage/approval routing for the unified workflow driver, run:

```bash
node scripts/self-test-workflow-driver.cjs
```

This helper verifies:
- wrong approval is rejected at four-pack stage
- wrong approval is rejected at first-image confirm stage
- blocked first-image stage requires `retry-first-image`
- blocked stage enters retry branch when `retry-first-image` is provided
- unknown stage is rejected explicitly

## Minimal config verification helper

A JS fallback helper now exists for environments that cannot run `tsx` directly.
Use it to verify that formal Seedance upstream config is actually readable before claiming Phase 0 is runnable.

```bash
node scripts/verify-seedance-config.cjs \
  ./config/pipeline.config.json
```

## Current script usage examples

All examples below keep paths portable and avoid machine-specific assumptions.

### 0) Run the unified Seedance workflow driver

Use this as the preferred top-level entry when the assistant is acting only as a scheduler.
The assistant should call this driver with `start` or `continue`; the skill's internal entrypoints handle the actual downstream execution.

```bash
node scripts/run-seedance-workflow.cjs \
  --action start \
  --config ./config/pipeline.config.json \
  --topic "智取生辰纲" \
  --episode E01 \
  --out-dir ./work/seedance/E01 \
  --result-json ./work/seedance/E01/workflow.result.json
```

### 0a) Run Seedance auto-entry from one topic

Use this lower-level entry when you intentionally want the four-pack generation stage itself.
It generates the formal four-pack, builds a user-facing confirmation bundle, and automatically stops at the user-confirmation checkpoint.

### 0c) Continue after four-pack confirmation

After the user confirms the four-pack, the assistant should only notify the skill to continue.
The downstream continuation itself must still run through the skill's own continuation entrypoint.
The skill may generate first-image prompt/spec material internally, but should not surface that intermediate bundle to the user by default.
Instead, the next user-visible checkpoint should be the first actual generated first-image asset.

### 0d) Continue after first-image confirmation

After the user confirms the first actual generated first-image asset, the assistant should still only notify the unified workflow driver.
At the current implementation stage, the driver must either continue internally into runnable downstream production, or return an explicit stop checkpoint explaining which internal prerequisites are still missing.
Do not let the assistant manually improvise the missing image/video continuation chain.

```bash
node scripts/continue-seedance-flow.cjs \
  --config ./config/pipeline.config.json \
  --entry-result ./work/seedance/E01/entry.result.json \
  --confirmed true \
  --panel-index 1 \
  --result-json ./work/seedance/E01/continue.result.json
```

### 0e) Continue with unified driver (stage-aware approvals)

Use the unified driver for all post-checkpoint continuation.
Approval value must match the current stage:
- `seedance-four-pack-confirm` -> `four-pack-approved` (pass) / `revise-four-pack` (revise with `--revision-note`)
- `first-image-asset-confirm` -> `first-image-approved` (pass) / `revise-first-image` (revise with `--revision-note`)
- `first-image-asset-blocked` (after config fixed) -> `retry-first-image`

```bash
node scripts/run-seedance-workflow.cjs \
  --action continue \
  --config ./config/pipeline.config.json \
  --state ./work/seedance/E01/workflow.continue.result.json \
  --approval first-image-approved \
  --result-json ./work/seedance/E01/workflow.after-first-image.result.json
```

```bash
node scripts/run-seedance-workflow.cjs \
  --action continue \
  --config ./config/pipeline.config.json \
  --state ./work/seedance/E01/workflow.continue.result.json \
  --approval retry-first-image \
  --result-json ./work/seedance/E01/workflow.continue.retry-first-image.result.json
```

```bash
node scripts/run-seedance-entry.cjs \
  --config ./config/pipeline.config.json \
  --topic "智取生辰纲" \
  --episode E01 \
  --out-dir ./work/seedance/E01 \
  --result-json ./work/seedance/E01/entry.result.json
```

### 0b) Generate formal Seedance story pack from upstream text model directly

Use this lower-level helper only when you intentionally want the upstream generation step itself.

```bash
node scripts/generate-seedance-pack.cjs \
  --config ./config/pipeline.config.json \
  --topic "智取生辰纲" \
  --episode E01 \
  --out-dir ./work/seedance/E01 \
  --result-json ./work/seedance/E01/seedance-pack.result.json
```

### 1) Pick the active panel context

```bash
tsx scripts/get-panel-context.ts \
  --input ./config/sample.storyboard.json \
  --panel-index 0 \
  --out ./work/panel-context.json
```

### 2) Prepare submit with panel guard

```bash
tsx scripts/prepare-video-submit.ts \
  --config ./config/pipeline.config.json \
  --panel ./work/panel-context.json \
  --duration 6 \
  --resolution 768P \
  --require-image-approval \
  --out ./work/video-submit.prepare.json
```

### 3) Submit official video generation

Before paid generation, the submit step now runs panel guard validation again.
If identity/ordering is uncertain, it stops instead of silently continuing.

```bash
tsx scripts/submit-official-video.ts \
  --config ./config/pipeline.config.json \
  --panel ./work/panel-context.json \
  --duration 6 \
  --resolution 768P \
  --require-image-approval \
  --out ./work/video-submit.json
```

### 4) Poll official video task

```bash
tsx scripts/poll-official-video.ts \
  --config ./config/pipeline.config.json \
  --task-id <task-id> \
  --out ./work/video-poll.json
```

### 5) Download official video file

```bash
tsx scripts/download-official-video.ts \
  --config ./config/pipeline.config.json \
  --task-id <task-id> \
  --file-id <file-id> \
  --out ./work/raw/main-clip.mp4 \
  --result-json ./work/raw/main-clip.download.json
```

### 6) Generate TTS audio

```bash
tsx scripts/generate-tts.ts \
  --config ./config/pipeline.config.json \
  --text "只得暂避到山神庙" \
  --out ./work/audio/tts.mp3 \
  --result-json ./work/audio/tts.json \
  --voice-id male-qn-qingse
```

### 7) Resolve ambience input

```bash
tsx scripts/prepare-ambience.ts \
  --preferred ./assets/ambience/snow-ambience.mp3 \
  --dir ./assets/ambience \
  --out ./work/audio/ambience.json
```

### 8) Mix final single clip and validate with ffprobe

```bash
tsx scripts/mix-final-video.ts \
  --config ./config/pipeline.config.json \
  --video ./work/raw/main-clip.mp4 \
  --tts ./work/audio/tts.mp3 \
  --ambience ./assets/ambience/snow-ambience.mp3 \
  --out ./work/final/main-clip.final.mp4 \
  --result-json ./work/final/main-clip.final.json
```

### 9) Build delivery manifest with probe metadata

```bash
tsx scripts/build-delivery-manifest.ts \
  --config ./config/pipeline.config.json \
  --raw ./work/raw/main-clip.mp4 \
  --tts-video ./work/final/main-clip.final.mp4 \
  --final ./work/final/main-clip.final.mp4 \
  --status final \
  --formal true \
  --note "single clip validated with ffprobe" \
  --out ./work/final/delivery-manifest.json
```

### 10) Guard merge ordering before multi-clip export

```bash
tsx scripts/guard-merge-order.ts \
  --input ./config/sample.storyboard.json \
  --panel-indexes 0,1,2 \
  --allow-selective-cut false \
  --out ./work/final/merge-guard.json
```

### 11) Merge final videos through guarded export entrypoint

```bash
tsx scripts/merge-final-videos.ts \
  --config ./config/pipeline.config.json \
  --storyboard ./config/sample.storyboard.json \
  --inputs ./work/final/clip-0.mp4,./work/final/clip-1.mp4,./work/final/clip-2.mp4 \
  --panel-indexes 0,1,2 \
  --out ./work/final/merged.final.mp4 \
  --result-json ./work/final/merged.final.json
```

### 12) Unified submit/poll/download chain after first-image approval

Use this script to avoid manually stitching submit + poll + download commands.

Submit only (no polling):

```bash
node scripts/run-video-submit-chain.cjs \
  --config ./config/pipeline.config.json \
  --panel ./work/seedance/E01/panel-context.approved.json \
  --out-dir ./work/seedance/E01 \
  --duration 6 \
  --resolution 768P
```

Submit and poll until terminal state:

```bash
node scripts/run-video-submit-chain.cjs \
  --config ./config/pipeline.config.json \
  --panel ./work/seedance/E01/panel-context.approved.json \
  --out-dir ./work/seedance/E01 \
  --wait true \
  --max-polls 40 \
  --interval-ms 15000
```

Resume from existing chain state and download on success:

```bash
node scripts/run-video-submit-chain.cjs \
  --config ./config/pipeline.config.json \
  --state ./work/seedance/E01/video-submit-chain.result.json \
  --wait true \
  --download true \
  --output-file ./work/seedance/E01/raw/main-clip.mp4
```

### 13) Dispatch-only planning (no execution)

If assistant role must stay in scheduling-only mode, generate dispatch commands from state without executing anything:

```bash
node scripts/build-dispatch-plan.cjs \
  --state ./work/seedance/E01/workflow.after-first-image.result.json \
  --config ./config/pipeline.config.json \
  --out ./work/seedance/E01/dispatch.plan.json
```

The output includes:
- stage summary
- checkpoint gate
- ready-to-run command strings for operator execution

### 14) New-machine first-run diagnostics (market packaging)

Before first execution on a fresh machine, run:

```bash
node scripts/diagnose-environment.cjs \
  --config ./config/pipeline.config.json \
  --out ./work/diagnostics/seedance-env-check.json
```

This checks:
- required model blocks and placeholder API keys
- ffmpeg / ffprobe availability (PATH or runtime config)
- tsx availability for TS helpers

Mode behavior:
- `minimax_full`: validates upstream + downstream(image/video/tts)
- `vidu_simple`: validates downstream video block first (minimal onboarding; vendor `vidu` or `minimax`)

### 15) Auto onboarding + direct start in `vidu_simple`

`run-seedance-workflow.cjs --action start` now behaves as:
- if config missing/incomplete: returns `currentStage=configuration-guidance` JSON (no hard crash)
- if `runtime.pipelineMode=vidu_simple` and config is ready:
  - builds panel context directly from topic
  - immediately calls `run-video-submit-chain.cjs`
  - returns task/state artifacts for follow-up polling/download

Direct video adapters in current scripts:
- `minimax`: legacy `/video_generation` + query + files retrieve
- `vidu` (ToAPIs-compatible):
  - submit: `POST /v1/videos/generations`
  - poll: `GET /v1/videos/generations/{task_id}`
  - download: use `result.data[0].url` direct download
  - if panel image is local/data-url, upload first via `POST /v1/uploads/images`
- `seedance` (Volcengine Ark-compatible):
  - submit: `POST /api/v3/contents/generations/tasks`
  - poll: `GET /api/v3/contents/generations/tasks/{task_id}`
  - download: use `content.video_url` direct download

### 16) Seedance strict-script runbook (doc-style)

For high-fidelity script matching, use Seedance full-doc-style body:
- `content` includes:
  - `type=text` (strict scene + dialogue semantics)
  - `type=image_url, role=first_frame` (image anchor)
- explicit controls:
  - `duration`, `resolution`, `generate_audio`, `camera_fixed`, `draft`, `seed`, `return_last_frame`

Provider caveat:
- `first_frame/last_frame` cannot be mixed with `reference_image` in one request body, otherwise API returns `InvalidParameter`.

Execution preference:
- split 10s target into panelized `5s + 5s` then concat merge, rather than one long prompt-only generation.

## Output convention summary

- media-producing scripts keep `--out` for the media file itself
- media-producing scripts use `--result-json` for structured metadata output
- pure JSON helper scripts keep `--out` as the JSON destination
- `runtime.ffmpeg` / `runtime.ffprobe` may be supplied in config when PATH is not enough

## Reference files added in this refactor

- `references/checkpoint-policy.md`
- `references/clip-state-contract.md`
- `references/audio-policy.md`
- `references/lipsync-decision-tree.md`
- `references/rhythm-rules.md`
