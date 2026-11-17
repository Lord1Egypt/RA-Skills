// Registry migrations for ~/.ldm/extensions/registry.json.
//
// Phase 1 of the source-types refactor. Pure planner + npm-probe helper.
// Called by bin/ldm.js during `ldm install`. Idempotent: entries that already
// carry `updateSource` are skipped.
//
// `planLegacyNpmSourcesMigration` is pure (no filesystem I/O). The companion
// `executeDirectoryMoves` IS side-effecting; the planner emits a list of
// directory-move plans and the executor performs them. The split lets tests
// drive the planner with in-memory fixtures and exercise the executor against
// a real temp filesystem.
//
// See ai/product/bugs/installer/2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md
// and the parent design ai/product/bugs/installer/2026-05-13--cc-mini--installer-registry-source-types-architecture.md

import { existsSync, mkdirSync, renameSync } from 'node:fs';
import { join } from 'node:path';

const DEFAULT_NPM_REGISTRY = 'https://registry.npmjs.org';

// Phase 1 expedient. The known duplicate pairs surfaced on Parker's machine
// during the 2026-05-13 dogfood. General-case duplicate detection is the
// hygiene-audit ticket's Check 1
// (ai/product/bugs/installer/2026-05-13--cc-mini--installer-registry-hygiene-audit.md);
// do NOT extend this list as a long-term shape. Future entries belong in
// that audit, not here.
//
// Dedupe drops the duplicate's `installed` block entirely. Today both rows
// in each pair carry the same version, so no data is lost. If a duplicate
// ever carried a newer version than its canonical, the dedup would silently
// discard that information. Acceptable for the known pairs; not a general
// safe pattern.
const KNOWN_DUPLICATE_PAIRS = [
  { keep: 'cc-session-export', remove: 'session-export' },
  { keep: 'wip-branch-guard',  remove: 'package' },
];

export function emptyLegacyNpmSourcesSummary() {
  return {
    migrated: [],
    phantomsRemoved: [],
    duplicatesRemoved: [],
    // Directory moves to perform AFTER the registry write. The planner
    // emits these as a parallel list to duplicatesRemoved (1:1); the
    // wrapper in bin/ldm.js executes them. See
    // ai/product/bugs/installer/2026-05-13--cc-mini--installer-dedup-reverts-between-installs.md
    // for the bug fix: without moving the on-disk directory out of
    // ~/.ldm/extensions/, autoDetectExtensions re-registers the duplicate
    // on the same install run and the dedup never persists.
    directoryMoves: [],
    directoryMovesPerformed: [],
    directoryMovesSkipped: [],
    probedCount: 0,
    probeFailures: [],
    timestamp: new Date().toISOString(),
  };
}

export function summaryHasChanges(summary) {
  return summary.migrated.length > 0
    || summary.phantomsRemoved.length > 0
    || summary.duplicatesRemoved.length > 0;
}

// Pure planner. Returns { newRegistry, summary } without touching the
// filesystem. Tests pass an in-memory registry, a fake `probeNpm`, and a
// fake `extensionExists`. Real callers inject the file-backed versions.
//
// probeNpm contract:
//   returns true  if the package exists on npm
//   returns false if the package returns 404 (definitely doesn't exist)
//   returns null  if the probe failed (timeout / network) ... entry is left
//                  alone and retried on the next install
//
// extensionExists contract:
//   called as (name, entry) -> boolean
//   The entry is provided so the resolver can honor `entry.paths.ldm` and
//   the legacy `entry.ldmPath` field before falling back to the default
//   ~/.ldm/extensions/<name> path. A naive resolver that only checks the
//   default location would falsely classify custom-path entries as
//   phantoms and remove them. Real callers must check both.
export async function planLegacyNpmSourcesMigration({
  registry,
  probeNpm,
  extensionExists,
  now,
}) {
  const summary = emptyLegacyNpmSourcesSummary();
  if (now) summary.timestamp = now().toISOString();
  if (!registry?.extensions) return { newRegistry: registry, summary };

  // Shallow-clone the top level and each entry so the input is not mutated.
  const newRegistry = { ...registry, extensions: {} };
  for (const [name, entry] of Object.entries(registry.extensions)) {
    newRegistry.extensions[name] = { ...entry };
  }

  // Step 1: phantoms. Registry rows with no on-disk extension directory.
  // The acceptance criterion says these are removed entirely; they're
  // surfaced as an explicit summary delta, not silent.
  //
  // extensionExists is called with both name and entry so the resolver can
  // honor entry.paths.ldm / entry.ldmPath. A custom-path entry must not be
  // misclassified as phantom.
  for (const [name, entry] of Object.entries(newRegistry.extensions)) {
    if (entry.updateSource) continue;
    if (extensionExists(name, entry)) continue;
    summary.phantomsRemoved.push({
      name,
      reason: 'directory missing',
      legacyNpmName: entry.source?.npm || null,
    });
    delete newRegistry.extensions[name];
  }

  // Step 2: dedupe known pairs. Pure structural fix; the canonical row stays
  // untouched. Future drift is the hygiene-audit ticket's job, not this one.
  //
  // Each removed duplicate also emits a directoryMoves entry: the wrapper
  // moves ~/.ldm/extensions/<remove> to ~/.ldm/_trash/<remove>-deduplicated-<ts>
  // after the registry write so autoDetectExtensions cannot re-register
  // the duplicate on the same install run.
  const trashStamp = summary.timestamp.replace(/[:.]/g, '-');
  for (const { keep, remove } of KNOWN_DUPLICATE_PAIRS) {
    if (newRegistry.extensions[keep] && newRegistry.extensions[remove]) {
      summary.duplicatesRemoved.push({ keep, removed: remove });
      summary.directoryMoves.push({
        name: remove,
        reason: 'deduplicated',
        trashName: `${remove}-deduplicated-${trashStamp}`,
      });
      delete newRegistry.extensions[remove];
    }
  }

  // Step 3: probe entries that still carry a legacy `source.npm` value.
  // 404 -> migrate to untracked + provenance. 200 -> leave alone. Unknown ->
  // leave alone; the next install will retry.
  const probeTargets = [];
  for (const [name, entry] of Object.entries(newRegistry.extensions)) {
    if (entry.updateSource) continue;
    const npmName = entry.source?.npm;
    if (!npmName) continue;
    probeTargets.push({ name, npmName });
  }

  const probeResults = await Promise.all(
    probeTargets.map(async ({ name, npmName }) => {
      const exists = await probeNpm(npmName);
      summary.probedCount++;
      return { name, npmName, exists };
    })
  );

  for (const { name, npmName, exists } of probeResults) {
    if (exists === true) continue;
    if (exists === null) {
      summary.probeFailures.push({ name, npmName });
      continue;
    }
    const entry = newRegistry.extensions[name];
    const legacyRepo = entry.source?.repo || null;
    summary.migrated.push({ name, legacyNpmName: npmName, legacyRepo });
    entry.updateSource = { type: 'untracked' };
    entry.provenance = { ...(entry.provenance || {}) };
    entry.provenance['legacy-npm-name'] = npmName;
    if (legacyRepo) entry.provenance.repo = legacyRepo;
    entry.provenance.untrackedSince = summary.timestamp;
    delete entry.source;
  }

  // Step 4: entries with no source info at all (the mystery `run`-style row).
  // Per the ticket, migrate to untracked so they stay visible in `ldm status`.
  for (const [name, entry] of Object.entries(newRegistry.extensions)) {
    if (entry.updateSource) continue;
    if (entry.source?.npm || entry.source?.repo) continue;
    summary.migrated.push({
      name,
      legacyNpmName: null,
      legacyRepo: null,
      reason: 'no-source-info',
    });
    entry.updateSource = { type: 'untracked' };
    entry.provenance = { ...(entry.provenance || {}) };
    entry.provenance.untrackedSince = summary.timestamp;
    if ('source' in entry) delete entry.source;
  }

  return { newRegistry, summary };
}

// Execute the directory-move plans emitted by planLegacyNpmSourcesMigration.
// Side-effecting: moves directories from `extensionsRoot/<name>` to
// `trashRoot/<trashName>`. Creates `trashRoot` if needed. Skips moves whose
// source is missing or whose rename fails. Idempotent: a second call with the
// same plan returns all-skipped (source-missing) once the moves are done.
//
// Returns `{ performed: [...], skipped: [...] }` for the caller to append to
// the migration summary. Each performed entry gains a `destPath`; each skipped
// entry gains a `reason`.
//
// The contract is split from the planner so:
//   - the planner stays pure and trivially testable with in-memory fixtures,
//   - the executor can be exercised against a real temp filesystem in a test
//     fixture without spawning a full `ldm install` run,
//   - tests can inject `fs` primitives via the optional `fs` option for
//     paranoid scenarios.
export function executeDirectoryMoves({
  directoryMoves,
  extensionsRoot,
  trashRoot,
  fs,
}) {
  const _existsSync = fs?.existsSync || existsSync;
  const _mkdirSync = fs?.mkdirSync || mkdirSync;
  const _renameSync = fs?.renameSync || renameSync;

  const performed = [];
  const skipped = [];
  if (!directoryMoves || directoryMoves.length === 0) {
    return { performed, skipped };
  }

  _mkdirSync(trashRoot, { recursive: true });

  for (const move of directoryMoves) {
    const src = join(extensionsRoot, move.name);
    const dest = join(trashRoot, move.trashName);
    if (!_existsSync(src)) {
      skipped.push({ ...move, reason: 'source-missing' });
      continue;
    }
    try {
      _renameSync(src, dest);
      performed.push({ ...move, destPath: dest });
    } catch (err) {
      skipped.push({ ...move, reason: `rename-failed: ${err.message}` });
    }
  }

  return { performed, skipped };
}

// Real npm-registry probe. Returns true/false/null per the planner contract.
// Mirrors the fetch pattern used by npmViewVersionForStatus in bin/ldm.js.
export async function npmPackageExists(pkgName, opts = {}) {
  const registryUrl = (opts.registryUrl || DEFAULT_NPM_REGISTRY).replace(/\/+$/, '');
  const timeoutMs = Number.isFinite(opts.timeoutMs) ? opts.timeoutMs : 2000;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const url = `${registryUrl}/${encodeURIComponent(pkgName)}`;
    const response = await fetch(url, {
      signal: controller.signal,
      headers: { accept: 'application/vnd.npm.install-v1+json, application/json' },
    });
    if (response.status === 404) return false;
    if (response.ok) return true;
    return null;
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

// Doctor check: returns a list of registry entries that still carry a
// `source.npm` value pointing at a package that returns 404. These are
// candidates for migration on the next `ldm install`, but if the doctor
// runs first (Parker checks status / doctor before running install) we
// warn so it's not invisible.
//
// Returns: [{ name, npmName }] in lexical order.
export async function findLegacyNpm404Entries({
  registry,
  probeNpm,
}) {
  if (!registry?.extensions) return [];
  const targets = [];
  for (const [name, entry] of Object.entries(registry.extensions)) {
    if (entry.updateSource) continue;
    const npmName = entry.source?.npm;
    if (!npmName) continue;
    targets.push({ name, npmName });
  }
  const results = await Promise.all(
    targets.map(async ({ name, npmName }) => {
      const exists = await probeNpm(npmName);
      return { name, npmName, exists };
    })
  );
  return results
    .filter(r => r.exists === false)
    .map(({ name, npmName }) => ({ name, npmName }))
    .sort((a, b) => a.name.localeCompare(b.name));
}
