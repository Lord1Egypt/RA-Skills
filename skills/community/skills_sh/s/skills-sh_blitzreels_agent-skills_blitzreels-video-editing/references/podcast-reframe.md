# Podcast Reframe Reference

Use this reference when the user wants any of:

- podcast-to-shorts
- host/guest split layout
- interviewer on one side, guest on the other
- ROI-aware reframing from one landscape source
- source-view or view-based reframing
- editable podcast reframing instead of a baked vertical MP4

## Decision

Prefer source-view planner reframing when the public automatic-layout API or the
internal editor planner exposes it.

Why:

- editable timeline output
- sync-locked multi-pane views from one source
- safer path for split speaker layouts
- better fit for podcast clips than a single baked smart-crop window

Treat derived smart-crop assets as a fallback or perf helper, not the preferred
truth, when a source-view planner path is available.

## API Surface

### Public REST API

Public clipping now supports named automatic-layout endpoints:

- `GET /workspace/media/assets/{assetId}/reframe-analysis`
- `POST /workspace/media/assets/{assetId}/reframe-analysis`
- `POST /workspace/media/assets/{assetId}/reframe-plan`
- `POST /workspace/media/assets/{assetId}/reframe-plan/apply`
- `POST /workspace/media/assets/{assetId}/short-suggestions/{suggestionId}/apply`
  with `automatic_layout`

Use these first when the task must stay inside the public API.

### Internal App/Editor API

When operating inside the BlitzReels app/editor stack, the lower-level path is:

- `timeline.generateReframePlan`
- `timeline.applyReframePlan`

Those endpoints can create inspectable source-view timeline segments directly.

Treat them as internal app/editor APIs, not the default documented route.

## Preferred Order

1. If the public automatic-layout API is available:
   - prefer `reframe-plan` when the user wants inspectable output
   - prefer `reframe-plan/apply` when the user wants explicit planner control
   - or use suggestion apply with `automatic_layout` for one-call clipping
2. Else if internal source-view planner APIs are available:
   - prefer `generateReframePlan`
   - inspect the plan if needed
   - apply with `applyReframePlan`
3. Else if suggestion apply preserves strong reframing:
   - use suggestion apply
4. Else:
   - fall back to the best available smart-crop asset or manual timeline path

## What To Prefer By Content Type

### Stable two-speaker podcast

Prefer:

- source-view planner split layout
- or source-view linked panes

Fallback:

- smart-crop asset if planner is unavailable

### Podcast with changing speaker focus

Prefer:

- temporal source-view planner segments

Fallback:

- suggestion apply if it preserves ROI-aware reframing

### Podcast with B-roll or screen inserts

Prefer:

- source-view planner with segment fallback

Avoid:

- forcing split-screen across the entire clip

## QA Checks

- reframing is not a blind center crop
- split panes are frame-locked when both are present
- focus cuts do not drift off the speaker
- warnings explain any fallback from split to focus or letterbox
- clip-window captions still match the selected suggestion timing
- exported short stays `9:16`

## Reporting

When you use this path, report:

- whether the environment was public REST or internal app/editor
- whether public `reframe-plan` or `automatic_layout` was used
- whether source-view planner APIs were available
- whether the final path used source-view reframe, smart-crop asset, or fallback
- any reason the stronger podcast reframe path could not be used
