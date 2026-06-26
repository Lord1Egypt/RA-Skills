# RollingGo Flight UVX Reference

## Table of Contents
- [Run Modes](#run-modes)
- [Version Freshness](#version-freshness)
- [API Key Setup](#api-key-setup)
- [Command Guide](#command-guide)
- [Workflow Tutorials](flight-workflows.md)
- [Troubleshooting](#troubleshooting)

---

## Run Modes

### Temporary (uvx — no install needed)
```bash
uvx --refresh --from rollinggo-flight@latest rollinggo-flight --help
uvx --refresh --from rollinggo-flight@latest rollinggo-flight search-airports --keyword "Hangzhou"
```

### Installed tool (recommended for repeated use)
```bash
uv tool install rollinggo-flight@latest
uv tool upgrade rollinggo-flight@latest
rollinggo-flight --help

# If shell can't find the command after install:
uv tool update-shell
```

### Standalone binary (no Node.js or Python required)

**Linux / macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/RollingGo-AI/rollinggo-flight-cli/main/scripts/install.sh | sh
rollinggo-flight --help
```

**Windows PowerShell:**
```powershell
irm https://raw.githubusercontent.com/RollingGo-AI/rollinggo-flight-cli/main/scripts/install.ps1 | iex
rollinggo-flight --help
```

Installs to `~/.local/bin` (Linux/macOS) or `%LOCALAPPDATA%\Programs\rollinggo-flight` (Windows). The binary is self-contained (~40 MB) — no runtime dependencies.

---

## Version Freshness
Default in this reference: guarantee the latest PyPI release on every execution.

```bash
uvx --refresh --from rollinggo-flight@latest rollinggo-flight <subcommand> ...
```

If using an installed tool, upgrade first:
```bash
uv tool upgrade rollinggo-flight@latest
```

---

## API Key Setup
Resolution order: `--api-key` flag → `ROLLINGGO_API_KEY` env var.

```bash
# Bash / zsh
export ROLLINGGO_API_KEY="YOUR_API_KEY"

# PowerShell
$env:ROLLINGGO_API_KEY="YOUR_API_KEY"

# Single-command override
rollinggo-flight search-airports --api-key YOUR_API_KEY --keyword "Beijing"
```

---

## Command Guide
Commands below use the installed `rollinggo-flight` binary for readability. The latest-by-default prefix in this reference is `uvx --refresh --from rollinggo-flight@latest rollinggo-flight`.

### `search-airports`
Required: `--keyword`

```bash
# Minimal
rollinggo-flight search-airports --keyword "Hangzhou"

# Table output
rollinggo-flight search-airports --keyword "Beijing" --format table
```

Optional flags: `--format json|table`

### `search-flights`
Required: `--from-date`, `--trip-type`, `--adult-number`, `--child-number`, `--cabin-grade`  
Required (one of): `--from-city` or `--from-airport`  
Required (one of): `--to-city` or `--to-airport`

```bash
# One-way, by city code
rollinggo-flight search-flights \
  --from-city HGH --to-city CTU \
  --from-date 2026-06-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY

# Round-trip, by airport code
rollinggo-flight search-flights \
  --from-airport PEK --to-airport PVG \
  --from-date 2026-06-01 --ret-date 2026-06-05 \
  --trip-type ROUND_TRIP \
  --adult-number 2 --child-number 0 \
  --cabin-grade BUSINESS

# Table output
rollinggo-flight search-flights \
  --from-city SHA --to-city BJS \
  --from-date 2026-06-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY \
  --format table
```

Optional flags: `--ret-date`, `--format json|table`

---

## Workflow Tutorials
For step-by-step, scenario-based tutorials, see [flight-workflows.md](flight-workflows.md).

---

## Troubleshooting
- **401 Unauthorized** → API key missing or invalid. Check `ROLLINGGO_API_KEY` env var or pass `--api-key`.
- **Validation error (exit 2)** → Check required flags. Run `rollinggo-flight search-flights --help` to inspect all options.
- **Empty `flightInformationList`** → Try loosening filters: different dates, city codes instead of airport codes, or different cabin grade.
- **`--ret-date` missing error** → Always required when `--trip-type ROUND_TRIP`.
