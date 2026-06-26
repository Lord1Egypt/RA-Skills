# Clipping Reference

Use this reference when the user wants to turn long-form video into short-form clips with captions and export.

Important: the current public API does not expose a single one-shot clipping endpoint. The workflow is orchestrated from existing ingest, transcript, suggestion, timeline, preview, visual QA, repair, caption, and export endpoints.

## What Good Looks Like

- transcript exists and has non-zero words
- short suggestions exist
- chosen suggestion is applied to a project timeline
- the clip uses automatic layout, a smart-cropped vertical asset, source-view podcast reframe, or ROI-aware reframing when available
- preview frames show visible faces and no obvious dead-space failure
- podcast clips pass visual QA before export
- caption items exist on the timeline before export
- captions only cover the selected clip window
- there are no overlapping duplicate captions
- final export duration matches the chosen suggestion envelope within a small frame-rounding delta

## Endpoint Index

| Method | Path | Stage | Operator note |
|--------|------|-------|---------------|
| POST | `/workspace/media/import/youtube` | Ingest | Use for YouTube sources when the user explicitly wants workspace import. |
| POST | `/projects/{id}/media` | Ingest | Use for project-bound local or URL ingest when you need a reliable export path. |
| GET | `/workspace/media/assets/{assetId}` | Readiness | Confirms the media object exists; does not mean clipping is ready. |
| GET | `/workspace/media/assets/{assetId}/reframe-analysis` | Layout readiness | Read the current public automatic-layout analysis state and summary. |
| POST | `/workspace/media/assets/{assetId}/reframe-analysis` | Layout readiness | Queue or materialize reframe analysis before planning or applying layout. |
| POST | `/workspace/media/assets/{assetId}/reframe-plan` | Layout planning | Generate an inspectable public reframe plan with segments, views, and warnings. |
| POST | `/workspace/media/assets/{assetId}/reframe-plan/preview` | Layout planning | Generate a plan plus preview stills before apply. |
| POST | `/workspace/media/assets/{assetId}/reframe-plan/apply` | Layout apply | Apply the public reframe plan to a project timeline. |
| GET | `/projects/{id}/transcript` | Readiness | Use to confirm transcript timing before trusting captions or clip windows. |
| GET | `/workspace/media/assets/{assetId}/short-suggestions` | Readiness | Do not assume asset existence means suggestions are ready. |
| POST | `/workspace/media/assets/{assetId}/short-suggestions/{suggestionId}/apply` | Apply | Prefer this with `automatic_layout` when you want one-call clipping plus planner-backed layout. |
| POST | `/projects/{id}/preview-frame` | Preview | Render one still for quick verification. |
| POST | `/projects/{id}/preview-frames` | Preview | Render several ordered stills for QA. |
| POST | `/projects/{id}/visual-analysis` | Visual QA | Get structured issues from preview stills. |
| GET | `/projects/{id}/visual-debug` | Visual QA | Inspect layout geometry, visible rects, crops, and caption rects. |
| POST | `/projects/{id}/timeline/media-views/{timelineItemId}` | Repair | Upsert crop/canvas/fit/planner state for one item. |
| POST | `/projects/{id}/timeline/media-views/duplicate` | Repair | Duplicate a linked source view to another item for split layouts. |
| INTERNAL | `timeline.generateReframePlan` | Apply | Internal app/editor API only. Use only when operating inside the editor stack and the public API is unavailable. |
| INTERNAL | `timeline.applyReframePlan` | Apply | Internal app/editor API only. Use only when operating inside the editor stack and the public API is unavailable. |
| POST | `/projects/{id}/timeline/media` | Apply fallback | Fallback only when suggestion-apply is missing or weaker than manual assembly. |
| POST | `/projects/{id}/timeline/trim` | Apply fallback | Fallback only; use to reconstruct the suggestion window after timeline insert. |
| POST | `/projects/{id}/captions` | Captions | Captions must be clip-window-aware, not full-asset transcript overlays. |
| GET | `/projects/{id}/context?mode=timeline` | Timeline verify | Use to confirm the clip, captions, and reframing actually landed correctly. |
| POST | `/projects/{id}/export` | Export | Start export only after clip and captions are verified on the timeline. |
| GET | `/jobs/{jobId}` | Export polling | Poll async ingest, transcript, or export work until complete. |
| GET | `/exports/{exportId}` | Export polling | Use for final export status and download URL. |

## Preferred Flow

### Podcast clipping with visual QA

Use this as the normal path for podcast, interview, or two-speaker material.

1. `POST /projects`
2. ingest media
3. wait for transcript and suggestions
4. `POST /workspace/media/assets/{assetId}/short-suggestions/{suggestionId}/apply`
   - send `automatic_layout.enabled: true`
   - send podcast hints
5. inspect apply response
   - check `automatic_layout_applied`
   - check `analysis_status`
   - check `analysis_version`
   - check `layout_summary`
   - check `warnings`
   - if available in the deployed API, also check `visual_qa_status`, `visual_qa_required`, `visual_qa_passed`, and `preview_frame_count`
6. if apply passed QA, export
7. if apply failed QA or visual output is still bad:
   - inspect returned `visual_qa` if present
   - use project preview and visual debug endpoints if available
   - try one repair path
   - rerender previews
   - rerun visual analysis
   - export only after QA passes
8. only bypass with `allow_unverified_export: true` when the deployed API supports it

Blocking QA failures for podcast:

- invalid crop values
- out-of-bounds crops
- single thin strip inside a larger wrapper
- lost faces from bad crop
- captions on faces when split gap or free space exists

### Local file to exported short

Use this path when the user wants a reliable end-to-end result.

1. `POST /projects`
2. `POST /projects/{projectId}/media` with `file_name` and `content_type` to get upload info
3. `PUT` file to the presigned URL
4. `POST /projects/{projectId}/media` with `storage_key`, `file_name`, `content_type`, `file_size_bytes`, `auto_transcribe`, `auto_suggest_shorts`
5. Poll transcript readiness:
   - `GET /projects/{projectId}/transcript?media_id=...`
6. If transcript is still missing after project media processing is `completed`, recover with:
   - `POST /projects/{projectId}/transcribe`
   - then poll `GET /jobs/{jobId}`
7. Poll suggestions:
   - `GET /workspace/media/assets/{assetId}/short-suggestions`
8. Pick a suggestion and apply it through the strongest available path:
   - endpoint stage: Apply
   - for podcast or split-speaker clips, read `podcast-reframe.md`
   - prefer public `reframe-plan` or `reframe-plan/apply` when you need inspectable automatic layout or explicit plan control
   - otherwise prefer suggestion apply with `automatic_layout`
   - prefer a project or API flow that resolves the smart-cropped vertical asset
   - prefer a flow that inserts only caption overlaps for the chosen clip window
   - if a podcast clip returns `409` with `podcast_letterbox_rejected`, treat that as blocked instead of exporting
   - if a podcast clip returns `409` with `podcast_visual_qa_failed`, treat that as blocked and inspect `visual_qa`
   - avoid static `fullscreen` crop plus later trim if a smarter path exists
9. For podcast or two-speaker clips, verify previews before export when the deployed API exposes them:
   - `POST /projects/{projectId}/preview-frames`
   - `POST /projects/{projectId}/visual-analysis`
   - `GET /projects/{projectId}/visual-debug`
10. Apply captions only for the chosen clip window:
   - endpoint stage: Captions
   - if captions are attached by source asset timing, rebase them to the clip start
   - do not attach the entire source transcript to the project timeline
11. Verify timeline:
   - `GET /projects/{projectId}/context?mode=timeline`
   - confirm reframing is not just a static center crop unless no better option exists
   - confirm captions do not overlap or double-render
12. Export:
   - `POST /projects/{projectId}/export`
   - poll `GET /jobs/{jobId}` or `GET /exports/{exportId}`

### YouTube URL to suggestions

Use this when the user explicitly wants BlitzReels to fetch the YouTube video.

1. `POST /workspace/media/import/youtube`
2. Poll:
   - `GET /workspace/media/assets/{assetId}`
   - `GET /workspace/media/assets/{assetId}/short-suggestions`
3. Do not assume success means transcript or suggestions exist.
4. If the user needs a final exported short and the YouTube path does not produce transcript plus suggestions, fall back to a project-bound ingest path.

## Polling Rules

- Asset detail answers "is the media object created?" not "is clipping ready?"
- Transcript answers "can captions and suggestions trust text timing?"
- Short suggestions answer "is clipping ideation ready?"
- Timeline context answers "did the chosen clip and captions actually land in the project?"
- Export status answers "is the deliverable downloadable?"

## Apply Suggestion Manually

Public API does not currently expose a direct "create project from suggestion" flow. Apply it with:

1. Resolve the best clip source first
   - endpoint stage: Apply fallback
   - prefer a derived vertical smart-crop asset
   - otherwise use ROI or analysis-driven reframing
   - only use a static center crop as a fallback
2. Insert the clip with source trim values that match the suggestion window
3. Insert captions only where caption timing overlaps the chosen clip window
4. Rebase caption timeline start times so the clip begins at `0`
5. Verify the new timeline duration matches the suggestion window

Prefer transcript or suggestion timing over asset detail timing if they disagree.

## Repair Paths

Prefer these before giving up on a podcast clip:

1. preview planner output before apply
   - `POST /workspace/media/assets/{assetId}/reframe-plan/preview`
2. inspect layout geometry
   - `GET /projects/{projectId}/visual-debug`
3. repair one item source view
   - `POST /projects/{projectId}/timeline/media-views/{timelineItemId}`
4. duplicate a linked source view to build a split pair
   - `POST /projects/{projectId}/timeline/media-views/duplicate`
5. rerender stills and rerun visual analysis

Do not blind-retry suggestion apply multiple times without inspecting previews or debug data.

## Public Automatic Layout

Use this when the user wants clipping to stay inside the public API and still
benefit from source-view planning.

### One-call suggestion apply

Use:

- `POST /workspace/media/assets/{assetId}/short-suggestions/{suggestionId}/apply`

Include:

- `automatic_layout.enabled=true`
- `automatic_layout.content_type_hint=auto|podcast|tutorial|generic`
- `automatic_layout.layout_strategy=auto|letterbox|split|focus`
- `automatic_layout.aspect_ratio_override=9:16|1:1|4:5|16:9|null`

Expect:

- `automatic_layout_applied`
- `analysis_status`
- `analysis_version`
- `layout_summary`
- `warnings`

### Explicit analyze -> plan -> apply

Use this when the user wants inspectable planner output or tighter control.

1. Read or trigger analysis:
   - `GET /workspace/media/assets/{assetId}/reframe-analysis`
   - `POST /workspace/media/assets/{assetId}/reframe-analysis`
2. Generate plan:
   - `POST /workspace/media/assets/{assetId}/reframe-plan`
3. Apply plan:
   - `POST /workspace/media/assets/{assetId}/reframe-plan/apply`

Hints are advisory, not hard overrides:

- `podcast` can bias toward split or focus
- `tutorial` can bias away from split
- `split` still requires dual-speaker evidence
- `focus` still requires a dominant subject
- weak evidence should fall back with warnings instead of forcing the layout

## Podcast-Specific Reframing

If the user is clipping a podcast, interview, or two-speaker video:

1. Prefer source-view planner reframing when the environment exposes internal
   reframe APIs or the public `reframe-plan` / `reframe-plan/apply` endpoints.
2. Prefer temporal planner segments over one global crop when speaker layout can
   change during the clip.
3. Treat smart-crop derived assets as fallback or perf helpers, not the default
   best path, when planner APIs are available.
4. Avoid forcing one split-screen layout across B-roll or screen-share sections.

## Known Failure Modes

### Processing complete, transcript missing

Meaning:
- ingest pipeline completed enough to mark the asset as processed
- transcription is not yet available or did not run

Recovery:
- call `POST /projects/{projectId}/transcribe`
- poll `GET /jobs/{jobId}`

### Transcript exists but suggestions are empty

Meaning:
- auto-suggest may not have run yet
- or the asset is not eligible

Recovery:
- poll again
- then use `POST /workspace/media/assets/{assetId}/short-suggestions` if available for the asset

### Durations disagree across endpoints

Treat this as a reliability risk.

Use this priority order:
1. chosen suggestion window
2. transcript timing
3. timeline context after trim
4. asset detail duration

### YouTube import gives media but no shorts

Treat YouTube workspace import as ingest-only until transcript and suggestions are confirmed.

### User expects a one-shot clipping endpoint

Meaning:
- the user expects one request to ingest, transcribe, suggest, clip, caption, and export
- the current API does not provide that shape

Recovery:
- explain that clipping is currently a multi-step orchestration
- use the endpoint index stages in order
- only describe a one-shot route as a future product improvement, not as existing API behavior

### Suggestion apply succeeds but podcast framing is still bad

Meaning:
- timeline item exists
- automatic layout may have run
- but visual output is still wrong

Recovery:
- inspect `layout_summary` and `warnings`
- inspect `visual_qa_status` and `visual_qa` if the deployed API exposes them
- render `preview-frames` when available
- inspect `visual-debug` when available
- try `reframe-plan/preview` or media-view repair
- export only after QA passes or the caller explicitly opts into an unverified result

## QA Checklist

- suggestion title matches the actual spoken content
- clip starts with a real hook in the first 1 to 2 seconds
- no dead air at the start or end
- framing follows the area of interest instead of a blind center crop when smart crop or analysis exists
- layout summary and warnings make sense for the chosen clip
- captions exist on the timeline
- captions are limited to the clip window
- no duplicate or overlapping caption overlays appear
- captions are readable against the video background
- preview frames do not show a thin strip or wrong-center crop
- for split podcasts, the split is visibly real and not just stacked bad crops
- export duration is close to the target clip duration
- export format and aspect ratio match the request

## Minimal Commands

```bash
# Poll transcript
bash scripts/blitzreels.sh GET "/projects/${PROJECT_ID}/transcript?media_id=${MEDIA_ID}"

# Poll suggestions
bash scripts/blitzreels.sh GET "/workspace/media/assets/${MEDIA_ID}/short-suggestions"

# Add and trim manually
bash scripts/editor.sh add-media "${PROJECT_ID}" "${MEDIA_ID}"
bash scripts/editor.sh trim "${PROJECT_ID}" "${ITEM_ID}" "${START_DELTA}" "${END_DELTA}"

# Apply captions and export
bash scripts/editor.sh captions "${PROJECT_ID}" viral-center
bash scripts/editor.sh export "${PROJECT_ID}" --resolution 1080p
```
