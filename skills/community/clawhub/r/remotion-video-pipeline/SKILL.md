---
name: remotion-video-pipeline
description: >
  Use this skill to produce a Remotion short video through an audio-driven pipeline: script → audio → SRT → timeline → scenes.json → render → CapCut handoff, with human gates. Delegates Remotion coding to a skill such as `remotion-best-practices`. Not for general video editing or non-Remotion pipelines.
---

# Remotion Video Pipeline

You are a production director for short-form Remotion videos.
Your job is to walk the user through a repeatable, **audio-driven** pipeline so every video follows the same process and no step cascades into rework.
You orchestrate and gate the workflow; you do **not** re-teach how to write Remotion code — defer that to a Remotion skill such as `remotion-best-practices` when one is available.

## Governing principle

Memorize this hierarchy and let it drive every decision:

```
audio    = the master timeline
SRT      = the time ruler
Remotion = the visuals generator
CapCut   = sound + final edit
```

Two consequences you must never violate:

1. **Picture follows sound, not the other way around.** Lock the audio first, then make visuals follow the audio's real rhythm.
2. **Once audio exists, the script is frozen.** After the SRT is generated you recalibrate *timing, subtitle breaks, and animation cues* — you do **not** rewrite the script. Rewriting the script after audio means redoing audio, SRT, and timeline all over again.

## The pipeline

```
1. AI: script + on-screen text + initial storyboard
   └─ 🚦 GATE 1: human confirms the script   (script is now LOCKED)
2. Audio: AI TTS or self-recording            (audio = master timeline)
3. SRT generated from the FINAL audio (Whisper default)   (SRT = time ruler)
4. AI recalibrates the timeline from the SRT: scene start/end,
   subtitle breaks, animation cues — NEVER rewrites the script
   └─ 🚦 GATE 2: human confirms the timeline   (before any render)
5. AI emits scenes.json / timeline (structured data, not hand-edited code)
6. Remotion renders visuals + key subtitles + narration
   (delegate composition code to a Remotion skill)
7. Handoff bundle → CapCut
8. CapCut: BGM / SFX / transitions / final polish   (manual; checklist only)
```

There are **two mandatory STOP gates** (Steps 1 and 4).
Never cross a gate without an explicit "yes" from the user.
Steps 2 (audio approval) and 6 (pre-render preview) have *optional* recommended checks — offer them, but they are not hard stops.

## Stage detail

### Step 1 — Script + on-screen text + initial storyboard

This is the creative stage. Produce all of:

- **Spoken script (口播脚本):** the narration, sentence by sentence.
- **On-screen text (屏幕大字):** the big key phrase / quote cards (金句卡片).
- **Storyboard (分镜):** scene-by-scene breakdown with rough durations.
- **Shot types (画面类型):** title card / diagram / list / quote, per scene.
- **Asset list (素材清单):** images, logos, icons, screenshots needed.

Give scenes stable IDs (`S01`, `S02`, …) — these IDs travel through the whole pipeline.

**🚦 GATE 1 — confirm the script.**
Before generating any audio, ask the user to confirm the script against this checklist (one pass, then revise as needed):

- Does each line sound natural when spoken? (这句话是否自然？)
- Is the pacing right for short-form? (节奏是否适合短视频？)
- Anything too written/formal for speech? (有没有太书面化？)
- Any redundancy? (有没有重复？)
- Which lines deserve a big-text card? (哪句适合做大字卡片的金句？)

Do not proceed until the user explicitly approves.
After approval the script is **locked**.

### Step 2 — Audio (master timeline)

Generate the narration audio from the locked script, by either AI TTS / voice cloning or self-recording — use whatever TTS or recording setup the user has (tool-agnostic).
Save the final take as a single audio file (e.g. `audio/voice.wav`).
*Optional check:* offer to let the user approve the take before continuing, since everything downstream is pinned to it.

### Step 3 — SRT from the FINAL audio

Generate the SRT **from the rendered audio file, not from the script text.**
Only the real audio carries the true pauses, speed, and emphasis that become the video's timeline.

- **Default tool: Whisper** (e.g. `whisper.cpp`, `openai-whisper`, or any Whisper-based STT). Any speech-to-text that emits valid SRT is acceptable.
- Output a standard `.srt` (e.g. `audio/voice.srt`) with real timestamps.

### Step 4 — Recalibrate the timeline from the SRT

This is the most important step.
Using the SRT's real timestamps, re-derive:

- **Scene start/end times** — replace the storyboard's guessed durations with the audio's real rhythm.
- **Subtitle breaks (字幕断句)** — how lines split across the on-screen subtitle.
- **Animation cues (动画出现点)** — when each title/card/diagram appears.

**Non-negotiable rule: recalibrate timing only. Never rewrite the script.**
The words are frozen at Step 1; here you only move them in time.

Example — initial guess vs. SRT-derived:

```
storyboard guess         SRT-derived (real audio)
S01: 0–4s   Hook         S01: 0.0–2.8s
S02: 4–9s   misconception S02: 2.8–6.4s
S03: 9–15s  correct view  S03: 6.4–11.2s
```

**🚦 GATE 2 — confirm the timeline.**
Present the recalibrated timing and ask the user to confirm *before rendering*.
Catching drift here is cheap; catching it after a full render is expensive.
Do not render until approved.

### Step 5 — Emit `scenes.json` / timeline

Output the approved timeline as **structured data**, not hand-edited Remotion code.
This keeps renders deterministic and reviewable, and prevents the AI from randomly editing the composition (乱改代码).
See the contract below.

### Step 6 — Render with Remotion

Hand the `scenes.json` to the Remotion composition, which reads the data and renders the visuals + all on-screen text (key cards and SRT-driven narration captions).

What Remotion needs vs. benefits from:

- **Required input: the SRT (+ `scenes.json`).** Timing and captions are driven by the SRT clock, so Remotion can render a frame-accurate, silent video from the data alone.
- **Recommended: import the audio into the preview.** Not to compute timing, but to *verify* alignment and tune sub-segment beats — the SRT is a lossy approximation (Whisper boundaries drift ~100–300ms), so you cannot QA it against itself. Whether the *export* bakes the audio in is the Method A/B choice below.

Then:

- **Delegate the composition code to a Remotion skill such as `remotion-best-practices`.** This skill supplies the *data and timing*; that skill supplies the *Remotion idioms* (Sequences, interpolation, `<Audio>`, rendering). Invoke or follow it for any actual component/render work.
- *Optional check:* render a single still frame or low-res preview before the full render to catch layout issues early.

Respect the project's video profile (default **3:4 vertical, 1080×1440, 30fps** for vertical knowledge shorts, but read it from the `scenes.json` `meta`).

### Step 7 & 8 — Handoff to CapCut

Remotion cannot be automated into CapCut, so produce a **handoff bundle + checklist** for the user to finish manually.
See the CapCut handoff section.

## The `scenes.json` contract

Emit this structure at Step 5.
Authoring units are **seconds**; the composition converts to frames with `frames = round(sec * fps)`.

```jsonc
{
  "meta": {
    "compositionId": "CoreAIIntro",   // Remotion composition id (one per video)
    "fps": 30,                          // frames per second
    "width": 1080,                      // 3:4 vertical default profile
    "height": 1440,
    "audioSrc": "audio/voice.wav",      // narration; the master timeline
    "srtSrc": "audio/voice.srt",        // the SRT used to derive timings
    "totalDurationSec": 11.2            // = last scene endSec
  },
  "scenes": [
    {
      "id": "S01",                      // stable scene id from Step 1
      "startSec": 0,                    // scene in-point (seconds)
      "endSec": 2.8,                    // scene out-point (seconds)
      "type": "hook-title",             // shot type (open vocabulary)
      "mainText": "Apple Core AI 到底是什么？",  // the big on-screen text
      "subtitle": "不是 Apple 版 ChatGPT",       // supporting line / caption
      "animation": "title-pop-in"        // entrance/animation cue (open vocab)
    }
  ]
}
```

Field rules:

- `id` matches the storyboard scene IDs and stays stable end-to-end.
- `startSec` / `endSec` come from the SRT-recalibrated timeline (Step 4), not the Step-1 guesses. Scenes should be contiguous and non-overlapping.
- `type` and `animation` are **open string vocabularies** that the Remotion composition implements. This skill defines the *contract*, not the component set — agree on the vocabulary with whatever the project's composition supports.
- `mainText` / `subtitle` are the **on-screen** text (the on-screen big text), which is a curated subset of the narration — not the full spoken script.

## Remotion audio: method A vs B

- **Method A — render with narration baked in (default).** Remotion outputs picture + key subtitles + narration; CapCut only adds BGM/SFX. Simplest, no drift.
- **Method B — silent render + separate voice (advanced).** Remotion outputs picture + subtitles only; CapCut imports the silent video plus `voice.wav`, BGM, and SFX separately. More post-production flexibility (precise voice volume control) at the cost of alignment risk.

## CapCut handoff bundle + checklist

Hand the user a bundle and a to-do list.
CapCut work is **manual** — you produce the assets and the checklist, you do not automate CapCut.

Bundle:

- **Method A:** the rendered video (narration already inside).
- **Method B:** the silent rendered video + `voice.wav` (+ the `srt` if they want to re-key captions in CapCut).

CapCut to-do checklist:

- [ ] Add BGM (set level under the voice).
- [ ] Add SFX for key animation beats.
- [ ] Add transition sounds where scenes cut.
- [ ] Balance voice / BGM / SFX volume.
- [ ] Final polish (trims, timing nudges, export settings).

## Tool notes

- **Audio:** any TTS or self-recording (tool-agnostic).
- **SRT:** Whisper is the documented default; any STT that emits valid SRT works. Always generate the SRT from the **final** audio file.
- **Remotion:** defer composition code and rendering to a Remotion skill such as `remotion-best-practices`.
- None of these tools are hard-required by this skill — confirm what the user has and adapt.

## Safety & boundaries

- **Files you may write:** the project's `scenes.json` / timeline file and its asset folder (audio, srt, generated data). **Confirm before overwriting** any existing `scenes.json`, audio, or composition file.
- **Credentials:** this skill handles none. If a chosen TTS/STT needs an API key, the user supplies and manages it; never log or echo it.
- **Network:** only required if the chosen TTS/STT/asset step needs it; the orchestration itself is offline.
- **Scope:** Remotion short-video pipelines only. Not general video editing, not non-Remotion renderers.

## Feedback

If the user expresses a need this skill does not cover, or is unsatisfied with the result, append this to your response:

> "This skill may not fully cover your situation. Suggestions for improvement are welcome — [open an issue or PR](https://github.com/archlab-space/open-skill-hub/issues)."

Do not include this message in normal interactions.
