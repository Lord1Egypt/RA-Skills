---
name: replace-in-video
description: >
  Swap one on-camera element in an existing video while everything else stays put. Use when the
  user says "recast this character", "put a different actor in this clip", "swap the product she's
  holding", "change the shirt he's wearing", "change the car's color", "repaint the jacket", "drop
  my mascot into this scene", or "replace X but keep the rest". Keeps the original motion, timing,
  camera, lighting, and audio untouched. For a whole-frame restyle or relight, use edit-video
  instead.
---

# Replace in video

Swap a single on-camera element in a source video (a character, a product, a garment) for one from a reference image, while the motion, timing, camera movement, lighting, audio, and background all carry through unchanged. The lever is a source video plus one to three reference images, and a prompt that names exactly what to **replace** and what to **preserve**. This is not re-shooting or re-prompting the scene, it is a targeted swap that leaves everything else frame-faithful.

## Inputs to collect

- **The source video.** The clip whose scene, motion, and audio you want to keep. Bring footage you have rights to (see Technique). (Ask only if none provided.)
- **The reference image(s).** What the new element should look like: a clean portrait for a character recast, a bare product/garment photo for an object swap. One is enough, up to three.
- **What to replace and what to keep.** The specific on-camera element being swapped, and whether anything ambiguous nearby (a second character, a held object) must stay.
- Optional: target resolution (720p draft vs 1080p finish), and whether the source audio should play, drive lip sync, or be stripped.

## Models

- **Default: Pruna P-Video-Replace** (`prunaai:p-video@replace`). The model for swapping one on-camera element in a clip while preserving the rest. Takes the source under `inputs.video` and up to **3** images under `inputs.referenceImages`. Capability `io:video-to-video` + `op:edit`.
- **Reversed direction:** if you want the *image* to be the scene and the video to only lend its motion, that is P-Video-Animate (`prunaai:p-video@animate`), not this. Replace keeps the video's world, Animate keeps the image's.
- **To generate the source first** (an iconic shot, a UGC pitch) before recasting it, route the generation to a flagship image-to-video model via `product-ad-video`, then run replace on the result.
- Confirm the model is `live` and inspect its exact input fields via `runware-models` + `runware-run` before calling. Never hardcode a stale choice.

## Workflow

1. Resolve the schema (`runware-run`) and confirm the input fields (`inputs.video`, `inputs.referenceImages`), the `resolution` and `fps` options, and that the task is `videoInference`.
2. Upload the source video and the reference image(s) as URLs or base64 into `inputs.video` and `inputs.referenceImages`.
3. Run `videoInference` **asynchronously** (`deliveryMethod: async`). The call returns a `taskUUID`. Poll `getResponse` until terminal, then read `videoURL`. Video is never a blocked sync call.
4. For a localised swap (product, garment, or one character among several), add a `positivePrompt` that names the element to replace and lists everything to preserve. For a clean single-character recast, the prompt is optional.
5. Review the output for identity/object fidelity and for unwanted changes elsewhere in the frame. Retry drifters with a clearer reference or a tighter preserve list.

See `references/examples.md` for three worked async `videoInference` recipes (recast a character, swap a product or garment, drop a subject into a generated scene) with the real request and `videoURL` result shape.

## Technique

- **Name what to replace and what to preserve.** This is the load-bearing pattern. The reference image carries *what the new element should look like*, the `positivePrompt` carries *what gets swapped for it and what stays*. The closing direction "Only the X should change, everything else stays as the source" is what turns a global appearance match into a localised swap. Be specific about the target: "replace the matte-black earbuds case she's holding" works, "replace the product" is too vague and drifts between runs. Template: `Replace [specific source element] with [the X] from the reference image. Preserve [list everything that stays] exactly as they appear in the source. Only [the named element] should change, everything else stays as the source.`
- **Character recast: clean portrait in, identity out.** For a character swap the reference only needs the face, hair, build, and identity. The source carries the costume, the lighting, the setting, and the action, so do not dress the reference to match the scene. A clearly visible front or three-quarter face is the safest reference. For a single-character clip with no ambiguity, no prompt is needed.
- **Object swap: bare product/garment photo in.** For a product or wardrobe swap the reference should be a clean photograph of the target object alone, no person or hands, plain neutral background. Match the reference framing to how the source presents the element (a vertical held product pairs with a vertical product shot, a torso-on garment pairs with a front-facing flat-lay).
- **Three references hold identity through head turns.** `referenceImages` accepts up to 3. Sending a front plus three-quarter left and right tightens a character recast when the source head turns away from camera. The single front reference is enough for static or near-static shots.
- **One reference per element for multi-swaps.** When the source has two on-camera characters, or you want to swap a garment and a product in one call, send one reference per target and index each in the prompt ("reference image 1", "reference image 2"), mapping each to its position or its element. Without a prompt the model auto-assigns by visual cues, which works when the references are visually distinct.
- **Rights and likeness are the caller's responsibility.** Replace does not care whether the source was generated, recorded, or licensed, and it will recast a real person's likeness. Bring source footage and reference images you have the rights to. Do not recast a real, identifiable person without their consent.

## Parameters that matter

- `taskType: videoInference` and `deliveryMethod: async`. Always polled, never a blocked sync call.
- `inputs.video` is the source clip. `inputs.referenceImages` takes up to **3** images. Confirm the exact field names against the live schema, never guess.
- `positivePrompt` is optional. Required for localised object/garment swaps and for multi-character disambiguation. Names the replace target and the preserve list.
- `resolution` is `720p` or `1080p`. Output inherits the source's aspect ratio, so this is the only sizing call. 1080p roughly doubles the per-second cost. Draft a variant batch at 720p, re-run only approved variants at 1080p.
- `fps` accepts `24` or `48` only. Omit it to inherit the source's native frame rate, which is what most workflows want.
- `settings.preserveAudio` (default `true`) controls whether the source audio is in the output at all. Set `false` for a silent output you intend to re-dub.
- `settings.sourceAudioSync` (default `true`) controls whether the source audio drives the character's lip and motion sync. Set `false` when the audio is incidental (room tone, music) and should not pull the face around.
- `seed`: fix it to hold a take while iterating, vary it for alternates.

## Quality bar

- Only the named element changed. The actor (or the rest of the cast), the motion, timing, camera, lighting, background, and audio of the source are intact.
- Identity or object fidelity reads true: a recast character is recognizably the reference, a swapped product matches its shape, color, and material.
- Audio and face align where it matters. Source audio is preserved by default, so a male reference into a female-voiced source yields a mismatched voice unless you gender-match or strip the audio.
- Watch the failure modes: extreme camera motion or back-of-head framing with no face anchor makes the model improvise a new scene, and tiny details (a logo, small print, a jersey number) may drift. For pixel-perfect detail preservation, use an inpainting model with a mask instead. Retry anything that improvised or drifted.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `edit-video` (general video editing/restyle of a whole clip), `product-ad-video` (generate the source spot, or swap a product into shot footage).
