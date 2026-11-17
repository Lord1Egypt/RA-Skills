#!/usr/bin/env node
// Regression test: configureSessionStartHook() registration semantics.
//
// Covers the 2026-07-04 tickets:
//   ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--boot-hook-update-in-place-never-persists.md
//   ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--installer-sessionstart-hook-duplicate-registration.md
//
// Cases:
//   1. Fresh install: entry added and persisted.
//   2. Repeat run: no duplicate, file byte-identical (no write).
//   3. Changed entry (old command path, old timeout): updated ON DISK.
//      This is the update-in-place-never-persists bug.
//   4. Duplicate-laden settings (10 boot-hook copies + 1 unrelated hook):
//      collapses to 1 boot entry, unrelated hook preserved, persisted.

import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

// Note: the temp prefix must not contain "boot-hook" or "shared/boot".
// Those substrings are the installer's ownership matchers, and the temp
// HOME path ends up inside every fixture hook command.
const tempHome = mkdtempSync(join(tmpdir(), 'ldm-bootreg-'));

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

try {
  // HOME must be set before the module import: installer.mjs resolves
  // homedir() into module-level constants at import time.
  process.env.HOME = tempHome;
  const { configureSessionStartHook } = await import('../src/boot/installer.mjs');
  const expectedCommand = `node ${join(tempHome, '.ldm', 'shared', 'boot', 'boot-hook.mjs')}`;

  console.log('Test 1: fresh install adds and persists the entry');
  {
    seedSettings({ hooks: {} });
    const msg = configureSessionStartHook();
    const s = readSettings();
    assert(/added/.test(msg), `reports added (got: ${msg})`);
    assert(bootEntries(s).length === 1, 'exactly one boot-hook entry on disk');
    assert(s.hooks.SessionStart[0].hooks[0].command === expectedCommand, 'command path is BOOT_DIR boot-hook.mjs');
  }

  console.log('Test 2: repeat run is a no-op, byte-identical file');
  {
    const before = readFileSync(settingsPath, 'utf-8');
    const msg = configureSessionStartHook();
    const after = readFileSync(settingsPath, 'utf-8');
    assert(/already configured/.test(msg), `reports already configured (got: ${msg})`);
    assert(before === after, 'settings.json byte-identical after second run');
  }

  console.log('Test 3: changed entry is updated ON DISK (the persist bug)');
  {
    seedSettings({
      hooks: {
        SessionStart: [
          {
            matcher: '*',
            hooks: [{ type: 'command', command: 'node /old/path/shared/boot/boot-hook.mjs', timeout: 10 }],
          },
        ],
      },
    });
    const msg = configureSessionStartHook();
    const s = readSettings();
    assert(/updated/.test(msg), `reports updated (got: ${msg})`);
    assert(bootEntries(s).length === 1, 'still exactly one boot-hook entry');
    assert(
      s.hooks.SessionStart[0].hooks[0].command === expectedCommand,
      'new command path persisted to disk',
      `on disk: ${s.hooks.SessionStart[0].hooks[0].command}`
    );
    assert(s.hooks.SessionStart[0].hooks[0].timeout === 15, 'new timeout persisted to disk');
  }

  console.log('Test 4: duplicate-laden settings collapse to one, unrelated hooks preserved');
  {
    const bootEntry = {
      matcher: '*',
      hooks: [{ type: 'command', command: expectedCommand, timeout: 15 }],
    };
    const guardEntry = {
      hooks: [{ type: 'command', command: `node ${join(tempHome, '.ldm', 'extensions', 'wip-branch-guard', 'guard.mjs')}`, timeout: 10 }],
    };
    seedSettings({
      hooks: {
        SessionStart: [
          ...Array.from({ length: 5 }, () => structuredClone(bootEntry)),
          guardEntry,
          ...Array.from({ length: 5 }, () => structuredClone(bootEntry)),
        ],
      },
    });
    const msg = configureSessionStartHook();
    const s = readSettings();
    assert(/removed 9 duplicate entries/.test(msg), `reports 9 duplicates removed (got: ${msg})`);
    assert(bootEntries(s).length === 1, 'exactly one boot-hook entry after collapse');
    assert(s.hooks.SessionStart.length === 2, 'boot hook + branch guard remain');
    assert(
      s.hooks.SessionStart.some((e) => e.hooks?.[0]?.command?.includes('wip-branch-guard')),
      'unrelated branch-guard entry preserved'
    );
  }
} finally {
  rmSync(tempHome, { recursive: true, force: true });
}

if (failed > 0) {
  console.log(`\n${failed} assertion(s) failed`);
  process.exit(1);
}
console.log('\nAll boot-hook registration tests passed');
