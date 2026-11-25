---
name: subclip-music-generation
description: Generate instrumental background music, soundtracks, underscore, or original music beds for product demos, SaaS launches, ads, explainers, talking heads, stories and travel videos using Subclip cloud music models. Use for new music, music variations, image-inspired music or reusing generated tracks, and for AI sound effects (whooshes, hits, risers, UI sounds, foley, ambience). For sung lyrics, also read subclip-songwriting.
---

# Music generation

Use Subclip MCP `generate_music`; outputs live under **Audio**, not a separate category. Read [prompt recipes](references/prompt-recipes.md) for the matching use case before drafting. This skill is for generating media, not publishing or licensing claims.

## Model preference

Default to **Google Lyria 3 Pro** (`modelId: "lyria-3-pro"`) for all music and song generation. Switch to another music model only when the user explicitly requests that model or asks to switch. Do not switch automatically for duration, output format, cost, lyrics, or after a failure. If Lyria cannot meet a requirement or is unavailable, explain the limitation and ask which model the user wants before generating with another model.

Sound effects are not music: for a whoosh, hit, UI sound, foley or ambience use **ElevenLabs Sound Effects** (`elevenlabs-sound-effects`) as described in [Sound effects](#sound-effects), not Lyria.

## Prepare a useful brief

Identify the intended scene, approximate length, mood/energy arc, genre, 2–4 instruments, tempo or groove, and whether narration needs room. Default a background-music request to `settings.mode: instrumental`; explicitly request no vocals, humming or speech. Do not invent song lyrics for an instrumental request.

Use a compact positive brief: **purpose + style/mood + rhythm + instrumentation + progression + mix constraints**. Avoid unrelated genre lists and contradictory tempo or energy instructions. Describe approximate scene beats in seconds when useful; Lyria and MiniMax have no duration parameter. ElevenLabs offers a target length, but musical events still need review and may need trimming. Generate a usable track, then trim/fade/mix the imported audio to the actual timeline.

## Discover and generate

1. `list_ai_models(kind: audio)` and filter `operations` for `text_to_music`. Read live pricing/settings and use `get_ai_credit_status` when estimating available credits. Speech voices are unrelated; do not call `list_ai_voices` for music.
2. Use Lyria by default; consult other model capabilities only for an explicit user-requested model:
   - **Lyria 3 Pro**: prompt and up to 10 image references, optional seed; approximately up to 3 minutes. Images convey scene, palette and mood. Lyrics, language, vocals and progression are written into the prompt by the adapter. No separate duration, bitrate, sample-rate or instrumental provider fields. A seed does not guarantee identical output.
   - **MiniMax Music 2.6**: description up to 2,000 characters, custom lyrics up to 3,500, instrumental mode or automatic lyrics. Sample rates 16/24/32/44.1 kHz; MP3 bitrates 32/64/128/256 kbps; MP3 or WAV. Subclip's `pcm` option delivers PCM in a WAV container for safe playback/import. No images, audio reference, seed or exact-duration field. Tracks may reach 6 minutes.
   - **ElevenLabs Music** (`elevenlabs-music`): `settings.music_length_ms` from 5,000 to 300,000 (default 10,000). `settings.output_format`: `mp3_standard` (128 kbps), `mp3_high_quality` (192 kbps), `wav_16khz`, `wav_22khz`, `wav_24khz`, `wav_cd_quality` (44.1 kHz). No images, audio references, seed, model-version selector or composition-plan field in this Replicate endpoint. Custom lyrics are appended to the prompt; total provider prompt including instructions is limited to 4,100 characters. `instrumental` maps to `force_instrumental: true`; song modes set it false and describe vocals in the prompt. Do not confuse the wider native ElevenLabs API with the Replicate wrapper.
3. Resolve user-authorized image references with `list_editor_assets`; send exact source file/item IDs in `sourceAssets` with `role: reference`. Never put paths, URLs or hidden asset IDs in settings. Do not upload a visible attachment without authorization to use it.
4. Establish the exact music brief, model, image inputs, lyrics mode, settings and credit estimate. An explicit generation request authorizes one matching generation; ask only for missing material choices or an unapproved change. Prices come from the live catalog. Lyria/MiniMax charge per successful track. ElevenLabs is billed per second of validated output: currently 0.7055 credits/second (42.33/minute), rounded up once at the total. Estimate uses requested seconds plus 1 second of codec padding; only actual output duration is charged. Read the live catalog instead of assuming these rates stay fixed. Successful output is charged once, not per retry; cloud files also use storage.
5. Call `generate_music` once with `confirmed: true` after authorization. Use `settings: {mode: 'instrumental'}` for background music. Do not send top-level durationSeconds, video generateAudio or negativePrompt. For ElevenLabs put target duration in settings.music_length_ms and the format in settings.output_format. For other models describe approximate timing in the prompt.
6. Keep the operation ID. In-app agents **end the turn after the accepted async result**; Subclip resumes the conversation on completion/failure. Do not loop, sleep-poll or resubmit because the track is queued. External clients can inspect `get_ai_operation` later.
7. On completion use `get_ai_operation` and `import_ai_operation_to_timeline` by stable ID when the user asked to place it. Keep original editable visuals and audio intact. A generated track imports as one Audio asset, not stems. Adjust gain beneath narration; trim and add fades with audio-editing tools when requested. Inspect duration before placement.

## Sound effects

Use `generate_music` with `modelId: "elevenlabs-sound-effects"` for short non-musical sounds: transition whooshes and swishes, impacts and hits, risers, UI clicks and notifications, foley (footsteps, doors, paper), and ambience beds (rain, café, room tone). Do not use it for music beds or songs, and do not use speech tools for sound effects.

- Prompt: one sound, at most 450 characters. Describe the source, action, space and texture, for example "heavy wooden door slams in a stone hall" or "fast airy whoosh sweeping left to right, clean, no music". Generate one sound per call; place several calls on the timeline for a sequence.
- `settings.duration_seconds`: 0.5–22. Match the timeline gap (a transition whoosh is usually 0.5–1.5 s, a hit 1–2 s). Omit it for automatic length.
- `settings.prompt_influence`: 0–1, default 0.3. Raise it (0.6–0.8) for a precise, literal sound; lower it for variety.
- `settings.loop: true` only for ambience or backgrounds that will loop under the edit; then set `loop` on the placed audio item with `update_audio_item`.
- `settings.output_format`: `mp3_44100_64`, `mp3_44100_128` (default) or `mp3_44100_192`.
- Not accepted: song modes or lyrics (keep `mode` instrumental or omit it), `music_length_ms`, image references, seed, and MiniMax `audio_format`/`sample_rate`/`bitrate`.
- Pricing: billed per second of the saved sound, currently 0.17 credits/second. The estimate is (duration_seconds + 1) × rate; automatic length is quoted at the 22-second maximum (3.91 credits). Quote with `estimate_ai_generation` (`kind: "audio"`, `modelId: "elevenlabs-sound-effects"`, `durationSeconds` equal to `duration_seconds`, or omitted for automatic). Read the live catalog instead of assuming the rate stays fixed.

```json
{"confirmed":true,"modelId":"elevenlabs-sound-effects","prompt":"Fast airy whoosh transition sweeping from left to right, clean, no music.","settings":{"duration_seconds":1,"prompt_influence":0.5}}
```

After completion, import it with `import_ai_operation_to_timeline` and set its volume with the subclip-audio-editing mixing defaults: sound effects sit under speech, so start around 0.4–0.7.

## Example call

After live discovery and an authorized request for a demo soundtrack:

```json
{"confirmed":true,"modelId":"lyria-3-pro","prompt":"Optimistic electronic underscore for a product demo, 108 BPM. Warm synth pulses, muted plucks and restrained percussion. Start simply, lift gently at the feature reveal, then resolve. Sparse midrange for spoken narration. Instrumental, no vocals.","settings":{"mode":"instrumental"}}
```

A changed prompt/model or new variation creates a new paid operation; do not silently regenerate. For a failed transfer/billing completion use the existing `retry_ai_operation` and its recovery rules, not a new generation. For deletion identify exact IDs and confirm unless the user already asked to delete those items. For a running music operation, deletion also requests cancellation. Respect any conflict returned by the service and do not promise cancellation or a refund before it is confirmed. No live generation in plan mode: read-only discovery, brief and estimate only.

Sources: [ElevenLabs Replicate schema](https://replicate.com/elevenlabs/music/api/schema), [ElevenLabs prompting guide](https://elevenlabs.io/docs/overview/capabilities/music/best-practices), [MiniMax schema and guidance](https://replicate.com/minimax/music-2.6), [Lyria schema](https://replicate.com/google/lyria-3-pro), [Google prompting guide](https://deepmind.google/models/lyria/prompt-guide/). API catalog remains authoritative if capabilities change.
