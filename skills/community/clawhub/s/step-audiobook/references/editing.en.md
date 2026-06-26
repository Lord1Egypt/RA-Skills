# Audiobook Editing Guide

Language switch: you are reading English | [中文说明](./editing.md)

This document answers two practical questions:

1. Which file should I edit when I want to change a result?
2. After editing it, which step should I rerun?

## Reading Guide / 阅读导航

- Want the root overview and global conventions? Go back to `../SKILL.en.md`
- Want the full execution order? Read `./workflows.en.md`
- Want to understand the voice library first? Read `./voice-library.en.md`
- Want the downstream TTS chain? Read `./synthesis.en.md`

If this is your first time manually editing intermediate artifacts, the recommended order is:

1. `../SKILL.en.md`
2. `./workflows.en.md`
3. this file `./editing.en.md`
4. return to `./voice-library.en.md` when the issue is voice-related

## Which file should I inspect first?

### I want to fix the real description of a clone voice

Edit:

- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`
- Path: `clones.<asset_id>.manual`

Then run:

```bash
python3 scripts/sync_voice_library.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --asset-id <asset_id> --refresh-profiles-only
```

### I want to quickly see which clone voices still need manual review

Run:

```bash
python3 scripts/list_pending_reviews.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --pretty
```

If you want both reviewed and pending items:

```bash
python3 scripts/list_pending_reviews.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --all --pretty
```

### I want to inspect the raw model analysis for one reference audio file

Check:

- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-analysis/<asset_id>.json`
- or `voice-reviews.yaml -> clones.<asset_id>.model_analysis`

These files are mainly for debugging. Do not edit them unless you are debugging the pipeline itself.

### I want to see the clone profile that is currently effective

Check:

- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`

If the effective profile view does not match your expectation, go back to `voice-reviews.yaml -> manual` first.

### I want to inspect the unified voice input that downstream casting actually reads

Check:

- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

or run:

```bash
python3 scripts/list_voice_candidates.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --pretty
```

### I want to change the final voice chosen for a role

Edit:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-review.yaml`
- Path: `roles.<role_id>.manual`

Then run:

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /absolute/path/structured-script.yaml --refresh-only
```

### I want to decide whether a clone is worth paying for

Edit:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.clone-review.yaml`
- Path: `items.<asset_id>.manual.decision`

Allowed values:

- `confirm_clone`
- `skip`
- `pending`

Then run:

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /absolute/path/structured-script.yaml --refresh-only
```

### I want to edit story content, speaker assignment, or scene hints

Edit:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml`

Then run:

```bash
python3 scripts/build_tts_requests.py --input /absolute/path/structured-script.yaml
```

### I want to change the real text or instruction sent to TTS for one segment

Edit:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.tts-requests.json`

Common fields:

- `segments[].input_text`
- `segments[].instruction`
- `segments[].extra_body`
- `common_request.extra_body`

Then run:

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json
```

If you only want to replay part of the file:

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json --segments 1,3-5
```

### I want to preview finished segments instead of exporting the whole book

Run:

```bash
python3 scripts/finalize_audiobook.py --input /absolute/path/<base>.tts-requests.json --segments 1,3-5
```

## Generated files you should usually not edit directly

These files are meant to be inspected, not manually maintained:

- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/official-voices-cache.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.artifacts.json`

If one of these looks wrong, go back to the upstream manual entry point and rerun the matching step.

## Quick rerun reference

### I edited a manual clone description

```bash
python3 scripts/sync_voice_library.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --asset-id <asset_id> --refresh-profiles-only
```

### I edited casting confirmation

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /absolute/path/structured-script.yaml --refresh-only
```

### I edited the structured script

```bash
python3 scripts/build_tts_requests.py --input /absolute/path/structured-script.yaml
```

### I edited TTS requests

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json
```

### I only want to rerun failed segments

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json --only-failed
```

### I want to force overwrite segments that already succeeded

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json --force
```

### I want to export the whole book again

```bash
python3 scripts/finalize_audiobook.py --input /absolute/path/<base>.tts-requests.json --force
```

## Final check after manual edits

After any manual change, it is a good habit to check:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.artifacts.json
```

or run:

```bash
python3 scripts/list_story_artifacts.py --manifest /absolute/path/<base>.artifacts.json --level review --pretty
```

This is more stable than remembering every intermediate file path by hand, and it is also the best handoff point for programmatic integrations.
