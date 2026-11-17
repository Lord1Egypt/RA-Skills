# Delivery QA

## Machine Checks

Run:

```bash
python scripts/qa_video.py \
  --video release/video.mp4 \
  --timeline production/timeline.json \
  --cover release/cover.jpg \
  --report release/qa-report.json
```

The report must verify:

- H.264 video and AAC audio
- 1080x1920, 30 fps, `yuv420p`
- stream and container start times near zero
- expected duration within tolerance
- non-black encoded first frame
- MP4 `moov` atom before `mdat` (`faststart`)
- standalone cover exported from the first encoded frame

Run `ffprobe` manually when a check is unclear:

```bash
ffprobe -v error -show_streams -show_format -of json release/video.mp4
```

## Visual Contact Sheet

Generate three samples per scene:

```bash
python scripts/make_contact_sheet.py \
  --video release/video.mp4 \
  --timeline production/timeline.json \
  --output release/contact-sheet.jpg
```

Inspect every tile at a small size. Thumbnail inspection exposes weak hierarchy and empty frames faster than full-screen playback.

Reject when:

- frame 0 is black, incomplete, or missing the article subject
- a scene is blank while waiting for animation
- the lower half remains purposelessly empty
- the product cannot be inspected
- adjacent scenes have the same silhouette
- captions overlap key visuals or fall outside the safe zone
- the CTA or disclaimer is unreadable

## Synchronization Checks

Inspect at least:

- first spoken sentence
- one sentence near the middle
- final CTA and disclaimer

The caption must change at the Edge subtitle boundary, not at a character-count estimate. Check that visual emphasis occurs during the matching sentence, not before or after it.

## Medical Fact Check

Compare the final narration and on-screen text with `content-brief.json`:

- names and dosage forms
- dates and registered capital
- indications and specifications
- platform reach or service claims
- CTA
- disclaimer

No unsupported sentence may remain because it “sounds better.”

## Key-Information Coverage

For `compact-standard`, build a final coverage table before delivery:

| Critical claim | Voiceover | On screen | Contact-sheet tile | Result |
| --- | --- | --- | --- | --- |
| Company date/capital | yes/no | yes/no | scene id | pass/fail |
| Qualification/domain evidence | yes/no | yes/no | scene id | pass/fail |
| Product name/dosage form | yes/no | yes/no | scene id | pass/fail |
| Main indication/use | yes/no | yes/no | scene id | pass/fail |
| Material specification | yes/no | yes/no | scene id | pass/fail |
| CTA | yes/no | yes/no | scene id | pass/fail |
| Disclaimer | yes/no | yes/no | scene id | pass/fail |

Every `critical_claim_id` must be visible on screen or spoken, traceable to a scene, and readable in the contact sheet. Reject a short video that reaches its duration by dropping a critical row.

Confirm compact-standard duration policy:

- ideal output: 30-40 seconds
- preferred information-complete result: 34-38 seconds
- Edge TTS rate: no faster than `+20%`
- exact 30 seconds is not required when it harms readability or coverage

## Encoding Notes

- Build the cover inside the rendered composition at `0.0s`.
- Do not prepend a JPEG using `concat -c copy`.
- Encode with `-movflags +faststart` when FFmpeg is part of the pipeline.
- If the user reports a black idle preview, extract encoded frame 0 and inspect stream start times before changing the design.
