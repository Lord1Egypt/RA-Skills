---
name: camsnap
description: Take camera snapshots and save them to disk. Use when the user asks to take a photo, capture an image from webcam, or take a snapshot.
allowed-tools: Bash
argument-hint: "[output_path] [--preview]"
---
Take a snapshot from the default webcam using the camsnap utility.

## Usage
/camsnap [output_path] [--preview]

If no output path is provided, the snapshot will be saved to the `./snapshots/` directory with a timestamp filename.

## Steps
1. Run the snapshot script:
```bash
python {{SKILL_DIR}}/src/camsnap.py {{ $ARGUMENTS }}
```
2. Confirm the snapshot was saved successfully and return the file path.
