# RapidOCR Skill

ClawHub skill for local image OCR with RapidOCR.

## Files

- `SKILL.md`: ClawHub skill definition
- `run_rapidocr.js`: wrapper that extracts a local image path and launches Python
- `run_rapidocr.py`: Python OCR entrypoint
- `_meta.json`: local publish metadata

## Features

- Local image OCR for `png`, `jpg`, `jpeg`, `webp`, `bmp`, `tif`, `tiff`
- Natural-language input parsing
- Plain text output
- JSON output with `text`, `lines`, `boxes`, `scores`, `source`
- No remote URL download

## Dependencies

Install RapidOCR into the interpreter you want to use:

```bash
python -m pip install rapidocr onnxruntime
```

The wrapper auto-discovers `python3`, `python`, or `py`.

For local testing, you can override the interpreter:

```bash
RAPIDOCR_PYTHON=/path/to/python node ./run_rapidocr.js "/absolute/path/to/demo.png" --json
```

## Publish

Recommended ClawHub slug: `rapidocr`

Typical publish flow:

```bash
clawhub skill publish . --slug rapidocr --version 1.0.3
```
