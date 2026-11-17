---
name: socialkit-youtube-script
description: Writes or revises a YouTube video script (long-form or Shorts) with a hook, structured sections, on-screen cues and a call to action, saved as script.md in the project folder. Use when the user asks for a YouTube script, outline, voiceover text or rewrite of a video draft.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: youtube
  requires: socialkit-social-core
---

# YouTube script

Apply socialkit-social-core voice rules. Use [the template](assets/script-template.md) and the
[structure guide](references/structure.md).

## Steps

1. Confirm: audience, promise of the video (one sentence), target length, format
   (long-form or Short), and source material. Read `research.md` if it exists.
2. Draft `script.md` from the template. Narration at roughly 150 words per minute; state
   the word count and estimated duration at the top.
3. Mark every factual claim that needs a source with `[source: ...]`. Use only sources
   the user provided or that appear in `research.md`. If a claim has no source, flag it
   instead of inventing one.
4. Mark visual cues in the script with `[VISUAL: ...]` so socialkit-youtube-visuals can build the
   shot list.
5. Present the draft and list open questions. Revise on feedback.

This skill ends at a draft. The script approval checkpoint belongs to socialkit-youtube-pipeline.

## Output contract

`script.md` with: title idea, promise, word count, estimated duration, hook, sections
with narration and visual cues, call to action, and a sources list.

## Failure handling

- Missing audience or promise: ask before drafting.
- Script would exceed the target length by more than 15%: say so and propose cuts.
