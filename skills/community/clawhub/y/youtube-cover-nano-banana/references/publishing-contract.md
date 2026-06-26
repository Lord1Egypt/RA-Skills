# Publishing Contract

## Purpose

Use `scripts/create_thumbnail.py` as the single release entrypoint for Clawhub-style integrations.

## Command

```bash
python3 scripts/create_thumbnail.py \
  --copy "Man fights tiger" \
  --stdout-json
```

Add `--generate-image` when the caller wants the PNG rendered after the plan is created.

Run a local contract smoke test before publishing:

```bash
python3 scripts/selftest.py
```

## Inputs

### Required

- `--copy`: raw source copy, title, hook, or concept

### Optional

- `--audience`: target audience
- `--style`: requested visual style
- `--brand-colors`: brand palette constraints
- `--must-include`: required visual elements
- `--avoid`: banned elements
- `--generate-image`: render PNG after plan creation
- `--output-json`: write the final result object to disk
- `--image-output`: PNG output path
- `--stdout-json`: print the final result object to stdout

## Environment

- `GEMINI_API_KEY` or `GOOGLE_API_KEY` must be set
- `python3` must be available on `PATH`

## Success Shape

The command returns exit code `0` and writes a JSON object with this shape:

```json
{
  "ok": true,
  "input": {
    "copy": "Man fights tiger",
    "audience": null,
    "style": null,
    "brand_colors": null,
    "must_include": null,
    "avoid": null,
    "generate_image": false,
    "text_model": "gemini-2.5-flash",
    "image_model": "gemini-2.5-flash-image"
  },
  "plan": {
    "angle": "Single-sentence thumbnail angle",
    "overlay_text": "Short headline",
    "prompt": "Final English prompt",
    "generation_notes": "One short note"
  },
  "artifacts": {
    "plan_json": "outputs/thumbnail-plan.json",
    "image_png": null,
    "image_metadata_json": null
  },
  "error": null
}
```

## Failure Shape

The command returns a non-zero exit code and still writes a JSON object:

```json
{
  "ok": false,
  "input": {},
  "plan": null,
  "artifacts": {
    "plan_json": "outputs/thumbnail-plan.json",
    "image_png": null,
    "image_metadata_json": null
  },
  "error": {
    "code": "invalid_arguments | runtime_error",
    "message": "Readable failure reason"
  }
}
```

## Exit Codes

- `0`: success
- `1`: runtime failure such as API failure or invalid model response
- `2`: invalid arguments
