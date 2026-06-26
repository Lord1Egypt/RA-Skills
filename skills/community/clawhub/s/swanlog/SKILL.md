---
name: swanlog
description: Pull a SwanLab cloud experiment (metrics + config + metadata + requirements) down to a local directory in one shot. Use this whenever the user wants to inspect, sync, archive, diff, or analyze a remote SwanLab run from the laptop — including phrases like "拉一下 swanlab", "看下最新实验", "fetch SwanLab logs", "sync experiment from cloud", "I can't ssh into the GPU box, just grab the run", or any time a user references a SwanLab experiment ID/URL and needs the data on disk. Trigger this skill aggressively for any read-side SwanLab interaction; do NOT trigger when the user is starting a new training run, editing configs, troubleshooting login itself, or asking generic ML/SwanLab questions that don't require pulling data to disk.
---

# swanlog

Fetch a SwanLab cloud experiment to a local directory and brief the user on what came back. The skill is a thin wrapper around `scripts/fetch_swanlog.py`, which handles auth, API calls, profile extraction, and produces a ready-to-read `brief.md`. Your job is to invoke it correctly and translate that brief into a short message for the user.

## How to invoke

The script lives next to this SKILL.md at `scripts/fetch_swanlog.py`. Use the absolute path you were given when this skill was activated — that's the directory containing this file; tack on `/scripts/fetch_swanlog.py`.

Default form (no args from user → fetch latest):

```bash
python <skill-dir>/scripts/fetch_swanlog.py --latest --project <project>
```

If the user passes `--exp-id <id>`, forward it instead of `--latest` (they're mutually exclusive). If the user wants a custom output location, pass `-o <dir>`; otherwise the script writes to `./swanlog_<YYYY-MM-DD_HH-MM-SS>/` in the current working directory.

**The script auto-enumerates every scalar metric the run actually logged** and pulls all of them — the user does not need to know what was logged in advance. Only pass `--keys "k1,k2,..."` if the user explicitly wants a subset (e.g. "I just want train and val loss"). If auto-enumeration fails (SwanLab API drift, auth issue), the script falls back to a generic key list and prints a warning; surface that warning, but the dump itself still succeeds.

If the user hasn't named a project and `SWANLAB_PROJECT` isn't set, ask once: *"Which SwanLab project?"*

## Workflow

1. **Run the script** with `Bash`, capturing full stdout/stderr.

2. **If the script exited non-zero**, show the last 10 lines of stderr verbatim, then stop. Common signals and the right hint:
   - `ApiError` mentioning auth / 401 / netrc → tell the user to run `swanlab login`
   - `ModuleNotFoundError: swanlab` (or pandas / omegaconf) → `pip install swanlab>=0.7.15 pandas omegaconf`
   - `RuntimeError: No experiments in ...` → user named the wrong project, or hasn't pushed any run yet
   - `404` on the experiment ID → ID typo or experiment was deleted
   - Network errors → relay verbatim, don't speculate

3. **On success, read `<output_dir>/brief.md`** — the script writes a fixed-format Markdown brief containing run metadata, the latest non-NaN value of every scalar with its step, and the dump's row × col count. Don't reinvent this with `awk` / one-liners over `metrics.csv`; the brief is the contract. If `brief.md` is missing or empty, that's a bug in the script — surface it.

4. **Tell the user** what's in `brief.md`, in their language (mirror Chinese if they wrote Chinese). Keep it tight — one heading for the run, one short list / table for the latest scalars, end with the absolute path of the output directory so they can `cd` or `open` it. You don't need to dump every scalar if there are many; pick the ones the user is likely to care about (typically a `train/loss*`, `epoch/avg_loss`, `val/*`, plus anything they named earlier in the conversation).

## Idempotency

Re-running the script for the same run (same `--exp-id`, or `--latest` resolving to the same run) overwrites files in the matching `swanlog_<timestamp>/` directory rather than accumulating duplicates. The timestamp comes from `run.created_at`, not the wall clock at fetch time, so the directory name is stable across re-fetches. Safe to call repeatedly to refresh metrics on a still-running experiment.

## Boundaries

- This skill only **reads** from SwanLab. It never starts training, modifies configs, deletes runs, or pushes anything to the cloud.
- It does not assume any particular ML framework, dataset, or directory layout — it works against any SwanLab project.
- `metrics.csv` only contains scalar columns (FLOAT / INTEGER). IMAGE / AUDIO / TEXT artifacts are skipped — they don't fit a flat CSV. If the user needs those, point them to the WebUI URL from the brief.
