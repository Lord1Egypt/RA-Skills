# CLI Capture: Fixing the Cron Scheduling

**Date:** 2026-03-02
**Author:** CC-Mini
**Status:** Needs fix (blocking Phase 1 completion)
**Priority:** Immediate

---

## The Problem

crystal-capture.sh runs every minute via cron. The script lives in iCloud Drive (ldm-os repo). Two issues:

1. **Bare cron can't access iCloud Drive.** macOS sandboxing blocks /bin/bash from reading iCloud-synced files without Full Disk Access.
2. **LDM Dev Tools.app fails at every-minute frequency.** `open -W` returns error -1712 (Launch Services error). The app approach works for once-a-day jobs but not for every-minute polling.

## Recommended Fix: Copy Script to ~/.ldm/bin/

The simplest solution. CLI users are advanced. The install process copies the script to a local, non-iCloud path.

```bash
# During install (crystal init or manual setup):
mkdir -p ~/.ldm/bin
cp crystal-capture.sh ~/.ldm/bin/crystal-capture.sh
chmod +x ~/.ldm/bin/crystal-capture.sh

# Cron entry (no FDA needed, ~/.ldm/ is not iCloud):
* * * * * ~/.ldm/bin/crystal-capture.sh >> /tmp/ldm-dev-tools/crystal-capture.log 2>&1
```

**Why this works:**
- ~/.ldm/ is a local directory, not iCloud-synced. No FDA needed.
- Bare cron can read/write to ~/.ldm/ without any app wrapper.
- The script itself uses $HOME which cron's bash expands fine.
- Simple, portable, works on any Mac or Linux.
- `crystal init` handles the copy during installation.

**Why this is better than the alternatives:**

| Approach | Problem |
|----------|---------|
| LDM Dev Tools.app (open -W) | Error -1712 at every-minute frequency |
| LaunchAgent plist | Parker doesn't want another plist. Also overkill for a simple script. |
| Bare cron + iCloud path | FDA blocks access |
| **~/.ldm/bin/ + bare cron** | **Works. Simple. Portable.** |

## What Changes

1. `crystal init` copies crystal-capture.sh to `~/.ldm/bin/`
2. `crystal init` installs cron entry pointing to `~/.ldm/bin/crystal-capture.sh`
3. Source of truth stays in the repo (ldm-jobs/crystal-capture.sh)
4. Deploy script copies to ~/.ldm/bin/ as part of the build/deploy step
5. LDM Dev Tools.app keeps crystal-capture.sh in its jobs/ folder for manual runs, but the cron doesn't use it

## For Parker's Setup (Immediate Fix)

```bash
mkdir -p ~/.ldm/bin
cp ~/Applications/LDMDevTools.app/Contents/Resources/jobs/crystal-capture.sh ~/.ldm/bin/
chmod +x ~/.ldm/bin/crystal-capture.sh

# Update crontab:
# Replace the open -W line with:
# * * * * * ~/.ldm/bin/crystal-capture.sh >> /tmp/ldm-dev-tools/crystal-capture.log 2>&1
```

This unblocks Phase 1 without any code changes. Just a path fix.
