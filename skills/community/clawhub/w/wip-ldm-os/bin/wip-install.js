#!/usr/bin/env node
// wip-install: thin bootstrap + delegate to ldm install.
// If ldm is on PATH, delegates immediately.
// If not, installs LDM OS from npm, then delegates.
// Replaces the standalone 700-line install.js from wip-ai-devops-toolbox.

// Handle --version directly to prevent recursive spawn loop (#70)
// detectCLIBinaries() calls wip-install --version which would trigger
// ldm install which triggers npm checks which spawn more processes.
const args = process.argv.slice(2);
if (args.includes('--version') || args.includes('-v')) {
  const { readFileSync } = await import('node:fs');
  const { join, dirname } = await import('node:path');
  const { fileURLToPath } = await import('node:url');
  const __dirname = dirname(fileURLToPath(import.meta.url));
  try {
    const pkg = JSON.parse(readFileSync(join(__dirname, '..', 'package.json'), 'utf8'));
    console.log(pkg.version);
  } catch { console.log('unknown'); }
  process.exit(0);
}

import { run } from '../lib/bootstrap.mjs';
run(args);
