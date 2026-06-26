#!/usr/bin/env node
/**
 * wip-repo-permissions-hook/cli.js
 * CLI for repo visibility permissions.
 *
 * Usage:
 *   wip-repo-permissions check <org/repo>      Check if repo can be public
 *   wip-repo-permissions audit <org>            Audit all public repos
 *   wip-repo-permissions can-publish <org/repo> Alias for check
 */

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkPrivateCounterpart, auditOrg } from './core.mjs';

if (process.argv.includes('--version') || process.argv.includes('-v')) {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}

const args = process.argv.slice(2);
const command = args[0];
const target = args[1];

function usage() {
  console.log('wip-repo-permissions ... repo visibility guard\n');
  console.log('Usage:');
  console.log('  wip-repo-permissions check <org/repo>       Check if repo can be made public');
  console.log('  wip-repo-permissions audit <org>             Audit all public repos in org');
  console.log('  wip-repo-permissions can-publish <org/repo>  Alias for check');
  console.log('\nExamples:');
  console.log('  wip-repo-permissions check wipcomputer/wip-bridge');
  console.log('  wip-repo-permissions audit wipcomputer');
  process.exit(1);
}

if (!command || !target) usage();

switch (command) {
  case 'check':
  case 'can-publish': {
    const parts = target.split('/');
    if (parts.length !== 2) {
      console.error('Error: target must be org/repo (e.g. wipcomputer/memory-crystal)');
      process.exit(1);
    }
    const [org, repo] = parts;
    const result = checkPrivateCounterpart(org, repo);

    if (result.allowed) {
      console.log(`  OK: ${result.reason}`);
      process.exit(0);
    } else {
      console.error(`  ${result.reason}`);
      process.exit(1);
    }
    break;
  }

  case 'audit': {
    const org = target;
    console.log(`\nAuditing public repos in ${org}...\n`);

    const { violations, ok } = auditOrg(org);

    if (ok.length > 0) {
      console.log(`  Compliant (${ok.length}):`);
      for (const r of ok) {
        console.log(`    OK  ${r.name}`);
      }
      console.log('');
    }

    if (violations.length > 0) {
      console.log(`  VIOLATIONS (${violations.length}):`);
      for (const v of violations) {
        console.log(`    !!  ${v.name} ... no -private counterpart`);
      }
      console.log('');
      console.error(`  ${violations.length} repo(s) are public without a -private counterpart.`);
      process.exit(1);
    } else {
      console.log('  All public repos have -private counterparts (or are exempt forks).');
      process.exit(0);
    }
  }

  default:
    usage();
}
