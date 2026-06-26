# Text-to-Sound-Effect Prompt Guide

## Goal

Write concise, concrete prompts that describe one coherent sound event or ambience.

## Formula

`Sound Source + Action/Context + Acoustic Characteristics`

## Good Prompt Patterns

- Source: what makes the sound
- Context: where or under what condition
- Characteristics: loudness, texture, rhythm, distance, reverb

Examples:

- `Heavy rain hitting a metal roof, steady rhythm, distant thunder`
- `Glass bottle shattering on concrete, sharp and bright transient`
- `Busy office ambience with keyboard typing and quiet chatter`
- `Retro game UI confirmation beep, short and clean`
- `Wooden door creaking open in an empty hallway, long reverb`

## Do

- Keep one primary sound scene per request.
- Include intensity and environment cues.
- Specify if you want short event vs continuous ambience.

## Avoid

- Multiple unrelated scenes in one prompt.
- Contradictory adjectives (for example: `very soft and extremely loud`).
- Overly abstract instructions with no physical source.

## Iteration Strategy

1. Start with a short prompt.
2. If output is too generic, add source detail.
3. If output is too busy, remove secondary sounds.
4. Tune duration for intended usage (UI, transition, ambience loop).

## Duration Guidance

- `5-10s`: UI or single events
- `10-30s`: transitions and short scenes
- `30-180s`: ambience beds and environmental loops
