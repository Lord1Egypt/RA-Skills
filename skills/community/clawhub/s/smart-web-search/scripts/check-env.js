#!/usr/bin/env node
/**
 * check-env.js - Verify smart-web-search dependencies
 */
import process from 'process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..');

async function checkDeps() {
  const missing = [];
  const deps = ['cheerio', 'commander', 'iconv-lite', 'playwright'];

  console.log('Checking smart-web-search dependencies...\n');

  for (const mod of deps) {
    try {
      await import(mod);
      console.log(`✓ ${mod}`);
    } catch {
      console.log(`✗ ${mod}`);
      missing.push(mod);
    }
  }

  if (missing.length === 0) {
    console.log('\n✓ All dependencies are installed.');
    process.exit(0);
  }

  console.error(`\n✗ Missing dependencies: ${missing.join(', ')}\n`);
  console.error('Install them with:\n');
  console.error('  One-command setup (recommended):');
  console.error(`    cd "${SKILL_ROOT}" && bash scripts/setup.sh`);
  console.error('  Windows:');
  console.error(`    cd "${SKILL_ROOT}"; powershell -File scripts/setup.ps1\n`);
  console.error('  Manual install:');
  console.error(`    cd "${SKILL_ROOT}" && npm install && npx playwright install chromium\n`);
  process.exit(1);
}

checkDeps();
