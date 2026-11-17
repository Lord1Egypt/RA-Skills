#!/usr/bin/env node
// Regression test: manifest-driven boot-hook registration is single-owner.
//
// Covers:
//   ai/product/bugs/installer/open-tickets/2026-07-05--cc-mini--deploy-hook-ownership-misses-boot-hook.md
//
// Before this fix, lib/deploy.mjs installClaudeCodeHookEvent() matched owned
// hook entries by an extension-dir tag (`/<toolName>/`). The boot hook's
// deployed command is `node ~/.ldm/shared/boot/boot-hook.mjs`, which contains
// no `/wip-ldm-os/` segment, so the ownership match found nothing and appended
// a fresh SessionStart entry on every manifest-driven `ldm install` (the real
// mechanism behind the 10-entry accumulation on 2026-07-04).
//
// The fix routes boot-hook doors to configureSessionStartHook() (the single
// canonical registrar), so the deploy path no longer appends.
//
// Cases:
//   1. Fresh manifest install: exactly one boot entry, canonical command.
//   2. Repeat manifest install: byte-identical settings.json (true no-op).
//   3. Pre-accumulated + unrelated SessionStart hook: collapses boot entries
//      to one, preserves the non-boot SessionStart entry (discriminates on the
//      command, not the event).
//   4. Dry run: reports intent, writes nothing.
//
// HOME must be set before importing deploy.mjs: both deploy.mjs (process.env.HOME)
// and the transitively-imported src/boot/installer.mjs (os.homedir()) resolve
// their HOME-based constants at module-load time.

import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

// The temp prefix must not contain "boot-hook" or "shared/boot": those are the
// ownership matchers, and the temp HOME ends up inside every fixture command.
const tempHome = mkdtempSync(join(tmpdir(), 'ldm-deployown-'));
process.env.HOME = tempHome;

const { installClaudeCodeHook, setFlags } = await import('../lib/deploy.mjs');

// Mirror detect.mjs: the wip-ldm-os package.json declares a single SessionStart
// boot-hook door. deploy.mjs receives it as a one-element array.
const bootDoor = {
  event: 'SessionStart',
  matcher: '*',
  command: `node ${join(tempHome, '.ldm', 'shared', 'boot', 'boot-hook.mjs')}`,
  timeout: 15,
};
const expectedCommand = `node ${join(tempHome, '.ldm', 'shared', 'boot', 'boot-hook.mjs')}`;

let failed = 0;
function assert(cond, label, detail = '') {
  if (cond) {
    console.log(`  [PASS] ${label}`);
  } else {
    console.log(`  [FAIL] ${label}`);
    if (detail) console.log(`         ${detail}`);
    failed++;
  }
}

const settingsPath = join(tempHome, '.claude', 'settings.json');
function seedSettings(obj) {
  mkdirSync(join(tempHome, '.claude'), { recursive: true });
  writeFileSync(settingsPath, JSON.stringify(obj, null, 2) + '\n');
}
function readSettings() {
  return JSON.parse(readFileSync(settingsPath, 'utf-8'));
}
function bootEntries(settings) {
  return (settings.hooks?.SessionStart || []).filter((entry) =>
    (entry?.hooks || []).some((h) => h?.command?.includes('boot-hook'))
  );
}
// Install through the manifest wrapper exactly as detect.mjs feeds it: an array.
function manifestInstall() {
  return installClaudeCodeHook(join(tempHome, 'repo'), [bootDoor], 'wip-ldm-os');
}

try {
  console.log('Test 1: fresh manifest install adds exactly one boot entry');
  {
    seedSettings({ hooks: {} });
    manifestInstall();
    const s = readSettings();
    assert(bootEntries(s).length === 1, 'exactly one boot-hook SessionStart entry');
    assert(
      s.hooks.SessionStart[0].hooks[0].command === expectedCommand,
      'command canonicalized to BOOT_DIR boot-hook.mjs',
      `on disk: ${s.hooks.SessionStart[0].hooks[0].command}`
    );
  }

  console.log('Test 2: repeat manifest install is a byte-identical no-op');
  {
    const before = readFileSync(settingsPath, 'utf-8');
    manifestInstall();
    const after = readFileSync(settingsPath, 'utf-8');
    assert(before === after, 'settings.json byte-identical after second manifest install');
    assert(bootEntries(readSettings()).length === 1, 'still exactly one boot-hook entry (no append)');
  }

  console.log('Test 3: pre-accumulated boot entries collapse; unrelated SessionStart hook preserved');
  {
    // Three legacy boot appends (the pre-fix accumulation) using the old
    // hardcoded absolute path, plus an unrelated SessionStart guard entry.
    const legacyBoot = {
      matcher: '*',
      hooks: [{ type: 'command', command: 'node /Users/someone/.ldm/shared/boot/boot-hook.mjs', timeout: 15 }],
    };
    const guardSessionStart = {
      matcher: 'Read|Glob',
      hooks: [{ type: 'command', command: `node ${join(tempHome, '.ldm', 'extensions', 'wip-branch-guard', 'guard.mjs')}`, timeout: 10 }],
    };
    seedSettings({
      hooks: {
        SessionStart: [
          structuredClone(legacyBoot),
          structuredClone(legacyBoot),
          guardSessionStart,
          structuredClone(legacyBoot),
        ],
      },
    });
    manifestInstall();
    const s = readSettings();
    assert(bootEntries(s).length === 1, 'boot entries collapsed to one');
    assert(
      s.hooks.SessionStart[0].hooks[0].command === expectedCommand,
      'surviving boot entry canonicalized to BOOT_DIR'
    );
    assert(
      s.hooks.SessionStart.some((e) => e.hooks?.[0]?.command?.includes('wip-branch-guard')),
      'unrelated SessionStart guard entry preserved (discriminates on command, not event)'
    );
    assert(s.hooks.SessionStart.length === 2, 'exactly boot + guard remain');
  }

  console.log('Test 4: dry run reports intent and writes nothing');
  {
    seedSettings({ hooks: {} });
    const before = readFileSync(settingsPath, 'utf-8');
    setFlags({ dryRun: true });
    try {
      manifestInstall();
    } finally {
      setFlags({ dryRun: false });
    }
    const after = readFileSync(settingsPath, 'utf-8');
    assert(before === after, 'settings.json untouched under dry run');
    assert(bootEntries(readSettings()).length === 0, 'no boot entry written under dry run');
  }
} finally {
  rmSync(tempHome, { recursive: true, force: true });
}

if (failed > 0) {
  console.log(`\n${failed} assertion(s) failed`);
  process.exit(1);
}
console.log('\nAll deploy-hook ownership tests passed');
