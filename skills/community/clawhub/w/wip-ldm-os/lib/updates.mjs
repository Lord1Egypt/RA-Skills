/**
 * lib/updates.mjs
 * NPM update checker with cached manifest.
 * Reads the extension registry, checks npm for newer versions,
 * and writes results to ~/.ldm/state/available-updates.json.
 * Zero external dependencies.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { execSync } from 'node:child_process';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const LDM_EXTENSIONS = join(LDM_ROOT, 'extensions');
const STATE_DIR = join(LDM_ROOT, 'state');
const UPDATES_PATH = join(STATE_DIR, 'available-updates.json');
const REGISTRY_PATH = join(LDM_EXTENSIONS, 'registry.json');

// ── Helpers ──

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function writeJSON(path, data) {
  mkdirSync(join(path, '..'), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
}

// ── Semver comparison ──
// Copied from deploy.mjs to keep this module self-contained.

/**
 * Compare two semver strings. Returns 1 if a > b, -1 if a < b, 0 if equal.
 */
export function compareSemver(a, b) {
  if (!a || !b) return 0;
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    const na = pa[i] || 0;
    const nb = pb[i] || 0;
    if (na > nb) return 1;
    if (na < nb) return -1;
  }
  return 0;
}

// ── Catalog lookup ──

let _catalog = null;

function loadCatalog() {
  if (_catalog) return _catalog;
  try {
    // Try the installed location first, then the repo-relative location
    const paths = [
      join(LDM_EXTENSIONS, 'wip-ldm-os', 'catalog.json'),
      join(LDM_ROOT, 'catalog.json'),
    ];
    for (const p of paths) {
      const data = readJSON(p);
      if (data?.components) {
        _catalog = data;
        return data;
      }
    }
  } catch {}
  return { components: [] };
}

/**
 * Resolve the npm package name for a registry entry.
 * Checks the catalog for an npm field, or infers from the name.
 * @param {string} name - Extension name from registry
 * @param {Object} info - Registry entry info
 * @returns {string|null} npm package name or null
 */
export function resolveNpmName(name, info) {
  // Check catalog for npm field
  const catalog = loadCatalog();
  for (const c of catalog.components || []) {
    // Match by ID or by registryMatches
    if (c.id === name || (c.registryMatches || []).includes(name)) {
      if (c.npm) return c.npm;
    }
  }

  // Check if the registry entry itself has a packageName
  if (info?.packageName) return info.packageName;

  // Check deployed package.json for npm name
  if (info?.ldmPath) {
    const pkg = readJSON(join(info.ldmPath, 'package.json'));
    if (pkg?.name) return pkg.name;
  }

  return null;
}

// ── Update checking ──

/**
 * Check for available updates by querying npm registry.
 * Reads ~/.ldm/extensions/registry.json, checks each entry against npm,
 * and writes results to ~/.ldm/state/available-updates.json.
 * @returns {{ checkedAt: string, checked: number, updatesAvailable: number, updates: Array }}
 */
export function checkForUpdates() {
  const registry = readJSON(REGISTRY_PATH);
  if (!registry?.extensions) {
    return { checkedAt: new Date().toISOString(), checked: 0, updatesAvailable: 0, updates: [] };
  }

  const updates = [];
  let checked = 0;

  for (const [name, info] of Object.entries(registry.extensions)) {
    const npmName = resolveNpmName(name, info);
    if (!npmName) continue;

    const currentVersion = info.version;
    if (!currentVersion || currentVersion === 'unknown' || currentVersion === '?') continue;

    try {
      const result = execSync(`npm view ${npmName} version 2>/dev/null`, {
        encoding: 'utf8',
        timeout: 10000,
      }).trim();

      checked++;

      if (result && compareSemver(result, currentVersion) > 0) {
        updates.push({
          name,
          packageName: npmName,
          currentVersion,
          latestVersion: result,
          checkedAt: new Date().toISOString(),
        });
      }
    } catch {
      // Skip on failure (network error, package not found, timeout, etc.)
    }
  }

  const manifest = {
    checkedAt: new Date().toISOString(),
    checked,
    updatesAvailable: updates.length,
    updates,
  };

  // Write to cache
  try {
    writeJSON(UPDATES_PATH, manifest);
  } catch {}

  return manifest;
}

/**
 * Read the cached update manifest without re-checking npm.
 * @returns {Object|null} The cached manifest or null if not found
 */
export function readUpdateManifest() {
  return readJSON(UPDATES_PATH);
}
