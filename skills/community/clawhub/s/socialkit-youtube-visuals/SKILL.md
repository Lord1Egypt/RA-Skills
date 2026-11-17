---
name: socialkit-youtube-visuals
description: Turns an approved YouTube script into a shot list (shot-list.json) that maps each script section to a visual asset - user footage, screen recordings, slides, images or licensed stock - with durations, plus an asset checklist. Use when planning B-roll, visuals, scenes or slides for a YouTube video.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: youtube
  requires: socialkit-social-core
---

# YouTube visuals

Plans visuals; it does not generate or download media. Every asset comes from the user
or from a source the user has rights to use.

## Steps

1. Read the approved `script.md` and its `[VISUAL: ...]` cues.
2. For each section propose one or more segments: what to show, the asset type
   (footage, screen recording, slide, image, licensed stock) and a duration that covers
   the narration at about 150 words per minute.
3. Write `shot-list.json` in the project folder following
   [the schema](assets/shot-list.schema.json). Use paths under `assets/`; it is fine for
   files not to exist yet.
4. Give the user an asset checklist: file name, what it should show, where it could come
   from, and licence notes. Ask them to place files in `assets/` and record the
   voiceover as `assets/voiceover.mp3` (or update the path).
5. Ask whether any asset is realistic AI-generated or altered media. If yes, note it so
   the upload step sets the synthetic media disclosure.

## Output contract

`shot-list.json` valid against the schema, and an asset checklist in the reply.

## Failure handling

- No script: ask for it or follow socialkit-youtube-script first.
- User has no rights to an asset: replace it; never suggest pulling clips from other
  creators' videos.
