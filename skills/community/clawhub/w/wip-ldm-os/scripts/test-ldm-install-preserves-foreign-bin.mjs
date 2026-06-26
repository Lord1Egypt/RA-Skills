#!/usr/bin/env node
// Regression test: `ldm install` must not remove or clobber foreign shims in
// ~/.ldm/bin. Memory Crystal owns crystal-capture.sh, but the LDM installer
// deploys its own scripts into the same directory on every install.
//
// This uses the real bin/ldm.js install path against a temp HOME. External
// commands that would hit the network or operator crontab are shimmed through
// PATH so the test is deterministic in CI and local sandboxes.

import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const cli = join(repo, 'bin', 'ldm.js');
const pkg = JSON.parse(readFileSync(join(repo, 'package.json'), 'utf8'));

function fail(message, output = '') {
  console.error(`FAIL: ${message}`);
  if (output) {
    console.error('\n--- ldm output ---');
    console.error(output.trim());
  }
  process.exit(1);
}

function assert(condition, message, output = '') {
  if (!condition) fail(message, output);
  console.log(`PASS: ${message}`);
}

const home = mkdtempSync(join(tmpdir(), 'ldm-install-bin-shim-'));

try {
  const ldmRoot = join(home, '.ldm');
  const binDir = join(ldmRoot, 'bin');
  const extDir = join(ldmRoot, 'extensions');
  const stateDir = join(ldmRoot, 'state');
  const fakeBin = join(home, 'fakebin');

  mkdirSync(binDir, { recursive: true });
  mkdirSync(extDir, { recursive: true });
  mkdirSync(stateDir, { recursive: true });
  mkdirSync(fakeBin, { recursive: true });

  writeFileSync(join(ldmRoot, 'version.json'), JSON.stringify({ version: pkg.version }, null, 2) + '\n');
  writeFileSync(join(extDir, 'registry.json'), JSON.stringify({ extensions: {} }, null, 2) + '\n');

  const shimPath = join(binDir, 'crystal-capture.sh');
  const shimContent = '#!/bin/sh\nprintf "memory-crystal sentinel\\n"\n';
  writeFileSync(shimPath, shimContent);
  chmodSync(shimPath, 0o755);

  // Avoid network-dependent version checks while still exercising real install.
  const npmShim = join(fakeBin, 'npm');
  writeFileSync(
    npmShim,
    `#!/bin/sh
if [ "$1" = "view" ]; then
  case "$3" in
    version|dist-tags.alpha|dist-tags.beta) printf '%s\\n' '${pkg.version}' ;;
    *) printf '%s\\n' '${pkg.version}' ;;
  esac
  exit 0
fi
if [ "$1" = "list" ]; then
  printf '{}\\n'
  exit 0
fi
exit 0
`,
  );
  chmodSync(npmShim, 0o755);

  // Avoid touching the operator's real crontab in any health path.
  const crontabShim = join(fakeBin, 'crontab');
  writeFileSync(crontabShim, '#!/bin/sh\nif [ "$1" = "-l" ]; then exit 1; fi\nexit 0\n');
  chmodSync(crontabShim, 0o755);

  let output = '';
  try {
    output = execFileSync('node', [cli, 'install'], {
      env: {
        ...process.env,
        HOME: home,
        PATH: `${fakeBin}:${process.env.PATH}`,
        LDM_SELF_UPDATED: '1',
      },
      encoding: 'utf8',
      timeout: 30000,
    });
  } catch (err) {
    output = `${err.stdout || ''}${err.stderr || ''}`;
    fail('real ldm install command should complete in temp HOME', output);
  }

  assert(existsSync(shimPath), 'foreign Memory Crystal shim still exists after ldm install', output);
  assert(readFileSync(shimPath, 'utf8') === shimContent, 'foreign Memory Crystal shim content was not clobbered', output);
  assert((readFileSync(shimPath, 'utf8').includes('memory-crystal sentinel')), 'foreign shim sentinel is intact', output);
  assert((readFileSync(shimPath).length > 0), 'foreign shim remains non-empty', output);
  assert((statSync(shimPath).mode & 0o111) !== 0, 'foreign shim remains executable', output);
  assert((existsSync(join(binDir, 'ldm-backup.sh'))), 'ldm-owned scripts still deploy into ~/.ldm/bin', output);

  const restored = readFileSync(shimPath);
  assert(restored.length === Buffer.byteLength(shimContent), 'foreign shim size is unchanged', output);

  console.log('\nldm install foreign-bin preservation regression passed.');
} finally {
  rmSync(home, { recursive: true, force: true });
}
