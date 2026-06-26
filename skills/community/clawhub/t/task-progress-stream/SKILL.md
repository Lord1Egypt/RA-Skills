---
name: task-progress-stream
description: Stream long-running task progress into the OpenClaw chat UI.
version: 0.1.0
author: LiyooYin
license: MIT
tags:
  - monitoring
  - progress
  - training
---

# task-progress-stream

Use this skill when the user wants **real-time progress updates inside the OpenClaw chat UI** for a long-running task such as:

- model training
- evaluation
- inference
- data preprocessing
- long shell jobs
- benchmark runs

It works in two modes:

1. **run**  
   Start a command, capture stdout/stderr, parse common metrics, and periodically inject progress summaries into chat.

2. **tail**  
   Monitor an existing log file and periodically inject parsed progress summaries into chat.

## What it extracts

It tries to recognize common fields from logs:

- epoch / max_epoch
- step / max_step
- loss
- learning rate
- validation metric
- best metric
- ETA
- speed

## Typical usage

### Start a training job and stream progress into chat

```bash
node ./scripts/task_progress_stream.js run \
  --session main \
  --label train \
  --cwd /path/to/project \
  --cmd "python src/train.py --config configs/train.yaml" \
  --interval-sec 20
