# LDM OS Dogfood Bug Sweep (March 16-17, 2026)

Parker dogfooded LDM OS v0.3.0 through v0.4.14. Every step broke something. This documents all bugs found, fixes applied, and remaining work.

## Fixed This Session

| Bug | Fix | Release | Issue |
|-----|-----|---------|-------|
| Guard blocks non-repo files | Allow when findRepoRoot returns null | Toolbox v1.9.42 | #77 closed |
| UTC date in wip-release | Local date instead of toISOString (3 locations) | Toolbox v1.9.42 | #205 closed |
| Bridge unified session | Send user="main" to route CC to Parker's TUI session | LDM OS v0.4.15 | #76 closed |
| trashReleaseNotes crash | Check if file is tracked before git rm --cached | Toolbox v1.9.43 | #78 partial |
| Guard installed manually | Parker copied v1.9.42 guard.mjs to ~/.ldm/extensions/ | Manual hotfix | #77 |

## System Fixes Needed (no code changes)

These require Parker to run commands. The code bugs that caused them are already fixed in released versions.

### CRITICAL: /tmp/ symlinks (3 packages)

Three global npm packages symlinked to /private/tmp/. macOS cleans /tmp/ on reboot. One restart = dead CLIs.

```
memory-crystal -> /private/tmp/ldm-install-memory-crystal
wip-readme-format -> /private/tmp/ldm-install-wip-ai-devops-toolbox/tools/wip-readme-format
universal-installer -> /private/tmp/ldm-install-wip-ai-devops-toolbox/tools/wip-universal-installer
```

Fix: `npm install -g` from registry (copies files, no symlinks):
```bash
npm install -g @wipcomputer/memory-crystal@0.7.26
npm install -g @wipcomputer/wip-readme-format@1.9.43
npm install -g @wipcomputer/universal-installer@2.1.5
```

### HIGH: Orphaned /tmp/ dirs (5,173 dirs)
```bash
rm -rf /private/tmp/ldm-install-*
```

### HIGH: ldm CLI outdated (v0.4.12, latest v0.4.15)
```bash
npm install -g @wipcomputer/wip-ldm-os@0.4.15
```

### HIGH: crystal CLI missing
Should be restored by memory-crystal reinstall above. Verify:
```bash
which crystal && crystal --version
```

### LOW: registry.json "null" entry
```bash
ldm doctor --fix
```

## Still Open (needs future work)

| Bug | Severity | Notes |
|-----|----------|-------|
| ClawHub root publish timeout | LOW | Large repos timeout. Sub-tools succeed. Needs clawhub investigation. |
| #78 remaining sub-bugs | MEDIUM | Guard still blocks recovery ops (git stash, git checkout) on main after failed release. By design, but painful. |

## Root Causes

1. **ldm install used local clones in /tmp/** instead of npm registry installs. Fixed in code (#55 closed), but existing symlinks from old installs still present.
2. **wip-release used UTC dates** but dev-update files use local PST dates. 4 PM-midnight window broke detection.
3. **Guard fell back to CWD** when target file wasn't in any git repo. ~/.claude/plans/ and similar paths were incorrectly blocked.
4. **Bridge sent wrong user field** creating isolated sessions instead of routing to main session.
5. **trashReleaseNotes assumed files were tracked.** Scaffolded files from failed releases aren't in the git index.

## Verification Checklist

After all fixes applied:
- [ ] `ls -la /opt/homebrew/lib/node_modules/@wipcomputer/ | grep tmp` shows nothing
- [ ] `ldm --version` shows 0.4.15
- [ ] `crystal --version` shows 0.7.26
- [ ] `wip-release --version` shows 1.9.43
- [ ] `ldm doctor` shows no issues
- [ ] `ldm install --dry-run` shows no updates (or only expected ones)
- [ ] Write to ~/.claude/plans/ works from CC in ~/.openclaw
