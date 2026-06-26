# Audiobook Casting

Language switch: you are reading English | [中文说明](./casting.md)

`recommend_casting.py` maps roles from the structured script onto one currently effective voice from the unified voice candidate pool, and separates paid clone decisions into a dedicated review file.

## Reading Guide / 阅读导航

- Want the root overview and global conventions? Go back to `../SKILL.en.md`
- Want the full execution order? Read `./workflows.en.md`
- Want to understand where the structured script comes from first? Read `./script-format.en.md`
- Want the downstream TTS request and synthesis chain? Read `./synthesis.en.md`

If this is your first time reviewing casting logic, the recommended order is:

1. `../SKILL.en.md`
2. `./voice-library.en.md`
3. `./script-format.en.md`
4. this file `./casting.en.md`

## Input files

Casting depends on two inputs:

1. the structured script
2. the unified voice candidate pool

Default paths:

- script: `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml`
- candidate pool: `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

The unified voice candidate pool is the only voice input source that casting should read. Do not go back to `voice-reviews.yaml` or `voice-library.yaml` directly during the matching stage.

## Output files

`recommend_casting.py` generates five outputs by default:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-plan.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.clone-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.role-profiles.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.casting-selection.json`

Their roles are:

### `casting-review.yaml`

This is the human review entry point.

Here you may manually change:

- which candidate voice is finally chosen for a role
- the stable instruction for that role
- casting notes

### `casting-plan.yaml`

This is the effective casting result.

Downstream `build_tts_requests.py` reads this file, not `casting-review.yaml`.

### `clone-review.yaml`

This file is dedicated to paid clone decisions.

It summarizes:

- which roles strongly depend on a clone
- whether that clone should really be paid for
- the user's final `confirm_clone / skip / pending`

Important: this file itself is not the direct input to the paid clone step. The real input for `clone_selected_voices.py` is the synchronized library state where `voice-library.yaml` has `selected_for_clone=true` for the chosen assets.

### `role-profiles.json`

The raw role voice profiles extracted by the LLM, with supporting evidence.

This is useful when you need to understand why a role was interpreted as needing a certain kind of voice.

### `casting-selection.json`

The raw archive of the LLM casting decision.

This is useful when you need to inspect why the model chose a specific candidate.

## Current casting rules

### Rule 1: only match against the unified voice candidate pool

The pool mixes two kinds of voices:

- `source=official`
- `source=clone`

Casting no longer runs separate logic branches for them.

### Rule 2: do not guess official voice semantics from the name

Official voices are matched mainly through these fields:

- `official_description`
- `recommended_scenes`
- `selection_summary`
- `information_quality`

`display_name` is for display only and should not be the primary casting signal.

If an official voice lacks description and recommended scenes, it is marked as `information_quality=missing` and should only be treated as a low-information fallback.

### Rule 3: clone voices use the effective profile

The main clone candidate information comes from:

- `.audiobook/effective-voice-library.yaml`
- then merged into `.audiobook/voice-candidate-pool.yaml`

In practice, casting sees these clone fields:

- `description`
- `tags`
- `suitable_scenes`
- `avoid_scenes`
- `stable_instruction`
- `selection_summary`

The effective profile follows this precedence:

```text
manual > archived_analysis > empty
```

### Rule 4: prefer ready voices when scores are close

If an official ready voice and a pending clone are close in fit, the system should prefer the ready voice by default.

A clone should be pushed into `clone-review.yaml` only when it is clearly better for the role and worth a real paid cloning decision.

## Current LLM configuration source

Casting defaults to the top-level LLM configuration in `voice-library.yaml`:

- `llm.defaults`
- `llm.tasks.casting_role_extraction`
- `llm.tasks.casting_selection`

This means:

- the default is Step 3.5
- the default `step-3.5` call uses Step's `step_plan` reasoning endpoint
- the default endpoint is `https://api.stepfun.com/step_plan/v1`
- later, you can switch to another OpenAI-compatible model if needed
- both docs and code try to avoid hard-coding the whole decision into large regex and weighted NLP rules

## How to refresh after manual confirmation

### After editing `casting-review.yaml`

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /absolute/path/structured-script.yaml --refresh-only
```

### After editing `clone-review.yaml`

Run the same command:

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /absolute/path/structured-script.yaml --refresh-only
```

Refresh will:

- rebuild `casting-plan.yaml`
- rebuild `clone-review.yaml`
- sync `confirm_clone / skip` back into `voice-library.yaml -> selected_for_clone`

In other words, every time you manually change `clone-review.yaml`, you must run this refresh step before calling `clone_selected_voices.py`.

## Checks before continuing downstream

Before entering `build_tts_requests.py`, confirm at least:

- every speaking role in `casting-plan.yaml` has a `selected_voice_id`
- `selected_status=ready`
- no role still depends on a paid clone that has not been completed yet

If any of these conditions are missing, `build_tts_requests.py` stops with an error instead of generating an incomplete request list.
