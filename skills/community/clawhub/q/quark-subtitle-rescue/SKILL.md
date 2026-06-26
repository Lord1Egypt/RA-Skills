---
name: quark-subtitle-rescue
description: Bulk add subtitles to Quark movie folders with high success and low wrong-match risk. Best for "all subfolders" jobs, interrupted runs, and retrying failed titles with multi-source fallback (OpenSubtitles/SubHD/YIFY), strict matching, rollback safety, and completion reporting.
---

# Quark Subtitle Rescue

High-success, low-risk workflow for Quark 网盘字幕批处理。

## What this skill solves

- One-click style recovery for: “给电影文件夹所有子目录补字幕”
- Resume from partial progress after interruptions/429/timeout
- Reduce bad matches via strict retries and staged fallback
- Keep an auditable trail: progress, failures, and final completion report

## Use this skill when

- User asks for **batch subtitles across many Quark subfolders**
- Previous run is partially done and needs **rescue/retry**
- Need to switch subtitle providers for better hit rate
- Need safe rollback/checks after suspected wrong matches

## Don’t use this skill when

- User only needs subtitle for a **single local file**
- There is no valid Quark login/cookie context


## Quick Start

1. Confirm tool root exists: `quark_subtitle_tool/`.
2. Ensure config exists: `~/.config/quark_subtitle.json` with valid `cookie`.
3. Activate venv: `source quark_subtitle_tool/venv/bin/activate`.
4. Run staged workflow (below), do not jump directly to aggressive retries.

### Minimal inputs expected

- Quark target path (example: `全部文件/来自：分享/电影`)
- Subtitle preference (default: bilingual zh+en)
- Whether to allow Chinese-only fallback when bilingual is unavailable

## Staged Workflow

### Stage 1 — Baseline batch run
Run:

```bash
python quark_subtitle_tool/batch_subtitle_runner.py
```

Check output:
- `quark_subtitle_tool/quark_work/batch_progress.json`
- `quark_subtitle_tool/quark_work/batch_failures.jsonl`

### Stage 2 — Strict retry on failures
Run strict retry (avoid broad fuzzy terms like director names):

```bash
python quark_subtitle_tool/strict_top10_retry.py
python quark_subtitle_tool/strict_remaining_retry.py
```

Rule: prioritize `title + year`; avoid generic query terms.

### Stage 3 — Folder-specific rescue
If one folder remains stubborn, run dedicated script for that folder with filename-derived queries (example scripts in `quark_subtitle_tool/*_retry.py`).

### Stage 4 — Final two/small-tail manual precision
For 1–5 leftovers, use explicit aliases (English original title + year), then run a targeted retry script.

## Provider Order and Matching Policy

Default order:
1. OpenSubtitles
2. SubHD (射手系)
3. YIFY
4. Legacy providers (podnapisi/subtis/tvsubtitles)

Policy:
- If provider N hits, stop and do not query lower-priority providers.
- **Default success target: bilingual (zh+en)**. If bilingual is unavailable, fall back to Chinese-only only when user allows it.
- Treat “search page hit” and “download hit” separately; only download hit counts as success.

## Safety Guardrails (Mandatory)

1. Never use broad person-name queries (e.g., director name) for batch upload.
2. If many files suddenly “succeed” with same query, run hash-based spot check before declaring success.
3. If wrong-match batch is found, rollback before continuing.
4. Produce a clear report: total / success / failed / pending folders.

Use helper:

```bash
python skills/quark-subtitle-rescue/scripts/report_progress.py
```

## Troubleshooting

Read `references/troubleshooting.md` when you see:
- OpenSubtitlesCom Bad Request
- dogpile RegionNotConfigured
- 429 rate limits
- folder enter failures due to special chars
- delete/rollback auth failures

## Resources

- `scripts/report_progress.py`: summarize completion from generated JSON reports.
- `references/workflow.md`: reusable decision flow for batch rescue.
- `references/troubleshooting.md`: common failures and mitigations.
