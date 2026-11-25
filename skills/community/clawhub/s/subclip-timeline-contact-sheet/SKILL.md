---
name: subclip-timeline-contact-sheet
description: Review and analyse a whole Subclip timeline in bulk. Use analyze_timeline for a one-call structural reading of the project and get_timeline_contact_sheet to see many labelled frames of the composed timeline in one image. Use before and after edits, for QA, for style and theme checks, and whenever more than one frame needs a decision, instead of viewing frames one at a time.
---

# Subclip Timeline Contact Sheets

One frame per call is slow and spends tokens on repeated setup. A contact sheet renders the moments you choose from the saved, composed timeline (media, Remotion, HyperFrames, 3D, text, captions) and returns them together as a labelled grid, so you can judge every doubtful moment in one round and fix them in bulk.

## Tools

- `analyze_timeline`: one call, no guessing. Duration, canvas, layers by lane, scene boundaries and pacing, audio roles and volumes, titles and caption summary, fonts and colours, mood hints, a colour palette sampled from real frames, a list of issues with times, and `recommendedContactSheetTimes`. `withContactSheet: true` adds the overview sheet. `renderFrames: false` gives an instant text-only answer.
- `get_timeline_contact_sheet`: the images. Pick moments with `times` (seconds), or `from` + `to` with `count` or `every`, or `at`: `auto`, `scene-changes`, `layer-starts`, `caption-pages`. Each tile shows `#index  m:ss.s  fFRAME`; refer to "tile 7" or "0:12.4" in your notes and in follow-up edits. Tiles marked `HF OFF` were rendered without HyperFrames layers (the HyperFrames browser was unavailable, or you asked for `hideHyperframes: true`); do not judge those layers from them.

Both are fast by default: `detail: "fast"` renders every tile at tile size (320 px), not at full canvas size, so a sheet of 12 usually returns in a few seconds, and frames already rendered for the current saved revision are reused (repeating a sheet, or re-checking just the changed times, is almost instant). This is a medium-resolution look meant for quick decisions, not for reading small print. Use `detail: "balanced"` (384 px tiles from a 2x render) when text in tiles is hard to read, and `detail: "full"` (whole canvas rendered, then scaled down: the slowest) or a single full-size frame with `view_current_frame` / `export_current_frame` only for the few moments that need a close look. Do not ask for `full` for a first review.

Sheets and manifests are written to the app cache (not into the project), and the result gives their absolute paths; pass `saveToProject: true` on `get_timeline_contact_sheet` to keep them in the project workspace. Both work in the background on the latest saved revision; the project does not need to be open. If a render takes longer than `waitSeconds`, the result has `status: "running"` and a `jobId`: call `get_timeline_contact_sheet` again with that `jobId`. Read `progress.progressState` (`advancing`, `waiting`, `stalled`) and `progressPercent` before you decide anything is stuck; the first HyperFrames frame can take a while while its browser starts. Sheets are saved in `outputDirectory` (the app cache by default), so you can read them again without rendering.

## Workflow

1. Orient: `analyze_timeline` (default settings). Read `issues` first, then `scenes`, `style` and `text`. This replaces most outline reads for a first look.
2. Look: `get_timeline_contact_sheet` with `at: "auto"`, or with `times` taken from `issues[].at` and `recommendedContactSheetTimes`. Put every moment you are unsure about into the same call.
3. Decide in bulk: write one fix list keyed by tile number and time (for example "tile 4 0:08.2 title clipped right; tile 7 1:02.0 caption over logo"), then apply all the fixes before looking again.
4. Verify only what changed: call `get_timeline_contact_sheet` again with `times` limited to the changed moments (and one moment either side of a cut you moved). Compare with the first sheet. Do not re-render the whole timeline after a small edit.
5. Finish with one overview sheet (`at: "auto"`) as the final evidence. Never claim a visual result you have not seen in a rendered tile after your last edit.

## Choosing times

- Whole-video review: `at: "auto"` (12 tiles). Longer videos: `count: 24` (two sheets) or several `from`/`to` windows.
- Pacing and cuts: `at: "scene-changes"`. Titles and overlays: `at: "layer-starts"`. Caption styling and line breaks: `at: "caption-pages"`.
- Timing of a transition, entrance or exit: one sheet with `every: 0.1` (or about three frames either side of the moment) over a short `from`/`to` window. Sheets a second apart miss 1 to 3 frame timing. Convert frames to seconds as frame divided by fps, rounded down.
- Before and after: render the same `times` before and after the edit and compare tile by tile.
- A time past the end is moved to the last frame; two times on the same frame are merged. Read `notes` in the result.

## Token budget

- A tile is 320 px wide by default and a sheet of 12 costs roughly 1,000 to 1,500 image tokens (see `estimatedImageTokens`). Use the defaults for review. For small text prefer `detail: "balanced"` over a bigger sheet; raise `tileWidth` (up to 960) and lower the tile count only when you really need more pixels per tile. Check `renderSeconds`, `cacheHits` and `concurrency` in the result to see how much was rendered versus reused.
- Prefer fewer, deliberate sheets. Up to 48 tiles per call (split into sheets of 12). Use `includeImages: false` when you only need the saved files or a count.
- HyperFrames layers are captured through a browser; the first frame of each layer is the slow one, later frames of the same layer reuse the warm browser. `hideHyperframes: true` is still the fastest path for a quick layout check on a heavy project; render the HyperFrames layers on the final check.

## Reading what you see

Check, per tile: clipping and off-canvas placement, text collisions and safe margins, black or empty frames, stacking order, caption legibility, consistent fonts and colours with the rest of the video, and anything that looks different from the neighbouring tiles. Compare the picture with `analyze_timeline`: a tile that is empty where a layer should be visible is a real defect, not a rendering quirk, unless it is marked `HF OFF`.

Use `view_current_frame` (full size) only for the single moment you need to inspect closely after the sheet shows a doubt; use `extract_video_frames` only on a source file, not on the timeline.
