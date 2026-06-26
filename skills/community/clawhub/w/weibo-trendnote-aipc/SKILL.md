---
name: weibo-trendnote-aipc
description: >
  Fetch Weibo realtime hot search rankings, summarize trending topics with a local model,
  and append the hot list plus digest to an Obsidian note.
  Supports one-time runs and optional recurring cron setup on Windows.
user-invocable: true
metadata: {"openclaw":{"os":["win32"],"requires":{"anyBins":["python","py"],"bins":["openclaw"]},"homepage":"https://docs.openclaw.ai/tools/skills"}}
---

# Weibo TrendNote AI PC

Use this skill to fetch current Weibo hot trends, summarize them locally, and append the result to Obsidian.

## What it does
- Fetches the current Weibo hot search list.
- Summarizes the latest hot topics with a local summarize CLI / local model flow.
- Appends the hot list and summary to an Obsidian note.
- Can optionally register recurring cron jobs, but only when the user explicitly asks for scheduled automation.

## Safety and side effects
- This skill writes local state files under `C:\Users\Intel\.openclaw\state\weibo_hot`.
- This skill appends content to an Obsidian note.
- Optional cron setup creates persistent scheduled jobs in OpenClaw.
- Do not install recurring cron jobs unless the user explicitly asks for ongoing automation.

## Recommended commands

### One-time run
Use this for a normal fetch → summarize → write pass:

    exec: python "{baseDir}/skill_runner.py" once

To force a full run even when the hot list has not changed:

    exec: python "{baseDir}/skill_runner.py" once --force

### Optional recurring automation
Only use this after the user explicitly asks to enable scheduled runs:

    exec: python "{baseDir}/skill_runner.py" install-crons

## Notes
- This skill is Windows-only.
- The runner loads optional values from `C:\Users\Intel\.openclaw\state\weibo_hot\env.ps1` when present.
- If `env.ps1` is absent, the bundled scripts fall back to their built-in defaults.
