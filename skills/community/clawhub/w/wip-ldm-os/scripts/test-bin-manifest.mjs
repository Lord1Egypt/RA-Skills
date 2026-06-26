#!/usr/bin/env node
// Regression test: bin ownership manifest aggregator + heal + integration.
//
// Unit: aggregateBinManifest, healBinManifest, validateDeclarations.
// Integration: real `node bin/ldm.js install` against a temp HOME with a
// fake extension declaring binFiles. Verifies install-time self-heal
// restores a missing file from the declared source. Verifies that on
// conflict the install aborts BEFORE any writes (per the design's
// strict pre-write conflict rule).

import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync, readdirSync, copyFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import {
  aggregateBinManifest,
  healBinManifest,
  validateDeclarations,
  validateDeclaration,
} from '../lib/bin-manifest.mjs';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const cli = join(repo, 'bin', 'ldm.js');
const pkg = JSON.parse(readFileSync(join(repo, 'package.json'), 'utf8'));

let failed = 0;
function assert(cond, label, output = '') {
  if (cond) {
    console.log(`  [PASS] ${label}`);
  } else {
    console.log(`  [FAIL] ${label}`);
    if (output) console.log(`         --- ldm output (last lines) ---\n         ${output.trim().split('\n').slice(-30).join('\n         ')}`);
    failed++;
  }
}

// ── Unit: validateDeclaration ──
console.log('Unit: validateDeclaration shape checks');
{
  assert(validateDeclaration({ name: 'a.sh', source: 'x/a.sh' }).length === 0, 'valid declaration passes');
  assert(validateDeclaration(null).length > 0, 'null declaration fails');
  assert(validateDeclaration({ source: 'x' }).length > 0, 'missing name fails');
  assert(validateDeclaration({ name: 'a.sh' }).length > 0, 'missing source fails');
  assert(validateDeclaration({ name: '../../etc/passwd', source: 'x' }).length > 0, 'name with .. fails');
  assert(validateDeclaration({ name: 'sub/a.sh', source: 'x' }).length > 0, 'name with / fails');
  assert(validateDeclaration({ name: 'a.sh', source: '../escape/a.sh' }).length > 0, 'source with .. fails');
  assert(validateDeclaration({ name: 'a.sh', source: 'x', executable: 'yes' }).length > 0, 'non-boolean executable fails');
}

// ── Unit: validateDeclarations (multi-decl) ──
console.log('Unit: validateDeclarations against on-disk source');
{
  const tmp = mkdtempSync(join(tmpdir(), 'mc-validate-'));
  mkdirSync(join(tmp, 'src'), { recursive: true });
  writeFileSync(join(tmp, 'src', 'good.sh'), '#!/bin/sh\n');
  const res1 = validateDeclarations('test', tmp, [{ name: 'good.sh', source: 'src/good.sh' }]);
  assert(res1.valid, 'declaration with existing source passes');

  const res2 = validateDeclarations('test', tmp, [{ name: 'missing.sh', source: 'src/missing.sh' }]);
  assert(!res2.valid && res2.errors.some(e => /source not found/.test(e)), 'declaration with missing source fails');

  const res3 = validateDeclarations('test', tmp, [
    { name: 'good.sh', source: 'src/good.sh' },
    { name: 'good.sh', source: 'src/good.sh' },
  ]);
  assert(!res3.valid && res3.errors.some(e => /duplicate name/.test(e)), 'internal duplicate names fail');
  rmSync(tmp, { recursive: true, force: true });
}

// ── Unit: aggregateBinManifest produces entries from both declarers ──
console.log('Unit: aggregateBinManifest combines LDM CLI + extensions');
{
  const tmp = mkdtempSync(join(tmpdir(), 'mc-agg-'));
  const ldmCliRoot = join(tmp, 'cli');
  const extensionsRoot = join(tmp, 'extensions');
  const binDir = join(tmp, 'bin');
  mkdirSync(ldmCliRoot, { recursive: true });
  mkdirSync(join(extensionsRoot, 'mc'), { recursive: true });
  mkdirSync(binDir, { recursive: true });
  writeFileSync(join(ldmCliRoot, 'package.json'), JSON.stringify({
    wipLdmOs: { binFiles: [{ name: 'cli-tool.sh', source: 'cli-tool.sh' }] },
  }));
  writeFileSync(join(ldmCliRoot, 'cli-tool.sh'), '#!/bin/sh\n');
  writeFileSync(join(extensionsRoot, 'mc', 'openclaw.plugin.json'), JSON.stringify({
    binFiles: [{ name: 'ext-shim.sh', source: 'dist/ext-shim.sh' }],
  }));
  mkdirSync(join(extensionsRoot, 'mc', 'dist'), { recursive: true });
  writeFileSync(join(extensionsRoot, 'mc', 'dist', 'ext-shim.sh'), '#!/bin/sh\n');

  const m = aggregateBinManifest({
    ldmCliRoot, extensionsRoot, binDir,
    registry: { extensions: { mc: {} } },
  });
  assert(m.entries.length === 2, 'two entries aggregated');
  assert(m.entries.some(e => e.declarer === 'wip-ldm-os' && e.name === 'cli-tool.sh'), 'LDM CLI entry present');
  assert(m.entries.some(e => e.declarer === 'mc' && e.name === 'ext-shim.sh'), 'extension entry present');
  assert(m.conflicts.length === 0, 'no conflicts when names are distinct');
  rmSync(tmp, { recursive: true, force: true });
}

// ── Unit: aggregateBinManifest detects conflicts ──
console.log('Unit: aggregateBinManifest detects same-name conflicts');
{
  const tmp = mkdtempSync(join(tmpdir(), 'mc-conflict-'));
  const ldmCliRoot = join(tmp, 'cli');
  const extensionsRoot = join(tmp, 'extensions');
  mkdirSync(ldmCliRoot, { recursive: true });
  mkdirSync(join(extensionsRoot, 'mc'), { recursive: true });
  writeFileSync(join(ldmCliRoot, 'package.json'), JSON.stringify({
    wipLdmOs: { binFiles: [{ name: 'shared.sh', source: 'a.sh' }] },
  }));
  writeFileSync(join(ldmCliRoot, 'a.sh'), '');
  writeFileSync(join(extensionsRoot, 'mc', 'openclaw.plugin.json'), JSON.stringify({
    binFiles: [{ name: 'shared.sh', source: 'b.sh' }],
  }));
  writeFileSync(join(extensionsRoot, 'mc', 'b.sh'), '');

  const m = aggregateBinManifest({
    ldmCliRoot, extensionsRoot, binDir: join(tmp, 'bin'),
    registry: { extensions: { mc: {} } },
  });
  assert(m.conflicts.length === 1, 'one conflict detected');
  assert(m.conflicts[0].name === 'shared.sh', 'conflict names the disputed file');
  assert(m.conflicts[0].declarers.length === 2, 'both declarers listed');
  rmSync(tmp, { recursive: true, force: true });
}

// ── Unit: healBinManifest read-only and heal modes ──
console.log('Unit: healBinManifest classifies and restores');
{
  const tmp = mkdtempSync(join(tmpdir(), 'mc-heal-'));
  const binDir = join(tmp, 'bin');
  mkdirSync(binDir, { recursive: true });
  const sourceDir = join(tmp, 'src');
  mkdirSync(sourceDir, { recursive: true });
  writeFileSync(join(sourceDir, 'a.sh'), '#!/bin/sh\necho a\n');

  const entryMissing = {
    name: 'a.sh', destPath: join(binDir, 'a.sh'), sourcePath: join(sourceDir, 'a.sh'),
    executable: true, declarer: 'test',
  };

  const ro = healBinManifest([entryMissing]);
  assert(ro.missing.length === 1, 'read-only reports missing');
  assert(ro.healed.length === 0, 'read-only does not restore');
  assert(!existsSync(entryMissing.destPath), 'no write happened in read-only mode');

  const wr = healBinManifest([entryMissing], { heal: true });
  assert(wr.healed.length === 1, 'heal restores missing file');
  assert(existsSync(entryMissing.destPath), 'file present after heal');
  assert((statSync(entryMissing.destPath).mode & 0o111) !== 0, 'restored file is executable');

  // Now make it non-executable and heal again.
  chmodSync(entryMissing.destPath, 0o644);
  const wr2 = healBinManifest([entryMissing], { heal: true });
  assert(wr2.healed.length === 1, 'heal restores executable bit');
  assert((statSync(entryMissing.destPath).mode & 0o111) !== 0, 'file is executable after second heal');

  // Source missing case.
  rmSync(join(sourceDir, 'a.sh'));
  rmSync(entryMissing.destPath);
  const noSrc = healBinManifest([entryMissing], { heal: true });
  assert(noSrc.sourceMissing.length === 1, 'reports source missing');
  assert(noSrc.failed.length === 1, 'failed records the entry');
  rmSync(tmp, { recursive: true, force: true });
}

// ── Integration: real `ldm install` heals a declared extension shim ──
console.log('Integration: ldm install restores missing extension-declared shim');
function makeIntegrationHome({ extDecls = null, extraExtension = null } = {}) {
  const home = mkdtempSync(join(tmpdir(), 'ldm-bin-manifest-'));
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

  // Optional fake plugin with binFiles.
  const registryEntries = {};
  if (extDecls) {
    const pluginDir = join(extDir, 'fake-plugin');
    const pluginDist = join(pluginDir, 'dist');
    mkdirSync(pluginDist, { recursive: true });
    writeFileSync(join(pluginDir, 'openclaw.plugin.json'), JSON.stringify({
      id: 'fake-plugin', name: 'Fake Plugin', binFiles: extDecls,
    }));
    writeFileSync(join(pluginDist, 'fake-shim.sh'), '#!/bin/sh\necho fake\n');
    chmodSync(join(pluginDist, 'fake-shim.sh'), 0o755);
    registryEntries['fake-plugin'] = {};
  }
  if (extraExtension) {
    const pluginDir = join(extDir, extraExtension.name);
    mkdirSync(pluginDir, { recursive: true });
    writeFileSync(join(pluginDir, 'openclaw.plugin.json'), JSON.stringify({
      id: extraExtension.name, name: extraExtension.name, binFiles: extraExtension.binFiles,
    }));
    if (extraExtension.sourceFiles) {
      for (const [rel, content] of Object.entries(extraExtension.sourceFiles)) {
        const fp = join(pluginDir, rel);
        mkdirSync(dirname(fp), { recursive: true });
        writeFileSync(fp, content);
        chmodSync(fp, 0o755);
      }
    }
    registryEntries[extraExtension.name] = {};
  }
  writeFileSync(join(extDir, 'registry.json'), JSON.stringify({
    _format: 'v2', extensions: registryEntries,
  }, null, 2) + '\n');

  // npm + crontab shims.
  writeFileSync(join(fakeBin, 'npm'), '#!/bin/sh\nexit 0\n');
  chmodSync(join(fakeBin, 'npm'), 0o755);
  writeFileSync(join(fakeBin, 'crontab'), '#!/bin/sh\nif [ "$1" = "-l" ]; then exit 1; fi\nexit 0\n');
  chmodSync(join(fakeBin, 'crontab'), 0o755);

  return { home, binDir, extDir, fakeBin };
}

function runInstall({ home, fakeBin }) {
  try {
    return execFileSync('node', [cli, 'install'], {
      env: { ...process.env, HOME: home, PATH: `${fakeBin}:${process.env.PATH}`, LDM_SELF_UPDATED: '1' },
      encoding: 'utf-8',
      timeout: 30000,
    });
  } catch (err) {
    return { error: true, output: (err.stdout || '') + (err.stderr || ''), code: err.status };
  }
}

// Test A: extension declares fake-shim.sh; install heal-restores it because dest is absent.
{
  const w = makeIntegrationHome({
    extDecls: [{ name: 'fake-shim.sh', source: 'dist/fake-shim.sh' }],
  });
  const out = runInstall(w);
  const text = typeof out === 'string' ? out : out.output;
  const restored = join(w.binDir, 'fake-shim.sh');
  assert(/Restored fake-shim\.sh/.test(text), 'install logs restore', text);
  assert(existsSync(restored), 'fake-shim.sh present in ~/.ldm/bin/ after install', text);
  assert((statSync(restored).mode & 0o111) !== 0, 'restored shim is executable', text);
  rmSync(w.home, { recursive: true, force: true });
}

// Test B: conflict between LDM CLI and a fake plugin BOTH claiming the same name.
//         Install must abort BEFORE writing fake-shim.sh.
console.log('Integration: ldm install aborts on conflict before writing');
{
  // The LDM CLI's wipLdmOs.binFiles already declares ldm-backup.sh.
  // We add a fake plugin claiming the same name.
  const w = makeIntegrationHome({
    extDecls: [{ name: 'ldm-backup.sh', source: 'dist/fake-shim.sh' }],
  });
  const out = runInstall(w);
  const text = typeof out === 'string' ? out : out.output;
  assert(out.error === true, 'install exits non-zero on conflict', text);
  assert(/bin manifest conflict/.test(text), 'output names the conflict', text);
  assert(/aborting before seedLocalCatalog\/deployBridge\/deployScripts run/.test(text), 'output declares pre-write abort', text);
  // Pre-write invariant: install bailed before any of seedLocalCatalog,
  // deployBridge, or deployScripts ran. Verify each.
  const backupShim = join(w.binDir, 'ldm-backup.sh');
  assert(!existsSync(backupShim), 'no partial state: ldm-backup.sh was NOT written', text);
  const catalogFile = join(w.home, '.ldm', 'catalog.json');
  assert(!existsSync(catalogFile), 'no partial state: ~/.ldm/catalog.json was NOT seeded', text);
  const bridgeDist = join(w.extDir, 'lesa-bridge', 'dist');
  assert(!existsSync(bridgeDist), 'no partial state: bridge files were NOT deployed', text);
  rmSync(w.home, { recursive: true, force: true });
}

console.log('');
if (failed > 0) {
  console.log(`${failed} test(s) failed.`);
  process.exit(1);
}
console.log('All bin manifest tests passed.');
