# Talking avatar worked recipes

Three end-to-end recipes for the `talking-avatar` outcome: a script-driven talking head (TTS path), an audio-driven one (lip-sync path), and a lip-sync onto existing footage (sync model). Each gives the scenario, the real async request, the drive path, the framing and background choices, a poll note, and the result shape. Adapt the values, then confirm field names and ranges against the live schema (`runware-run`) before sending.

Confirm every model is `live` via `runware-models` first. On HeyGen, `inputs.avatar` and `speech.voice` are catalog IDs validated against an enum at request time, so resolve the current catalog rather than copying these verbatim. Every request runs `taskType: "videoInference"`, returns a `taskUUID`, and is polled with `getResponse` until terminal. Read `videoURL` from the result.

Pick exactly one drive mode per request. TTS path sets a `speech` block and omits `inputs.audio`. Lip-sync path sets `inputs.audio` and omits `speech`. Sending both errors.

## Recipe 1: Script-driven talking head (TTS path)

**Scenario.** A 16:9 explainer for web and YouTube. The user has a written script and no recorded audio, so the model speaks it. One registered avatar, branded image background, captions off because the player carries its own.

**Drive path.** TTS. `speech.text` plus `speech.voice` present, no `inputs.audio`.

**Request.**

```json
{
  "taskType": "videoInference",
  "taskUUID": "11111111-1111-1111-1111-111111111111",
  "model": "heygen:avatar@5",
  "inputs": {
    "avatar": "Brandon_Office_Standing_Front_public",
    "background": "https://im.runware.ai/uploads/office-16x9.jpg"
  },
  "speech": {
    "text": "Setting up your workspace takes about two minutes. Connect your inbox, pick a folder, and every receipt files itself from there.",
    "voice": "chill_brian_male_english",
    "speed": 1.0
  },
  "width": 1920,
  "height": 1080,
  "settings": {
    "removeBackground": true
  }
}
```

**Notes.** TTS path means `speech` is present and `inputs.audio` is absent. `inputs.avatar` is required on every HeyGen request, including audio-path ones. `removeBackground` runs with a replacement (the `inputs.background` image), never alone, otherwise it falls back to the avatar's source environment. Match the background image aspect to the canvas (16:9 here) so it is not cropped or letterboxed. `width`/`height` and `resolution` are mutually exclusive, so send one pair, not both. To localize, hold the avatar and voice fixed, translate `speech.text`, and add a `speech.language` BCP 47 code (`es-ES`, `fr-FR`). Voice tuning (`speed` `0.5` to `1.5`, `pitch` `-50` to `+50`, `volume` `0.0` to `1.0`) exists only on this path.

**Result.** Poll `getResponse` until terminal, then read `videoURL`. A 1920x1080 MP4 of the avatar speaking the script, matted onto the office background.

## Recipe 2: Audio-driven talking head (lip-sync path)

**Scenario.** The user already has the exact delivery they want, a recording or a `voiceover` run, and wants it preserved. Drive the avatar with the audio file. No `speech` block. Solid-color background for downstream compositing.

**Drive path.** Lip-sync. `inputs.audio` present, `speech` omitted entirely.

**Request.**

```json
{
  "taskType": "videoInference",
  "taskUUID": "22222222-2222-2222-2222-222222222222",
  "model": "heygen:avatar@5",
  "inputs": {
    "avatar": "man_casual_young_adult",
    "audio": "https://im.runware.ai/uploads/brand-vo.mp3"
  },
  "width": 1920,
  "height": 1080,
  "settings": {
    "removeBackground": true,
    "backgroundColor": "#0a0e27"
  }
}
```

**Notes.** Lip-sync path means `inputs.audio` is present and `speech` is omitted. Sending both errors. The audio is a public URL or an uploaded-asset UUID, so upload the recording first, then reference it. The model extracts phonemes from the audio and animates the mouth to match. Voice tuning (`speed`, `pitch`, `volume`, `language`) does not exist on this path, so shape the delivery upstream in whatever produced the audio. The same path accepts a voice clone or a track from a separate `voiceover` run. A solid `backgroundColor` suits chroma-key style compositing or a fixed brand plate, again paired with `removeBackground`.

**Result.** Poll `getResponse` until terminal, then read `videoURL`. A 1920x1080 MP4 of the avatar, matted onto the dark navy plate, mouth synced to the supplied recording.

## Recipe 3: Lip-sync onto existing footage (sync model)

**Scenario.** The user has footage of a real person already on camera and wants to re-voice it. There is no avatar to generate, only a face already in a video. Drive the sync model with the source video plus the new voice. Send the new voice either as audio (preserve a recording) or as a script (let the model generate the TTS). This recipe shows the audio variant.

**Drive path.** Lip-sync onto video. `inputs.video` is the source footage, `inputs.audio` is the new voice. For the script variant, drop `inputs.audio` and add a `speech` block with `text` and `voice` instead. Exactly one of those two, never both.

**Request.**

```json
{
  "taskType": "videoInference",
  "taskUUID": "33333333-3333-3333-3333-333333333333",
  "model": "sync:3@0",
  "inputs": {
    "video": "https://im.runware.ai/uploads/source-presenter.mp4",
    "audio": "https://im.runware.ai/uploads/new-voiceover.mp3"
  }
}
```

**Notes.** sync-3 re-voices a person already on camera, so it takes `inputs.video` (required) rather than an avatar, and has no HeyGen background or framing controls. The output keeps the source video's resolution and scene, including the original background, so there is no `width`/`height` or `removeBackground` here. `inputs.audio` and a `speech` block are mutually exclusive on this model too, same rule as HeyGen. For the script variant, swap `audio` for `speech: { "text": "...", "voice": "..." }`. sync-3 handles obstruction and full-scene lip sync. For higher-resolution editing up to 4K, swap the model to `sync:lipsync-2-pro@1` and confirm its field names against the live schema, as they differ.

**Result.** Poll `getResponse` until terminal, then read `videoURL`. An MP4 at the source video's resolution, the on-camera person's mouth re-synced to the new voice, the rest of the scene unchanged.
