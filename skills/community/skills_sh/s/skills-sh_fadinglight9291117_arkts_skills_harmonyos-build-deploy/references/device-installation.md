# Device Installation Guide

Detailed guide for verifying build outputs and automating device installation. This supplements the main [SKILL.md](../SKILL.md) with version verification scripts and an installation script.

**Note:** All device paths use `//` prefix for Git Bash compatibility on Windows.

**Git Bash on Windows (IMPORTANT):** disable MSYS path conversion for `hdc`.

Without this, MSYS may rewrite paths and `hdc file send` can behave unexpectedly.

```bash
export MSYS_NO_PATHCONV=1
```

## Common Errors

### `install file path invalid`

This means the path passed to `bm install -p` does not directly contain any `.hap`/`.hsp` files.

The recommended workflow (see [SKILL.md](../SKILL.md)) pushes each file to an explicit remote file path, which avoids this problem. The error typically occurs only when pushing a **whole directory**: `hdc file send` preserves the local directory name on the device, so pushing `outputs/` to `$REMOTE_PATH/` places the artifacts under `$REMOTE_PATH/outputs/`, not `$REMOTE_PATH/`.

To diagnose, check where the files actually landed:

```bash
hdc -t "$DEVICE_ID" shell "find $REMOTE_PATH -maxdepth 2 -type f -print"
```

Then point `bm install -p` at the directory that directly contains the packages. If you are on Git Bash, also ensure `MSYS_NO_PATHCONV=1` is set before running `hdc`.

## Prerequisites

- **hdc**: HarmonyOS Device Connector (included in HarmonyOS SDK)
- **Device**: HarmonyOS device with USB debugging enabled
- **Build Output**: Signed HAP/HSP files from `hvigorw assembleApp`

## Verifying Build Outputs Before Installation

All HAP/HSP modules must have the **same versionCode**. Mismatched versions cause `"version code not same"` errors during installation.

### Check versionCode of All Modules

```bash
# Using Python (cross-platform)
python3 -c "
import zipfile, json, glob
for f in glob.glob('outputs/*.hap') + glob.glob('outputs/*.hsp'):
    z = zipfile.ZipFile(f)
    data = json.loads(z.read('module.json'))
    print(f\"{f.split('/')[-1]}: versionCode = {data['app']['versionCode']}\")
"

# Using unzip + grep (Linux/macOS)
for f in outputs/*.hap outputs/*.hsp; do
    [ -f "$f" ] || continue
    echo -n "$(basename $f): "
    unzip -p "$f" module.json | grep -o '"versionCode":[0-9]*'
done
```

### Identifying Problematic Modules

A module should be removed from the output before installation if:

1. Module directory has no `src/` folder (precompiled binary only)
2. Module not listed in `build-profile.json5` modules array
3. Module versionCode differs from `AppScope/app.json5`

```bash
rm outputs/problematic-module-default-signed.hsp
```

## Quick Installation Script

Save as `install.sh` (Linux/macOS/Git Bash):

```bash
#!/bin/bash

# === Configuration ===
# hdc prints "[Empty]" (not empty output) when no device is connected;
# strip \r for Git Bash on Windows.
DEVICE_ID="${1:-$(hdc list targets | tr -d '\r' | grep -v '^\[Empty\]$' | head -1)}"
SIGNED_PATH="${2:-outputs}"
BUNDLE_NAME="${3:-}"
REMOTE_PATH="//data/local/tmp/install_$(date +%s)"

# Disable MSYS path conversion (Git Bash on Windows)
export MSYS_NO_PATHCONV=1

if [ -z "$DEVICE_ID" ]; then
    echo "Error: No device found. Connect a device or specify UDID as first argument."
    exit 1
fi

echo "Device: $DEVICE_ID"
echo "Source: $SIGNED_PATH"
echo "Remote: $REMOTE_PATH"

# === Create remote directory ===
hdc -t "$DEVICE_ID" shell "mkdir -p $REMOTE_PATH"

# === Push only .hap and .hsp files (one-by-one) to explicit remote file paths ===
for f in "$SIGNED_PATH"/*.hap "$SIGNED_PATH"/*.hsp; do
    [ -f "$f" ] && hdc -t "$DEVICE_ID" file send "$f" "$REMOTE_PATH/$(basename "$f")"
done

# === Install (reinstall) ===
# Install HSPs first, then the HAP.
for f in "$SIGNED_PATH"/*.hsp "$SIGNED_PATH"/*.hap; do
    [ -f "$f" ] && hdc -t "$DEVICE_ID" shell "bm install -p $REMOTE_PATH/$(basename \"$f\") -r"
done

# === Clean up ===
hdc -t "$DEVICE_ID" shell "rm -rf $REMOTE_PATH"

echo ""
echo "Installation complete!"

# === Optional: Launch app ===
if [ -n "$BUNDLE_NAME" ]; then
    echo "Launching $BUNDLE_NAME..."
    hdc -t "$DEVICE_ID" shell "aa start -a EntryAbility -b $BUNDLE_NAME"
fi
```

Usage:

```bash
# Auto-detect device, use default path
./install.sh

# Specify device UDID
./install.sh 1234567890ABCDEF

# Specify device and path
./install.sh 1234567890ABCDEF outputs

# Specify device, path, and bundle name (auto-launch)
./install.sh 1234567890ABCDEF outputs com.example.app
```
