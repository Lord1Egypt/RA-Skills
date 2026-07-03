#!/usr/bin/env node
/** One-command install from repo root or extracted Hermes pack. */
import { execSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const packRoot = existsSync(join(here, 'scripts', 'urufu-steward.mjs'))
  ? here
  : existsSync(join(here, 'dist', 'urufu-steward-hermes', 'scripts'))
    ? join(here, 'dist', 'urufu-steward-hermes')
    : null;

if (!packRoot) {
  console.error('Run npm run pack-hermes first, or extract the tarball.');
  process.exit(1);
}

console.log(`Installing from ${packRoot}...`);
execSync(`node "${join(packRoot, 'install.mjs')}"`, { stdio: 'inherit' });
