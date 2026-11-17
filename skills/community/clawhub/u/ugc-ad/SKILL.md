---
name: ugc-ad
description: >
  Make a creator-style or UGC ad video: a direct-to-camera testimonial, a product demo, an
  unboxing, or a faceless voiceover cut. Use when the user says "make a UGC ad", "creator-style
  ad", "talking-head ad for TikTok", "spokesperson reading my script", "product demo video",
  "testimonial-style ad", or "voiceover ad for Reels". A top-of-funnel social format. For a
  polished hero product spot with no creator, use product-ad-video. For just a talking portrait
  with no ad structure, use talking-avatar.
---

# UGC ad video

Produce a short, creator-style ad: a presenter talking straight to camera (testimonial, demo, unboxing) or a faceless voiceover over product footage. The output reads like organic social content, not a polished broadcast spot. The levers are a talking-avatar presenter, the script or audio that drives it, and the background/framing/captions tuned for the target feed.

## Inputs to collect

- **The format:** direct-to-camera testimonial, product demo, unboxing, or faceless voiceover. This decides whether you need a presenter on camera at all.
- **The script** (for the TTS path) or **your own audio file** (for the lip-sync path). One or the other, never both.
- **The product** and the single claim the ad should land. (Ask for real specifics. Do not invent features.)
- **Target platform and orientation:** 9:16 for TikTok / Reels / Shorts, 16:9 for YouTube / web.
- Optional: a chosen avatar/voice, a brand background, whether captions should be burned in.

## Models

- **Presenter on camera. Default: HeyGen Avatar V** (`heygen:avatar@5`). A registered-look talking avatar with two drive modes (script-to-speech or your own audio) plus background, fit, and caption controls. Best general pick for a person reading the ad.
- **Presenter alternative: OmniHuman-1.5** (`bytedance:5@2`) when you want to animate a specific supplied photo into a speaking presenter rather than pick from a registered catalog.
- **Faceless voiceover:** generate the spoken track with the `voiceover` skill (a TTS model), then lay it over product footage produced by `product-ad-video`. No avatar needed.
- Confirm each model is `live` and inspect its schema via `runware-models` + `runware-run` before calling. Never hardcode a stale choice, since the catalog changes weekly.

## Workflow

This is an **async** outcome (video). Follow the `runware-run` contract.

1. Resolve the presenter model's schema (`runware-run`) and confirm the field names: the required avatar/look input, the `speech` block, the `inputs.audio` field, and the `settings` for background/fit/caption.
2. Upload any inputs (a supplied photo for OmniHuman, a brand background image, or your own audio) and reference them by URL or UUID.
3. Build the request with `taskType: "videoInference"`, the model AIR, the avatar/look, and **exactly one** drive path (see Technique).
4. Set `width`/`height` for the target orientation and the `settings` for background, fit, and captions.
5. Run **async**: the task returns a `taskUUID`. Poll `getResponse` until terminal, then read `videoURL` from the result.
6. Iterate on a short take first (a 10-second script renders fast and surfaces avatar/voice mismatches), then send the full cut.

## Technique

Ground the ad in a **named build-order** so it earns attention before it asks for anything:

1. **Hook.** The first two seconds: a problem, a bold claim, or a pattern interrupt. Attention drops off fast on social, so the hook carries the ad.
2. **Context.** Who this is for and the problem it solves.
3. **Product moment.** Show or name the product doing the thing.
4. **Proof.** A real demonstration or genuine result. Never a fabricated testimonial, metric, or review.
5. **Call to action.** One clear next step.

Fill this in with the user's real copy before generating the script, then flatten it into `speech.text` (or the recorded audio):

```
HOOK (0-2s): <problem, bold claim, or pattern interrupt>
CONTEXT: <who this is for and the problem it solves>
PRODUCT MOMENT: <the product doing the one thing>
PROOF: <a real demonstration or genuine result, supplied wording only>
CALL TO ACTION: <one clear next step>
```

Load `references/examples.md` for three worked recipes (TTS testimonial, own-audio demo, 9:16 captioned cut) with the full request and result shape.

**Pick exactly one drive path. Sending both errors.**

- **TTS path:** supply a `speech` block with `text` (the literal script) and `voice` (the catalog voice). Best for fast copy iteration and localization. Voice tuning (`speed`, `pitch`, `volume`, `language`) only exists on this path.
- **Lip-sync path:** supply `inputs.audio` (a public URL or an uploaded-asset UUID) and omit the `speech` block entirely. Best when you already have the exact delivery: a real human recording, a voice clone, or a track from a separate TTS run (the `voiceover` skill). The model extracts phonemes from the audio and animates the mouth to match.

**Compose for the feed, not the model.** Most of what makes UGC read as native happens around the presenter:

- **Background:** run `settings.removeBackground: true` together with **either** `settings.backgroundColor` (a hex string) **or** `inputs.background` (an image). Removing the background alone just falls back to the avatar's original environment. Matting only works for avatars trained with it enabled.
- **Orientation first, then resolution.** Choose 9:16 vs 16:9 by where the ad plays, then pick the resolution. Match any background image's aspect ratio to your output dimensions.
- **Fit:** for portrait output, `settings.fit: cover` is almost always right (it crops the landscape source to fill the tall frame). `contain` letterboxes and rarely looks production-ready in portrait.
- **Captions:** `settings.caption: true` burns subtitles into the video. Use it for silent-autoplay feeds and accessibility. The style is fixed, so render without it and overlay your own if you need custom typography.

**Persona match.** Pair the avatar and voice deliberately. A mismatched voice and face is jarring and breaks the organic feel UGC depends on. Lock both before iterating on copy.

## Parameters that matter

- **Drive path is mutually exclusive:** `speech` (TTS) **or** `inputs.audio` (lip-sync), never both.
- `speech.speed`: `0.5` to `1.5`, default `1.0`. Faster reads suit short social cuts where attention drops early.
- `speech.pitch`: `-50` to `+50`, default `0`. Keep adjustments small (±5 to ±15) or it sounds processed.
- `speech.volume`: `0.0` to `1.0`, default `1.0`. Lower it to leave room for a music mix.
- `speech.language`: a BCP 47 locale (`en-US`, `es-ES`, and so on). Same voice, translated script, one locale code per market is the cheapest way to localize at scale.
- `width`/`height`: fixed 16:9 or 9:16 sets (e.g. 1080×1920 portrait, 1920×1080 landscape). 1080p is the production default, 720p for iteration.
- `settings.removeBackground`, `settings.backgroundColor`, `inputs.background`, `settings.fit`, `settings.caption`: the composition levers above.
- Confirm exact field names against the live schema (`runware-run`); never guess.

## Quality bar

- The hook lands in the first two seconds and the build-order flows Hook → context → product moment → proof → call to action.
- Exactly one drive path is set. The request validates (dry-run via `runware-run` if unsure).
- No fabricated testimonials, metrics, reviews, or on-screen claims. Only real, supplied wording appears as readable copy.
- Avatar and voice are a believable pair, not a jarring mismatch.
- Orientation, fit, background, and captions match the target platform: portrait plus `cover` plus burned-in captions for Reels/TikTok, landscape for YouTube/web.
- The cut reads as native creator content, not a stiff corporate spot.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `voiceover` (generate the spoken track for the lip-sync path), `talking-avatar` (presenter mechanics in depth), `product-ad-video` (footage for faceless cuts).
