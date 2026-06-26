---
name: rpm-ostree-toolkit
description: Immutable OS management for Fedora Atomic / Bazzite — rpm-ostree layering, rollbacks, rebasing, system upgrades
version: 1.0.0
tags:
  - rpm-ostree
  - bazzite
  - fedora-atomic
  - silverblue
  - immutable
  - system
  - linux
metadata:
  {"openclaw": {"requires": {"bins": ["rpm-ostree"], "anyBins": ["ostree"]}, "os": ["linux"]}}
---

# rpm-ostree Toolkit

Manage Fedora Atomic / Bazzite immutable OS through rpm-ostree layering, rollbacks, and rebasing.

## When to Use

- User asks about system updates, rollbacks, or package management on immutable OS
- Installing packages on Bazzite / Fedora Silverblue / Kinoite
- Rebase to new deployment or track different remote
- Check deployment history or pending updates
- Troubleshoot rpm-ostree conflicts or overlay issues

## Prerequisites

- rpm-ostree installed (default on Fedora Atomic / Bazzite)
- Root or wheel privileges for `rpm-ostree` commands

## Core Concepts

rpm-ostree manages an immutable base filesystem + layered packages. Unlike dnf, changes require a deployment reboot.

**Immutable base** → **Layered packages** → **Reboot to apply**

## Commands Reference

### System Status

```bash
# Current deployment info
rpm-ostree status

# Show only current deployment
rpm-ostree status --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
deployments = d.get('deployments', [])
if deployments:
    c = deployments[0]
    print(f\"OS: {c.get('osname','?')}\")
    print(f\"Version: {c.get('version','?')}\")
    print(f\"Base: {c.get('base-commit','?')[:12]}\")
    print(f\"Booted: {c.get('booted',False)}\")
    print(f\"Layered: {len(c.get('requested-packages',[]))} packages\")
    print(f\"Pending: {len(c.get('requested-local-packages',[]))} local pkgs\")
"

# Check for available updates
rpm-ostree upgrade --check 2>&1

# Pending transactions
rpm-ostree dbus-xml 2>/dev/null | head -5
```

### Installing Packages

```bash
# Install a package (creates new layer)
rpm-ostree install <package>

# Install multiple packages
rpm-ostree install gh vim tmux htop

# Install from URL (RPM)
rpm-ostree install https://example.com/package.rpm

# Overlay from local RPM
rpm-ostree overlay /path/to/package.rpm
```

### Removing Packages

```bash
# Remove a layered package
rpm-ostree uninstall <package>

# Remove multiple
rpm-ostree uninstall package1 package2

# Remove all overlays and reset to base
rpm-ostree override reset
```

### System Updates

```bash
# Check for updates (no apply)
rpm-ostree upgrade --check

# Apply update (requires reboot)
rpm-ostree upgrade

# Apply and reboot
rpm-ostree upgrade && systemctl reboot
```

### Rollbacks

```bash
# Rollback to previous deployment
rpm-ostree rollback

# List all deployments
rpm-ostree status

# Pin current deployment (prevent GC)
rpm-ostree pin

# Unpin
rpm-ostree pin --remove
```

### Rebasing

```bash
# Rebase to different remote/branch
rpm-ostree rebase fedora:fedora/40/x86_64/silverblue

# Rebase to Bazzite
rpm-ostree rebase ostree-image-signed:docker://ghcr.io/ublue-os/bazzite:stable

# Cancel pending rebase
rpm-ostree rebase --cancel

# Check pending rebase
rpm-ostree status | head -5
```

### Overlays & Overrides

```bash
# Override a base package with specific version
rpm-ostree override replace <rpm-url>

# Remove a package from base (create exclude)
rpm-ostree override remove <package>

# Reset all overrides
rpm-ostree override reset
```

### Kernel Management

```bash
# List available kernels
rpm-ostree kdump list 2>/dev/null

# Current kernel args
rpm-ostree kargs

# Modify kernel args
rpm-ostree kargs --append=nvidia-drm.modeset=1

# Reset kernel args to default
rpm-ostree kargs --reset
```

### Cleaning Up

```bash
# Remove old deployments (keep 2)
rpm-ostree cleanup -rp

# Remove only pending deployments
rpm-ostree cleanup -p

# Remove cached data
rpm-ostree cleanup -m
```

### Conflicts & Troubleshooting

```bash
# When package conflicts with base
rpm-ostree override replace <url>  # replace the conflicting package

# When layering fails
rpm-ostree cancel  # cancel pending transaction

# When deployment is corrupted
rpm-ostree rollback  # boot into previous

# Check transaction log
journalctl -u rpm-ostreed --since "1 hour ago" --no-pager | tail -30
```

## Common Tasks

### Install GitHub CLI on Bazzite

```bash
rpm-ostree install gh
# Reboot to apply
systemctl reboot
```

### Rebase from Silverblue to Bazzite

```bash
rpm-ostree rebase ostree-image-signed:docker://ghcr.io/ublue-os/bazzite:stable
systemctl reboot
```

### Check if update needed

```bash
# Returns exit code 0 if updates available, 1 if not
if rpm-ostree upgrade --check 2>&1 | grep -q "Upgrade available"; then
  echo "Updates available"
else
  echo "System is up to date"
fi
```

## Important Notes

- **Every layering change requires reboot** to take effect
- **Rollback is instant** — just boot into previous deployment
- **No partial updates** — the entire base is atomic
- `rpm-ostree install` ≠ `dnf install` — layered, not mutable
- Use `flatpak` for GUI apps, `rpm-ostree` for CLI/system packages
- Bazzite uses `ublue-os` signing keys
