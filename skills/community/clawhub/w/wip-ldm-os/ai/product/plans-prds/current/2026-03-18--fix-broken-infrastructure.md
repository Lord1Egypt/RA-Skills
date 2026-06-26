# Plan: Fix Broken Infrastructure (#120, #121, #125)

## Context

Health check found 7 broken things after folder restructure and LDM installer work. Three quick local fixes done (#122 op-secrets rename, #123 broken symlinks, #124 ghost extensions). Three remain: logs in /tmp/ (#120), healthcheck dead (#121), gateway logs bloated (#125). Tickets filed on wipcomputer/wip-ldm-os.

## Phase 0: Truncate gateway logs (#125)

Live system. No repo changes.

1. Truncate both logs (preserves file descriptor):
   ```bash
   : > ~/.openclaw/logs/gateway.err.log
   : > ~/.openclaw/logs/gateway.log
   ```
2. Restart gateway so the wip-1password config fix takes effect:
   ```bash
   openclaw gateway restart
   ```
3. Verify no more op-secrets spam in logs

## Phase 1: memory-crystal-private source fixes (#120)

**Repo:** `components/memory-crystal-private/`
**Branch:** `cc-mini/logs-to-ldm-home`

### Files to edit

**src/ldm.ts:**
- Line 188: CRON_ENTRY `/tmp/ldm-dev-tools/crystal-capture.log` -> `~/.ldm/logs/crystal-capture.log`
- Line 198: `mkdirSync('/tmp/ldm-dev-tools')` -> `mkdirSync(join(HOME, '.ldm', 'logs'))`
- Lines 286-288: LaunchAgent plist template `/tmp/ldm-dev-tools/ldm-backup.log` -> `${HOME}/.ldm/logs/ldm-backup.log`

**src/cli.ts:**
- Line 184: Console output `/tmp/ldm-dev-tools/ldm-backup.log` -> `~/.ldm/logs/ldm-backup.log`

### Git workflow
1. `git checkout -b cc-mini/logs-to-ldm-home`
2. Edit src/ldm.ts and src/cli.ts
3. `npm run build` to verify
4. Commit, push, PR, merge (--merge, never squash)
5. `wip-release patch --notes="Move log paths from /tmp/ to ~/.ldm/logs/"`
6. `deploy-public.sh` to sync public repo

## Phase 2: wip-healthcheck install.sh (#120 + #121)

**Repo:** `utilities/wip-healthcheck-private/`
**Note:** Public repo is at `_to-privatize/wip-healthcheck/` (not split yet)

### File to edit

**install.sh:**
- Line 10: `LOG_DIR="/tmp/openclaw"` -> `LOG_DIR="$HOME/.ldm/logs"`

This fixes both issues: log path (#120) and when re-run, regenerates the plist with the correct script path (#121).

### Git workflow
Same pattern: branch, edit, commit, PR, merge, wip-release.

## Phase 3: Live system updates (#120 + #121)

After repos merged and released:

### 3a. Update deployed scripts
- `~/.ldm/bin/process-monitor.sh` line 6: `LOG="/tmp/ldm-process-monitor.log"` -> `LOG="$HOME/.ldm/logs/process-monitor.log"`
- `~/.ldm/bin/crystal-capture.sh` line 10: update comment

### 3b. Update crontab
```bash
# Replace /tmp/ldm-dev-tools/ with ~/.ldm/logs/ in all entries
crontab -l | sed 's|/tmp/ldm-dev-tools/|~/.ldm/logs/|g' | crontab -
```

### 3c. Reinstall healthcheck
Run the updated install.sh to regenerate the LaunchAgent plist with:
- Correct script path (fixes #121)
- ~/.ldm/logs/ for log output (fixes #120)

### 3d. Regenerate ldm-backup plist
After updated memory-crystal is installed, `crystal init` or `crystal backup setup` regenerates the plist with ~/.ldm/logs/ paths.

## Execution order

- Phase 0 first (immediate relief, independent)
- Phases 1 and 2 in parallel (different repos)
- Phase 3 after both repos merged

## Out of scope

- mlx-setup.ts /tmp/mlx-server.log (MLX server writes there, different issue)
- wip-healthcheck-private install.sh sibling path mismatch (pre-existing from restructure)
- Log rotation (separate issue to prevent future bloat)

## Verification

```bash
# After all phases:
grep -r "/tmp/" ~/.ldm/bin/                    # should find nothing
crontab -l | grep "/tmp/"                      # should find nothing
grep "/tmp/" ~/Library/LaunchAgents/ai.openclaw.*.plist  # should find nothing
ls ~/.ldm/logs/                                # should see log files appearing
tail -5 ~/.ldm/logs/crystal-capture.log        # verify capture logging
```
