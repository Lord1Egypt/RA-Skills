#!/usr/bin/env node
// scripts/validate-bin-manifest.mjs — prepublish gate for wipLdmOs.binFiles.
//
// Layer 1 of the release-blocker design (see
// ai/product/plans-prds/current/2026-04-28--cc-mini--ldm-bin-ownership-manifest-design.md).
// Runs before every publish to assert each declared bin file is real and
// internally consistent. A broken declaration cannot reach npm because
// `wip-release` calls `prepublishOnly` which calls this.
//
// Checks:
//   - Each declaration has a valid shape (name + source).
//   - `name` is a basename (no /, no \, no ..).
//   - `source` resolves to a real file under the package root.
//   - No two declarations within this package share the same `name`.
//
// This does NOT check for cross-package conflicts. That is layer 2 in
// the design and lands as a follow-up workflow once a known-extensions
// registry exists.

import { readFileSync } from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateDeclarations } from '../lib/bin-manifest.mjs';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const pkg = JSON.parse(readFileSync(join(repo, 'package.json'), 'utf8'));
const decls = pkg?.wipLdmOs?.binFiles;

if (!Array.isArray(decls)) {
  console.log('No wipLdmOs.binFiles declared. Skipping validation.');
  process.exit(0);
}

const result = validateDeclarations('wip-ldm-os', repo, decls);
if (!result.valid) {
  console.error('FAIL: wipLdmOs.binFiles validation failed:');
  for (const e of result.errors) console.error(`  - ${e}`);
  process.exit(1);
}

console.log(`OK: wipLdmOs.binFiles validated (${decls.length} entr${decls.length === 1 ? 'y' : 'ies'}).`);
