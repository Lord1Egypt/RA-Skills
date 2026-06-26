#!/usr/bin/env node

/**
 * wip-repos CLI ... repo manifest reconciler
 *
 * Commands:
 *   check   - Diff filesystem against manifest, flag drift
 *   sync    - Move local folders to match the manifest
 *   add     - Add a repo to the manifest
 *   move    - Move a repo to a different category in the manifest
 *   tree    - Generate directory tree from manifest
 */

import { check, planSync, executeSync, addRepo, moveRepo, generateReadmeTree, loadManifest, checkCompliance, fixCompliance, findUnmanifested } from './core.mjs';
import { runClaude } from './claude.mjs';
import { resolve, dirname, join } from 'node:path';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

if (process.argv.includes('--version') || process.argv.includes('-v')) {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}

const args = process.argv.slice(2);
const command = args[0];

function usage() {
  console.log(`wip-repos ... repo manifest reconciler

Usage:
  wip-repos check      [--manifest path] [--root path]
  wip-repos sync       [--manifest path] [--root path] [--dry-run]
  wip-repos compliance [--manifest path] [--root path] [--fix]
  wip-repos watchdog   [--manifest path] [--root path]
  wip-repos add <path> --remote <org/repo> [--category cat] [--description desc]
  wip-repos move <path> --to <new-path>
  wip-repos tree       [--manifest path]

Commands:
  check        Diff filesystem against manifest, flag drift
  sync         Move local folders to match the manifest
  compliance   Check all repos for .license-guard.json, LICENSE, CLA.md, .npmignore
  watchdog     Find repos on disk that are not in the manifest
  add          Add a repo to the manifest
  move         Move a repo to a different category in the manifest
  tree         Generate directory tree from manifest

Options:
  --manifest   Path to repos-manifest.json (default: ./repos-manifest.json)
  --root       Path to repos root directory (default: directory containing manifest)
  --dry-run    Show what would happen without making changes
  --fix        Create missing compliance files (with compliance command)
  --json       Output as JSON`);
}

function getFlag(flag) {
  const idx = args.indexOf(flag);
  if (idx === -1) return undefined;
  return args[idx + 1];
}

function hasFlag(flag) {
  return args.includes(flag);
}

const manifestPath = resolve(getFlag('--manifest') || 'repos-manifest.json');
const reposRoot = resolve(getFlag('--root') || dirname(manifestPath));
const dryRun = hasFlag('--dry-run');
const jsonOutput = hasFlag('--json');

try {
  switch (command) {
    case 'check': {
      const result = check(manifestPath, reposRoot);

      if (jsonOutput) {
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      console.log(`Manifest: ${result.total.manifest} repos`);
      console.log(`On disk:  ${result.total.disk} repos`);
      console.log(`Matched:  ${result.total.matched}`);
      console.log();

      if (result.onDiskOnly.length > 0) {
        console.log(`On disk but NOT in manifest (${result.onDiskOnly.length}):`);
        for (const p of result.onDiskOnly) {
          console.log(`  + ${p}`);
        }
        console.log();
      }

      if (result.inManifestOnly.length > 0) {
        console.log(`In manifest but NOT on disk (${result.inManifestOnly.length}):`);
        for (const p of result.inManifestOnly) {
          console.log(`  - ${p}`);
        }
        console.log();
      }

      if (result.onDiskOnly.length === 0 && result.inManifestOnly.length === 0) {
        console.log('No drift. Manifest and filesystem are in sync.');
      }

      // Exit code 1 if drift detected
      if (result.onDiskOnly.length > 0 || result.inManifestOnly.length > 0) {
        process.exit(1);
      }
      break;
    }

    case 'sync': {
      const moves = planSync(manifestPath, reposRoot);

      if (moves.length === 0) {
        console.log('Nothing to sync. All repos are in the right place.');
        break;
      }

      if (jsonOutput) {
        console.log(JSON.stringify(moves, null, 2));
        break;
      }

      console.log(`Found ${moves.length} repo(s) to move:\n`);
      for (const m of moves) {
        console.log(`  ${m.from} -> ${m.to}`);
        console.log(`  (remote: ${m.remote})`);
        console.log();
      }

      if (dryRun) {
        console.log('Dry run. No changes made.');
        break;
      }

      const results = executeSync(moves, reposRoot);
      for (const r of results) {
        if (r.status === 'moved') {
          console.log(`  Moved: ${r.from} -> ${r.to}`);
        } else if (r.status === 'skipped') {
          console.log(`  Skipped: ${r.from} (${r.reason})`);
        } else {
          console.log(`  Error: ${r.from} (${r.reason})`);
        }
      }
      break;
    }

    case 'add': {
      const repoPath = args[1];
      const remote = getFlag('--remote');
      if (!repoPath || !remote) {
        console.error('Usage: wip-repos add <path> --remote <org/repo>');
        process.exit(1);
      }
      const entry = addRepo(manifestPath, repoPath, remote, {
        category: getFlag('--category'),
        description: getFlag('--description'),
      });
      console.log(`Added: ${repoPath} -> ${remote}`);
      if (jsonOutput) console.log(JSON.stringify(entry, null, 2));
      break;
    }

    case 'move': {
      const fromPath = args[1];
      const toPath = getFlag('--to');
      if (!fromPath || !toPath) {
        console.error('Usage: wip-repos move <path> --to <new-path>');
        process.exit(1);
      }
      const entry = moveRepo(manifestPath, fromPath, toPath);
      console.log(`Moved in manifest: ${fromPath} -> ${toPath}`);
      if (jsonOutput) console.log(JSON.stringify(entry, null, 2));
      break;
    }

    case 'tree': {
      const tree = generateReadmeTree(manifestPath);
      console.log(tree);
      break;
    }

    case 'compliance': {
      const results = checkCompliance(manifestPath, reposRoot);
      const failing = results.filter(r => !r.clean);
      const passing = results.filter(r => r.clean);

      if (jsonOutput) {
        console.log(JSON.stringify(results, null, 2));
        break;
      }

      console.log(`Compliance check: ${results.length} repos scanned\n`);

      if (failing.length > 0) {
        console.log(`FAILING (${failing.length}):`);
        for (const r of failing) {
          console.log(`  ✗ ${r.repoPath}`);
          for (const issue of r.issues) {
            console.log(`    - ${issue}`);
          }
        }
        console.log();
      }

      if (passing.length > 0) {
        console.log(`PASSING (${passing.length}):`);
        for (const r of passing) {
          console.log(`  ✓ ${r.repoPath}`);
        }
        console.log();
      }

      if (failing.length > 0 && hasFlag('--fix')) {
        console.log('Fixing...\n');
        for (const r of failing) {
          const created = fixCompliance(r.fullPath);
          if (created.length > 0) {
            console.log(`  ${r.repoPath}: created ${created.join(', ')}`);
          }
        }
        console.log('\nFiles created. You still need to commit and push each repo.');
      } else if (failing.length > 0) {
        console.log('Run with --fix to create missing files.');
      }

      if (failing.length > 0) process.exit(1);
      break;
    }

    case 'watchdog': {
      const unmanifested = findUnmanifested(manifestPath, reposRoot);
      if (jsonOutput) {
        console.log(JSON.stringify(unmanifested, null, 2));
        break;
      }
      if (unmanifested.length === 0) {
        console.log('All repos on disk are in the manifest.');
      } else {
        console.log(`Repos on disk but NOT in manifest (${unmanifested.length}):`);
        for (const p of unmanifested) {
          console.log(`  ! ${p}`);
        }
        console.log('\nAdd them with: wip-repos add <path> --remote <org/repo>');
        process.exit(1);
      }
      break;
    }

    case 'claude': {
      runClaude(manifestPath, args.slice(1));
      break;
    }

    default:
      usage();
      if (command && command !== '--help' && command !== '-h') {
        process.exit(1);
      }
  }
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
