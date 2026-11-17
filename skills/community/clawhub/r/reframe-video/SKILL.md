---
name: reframe-video
description: >
  Convert a video to a new aspect ratio without cropping the subject. Use when
  the user says "make this 16:9 clip vertical for Reels", "reframe to 9:16",
  "turn my landscape video into a square", "fit this for TikTok/Shorts", "add
  more space around the subject", or "extend the edges of this footage". The
  model paints the new edges instead of trimming the old ones.
---

# Reframe video

Take a finished clip and place it on a new canvas at a different aspect ratio, then let the model extend the scene to fill the space the original didn't cover. One horizontal master becomes a vertical cut for social or a square cut for a feed, without cropping away the subject, because the model generates the new edges. This is outpaint-style edge generation, distinct from `edit-video` (which reworks the look and holds the source aspect ratio) and from a plain crop (which throws pixels away).

## Inputs to collect

- **The source video** (URL or upload). This is the clip being reframed.
- **The target aspect ratio / canvas** (e.g. 16:9 → 9:16, or 1:1). This sets the new `width` and `height`.
- **What fills the new space.** A short description of the surroundings to extend ("sky above and sea below", "more street to the left"). The prompt drives the extension.
- Optional: **where the source sits** in the new frame, if not centered (bias the new space toward one edge).
- Optional: target resolution tier (360p through 1080p).

## Models

- **Luma Ray 3.2** (`luma:ray@3.2`) - the model for this outcome. It supports `inputs.video` with a new canvas at a different aspect ratio and `settings.sourcePosition` for placing the source. Confirm it is `live` and inspect its schema via the `runware-models` + `runware-run` skills before calling. Never hardcode a stale choice.
- No general fallback for reframing today. If reframing is unavailable, the alternative is a crop (loses the subject) or frame extension on a same-aspect canvas (see Technique).

## Workflow

1. Resolve the model schema (`runware-run`) and confirm `inputs.video`, the supported `width`/`height` pairs, and the `settings.sourcePosition` shape.
2. Upload or pass the source clip URL into `inputs.video`.
3. Run `videoInference` **asynchronously**: the call returns a `taskUUID`, then poll `getResponse` until terminal. Reframing is a video job, never block a sync call on it.
4. Set `width` and `height` to a supported pair at the **target** aspect ratio (different from the source).
5. Write a prompt that names what continues into the new area so the model extends the scene instead of inventing unrelated content.
6. Read the result from `videoURL`. Review the extended edges, then retry with a clearer prompt or a different `sourcePosition` if the extension drifts.

## Technique

- **Name what fills the new space.** A reframe prompt describes the surroundings to extend ("continuing the sky above and the sea below the lighthouse, matching the source light and motion"), so the model continues the scene rather than guessing. The prompt matters as much as the canvas.
- **Pick the new canvas from supported pairs.** `width`/`height` must be a real Ray 3.2 output size (the same set generation uses), landing at 360p through 1080p. Choose the pair whose ratio matches the target (e.g. 720 × 1280 for 9:16, 960 × 960 for 1:1).
- **Keep the subject off the edges you're growing.** Reframing has the most room to work when the subject sits clear of the sides being extended.
- **Position the source to bias where space opens.** By default the source centers in the new canvas. `settings.sourcePosition` overrides that with `x`, `y`, `width`, `height` as **fractions of the canvas**. Push the source toward one edge and the model fills the opposite side (raise `x` to pull it right so the new sea opens on the left, raise `y` to pull it down so more sky opens on top).
- **Shrink the source to extend, not just convert.** Set `sourcePosition` width/height below `1.0` (e.g. the middle 60%) and the model extends the scene all the way around the original. That turns reframing into frame extension on any canvas, including a same-aspect one.
- **Reframe as a final step.** Lock the look first with `edit-video`, then reframe the result, so you extend footage that already looks right.

## Parameters that matter

- `inputs.video` - the source clip (URL or base64). Required.
- `width` / `height` - the new canvas. Must be a supported pair and should differ in aspect ratio from the source. Output tiers run 360p through 1080p.
- `positivePrompt` - describes what continues into the extended area. This steers the edge generation.
- `settings.sourcePosition` - `{ x, y, width, height }`, each a fraction of the canvas, all four required when used. `x`/`y` place the source, `width`/`height` size it. Below `1.0` size means the model fills the border around the source.
- Reframe runs as standard dynamic range only and bills per second. Confirm pricing via `runware-models` or a dry-run (`runware-run`).
- Confirm exact field names and the live supported pairs against the schema (`runware-run`). Never guess.

## Quality bar

- The output is at the **target** aspect ratio and the subject is fully kept, not cropped.
- The extended edges continue the source scene (matching light, motion, and content), not unrelated invented material.
- Motion in the original region stays stable across the reframe.
- If the extension drifts, retry with a prompt that names the surroundings more precisely or a `sourcePosition` that opens space where you want it.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `edit-video` (transform the look at the source aspect ratio, the sibling operation), and lock the look there before reframing as a final step.
