# Audiobook Voice Library

Language switch: you are reading English | [中文说明](./voice-library.md)

This document explains where the `audiobook` voice library lives, what each file is responsible for, and how user reference audio flows into later casting and TTS.

## Reading Guide / 阅读导航

- Want the root overview and global conventions? Go back to `../SKILL.en.md`
- Want the full execution order? Read `./workflows.en.md`
- Want to hand-edit artifacts and rerun? Read `./editing.en.md`
- Want to understand how casting uses the voice library? Read `./casting.en.md`

If this is your first time maintaining the voice library, the recommended order is:

1. `../SKILL.en.md`
2. this file `./voice-library.en.md`
3. `./workflows.en.md`
4. then continue into `./editing.en.md` when manual correction is needed

## Default paths

```bash
WORKSPACE_ROOT=~/.openclaw/workspace
LIBRARY_ROOT=$WORKSPACE_ROOT/audiobook-library
VOICE_LIBRARY=$LIBRARY_ROOT/voice-library.yaml
```

If your team needs a custom directory layout, do not modify script constants first. Prefer changing `voice-library.yaml -> paths`. The examples in this document all use the default paths.

Default directory layout:

```text
audiobook-library/
  voice-library.yaml
  voice-reviews.yaml
  voices/
    inbox/
    references/
      <asset_id>/
        raw.<ext>
        reference.wav
  .audiobook/
    official-voices-cache.json
    voice-analysis/
      <asset_id>.json
    effective-voice-library.yaml
    voice-candidate-pool.yaml
    voice-registry.json
    voice-previews/
```

## Difference between template files and example files

The skill contains two groups of similar-looking files with different purposes:

1. `assets/voice-library.template.yaml` / `assets/voice-reviews.template.yaml`
   - used to initialize the real library files you will run with
   - comments are more complete and better for first-time setup
2. `examples/voice-library.minimal.yaml` / `examples/voice-reviews.minimal.yaml`
   - used to understand the smallest valid structure
   - good for field alignment, partial copy-paste, and small mocks
   - not recommended as a direct replacement for the long-lived runtime library files

`examples/voice-library.minimal.yaml` demonstrates two common clone states:

- one item already ingested and waiting for human confirmation before paid clone
- one item only pre-registered and not yet ingested from audio

`examples/voice-reviews.minimal.yaml` demonstrates:

- one item already confirmed by a human, where `manual` is effective
- one item still pending review, where the system can only fall back to `archived_analysis`

## Responsibilities of each file

### `voice-library.yaml`

Path: `~/.openclaw/workspace/audiobook-library/voice-library.yaml`

Purpose: the main configuration file for the voice library.

It stores:

- path configuration
- official voice sync state
- clone asset metadata
- `selected_for_clone`
- `source_file` / `raw_file`
- LLM configuration

It should not store the final human-authored clone profile body.

### `voice-reviews.yaml`

Path: `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`

Purpose: the only human review entry point for clone voice descriptions.

If you want a commented review skeleton before the first ingest, copy:

```bash
cp ~/.openclaw/workspace/skills/audiobook/assets/voice-reviews.template.yaml        ~/.openclaw/workspace/audiobook-library/voice-reviews.yaml
```

If you do not initialize it manually, that is fine too. The first run of `sync_voice_library.py` creates it automatically.

Each clone entry contains:

- `manual`: the human-confirmed description, tags, suitable scenes, avoid scenes, and stable instruction
- `model_analysis`: the archived model output for that run
- `archived_analysis`: the candidate profile distilled from model output
- `review`: whether the item is still waiting for confirmation

Effective precedence:

```text
manual > archived_analysis > empty
```

To quickly inspect which clone voices are still pending review:

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```

### `voices/inbox/`

Path: `~/.openclaw/workspace/audiobook-library/voices/inbox/`

Purpose: the drop zone for new reference audio waiting to be processed.

You can place new audio here and then run:

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY"
```

Two important notes:

- without `--input`, `sync_voice_library.py` currently consumes only the first pending audio file in `inbox/`
- after a successful ingest, the file is moved into `voices/references/<asset_id>/raw.<ext>` and does not stay in `inbox/`

If you want to process every file currently in `inbox/` in one go, prefer:

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --process-inbox --downstream-mode off
```

### `voices/references/<asset_id>/`

Purpose: the long-lived reference audio asset directory.

It usually contains:

- `raw.<ext>`: the original uploaded audio
- `reference.wav`: the normalized mono 24k wav

Both files should normally be kept long term. Do not automatically delete them after clone succeeds.

### `.audiobook/voice-analysis/<asset_id>.json`

Purpose: the full archive for one audio analysis run.

It keeps at least:

- `raw_text`
- `raw_model_result`
- `structured_result` if a second structuring pass was used
- `normalized_result`
- `analysis_pipeline`

This file is good for debugging model analysis issues, but it should not be used directly as the later casting input.

### `.audiobook/effective-voice-library.yaml`

Purpose: the generated effective profile view for clone voices.

Downstream flows should read clone voice information from here instead of going straight to `voice-reviews.yaml`.

### `.audiobook/official-voices-cache.json`

Purpose: the latest cached result from the official Step voice API.

It currently preserves:

- `official_description`
- `recommended_scenes`
- `selection_summary`
- `information_quality`

`display_name` is only for display and should not be the main casting signal.

### `.audiobook/voice-candidate-pool.yaml`

Purpose: the unified voice candidate pool that merges official voices and effective clone voices.

Casting should read only this file.

### `.audiobook/voice-registry.json`

Purpose: the registry of clones that have completed the paid clone step.

It stores:

- `voice_id`
- `file_id`
- `preview_wav`
- `prepared_at`

## Full flow for user reference audio

```text
raw audio
-> voices/inbox/                or --input /absolute/path/audio
-> voices/references/<asset_id>/raw.<ext>
-> voices/references/<asset_id>/reference.wav
-> step-audio-r1.1 analysis
-> .audiobook/voice-analysis/<asset_id>.json
-> voice-reviews.yaml
   - manual
   - archived_analysis
-> .audiobook/effective-voice-library.yaml
-> .audiobook/voice-candidate-pool.yaml
-> recommend_casting.py
```

## How the current r1.1 analysis stage works

For user reference audio, `sync_voice_library.py` performs the following:

1. normalize the source into `reference.wav`
2. call `step-audio-r1.1`
3. ask the model to analyze long-term voice traits instead of transcribing the spoken lines
4. if the first response still looks like transcript text, retry once with a stronger `no transcript` instruction
5. write the result into `voice-analysis/<asset_id>.json`
6. generate `archived_analysis`
7. preserve `manual` and never overwrite user-confirmed content automatically

Key rules:

- if evidence is weak, write `unknown`
- do not infer gender aggressively from words like `young`, `gentle`, or `sweet`
- `manual` always wins over automated analysis

## How official voices enter the library

Official voices are not written back into the main body of `voice-library.yaml`. They follow this route instead:

```text
Step official voices API
-> .audiobook/official-voices-cache.json
-> .audiobook/voice-candidate-pool.yaml
```

Benefits of this design:

- user-maintained fields are not overwritten by the official API
- official voices can be refreshed on every run
- casting only has to read one unified voice candidate pool

## The paid clone boundary

Only `clone_selected_voices.py` actually triggers the paid clone API.

Every earlier step only does:

- ingest reference audio
- analyze long-term voice traits
- shortlist candidate clones
- wait for human confirmation

Recommended sequence:

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

But the real input read by `clone_selected_voices.py` is not the story-level `clone-review.yaml`. It is the library-level state `voice-library.yaml -> clones.<asset_id>.selected_for_clone`.

If your clone decision comes from a story's `clone-review.yaml`, the sequence should be:

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /absolute/path/structured-script.yaml --refresh-only
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

The first step syncs `items.<asset_id>.manual.decision` back into the library-level `selected_for_clone`. After clone succeeds, `voice_id` is stored in `voice-registry.json` and propagated into the effective voice library and unified candidate pool.

## Recommended manual edit entry points

Only edit these places directly:

- adjust a clone description: `voice-reviews.yaml -> clones.<asset_id>.manual`
- adjust whether a clone enters the paid queue: `*.clone-review.yaml -> items.<asset_id>.manual.decision`
- adjust the library-level asset switch: `voice-library.yaml -> clones.<asset_id>.enabled / selected_for_clone`

Do not edit these generated files directly:

- `.audiobook/effective-voice-library.yaml`
- `.audiobook/voice-candidate-pool.yaml`
- `.audiobook/official-voices-cache.json`
- `.audiobook/voice-analysis/<asset_id>.json`

If you only want to see which entries are still pending, do not open raw YAML first. Prefer:

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```
