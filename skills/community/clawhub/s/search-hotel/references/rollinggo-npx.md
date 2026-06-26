# RollingGo NPX Reference

> Load this file for npm / npx / Node.js execution environment.
> Hotel search logic and filter rules → `SKILL.md`.

## Table of Contents

1. [Run Modes](#run-modes)
2. [API Key Setup](#api-key-setup)
3. [Command Guide](#command-guide)
4. [End-to-End Workflows](#end-to-end-workflows)
5. [Troubleshooting](#troubleshooting)
6. [Local Development](#local-development)

---

## Run Modes

### Temporary (npx — no install needed)

```bash
npx rollinggo --help
npx rollinggo search-hotels --origin-query "..." --place "Tokyo Disneyland" --place-type "<from --help>"
```

### Global install (recommended for repeated use)

```bash
npm install -g rollinggo
rollinggo --help
```

### Local source (this repo)

```bash
cd rollinggo-npx
npm install && npm run build
node dist/cli.js --help
node dist/cli.js search-hotels --help
```

---

## API Key Setup

Resolution order: `--api-key` flag → `AIGOHOTEL_API_KEY` env var.

```bash
# PowerShell
$env:AIGOHOTEL_API_KEY="YOUR_API_KEY"

# Bash / zsh
export AIGOHOTEL_API_KEY="YOUR_API_KEY"

# Single-command override
rollinggo hotel-tags --api-key YOUR_API_KEY
```

Apply at: https://mcp.agentichotel.cn/apply

---

## Command Guide

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
  --origin-query "Find family hotels near Shanghai Disneyland" \
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

- **`rollinggo: command not found`:** Run `npx rollinggo ...` or `npm install -g rollinggo`
- **Missing API key error:** Pass `--api-key` or set `AIGOHOTEL_API_KEY`
- **Exit code `2` (validation):** Rerun with `--help`; check required flags, date format, `--child-count` vs `--child-age` count
- **No hotels returned:** Remove `--star-ratings`, increase `--size` or `--distance-in-meter`, remove tag filters
- **`hotel-detail` returns no room plans:** Normal business result; try another hotel, different dates, or adjust occupancy

---

## Local Development

```bash
# Run from source
cd rollinggo-npx
npm install && npm run build
node dist/cli.js search-hotels --help

# Run tests
npm test
```

Parity checks against Python build: top-level help, `search-hotels --help`, exit code `2` on missing params, JSON-only for `hotel-detail` / `hotel-tags`, live API success.
