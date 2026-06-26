// lib/bin-manifest.mjs — bin ownership manifest aggregator + heal helpers
//
// Implements the design at
// ai/product/plans-prds/current/2026-04-28--cc-mini--ldm-bin-ownership-manifest-design.md
//
// Two declarers contribute entries:
//   - LDM CLI: package.json `wipLdmOs.binFiles`
//   - Extensions: ~/.ldm/extensions/<name>/openclaw.plugin.json `binFiles`
//
// Aggregation produces { entries, conflicts }. Conflicts are hard
// failures: callers MUST check `conflicts.length === 0` before any
// write. heal() never runs if conflicts exist.

import { existsSync, readFileSync, statSync, mkdirSync, copyFileSync, chmodSync } from 'node:fs';
import { join, dirname, basename } from 'node:path';

/**
 * @typedef {Object} BinDeclaration
 * @property {string} name        - basename written to <binDir>/<name>
 * @property {string} source      - relative to declarer's installed root
 * @property {boolean} [executable] - default true; chmod 0755 after copy
 * @property {string} [purpose]   - free-form, surfaces in verbose doctor
 */

/**
 * @typedef {Object} BinEntry
 * @property {string} name
 * @property {string} destPath    - resolved absolute path under binDir
 * @property {string} sourcePath  - resolved absolute path
 * @property {boolean} executable
 * @property {string} declarer    - 'wip-ldm-os' or extension name
 * @property {string} [purpose]
 */

/**
 * @typedef {Object} Conflict
 * @property {string} name
 * @property {{declarer: string, sourcePath: string}[]} declarers
 */

/**
 * Validate a single declaration shape. Returns array of error strings (empty = ok).
 * @param {BinDeclaration} decl
 * @returns {string[]}
 */
export function validateDeclaration(decl) {
  const errors = [];
  if (!decl || typeof decl !== 'object') {
    errors.push('declaration must be an object');
    return errors;
  }
  if (typeof decl.name !== 'string' || !decl.name) {
    errors.push('"name" must be a non-empty string');
  } else if (decl.name !== basename(decl.name) || decl.name.includes('/') || decl.name.includes('\\')) {
    errors.push(`"name" must be a basename, got "${decl.name}"`);
  } else if (decl.name.includes('..')) {
    errors.push(`"name" must not contain "..", got "${decl.name}"`);
  }
  if (typeof decl.source !== 'string' || !decl.source) {
    errors.push('"source" must be a non-empty string');
  } else if (decl.source.includes('..')) {
    errors.push(`"source" must not contain "..", got "${decl.source}"`);
  }
  if (decl.executable !== undefined && typeof decl.executable !== 'boolean') {
    errors.push('"executable" must be a boolean if provided');
  }
  return errors;
}

/**
 * Validate all declarations from one declarer (e.g. the LDM CLI's own
 * `wipLdmOs.binFiles`, or one extension's `binFiles`). Used by both
 * runtime aggregation and prepublish CI gate.
 *
 * Checks: shape per entry, no internal duplicate `name`, `source` exists
 * on disk under `packageRoot`.
 *
 * @param {string} declarer
 * @param {string} packageRoot - the absolute path to resolve `source` against
 * @param {BinDeclaration[]} decls
 * @returns {{valid: boolean, errors: string[]}}
 */
export function validateDeclarations(declarer, packageRoot, decls) {
  const errors = [];
  if (!Array.isArray(decls)) {
    return { valid: false, errors: [`${declarer}: binFiles must be an array`] };
  }
  const seen = new Set();
  for (let i = 0; i < decls.length; i++) {
    const d = decls[i];
    const ctx = `${declarer}[${i}]${d?.name ? ` ${d.name}` : ''}`;
    for (const e of validateDeclaration(d)) errors.push(`${ctx}: ${e}`);
    if (d && typeof d.name === 'string') {
      if (seen.has(d.name)) errors.push(`${declarer}: duplicate name within declarer: ${d.name}`);
      seen.add(d.name);
    }
    if (d && typeof d.source === 'string') {
      const src = join(packageRoot, d.source);
      if (!existsSync(src)) errors.push(`${ctx}: source not found at ${src}`);
    }
  }
  return { valid: errors.length === 0, errors };
}

/**
 * Read LDM CLI's own bin declarations from its package.json.
 * @param {string} ldmCliRoot
 * @returns {BinDeclaration[]}
 */
function readLdmCliDeclarations(ldmCliRoot) {
  const pkgPath = join(ldmCliRoot, 'package.json');
  if (!existsSync(pkgPath)) return [];
  try {
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
    return Array.isArray(pkg?.wipLdmOs?.binFiles) ? pkg.wipLdmOs.binFiles : [];
  } catch {
    return [];
  }
}

/**
 * Read one extension's bin declarations from its openclaw.plugin.json.
 * @param {string} extDir - ~/.ldm/extensions/<name>
 * @returns {BinDeclaration[]}
 */
function readExtensionDeclarations(extDir) {
  const manifestPath = join(extDir, 'openclaw.plugin.json');
  if (!existsSync(manifestPath)) return [];
  try {
    const m = JSON.parse(readFileSync(manifestPath, 'utf-8'));
    return Array.isArray(m?.binFiles) ? m.binFiles : [];
  } catch {
    return [];
  }
}

/**
 * Aggregate all bin entries across LDM CLI + registered extensions.
 * Returns conflicts for any name claimed by 2+ declarers.
 *
 * IMPORTANT: callers MUST check `conflicts.length === 0` before doing any
 * writes. Conflict means we cannot safely decide who owns the file.
 *
 * @param {Object} opts
 * @param {string} opts.ldmCliRoot       - absolute path to LDM CLI package root
 * @param {string} opts.extensionsRoot   - absolute path, typically ~/.ldm/extensions
 * @param {string} opts.binDir           - absolute path, typically ~/.ldm/bin
 * @param {Object} [opts.registry]       - optional ~/.ldm/extensions/registry.json contents
 * @returns {{entries: BinEntry[], conflicts: Conflict[]}}
 */
export function aggregateBinManifest({ ldmCliRoot, extensionsRoot, binDir, registry } = {}) {
  /** @type {BinEntry[]} */
  const entries = [];
  /** @type {Map<string, {declarer: string, sourcePath: string}[]>} */
  const claims = new Map();

  function record(declarer, declarerRoot, decls) {
    for (const d of decls) {
      if (!d || typeof d.name !== 'string' || typeof d.source !== 'string') continue;
      const sourcePath = join(declarerRoot, d.source);
      const list = claims.get(d.name) || [];
      list.push({ declarer, sourcePath });
      claims.set(d.name, list);
      entries.push({
        name: d.name,
        destPath: join(binDir, d.name),
        sourcePath,
        executable: d.executable !== false,
        declarer,
        purpose: d.purpose,
      });
    }
  }

  // 1. LDM CLI
  record('wip-ldm-os', ldmCliRoot, readLdmCliDeclarations(ldmCliRoot));

  // 2. Registered extensions
  const extNames = registry?.extensions ? Object.keys(registry.extensions) : [];
  for (const name of extNames) {
    const extDir = join(extensionsRoot, name);
    record(name, extDir, readExtensionDeclarations(extDir));
  }

  /** @type {Conflict[]} */
  const conflicts = [];
  for (const [name, declarers] of claims.entries()) {
    if (declarers.length > 1) conflicts.push({ name, declarers });
  }

  return { entries, conflicts };
}

/**
 * Verify and (optionally) heal each entry. heal=false is read-only and
 * just classifies. heal=true restores missing/unexecutable files from
 * `sourcePath`. Returns a per-entry result so callers can build their
 * own output.
 *
 * NEVER call this if aggregateBinManifest reported conflicts. The caller
 * must abort instead.
 *
 * @param {BinEntry[]} entries
 * @param {Object} [opts]
 * @param {boolean} [opts.heal] - default false
 * @returns {{
 *   ok: BinEntry[],
 *   missing: BinEntry[],
 *   notExecutable: BinEntry[],
 *   sourceMissing: BinEntry[],
 *   healed: BinEntry[],
 *   failed: {entry: BinEntry, reason: string}[]
 * }}
 */
export function healBinManifest(entries, opts = {}) {
  const heal = opts.heal === true;
  const ok = [];
  const missing = [];
  const notExecutable = [];
  const sourceMissing = [];
  const healed = [];
  const failed = [];

  for (const e of entries) {
    const destExists = existsSync(e.destPath);
    const destExecutable = destExists && (statSync(e.destPath).mode & 0o111) !== 0;
    const expectedExec = e.executable !== false;
    const destOk = destExists && (!expectedExec || destExecutable);

    if (destOk) {
      ok.push(e);
      continue;
    }

    if (!destExists) missing.push(e);
    else if (expectedExec && !destExecutable) notExecutable.push(e);

    if (!heal) continue;

    if (!existsSync(e.sourcePath)) {
      sourceMissing.push(e);
      failed.push({ entry: e, reason: `source missing at ${e.sourcePath}` });
      continue;
    }

    try {
      mkdirSync(dirname(e.destPath), { recursive: true });
      copyFileSync(e.sourcePath, e.destPath);
      if (expectedExec) chmodSync(e.destPath, 0o755);
      healed.push(e);
    } catch (err) {
      failed.push({ entry: e, reason: err.message });
    }
  }

  return { ok, missing, notExecutable, sourceMissing, healed, failed };
}
