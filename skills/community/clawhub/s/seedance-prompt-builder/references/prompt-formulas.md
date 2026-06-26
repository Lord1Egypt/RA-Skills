# Prompt formulas

## Basic formula

For quick use, choose the task formula from `task-routing.md` and write a concise prompt with clear asset references.

## Advanced formula

Build prompts in this order:

```text
precise subject + action details + scene environment + lighting and color + camera movement + visual style + quality + constraints
```

The intent is to give Seedance spatial information and temporal information separately and clearly.

## Subject definition

For any scene with multiple people, multiple assets, or reused characters, define subjects before the action.

Patterns:

```text
define the person in image1 with [2-3 stable traits] as [label].
define the person in image2 with [2-3 stable traits] as [label].
```

Rules:

- Use 2-3 stable visual traits such as clothing, hairstyle, category, face reference, or accessory.
- Keep using the same label after definition.
- For a simple unregistered subject, use a bound form such as `[subject]@image1` in every mention.
- If the user uses asset ids, still refer to imageN or videoN because the model does not directly map asset ids to visual content.
- Avoid redundant or contradictory subject descriptions.
- Prefer reference images for complex spatial relationships instead of long text descriptions.

## Storyboard sequence

Use `shot 1`, `shot 2`, `shot 3` for complex scenes. Do not default to exact time ranges such as 0-3 seconds; exact time constraints may destabilize results.

Each shot should include:

1. camera or transition method;
2. subject action and expression;
3. position or scene change;
4. audio, speech, or sound effects if relevant.

## Motion and emotion

Use visible action details instead of abstract emotion labels.

- Sadness: lowered head, slightly trembling shoulders, fingers gripping clothing, red eyes, tears held back.
- Joy: rising mouth corners, relaxed brows and eyes, lighter steps, humming, small spin.
- Tension: frequent watch checking, fingers tapping, quick breathing, evasive gaze.
- Anger: clenched fists, tight jaw, heaving chest, sharp gaze, strained voice.
- Relief: long exhale, relaxed shoulders, faint smile, looking into the distance.

Action details should name body parts and degree: slowly raises hand, quickly turns head, forcefully pushes off the ground, slightly lowers head.

Prefer slow, gentle, continuous small movements when stability matters. Avoid highly explosive movement unless the user needs it.

## Camera movement

Use standard camera language directly. One shot should usually contain only one primary camera movement.

Good examples:

- medium shot, smooth follow shot;
- wide shot slowly pushing in;
- fixed camera;
- cut to close-up;
- smooth lateral tracking.

Avoid stacking multiple movements such as push, pull, pan, orbit, handheld shake, and aerial dive in one shot.

## Quality, style, and constraints

Always add quality and constraints matched to the use case.

General quality:

```text
high definition, rich details, cinematic texture, natural color, soft lighting, stable subject identity, smooth natural motion, no flicker, no stutter, no deformation.
```

When no text is desired, add Chinese no-text constraints. Use the official guide wording from `official-guide.md` if exact Chinese wording is needed.

For style control, state the target style explicitly, especially when visual references and desired style conflict. Example: keep 3d guofeng cg xianxia style throughout; avoid drifting into live-action realism.

## Text, speech, sound, and symbols

Use symbol conventions from the official guide:

- Music: parentheses, for example `(fast rock music plays in the background)`.
- Sound effect: angle brackets, for example `<dog barking in the distance>`.
- Dialogue: braces, for example `{hello, world}`.
- On-screen title or subtitle text: square brackets in Chinese-style usage if the final prompt is Chinese.

When generating subtitles, specify appearance position, content, timing or synchronization, and style if strict control is needed.

For speech in a non-Chinese or non-English language, name the language before the dialogue.

For Chinese pronunciation issues, replace rare or ambiguous characters with common homophones when acceptable.
