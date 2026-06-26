# Task routing

Use this file to choose the correct Seedance task family before generating a prompt.

## Multimodal reference

Use when the user wants to extract a subject, style, scene, motion, camera language, special effect, sound, or voice from assets and create a new video.

Recommended patterns:

- Image reference: reference `imageN` for `[subject or visual element]`, then generate `[new scene]`.
- Video reference: reference `videoN` for `[motion, camera, style, sound, or effect]`, then generate `[new scene]`.
- Audio reference: reference `audioN` for voice timbre or sound mood, then generate `[dialogue or scene]`.

## Video editing

Use when the user wants to alter an existing video locally or globally. Unmentioned content should remain unchanged.

Patterns:

- Add element: describe the element features, appearance timing, and position.
- Modify element: strictly edit `videoN`, change `[original feature]` to `[new feature]`.
- Delete element: specify the element to remove and emphasize what must stay unchanged.

Important: do not say "reference videoN" for the source being edited. Say "strictly edit videoN" or directly use "in videoN".

## Video extension

Use when the user wants to continue a video forward or backward in time.

Patterns:

- Forward extension: extend `videoN` forward, generating `[continued action or story]`.
- Backward extension: extend `videoN` backward, generating `[setup action or prior dialogue]`.
- Preserve audiovisual continuity: subject identity, scene, lighting, style, and audio should remain consistent.

Important: do not say "reference videoN" for the video being extended.

## Track completion

Use when bridging two or three video clips with generated transitions.

Pattern:

```text
`video1`, [transition description], then connect to `video2`, [transition description], then connect to `video3`.
```

The official guide notes that Seedance 2.0 supports up to 3 video inputs for this task, with total input duration up to 15 seconds.

## Combined task

Use when referencing one asset while editing another.

Pattern:

```text
reference `imageN` or `videoN` for [reference dimension], strictly edit `videoX`, [specific edit].
```

## Ask or proceed

Ask a brief question only when the missing information changes task routing or subject identity. Otherwise, make a sensible default and return a prompt plus a short "assumptions" note.
