# Replace in video: worked recipes

Three end-to-end recipes. Each shows the scenario, the async `videoInference` request, a poll note, and the result shape. Confirm the AIR is `live` and the field names against the live schema before sending. Run async (`deliveryMethod: async`): the immediate response is an acknowledgment, then poll `getResponse` until terminal. The finished clip is at `videoURL`.

All AIRs below are verified `live` against the Runware catalog: `prunaai:p-video@replace` (Pruna P-Video-Replace), `bytedance:seedance@2.0` (Bytedance Seedance 2.0, used only to generate a source in recipe 3).

The load-bearing pattern is the **replace/preserve** naming in `positivePrompt`. The reference image carries what the new element looks like. The prompt carries what gets swapped for it and what stays. Name the specific source element to replace, list everything to preserve, and close with "Only the X should change, everything else stays as the source."

**Rights and likeness are the caller's responsibility.** Replace will recast a real person's likeness. Bring source footage and reference images you have the rights to, and do not recast a real, identifiable person without their consent.

## 1. Recast a character (single character, no prompt needed)

Scenario: a podcast-style talking-head clip exists, and the client wants the same delivery on a different on-camera person. One character, face visible to camera, no held object or second person to disambiguate. The reference carries identity (face, hair, build), the source carries the costume, lighting, scene, motion, and audio.

The reference is a clean chest-up portrait with the face clearly visible. Do not dress it to match the scene. For a clean single-character swap the `positivePrompt` is optional, so leave it out. The source audio is preserved verbatim by default, so match the reference's gender to the source's voice when face and voice alignment matters.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "model": "prunaai:p-video@replace",
    "deliveryMethod": "async",
    "inputs": {
      "video": "https://example.com/source-podcast.mp4",
      "referenceImages": ["https://example.com/ref-jordan-front.jpg"]
    },
    "resolution": "720p"
  }
]
```

Poll note: the request returns a `taskUUID` and acknowledges. Poll `getResponse` (or use a webhook) until the task is terminal, then read `videoURL`.

Result:

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "videoUUID": "f1e2d3c4-b5a6-7890-1234-567890abcdef",
    "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/f1e2d3c4-b5a6-7890-1234-567890abcdef.mp4",
    "seed": 837412938
  }
]
```

Why it works: a single character with the face visible gives the model a clean identity anchor, so auto-assignment lands without a prompt. Identity comes from the reference, everything else carries through from the source. To tighten identity through head turns, send up to 3 angles of the same character (front plus 3/4 left plus 3/4 right). If the reference style has minimal mouth detail (flat 2D, anime) and the output will be heard out loud, set `settings.sourceAudioSync: false` and re-sync lip motion in post.

## 2. Swap a product or garment (localised swap, prompt required)

Scenario: a creator pitches a matte-black earbuds case to camera, and the team wants the same recording presenting a different product without re-shooting. This is the localised-swap mode. Change one on-camera object and leave the creator, the room, the speech, and everything else frame-faithful.

The reference is a clean product photograph of the target object alone, no person or hands, plain neutral background. Match the reference framing to how the source presents the element (a vertical held product pairs with a vertical product shot, a torso-on garment pairs with a front-facing flat-lay). The `positivePrompt` is required here: it names the specific source element to replace and lists everything to preserve. "Replace the product" is too vague and drifts between runs, so name the exact object.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "b7e8d9c0-1a2b-3c4d-5e6f-708192a3b4c5",
    "model": "prunaai:p-video@replace",
    "deliveryMethod": "async",
    "inputs": {
      "video": "https://example.com/source-creator-pitch.mp4",
      "referenceImages": ["https://example.com/ref-product-tumbler.jpg"]
    },
    "positivePrompt": "Replace the matte-black earbuds case the woman is holding in the source video with the brushed-stainless-steel coffee tumbler from the reference image. Preserve the woman, her face, her hair, her olive-green t-shirt, her gestures, her speech, the studio, the lighting, the camera, and the audio exactly as they appear in the source. Only the object in her right hand should change, everything else stays as the source.",
    "resolution": "720p"
  }
]
```

Poll note: returns a `taskUUID`, then poll `getResponse` until terminal and read `videoURL`. Draft the variant batch at 720p, re-run only approved variants at 1080p (1080p roughly doubles the per-second cost).

Result:

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "b7e8d9c0-1a2b-3c4d-5e6f-708192a3b4c5",
    "videoUUID": "c1d2e3f4-a5b6-7890-cdef-1234567890ab",
    "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/c1d2e3f4-a5b6-7890-cdef-1234567890ab.mp4",
    "seed": 1042883771
  }
]
```

Why it works: the reference carries the object's shape, color, and material, the prompt scopes the swap to one named element, and the closing "only the object in her right hand should change" turns a global appearance match into a local one. To swap a garment and a product in one call, send one reference per element and index each in the prompt ("the t-shirt with reference image 1, the held object with reference image 2"). For pixel-perfect detail on small print, a logo, or a jersey number, use an inpainting model with a mask instead, since Replace matches the reference into the scene rather than pixel-for-pixel.

## 3. Drop a subject into a known scene (generate the source, then recast)

Scenario: a meme recreation where you drop a chosen character into a recognizable shot. Two steps. Generate the iconic shot composition with Bytedance Seedance 2.0, then recast the protagonist with Replace. The Seedance source determines the costume the role wears, so the reference only needs the face, hair, build, and identity.

Step A generates the source. Seedance is image-to-video or text-to-video, async like all video tasks, and returns its own `videoURL` to feed into step B.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f",
    "model": "bytedance:seedance@2.0",
    "deliveryMethod": "async",
    "positivePrompt": "An empty industrial loading area at sunrise outside a brick warehouse in a 1990s American crime film. A group of five men walk abreast in slow motion toward the camera across cracked asphalt, all in matching slim-fit black suits, white shirts, narrow black ties, and dark sunglasses. The man at the centre adjusts the bridge of his sunglasses with his index finger, the other four stare straight ahead. Steady slow backward tracking shot at chest height. Hard golden-hour side light from the left, long shadows. 35mm film grain, photorealistic. Cool surf-rock instrumental guitar, no spoken dialogue.",
    "width": 1280,
    "height": 720,
    "duration": 5
  }
]
```

Step B recasts the centre man with a single reference image. The source has five similar-looking figures, so the `positivePrompt` is a position-mapping prompt: name the target by its position and anchor ("the man in the centre, the one adjusting his sunglasses") and list the other four men plus the scene as preserved.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "d4c5b6a7-8e9f-0a1b-2c3d-4e5f60718293",
    "model": "prunaai:p-video@replace",
    "deliveryMethod": "async",
    "inputs": {
      "video": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/<seedance-output>.mp4",
      "referenceImages": ["https://example.com/ref-cast.jpg"]
    },
    "positivePrompt": "Replace the man in the centre of the group in the source video, the one adjusting his sunglasses, with the man from the reference image. Preserve the source video motion, audio, camera, lighting, and the other four men in the group exactly as they appear in the source.",
    "resolution": "720p"
  }
]
```

Poll note: both steps are async. Poll step A to terminal, read its `videoURL`, then feed that URL into step B's `inputs.video` and poll step B to terminal.

Result (step B):

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "d4c5b6a7-8e9f-0a1b-2c3d-4e5f60718293",
    "videoUUID": "ae78185a-4ca6-425e-aa85-1968de419142",
    "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/ae78185a-4ca6-425e-aa85-1968de419142.mp4",
    "seed": 558201476
  }
]
```

Why it works: the position-mapping prompt names the target by its anchor and lists every other on-camera character as preserved, so the model swaps only the centre man on a line of similar figures. The same source video file is reusable across many recasts (a real person, a stylized avatar, a brand mascot) at one replace run each. The source must show the target's face at least briefly. A whip pan or back-of-head-only framing leaves no anchor and the model improvises a new scene instead of recasting.
