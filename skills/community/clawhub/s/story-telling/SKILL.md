---
name: story-telling
description: >
  Generate a narration script (voiceover + shot list + per-clip visual
  prompts + music cues) for a personal travel-story video or essay, from a
  thought-flow master skill and the author's own photos. Use when the user
  wants "a script", "旁白脚本", a storytelling/故事化 script for a video, or
  asks to turn a personal travel story (e.g. the death-in-Mexico project) into
  a narrated video or essay. Output is Simplified Chinese first-person
  storytelling, engine-agnostic in voiceover and timing, engine-specific in
  clip prompts. Never runs automatically; acts only when the user asks for a
  script.
---

# Story-telling — narration script generation

Turn a thought-flow master skill plus the author's photos into a complete narration script. The script is the source document for `video-gen` and the skeleton for an essay.

## Inputs

- `master` — reference to a thought-flow master document, e.g. `death-thought-flow` (`ai-thoughts/docs/260817-death-thought-flow.md`). Required.
- `photos` — paths to 5+ of the author's own photos (e.g. `ai-thoughts/imgs/`). Required for a video target; optional for an essay.
- `target` — `video` (default) or `essay`. Optional.
- `duration` — target total length for a video (default: author's choice, typically 3–5 minutes). Optional.
- `mode` — `full` (default) or `trailer`. Trailer produces a short test cut: the author picks a subset of sections, target ≤ 60 s.

## Outputs

- A narration script in Markdown, written to a `YYMMDD-slug` file in the working directory (e.g. `ai-thoughts/docs/` for essays, or a working folder for videos). Format follows the template below.

## Procedure

1. **Load the master.** Read `master` in full. The master's content points and content sections are the fixed skeleton — never reorder, rephrase, or replace them.
2. **Verify facts.** Before any factual claim lands in the script, re-verify it with live web search (websearch / webfetch) and keep the source URL. Skip any claim that cannot be sourced.
3. **Build the section structure.** For a video, derive sections from the master's content points and lay out a timing budget across the total duration; allocate the supplied photos so every section has at least one (photo-light sections borrow from the pool where the master allows). In `trailer` mode, the author selects which sections to cover (the master's trailer defaults (if any, otherwise the author chooses); each chosen section becomes a distinct beat of ~15–20 s, chosen sections are never dropped or merged, photos may be reused across beats, and the soul line (as defined in the master's content points) lands in the trailer's opening or closing line.
4. **Write the voiceover.** Simplified Chinese, first-person storytelling tone, personal and warm, not official. Each section's voiceover advances the narrative and stays strictly inside the master's thought-flow and verified facts.
5. **Derive per-clip visual prompts.** For each photo, write an image-to-video prompt in the target engine's style (see Engine prompts): subject, setting, lighting, textures, camera movement, mood, cinematic documentary framing.
6. **Add music cues and timing.** Assign audio direction and timing per section so the whole script holds together rhythmically.
7. **Export.** Write the script in the template below and report the path. Do not start generating any video — that is `video-gen`'s job.

## Script template

```markdown
# <标题> — 旁白脚本 (narration script)

| Section | Time | Duration | Photos | Content |
|---------|------|----------|--------|---------|
| 1. <name> | 0:00-0:30 | 30s | n | <theme> |

## Section 1: <name> (0:00-0:30)

**Voiceover (简体中文):**
> "<voiceover line>"

**Photo Reference:** <path>

| Clip | Duration | Visual prompt | Audio |
|------|----------|---------------|-------|
| 1.1 | 8s | <engine prompt> | <music / ambience cue> |
```

The clip grid is per section, one row per image-to-video clip. Voiceover lines are quoted and verbatim-ready for a TTS engine.

## Trailer / test cut (mode: trailer)

Use for a short validation cut before the full video. Rules:

- **Timing budget for ~60 s:** 3–4 s title hold → N chosen beats (~15–20 s each, 1–2 clips of 8–12 s per beat) → 3–4 s end hold. Example for three beats: 4 s + 17 s + 17 s + 17 s + 4 s ≈ 59 s.
- **Sections:** only the author-chosen sections appear, each as a distinct beat. Unchosen sections are absent from this cut but stay intact in the master.
- **Photos:** reuse is allowed; a beat can animate the same photo twice with different motion prompts.
- **Voiceover:** one short line per beat (~35–50 Chinese characters fits a ~15–20 s beat). Mark each line so `video-gen` can render it as `.srt` subtitles.
- **Soul line:** the opening or closing beat carries the soul line as defined in the master.

## Engine prompts

- Default engine: Seedance image-to-video (`bytedance/seedance-2.0` via OpenRouter, async `/api/v1/videos` API — see the `video-gen` skill); the prompt style below matches it and is portable to other image-to-video engines.
- Prompt style: name the subject and setting from the photo, then specify lighting, textures, camera movement (dolly, pan, zoom, rack focus, slow tracking), and mood. End with "cinematic documentary style".
- If the user selects a different engine, adapt prompts to that engine's conventions instead.

## Guardrails

- The author's thought-flow stays verbatim and in order; no invented scenes, dialogue, or facts.
- Photos must be real author photos already on disk — never placeholders, stock images, or hallucinated descriptions.
- Voiceover must not introduce claims beyond the master's verified facts; uncitable facts are omitted, not fudged.
- Narrative text is Simplified Chinese; proper nouns, titles, and technical terms stay in Latin script.
- If the master, photos, duration, or target is missing or ambiguous, stop and ask — never guess.

## Verification

- In `full` mode, all content sections defined in the master are covered and the thought-flow order is preserved; in `trailer` mode, every author-chosen section is covered as a distinct beat and none is dropped or merged.
- Every covered section has at least one allocated real photo, and each photo path exists on disk.
- Every voiceover claim traces to the master or a cited live web source.
- Per-clip prompts follow the engine's prompt style and reference real photo content.
- The script is written to a `YYMMDD-slug` file and the path is reported to the user.
