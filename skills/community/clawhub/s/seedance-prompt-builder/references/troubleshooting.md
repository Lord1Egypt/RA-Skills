# Troubleshooting

Use this file to diagnose and repair Seedance prompts.

## Character id drift

Symptoms: the character does not match the reference image or changes face mid-video.

Likely causes:

- mixed reference collage where the face is too small;
- face, body pose, costume, and detail references are merged into one image;
- important face reference appears too late in the prompt.

Fixes:

- Ask for or recommend a separate face close-up plus one full-body or costume reference.
- Define the face reference first and give it high priority.
- Write subject definitions clearly and reuse the label.
- Do not use multi-view character sheets as the default; they can be interpreted as multiple subjects.

## Unwanted subtitles or text

Fixes:

- Add explicit no-subtitle and no-text constraints in Chinese.
- If reference media contains unwanted text, recommend removing it before use.
- When allowed, prefer landscape generation first, then crop to vertical if needed.

## Unwanted logo or watermark

Fix:

- Add explicit no-logo and no-watermark constraints in Chinese.

## Style drift

Symptoms: expected 2d or 3d animation becomes live-action or another style.

Fixes:

- Add a direct style lock at the end of the prompt.
- If style control must be strict, recommend transforming references into the target style before video generation.

## Extension jump or regression

Symptoms: a video extension jumps, rewinds, or visibly changes at the splice point.

Fixes:

- Prefer ending an extension prompt at a cut or transition moment.
- For post-production, trim the last 6 frames of the previous clip and the first 1 frame of the following clip at each join, then check smoothness.

## Twin or duplicate character problem

Symptoms: duplicated same-looking character appears in the same frame.

Fixes:

- Define every character and reference image clearly.
- Add a global constraint that the video must not include duplicated identical-looking people or twin effects.
- Use single-person independent reference images instead of three-view or multi-view sheets.
- Simplify long script text into focused instructions.

## Quality degradation after repeated extension

Fixes:

- Avoid too many generations of extension on model-produced clips.
- Use high-definition still references when possible.
- For severe degradation, recommend converting the source to a stable white 3d model video first, then extending from it.

## Special effect does not match expected logic

Fix:

- Use a reference video for the effect shape and motion logic. Text-only effect descriptions are weaker for precise effects such as countdowns, particle paths, wing generation, or UI animation.

## Too many referenced people

If more than four referenced people are needed, recommend grouping characters into generated images first, then use those images to generate the final video. This reduces missing people, extra people, and duplicates.

## Ending audio noise

Fixes:

- Regenerate, or use editing software to fade out the ending audio with a volume envelope.

## Chinese pronunciation issues

Fix:

- Replace rare, polyphonic, or visually similar characters with common homophones if acceptable.

## Voice reference mismatch

Fixes:

- Add explicit timbre descriptors in the prompt.
- Keep dialogue style close to the reference audio style, tone, and expression.
