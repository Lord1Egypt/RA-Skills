---
name: rapidocr
description: Extract text from local image files with RapidOCR. Use when the user wants OCR on a JPG, PNG, WEBP, BMP, or TIFF image and may want plain text or JSON output.
version: 1.0.3
homepage: https://rapidai.github.io/RapidOCRDocs
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["node"],"anyBins":["python3","python","py"]},"homepage":"https://rapidai.github.io/RapidOCRDocs","emoji":"🔎","os":["macos","linux","windows"]}}
---

# RapidOCR

ClawHub skill for local image OCR with RapidOCR.

## When to use

- The user wants text extracted from a local image file.
- The input is a local `png`, `jpg`, `jpeg`, `webp`, `bmp`, `tif`, or `tiff` file.
- The user wants either plain text output or structured JSON output.

## Do not use

- Remote image URLs.
- PDF OCR.
- Relative paths when an absolute path is available.

## Execution

1. Pass the user's original request directly to the wrapper script.
2. Run `node "{baseDir}/run_rapidocr.js" "{{input}}"`.
3. If the host does not substitute `{baseDir}`, resolve the directory containing this `SKILL.md` and run the sibling file `run_rapidocr.js` from there.
4. For local testing, `RAPIDOCR_PYTHON=/path/to/python` can be used to force a specific interpreter.
5. Otherwise the wrapper auto-discovers `python3`, `python`, or `py`.
6. If the user asks for JSON, preserve the script's JSON output exactly.
7. If dependencies are missing, tell the user to run `<python> -m pip install rapidocr onnxruntime` with the interpreter they intend to use.
8. Publish this folder to ClawHub with slug `rapidocr`.

## Behavior

- The wrapper extracts a local image path from natural language, JSON-like input, or a direct path.
- The wrapper only reads existing local image files.
- Default output is plain text, one recognized line per line.
- JSON mode returns `text`, `lines`, `boxes`, `scores`, and `source`.
