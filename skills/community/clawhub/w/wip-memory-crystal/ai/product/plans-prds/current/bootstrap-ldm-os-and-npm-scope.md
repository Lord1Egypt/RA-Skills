# Plan: crystal init bootstraps LDM OS + npm scoping rename

**Date:** 2026-03-13
**Issues:** #46 (scoping), new (bootstrap)
**Status:** Ready (blocked on LDM OS bin fix)

## Part A: Silent LDM OS bootstrap

### Current behavior (src/installer.ts)

- Lines 490-497: `ldmCliAvailable()` checks if `ldm --version` works
- Lines 566-588: If ldm on PATH, delegates generic install to `ldm install`
- Lines 807-812: If ldm NOT on PATH, prints tip: "Install LDM OS: npm install -g @wipcomputer/wip-ldm-os"

### New behavior

When `ldm` is NOT on PATH:
1. Print "Installing LDM OS infrastructure..."
2. Run `npm install -g @wipcomputer/wip-ldm-os`
3. Verify `ldm --version` works
4. If success: delegate to `ldm install` as normal, set `ldmDelegated = true`
5. If failure (npm offline, permissions, etc.): fall through to self-contained behavior
6. Only print the "tip" if bootstrap also failed

### Code changes

**New function (~line 498):**
```typescript
function bootstrapLdmOs(): boolean {
  try {
    execSync('npm install -g @wipcomputer/wip-ldm-os', { stdio: 'pipe', timeout: 60000 });
    // Verify it worked
    execSync('ldm --version', { stdio: 'pipe', timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}
```

**Modify delegation block (~line 566):**
```typescript
let hasLdmCli = ldmCliAvailable();

if (!hasLdmCli) {
  steps.push('Installing LDM OS infrastructure...');
  if (bootstrapLdmOs()) {
    hasLdmCli = true;
    steps.push('LDM OS installed successfully.');
  } else {
    steps.push('LDM OS install failed (npm offline?). Using standalone installer.');
  }
}

if (hasLdmCli) {
  // existing delegation code...
}
```

**Modify tip block (~line 807):**
Only show "Install LDM OS" tip if bootstrap was attempted and failed.

## Part B: npm scoping rename

Change `memory-crystal` to `@wipcomputer/memory-crystal`.

### Files to update

**This repo:**
1. `package.json` ... name field
2. `skills/memory/SKILL.md` ... install instructions (`npm install -g memory-crystal` becomes `npm install -g @wipcomputer/memory-crystal`)

**Cross-repo (same branch or coordinated):**
3. `wip-ldm-os-private/catalog.json` ... npm field
4. `wip-ldm-os-private/SKILL.md` ... install examples
5. `wip-ldm-os-private/bin/ldm.mjs` ... catalog ID check (line 262)
6. `wip-ai-devops-toolbox-private/tools/ldm-jobs/crystal-capture.sh` ... path ref
7. `open-claw-upgrade-private/UPGRADE-RUNBOOK.md` ... build/install steps

### Post-rename
```bash
npm deprecate memory-crystal "Moved to @wipcomputer/memory-crystal"
```

## Verify

```bash
# Bootstrap test (with ldm NOT on PATH):
crystal init --dry-run       # shows "Installing LDM OS..." step
crystal init                 # installs ldm + MC
ldm --version                # works (bootstrapped)
ldm status                   # shows MC as installed

# Scoping test:
npm info @wipcomputer/memory-crystal   # new name works
npm info memory-crystal                # shows deprecation notice
```

## Release

- Branch: `cc-mini/bootstrap-ldm-os`
- PR to main, merge
- `wip-release patch --notes="crystal init bootstraps LDM OS silently, npm scoped to @wipcomputer/memory-crystal"`
- Deploy to public
- Run `npm deprecate memory-crystal "Moved to @wipcomputer/memory-crystal"`

## Depends on

- **wip-ldm-os-private:** npm bin fix (issue #32). Without working bin entries, `npm install -g @wipcomputer/wip-ldm-os` won't create the `ldm` command.

## Unblocks

- Clean GitHub Packages publishing (no more 404)
- Any entry point installs the full ecosystem
