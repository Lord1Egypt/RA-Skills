# Plan: wip-install bootstraps LDM OS silently

**Date:** 2026-03-13
**Issue:** new
**Status:** DONE. Code shipped in install.js (lines 740-812). ldm is on PATH (v0.4.6). npm bin issue resolved.

## Current behavior (install.js)

- Lines 740-776: If `ldm --version` succeeds, delegates to `ldm install` and exits
- Lines 879-888: If ldm NOT on PATH, prints tip: "Install LDM OS: npm install -g @wipcomputer/wip-ldm-os"

## New behavior

When `ldm` is NOT on PATH:
1. Print "Installing LDM OS infrastructure..."
2. Run `npm install -g @wipcomputer/wip-ldm-os`
3. Verify `ldm --version` works
4. If success: delegate to `ldm install` as normal, exit
5. If failure: fall through to standalone installer (current behavior)
6. Only print the "tip" if bootstrap also failed

## Code changes

**New function (~line 738):**
```javascript
function bootstrapLdmOs() {
  try {
    execSync('npm install -g @wipcomputer/wip-ldm-os', { stdio: 'pipe', timeout: 60000 });
    execSync('ldm --version', { stdio: 'pipe', timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}
```

**Modify delegation block (~line 740):**
```javascript
let ldmAvailable = false;
try {
  execSync('ldm --version', { stdio: 'pipe' });
  ldmAvailable = true;
} catch {
  // ldm not on PATH, try bootstrap
  if (!JSON_OUTPUT) console.log('  Installing LDM OS infrastructure...');
  if (bootstrapLdmOs()) {
    ldmAvailable = true;
    if (!JSON_OUTPUT) console.log('  LDM OS installed.');
  } else {
    if (!JSON_OUTPUT) console.log('  LDM OS install failed. Using standalone installer.');
  }
}

if (ldmAvailable) {
  // existing delegation code (exec ldm install, process.exit(0))
}
// else: fall through to standalone
```

**Modify tip block (~line 879):**
Only show "Install LDM OS" tip if bootstrap was attempted and failed. If ldm was bootstrapped, it already delegated and exited.

## Files

- `tools/wip-universal-installer/install.js` ... add bootstrapLdmOs(), modify delegation block

## Verify

```bash
# With ldm NOT on PATH:
wip-install /path/to/some-tool --dry-run   # shows bootstrap step
wip-install /path/to/some-tool             # installs ldm + tool
ldm --version                               # works
ldm status                                  # shows tool installed
```

## Release

- Branch: `cc-mini/bootstrap-ldm-os`
- PR to main, merge
- `wip-release patch --notes="wip-install bootstraps LDM OS silently"`
- Deploy to public

## Depends on

- **wip-ldm-os-private:** npm bin fix (issue #32)

## Parallel with

- **memory-crystal-private:** crystal init bootstrap (same pattern, different repo)
