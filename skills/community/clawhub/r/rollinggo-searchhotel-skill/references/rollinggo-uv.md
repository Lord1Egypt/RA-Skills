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

---

## Run Modes

### Temporary (uvx — no install needed)

```bash
uvx --from rollinggo rollinggo --help
uvx --from rollinggo rollinggo search-hotels --origin-query "..." --place "Tokyo Disneyland" --place-type "<from --help>"
```

### Global install (recommended for repeated use)

```bash
uv tool install rollinggo
rollinggo --help
```

Upgrade an existing install:

```bash
uv tool upgrade rollinggo
```

---

## Version Freshness

Default in this reference: guarantee the latest release on every execution.

```bash
uvx --refresh --from rollinggo rollinggo <subcommand> ...
```

If using a globally installed command, upgrade first:

```bash
uv tool upgrade rollinggo
```

---

## API Key Setup

**Pre-configured Public API Key:**

```bash
AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f
```

For detailed usage instructions, see [env.md](env.md).

```bash
# Bash / zsh - Set environment variable
export AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f

# Single-command override
rollinggo hotel-tags --api-key mcp_171e1ffa7da343faa4ec43460c52b13f
```

---

## Command Guide

Commands below use the installed `rollinggo` binary for readability. The latest-by-default prefix in this reference is `uvx --refresh --from rollinggo rollinggo`.

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
  --place "Shanghai Disneyland" --place-type "<value from --help>" \
  --check-in-date 2026-04-01 --stay-nights 2 \
  --adult-count 2 --size 5 \
  --star-ratings 4.0,5.0 --max-price-per-night 800
```

### `hotel-detail`

```bash
rollinggo hotel-detail \
  --hotel-id 123456 \
  --check-in-date 2026-04-01 --check-out-date 2026-04-03 \
  --adult-count 2 --room-count 1
```

### `hotel-tags`

```bash
rollinggo hotel-tags
```

---

## End-to-End Workflows

### Workflow: Search → Detail

```bash
# Step 0: Setup API Key
export AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f

# Step 1: search
rollinggo search-hotels \
  --origin-query "Find hotels near Shanghai Disneyland" \
  --place "Shanghai Disneyland" --place-type "<from --help>" \
  --check-in-date 2026-04-01 --stay-nights 2 --size 3

# Step 2: detail
rollinggo hotel-detail \
  --hotel-id <hotelId> \
  --check-in-date 2026-04-01 --check-out-date 2026-04-03 \
  --adult-count 2 --room-count 1
```

---

## Troubleshooting

- **`rollinggo: command not found`:** Run `uvx --from rollinggo rollinggo ...` or `uv tool install rollinggo`
- **Missing API key error:** Pass `--api-key` or set `AIGOHOTEL_API_KEY=mcp_171e1ffa7da343faa4ec43460c52b13f`
- **Exit code `2` (validation):** Rerun with `--help`; check required flags, date format
- **No hotels returned:** Remove `--star-ratings`, increase `--size` or `--distance-in-meter`
