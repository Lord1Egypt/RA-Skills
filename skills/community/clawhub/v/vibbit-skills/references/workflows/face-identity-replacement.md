# Replace facial features and hair

Use when the user explicitly wants a person in a reference or adopted video to have the facial features of a supplied person, or reports that only clothing changed and the old face remained. Precise replacement, reference adaptation, template reuse, and batches share this workflow. Prepare an adopted target appearance, remove competing source identity, then generate and compare the result rather than repeating stronger face-swap wording on the same inputs.

Requests to keep the reference performer or only change clothes do not activate this workflow. Distinguish face-only changes, face plus hairstyle, and whole-person replacement. Preserve the requested hair, body, clothing, scene, and sound. This workflow does not guarantee exact identity fidelity with every model.

Retrieve target identity images, qualified upper-body references and saved sources by actual ID through [material reuse](../resources/materials.md). Search only discovers candidates; compare them against the selected person and outfit before adoption. Keep masking tracks, source/prepared-copy relations and local timing in private records; categories do not establish identity or justify reusing tracks from a different source.

## Establish the target appearance

1. **Fix the adopted inputs.** Locate the real source video, target person photo, product/clothing photos, and current result. The source performer supplies only the performance the user wants to retain; the target photo controls facial features. For several people, map each selected performer to its own references.
2. **Reuse or prepare one suitable appearance anchor.** Reuse an inspected photo combining the same intended person, outfit, and retained hairstyle. If absent, use an existing host image editor or [Vibbit image generation](../capabilities/generation/image-generation.md) to depict the target person with the required clothing and preserved features. The original person photo remains the facial authority; the anchor supplies a coherent person-plus-outfit reference. For face-only replacement, retain the adopted clothing and hair. Do not generate a new look, multiple candidates, or a new anchor for every clip/template.
3. **Inspect the anchor first.** Compare eyes, eyebrows, nose, lips, face outline, and requested hair against the original target, then check garment construction. Resolve an already-wrong face, shoulder strap, or old outfit before sending that anchor into video generation. Keep the face readable; use an existing clear close-up when helpful without inventing profile evidence or claiming identity training.

Use the image tools and models actually available in the host. Do not require every Agent to have the same image tool or silently substitute a video model through the image stage. Keep the user's video model and resolution, following the [720p default](../capabilities/generation/video-generation.md#paid-video-settings) when unspecified. Continue necessary preparation within the authorized production; ask only for missing target identity, an actual execution blocker, or expanded quantities/cost.

## Prepare a real motion reference without the old identity

Create a separate derivative retaining the actual reference video's shots, body/hand movement, and setting while obscuring the source facial features. Include source hair when changing hair or the whole person. Follow actual head position, scale, turns, wide/close views, cuts, reappearances after occlusion, and selected reflections or on-screen appearances. A single-frame patch, weak blur that preserves the old face, or a fixed box missing the moving head is insufficient.

Cover only the parts being replaced and retain useful movement and setting cues. Preserve source hair when requested. Keep the original and adopted result separate from the derivative; save tracking with this production. Reuse an already-inspected anonymized motion reference when applicable.

Use an available host video tool or the bundled [local preparation helper](../../scripts/prepare-identity-reference.js). It needs existing Node.js, FFmpeg, and ffprobe; no API key, Python imaging library, face-recognition model, or dependency installation. It produces a silent reference from regions measured by the Agent. It does not detect faces, prove coverage, or perform face replacement. If processing is unavailable, reuse a suitable existing derivative or an actual supported host route. Otherwise preserve progress and explain the missing capability rather than silently spending a generation with the competing old face.

### Local preparation helper

Trim the needed source clip and normalize orientation before measuring regions. Times are **clip-local seconds** from its first video frame; `box` uses source pixels `[x, y, width, height]`, not normalized coordinates. Use a separate track per appearance interval. Keyframe times increase and cover both ends of that interval; do not interpolate across cuts. Choose enough keyframes for actual movement.

This illustrates structure only. Replace the file, times, and coordinates with actual measurements:

```json
{
  "source_file": "/absolute/private/source-clip.mp4",
  "fps": 30,
  "tracks": [
    {
      "id": "selected-presenter-shot-1",
      "from_seconds": 0,
      "to_seconds": 4,
      "keyframes": [
        { "at_seconds": 0, "box": [80, 180, 160, 260] },
        { "at_seconds": 2, "box": [170, 120, 220, 340] },
        { "at_seconds": 4, "box": [220, 70, 280, 410] }
      ]
    }
  ]
}
```

```bash
node "$VIBBIT_SKILL_DIR/scripts/prepare-identity-reference.js" --plan /absolute/private/tracking.json --out /absolute/private/reference-head-obscured.mp4 --dry-run
node "$VIBBIT_SKILL_DIR/scripts/prepare-identity-reference.js" --plan /absolute/private/tracking.json --out /absolute/private/reference-head-obscured.mp4
```

The output keeps source dimensions, normalizes to the requested frame rate, and obscures measured regions. Source audio is absent from this intermediate file. Existing output is never overwritten. The report records hashes, frames, duration, and tracked-region counts; technical success does not verify visual coverage. Inspect turns, movement boundaries, wide shots, and the ending for exposed old faces or excessive loss of useful motion. Gray regions are reconstruction guidance and must not appear in the delivered video.

## Bind the real request and sound

- Assign actual input roles: original person photo for facial features, appearance anchor for a coherent person and outfit, product front/back photos for construction, and the **actual anonymized video** for motion/camera/setting. Avoid transferring old people, clothing, or photo backgrounds. When the user requested a video reference, verify `reference_video_urls` is populated and retain source-to-derivative provenance; a written description does not count as a submitted video.
- State that the source head was deliberately obscured and must be fully reconstructed as the selected person. Exclude censor boxes, blank/blurred faces, and the old performer. Define original-photo versus anchor priority; actual target facial features and product evidence take precedence over anchor errors. Number only the files actually supplied; do not add irrelevant images to fill a template.
- Validate the actual model, resolution, reference counts, duration, and mode against the [Seedance API](../api/seedance.md). Omit `omni_reference_task_type` for 2.0/fast/mini. For 2.5, select reference generation or original-footage editing according to user intent. Identity priority does not authorize changing the chosen remake approach.
- Follow the parent workflow's sound route. For visual-only changes, follow [precise replacement audio handling](one-to-one-remake.md#route-audio-before-submission), preserve the full original soundtrack, and restore it after visual assembly and alignment. If the editing route needs audible source input, restore actual source audio to the helper's silent derivative before upload; the helper must not silently remove that requirement. New-script adaptation explicitly generates new speech rather than inheriting old product claims. Check real timing, performance, and lip sync.

Do not promise frame-exact preservation or perfect identity fidelity. A more expensive model, 1080p, repeated prompts, or silently dropping the requested video reference does not replace this preparation.

## Review, revise, and reuse

Review the actual result with [video review and targeted revisions](../capabilities/analysis/video-review.md):

- Compare eyes/brows, nose, lips, face outline, and hair with the target photo in wide, frontal, profile, post-turn, and final close-up views. Changing only hair or clothing while retaining source facial features is not successful face replacement.
- Check for copied masks/blur/blank faces and regressions in people, clothing, straps, color, hands, and retained elements. ASR, task completion, hashes, or a face merely differing from the previous result cannot establish target resemblance.
- When playback is possible, assess motion, sound, and lip sync. With stills only, disclose that scope; leave final resemblance to actual viewing and user adoption rather than claiming a perfect match.

For isolated drifting shots, reuse good footage, references, and sound; repair only affected clips with necessary context and splice back. Expand to all appearances only when the identity error is global. Reuse one suitable appearance anchor across batch items sharing person and outfit. Resume existing task IDs. Continue ordinary authorized preparation/revisions without repeated per-clip approval, while avoiding unlimited automatic regeneration.

Keep original person/product photos, the anchor and its roles, source/anonymized video, measured regions/time mappings, prompts, requests, tasks, sound route, and results in private [production handoff](../contracts/creative-handoff.md). Record the facial authority and reviewed clips. Preserve the base template; never include customer media or real task links in the public Skill.
