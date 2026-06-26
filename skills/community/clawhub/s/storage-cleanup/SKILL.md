---
name: storage-cleanup
description: One-command disk cleanup for macOS and Linux — trash, caches, temp files, old kernels, snap revisions, Homebrew, Docker, and Xcode artifacts. Use when user asks to free storage, clean up disk, reclaim space, reduce disk usage, or encounters low disk / "disk full" warnings. Safe by default with dry-run mode. No dependencies beyond bash and awk.
---

# Storage Cleanup

Reclaim tens of gigabytes in one command. No config files, no dependencies, no damage.

## Why This Skill

Systems accumulate junk silently — IDE caches, old snap revisions, stale pip builds, forgotten trash, outdated kernels. Manually hunting them down wastes time and risks deleting the wrong thing.

This skill:
- **Scans 12+ cleanup targets** across both macOS and Linux in a single pass
- **Safe by default** — `--dry-run` shows exactly what would be cleaned before touching anything
- **Zero dependencies** — pure bash + awk, works on any stock macOS or Linux install
- **Cross-platform** — auto-detects OS and runs only what applies (no errors on missing tools)
- **Selective** — skip any category with `--skip-kernels`, `--skip-docker`, `--skip-brew`, `--skip-snap`
- **Reports savings** — shows before/after disk usage and exact bytes freed

## Quick Start

```bash
# Preview what would be cleaned (safe, changes nothing)
bash scripts/cleanup.sh --dry-run

# Clean everything
bash scripts/cleanup.sh --yes

# Clean but keep Docker and old kernels
bash scripts/cleanup.sh --yes --skip-docker --skip-kernels
```

## What Gets Cleaned

### Both Platforms
| Target | Typical Size | Notes |
|--------|-------------|-------|
| Trash | 1–50 GB | macOS `~/.Trash`, Linux `~/.local/share/Trash` |
| Stale `/tmp` | 1–10 GB | pip/npm/rust build dirs older than 60 min |
| pip cache | 50–500 MB | `pip cache purge` |
| Go build cache | 100 MB–2 GB | `go clean -cache` |
| pnpm / yarn / node caches | 50–500 MB | Safe to regenerate |
| JetBrains IDE cache | 1–10 GB | IntelliJ, PyCharm, WebStorm, etc. |
| Whisper model cache | 1–5 GB | Redownloads on demand |
| Chrome / Firefox cache | 200 MB–2 GB | Browsing cache only |
| Playwright browsers | 200 MB–1 GB | Redownloads on demand |
| Docker dangling images | 0–10 GB | Only unreferenced images + build cache |

### Linux Only
| Target | Typical Size | Notes |
|--------|-------------|-------|
| Apt cache | 200 MB–2 GB | `apt clean` |
| Journal logs | 500 MB–4 GB | Vacuumed to 200 MB |
| Disabled snap revisions | 500 MB–5 GB | Old versions kept by snapd |
| Old kernels | 200–800 MB | Keeps current running kernel |

### macOS Only
| Target | Typical Size | Notes |
|--------|-------------|-------|
| Homebrew old versions | 500 MB–5 GB | `brew cleanup --prune=7` |
| Xcode DerivedData | 2–30 GB | Build artifacts, safe to clear |
| Xcode Archives | 1–20 GB | Old build archives |
| iOS DeviceSupport | 2–15 GB | Old device symbols |
| CoreSimulator caches | 500 MB–5 GB | Simulator disk images |
| Old user logs | 100 MB–1 GB | Logs older than 30 days |

## Options

| Flag | Effect |
|------|--------|
| `--dry-run` | Preview cleanup without deleting anything |
| `--yes` / `-y` | Run without confirmation prompts |
| `--skip-kernels` | Don't remove old kernels (Linux) |
| `--skip-snap` | Don't remove disabled snap revisions (Linux) |
| `--skip-docker` | Don't prune Docker |
| `--skip-brew` | Don't clean Homebrew |

## Manual Extras

Targets the script doesn't touch (check manually if needed):
- **Ollama models**: `ollama list` → `ollama rm <unused>`
- **npm global cache**: `npm cache clean --force`
- **Conda envs**: `conda env list` → `conda remove -n <env> --all`
- **Compressed logs**: `sudo find /var/log -name "*.gz" -delete`
- **Flatpak** (Linux): `flatpak uninstall --unused`
- **Time Machine snapshots** (macOS): `tmutil listlocalsnapshots /` → `tmutil deletelocalsnapshots <date>`
