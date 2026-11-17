#!/usr/bin/env node
// Fixture test for the Phase 1 source-types migration planner.
// See lib/registry-migrations.mjs and
// ai/product/bugs/installer/2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md

import { mkdtempSync, mkdirSync, writeFileSync, existsSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import {
  planLegacyNpmSourcesMigration,
  summaryHasChanges,
  emptyLegacyNpmSourcesSummary,
  executeDirectoryMoves,
} from '../lib/registry-migrations.mjs';

function fail(msg) {
  throw new Error(msg);
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    fail(`${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertDeepEqual(actual, expected, label) {
  const a = JSON.stringify(actual, Object.keys(actual || {}).sort());
  const e = JSON.stringify(expected, Object.keys(expected || {}).sort());
  if (a !== e) {
    fail(`${label}: expected ${e}, got ${a}`);
  }
}

// Mirrors the shape we see on Parker's machine in the 2026-05-13 dogfood.
function buildFixtureRegistry() {
  return {
    _format: 'v2',
    extensions: {
      // 404 npm + on-disk: should migrate to untracked.
      'cc-session-export': {
        source: { type: 'github', npm: 'session-export', repo: 'wipcomputer/cc-session-export' },
        installed: { version: '1.0.0' },
      },
      // Duplicate of cc-session-export: should be deduped (removed).
      'session-export': {
        source: { type: 'github', npm: 'session-export' },
        installed: { version: '1.0.0' },
      },
      'compaction-indicator': {
        source: { type: 'github', npm: 'compaction-indicator' },
        installed: { version: '1.0.1' },
      },
      'lesa-bridge': {
        source: { type: 'github', npm: 'lesa-bridge' },
        installed: { version: '0.3.0' },
      },
      // Duplicate of wip-branch-guard: should be deduped.
      'package': {
        source: { type: 'github', npm: '@wipcomputer/wip-branch-guard' },
        installed: { version: '1.0.0' },
      },
      'wip-branch-guard': {
        source: { type: 'github', npm: '@wipcomputer/wip-branch-guard' },
        installed: { version: '1.0.0' },
      },
      // Real npm package: should be left alone.
      'memory-crystal': {
        source: { type: 'github', npm: '@wipcomputer/memory-crystal' },
        installed: { version: '2.0.0' },
      },
      // Phantom: no on-disk directory. Should be removed.
      'tavily': {
        source: { type: 'github', npm: '@wipcomputer/openclaw-tavily' },
        installed: { version: '0.1.0' },
      },
      // Mystery row: no source info at all but on-disk. Should be classified
      // untracked (Step 4 path in the planner).
      //
      // Note: on Parker's real machine the `run` entry has no on-disk
      // directory, so it hits Step 1 (phantom removal) instead. We exercise
      // the Step 4 path here via this fixture; Step 1 is covered by the
      // `tavily` fixture below.
      'run': {
        installed: { version: 'unknown' },
      },
      // Already migrated: must be skipped (idempotency).
      'already-untracked': {
        updateSource: { type: 'untracked' },
        provenance: { 'legacy-npm-name': 'already-untracked', untrackedSince: '2026-05-13T00:00:00.000Z' },
        installed: { version: '0.1.0' },
      },
      // Probe will fail (timeout). Should be left alone, listed in probeFailures.
      'flaky-network': {
        source: { type: 'github', npm: 'flaky-network' },
        installed: { version: '0.1.0' },
      },
      // Custom-path entry: declares `paths.ldm` pointing outside the default
      // ~/.ldm/extensions/<name> location. The planner must NOT classify
      // this as a phantom. Its source.npm is 404, so it should be migrated
      // to untracked while the custom path is preserved.
      'custom-path-untracked': {
        source: { type: 'github', npm: 'custom-path-untracked' },
        paths: { ldm: '/custom/location/path' },
        installed: { version: '1.0.0' },
      },
      // Legacy custom-path field (`ldmPath` flat). Same expectation.
      'legacy-custom-path': {
        source: { type: 'github', npm: 'legacy-custom-path' },
        ldmPath: '/legacy/custom/path',
        installed: { version: '0.2.0' },
      },
    },
  };
}

const NPM_404 = new Set([
  'session-export',
  'compaction-indicator',
  'lesa-bridge',
  'custom-path-untracked',
  'legacy-custom-path',
  // @wipcomputer/wip-branch-guard simulated as 200 (exists). But the dedupe
  // happens first, so `package` is gone before the probe runs.
  // The remaining `wip-branch-guard` will see exists=true and be left alone.
]);
const NPM_200 = new Set([
  '@wipcomputer/memory-crystal',
  '@wipcomputer/wip-branch-guard',
]);
const NPM_FAIL = new Set([
  'flaky-network',
]);

function fakeProbeNpm(name) {
  if (NPM_FAIL.has(name)) return Promise.resolve(null);
  if (NPM_200.has(name)) return Promise.resolve(true);
  if (NPM_404.has(name)) return Promise.resolve(false);
  // Fail loudly when the planner probes an npm name the test forgot to
  // enumerate. Future planner changes that call probeNpm with new names
  // must explicitly declare expected behavior here; silent 404 defaults
  // would swallow regressions.
  fail(`fakeProbeNpm called with un-enumerated name "${name}"`);
}

// On-disk extension simulator. `tavily` is a phantom (no directory at any
// location). All other names get a default directory unless they declare a
// custom path, in which case we honor the custom path. The planner must
// pass the entry to extensionExists for this to work.
const PHANTOM_NAMES = new Set(['tavily']);
const CUSTOM_PATH_EXISTS = new Set(['/custom/location/path', '/legacy/custom/path']);
function fakeExtensionExists(name, entry) {
  if (entry?.paths?.ldm) return CUSTOM_PATH_EXISTS.has(entry.paths.ldm);
  if (entry?.ldmPath) return CUSTOM_PATH_EXISTS.has(entry.ldmPath);
  return !PHANTOM_NAMES.has(name);
}

const FIXED_NOW = () => new Date('2026-05-13T18:00:00.000Z');

// ── Test 1: full migration on fixture ──────────────────────────────────────
{
  const input = buildFixtureRegistry();
  const inputSnapshot = JSON.stringify(input);

  const { newRegistry, summary } = await planLegacyNpmSourcesMigration({
    registry: input,
    probeNpm: fakeProbeNpm,
    extensionExists: fakeExtensionExists,
    now: FIXED_NOW,
  });

  // Input must not be mutated.
  assertEqual(JSON.stringify(input), inputSnapshot, 'input registry mutated');

  // Phantoms removed.
  assertEqual(summary.phantomsRemoved.length, 1, 'phantomsRemoved.length');
  assertEqual(summary.phantomsRemoved[0].name, 'tavily', 'phantom name');
  assertEqual(newRegistry.extensions.tavily, undefined, 'phantom still in registry');

  // Duplicates removed.
  assertEqual(summary.duplicatesRemoved.length, 2, 'duplicatesRemoved.length');
  const removedDupes = summary.duplicatesRemoved.map(d => d.removed).sort();
  assertDeepEqual(removedDupes, ['package', 'session-export'], 'dedupe targets');
  assertEqual(newRegistry.extensions['session-export'], undefined, 'session-export still in registry');
  assertEqual(newRegistry.extensions['package'], undefined, 'package still in registry');
  if (!newRegistry.extensions['cc-session-export']) fail('canonical cc-session-export removed');
  if (!newRegistry.extensions['wip-branch-guard']) fail('canonical wip-branch-guard removed');

  // Each removed duplicate must also produce a directoryMoves entry. The
  // wrapper in bin/ldm.js executes these moves after the registry write so
  // autoDetectExtensions cannot re-register the duplicate on the same install
  // run. Without this contract, the registry dedup reverts (see
  // ai/product/bugs/installer/2026-05-13--cc-mini--installer-dedup-reverts-between-installs.md).
  assertEqual(summary.directoryMoves.length, 2, 'directoryMoves.length');
  const moveNames = summary.directoryMoves.map(m => m.name).sort();
  assertDeepEqual(moveNames, ['package', 'session-export'], 'directoryMoves names');
  for (const m of summary.directoryMoves) {
    assertEqual(m.reason, 'deduplicated', `directoryMoves[${m.name}].reason`);
    if (!m.trashName.startsWith(`${m.name}-deduplicated-`)) {
      fail(`directoryMoves[${m.name}].trashName should start with "${m.name}-deduplicated-" but was "${m.trashName}"`);
    }
    if (!m.trashName.includes('2026-05-13T18-00-00-000Z')) {
      fail(`directoryMoves[${m.name}].trashName should embed the fixed-now timestamp but was "${m.trashName}"`);
    }
  }

  // The planner is pure: it must NOT pre-populate directoryMovesPerformed or
  // directoryMovesSkipped. Those are wrapper outputs from real filesystem I/O.
  assertEqual(summary.directoryMovesPerformed.length, 0, 'directoryMovesPerformed should be empty from pure planner');
  assertEqual(summary.directoryMovesSkipped.length, 0, 'directoryMovesSkipped should be empty from pure planner');

  // Migrated entries: cc-session-export, compaction-indicator, lesa-bridge,
  // run, plus the two custom-path entries (custom-path-untracked,
  // legacy-custom-path). `session-export` and `package` were deduped before
  // probe. `wip-branch-guard` exists on npm. `flaky-network` probe failed.
  const migratedNames = summary.migrated.map(m => m.name).sort();
  assertDeepEqual(migratedNames, [
    'cc-session-export', 'compaction-indicator', 'custom-path-untracked',
    'legacy-custom-path', 'lesa-bridge', 'run',
  ], 'migrated names');

  // Custom-path entries must NOT be removed as phantoms. The planner must
  // pass the entry to extensionExists so the custom path is honored.
  // Regression guard for the round-3 Codex blocker (data-loss path on
  // entries with entry.paths.ldm or entry.ldmPath).
  const cpu = newRegistry.extensions['custom-path-untracked'];
  if (!cpu) fail('custom-path-untracked was removed as phantom (extensionExists ignored entry.paths.ldm)');
  assertEqual(cpu.updateSource?.type, 'untracked', 'custom-path-untracked.updateSource.type');
  assertEqual(cpu.paths?.ldm, '/custom/location/path', 'custom-path-untracked.paths.ldm preserved');
  const lcp = newRegistry.extensions['legacy-custom-path'];
  if (!lcp) fail('legacy-custom-path was removed as phantom (extensionExists ignored entry.ldmPath)');
  assertEqual(lcp.updateSource?.type, 'untracked', 'legacy-custom-path.updateSource.type');
  assertEqual(lcp.ldmPath, '/legacy/custom/path', 'legacy-custom-path.ldmPath preserved');

  // Each migrated entry has updateSource.type=untracked.
  for (const name of migratedNames) {
    const e = newRegistry.extensions[name];
    if (!e) fail(`migrated entry ${name} missing from newRegistry`);
    assertEqual(e.updateSource?.type, 'untracked', `${name}.updateSource.type`);
    if ('source' in e) fail(`${name}.source should be deleted`);
    if (!e.provenance) fail(`${name}.provenance missing`);
    assertEqual(e.provenance.untrackedSince, '2026-05-13T18:00:00.000Z', `${name}.provenance.untrackedSince`);
  }

  // cc-session-export specifically: legacy-npm-name + repo preserved.
  const ccse = newRegistry.extensions['cc-session-export'];
  assertEqual(ccse.provenance['legacy-npm-name'], 'session-export', 'cc-session-export legacy-npm-name');
  assertEqual(ccse.provenance.repo, 'wipcomputer/cc-session-export', 'cc-session-export legacy repo');

  // `run` had no source info: legacy-npm-name absent, no repo, but still classified.
  const runEntry = newRegistry.extensions.run;
  if ('legacy-npm-name' in runEntry.provenance) fail('run.provenance should not have legacy-npm-name');
  if ('repo' in runEntry.provenance) fail('run.provenance should not have repo');

  // Real npm package left alone.
  const mc = newRegistry.extensions['memory-crystal'];
  if (mc.updateSource) fail('memory-crystal should not be migrated (real npm pkg)');
  assertEqual(mc.source?.npm, '@wipcomputer/memory-crystal', 'memory-crystal source preserved');

  // wip-branch-guard left alone (real npm pkg).
  const wbg = newRegistry.extensions['wip-branch-guard'];
  if (wbg.updateSource) fail('wip-branch-guard should not be migrated (real npm pkg)');

  // Already-untracked entry is unchanged.
  const au = newRegistry.extensions['already-untracked'];
  assertEqual(au.provenance.untrackedSince, '2026-05-13T00:00:00.000Z', 'already-untracked untracked since preserved');

  // Probe failures recorded, entry untouched.
  assertEqual(summary.probeFailures.length, 1, 'probeFailures.length');
  assertEqual(summary.probeFailures[0].name, 'flaky-network', 'probe failure name');
  const fn = newRegistry.extensions['flaky-network'];
  if (fn.updateSource) fail('flaky-network should not be migrated (probe failed)');
  assertEqual(fn.source?.npm, 'flaky-network', 'flaky-network source preserved');

  // summaryHasChanges flips true when anything happens.
  assertEqual(summaryHasChanges(summary), true, 'summaryHasChanges on populated summary');
}

// ── Test 2: idempotency on a fully-migrated registry ───────────────────────
{
  const registry = {
    extensions: {
      'a': {
        updateSource: { type: 'untracked' },
        provenance: { untrackedSince: '2026-05-13T00:00:00.000Z' },
        installed: { version: '1.0.0' },
      },
      'b': {
        updateSource: { type: 'untracked' },
        provenance: { 'legacy-npm-name': 'b', untrackedSince: '2026-05-13T00:00:00.000Z' },
        installed: { version: '0.1.0' },
      },
    },
  };
  const before = JSON.stringify(registry);
  const { newRegistry, summary } = await planLegacyNpmSourcesMigration({
    registry,
    probeNpm: () => fail('probeNpm should not be called on fully-migrated registry'),
    extensionExists: () => true,
    now: FIXED_NOW,
  });
  assertEqual(JSON.stringify(registry), before, 'input mutated on idempotent run');
  assertEqual(summary.migrated.length, 0, 'migrated.length on idempotent run');
  assertEqual(summary.phantomsRemoved.length, 0, 'phantomsRemoved.length on idempotent run');
  assertEqual(summary.duplicatesRemoved.length, 0, 'duplicatesRemoved.length on idempotent run');
  assertEqual(summary.directoryMoves.length, 0, 'directoryMoves.length on idempotent run');
  assertEqual(summaryHasChanges(summary), false, 'summaryHasChanges on empty summary');
  assertDeepEqual(
    Object.keys(newRegistry.extensions).sort(),
    ['a', 'b'],
    'extensions preserved on idempotent run',
  );
}

// ── Test 3: emptyLegacyNpmSourcesSummary returns the canonical shape ───────
{
  const e = emptyLegacyNpmSourcesSummary();
  assertDeepEqual(Object.keys(e).sort(), [
    'directoryMoves',
    'directoryMovesPerformed',
    'directoryMovesSkipped',
    'duplicatesRemoved',
    'migrated',
    'phantomsRemoved',
    'probeFailures',
    'probedCount',
    'timestamp',
  ], 'empty summary keys');
  // Wrapper-output fields start empty even though the planner doesn't
  // populate them ... the wrapper is responsible for appending.
  assertEqual(e.directoryMoves.length, 0, 'empty.directoryMoves');
  assertEqual(e.directoryMovesPerformed.length, 0, 'empty.directoryMovesPerformed');
  assertEqual(e.directoryMovesSkipped.length, 0, 'empty.directoryMovesSkipped');
}

// ── Test 4: executeDirectoryMoves against a real temp filesystem ──────────
// Regression guard for the bug fixed by this PR
// (ai/product/bugs/installer/2026-05-13--cc-mini--installer-dedup-reverts-between-installs.md).
// The planner emits directoryMoves entries; the executor must actually move
// the on-disk directories into trash so autoDetectExtensions cannot
// re-register them on the next install scan.
{
  const tmpHome = mkdtempSync(join(tmpdir(), 'ldm-dedup-trash-'));
  try {
    const extensionsRoot = join(tmpHome, 'extensions');
    const trashRoot = join(tmpHome, '_trash');
    mkdirSync(extensionsRoot, { recursive: true });

    // Stand up the two duplicate directories the planner would dedup.
    for (const name of ['session-export', 'package']) {
      const dir = join(extensionsRoot, name);
      mkdirSync(dir, { recursive: true });
      writeFileSync(join(dir, 'package.json'), JSON.stringify({ name, version: '1.0.0' }) + '\n');
    }
    // And a non-duplicate that must be left alone (proxy for cc-session-export).
    const ccsePath = join(extensionsRoot, 'cc-session-export');
    mkdirSync(ccsePath, { recursive: true });
    writeFileSync(join(ccsePath, 'package.json'), JSON.stringify({ name: 'cc-session-export', version: '1.0.0' }) + '\n');

    // Run the planner with the fixture to get a real directoryMoves plan.
    const registry = {
      extensions: {
        'cc-session-export': { source: { npm: 'session-export' }, installed: { version: '1.0.0' } },
        'session-export':    { source: { npm: 'session-export' }, installed: { version: '1.0.0' } },
        'wip-branch-guard':  { source: { npm: '@wipcomputer/wip-branch-guard' }, installed: { version: '1.0.0' } },
        'package':           { source: { npm: '@wipcomputer/wip-branch-guard' }, installed: { version: '1.0.0' } },
      },
    };
    const { summary } = await planLegacyNpmSourcesMigration({
      registry,
      probeNpm: (name) => Promise.resolve(name === '@wipcomputer/wip-branch-guard'),
      extensionExists: () => true,
      now: FIXED_NOW,
    });
    assertEqual(summary.directoryMoves.length, 2, 'dedup plan produces 2 directoryMoves');

    // Execute the moves against the temp filesystem.
    const { performed, skipped } = executeDirectoryMoves({
      directoryMoves: summary.directoryMoves,
      extensionsRoot,
      trashRoot,
    });
    assertEqual(performed.length, 2, 'executor performed 2 moves');
    assertEqual(skipped.length, 0, 'executor did not skip any moves');

    // Source directories are gone.
    if (existsSync(join(extensionsRoot, 'session-export'))) {
      fail('session-export directory should have been moved out of extensions/');
    }
    if (existsSync(join(extensionsRoot, 'package'))) {
      fail('package directory should have been moved out of extensions/');
    }

    // Trash directory now has the moved entries with the deduplicated suffix.
    const trashContents = readdirSync(trashRoot);
    if (!trashContents.some(name => name.startsWith('session-export-deduplicated-'))) {
      fail(`trash should contain session-export-deduplicated-* but had: ${trashContents.join(', ')}`);
    }
    if (!trashContents.some(name => name.startsWith('package-deduplicated-'))) {
      fail(`trash should contain package-deduplicated-* but had: ${trashContents.join(', ')}`);
    }

    // Non-duplicate must NOT have been touched.
    if (!existsSync(ccsePath)) fail('cc-session-export directory should be untouched');

    // autoDetectExtensions simulation: a fresh scan of extensionsRoot must
    // NOT see the moved duplicates. We replicate the production logic
    // (bin/ldm.js autoDetectExtensions): scan top-level dirs in
    // extensionsRoot, skip dirs named `_trash` or starting with `.` or
    // `ldm-install-`, and treat any remaining dir with a package.json as a
    // candidate for auto-registration.
    const candidatesAfterMove = readdirSync(extensionsRoot, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name)
      .filter(name => name !== '_trash' && !name.startsWith('.') && !name.startsWith('ldm-install-'))
      .filter(name => existsSync(join(extensionsRoot, name, 'package.json')))
      .sort();
    assertDeepEqual(
      candidatesAfterMove,
      ['cc-session-export'],
      'autoDetect should see only the non-duplicate after the moves; duplicates must be gone',
    );

    // Idempotency: running executeDirectoryMoves again must skip all
    // (source-missing) and not fail.
    const second = executeDirectoryMoves({
      directoryMoves: summary.directoryMoves,
      extensionsRoot,
      trashRoot,
    });
    assertEqual(second.performed.length, 0, 'second execute call performs nothing');
    assertEqual(second.skipped.length, 2, 'second execute call skips both moves');
    for (const s of second.skipped) {
      assertEqual(s.reason, 'source-missing', `second-call skip reason for ${s.name}`);
    }
  } finally {
    rmSync(tmpHome, { recursive: true, force: true });
  }
}

// ── Test 5: executeDirectoryMoves with no moves is a no-op ───────────────
{
  const tmpHome = mkdtempSync(join(tmpdir(), 'ldm-dedup-trash-empty-'));
  try {
    const result = executeDirectoryMoves({
      directoryMoves: [],
      extensionsRoot: join(tmpHome, 'extensions'),
      trashRoot: join(tmpHome, '_trash'),
    });
    assertEqual(result.performed.length, 0, 'empty plan -> no performed');
    assertEqual(result.skipped.length, 0, 'empty plan -> no skipped');
    if (existsSync(join(tmpHome, '_trash'))) {
      fail('executor should not pre-create trashRoot when there are no moves');
    }
  } finally {
    rmSync(tmpHome, { recursive: true, force: true });
  }
}

console.log('test-legacy-npm-sources-migration: all tests passed');
