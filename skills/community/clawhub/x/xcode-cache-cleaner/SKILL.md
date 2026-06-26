---
name: xcode-cache-cleaner
description: Scan and clean build caches for iOS/macOS developers — with first-class Xcode support (global DerivedData, iOS/watchOS/tvOS/macOS DeviceSupport, Caches/com.apple.dt.Xcode, CoreSimulator unavailable devices) plus per-project cleanup (SPM .build, Pods, Carthage, xcresult, and generic node_modules/Gradle/Rust target/Python __pycache__). Use when user asks to clean Xcode caches, reclaim disk from Xcode, remove DerivedData, free space on a Mac dev machine, or clear build artifacts in a project folder. Triggers on phrases like "clean Xcode", "清理 Xcode 缓存", "remove DerivedData", "free disk space", "why is this folder so big", "clear build files".
---

# Xcode Cache Cleaner

Scan a project directory **or** the global Xcode caches under `~/Library/Developer/`, report sizes, and optionally delete to free disk space.

## Two Modes

### 1. Project cache cleanup (per-folder)

```bash
bash scripts/clean-cache.sh <target-dir> [--dry-run] [--yes]
```

Use when the user points at a specific project directory (SPM `.build`, Pods, `node_modules`, etc.).

### 2. Global Xcode cache cleanup (system-wide)

```bash
bash scripts/clean-xcode-global.sh [--dry-run] [--yes] \
     [--keep-ios <pattern>]... [--include-archives]
```

Use when the user asks to clean Xcode / DerivedData / iOS DeviceSupport / simulators globally (e.g. "清一下 Xcode 缓存"、"free space on my mac", "reclaim disk from Xcode").

Covers:
- `~/Library/Developer/Xcode/DerivedData/*` — all deleted
- `~/Library/Developer/Xcode/{iOS,watchOS,tvOS,macOS} DeviceSupport/*` — by default keeps the highest-version folder per platform; pass `--keep-ios 26.4.2 --keep-ios 18.5` (repeatable, substring match) to override
- `~/Library/Caches/com.apple.dt.Xcode` — deleted
- `~/Library/Developer/Xcode/Archives/*` — **listed but NOT deleted** by default (these are signed `.xcarchive` builds). Pass `--include-archives` to also delete.
- CoreSimulator unavailable devices — runs `xcrun simctl delete unavailable` (safe; only removes devices Xcode already lost track of)

Flags:
- `--dry-run` — Scan and report only, no deletions
- `--yes` / `-y` — Skip confirmation prompt (use when agent is driving)
- `--keep-ios <pattern>` — Keep DeviceSupport folders matching this substring (repeatable). Applied across all `*OS DeviceSupport` dirs, not just iOS.
- `--include-archives` — Also delete `Archives/*` (default: keep)

**Always run `--dry-run` first**, show the user the results, then ask before running the actual cleanup (or pass `--yes` if the user already confirmed). Both scripts prefer `trash` (recoverable) over `rm -rf` when available.

## Supported Cache Types

| Cache | Pattern | Ecosystems |
|-------|---------|------------|
| SPM .build | `.build/` dirs | Swift / iOS |
| DerivedData | `DerivedData/` dirs | Xcode |
| xcresult | `*.xcresult` bundles | Xcode tests |
| Pods | `Pods/` dirs | CocoaPods |
| Carthage/Build | `Carthage/Build/` | Carthage |
| node_modules | `node_modules/` | Node.js |
| Gradle .gradle | `.gradle/` dirs | Android / Java |
| Gradle build | `build/` under `.gradle` | Android / Java |
| Rust target | `target/` next to `Cargo.toml` | Rust |
| Python __pycache__ | `__pycache__/` dirs | Python |
| .pytest_cache | `.pytest_cache/` dirs | Python |
| .mypy_cache | `.mypy_cache/` dirs | Python |

The script also reports `.git` size (not deleted) with a hint to run `git gc --aggressive`.

## Notes

- All deletions are recoverable by re-building (or via Trash if `trash` is installed). No source code is touched.
- The project-mode script resolves the target to an absolute path before scanning.
- For very large projects, the initial `du` scan may take a minute.
- Global-mode default for DeviceSupport (keep highest version) is conservative; if the user has multiple physical devices on different iOS versions, prompt for explicit `--keep-ios` patterns before deleting.
