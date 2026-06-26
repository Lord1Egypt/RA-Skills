# Audiobook Workflows

Language switch: you are reading English | [中文说明](./workflows.md)

This document answers one question only: given a certain input, in what order should you run `audiobook`, and which files does each step produce?

## Reading Guide / 阅读导航

- Want the root overview and global conventions? Go back to `../SKILL.en.md`
- Want to understand the voice library first? Read `./voice-library.en.md`
- Want to hand-edit intermediate artifacts and rerun? Read `./editing.en.md`
- Want the structured script format? Read `./script-format.en.md`
- Want TTS synthesis and export details? Read `./synthesis.en.md`

If this is your first time reading the skill, the recommended order is:

1. `../SKILL.en.md`
2. `./voice-library.en.md`
3. this file `./workflows.en.md`
4. then continue into `./editing.en.md` or `./synthesis.en.md` as needed

## Shared path conventions

```bash
WORKSPACE_ROOT=~/.openclaw/workspace
SKILL_ROOT=$WORKSPACE_ROOT/skills/audiobook
VOICE_LIBRARY=$WORKSPACE_ROOT/audiobook-library/voice-library.yaml
LIBRARY_ROOT=$WORKSPACE_ROOT/audiobook-library
STORY_ROOT=$WORKSPACE_ROOT/audiobook-stories          # recommended
RUN_ROOT=$WORKSPACE_ROOT/runs/audiobook
```

Output paths follow two stable scopes:

- library-side artifacts: `$LIBRARY_ROOT/...`
- per-book artifacts: `$RUN_ROOT/<slug>/...`

All command examples below assume you are running them from `"$SKILL_ROOT"`. Start with:

```bash
cd "$SKILL_ROOT"
```

Additional notes:

- the default LLM for long-text understanding, role analysis, and casting reasoning is currently `step-3.5`
- the default `step-3.5` call uses Step's `step_plan` reasoning endpoint
- the default endpoint is `https://api.stepfun.com/step_plan/v1`
- if you change `provider / model / base_url` under `voice-library.yaml -> llm`, those understanding-oriented steps can switch by configuration

## Workflow A: maintain only the voice library

Use this when you want to prepare official voices and user reference audio before working on any specific book.

### A1. Initialize or inspect the voice library

```bash
mkdir -p "$LIBRARY_ROOT"
cp       "$SKILL_ROOT/assets/voice-library.template.yaml"       "$VOICE_LIBRARY"
```

If you want the human review file to exist before the first sync, you can also copy:

```bash
cp       "$SKILL_ROOT/assets/voice-reviews.template.yaml"       "$LIBRARY_ROOT/voice-reviews.yaml"
```

Core files:

- `~/.openclaw/workspace/audiobook-library/voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`

### A2. Refresh official voices

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --refresh-official-only
```

This updates:

- `~/.openclaw/workspace/audiobook-library/.audiobook/official-voices-cache.json`
- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

### A3. Analyze one user reference audio file

Pass the file directly:

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --input /absolute/path/reference-audio.m4a
```

Or drop it into the inbox first:

```bash
cp /absolute/path/reference-audio.m4a ~/.openclaw/workspace/audiobook-library/voices/inbox/
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY"
```

Important details:

- without `--input`, `sync_voice_library.py` currently consumes only one file from `inbox/`
- if you want to process everything currently in `inbox/`, use:

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --process-inbox --downstream-mode off
```

After success, you get:

- `~/.openclaw/workspace/audiobook-library/voices/references/<asset_id>/raw.<ext>`
- `~/.openclaw/workspace/audiobook-library/voices/references/<asset_id>/reference.wav`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-analysis/<asset_id>.json`
- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

If the input came from `voices/inbox/`, the raw file is consumed into `voices/references/<asset_id>/raw.<ext>` and no duplicate is left in the inbox.

### A4. Manually confirm the clone description

Edit:

- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`

What really becomes effective is:

- `manual`
- and if a certain field in `manual` is empty, it falls back to `archived_analysis`

Refresh after editing:

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --asset-id <asset_id> --refresh-profiles-only
```

### A5. Confirm a real paid clone

If the clone decision comes from a book's `clone-review.yaml`, the recommended order is:

1. change `items.<asset_id>.manual.decision` to `confirm_clone`
2. run `recommend_casting.py --refresh-only`
3. confirm `voice-library.yaml -> clones.<asset_id>.selected_for_clone=true`

Then run:

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

If you are not coming from a story-level `clone-review.yaml`, you can also set `voice-library.yaml -> clones.<asset_id>.selected_for_clone=true` directly and then run the same dry-run and actual clone commands.

After success, the following update:

- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-registry.json`
- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

## Workflow B: raw `txt` to final audio

This is the full story workflow.

If you only want to understand the intermediate artifacts first, start with the smallest example chain in `examples/`:

- `story-minimal.txt`
- `story-minimal.structured-script.yaml`
- `story-minimal.casting-plan.yaml`
- `story-minimal.tts-requests.json`

They correspond to the four stages `txt -> structured-script -> casting-plan -> tts-requests`.

### B1. One unified entry point

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --story-input /absolute/path/story.txt
```

Good when you:

- want the full intermediate chain quickly
- are willing to stop and review manually when a blocker appears

Default behavior:

1. refresh official voices
2. process new reference audio if `--voice-input` or `--process-inbox` is used
3. run `txt -> structured-script`
4. generate `casting-review`, `casting-plan`, and `clone-review`
5. preview clone candidates
6. continue into `tts-requests -> synthesize -> finalize` if no blocker remains

Main blockers are:

- clone descriptions still need manual confirmation
- some role selections still need manual confirmation
- some roles still depend on a clone that has not gone through the paid step yet

### B2. Run step by step

Use this when you expect to frequently edit intermediate artifacts by hand.

#### Step 1: raw `txt` -> structured script

```bash
python3 scripts/generate_structured_script.py --library "$VOICE_LIBRARY" --input /absolute/path/story.txt
```

This stage now includes:

- chapter-heading aware pre-splitting
- chunk-level checkpoint and resume
- independent timeout for every LLM request
- `step-3.5` by default, using `https://api.stepfun.com/step_plan/v1` by default

Outputs:

- `$RUN_ROOT/<slug>/<base>.structured-script.yaml`
- `$RUN_ROOT/<slug>/<base>.structured-script.generation.json`

#### Step 2: structured script -> casting

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input $RUN_ROOT/<slug>/<base>.structured-script.yaml
```

This stage also defaults to `step-3.5`, using `https://api.stepfun.com/step_plan/v1` by default.

Outputs:

- `$RUN_ROOT/<slug>/<base>.casting-review.yaml`
- `$RUN_ROOT/<slug>/<base>.casting-plan.yaml`
- `$RUN_ROOT/<slug>/<base>.clone-review.yaml`
- `$RUN_ROOT/<slug>/.audiobook/<base>.casting-plan.role-profiles.json`
- `$RUN_ROOT/<slug>/.audiobook/<base>.casting-plan.casting-selection.json`

#### Step 3: casting -> tts-requests

```bash
python3 scripts/build_tts_requests.py --input $RUN_ROOT/<slug>/<base>.structured-script.yaml
```

Outputs:

- `$RUN_ROOT/<slug>/<base>.script-runtime.json`
- `$RUN_ROOT/<slug>/<base>.tts-requests.json`

#### Step 4: tts-requests -> segments

```bash
python3 scripts/synthesize_tts_requests.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
```

Outputs:

- `$RUN_ROOT/<slug>/<base>.segments/`

#### Step 5: segments -> final audio

```bash
python3 scripts/finalize_audiobook.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
```

Output:

- `$RUN_ROOT/<slug>/<base>.audiobook.<response_format>`

The default `response_format` is `wav`, so the most common full-book file name is still `$RUN_ROOT/<slug>/<base>.audiobook.wav`.

## Workflow C: start from an existing structured script

If you already have a structured YAML or JSON script, you do not need `generate_structured_script.py` first.

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /absolute/path/script.yaml
python3 scripts/build_tts_requests.py --input /absolute/path/script.yaml
python3 scripts/synthesize_tts_requests.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
python3 scripts/finalize_audiobook.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
```

Important: `build_tts_requests.py` accepts only structured YAML or JSON, not raw `txt`.

## Workflow D: rerun from any intermediate stage

### After editing `voice-reviews.yaml`

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --asset-id <asset_id> --refresh-profiles-only
```

### After editing `casting-review.yaml` or `clone-review.yaml`

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /absolute/path/structured-script.yaml --refresh-only
```

### After editing `structured-script.yaml` or `casting-plan.yaml`

```bash
python3 scripts/build_tts_requests.py --input /absolute/path/structured-script.yaml
```

### After editing `tts-requests.json`

Replay all:

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json
```

Replay only part of it:

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json --segments 1,3-5
```

Replay only failed segments:

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json --only-failed
```

### Export only a preview clip

```bash
python3 scripts/finalize_audiobook.py --input /absolute/path/<base>.tts-requests.json --segments 1,3-5
```

## Shared checkpoint after each run

Whether you used the unified entry point or a step-by-step run, it is recommended to inspect:

```text
$RUN_ROOT/<slug>/<base>.artifacts.json
```

or run:

```bash
python3 scripts/list_story_artifacts.py --manifest /absolute/path/<base>.artifacts.json --level review --pretty
```

This manifest is currently the most stable file index entry point for both human review and programmatic integrations.
