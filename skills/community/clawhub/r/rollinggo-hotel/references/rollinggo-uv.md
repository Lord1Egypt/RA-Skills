# RollingGo UV Reference

> Load this file for uv / uvx / Python execution environment.
> Hotel search logic and filter rules → `SKILL.md`.

## Table of Contents

1. [Run Modes](#run-modes)
2. [Version Freshness](#version-freshness)
3. [API Key Setup](#api-key-setup)
4. [Command Guide](#command-guide)
5. [End-to-End Workflows](#end-to-end-workflows)
6. [Troubleshooting](#troubleshooting)
7. [Local Development](#local-development)

---

## Run Modes

### Temporary (uvx — no install needed)

> Note: package name and command name are both `rollinggo`, hence the `--from` syntax.
> Use `rollinggo@latest` explicitly so uv resolves the current latest published release.

```bash
uvx --refresh --from rollinggo@latest rollinggo --help
uvx --refresh --from rollinggo@latest rollinggo search-hotels \
  --origin-query "Find hotels near Tokyo Disneyland" \
  --place "Tokyo Disneyland" --place-type "<from --help>"
```

### Installed tool (recommended for repeated use)

```bash
uv tool install rollinggo@latest
uv tool upgrade rollinggo@latest
rollinggo --help

# If shell can't find the command after install:
uv tool update-shell
```

### Local source (this repo)

```bash
uv run --directory rollinggo-uv rollinggo --help
uv run --directory rollinggo-uv rollinggo search-hotels --help
```

---

## Version Freshness

Default in this reference: guarantee the latest PyPI release on every execution.

```bash
uvx --refresh --from rollinggo@latest rollinggo <subcommand> ...
```

If using an installed tool, upgrade first:

```bash
uv tool upgrade rollinggo@latest
```

---

## API Key Setup

Resolution order: `--api-key` flag → `RollingGo_API_KEY` env var.

```bash
# Bash / zsh
export RollingGo_API_KEY="YOUR_API_KEY"

# PowerShell
$env:RollingGo_API_KEY="YOUR_API_KEY"

# Single-command override
rollinggo hotel-tags --api-key YOUR_API_KEY
```

If the host drops `RollingGo_API_KEY` between runs, see [claw-host-env.md](claw-host-env.md) for persistent injection options.

Apply at: https://mcp.agentichotel.cn/apply

---

## Command Guide

Commands below use the installed `rollinggo` binary for readability. The latest-by-default prefix in this reference is `uvx --refresh --from rollinggo@latest rollinggo`.

### `search-hotels`

Required: `--origin-query`, `--place`, `--place-type`

```bash
# Minimal
rollinggo search-hotels \
  --origin-query "Find hotels near Tokyo Disneyland" \
  --place "Tokyo Disneyland" \
  --place-type "<value from --help>"

# With filters
rollinggo search-hotels \
  --origin-query "Find family friendly hotels near Shanghai Disneyland" \
  --place "Shanghai Disneyland" \
  --place-type "<value from --help>" \
  --check-in-date 2026-04-01 --stay-nights 2 \
  --adult-count 2 --size 5 \
  --star-ratings 4.0,5.0 --max-price-per-night 800

# Human-readable table
rollinggo search-hotels --origin-query "Hotels in Tokyo" --place "Tokyo" \
  --place-type "<value from --help>" --format table
```

Optional flags: `--country-code`, `--size`, `--check-in-date`, `--stay-nights`, `--adult-count`, `--distance-in-meter`, `--star-ratings min,max`, `--preferred-tag`, `--required-tag`, `--excluded-tag`, `--preferred-brand`, `--max-price-per-night`, `--min-room-size`, `--format json|table`

### `hotel-detail`

Pass one of `--hotel-id` (preferred) or `--name`. `--format table` is not allowed.

```bash
# By ID with dates and occupancy
rollinggo hotel-detail \
  --hotel-id 123456 \
  --check-in-date 2026-04-01 --check-out-date 2026-04-03 \
  --adult-count 2 --room-count 1

# With children
rollinggo hotel-detail \
  --hotel-id 123456 \
  --check-in-date 2026-04-01 --check-out-date 2026-04-03 \
  --adult-count 2 --child-count 2 --child-age 4 --child-age 7 --room-count 1

# By name (fuzzy match)
rollinggo hotel-detail --name "The Ritz-Carlton Tokyo" \
  --check-in-date 2026-04-01 --check-out-date 2026-04-03
```

### `hotel-tags`

```bash
rollinggo hotel-tags
rollinggo hotel-tags --api-key YOUR_API_KEY

# Temporary execution without install
uvx --refresh --from rollinggo@latest rollinggo hotel-tags
```

Use returned tag strings exactly when building `--preferred-tag` / `--required-tag` / `--excluded-tag` filters.

---

## End-to-End Workflows

### Workflow 1: Search → Detail

```bash
# Step 1: search
rollinggo search-hotels \
  --origin-query "Find hotels near Shanghai Disneyland" \
  --place "Shanghai Disneyland" --place-type "<from --help>" \
  --check-in-date 2026-04-01 --stay-nights 2 --size 3

# Step 2: extract hotelId from JSON, then:
rollinggo hotel-detail \
  --hotel-id <hotelId> \
  --check-in-date 2026-04-01 --check-out-date 2026-04-03 \
  --adult-count 2 --room-count 1
```

### Workflow 2: Tag-filtered search

```bash
# Step 1: discover tags
rollinggo hotel-tags

# Step 2: search with tags
rollinggo search-hotels \
  --origin-query "Family hotels with breakfast near Tokyo Disneyland" \
  --place "Tokyo Disneyland" --place-type "<from --help>" \
  --required-tag "breakfast included" --preferred-tag "family friendly"
```

---

## Troubleshooting

- **`rollinggo: command not found`:** Run `uvx --refresh --from rollinggo@latest rollinggo ...` or `uv tool install rollinggo@latest && uv tool update-shell`
- **Missing API key error:** Pass `--api-key`, set `RollingGo_API_KEY`, or if you are inside any claw-style host, follow [claw-host-env.md](claw-host-env.md) and inject the same key through that host's config layer
- **Exit code `2` (validation):** Rerun with `--help`; check required flags, date format, `--child-count` vs `--child-age` count
- **No hotels returned:** Remove `--star-ratings`, increase `--size` or `--distance-in-meter`, remove tag filters
- **`hotel-detail` returns no room plans:** Normal business result; try another hotel, different dates, or adjust occupancy

---

## Local Development

```bash
# Run from source
uv run --directory rollinggo-uv rollinggo --help

# Run tests
uv run --directory rollinggo-uv --extra dev python -m pytest

# Refresh temporary execution against local source
uvx --refresh --from . rollinggo --help
```

Parity checks against Node build: top-level help, `search-hotels --help`, exit code `2` on missing params, JSON-only for `hotel-detail` / `hotel-tags`, live API success.
