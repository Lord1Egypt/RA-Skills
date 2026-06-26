# Audiobook

Language switch: you are reading English | [中文说明](./SKILL.md)

This file is the English companion to `SKILL.md`.

`audiobook` is a complete local audiobook workflow with four stages:

1. voice library maintenance: official voice sync, user reference audio analysis, and paid clone preparation
2. script preparation: `txt -> structured-script`
3. casting: `structured-script -> casting-review -> casting-plan`
4. synthesis and export: `casting-plan -> tts-requests -> segments -> final audio`

It is designed for two kinds of callers:

- human users who want to review and edit intermediate artifacts step by step
- programmatic callers that read each script's JSON stdout and the unified `artifacts.json`

`audiobook` is not just a TTS tool that reads a novel aloud. It is a full local workflow around voice assets, structured scripts, role casting, replayable TTS requests, and final audio export.

Design principles:

- Step-specific audio capabilities keep using Step native APIs, such as `step-audio-r1.1`, the official voice API, the voice cloning API, and `stepaudio-2.5-tts`
- long-text understanding, role analysis, and casting reasoning use `step-3.5` by default
- the default `step-3.5` call uses Step's `step_plan` reasoning endpoint at `https://api.stepfun.com/step_plan/v1`
- the LLM understanding layer is intentionally implemented through a configurable compatibility layer so it can later switch to another compatible LLM
- intermediate artifacts are written to disk by default so humans can review them and programs can resume from any stage

## Capability scope

`audiobook` currently covers the following capabilities:

1. Users can prepare a set of candidate reference audio files for future cloning. The skill calls `step-audio-r1.1` to analyze long-term voice traits and stores the result as a usable profile for later role casting.
2. After reviewing the analysis, users can explicitly choose which candidate voices are worth sending through the real StepFun paid clone flow. Paid cloning is never triggered automatically in the default path.
3. The skill automatically combines official StepFun system voices, user-completed clone voices, and locally maintained pending clone analyses into one unified voice library and one unified voice candidate pool.
4. Given one or more raw text files, the skill uses `step-3.5` by default for chunking, chapter-aware analysis, role extraction, and structured script generation, including the narrator. The current default path uses Step's `step_plan` reasoning endpoint.
5. Based on the structured script and the unified voice library, the skill produces a role-to-voice casting plan. These semantic reasoning steps default to `step-3.5`, but the implementation tries to avoid hard-coded NLP logic so the LLM layer can later be replaced by another compatible model.
6. Based on the final casting result, the skill generates a replayable request manifest that matches the calling style of `stepaudio-2.5-tts`, making it easy to batch synthesize, rerun selected segments, and tune parameters.
7. The skill supports per-segment synthesis and can concatenate those segments into one or more final output files, including a full-book export and partial preview exports.
8. Every major intermediate artifact can be reviewed and edited by a human. Users can resume from a chosen stage instead of rerunning the whole pipeline from the beginning each time.

## Terminology conventions

- `structured script`: the English name for `结构化剧本`
- `unified voice candidate pool`: the English name for `统一音色候选池`
- `effective profile`: the English name for `生效画像`, meaning the clone voice profile that really participates in casting
- `paid clone`: the English name for `付费 clone`, meaning the real Step voice cloning API call
- `intermediate artifacts`: the English name for `中间产物`
- `human review` / `manual confirmation`: the English name for `人工确认`
- `ready voice`: the English name for `ready 音色`, meaning a voice that can already enter downstream TTS directly

## LLM replacement boundary

One important clarification is that not every part of the skill is meant to be replaceable.

- replaceable by default: long-text structuring, role extraction, casting reasoning, and related LLM understanding tasks
- these tasks currently default to `step-3.5`, using `https://api.stepfun.com/step_plan/v1`
- not replaced by default: `step-audio-r1.1` audio analysis, Step official voice sync, Step voice cloning, and `stepaudio-2.5-tts` synthesis
- in other words, `audiobook` is currently designed as Step-native audio capability plus a configurable reasoning layer, not as a completely provider-agnostic abstraction for every feature

## Default paths

The current default directory conventions are:

```bash
WORKSPACE_ROOT=~/.openclaw/workspace
SKILL_ROOT=$WORKSPACE_ROOT/skills/audiobook
EXAMPLES_ROOT=$SKILL_ROOT/examples
VOICE_LIBRARY=$WORKSPACE_ROOT/audiobook-library/voice-library.yaml
LIBRARY_ROOT=$WORKSPACE_ROOT/audiobook-library
STORY_ROOT=$WORKSPACE_ROOT/audiobook-stories          # recommended place for raw txt / yaml / json
RUN_ROOT=$WORKSPACE_ROOT/runs/audiobook
```

All command examples below assume you are running from `"$SKILL_ROOT"`, so the recommended first step is:

```bash
cd "$SKILL_ROOT"
```

If you do not want to change directories, replace `scripts/<name>.py` in the examples with absolute paths.

Key locations:

- voice library entry point: `$VOICE_LIBRARY`
- drop zone for user reference audio waiting to be analyzed: `$LIBRARY_ROOT/voices/inbox/`
- long-lived reference audio directory: `$LIBRARY_ROOT/voices/references/<asset_id>/`
- voice analysis, cache, and unified voice candidate pool: `$LIBRARY_ROOT/.audiobook/`
- per-book intermediate and final outputs: `$RUN_ROOT/<slug>/`
- lightweight reference examples: `$EXAMPLES_ROOT/`

Recommended but not mandatory: keep raw story files under `~/.openclaw/workspace/audiobook-stories/`. The scripts accept any absolute path, but a shared story directory makes both human and programmatic management easier.

## Before you run

Before executing any main workflow, make sure that:

- `STEP_API_KEY` is available in the environment
- `ffmpeg` is installed
- `ffprobe` is installed if you want final export or duration probing

## Security and billing notes

- `audiobook` should now be treated as an explicitly invoked skill, not something you rely on for implicit injection; it is a workflow skill that reads and writes local files and may call external APIs.
- By default, audio analysis, official voice sync, voice cloning, and TTS synthesis all call Step endpoints. If you override `voice-library.yaml -> llm.*.base_url`, the long-text reasoning layer will call the compatible LLM endpoint that you configured.
- Prefer a test key, a limited-scope key, or at least rotate the key after first validation. If you do not fully trust the current setup, run the workflow in a sandbox or isolated environment first.
- Install `ffmpeg` and `ffprobe` only from trusted sources.
- The only step that may trigger paid billing is `clone_selected_voices.py`; and now, besides `selected_for_clone=true`, it also requires an explicit `--confirm-paid-action` flag before a real clone is executed.
- `run_audiobook.py` only performs a clone preview with `--dry-run` by default and does not automatically perform the real paid clone for you.
- If you are auditing the skill, or want to verify the default endpoints and environment-variable usage, read `references/security.en.md`.

If `voice-library.yaml` does not exist yet, initialize it from the template:

```bash
mkdir -p "$LIBRARY_ROOT"
cp       "$SKILL_ROOT/assets/voice-library.template.yaml"       "$VOICE_LIBRARY"
```

If you also want to see a commented review skeleton before the first ingest, initialize this too:

```bash
cp       "$SKILL_ROOT/assets/voice-reviews.template.yaml"       "$LIBRARY_ROOT/voice-reviews.yaml"
```

## Minimal examples

The `examples/` directory now contains seven lightweight examples that are useful for understanding the data shapes before copying them into your own workspace:

- `examples/story-minimal.txt`: the smallest raw story sample
- `examples/story-minimal.structured-script.yaml`: the corresponding structured script
- `examples/voice-library.minimal.yaml`: the smallest voice library configuration example
- `examples/voice-reviews.minimal.yaml`: the smallest human review example
- `examples/story-minimal.casting-plan.yaml`: the smallest effective casting result that can continue downstream
- `examples/story-minimal.tts-requests.json`: the smallest replayable TTS request example
- `examples/story-minimal.script-runtime.json`: the normalized companion generated by `build_tts_requests.py`

Recommended usage:

- for real initialization, copy `assets/*.template.yaml`
- `examples/*minimal*` are better for understanding the structure, copying partial sections, or aligning fields in another program
- path fields inside `examples/*.json` and `*.yaml` now use `$EXAMPLES_ROOT` / `$RUN_ROOT` placeholders instead of machine-local absolute paths
- do not use `examples/voice-library.minimal.yaml` as your long-lived production library file

## Most common entry point

To run the full main workflow in one go, start with:

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --story-input /absolute/path/story.txt
```

This command will try to:

1. refresh the official voice cache
2. process new audio from `--voice-input` or `--process-inbox`
3. generate `structured-script` when the input is `txt`
4. generate `casting-review`, `casting-plan`, and `clone-review`
5. preview which clone candidates are worth a paid clone
6. continue into `tts-requests -> synthesize -> finalize` only when role and clone state allow it

If you prefer step-by-step control, see `references/workflows.md` and its English companion `references/workflows.en.md`.

## Recommended command sequence

### 1. Voice library sync and audio analysis

Analyze one audio file:

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --input /absolute/path/reference-audio.m4a
```

Process the inbox in batch as part of a run:

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --story-input /absolute/path/story.txt --process-inbox
```

Process only the inbox and do not enter the story workflow:

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --process-inbox --downstream-mode off
```

Refresh official voices only:

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --refresh-official-only
```

Quickly list clone voices that still need manual confirmation:

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```

### 2. Raw story to structured script

```bash
python3 scripts/generate_structured_script.py --library "$VOICE_LIBRARY" --input /absolute/path/story.txt
```

Default output:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml
```

### 3. Generate casting outputs

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /absolute/path/structured-script.yaml
```

Default outputs:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-plan.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.clone-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.role-profiles.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.casting-selection.json`

### 4. Build replayable TTS requests

```bash
python3 scripts/build_tts_requests.py --input /absolute/path/structured-script.yaml
```

Default outputs:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.tts-requests.json`

### 5. Synthesize segment audio

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json
```

Default output:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.segments/`

### 6. Export the full book or a preview

```bash
python3 scripts/finalize_audiobook.py --input /absolute/path/<base>.tts-requests.json
```

Default full-book output:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.audiobook.wav
```

If you change `response_format` to `mp3`, `flac`, or `opus`, the extension follows that value. The default is still `wav`.

If you export only selected segments, the output becomes:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.preview-<segments>.<response_format>
```

## How to inspect intermediate artifacts

Every book run has one unified manifest:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.artifacts.json
```

It lists:

- source text and structured script
- casting review files and effective casting outputs
- library-side `voice-reviews`, `effective-voice-library`, `voice-candidate-pool`, and `official-voices-cache`
- `script-runtime` and `tts-requests`
- `segments/`
- the latest export and final output

For human inspection:

```bash
python3 scripts/list_story_artifacts.py --manifest /absolute/path/<base>.artifacts.json --level review --pretty
```

For programmatic callers: read `artifacts.json` directly instead of hard-coding path rules.

If you only want to inspect which clone descriptions are still pending manual confirmation, use:

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```

## Which files may be edited and which should not be edited directly

Recommended manual edit targets:

- `voice-reviews.yaml`
- `*.casting-review.yaml`
- `*.clone-review.yaml`
- `*.structured-script.yaml`
- `*.tts-requests.json`

Generated files that should usually not be edited directly:

- `.audiobook/effective-voice-library.yaml`
- `.audiobook/voice-candidate-pool.yaml`
- `.audiobook/official-voices-cache.json`
- `*.casting-plan.yaml` unless you really know what you are doing
- `*.script-runtime.json`
- `*.artifacts.json`

For rerun commands after manual edits, see `references/editing.md` or `references/editing.en.md`.

## The two `.audiobook/` directories

This is the most common source of confusion:

- `~/.openclaw/workspace/audiobook-library/.audiobook/`: generated files for the voice library side
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/`: trace and debug files for one specific story run

The former serves the shared voice library. The latter serves one book run only.

## Paid boundary

`clone_selected_voices.py` is the only step that can trigger paid cloning. The default workflow only:

- analyzes reference audio
- generates clone candidates
- waits for confirmation in `clone-review.yaml`

Before the real paid call, always run:

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
```

For real execution, an extra confirmation flag is now required:

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

## Machine-readable interfaces

These scripts all print JSON to stdout and are suitable for programmatic calling:

- `sync_voice_library.py`
- `generate_structured_script.py`
- `recommend_casting.py`
- `build_tts_requests.py`
- `synthesize_tts_requests.py`
- `finalize_audiobook.py`
- `run_audiobook.py`

For programs, the safest pattern is:

1. call the main script and read its stdout JSON
2. read `artifacts.json` for the full file inventory

## Reference Index / 参考文档索引

If you are a human Chinese reader, start with the Chinese documents. If you are an English-speaking agent or program, go directly to the English companion files.

- Full workflow / 完整执行顺序: Chinese `references/workflows.md` | English `references/workflows.en.md`
- Voice library structure / 音色库结构与字段: Chinese `references/voice-library.md` | English `references/voice-library.en.md`
- Structured script format / 结构化剧本格式: Chinese `references/script-format.md` | English `references/script-format.en.md`
- Casting rules and outputs / 选角规则与输出: Chinese `references/casting.md` | English `references/casting.en.md`
- Synthesis and export / TTS、replay 与最终导出: Chinese `references/synthesis.md` | English `references/synthesis.en.md`
- Manual editing and reruns / 人工修改与重跑: Chinese `references/editing.md` | English `references/editing.en.md`
- Security and external access / 安全与外部访问: Chinese `references/security.md` | English `references/security.en.md`

If you only want the fastest reading path, use this order:

1. Start with `references/workflows.en.md` for the end-to-end chain
2. Read `references/voice-library.en.md` when you need voice asset maintenance
3. Read `references/editing.en.md` when you need to modify intermediate artifacts by hand
