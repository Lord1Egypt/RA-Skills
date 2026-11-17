---
name: talking-avatar
description: >
  Make a person, portrait, or avatar talk on camera. Use when the user says "make this photo
  talk", "talking head video", "lip-sync this to my audio", "turn my script into a presenter",
  "avatar reads this text", "sync this video to a new voiceover", or wants a spokesperson,
  explainer, or presenter driven from a script or audio file. For a full creator-style ad built
  around the talking head, use ugc-ad. For only the spoken audio with no video, use voiceover.
---

# Talking avatar

Drive a talking-head video from a still portrait or a registered avatar. Two ways in: write a script and let the model speak it (text-to-speech), or hand the model your own audio and it lip-syncs the face to it. The output is a video of someone delivering your words. Use this for presenters, explainers, spokespeople, and re-voicing footage. For a full ad or a standalone voice track, compose with the sibling skills below.

## Inputs to collect

- **The face.** A portrait image of the person, or a registered avatar ID for catalog-based models. (Ask only if none provided.)
- **The words.** Either a script (you generate the voice) or an audio file (you supply the voice). One or the other, not both.
- **Voice** if going the script route: which TTS voice reads it, plus optional target language.
- **Where it plays:** orientation and resolution for the target platform (16:9 for web/YouTube, 9:16 for Reels/TikTok/Shorts).
- Optional: a background to composite behind the speaker, and whether to burn in captions.

## Models

Confirm the live model + its schema via `runware-models` + `runware-run` before calling. Never hardcode a stale choice. All carry the `io:audio-to-video` capability.

**Portrait / avatar driven** (a still image or registered look becomes the speaker):

- **HeyGen Avatar V** (`heygen:avatar@5`): registered-avatar presenter with the richest composition controls (background, framing, captions, multilingual TTS). Best general pick for a polished spokesperson.
- **OmniHuman-1.5** (`bytedance:5@2`): image + audio, strong expressive full-body motion from a single portrait.
- **KlingAI Avatar 2.0** (`klingai:avatar@2.0-standard`): expressive avatar video from image + audio.

**Lip-sync onto existing footage** (re-voice a person already on camera):

- **sync-3** (`sync:3@0`): full-scene lip sync with obstruction handling. Accepts a script or audio.
- **lipsync-2-pro** (`sync:lipsync-2-pro@1`): high-resolution diffusion lip-sync editing up to 4K.
- **PixVerse LipSync** (`pixverse:lipsync@1`): realistic lip sync from audio onto any reference video.

## Workflow

These are video tasks, so they run **asynchronously**.

1. **Pick the model + path.** Portrait/avatar to a talking head: HeyGen / OmniHuman / Kling. Re-syncing existing footage: sync-3 / lipsync-2-pro / PixVerse. Resolve the schema (`runware-run`) and confirm the exact `inputs` field names before calling.
2. **Choose exactly one drive mode:**
   - **TTS path:** set `speech.text` (the script) and `speech.voice`. The model generates the voice.
   - **Audio path:** set `inputs.audio` (a public URL or an uploaded asset UUID). The model extracts phonemes and animates the mouth to match.
   - Sending both errors. Not every model exposes `speech`, so on those use the audio path.
3. **Provide the face.** Upload the portrait into the image field (`inputs.image`), pass a catalog `inputs.avatar` ID where the model uses one, or for lip-sync pass the source footage (`inputs.video` / `inputs.referenceVideos`).
4. **Compose for the platform** (HeyGen): set `width`/`height` for the orientation, optionally `inputs.background` + `settings.removeBackground` to replace the scene, `settings.fit` to resolve aspect mismatch, `settings.caption` to burn in subtitles.
5. **Run async and poll.** Submit `videoInference`, get a `taskUUID`, poll `getResponse` until terminal. Read the result from `videoURL`.

## Technique

- **The face and the voice are independent.** Pick the avatar/portrait and the voice separately. Lip sync adapts to whatever face you pair the audio with. A masculine voice on a feminine avatar will sync correctly but reads as a jarring mismatch, so pair them deliberately.
- **TTS path for iterating on copy.** Two requests with different `speech.text` give two videos in minutes, and `speech.language` localizes the same voice across locales (BCP 47 codes like `en-US`, `es-ES`). This is the cheapest way to A/B copy or fan a script out across languages. Translate, don't transliterate. The language code alone won't fix awkward source copy.
- **Audio path for brand voices.** When you already have the exact delivery (a recording, a voice clone, a separate TTS pass), feed it as `inputs.audio` and let the lip sync wrap it. You give up the TTS tuning knobs on this path, so shape the voice upstream instead.
- **Lock the avatar and voice before iterating.** Both are visible-in-the-output decisions. Test the pairing on a short 10-second script first, then send the full read once it feels right.
- **Background and framing are where it reads as production.** Most of the polish lives around the speaker, not in the face. `settings.removeBackground` only matters paired with a replacement (`settings.backgroundColor` hex, or an image in `inputs.background`). Alone it falls back to the source environment. Match the background image's aspect to the output canvas to avoid crop or letterbox.
- **Pick orientation before the look.** A wide-framed avatar forced into a 9:16 canvas needs `fit: cover` and still looks awkward. For mobile-first output, choose a look that frames vertically. `cover` fills and crops, `contain` letterboxes, and omitting `fit` lets the server choose.

Fill this in before building the request:

```
Drive mode (pick ONE):
  [ ] TTS    -> speech.text = "<script>", speech.voice = "<voice ID>"  (no inputs.audio)
  [ ] Audio  -> inputs.audio = "<URL or UUID>"                          (no speech block)
Face: avatar = "<catalog ID>"  | portrait = "<image>"  | lip-sync source video = "<video>"
Orientation + resolution: <16:9 or 9:16> @ <720p / 1080p / 4K>
Background: <none / backgroundColor #hex / inputs.background image>  (+ removeBackground if replacing)
Fit: <cover / contain / omit>   Captions: <on / off>
```

For full worked requests covering each drive path, load `references/examples.md`.

## Parameters that matter

- **One of `speech` or `inputs.audio`, never both.** `speech.text` + `speech.voice` are required together on the TTS path.
- `speech.speed` (HeyGen `0.5` to `1.5`, default `1.0`), `speech.pitch` (`-50` to `+50`, default `0`, keep adjustments small), `speech.volume` (`0.0` to `1.0`). TTS-path only.
- `speech.language`: a BCP 47 locale that adapts the voice's pronunciation to the target language.
- `inputs.image` (portrait), `inputs.avatar` (catalog ID, validated against an enum on avatar models), `inputs.video` / `inputs.referenceVideos` (lip-sync source), `inputs.audio` (URL or UUID).
- `width`/`height`: HeyGen outputs fixed 16:9 or 9:16 resolutions (720p / 1080p / 4K). 1080p is the production default, 720p for previews.
- `settings.removeBackground`, `settings.backgroundColor`, `inputs.background`, `settings.fit` (`cover`/`contain`), `settings.caption`: HeyGen composition controls. Burned-in captions are permanent and use a fixed style.
- Confirm exact field names and ranges against the live schema (`runware-run`). They vary across these models. Never guess.

## Quality bar

- Lip sync tracks the audio cleanly, with no drift or mouth artifacts across the clip.
- Exactly one drive mode was sent (script or audio), so the request validated.
- Orientation and resolution match the destination platform, and `fit` resolves any aspect mismatch without ugly letterboxing.
- If a background was replaced, `removeBackground` ran with a real replacement and the background aspect matches the canvas.
- No fabricated endorsements or on-screen claims. Only use copy the user supplied.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `voiceover` (generate or clone the audio you feed in), `ugc-ad` (wrap the talking head into a full ad), `character-consistency` (keep the same presenter across videos).
