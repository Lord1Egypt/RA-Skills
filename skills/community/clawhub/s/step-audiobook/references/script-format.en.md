# Audiobook Script Format

Language switch: you are reading English | [中文说明](./script-format.md)

Downstream steps in `audiobook` only accept a structured script. A raw story `txt` must first be converted into structured YAML by `generate_structured_script.py`.

## Reading Guide / 阅读导航

- Want the root overview and global conventions? Go back to `../SKILL.en.md`
- Want the full execution order? Read `./workflows.en.md`
- Want to see how casting uses the structured script? Read `./casting.en.md`
- Want to see how downstream TTS requests are built from the script? Read `./synthesis.en.md`

If this is your first time converting raw text into a structured script, the recommended order is:

1. `../SKILL.en.md`
2. `./workflows.en.md`
3. this file `./script-format.en.md`
4. then continue into `./casting.en.md`

## Supported input types

The workflow currently accepts three story input shapes:

1. Raw `txt`
2. Structured `yaml`
3. Structured `json`

In practice:

- `txt`: run `generate_structured_script.py` first
- `yaml/json`: you can go directly into `recommend_casting.py` or `build_tts_requests.py`

Additional notes:

- `txt -> structured-script` currently defaults to `step-3.5`
- The default `step-3.5` call uses Step's `step_plan` reasoning endpoint
- The default endpoint is `https://api.stepfun.com/step_plan/v1`
- If you change `provider / model / base_url` under `voice-library.yaml -> llm.tasks.script_generation`, this step can switch to another compatible LLM

## Output paths for raw `txt`

```bash
python3 scripts/generate_structured_script.py --input /absolute/path/story.txt
```

Default outputs:

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.generation.json`

The first file is the structured script that downstream steps actually use. The second file is the generation archive.

`structured-script.generation.json` now serves two purposes beyond archiving:

- it stores the full trace for overview / chunk / finalization
- it acts as the chunk-level resume checkpoint when `txt -> structured-script` is interrupted

In other words, if a long story fails on chunk `N`, you can fix the network or parameters and rerun the same `generate_structured_script.py` command. By default, it will try to resume from the compatible checkpoint instead of regenerating every chunk from scratch.

If you pass an existing structured `yaml/json` directly to `run_audiobook.py --story-input`, the script first copies that file into `~/.openclaw/workspace/runs/audiobook/<slug>/`, so the later `casting-plan`, `tts-requests`, and `artifacts.json` stay together under the same run directory.

## Minimal script examples in `examples/`

The skill ships with two script-related reference files:

- `examples/story-minimal.txt`
- `examples/story-minimal.structured-script.yaml`

They describe the same tiny scene: an alley after rain, one narrator, and two speaking characters.

Recommended usage:

- Want to see the target shape of `txt -> structured-script`? Read these two files side by side.
- Want to hand-write your own structured script? Copy `story-minimal.structured-script.yaml` and edit it.
- Want to align fields for a program? Emit the same `characters + segments` structure as the example YAML.

These are reference examples, not the only runtime source. For real runs, it is recommended to place your own story files under `~/.openclaw/workspace/audiobook-stories/`.

## Chunking and timeout protection for long text

`generate_structured_script.py` now applies three layers of protection by default:

1. split the story into base chunks by paragraphs and sentences
2. if chapter-like headings are detected, split by chapter first and only then chunk within each section
3. send every LLM request with its own `timeout_seconds`

Default behavior:

- automatic resume after interruption
- chapter-aware splitting enabled
- single-request HTTP timeout defaults to 180 seconds

If you explicitly do not want checkpoint reuse, add:

```bash
python3 scripts/generate_structured_script.py --input /absolute/path/story.txt --no-resume
```

## Supported structured script shapes

`build_tts_requests.py` supports two shapes:

1. `characters + dialogues`
2. `characters + segments`

## Shape A: `characters + dialogues`

This is the lowest-cost format if you want to hand-write it.

```yaml
title: Sample
global_instruction: scene=city night street | narration=neutral and clear | dialogue=natural and restrained
characters:
  - id: narrator
    name: Narrator
    instruction: Neutral and clear narration
  - id: hero
    name: Hero
    instruction: Adult male, natural and restrained delivery

dialogues:
  - speaker: narrator
    text: He stopped and looked into the deeper part of the alley.
  - speaker: hero
    text: "(lowering his voice) Something is wrong."
```

Minimum requirements:

- `characters[].id` is required
- `dialogues[].speaker` is required
- `dialogues[].text` is required

Automatic behavior:

- text starting with `( ... )` is split into `inline_instruction + clean_text`
- `speaker=narrator` defaults to `delivery_mode=narration`
- other speakers default to `delivery_mode=dialogue`

## Shape B: `characters + segments`

Use this when you want explicit runtime-level control.

```yaml
title: Sample
global_instruction: scene=suspenseful night road | narration=neutral and clear | dialogue=natural and restrained
characters:
  - id: narrator
    name: Narrator
    instruction: Neutral and clear narration
  - id: hero
    name: Hero
    instruction: Adult male, natural and restrained delivery

segments:
  - index: 0
    speaker: narrator
    raw_text: He stopped and looked into the deeper part of the alley.
    delivery_mode: narration
  - index: 1
    speaker: hero
    raw_text: "(lowering his voice) Something is wrong."
    delivery_mode: inner_monologue
    scene_instruction: Quiet alley entrance, close whispering feel
```

Supported fields:

- `speaker`: required
- `raw_text / text / tts_input_text / clean_text`: provide at least one
- `delivery_mode`: optional, supported values are
  - `narration`
  - `dialogue`
  - `inner_monologue`
- `inline_instruction`: optional
- `scene_instruction`: optional
- `character_instruction`: optional
- `metadata`: optional object

## Normalized runtime output

Whether you provide `dialogues` or `segments`, the pipeline first normalizes everything into:

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json
```

This runtime file is generated automatically and is not intended for long-term manual maintenance. Its job is to:

- normalize `speaker / character_name / delivery_mode`
- split `raw_text / clean_text / inline_instruction`
- fill in placeholder character info when needed

## Recommended style for `global_instruction`

It is best to keep global reading requirements stable and reusable, for example:

```text
scene=city night street | narration=neutral and clear | dialogue=natural and restrained
```

Not recommended:

- a full plot summary
- instructions tightly bound to one local emotional beat
- descriptions that conflict with a character's long-term voice identity

## Advice for programmatic callers

If you are a program instead of a human editor, the recommended pattern is:

1. feed `txt` into `generate_structured_script.py` and read its stdout JSON
2. read the `output_path` it returns
3. keep using that generated `structured-script.yaml` for casting and TTS

This avoids having to derive `<slug>` and `<base>` yourself.
