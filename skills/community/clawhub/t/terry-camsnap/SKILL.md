---
name: camsnap
description: Take camera snapshots and save them to disk. Use when the user asks to take a photo, capture an image from webcam, or take a snapshot.
allowed-tools: Bash
argument-hint: "[output_path] [--preview]"
---
Take a snapshot from the default webcam using the camsnap utility.

## Usage
/camsnap [output_path] [--preview] [--output-dir DIR]

If no output path is provided, the snapshot will be saved to the `./snapshots/` directory with a timestamp filename.

## Steps
1. Run the snapshot script:
```bash
python3 ~/.openclaw/workspace/src/camsnap.py {{ $ARGUMENTS }}
```
2. Confirm the snapshot was saved successfully and return the file path.

## Notes
- The script discards the first few warm-up frames to avoid underexposed captures.
- Output paths are validated against path-traversal; only allowed directories are writable.
- Use `--preview` only in environments with a display (headless servers will fail).
