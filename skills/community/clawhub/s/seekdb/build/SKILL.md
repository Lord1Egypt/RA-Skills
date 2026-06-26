---
name: seekdb-build
description: Build SeekDB binaries and installation packages from source for one or more target platforms (macOS, Linux, Android cross-compile, Windows native, Python wheel). Handles argument parsing, target-aware dependency initialization (MD5 marker check), and dispatches to platform-specific build scripts. Use when the user says "build seekdb", "compile seekdb", "make a release rpm/deb/tgz/apk/installer", "/build-seekdb", or asks how to produce a SeekDB binary or package.
compatibility: macOS arm64 (≥13), Linux x86_64 (el8/el9), Android arm64-v8a (cross-compile on macOS/Linux), Windows x86_64 (native only).
metadata:
  author: oceanbase
  version: "1.0"
---

# Build SeekDB

Build SeekDB binaries and/or installation packages for one or more target platforms.

## Usage

```
/build-seekdb [platform] [action] [options]
```

**platform** (default: auto-detect current OS):
- `mac`     — macOS arm64/x86_64
- `linux`   — Linux x86_64
- `android` — Android arm64-v8a (cross-compile on macOS/Linux host)
- `windows` — Windows x86_64 (native PowerShell environment only)

**action** — what to do (default: `compile release`):

| Platform | Compile actions | Package actions |
|----------|----------------|-----------------|
| `mac`    | `release` `debug` `perf` | `tgz` |
| `linux`  | `release` `debug` `perf` | `rpm` `deb` |
| `android`| `release` `debug` | `apk` |
| `windows`| `release` `debug` | `installer` |

- Compile actions build the seekdb binary + `libseekdb_embed_c`.
- Package actions build an installable artifact (implies a release compile first if needed).
- Multiple actions can be requested in one invocation, e.g. `release tgz` or `debug rpm`.

**options**:
- `--init`        — Force re-initialize dependencies before building
- `--jobs N`      — Parallel jobs (default: all CPU cores)
- `--version V`   — Version string for package naming (e.g. `4.3.5`, default: `beta`)
- `--release R`   — Release/date string for package naming (e.g. `20260407`, default: today's date)
- `--with-jni`    — (Android only) Also build `libseekdb_embed.so` JNI library
- `--install`     — (Android only) `adb install` the APK after building

---

## Instructions

When the user runs `/build-seekdb`, follow these steps.

### Step 1 — Parse arguments

- Extract platform, action(s), and options from `$ARGUMENTS`.
- If no platform given, detect via `uname -s`: Darwin → mac, Linux → linux.
- If no action given, default to `release` (compile only).
- Default version: `beta`. Default release: today's date as `YYYYMMDD`.
- Default jobs: detect with `sysctl -n hw.ncpu` (mac/android) or `nproc` (linux).
- Reject invalid combinations (e.g. `deb` on mac, `tgz` on linux, `perf` on android/windows)
  and tell the user which package/compile types are supported for their platform.

---

### Step 2 — Determine repo root

```bash
REPO_ROOT=$(pwd)
```
Use `$REPO_ROOT` for all subsequent commands. Do NOT hardcode any absolute path.

**Key rule — package actions vs compile-only actions:**

- **Package actions** (`apk`, `rpm`, `deb`, `tgz`, `installer`): call the dedicated packaging
  script directly. These scripts already handle clean + init + make internally.
  **Do NOT run a separate init step before them.**

- **Compile-only actions** (`release`, `debug`, `perf`): no packaging script is involved.
  Run the dep check below first, then call `build.sh --make`.

#### Dependency check (compile-only actions only)

`dep_create.sh` writes two marker files on successful init:
- `deps/3rd/DONE` — generic completion flag
- `deps/3rd/<MD5>` — MD5 of the platform-specific `.deps` file

**Checking only `DONE` is insufficient.** The MD5 marker must match the *current* `.deps`
file for the *target* platform. A missing MD5 marker means:
- the `.deps` file was updated (new or changed packages), OR
- the last init was for a different platform (e.g. macOS deps present, but Android marker absent).

```bash
# 1. Determine the .deps file for the target platform
#    Android:          $REPO_ROOT/deps/init/oceanbase.android.arm64.deps
#    macOS arm64 ≥15:  $REPO_ROOT/deps/init/oceanbase.macos15.arm64.deps
#    macOS arm64 13-14:$REPO_ROOT/deps/init/oceanbase.macos13.arm64.deps
#    Linux el8 x86_64: $REPO_ROOT/deps/init/oceanbase.el8.x86_64.deps
#    Linux el9 x86_64: $REPO_ROOT/deps/init/oceanbase.el9.x86_64.deps
#
# 2. Compute its MD5
#    macOS: MD5=$(md5 -r <DEPS_FILE> | cut -d' ' -f1)
#    Linux: MD5=$(md5sum <DEPS_FILE>  | cut -d' ' -f1)
#
# 3. Check the marker
DEPS_MARKER="$REPO_ROOT/deps/3rd/$MD5"
```

**OS_TAG reference table:**

| Target | OS_TAG |
|--------|--------|
| Android cross-compile | `android.arm64` |
| macOS arm64, macOS ≥ 15 | `macos15.arm64` |
| macOS arm64, macOS 13–14 | `macos13.arm64` |
| macOS x86_64, macOS ≥ 15 | `macos15.x86_64` |
| Linux x86_64, RHEL/CentOS 8 | `el8.x86_64` |
| Linux x86_64, RHEL/CentOS 9 | `el9.x86_64` |

On macOS: detect version with `sw_vers -productVersion`; detect arch with
`sysctl -n hw.optional.arm64` (returns `1` for arm64, correct even under Rosetta).

**Decision logic (compile-only):**

| Condition | Action |
|-----------|--------|
| `--init` explicitly passed | Always run init: `./build.sh release [--android] --init` |
| `$DEPS_MARKER` missing | Auto-run init, print `[build-seekdb] deps marker not found — running --init for <PLATFORM> ...` |
| `$DEPS_MARKER` exists | Skip init, print `[build-seekdb] deps OK — skipping init.` |

> `dep_create.sh` is idempotent — if the MD5 marker already matches it exits immediately.

---

### Step 3 — Execute builds

Pick the matching platform reference and follow it end-to-end. Each reference covers
compile modes, build directories, artifact paths, and the relevant packaging script.

| Target | Reference |
|--------|-----------|
| macOS (compile + tgz) | [references/build-macos.md](references/build-macos.md) |
| Linux (compile + rpm/deb) | [references/build-linux.md](references/build-linux.md) |
| Android (cross-compile + apk) | [references/build-android.md](references/build-android.md) |
| Windows (native compile + installer) | [references/build-windows.md](references/build-windows.md) |
| Python wheel (manylinux only) | [references/build-python-wheel.md](references/build-python-wheel.md) |

---

### Step 4 — Report results

After each action:
- Print success or failure (exit code).
- Print artifact path(s) and file sizes (`ls -lh`).
- If init failed → abort, report error, do not proceed to make.
- If make failed after successful init → suggest re-running with `--init` (marker may be stale).
- If Android NDK missing → remind user to set `ANDROID_NDK_HOME`.
- If `windows` requested on non-Windows → show PowerShell instructions, do not attempt build.
