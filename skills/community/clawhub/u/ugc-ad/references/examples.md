# UGC ad worked recipes

Three end-to-end recipes for the `ugc-ad` outcome. Each gives the scenario, the real async request, and the result shape. Adapt the values, then confirm field names and ranges against the live schema (`runware-run`) before sending.

All three use HeyGen Avatar V (`heygen:avatar@5`). Confirm it is `live` via `runware-models` first. The `inputs.avatar` and `speech.voice` strings are catalog IDs validated against an enum at request time, so resolve the current catalog rather than copying these verbatim. Every request runs `taskType: "videoInference"`, returns a `taskUUID`, and is polled with `getResponse` until terminal. Read `videoURL` from the result.

Never put a claim, testimonial, metric, or review on screen unless the user supplied the exact wording. The scripts below are placeholders for real, user-supplied copy.

## Recipe 1: Testimonial talking-head from a script (TTS path)

**Scenario.** A 16:9 testimonial-style spot for web and YouTube. The user has a written script and no recorded audio, so the model speaks the script. One presenter, plain branded background, captions off because the player carries its own.

**Request.**

```json
{
  "taskType": "videoInference",
  "taskUUID": "11111111-1111-1111-1111-111111111111",
  "model": "heygen:avatar@5",
  "inputs": {
    "avatar": "woman_business_office"
  },
  "speech": {
    "text": "I kept missing invoices until I started using this. Now every receipt files itself the second it lands in my inbox, and my month-end close takes an afternoon instead of a weekend. If you run a small shop, start the free trial today.",
    "voice": "jenny_female_english",
    "speed": 1.05
  },
  "width": 1920,
  "height": 1080,
  "settings": {
    "removeBackground": true,
    "backgroundColor": "#f5f0e6"
  }
}
```

**Notes.** TTS path means `speech` is present and `inputs.audio` is absent. `speed: 1.05` keeps the read brisk for a social-leaning testimonial. `removeBackground` runs with a replacement (`backgroundColor`), never alone. To localize, hold the avatar and voice fixed, translate `speech.text`, and add a `speech.language` BCP 47 code (`es-ES`, `fr-FR`).

**Result.** Poll `getResponse` until terminal, then read `videoURL`. A 1920x1080 MP4 of the presenter speaking the script over the cream background.

## Recipe 2: Product demo driven by the creator's own audio (lip-sync path)

**Scenario.** The creator recorded their own voice delivering the demo and wants that exact performance preserved. Drive the avatar with the audio file. No `speech` block.

**Request.**

```json
{
  "taskType": "videoInference",
  "taskUUID": "22222222-2222-2222-2222-222222222222",
  "model": "heygen:avatar@5",
  "inputs": {
    "avatar": "man_casual_young_adult",
    "audio": "https://im.runware.ai/uploads/creator-demo-vo.mp3",
    "background": "https://im.runware.ai/uploads/kitchen-counter-16x9.jpg"
  },
  "width": 1920,
  "height": 1080,
  "settings": {
    "removeBackground": true
  }
}
```

**Notes.** Lip-sync path means `inputs.audio` is present and `speech` is omitted entirely. Sending both errors. The audio is a public URL or an uploaded-asset UUID. Upload the recording and the background image first, then reference them. Voice tuning (`speed`, `pitch`, `volume`, `language`) does not exist on this path, so shape the delivery upstream in the recording. Match the background image's aspect ratio to the output canvas (16:9 here) so it is not cropped or letterboxed. The same path accepts a voice clone or a track from a separate `voiceover` run.

**Result.** Poll `getResponse`, then read `videoURL`. A 1920x1080 MP4 of the presenter, matted onto the kitchen-counter scene, mouth synced to the supplied recording.

## Recipe 3: 9:16 social cut with burned-in captions (TTS path)

**Scenario.** A vertical cut for TikTok, Reels, and Shorts. Silent autoplay is the norm, so burn captions in. Portrait orientation needs `fit: cover`.

**Request.**

```json
{
  "taskType": "videoInference",
  "taskUUID": "33333333-3333-3333-3333-333333333333",
  "model": "heygen:avatar@5",
  "inputs": {
    "avatar": "casual_sitting_young_adult"
  },
  "speech": {
    "text": "Stop scrolling. This is the bottle that finally got me to drink enough water. It tells you when to sip, it keeps cold for a full day, and it fits every cup holder I own. Tap the link to grab yours.",
    "voice": "chill_brian_male_english",
    "speed": 1.1
  },
  "width": 1080,
  "height": 1920,
  "settings": {
    "removeBackground": true,
    "backgroundColor": "#0a0e27",
    "fit": "cover",
    "caption": true
  }
}
```

**Notes.** `width: 1080`, `height: 1920` is portrait 1080p. `fit: cover` crops the landscape source to fill the tall frame, which is almost always right for portrait. `contain` would letterbox and rarely looks production-ready. `caption: true` burns subtitles in with a fixed style. If the user needs custom caption typography, render with `caption: false` and overlay subtitles in post. The hook ("Stop scrolling") lands in the first two seconds.

**Result.** Poll `getResponse`, then read `videoURL`. A 1080x1920 MP4 with the presenter cropped to fill the vertical frame and captions burned in.
