---
name: github-traffic
description: Fetch, store, and visualize GitHub repository traffic data (views, clones, referrers, stars) with trend charts. Requires repo push access.
---

# Skill: GitHub Traffic

Fetch and analyze GitHub repository traffic data — page views, git clones, referral sources, popular pages, and star growth. Optionally generate trend charts as PNG images.

> **Prerequisites:**
> - `gh` CLI must be installed and authenticated
> - **Push (write) access** to the target repository is required — GitHub's Traffic API does not work with read-only access
> - `matplotlib` is optional (for PNG chart generation; falls back to ASCII if unavailable)

---

## When to Use

- The user asks about repository traffic, page views, clone counts, or where visitors come from
- The user wants to see traffic trends over time (weekly, monthly, quarterly)
- The user wants to generate traffic report charts for sharing or documentation
- The user wants to periodically snapshot traffic data to build long-term history

---

## Important: GitHub Traffic API Limitations

GitHub only provides the **last 14 days** of traffic data. To track trends over longer periods (30 days, 90 days, etc.), the script stores each fetch in a local history file (`~/.github-traffic/<repo>_traffic.json`). **Regular snapshots are required to build up history.**

Recommended: set up a cron job or CI schedule to run the snapshot command periodically:

```bash
# Daily snapshot via cron (no output, just stores data)
0 9 * * * python /path/to/scripts/github_traffic.py owner/repo --snapshot
```

---

## Default Workflow

```bash
python /path/to/skills/github-traffic/scripts/github_traffic.py <owner/repo>
```

This will:
1. Fetch current traffic data via `gh api`
2. Save a snapshot to `~/.github-traffic/` for historical tracking
3. Display a formatted summary (views, clones, referrers, popular pages)

---

## Generating Charts

```bash
# Generate PNG trend chart (last 30 days, default)
python .../github_traffic.py owner/repo --chart

# Last 7 days
python .../github_traffic.py owner/repo --chart --days 7

# Last 90 days (needs accumulated history)
python .../github_traffic.py owner/repo --chart --days 90

# ASCII chart (no matplotlib needed)
python .../github_traffic.py owner/repo --ascii
```

The PNG chart includes up to 3 panels:
1. **Page Views** — total views and unique visitors (area chart)
2. **Git Clones** — total clones and unique cloners (bar + line chart)
3. **Star Growth** — star count over time (line chart, shown when multiple snapshots exist)

---

## Script Options

| Flag | Default | Description |
|------|---------|-------------|
| `repo` (positional) | required | Repository in `owner/name` format |
| `--chart` | off | Generate PNG trend chart |
| `--ascii` | off | Force ASCII bar chart output |
| `--days` | `30` | Number of days to include in chart |
| `--history-dir` | `~/.github-traffic/` | Directory for historical data storage |
| `--output` | `<repo>_traffic.png` | Output path for chart image |
| `--snapshot` | off | Fetch and store data only (no display) |

---

## Examples

```bash
# Quick traffic summary
python .../github_traffic.py zilliztech/memsearch

# Weekly trend chart
python .../github_traffic.py zilliztech/memsearch --chart --days 7

# Monthly trend chart, custom output path
python .../github_traffic.py zilliztech/memsearch --chart --days 30 --output ./reports/traffic.png

# Just store a snapshot (for cron jobs)
python .../github_traffic.py zilliztech/memsearch --snapshot

# ASCII chart when matplotlib is not available
python .../github_traffic.py zilliztech/memsearch --ascii --days 14
```

---

## History & Long-Term Tracking

Each run merges the current 14-day window into a persistent JSON file at `~/.github-traffic/<owner>_<repo>_traffic.json`. The file contains:

- **Daily views**: date → {views, unique}
- **Daily clones**: date → {clones, unique}
- **Star snapshots**: date → star count
- **Fetch metadata**: timestamp, 14-day totals, stars, forks

To build meaningful 30/90-day charts, run the script at least every 14 days (daily is ideal). Gaps longer than 14 days will show as missing data in charts.

---

## Permissions

The GitHub Traffic API requires **push access** to the repository. This means:
- Repository owners and admins: full access
- Collaborators with write/maintain role: full access
- Read-only users and forkers: **no access** (API returns 403)

If you get a permission error, check your `gh auth status` and ensure your token has the `repo` scope.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Must have push access" error | You need write access to the repo. Check `gh auth status`. |
| Chart shows only 14 days | GitHub only provides 14-day windows. Run `--snapshot` regularly to accumulate history. |
| matplotlib not found | Install with `pip install matplotlib`. Or use `--ascii` for text-based charts. |
| No data for some dates | GitHub may not report days with zero traffic. These gaps are normal. |
