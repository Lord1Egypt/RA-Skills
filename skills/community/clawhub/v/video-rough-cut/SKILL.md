---
name: video-rough-cut
description: >
  Use this skill for fast rough-cut cleanup of a single talking-head or voiceover
  video using the local B-Roll Studio rough-cut pipeline. It uploads one raw
  video, removes pauses and breaths, trims head/tail clutter, optionally applies
  brightness correction, stabilization, centering, and beauty, then exports a
  cleaned draft. Triggers on: 粗剪, 去停顿, 去气口, 去头尾, 自动粗剪, 防抖,
  人物居中, 亮度修正, talking head cleanup, rough cut, jump cut cleanup.
---

# Video Rough Cut

Use this skill when the user has **one raw talking-head /口播视频** and wants a
cleaned first-pass edit, not a full B-roll edit.

Default output:
- one cleaned draft video
- optional cut-decision review data

## Inputs

Required:
- one local video file

Optional:
- platform preset (`douyin`, etc.)
- whether to remove pauses
- whether to remove breaths
- whether to trim head/tail clutter
- whether to stabilize, auto-center, adjust brightness, apply beauty

## Preferred execution path

Prefer the local B-Roll Studio rough-cut API if the app is running.

Base URL:
- `http://localhost/api/v1`

Use the bundled script:
- `scripts/run_rough_cut.py`

Read [references/api.md](references/api.md) when you need endpoint details.
Read [references/pipeline.md](references/pipeline.md) when you need to explain
what the current rough-cut logic actually does.

## Workflow

### 1. Validate prerequisites

Confirm:
- the input video exists
- local B-Roll Studio is running if you plan to use the API

### 2. Submit a rough-cut job

Use the bundled script:

```bash
python3 <skill-path>/scripts/run_rough_cut.py \
  --video "/absolute/path/to/video.mp4" \
  --base-url "http://localhost/api/v1" \
  --wait \
  --download
```

### 3. Default processing assumptions

Unless the user says otherwise:
- remove pauses: on
- remove breaths: on
- trim head/tail clutter: on
- stabilize: on
- auto-center: on
- brightness adjustment: on
- beauty mode: `light`
- denoise audio: off

### 4. Interpret the output correctly

This pipeline is for **mechanical cleanup**, not final editorial polish.

It is good for:
- removing empty pauses
- trimming `321走 / 试音 / 收镜头动作`
- producing a cleaner draft for review

It is not the right tool for:
- detailed B-roll placement
- manual storytelling edits
- precision subtitle design

### 5. If the user reports quality issues

Typical corrective moves:
- **正文被裁掉**: reduce head/tail trimming confidence or review cut decisions
- **尾部收镜头没裁掉**: inspect cut decisions and rerun with trim enabled
- **声音发闷**: keep denoise off
- **画面太亮**: keep brightness adjustment on; the current pipeline clamps
  over-bright footage instead of only brightening

## Quality bar

The result should feel like a clean draft editor would hand off for review:
- no partial trim of `321走`
- no obvious trailing mirror-check / 收镜头动作
- pauses removed without harming正文
- brightness stays natural
- no heavy-handed denoise by default

## Fallback

If the local API is not available:
- explain that this skill depends on the local B-Roll Studio rough-cut service
- provide the API health check command
- do not invent a separate rough-cut algorithm unless the user explicitly asks
  you to rebuild one

## Bundled resources

- `scripts/run_rough_cut.py`
  Submit, poll, inspect, and download local rough-cut jobs.
- [references/api.md](references/api.md)
  Rough-cut API endpoints and request fields.
- [references/pipeline.md](references/pipeline.md)
  Current rough-cut architecture distilled from the project.
