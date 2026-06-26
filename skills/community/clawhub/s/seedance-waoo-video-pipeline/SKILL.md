---
name: seedance-waoo-video-pipeline
description: 自动化短视频工作流（story-to-video pipeline）：从剧本/分镜到生成、字幕 ASR、TTS、合并交付，支持 Seedance / Vidu / MiniMax 多厂商路由。
---

# Seedance + waoowaoo Video Pipeline

## Overview

Use this skill for **story-to-short-video** work where:
- Seedance handles pre-production thinking
- waoowaoo handles production state and media execution
- delivery must distinguish **raw / subtitled / voiced / final / merged** outputs

Seedance upstream must support its own independent configuration for:
- 厂商
- 接口地址
- 模型名
- API Key

This upstream configuration must remain decoupled from downstream image / video / TTS / ambience settings.

This skill is **not** tied to one video vendor.
Model/provider choice stays configurable.
Do **not** force Vidu unless the user explicitly asks for it.

## When to use

Typical triggers:
- “把小说做成短视频”
- “先出分镜，再出片”
- “统一风格做连续短视频”
- “先保一条完整可交付视频”
- “做 6 秒短视频流水线”
- “先做一条，再继续拼接后面的”

## Trigger rules

### Auto-trigger

Trigger this skill immediately when:
- the user wants to turn a story / novel / bridge scene into short video
- the user asks for script → storyboard → video flow
- the user asks for a continuous multi-clip narrative short video
- the user gives only one topic / one sentence / 一句文案 and expects the agent to start from scratch

### Conditional trigger

Use this skill but enter mid-pipeline when the user already has part of the chain ready, such as:
- existing script
- existing storyboard
- existing panel ids / panel images
- existing raw clips
- existing subtitle / TTS / ambience outputs

In that case, resume from the highest reliable completed stage instead of forcing a full restart.

### Do not trigger

Do not use this skill for:
- one-off format conversion
- long-form manual editing
- DAW-heavy sound design
- workflows that depend on fragile manual web login
- pure technical maintenance that is not story-to-video production

## Core principle

**先保主条目，再扩张；先保真实状态，再汇报完成。**

**默认从 0 开始。**
If the user gives only one short idea / one sentence / one文案, this skill must start from the Seedance pre-production side:
- story intent
- script line
- story pack
- storyboard / panel plan
- first image approval
- then downstream video generation

Do not jump directly into middle-stage project APIs, image regeneration, or video submission unless the user explicitly says they already have script/storyboard/panels ready.

Treat the pipeline as 7 execution phases instead of abstract layers:

0. **剧本前置思考 / Story Intent Brief**
1. **目标确认**
2. **素材确认**
3. **视频生成 / 获取**
4. **单条完善**
5. **多条拼接**
6. **交付汇报**

## Default execution policy

When the user does not specify otherwise:

1. Prefer **one fully finished main clip** over many half-finished clips
2. Treat **database/project state as source of truth**
3. Do not count **probe tasks** as formal deliverables
4. Subtitle text is authoritative unless the user explicitly overrides it
5. Ambience must sound like **environment**, not generic music bed
6. If quota is tight, finish the current main clip end-to-end before expanding
7. Lipsync is an **optional downstream stage**, not a default requirement

## User modes

Before running, decide which mode the user is asking for.

### Mode A — 单条保交付模式
Use when the user wants one clip fully usable before anything else.

Default behavior:
- lock one clip as the main target
- do not expand to neighbors until this clip is stable
- prioritize end-to-end delivery over exploration

### Mode B — 逐步确认模式
Use when the user wants to inspect intermediate outputs.

Typical checkpoints:
- outline / story pack
- image / keyframe
- main raw video
- audio direction
- final single clip
- merged cut

### Mode C — 配额敏感直跑模式
Use when the user says “直接做 / 不要一步步问 / 额度有限”.

Default behavior:
- only stop at high-risk checkpoints
- avoid exploratory retries
- preserve formal/probe distinction strictly

Read: `references/checkpoint-policy.md`

## Human-in-loop checkpoints (only two)

The pipeline should run internally end-to-end, but it must pause for user decision at only two checkpoints:

1) 四件套确认（剧本阶段）
2) 首图确认（首图阶段）

If user provides modification hints at either checkpoint, do not handcraft edits manually; route hints back into workflow driver via revision approvals.

Exception:
- when `runtime.pipelineMode=vidu_simple`, the flow may run direct video generation from topic without mandatory pre-production checkpoints (unless user explicitly asks for checkpoint mode).

## Unified workflow driver approvals

When scheduling with `scripts/run-seedance-workflow.cjs`, continue actions must map to stage-specific approvals:

- `seedance-four-pack-confirm`
  - pass: `--approval four-pack-approved`
  - revise: `--approval revise-four-pack --revision-note "<用户修改意见>"`
- `first-image-confirm` / `first-image-internal-generated` / `first-image-asset-confirm`
  - pass: `--approval first-image-approved`
  - revise: `--approval revise-first-image --revision-note "<用户修改意见>"`
- `first-image-asset-blocked` (配置补齐后重试首图)
  - retry: `--approval retry-first-image`

If approval value and stage do not match, the driver must stop with explicit error instead of silently continuing.

## First-run configuration

On first run, do **not** force internal words like `provider` on the user.
Use only:
- 厂商
- 接口地址
- 模型名
- API Key

Auto-detect `runtime.pipelineMode`:
- `minimax_full` (full upstream + downstream)
- `vidu_simple` (direct video-first, minimal keys)
- `seedance_simple` (direct video-first, minimal keys)

Use capability-based routing (not hardcoded model names):
- text only: route to best `text->video` provider
- image + text: route to best `image+text->video` provider
- text only + user requests first-image preview: route `text->image` first

Default routing rule (image + text input):
- If user already provides a reference image, after four-pack confirmation prefer direct `first_frame` binding and skip first-image asset generation.
- Keep script/storyboard continuity constraints, but bind identity from source image at pixel level.

Runtime overrides:
- `--video-vendor <seedance|vidu|minimax>`
- `--image-vendor <seedance|minimax>`
- `--prompt-mode <text-only|first-last-frame|all-reference>`
- `--prompt-style "..."`
- `--prompt-camera "..."`
- `--prompt-scenario <general|ecommerce|narrative|mv|tutorial>`
- `--prompt-auto-fallback <true|false>`（默认 true）
- `--prompt-min-score <0-100>`（默认 80）

Prompt engineering overlay (now built-in):
- `run-seedance-workflow.cjs --action start` will generate `prompt-pack.result.json`
- output includes: mode, assets mapping, timecoded beats, structured prompt blocks
- workflow result also includes `promptQuality`（score/level/suggestions）用于快速判断可用性
- when score < threshold, workflow can auto-try alternate scenarios and output `promptFallback` report
- implementation script: `scripts/build-seedance-prompt-pack.cjs`

ASR routing (subtitle alignment):
- prefer `volc_asr_auc` (`X-Api-Key` + `volc.seedasr.auc`)
- fallback `volc_vc` (`appid + token`, resource `vc.async.default`)
- fallback local `faster-whisper`

When user explicitly requests “按剧本锁定/严格按剧本”: prefer Seedance strict-script profile
- `content`: text + image_url(first_frame)
- explicit `duration / resolution / generate_audio / camera_fixed / draft / seed / return_last_frame`
- do not mix `first_frame/last_frame` with `reference_image` in one request body

Adapter note (current release):
- direct video submit/poll/download adapters are built-in for `minimax` / `vidu` / `seedance`
- config can be single-block (`downstream.waoo.video/image`) or multi-map (`downstream.waoo.videos.*`, `downstream.waoo.images.*`)

If configuration is incomplete, `run-seedance-workflow.cjs --action start` must return a structured `configuration-guidance` result instead of throwing or silently continuing.

**Hard rule for formal Seedance execution:**
- Phase 0 / `E01_前置思考.md` / `E01_剧本.md` count as formal Seedance outputs only when `upstream.seedance` is independently configured with a real 厂商 / 接口地址 / 模型名 / API Key.
- Do **not** silently substitute the current chat model as the formal Seedance upstream model.
- If `upstream.seedance` is missing, placeholder-only, or uses demo credentials, explicitly say that formal Seedance pre-production is not yet runnable and switch to configuration guidance mode.

Read:
- `references/first-run-guidance.md`
- `references/configuration-template.md`

## Phase 0 — 剧本前置思考 / Story Intent Brief

When the user starts from only a topic /一句文案, do not jump directly into script body or production calls.
First build a compact Story Intent Brief that locks:
- what exact event this episode is covering
- where Episode 1 begins and ends
- core conflict
- primary viewpoint
- intended style / tone
- rhythm shape (铺垫 / 设局 / 爆发 / 反转)
- whether the idea is better as one clip, one episode, or multi-clip chain
- obvious production risks

This brief is part of the formal Seedance pre-production stage, not an optional private thought.
It should be reflected forward into `E01_剧本.md`, `E01_素材清单.md`, and `E01_分镜.md`.

**User confirmation rule:**
- After formal Seedance generates the four-pack (`E01_前置思考.md`, `E01_剧本.md`, `E01_素材清单.md`, `E01_分镜.md`), surface that pack to the user for confirmation.
- Do **not** continue into first-image generation, panel execution, or downstream video generation until the user confirms the four-pack.
- Treat this as a required checkpoint, not an optional courtesy.
- After the four-pack is confirmed, the skill may continue internally to generate the first-image candidate.
- Do **not** surface the first-image prompt/spec bundle to the user by default.
- Instead, surface the actual generated first-image asset to the user, and require that approval before any downstream video generation.
- The user only confirms or requests changes.
- The assistant's job is only to notify the skill to continue after confirmation.
- The next internal workflow steps must still be executed by the skill's own continuation entrypoints, not improvised manually by the assistant.

Read:
- `references/story-pack-spec.md`
- `references/pipeline-overview.md`

## Phase 0.5 — Prompt Engineering Overlay（已并入）

Before first-image or video submit, apply Seedance prompt-engineering guardrails:

1) Declare mode first: Text-only / First-Frame / First+Last / All-Reference.
2) Add explicit Assets Mapping (`@image1/@video1/@audio1` each controls what).
3) Use timecoded beats (one major action per segment).
4) Keep prompt concise and controllable; add Negative Constraints when needed.
5) For strict-script requests, prioritize identity continuity + camera continuity.

If user asks for style-rich cinematic prompts, generate from the prompt playbook and then map into panel execution context (instead of freeform rewriting every time).

Read:
- `references/seedance-prompt-engineering.md`

## Phase 1 — 目标确认

Before generating anything, lock the exact target:
- episode id
- panel id / panelIndex
- main clip vs neighbor clip
- whether the user wants **single clip** or **merged output**
- whether the user wants **plain mix** or **optional lipsync**

If the target is ambiguous, resolve it first.
Do not generate against a guessed panel.

## Phase 2 — 素材确认

Resolve the active inputs:
- source image / first-frame image
- active subtitle text (`srtSegment` or equivalent)
- current video prompt
- existing raw outputs
- existing TTS / ambience / merged versions

If multiple versions exist, choose the current **main clip** explicitly.

Before a new generation or first-image approval, run a guard pass for:
- panel identity lock
- image/text/panel consistency
- ordering / duplicate check when multiple panels are involved

Read:
- `references/waoo-input-spec.md`
- `references/clip-state-contract.md`
- `references/panel-order-guard.md`

## Phase 3 — 视频生成 / 获取

If the clip does not exist yet:
1. prepare valid input media
2. submit video task
3. poll status
4. retrieve file / real media URL
5. download the actual file
6. classify the result

Possible classifications:
- probe only
- formal success
- duplicate of existing clip
- failed

If the clip already exists, do not regenerate unless the user asks.

Read:
- `references/model-routing.md`
- `references/runtime-policy.md`
- `references/output-contract.md`
- `references/failure-fallbacks.md`

## Phase 4 — 单条完善

For a single clip, finish in this order:
1. subtitle alignment
2. TTS / dialogue decision
3. ambience decision
4. optional lipsync
5. final single-clip export

### Subtitle rule
The active subtitle text wins unless the user explicitly changes it.
Do not borrow text from neighboring panels.

### Audio rule
Audio strategy must match the user’s request:
- 旁白为主
- 环境音优先
- 不要明显配乐
- 只要无台词环境版
- 要真实说话感 / 要口型验证

Read:
- `references/audio-policy.md`

### Lipsync rule
Lipsync is optional and should only be used when clearly requested.
Do **not** assume lipsync belongs in the main path.

If lipsync is used:
- keep the original full clip as the base truth
- treat lipsync output as a candidate until duration / sync / naturalness are checked
- never silently replace the formal main clip with an obviously shortened or degraded result

Read:
- `references/lipsync-decision-tree.md`

## Phase 5 — 多条拼接

Only merge clips after each included clip has an honest state label.

Before merging:
- confirm ordering
- confirm each clip’s delivery state
- confirm whether to use raw / voiced / ambience / lipsync version
- rebalance cross-clip ambience and loudness

Merged output should not be reported as “完整成片” if one included clip is still experimental.

Read:
- `references/rhythm-rules.md`
- `references/audio-policy.md`

## Phase 6 — 交付汇报

Always distinguish:
- raw generated clip
- subtitled clip
- subtitle + TTS clip
- final single clip
- merged clip

Never call a clip “final” if:
- narration and subtitle are misaligned
- ambience is claimed but not actually audible
- the file was accidentally truncated
- the result only came from a probe task

## Result reporting policy

Always report in this structure:
- **结论**
- **关键点** (1–2 items)
- **下一步**

Never blur these categories:
- probe success
- formal success
- duplicate output
- temporary preview
- final delivery

## References to load when needed

- `references/pipeline-overview.md`
- `references/story-pack-spec.md`
- `references/waoo-input-spec.md`
- `references/model-routing.md`
- `references/runtime-policy.md`
- `references/output-contract.md`
- `references/failure-fallbacks.md`
- `references/checkpoint-policy.md`
- `references/clip-state-contract.md`
- `references/audio-policy.md`
- `references/lipsync-decision-tree.md`
- `references/rhythm-rules.md`
- `references/panel-order-guard.md`

## Scripts provided

Keep deterministic helper scripts small and single-purpose.

Current scripts:
- `scripts/get-panel-context.ts`
- `scripts/guard-panel-order.ts`
- `scripts/guard-merge-order.ts`
- `scripts/prepare-video-submit.ts`
- `scripts/submit-official-video.ts`
- `scripts/merge-final-videos.ts`
- `scripts/poll-official-video.ts`
- `scripts/download-official-video.ts`
- `scripts/generate-tts.ts` (TTS 选择后子脚本级配置检查，缺失返回结构化 `configuration-guidance`)
- `scripts/check-asr-config.ts` (ASR 选择后子脚本级配置检查，缺失返回结构化 `configuration-guidance`)
- `scripts/prepare-ambience.ts` (环境音选择后子脚本级配置检查，AI 模式缺失返回结构化 `configuration-guidance`)
- `scripts/mix-final-video.ts`
- `scripts/build-delivery-manifest.ts`
- `scripts/self-test-workflow-driver.cjs` (用于校验 workflow driver 的阶段/审批映射)
- `scripts/run-video-submit-chain.cjs` (首图确认后统一调度 提交/轮询/下载)
- `scripts/build-dispatch-plan.cjs` (只产出调度指令与检查点，不执行)
- `scripts/diagnose-environment.cjs` (新机器首跑环境自检)

## Guardrails

- Do not expand from one clip to many unless the current main clip is stable or the user explicitly asks
- Do not count probes as formal deliverables
- Do not report “统一风格完成” unless the compared clips were intentionally validated as consistent
- Do not claim environment sound exists unless it is clearly audible and semantically correct
- Do not use a different panel’s text for the active clip narration
- Do not hide failures behind “looks okay”

## Success definition

A clip is **fully delivered** only if all are true:
1. the target clip/panel is correctly identified
2. the video file is formally generated or formally accepted
3. subtitles match the clip content
4. narration/dialogue policy matches the user’s request
5. ambience is correct for the scene and audible
6. final mp4 is exportable and sendable
7. delivery status is reported truthfully

If any item is missing, report the clip as **partial**, not complete.
