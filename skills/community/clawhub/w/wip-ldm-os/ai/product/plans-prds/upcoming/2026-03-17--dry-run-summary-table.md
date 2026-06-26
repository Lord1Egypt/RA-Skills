# Plan: ldm install --dry-run summary table

**Issue:** https://github.com/wipcomputer/wip-ldm-os/issues/80
**Status:** Upcoming
**Filed:** 2026-03-17

## Context

During March 16-17 dogfood, every `ldm install --dry-run` required the AI to manually construct a summary. The CLI version gap (v0.4.12 vs v0.4.15) was invisible in the output. `ldm status` already has this logic. The dry-run should too.

## What to change

**File:** `bin/ldm.js`, inside the `DRY_RUN` block of `cmdInstallCatalog()` (lines 715-744)

Add a summary block **before** the extension table (before line 726). Reuse existing patterns from `cmdStatus()` (lines 1050-1098) and `checkCliVersion()` (lines 126-140).

## Implementation

Insert at line 716 (after `if (DRY_RUN) {`):

```javascript
// Summary block
const cliLatest = (() => {
  try {
    return execSync('npm view @wipcomputer/wip-ldm-os version 2>/dev/null', {
      encoding: 'utf8', timeout: 10000,
    }).trim();
  } catch { return null; }
})();

const agentDirs = (() => {
  try {
    return readdirSync(join(LDM_ROOT, 'agents'), { withFileTypes: true })
      .filter(d => d.isDirectory()).map(d => d.name);
  } catch { return []; }
})();

const totalExtensions = Object.keys(reconciled).length;
const majorBumps = npmUpdates.filter(e => {
  const curMajor = parseInt(e.currentVersion.split('.')[0], 10);
  const latMajor = parseInt(e.latestVersion.split('.')[0], 10);
  return latMajor > curMajor;
});

console.log('');
console.log('  Summary');
console.log('  ────────────────────────────────────');

if (cliLatest && cliLatest !== PKG_VERSION) {
  console.log(`  LDM OS CLI       v${PKG_VERSION}  ->  v${cliLatest}  (run: npm install -g @wipcomputer/wip-ldm-os@${cliLatest})`);
} else {
  console.log(`  LDM OS CLI       v${PKG_VERSION} (latest)`);
}

if (npmUpdates.length > 0) {
  console.log(`  Extensions       ${totalExtensions} installed, ${npmUpdates.length} update(s)`);
} else {
  console.log(`  Extensions       ${totalExtensions} installed, all up to date`);
}

for (const m of majorBumps) {
  console.log(`  Major bump       ${m.name} v${m.currentVersion} -> v${m.latestVersion}`);
}

if (agentDirs.length > 0) {
  console.log(`  Agents           ${agentDirs.join(', ')} (no change)`);
}

console.log(`  Data             crystal.db, agent files, secrets (never touched)`);
console.log('');
```

Then the existing extension table follows unchanged.

## Existing code to reuse

- `PKG_VERSION` (line ~18): current CLI version from package.json
- `checkCliVersion()` (line 126): same npm view logic
- `LDM_ROOT` constant: path to ~/.ldm/
- `reconciled` (line 634): already computed before DRY_RUN block
- `npmUpdates` (line 713): already computed with currentVersion/latestVersion

## Verification

```bash
ldm install --dry-run
# Should show Summary block before the extension table
```
