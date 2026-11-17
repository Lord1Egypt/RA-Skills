#!/usr/bin/env node
// Regression test: boot-hook payload trimming (CC speedup master plan, Task 4b).
//
// Covers:
//   1. A step with no maxLines in config gets the code default cap + a
//      truncation marker that names the full path.
//   2. A per-step maxLines in config overrides the default.
//   3. A most-recent step whose newest file is older than stalenessDays is
//      NOT injected: a path-only stale line is emitted instead.
//   4. A fresh most-recent file IS injected in full.
//   5. The payload ends with a one-line summary (bytes/lines/sections, capped,
//      stale).
//   6. maxTotalLines still stops the loop early.
//
// The hook resolves homedir() into a module-level constant at import time and
// loads boot-config.json relative to its own file. So each case copies the
// hook into a temp workdir next to a generated boot-config.json and runs it as
// a subprocess with HOME pointed at a temp fixture. The hook's dynamic imports
// of ../../lib/*.mjs fail harmlessly (they are wrapped in try/catch) from the
// temp location, which is fine: this test only exercises payload assembly.

import { mkdirSync, mkdtempSync, copyFileSync, writeFileSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const repo = dirname(dirname(fileURLToPath(import.meta.url)));
const HOOK_SRC = join(repo, 'src', 'boot', 'boot-hook.mjs');

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

// Compute today/yesterday in the hook's timezone so daily-log and fresh-journal
// filenames match what the hook looks for.
function ymd(offsetDays = 0) {
  const now = new Date();
  now.setDate(now.getDate() + offsetDays);
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Los_Angeles',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(now);
}

function lines(n, marker) {
  const out = [];
  for (let i = 1; i <= n; i++) out.push(`${marker} line ${i}`);
  return out.join('\n') + '\n';
}

// Run the hook with a given config object and a HOME-populating callback.
// Returns the injected additionalContext string.
function runHook(configObj, populateHome) {
  const work = mkdtempSync(join(tmpdir(), 'ldm-bootpay-work-'));
  const home = mkdtempSync(join(tmpdir(), 'ldm-bootpay-home-'));
  try {
    copyFileSync(HOOK_SRC, join(work, 'boot-hook.mjs'));
    writeFileSync(join(work, 'boot-config.json'), JSON.stringify(configObj, null, 2));
    populateHome(home);

    const stdout = execFileSync('node', [join(work, 'boot-hook.mjs')], {
      input: JSON.stringify({ session_id: 'test', hook_event_name: 'SessionStart', cwd: home }),
      env: { ...process.env, HOME: home },
      encoding: 'utf-8',
      timeout: 30000,
    });
    const parsed = JSON.parse(stdout);
    return parsed?.hookSpecificOutput?.additionalContext || '';
  } finally {
    rmSync(work, { recursive: true, force: true });
    rmSync(home, { recursive: true, force: true });
  }
}

function writeHomeFile(home, rel, content) {
  const full = join(home, rel);
  mkdirSync(dirname(full), { recursive: true });
  writeFileSync(full, content);
  return full;
}

// ── Case 1 + 2 + 5: default cap, config override, payload summary ──
console.log('Case 1/2/5: default cap, config override, payload summary');
{
  const config = {
    agentId: 'test-agent',
    timezone: 'America/Los_Angeles',
    maxTotalLines: 2000,
    steps: {
      // no maxLines -> code default for sharedContext is 80
      sharedContext: { path: '~/shared.md', label: 'SHARED', stepNumber: 2, critical: true },
      // no maxLines -> code default for soul is 80
      soul: { path: '~/soul.md', label: 'SOUL', stepNumber: 7 },
      // explicit maxLines overrides
      overridden: { path: '~/capped.md', label: 'CAPPED', stepNumber: 11, maxLines: 5 },
    },
  };
  let soulPath, cappedPath;
  const ctx = runHook(config, (home) => {
    writeHomeFile(home, 'shared.md', lines(20, 'SHARED_BODY')); // under cap, not truncated
    soulPath = writeHomeFile(home, 'soul.md', lines(200, 'SOUL_BODY')); // over default 80
    cappedPath = writeHomeFile(home, 'capped.md', lines(100, 'CAP_BODY')); // over explicit 5
  });

  assert(/truncated at 80 of \d+ lines/.test(ctx), 'soul truncated at default cap 80', ctx.match(/truncated at[^\n]*soul[^\n]*/)?.[0] || ctx.slice(0, 300));
  assert(ctx.includes(`Read the rest: ${soulPath}`), 'soul truncation marker names full path');
  assert(/truncated at 5 of \d+ lines/.test(ctx), 'config maxLines=5 override respected');
  assert(ctx.includes(`Read the rest: ${cappedPath}`), 'capped truncation marker names full path');
  assert(/SHARED_BODY line 20\b/.test(ctx), 'under-cap file not truncated (body fully present)');
  const summaryLine = ctx.match(/== Boot payload:[^\n]*/)?.[0] || '';
  assert(/== Boot payload: \d+ bytes, \d+ lines, \d+ sections\./.test(summaryLine), 'payload summary line present', summaryLine);
  const cappedPart = summaryLine.match(/Capped:([^.]*)\./)?.[1] || '';
  assert(/Step 7\b/.test(cappedPart) && /Step 11\b/.test(cappedPart), 'summary lists capped steps 7 and 11', summaryLine);
  assert(/Stale\/path-only: none\./.test(summaryLine), 'summary reports no stale steps', summaryLine);
}

// ── Case 3: stale most-recent journal emits path-only line ──
console.log('Case 3: stale journal is path-only, body not injected');
{
  const config = {
    agentId: 'test-agent',
    timezone: 'America/Los_Angeles',
    maxTotalLines: 2000,
    stalenessDays: 14,
    steps: {
      ccJournals: { dir: '~/journals', label: 'JOURNAL', stepNumber: 8, maxLines: 80, strategy: 'most-recent' },
    },
  };
  const staleDate = ymd(-100);
  let journalPath;
  const ctx = runHook(config, (home) => {
    journalPath = writeHomeFile(home, `journals/${staleDate}-journal.md`, lines(50, 'STALE_JOURNAL_BODY'));
  });

  assert(!/STALE_JOURNAL_BODY/.test(ctx), 'stale journal body is NOT injected');
  assert(new RegExp(`stale: newest file is ${staleDate}`).test(ctx), 'stale line names the file date');
  assert(/cutoff 14d/.test(ctx), 'stale line names the cutoff');
  assert(ctx.includes(`Read if needed: ${journalPath}`), 'stale line names the full path');
  assert(/Stale\/path-only: Step 8\b/.test(ctx), 'summary lists stale step 8');
}

// ── Case 4: fresh most-recent journal is injected in full ──
console.log('Case 4: fresh journal body IS injected');
{
  const config = {
    agentId: 'test-agent',
    timezone: 'America/Los_Angeles',
    maxTotalLines: 2000,
    stalenessDays: 14,
    steps: {
      ccJournals: { dir: '~/journals', label: 'JOURNAL', stepNumber: 8, maxLines: 80, strategy: 'most-recent' },
    },
  };
  const freshDate = ymd(0);
  const ctx = runHook(config, (home) => {
    writeHomeFile(home, `journals/${freshDate}-journal.md`, lines(10, 'FRESH_JOURNAL_BODY'));
  });

  assert(/FRESH_JOURNAL_BODY line 1\b/.test(ctx), 'fresh journal body injected');
  assert(!/stale:/.test(ctx), 'no stale marker for fresh journal');
  assert(/Stale\/path-only: none\./.test(ctx), 'summary reports no stale steps');
}

// ── Case 6: maxTotalLines stops the loop early ──
console.log('Case 6: maxTotalLines respected');
{
  const config = {
    agentId: 'test-agent',
    timezone: 'America/Los_Angeles',
    maxTotalLines: 5, // tiny: first big step blows past it
    steps: {
      sharedContext: { path: '~/shared.md', label: 'SHARED', stepNumber: 2, critical: true },
      context: { path: '~/context.md', label: 'CONTEXT', stepNumber: 6, critical: true },
    },
  };
  const ctx = runHook(config, (home) => {
    writeHomeFile(home, 'shared.md', lines(40, 'FIRST_BODY'));
    writeHomeFile(home, 'context.md', lines(40, 'SECOND_BODY'));
  });

  assert(/FIRST_BODY line 1\b/.test(ctx), 'first step loaded');
  assert(!/SECOND_BODY/.test(ctx), 'second step skipped after maxTotalLines cap');
}

console.log('');
if (failed > 0) {
  console.log(`${failed} test(s) failed.`);
  process.exit(1);
}
console.log('All boot payload trim tests passed.');
