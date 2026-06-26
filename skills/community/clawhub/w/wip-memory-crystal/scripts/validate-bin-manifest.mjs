#!/usr/bin/env node
// scripts/validate-bin-manifest.mjs — prepublish gate for Memory Crystal's
// `binFiles` declaration in openclaw.plugin.json.
//
// Layer 1 of the bin-manifest release-blocker design (defined in
// wipcomputer/wip-ldm-os-private:
// ai/product/plans-prds/current/2026-04-28--cc-mini--ldm-bin-ownership-manifest-design.md).
// LDM CLI runs an equivalent validator on its own declarations. This
// script duplicates the rule shape so MC does not need a runtime
// dependency on the LDM CLI.
//
// Checks:
//   - Each declaration has a valid shape (name + source).
//   - `name` is a basename (no /, no \, no ..).
//   - `source` is a relative path with no .. and resolves to a real
//     file under the package root.
//   - No two declarations within this package share the same `name`.

import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const manifestPath = join(repo, 'openclaw.plugin.json');

if (!existsSync(manifestPath)) {
  console.log('No openclaw.plugin.json. Skipping validation.');
  process.exit(0);
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const decls = manifest?.binFiles;

if (!Array.isArray(decls)) {
  console.log('No binFiles declared. Skipping validation.');
  process.exit(0);
}

const errors = [];
const seen = new Set();

for (let i = 0; i < decls.length; i++) {
  const d = decls[i];
  const ctx = `binFiles[${i}]${d?.name ? ` ${d.name}` : ''}`;

  if (!d || typeof d !== 'object') {
    errors.push(`${ctx}: must be an object`);
    continue;
  }
  if (typeof d.name !== 'string' || !d.name) {
    errors.push(`${ctx}: "name" must be a non-empty string`);
  } else if (d.name !== basename(d.name) || d.name.includes('/') || d.name.includes('\\') || d.name.includes('..')) {
    errors.push(`${ctx}: "name" must be a basename, got "${d.name}"`);
  } else {
    if (seen.has(d.name)) errors.push(`${ctx}: duplicate name within package: ${d.name}`);
    seen.add(d.name);
  }
  if (typeof d.source !== 'string' || !d.source) {
    errors.push(`${ctx}: "source" must be a non-empty string`);
  } else if (d.source.includes('..')) {
    errors.push(`${ctx}: "source" must not contain "..", got "${d.source}"`);
  } else {
    const src = join(repo, d.source);
    if (!existsSync(src)) errors.push(`${ctx}: source not found at ${src}`);
  }
  if (d.executable !== undefined && typeof d.executable !== 'boolean') {
    errors.push(`${ctx}: "executable" must be a boolean if provided`);
  }
}

if (errors.length > 0) {
  console.error('FAIL: openclaw.plugin.json binFiles validation failed:');
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

console.log(`OK: openclaw.plugin.json binFiles validated (${decls.length} entr${decls.length === 1 ? 'y' : 'ies'}).`);
