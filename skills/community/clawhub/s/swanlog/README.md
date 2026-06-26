# swanlog

A Claude Code / Codex **skill** that pulls a [SwanLab](https://swanlab.cn) cloud experiment — metrics, config, metadata, requirements, and run info — down to a local directory in one shot, then briefs you on what came back.

Built for the common workflow where you train on a remote GPU box, log to SwanLab, but want to inspect or compare runs on your laptop with **Claude Code / Codex** — without ever SSH-ing into the server.

## What it does

Given an experiment ID (or `--latest`), the skill:

1. Authenticates against SwanLab using your local `~/.swanlab/.netrc` credentials.
2. Pulls the experiment's `metrics` (as a tidy `metrics.csv`), the resolved `config.yaml`, the captured `metadata.json`, and a `requirements.txt` snapshot.
3. Saves everything under `./swanlog_<YYYY-MM-DD_HH-MM-SS>/`, named by `run.created_at` so the directory is **stable across re-fetches** of the same run (idempotent).
4. Returns a one-screen brief: run name / state / URL / latest train & val loss.

## Install

### As a Claude Code skill

```bash
git clone https://github.com/jasonwei1002/swanlog ~/.claude/skills/swanlog
```

Then in any Claude Code session: ask Claude to "pull the latest swanlab run" / "拉一下 swanlab" / etc., and it will trigger the skill automatically.

> **Auth**: as long as you've run `swanlab login` once in your terminal, credentials are cached in `~/.swanlab/.netrc` — the skill picks them up automatically, no extra config needed.

### As a standalone CLI

```bash
git clone https://github.com/jasonwei1002/swanlog
cd swanlog
pip install -r requirements.txt
swanlab login    # one-time, drops creds into ~/.swanlab/.netrc

python scripts/fetch_swanlog.py --latest --project MyProject
```

## Usage

```bash
# Most recent run — auto-detects every scalar metric the run logged
python scripts/fetch_swanlog.py --latest --project MyProject

# Specific run by ID (copy from the WebUI URL)
python scripts/fetch_swanlog.py --exp-id <experiment_id> --project MyProject

# Custom output location
python scripts/fetch_swanlog.py --latest --project MyProject -o /tmp/swanlab-dump

# Whitelist a subset (overrides auto-enumeration)
python scripts/fetch_swanlog.py --latest --project MyProject \
  --keys "train/loss,val/loss_mean"

# Or load keys from a file (one per line, # comments allowed)
python scripts/fetch_swanlog.py --latest --project MyProject --keys-file keys.txt

# Override the timezone of the output dir name
# (defaults to your system's local timezone — only set this if you want to pin
# a specific zone, e.g. on a CI runner whose TZ you don't control)
python scripts/fetch_swanlog.py --latest --project MyProject --tz Asia/Shanghai
```

You can also set `SWANLAB_PROJECT=MyProject` in your shell to drop the `--project` flag.

### Default behavior

By default the script asks SwanLab for the full list of scalar columns this run logged (FLOAT / INTEGER) and pulls all of them — you don't have to know in advance what your training loop wrote. Image / audio / text columns are skipped (they don't fit a flat CSV).

If the enumeration endpoint fails (e.g. SwanLab API change, auth issue), the script prints a warning.

## Output layout

```
swanlog_<YYYY-MM-DD_HH-MM-SS>/
├── metrics.csv         # all logged scalar metrics, columns indexed by step
├── config.yaml         # resolved Hydra / your-framework config from the run
├── metadata.json       # SwanLab's snapshot: hardware, OS, git SHA, ...
├── requirements.txt    # pip freeze captured at run start
├── run_info.json       # name / id / state / created_at / finished_at / url
└── brief.md            # human-readable digest: run header + latest non-NaN
                        # value (with step) for every scalar metric
```

`brief.md` is what the Claude skill reads to summarize the run for you — the same format works fine for humans skimming a directory.

## Analyze with AI

Once a run is pulled to disk, the directory is just plain text — `metrics.csv`, `config.yaml`, `metadata.json`, `brief.md`. That makes it trivial to hand off to any coding agent (Claude Code, Codex, Cursor, etc.) for deeper analysis without the agent ever needing SwanLab credentials or network access.

Typical follow-ups you can ask the agent to do:

- "Read `brief.md` and tell me whether this run converged or is still trending down."
- "Plot `train/loss` vs `val/loss` from `metrics.csv` and flag any overfitting."
- "Diff `config.yaml` against the previous run's `config.yaml` and explain what changed."
- "Compare `metrics.csv` across these three `swanlog_*` directories and pick the best checkpoint."
- "Read `metadata.json` — was this run on the same GPU / git SHA as the baseline?"

Because every dump is self-contained and idempotently named by `run.created_at`, you can keep multiple runs side-by-side and let the agent reason across them.

## Requirements

- Python 3.9+ (for `zoneinfo`)
- `swanlab>=0.7.15`, `pandas`, `omegaconf`
- A SwanLab account, logged in once via `swanlab login`

## License

MIT
