# Prompting Seedance 2.5

Describe visible subjects, actions, camera movement, setting, and required continuity. For staged action, use a small number of integer-second intervals compatible with the requested duration. Time descriptions guide generation; they are not frame-accurate editing controls.

A single movement needs no artificial segmentation. Example for five seconds: from 0–2 seconds steam rises from a blue cup; from 2–5 seconds the camera slowly pulls back. State unwanted speech or captions when their absence matters, and set the actual audio option appropriately.

Reference names must correspond to the real ordered input arrays. A written “first frame” instruction is not a substitute for the first-frame field. Preserve the user's creative wording where possible and avoid adding unrelated action.

Use [reference roles](reference-generation.md), [frame modes](frames-and-storyboards.md), and [API parameters](../../api/seedance.md) as needed.
