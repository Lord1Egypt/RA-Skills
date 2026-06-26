# Checkpoint Policy

## Goal

Define when the pipeline should stop for user confirmation versus auto-continue.

## Hard stop checkpoints

Always pause when any of these is true:
- the formal Seedance four-pack (`E01_前置思考.md`, `E01_剧本.md`, `E01_素材清单.md`, `E01_分镜.md`) has been generated and not yet confirmed by the user
- the first actual generated first-image asset has been produced and not yet confirmed by the user
- the target panel/clip is ambiguous
- panel identity lock fails, or `panelId` / `panelIndex` point to different targets
- image/text/panel consistency is uncertain for the active clip
- a new paid video generation is about to start
- the model/vendor is changing
- image style clearly drifts from approved neighbors
- the user’s subtitle/dialogue intent changes
- a result is only a probe but may be mistaken as formal success
- lipsync output may replace an existing formal clip

## Soft checkpoints

Usually pause, unless the user asked for direct-run mode:
- first usable image for a new clip
- first usable raw video for a new clip
- first full audio mix for a clip
- first merged multi-clip export
- any ordering warning before multi-clip merge (missing index / possible skip)

## Auto-continue allowed

You may continue without explicit confirmation when:
- only subtitle timing is being corrected
- TTS text exactly matches already approved subtitle text
- ambience is being fine-tuned without changing scene intent
- export format/container is being fixed
- a file needs simple resend/re-export

## Workflow driver approval mapping (hard rule)

When using `run-seedance-workflow.cjs --action continue`, approval must match stage:
- `seedance-four-pack-confirm` -> `four-pack-approved` (pass) or `revise-four-pack` (+ `--revision-note`)
- `first-image-confirm` / `first-image-internal-generated` / `first-image-asset-confirm` -> `first-image-approved` (pass) or `revise-first-image` (+ `--revision-note`)
- `first-image-asset-blocked` -> `retry-first-image` (only after config/input blocking reasons are fixed)

If stage and approval mismatch, the driver should stop with explicit error and no silent auto-progress.

## Mode-specific behavior

### 单条保交付模式
- prefer fewer checkpoints
- stop only on cost, model switch, or obvious drift

### 逐步确认模式
- stop after every meaningful artifact
- do not batch multiple new risks into one silent step

### 配额敏感直跑模式
- stop only at hard checkpoints
- preserve truthful status labels even if you do not pause often
