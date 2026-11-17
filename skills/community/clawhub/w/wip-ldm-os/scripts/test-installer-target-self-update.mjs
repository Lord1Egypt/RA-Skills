#!/usr/bin/env node
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const cli = readFileSync(join(root, 'bin', 'ldm.js'), 'utf8');

const helperName = 'function maybeSelfUpdateLdmCliBeforeInstall()';
const helperIdx = cli.indexOf(helperName);
if (helperIdx === -1) {
  throw new Error('Missing shared LDM OS self-update preflight helper');
}

const helperBlock = cli.slice(helperIdx, cli.indexOf('// ── Dead backup trigger cleanup', helperIdx));
if (!helperBlock.includes('Dry run only: continuing with v${PKG_VERSION}.')) {
  throw new Error('Self-update helper must warn on dry run without updating');
}

if (!helperBlock.includes("execSync(`npm install -g @wipcomputer/wip-ldm-os@${latest}`")) {
  throw new Error('Self-update helper must update LDM OS before real installs');
}

if (!helperBlock.includes("spawnSync('ldm'")) {
  throw new Error('Self-update helper must re-run the original install command without shell joining args');
}

if (helperBlock.includes('process.argv.slice(2).join')) {
  throw new Error('Self-update helper must preserve argv boundaries when re-running install');
}

const cmdInstallIdx = cli.indexOf('async function cmdInstall()');
const lockIdx = cli.indexOf('acquireInstallLock()', cmdInstallIdx);
const initIdx = cli.indexOf('LDM OS not initialized. Running init first', cmdInstallIdx);
const targetIdx = cli.indexOf('// Find the target (skip flags)', cmdInstallIdx);
const preflightCallIdx = cli.indexOf('maybeSelfUpdateLdmCliBeforeInstall();', cmdInstallIdx);
if (cmdInstallIdx === -1 || targetIdx === -1 || preflightCallIdx === -1) {
  throw new Error('Could not find cmdInstall self-update placement');
}

if (preflightCallIdx > lockIdx || preflightCallIdx > initIdx) {
  throw new Error('Self-update preflight must run before lock acquisition and init work');
}

if (preflightCallIdx > targetIdx) {
  throw new Error('Self-update preflight must run before target resolution so app installs are covered');
}

const catalogIdx = cli.indexOf('async function cmdInstallCatalog()');
const oldCatalogBlock = cli.indexOf('Self-update: check if CLI itself is outdated', catalogIdx);
const autoDetectIdx = cli.indexOf('autoDetectExtensions();', catalogIdx);
if (oldCatalogBlock !== -1 && oldCatalogBlock < autoDetectIdx) {
  throw new Error('Catalog install should not own the only self-update block');
}

const tempRoot = mkdtempSync(join(tmpdir(), 'ldm-target-self-update-'));
try {
  const home = join(tempRoot, 'home');
  const fakeBin = join(tempRoot, 'bin');
  const target = join(tempRoot, 'target skill with spaces');

  mkdirSync(join(home, '.ldm'), { recursive: true });
  writeFileSync(join(home, '.ldm', 'version.json'), JSON.stringify({
    version: '0.0.0',
    installed: new Date().toISOString(),
    updated: new Date().toISOString(),
  }, null, 2) + '\n');

  mkdirSync(fakeBin, { recursive: true });
  const fakeNpm = join(fakeBin, 'npm');
  writeFileSync(fakeNpm, `#!/usr/bin/env bash
if [ "$1" = "view" ] && [ "$2" = "@wipcomputer/wip-ldm-os" ] && [ "$3" = "dist-tags.alpha" ]; then
  echo "99.0.0-alpha.1"
  exit 0
fi
echo "unexpected npm command: $*" >&2
exit 64
`);
  chmodSync(fakeNpm, 0o755);

  mkdirSync(target, { recursive: true });
  writeFileSync(join(target, 'SKILL.md'), `---
name: test-target-skill
description: Test target skill for installer self-update dry-run checks.
---

# Test Target Skill
`);

  const result = spawnSync(process.execPath, [
    join(root, 'bin', 'ldm.js'),
    'install',
    '--alpha',
    '--dry-run',
    target,
  ], {
    cwd: root,
    encoding: 'utf8',
    env: {
      ...process.env,
      HOME: home,
      PATH: `${fakeBin}:${process.env.PATH || ''}`,
    },
  });

  if (result.status !== 0) {
    throw new Error(`Runtime dry-run exited ${result.status}\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`);
  }

  if (!result.stdout.includes('LDM OS CLI v')) {
    throw new Error(`Runtime dry-run did not print the LDM OS skew warning\nstdout:\n${result.stdout}`);
  }

  if (!result.stdout.includes('-> v99.0.0-alpha.1 (alpha track) is available.')) {
    throw new Error(`Runtime dry-run did not include the selected alpha track version\nstdout:\n${result.stdout}`);
  }

  if (!result.stdout.includes('Dry run only: continuing with v')) {
    throw new Error(`Runtime dry-run did not say it would continue without updating\nstdout:\n${result.stdout}`);
  }

  if (!result.stdout.includes('Installing: target skill with spaces (dry run)')) {
    throw new Error(`Runtime dry-run did not continue to the targeted install preview\nstdout:\n${result.stdout}`);
  }
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}

console.log('targeted install self-update regression checks passed');
