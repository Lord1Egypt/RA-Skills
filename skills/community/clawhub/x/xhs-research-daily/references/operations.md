# XHS Research Daily Operations

## Files

- `scripts/run_daily.py` - entry point
- `scripts/pipeline.py` - collection and summarization pipeline
- `scripts/xhs_client.py` - `mcporter` wrapper
- `scripts/render.py` - Xiaohongshu-style drafting
- `scripts/scoring.py` - lightweight ranking
- `config/topics.json` - topic definitions

## Environment

The scripts support overriding the mcporter config path with:

- `MCPORTER_CONFIG_PATH`

If not set, the script defaults to:

- `/Users/ailor/.openclaw/workspace/config/mcporter.json`

Change that on other machines.

## Typical Commands

Dry run:

```bash
cd /path/to/skills/xhs-research-daily
python3 scripts/run_daily.py --topic diffusion_llm --dry-run
```

Publish:

```bash
cd /path/to/skills/xhs-research-daily
python3 scripts/run_daily.py --topic diffusion_llm --publish
```

## Scheduling

Cron example:

```bash
0 9 * * * cd /path/to/skills/xhs-research-daily && MCPORTER_CONFIG_PATH=/path/to/mcporter.json /usr/bin/python3 scripts/run_daily.py --topic diffusion_llm --publish >> /path/to/xhs-research-daily/data/logs/diffusion_llm.log 2>&1
```

Start with `--dry-run` on a schedule before enabling `--publish`.

## Adding Topics

Copy the `diffusion_llm` entry and tune:

- keywords
- hashtags
- cover image
- retrieval depth
- title prefix

Keep the topic key machine-friendly, such as:

- `agent_memory`
- `llm_safety`
- `test_time_scaling`
- `multi_agent`

## Stability Advice

- Do not hammer detail pages for every result.
- Keep `max_posts_for_detail` low.
- Reuse one logged-in MCP service.
- If login keeps expiring, stop and stabilize the session before more runs.
