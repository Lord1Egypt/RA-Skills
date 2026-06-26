# Audiobook Synthesis

Language switch: you are reading English | [中文说明](./synthesis.md)

This document explains the downstream synthesis chain in `audiobook`: `build_tts_requests.py -> synthesize_tts_requests.py -> finalize_audiobook.py`.

## Reading Guide / 阅读导航

- Want the root overview and global conventions? Go back to `../SKILL.en.md`
- Want the full execution order? Read `./workflows.en.md`
- Want to understand structured script inputs and casting sources first? Read `./script-format.en.md` and `./casting.en.md`
- Want to manually edit requests and rerun? Read `./editing.en.md`

If this is your first time focusing on downstream synthesis, the recommended order is:

1. `../SKILL.en.md`
2. `./workflows.en.md`
3. `./casting.en.md`
4. this file `./synthesis.en.md`

## Path overview

By default, downstream outputs are stored under:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/
```

Key files:

- `<base>.script-runtime.json`
- `<base>.tts-requests.json`
- `<base>.segments/`
- `<base>.audiobook.<response_format>`
- `<base>.preview-<segments>.<response_format>`

The default `response_format` is `wav`, so `.wav` is still the most common output file extension.

## Step 1: build the TTS request list

```bash
python3 scripts/build_tts_requests.py --input /absolute/path/structured-script.yaml
```

## Minimal downstream examples in `examples/`

If you want to inspect the smallest possible downstream chain first, read these three files:

- `examples/story-minimal.casting-plan.yaml`
- `examples/story-minimal.tts-requests.json`
- `examples/story-minimal.script-runtime.json`

Together with `story-minimal.structured-script.yaml`, they describe the same small scene. Their roles are:

- `story-minimal.structured-script.yaml`: human-maintained structured script
- `story-minimal.casting-plan.yaml`: every role already has one selected `ready` voice
- `story-minimal.script-runtime.json`: normalized intermediate data produced by `build_tts_requests.py`
- `story-minimal.tts-requests.json`: the replayable request list that can go directly into `synthesize_tts_requests.py`

This example set intentionally uses only official ready voices so that it is easier to see:

- which fields a minimal `casting-plan` must contain
- what `instruction / input_text / voice_id` finally look like in `tts-requests.json`
- how `script-runtime` and `tts-requests` divide responsibilities

The builder reads:

- the structured script
- the same-name `*.casting-plan.yaml` in the same directory

It writes:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.tts-requests.json`

It also records the suggested final book output path in:

- `source.output_path`

That suggested path uses the same extension as `common_request.response_format`.

### Default model and extra parameters

Default model:

- `stepaudio-2.5-tts`

Book-level parameters that can be passed through:

- `--volume`
- `--tone-map`
- `--pronunciation-map-file`

These are written into:

- `common_request.extra_body`

## Core fields in `tts-requests.json`

This file is the main entry point for replay and partial manual fixes.

Most important top-level fields:

- `source`: input file metadata and the suggested output path
- `common_request`: model, sample rate, response format, and book-level `extra_body`
- `segments[]`: the real TTS request for each segment

Most important fields inside `segments[]`:

- `index`
- `speaker`
- `voice_id`
- `input_text`
- `instruction`
- `status`
- `audio_path`

## Split of responsibility between `instruction` and `input_text`

When calling StepAudio 2.5 TTS downstream, the default convention is:

- `input_text`: the text that should actually be spoken
- `instruction`: stable control hints that apply to the whole segment
- parentheses at the start of phrases inside `input_text`: fast inline changes for sub-phrases or immediate turns

Recommended style:

```text
instruction:
restrained emotion, medium to slightly slow pace, pressure rising only a little

input_text:
(holding back anger first) So you finally came back? (suddenly disappointed) Forget it. I should have expected this.
```

Current implementation limits:

- `input_text` is recommended to stay within 1000 characters
- `instruction` is recommended to stay within 200 characters
- `voice_label` is not supported

## Step 2: synthesize segment audio

```bash
python3 scripts/synthesize_tts_requests.py --input /absolute/path/<base>.tts-requests.json
```

Default behavior:

- call `POST /v1/audio/speech`
- write each segment audio file into `<base>.segments/`
- write back `segments[].status / audio_path / duration_ms`

Default output directory:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.segments/
```

### Replay behavior

Segments that already succeeded and still have a local audio file are skipped by default.

Common flags:

- only synthesize some segments: `--segments 1,3-5`
- rerun only failed segments: `--only-failed`
- force overwrite successful segments: `--force`
- preview only without a real API call: `--dry-run`

### Instruction sending mode

Default: `--request-mode auto`

Default behavior:

- first try to send `instruction` as a dedicated field
- if the API explicitly returns `instruction is not supported`, fall back to merging the control text into `input_text`

## Step 3: export the full book or a preview

Export the full book:

```bash
python3 scripts/finalize_audiobook.py --input /absolute/path/<base>.tts-requests.json
```

Default full-book output:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.audiobook.<response_format>
```

Export a preview clip:

```bash
python3 scripts/finalize_audiobook.py --input /absolute/path/<base>.tts-requests.json --segments 1,3-5
```

Default preview output:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.preview-1_3-5.<response_format>
```

During export, the script will:

- verify that every selected segment has already been synthesized successfully
- use `ffmpeg` to concatenate audio from `<base>.segments/`
- write back `tts-requests.json -> latest_export`
- also write `final_output` when exporting the whole book

## Recommended read path for programs

If another program wants to take over the downstream chain, the recommended sequence is:

1. run `build_tts_requests.py` and read `output_path` from stdout JSON
2. run `synthesize_tts_requests.py` and inspect `updated_segments`
3. run `finalize_audiobook.py` and read its `output_path`
4. read `<base>.artifacts.json` for the full file inventory

This is safer than reconstructing paths purely from file-name conventions.

## Conditions that block downstream execution

`build_tts_requests.py` fails early in the following cases:

- `casting-plan` is missing a role
- a role has no `selected_voice_id`
- a role has `selected_status != ready`
- a clone-dependent role is still waiting for paid cloning

This is intentional. It is better to fail early than to silently produce a half-broken request list.
