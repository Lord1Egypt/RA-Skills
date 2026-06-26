// scanner-sim: allow — *.test.ts files are excluded from the npm tarball (see "files" array in package.json) and never reach the OpenClaw runtime sandbox. This test invokes check-url-binding.mjs as a subprocess; the child_process import is test-infrastructure only and not shipped.
/**
 * Regression test for the env-binding contract after the F flip (3.3.12-rc.1).
 *
 * Hard invariants (post-F-flip):
 *   - Source default for `TOTALRECLAW_SERVER_URL` is `api.totalreclaw.xyz`.
 *   - Both `release-type=rc` and `release-type=stable` artifacts ship the
 *     production URL by default. There is no longer a publish-time URL
 *     rewrite — the source already binds to production.
 *   - Staging access is opt-in via env override
 *     (TOTALRECLAW_SERVER_URL=https://api-staging.totalreclaw.xyz).
 *
 * The `check-url-binding.mjs` guard asserts:
 *   - The artifact MUST contain `api.totalreclaw.xyz` somewhere
 *     (proves the canonical default-URL site is intact).
 *   - The artifact MUST NOT contain `api-staging.totalreclaw.xyz` anywhere
 *     in the artifact tree (no stranded staging defaults).
 *
 * Run with: `npx tsx url-binding.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const here = path.dirname(fileURLToPath(import.meta.url));
const SCRIPT = path.resolve(here, '..', 'scripts', 'check-url-binding.mjs');

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* swallow */ }
}

interface RunResult {
  status: number;
  stdout: string;
  stderr: string;
}

function runGuard(pluginRoot: string, mode: 'rc' | 'stable'): RunResult {
  const stagedScripts = path.join(pluginRoot, '..', 'scripts');
  fs.mkdirSync(stagedScripts, { recursive: true });
  const scriptCopy = path.join(stagedScripts, 'check-url-binding.mjs');
  if (!fs.existsSync(scriptCopy)) fs.copyFileSync(SCRIPT, scriptCopy);
  try {
    const out = execFileSync('node', [scriptCopy, `--release-type=${mode}`], {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return { status: 0, stdout: out, stderr: '' };
  } catch (err) {
    const e = err as { status?: number; stdout?: Buffer | string; stderr?: Buffer | string };
    return {
      stdout: typeof e.stdout === 'string' ? e.stdout : (e.stdout?.toString() ?? ''),
      stderr: typeof e.stderr === 'string' ? e.stderr : (e.stderr?.toString() ?? ''),
      status: e.status ?? -1,
    };
  }
}

function stagePluginTree(opts: { distContent: string; skillJson?: string }): {
  pluginRoot: string;
  cleanup: () => void;
} {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-url-binding-'));
  const pluginRoot = path.join(tmp, 'skill', 'plugin');
  fs.mkdirSync(path.join(pluginRoot, 'dist'), { recursive: true });
  fs.writeFileSync(path.join(pluginRoot, 'dist', 'config.js'), opts.distContent);
  // Default skill.json has the openclaw.config.serverUrl.default field bound
  // to production, matching the post-F-flip contract.
  const defaultSkillJson = JSON.stringify({
    version: 'test',
    openclaw: {
      config: {
        serverUrl: { default: 'https://api.totalreclaw.xyz' },
      },
    },
  });
  fs.writeFileSync(
    path.join(pluginRoot, 'skill.json'),
    opts.skillJson ?? defaultSkillJson,
  );
  return { pluginRoot, cleanup: () => rmrf(tmp) };
}

// ---------------------------------------------------------------------------
// Test 1 — RC artifact with production URL passes RC guard
// ---------------------------------------------------------------------------
{
  const { pluginRoot, cleanup } = stagePluginTree({
    distContent: `export const SERVER_URL = 'https://api.totalreclaw.xyz';\n`,
  });
  const r = runGuard(pluginRoot, 'rc');
  assert(r.status === 0, 'rc guard passes when artifact contains production URL');
  assert(r.stdout.includes('OK (rc mode)'), 'rc OK message in stdout');
  cleanup();
}

// ---------------------------------------------------------------------------
// Test 2 — RC artifact with JS-side staging-URL default literal FAILS RC guard
// (Defensive: prevents accidental staging stranding under post-F-flip rules.)
// ---------------------------------------------------------------------------
{
  const { pluginRoot, cleanup } = stagePluginTree({
    distContent: `export const SERVER_URL = 'https://api-staging.totalreclaw.xyz';\n`,
  });
  const r = runGuard(pluginRoot, 'rc');
  assert(r.status === 1, 'rc guard fails when artifact still contains staging URL literal');
  assert(r.stderr.includes('FAIL (rc mode)'), 'rc FAIL message in stderr');
  cleanup();
}

// ---------------------------------------------------------------------------
// Test 3 — stable artifact with production URL passes stable guard
// (default skillJson is well-formed and binds to production)
// ---------------------------------------------------------------------------
{
  const { pluginRoot, cleanup } = stagePluginTree({
    distContent: `export const SERVER_URL = 'https://api.totalreclaw.xyz';\n`,
  });
  const r = runGuard(pluginRoot, 'stable');
  assert(r.status === 0, 'stable guard passes when artifact contains production URL only');
  assert(r.stdout.includes('OK (stable mode)'), 'stable OK message in stdout');
  cleanup();
}

// ---------------------------------------------------------------------------
// Test 4 — stable artifact with JS-side staging-URL default literal FAILS
// ---------------------------------------------------------------------------
{
  const { pluginRoot, cleanup } = stagePluginTree({
    distContent: `export const SERVER_URL = 'https://api-staging.totalreclaw.xyz';\n`,
  });
  const r = runGuard(pluginRoot, 'stable');
  assert(r.status === 1, 'stable guard fails when artifact still contains staging URL literal');
  assert(r.stderr.includes('FAIL (stable mode)'), 'stable FAIL message in stderr');
  assert(
    r.stderr.includes('staging'),
    'stable FAIL message names the issue',
  );
  cleanup();
}

// ---------------------------------------------------------------------------
// Test 5 — stable artifact with NEITHER URL FAILS stable guard
// (No production hits anywhere; also skill.json structure missing.)
// ---------------------------------------------------------------------------
{
  const { pluginRoot, cleanup } = stagePluginTree({
    distContent: `export const NOTHING = 1;\n`,
    skillJson: '{"version": "test"}',
  });
  const r = runGuard(pluginRoot, 'stable');
  assert(r.status === 1, 'stable guard fails when artifact has no api.totalreclaw.xyz');
  assert(r.stderr.includes('FAIL (stable mode)'), 'stable FAIL message in stderr');
  cleanup();
}

// ---------------------------------------------------------------------------
console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) process.exit(1);
