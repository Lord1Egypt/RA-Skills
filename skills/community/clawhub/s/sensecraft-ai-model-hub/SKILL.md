---
name: sensecraft-ai-model-hub
description: Connect OpenClaw to the SenseCraft public model library to search, inspect, export, and download AI vision models for software and edge AI workflows.
---

# SenseCraft AI Model Hub

## Overview

Use this skill to treat the SenseCraft public model library as a practical source of pretrained vision models for OpenClaw.

The core workflow is fixed:

1. `list_model` to discover model IDs
2. `view_model` to resolve a model into full metadata and `file_url`
3. download from `file_url`

Assume:
- base URL: `https://sensecraft.seeed.cc/aiserverapi`
- default `appid=131`
- public endpoints are anonymous unless evidence shows otherwise
- list responses do **not** include direct download URLs
- the actual download URL is `data.file_url` from `view_model`

## Use bundled script first

Prefer the bundled script for repeatable work instead of rebuilding curl pipelines every time.

Commands:
- `scripts/sensecraft_models.py list` — list one page of public models
- `scripts/sensecraft_models.py view <id>` — show one model detail with URL hints
- `scripts/sensecraft_models.py index` — crawl all pages, fetch detail rows, summarize, and export an index
- `scripts/sensecraft_models.py download` — download one or more model files and emit a manifest
- `scripts/sensecraft_webcam_person_demo.py` — run a local webcam person-detection demo with a downloaded SenseCraft TFLite model

## Good default responses

### Find models

Use when the request is like:
- “search SenseCraft for person models”
- “list classification models”
- “show models for uniform_type 32”

Prefer:

```bash
python3 scripts/sensecraft_models.py list --search person --length 30
python3 scripts/sensecraft_models.py list --task 1 --uniform-type 32 --length 50
```

### Inspect one model

Use when the request is like:
- “what is model 60768?”
- “give me the download link for this model ID”

Prefer:

```bash
python3 scripts/sensecraft_models.py view 60768
```

This returns annotated detail including:
- `file_url`
- filename hint
- extension hint
- whether the URL looks like a `.tflite` artifact

### Export a searchable full index

Use when the request is like:
- “dump the whole public model catalog”
- “make me a JSON/CSV index”
- “summarize what model types are in the library”

Prefer:

```bash
python3 scripts/sensecraft_models.py index --format json --output ./sensecraft-models.json --summary --summary-json ./sensecraft-summary.json
python3 scripts/sensecraft_models.py index --format csv --output ./sensecraft-models.csv
```

Use filters to reduce scope when possible:

```bash
python3 scripts/sensecraft_models.py index --task 1 --uniform-type 32 --format json --output ./filtered.json
python3 scripts/sensecraft_models.py index --model-format 2 --format table --summary
```

### Download models

Use when the request is like:
- “download model 60768”
- “download these several models”
- “download everything from this exported index”

Prefer:

```bash
python3 scripts/sensecraft_models.py download --model-id 60768 --output-dir ./downloads --manifest ./downloaded.json --summary
python3 scripts/sensecraft_models.py download --from-index ./sensecraft-models.json --output-dir ./downloads --manifest ./downloaded.json --summary-json ./downloaded-summary.json
```

### Run a local webcam demo

Use when the request is like:
- “download a model and show me live inference from my webcam”
- “make a local Python script that opens the camera and draws boxes”
- “validate a SenseCraft model on my laptop before deployment”

Prefer this path for a minimal local demo:

1. Run `scripts/setup_local_demo_env.sh`
2. Let `scripts/run_local_person_demo.sh` auto-download model `60080` into `./models` if missing
3. Run the launcher script

Example:

```bash
bash scripts/setup_local_demo_env.sh
bash scripts/run_local_person_demo.sh
```

Helpful variants:

```bash
bash scripts/run_local_person_demo.sh --debug
bash scripts/run_local_person_demo.sh --camera 1
python3 scripts/sensecraft_webcam_person_demo.py --image ./sample.png --save ./annotated.png
```

Read `references/local-webcam-demo.md` before changing the postprocess logic or if the user reports bad boxes.
Keep local demo assets under the skill root with this layout:
- `models/` — downloaded TFLite artifacts and manifests
- `captures/` — saved annotated frames from live demos
- `scripts/` — setup, launcher, and Python entrypoints

## Output requirements

When summarizing models for the user, include as many of these as available:
- `id`
- `name`
- `description`
- `task`
- `uniform_types`
- `model_format`
- `file_url`
- filename or extension hint if relevant
- whether the artifact *looks like* `.tflite`

When recommending a model for OpenClaw integration, also include:
- expected purpose of the model
- uncertainty about task mapping or format
- whether the artifact should be inspected after download before claiming TFLite compatibility

## Field interpretation rule

Do not invent semantic names for `task`, `uniform_type`, or `model_format` unless the mapping is documented.

Safe behavior:
- report raw numeric values exactly
- compare/group/filter by those raw values
- if the user wants human-readable meanings, state that the meaning is not confirmed and ask for or look for authoritative mapping

Read `references/field-mapping-notes.md` if the user asks what those numeric values mean.

## API behavior

### List models

Call:

```text
GET /model/list_model
```

Typical parameters:
- `appid=131`
- `length`
- `page`
- `search`
- `uniform_type`
- repeated `task`

Returned list items typically include:
- `id`
- `name`
- `description`
- `uniform_types`
- `task`

Do not expect `file_url` here.

### View model detail

Call:

```text
GET /model/view_model?appid=131&model_id=<ID>
```

Read from the detail response:
- `data.id`
- `data.name`
- `data.description`
- `data.task`
- `data.uniform_types`
- `data.model_format`
- `data.file_url`

`data.file_url` is the real download link.

### Download model

Download with redirect following enabled.

Equivalent shell shape:

```bash
curl -L 'FILE_URL' -o output.bin
```

## Safety and reliability rules

- Treat the library as public, but do not assume the API contract is perfectly stable.
- Use small delays during bulk detail fetches or downloads; avoid aggressive parallel floods.
- Retry transient request failures a small number of times.
- If `view_model` fails for a specific ID, skip it and record the failure during bulk crawls.
- Preserve original metadata in exported JSON when possible.
- Do not claim a model is definitely TFLite only from category or filename hints.
- After download, inspect the artifact if exact runtime compatibility matters.
- Do not guess YOLO-family fused-output decoding from generic tutorials when SSCMA-Micro or model-specific evidence is available.
- For macOS local demos, warn that webcam access may fail until the terminal app has camera permission.

## References

- `references/sensecraft-api.md` — API contract and workflow notes
- `references/field-mapping-notes.md` — guidance for unknown numeric mappings
- `references/integration-notes.md` — post-download validation and TFLite integration checks
- `references/local-webcam-demo.md` — proven local webcam demo flow, package choices, and decoding caveats

## Decision rule

If the user wants source discovery, indexing, filtering, URL resolution, or downloading from SenseCraft, stay inside this skill.

If the user wants broader model selection across multiple ecosystems, use this skill to retrieve SenseCraft candidates first, then compare them against wider TFLite integration constraints.
