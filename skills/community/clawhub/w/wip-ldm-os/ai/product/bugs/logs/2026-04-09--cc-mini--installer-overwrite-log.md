# CRITICAL: Installer does not log file overwrites

**Date:** 2026-04-09
**Reporter:** cc-mini (with Parker)
**Component:** ldm install
**Severity:** critical

## Problem

When `ldm install` runs, it deploys scripts, docs, rules, hooks, and extensions. It overwrites existing files without logging what changed. There is no record of:
- Which files were overwritten
- Whether the content changed
- What the old content was
- What the new content is

This caused multiple incidents on 2026-04-08 and 2026-04-09:
- `~/.claude/CLAUDE.md` overwritten from 349 lines to 41 lines (Level 1 template destroyed full system instructions)
- `~/.ldm/hooks/pre-commit` destroyed by `git lfs install` (no log showing it was overwritten)
- `~/.ldm/shared/` contents emptied by stash operation (no log showing what was removed)
- Home docs at `~/wipcomputerinc/library/documentation/` overwritten with stale templates (no log)

In every case, we didn't know the overwrite happened until something broke.

## What the installer must log

Every file the installer writes must be logged to `~/.ldm/logs/install.log` with:

```
[2026-04-09 14:50:23] WRITE ~/.ldm/bin/ldm-backup.sh
  existed: yes
  changed: yes
  old_size: 4521 bytes
  new_size: 4892 bytes
  old_hash: sha256:abc123...
  new_hash: sha256:def456...
  source: wip-ldm-os-private/scripts/ldm-backup.sh
```

For files that didn't change:
```
[2026-04-09 14:50:23] SKIP ~/.ldm/bin/ldm-backup.sh (unchanged)
```

For new files:
```
[2026-04-09 14:50:23] CREATE ~/.ldm/library/documentation/how-agents-work.md
  size: 3200 bytes
  source: wip-ldm-os-private/shared/docs/how-agents-work.md.tmpl
```

## What needs to change

### 1. Add logging wrapper for file writes

Every `cpSync`, `writeFileSync`, and `cpSync` in the installer should go through a wrapper:

```javascript
function deployFile(src, dest, label) {
  const existed = existsSync(dest);
  const oldHash = existed ? hashFile(dest) : null;
  cpSync(src, dest);
  const newHash = hashFile(dest);
  const changed = oldHash !== newHash;
  
  installLog(`${changed ? 'WRITE' : 'SKIP'} ${dest} ${changed ? '(changed)' : '(unchanged)'}`, {
    existed, changed,
    oldSize: existed ? statSync(dest).size : 0,
    newSize: statSync(dest).size,
    source: label
  });
}
```

### 2. Separate overwrite log

In addition to install.log (which has general install output), create `~/.ldm/logs/deploy-manifest.log` that is ONLY file operations. One line per file. Machine-readable. Can be diffed between installs.

### 3. Verification after install

After deploying, read the deploy manifest and verify:
- All files that were written still exist
- No unexpected files were created (files on disk that aren't in the manifest)
- Hash of each file matches what was deployed

### 4. Documentation

Update `~/.ldm/library/documentation/logs/install-log.md` when this is built. Remove the "CRITICAL: Missing overwrite tracking" notice and document the new format.

## Files to change

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/bin/ldm.js` ... wrap file operations with logging
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/lib/deploy.mjs` ... same for extension deployment

## Related

- `~/.ldm/library/documentation/logs/install-log.md` (documents the gap)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/ldmos-core/2026-04-09--cc-mini--config-and-doc-deploy-pipeline.md`
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/installer/2026-04-09--cc-mini--installer-must-generate-extension-docs.md`
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/wip-code/2026-03-27--cc-mini--single-source-of-truth-reversed.md` (the CLAUDE.md overwrite incident)
