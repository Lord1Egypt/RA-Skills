---
name: harmonyos-build-deploy
description: HarmonyOS application build, clean, package and device installation. Use when building HarmonyOS projects with hvigorw, cleaning build artifacts, managing ohpm dependencies, packaging HAP/HSP/APP bundles, installing to devices via hdc, or troubleshooting installation errors like "version code not same".
---

# HarmonyOS Build & Deploy

Complete workflow for building, cleaning, packaging, and installing HarmonyOS applications.

## First Step: Confirm Operation with User

**IMPORTANT:** Before executing any build or deploy operation, confirm which specific operation(s) the user wants to perform. Ask the user to choose from:

| Operation | Description |
|-----------|-------------|
| Clean build artifacts | Remove previous build cache and outputs |
| Install dependencies | Use ohpm to install project dependencies |
| Build project | Use hvigorw to build HAP/APP packages |
| Install to device | Use hdc to install the app on a device |
| Full pipeline | Clean → install deps → build → deploy to device |

**Why confirm first:**
- Different scenarios require different operations (e.g., incremental build vs clean build)
- Avoid unnecessary time-consuming operations
- Give user control over the workflow
- Prevent accidental device installation

**After user responds:**
- Execute only the selected operations
- Report progress and results clearly

## Quick Reference

```bash
# Build complete app (incremental)
hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon

# List connected devices (returns UDID)
hdc list targets
```

**Note:** Build output path is `outputs/`. For device installation, see [Push and Install](#push-and-install).

## Workflows

**IMPORTANT:** Build, clean, and deploy operations are long-running (build ~30s, file transfer ~20s). Always delegate these workflows to a **subagent** to avoid timeout. This also provides better error handling and clearer progress reporting to the user.

### Clean Build & Deploy

Delegate to subagent with the following steps:

1. Clean: `hvigorw clean --no-daemon`
2. Install dependencies: `ohpm install --all`
3. Build: `hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon`
4. Deploy to device (see [Push and Install](#push-and-install) below)
5. Launch: `hdc -t <UDID> shell "aa start -a EntryAbility -b <bundleName>"`
6. Report success/failure with details

### Deploy Only (No Rebuild)

Delegate to subagent with the following steps:

1. Read `AppScope/app.json5` to get bundleName
2. Check `outputs/` for existing build outputs. If empty or missing, collect signed HAP/HSP from each module's build directory (`{srcPath}/build/default/outputs/default/*-signed.*`) into `outputs/`. See [module-discovery.md](references/module-discovery.md) for details.
3. Deploy to device (see [Push and Install](#push-and-install) below)
4. Launch: `hdc -t <UDID> shell "aa start -a EntryAbility -b <bundleName>"`
5. Report success/failure with details

### Clean App Cache/Data

Delegate to subagent:

1. Clean cache: `hdc -t <UDID> shell "bm clean -n <bundleName> -c"`
2. Clean data: `hdc -t <UDID> shell "bm clean -n <bundleName> -d"`
3. Report success/failure

## Build Commands (hvigorw)

### Incremental Build (Default)

Use incremental build for normal development - only changed modules are rebuilt:

```bash
# Build complete app (incremental)
hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon
```

### Single Module Build

Build only a specific module for faster iteration:

```bash
# Build single HAP module
hvigorw assembleHap -p module=entry@default --mode module -p buildMode=release --no-daemon

# Build single HSP module
hvigorw assembleHsp -p module=my_feature@default --mode module -p buildMode=release --no-daemon

# Build single HAR module
hvigorw assembleHar -p module=library@default --mode module -p buildMode=release --no-daemon

# Build multiple modules at once
hvigorw assembleHsp -p module=module1@default,module2@default --mode module -p buildMode=release --no-daemon
```

**Module name format:** `{moduleName}@{targetName}`
- `moduleName`: Directory name of the module (e.g., `entry`, `my_feature`)
- `targetName`: Target defined in module's `build-profile.json5` (usually `default`)

**When to use single module build:**
- Developing/debugging a specific module
- Faster build times during iteration
- Testing changes in isolated module

**Note:** After single module build, you still need to run `assembleApp` to package the complete application for installation.

### Clean Build (When Needed)

Only perform clean build when:
- First time building the project
- Encountering unexplained build errors
- After modifying `build-profile.json5` or SDK version
- Dependency resolution issues

```bash
# Clean build artifacts
hvigorw clean --no-daemon

# Deep clean (for dependency issues)
ohpm clean && ohpm cache clean
ohpm install --all
hvigorw --sync -p product=default -p buildMode=release --no-daemon
hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon
```

### Install Dependencies (ohpm)

```bash
# Install all dependencies (after clean or first clone)
ohpm install --all

# With custom registry
ohpm install --all --registry "https://repo.harmonyos.com/ohpm/"
```

### Sync Project

Only needed after modifying `build-profile.json5` or `oh-package.json5`:

```bash
hvigorw --sync -p product=default -p buildMode=release --no-daemon
```

### Build Parameters

| Parameter | Description |
|-----------|-------------|
| `-p product={name}` | Target product defined in build-profile.json5 |
| `-p buildMode={debug\|release}` | Build mode |
| `-p module={name}@{target}` | Target module with `--mode module` |
| `--mode project` | Build all modules in project |
| `--mode module` | Build specific module only |
| `--no-daemon` | Disable daemon (recommended for CI) |
| `--analyze=advanced` | Enable build analysis |

## Build Outputs

Build output path: `outputs/`

```
outputs/
├── entry-default-signed.hap
└── *.hsp
```

### Module Types

| Type | Extension | Description |
|------|-----------|-------------|
| HAP | `.hap` | Harmony Ability Package - Application entry module |
| HSP | `.hsp` | Harmony Shared Package - Dynamic shared library |
| HAR | `.har` | Harmony Archive - Static library (compiled into HAP) |
| APP | `.app` | Complete application bundle (all HAP + HSP) |

## Finding Modules

Modules are defined in `build-profile.json5` at the project root. The module type is determined by the `type` field in `{module}/src/main/module.json5`:

| `type` value | Module Type | Build Command |
|--------------|-------------|---------------|
| `"entry"` / `"feature"` | **HAP** | `assembleHap` |
| `"shared"` | **HSP** | `assembleHsp` |
| `"har"` | **HAR** | `assembleHar` |

Module build outputs: `{srcPath}/build/default/outputs/default/`

For detailed module discovery, build output structure, and handling unwanted modules, see [references/module-discovery.md](references/module-discovery.md).

## Device Installation (hdc)

hdc (HarmonyOS Device Connector) is the CLI tool for device communication, similar to Android's adb.

### Check Device

```bash
hdc list targets              # List connected devices (returns UDID)
hdc -t <UDID> shell "whoami"  # Test connection
```

### Push and Install

```bash
# Create temp directory on device (Git Bash compatible)
# If you use Git Bash on Windows, disable MSYS path conversion for hdc commands.
export MSYS_NO_PATHCONV=1

INSTALL_DIR="//data/local/tmp/install_$(date +%s)"
hdc -t <UDID> shell "mkdir -p $INSTALL_DIR"

# Push files one-by-one to explicit remote file paths (most reliable on Git Bash)
for f in outputs/*.hap outputs/*.hsp; do
    [ -f "$f" ] && hdc -t <UDID> file send "$f" "$INSTALL_DIR/$(basename "$f")"
done

# Install (reinstall) HSPs first, then the HAP
for f in outputs/*.hsp outputs/*.hap; do
    [ -f "$f" ] && hdc -t <UDID> shell "bm install -p $INSTALL_DIR/$(basename \"$f\") -r"
done

# Clean up temp directory
hdc -t <UDID> shell "rm -rf $INSTALL_DIR"
```

### Verify and Launch

```bash
# Check installation
hdc -t <UDID> shell "bm dump -n <bundleName>"

# Launch app (default ability)
hdc -t <UDID> shell "aa start -a EntryAbility -b <bundleName>"
```

### Uninstall

```bash
hdc -t <UDID> shell "bm uninstall -n <bundleName>"
```

## hdc Command Reference

| Command | Description |
|---------|-------------|
| `hdc list targets` | List connected devices |
| `hdc -t <UDID> shell "<cmd>"` | Execute shell command on device |
| `hdc -t <UDID> file send <local> <remote>` | Push file/directory to device |
| `hdc -t <UDID> file recv <remote> <local>` | Pull file/directory from device |
| `hdc kill` | Kill hdc server |
| `hdc start` | Start hdc server |
| `hdc version` | Show hdc version |

## Bundle Manager (bm)

Run via `hdc -t <UDID> shell "bm ..."`:

| Command | Description |
|---------|-------------|
| `bm install -p <path>` | Install from directory (all HAP/HSP) |
| `bm install -p <file.hap>` | Install single HAP file |
| `bm install -r -p <path>` | Reinstall (replace existing, keep data) |
| `bm uninstall -n <bundleName>` | Uninstall application |
| `bm dump -n <bundleName>` | Show package info |
| `bm dump -a` | List all installed packages |
| `bm clean -n <bundleName> -c` | Clean application cache |
| `bm clean -n <bundleName> -d` | Clean application data |

## Ability Assistant (aa)

Run via `hdc -t <UDID> shell "aa ..."`:

| Command | Description |
|---------|-------------|
| `aa start -a <ability> -b <bundle>` | Start specific ability |
| `aa force-stop <bundleName>` | Force stop application |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `version code not same` | HSP in output not in build-profile.json5 | Remove unwanted HSP files before install (see [module-discovery.md](references/module-discovery.md)) |
| `install parse profile prop check error` | Signature/profile mismatch | Check signing config in build-profile.json5; verify bundleName matches app.json5; check certificate not expired |
| `install failed due to older sdk version` | Device SDK < app's compatibleSdkVersion | Update device or lower compatibleSdkVersion |
| Device not found | Connection issue | Check USB; enable Developer Options (tap build number 7x) and USB debugging; `hdc kill && hdc start`; try different USB port/cable |
| `signature verification failed` | Invalid or expired certificate | Regenerate certificate in DevEco Studio; check validity period; ensure correct signing config for build type |

## Key Configuration Files

| File | Description |
|------|-------------|
| `AppScope/app.json5` | App metadata (bundleName, versionCode, versionName) |
| `build-profile.json5` | Modules list, products, signing configs |
| `{module}/src/main/module.json5` | Module config (abilities, permissions) |
| `{module}/oh-package.json5` | Module dependencies |

## Reference Files

- **Module Discovery & Build Outputs**: [references/module-discovery.md](references/module-discovery.md) - Module definitions, type identification, build output paths, unwanted modules
- **Complete Installation Guide**: [references/device-installation.md](references/device-installation.md) - Version verification scripts and installation script

## Related Skills

- **arkts-development**: ArkTS/ArkUI development patterns, state management, component lifecycle, and API usage. Use alongside this skill when developing HarmonyOS application code.
