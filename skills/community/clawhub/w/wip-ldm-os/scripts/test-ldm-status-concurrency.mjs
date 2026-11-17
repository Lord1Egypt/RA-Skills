#!/usr/bin/env node
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const tempRoot = mkdtempSync(join(tmpdir(), 'ldm-status-concurrency-'));
const sourceVersion = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address()));
  });
}

function createRegistryServer(delayMs) {
  let active = 0;
  let maxActive = 0;
  const server = createServer((_req, res) => {
    active += 1;
    maxActive = Math.max(maxActive, active);
    setTimeout(() => {
      res.setHeader('content-type', 'application/json');
      res.end(JSON.stringify({ 'dist-tags': { latest: '1.0.0' } }));
      active -= 1;
    }, delayMs);
  });
  return { server, getMaxActive: () => maxActive };
}

function writeFixture(home) {
  const extensions = join(home, '.ldm', 'extensions');
  mkdirSync(extensions, { recursive: true });
  writeFileSync(join(home, '.ldm', 'version.json'), JSON.stringify({
    version: '0.0.0-test',
    installed: '2026-05-12T00:00:00.000Z',
    updated: '2026-05-12T00:00:00.000Z',
  }, null, 2) + '\n');

  const registry = { extensions: {} };
  for (let i = 1; i <= 8; i += 1) {
    registry.extensions[`ext-${i}`] = {
      source: { npm: `ext-${i}` },
      installed: { version: '1.0.0' },
    };
  }
  writeFileSync(join(extensions, 'registry.json'), JSON.stringify(registry, null, 2) + '\n');
}

function runStatus({ concurrency, registryUrl, home }) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [join(root, 'bin', 'ldm.js'), 'status'], {
      cwd: root,
      env: {
        ...process.env,
        HOME: home,
        LDM_STATUS_NPM_REGISTRY_URL: registryUrl,
        LDM_STATUS_NPM_CONCURRENCY: String(concurrency),
        LDM_STATUS_NPM_TIMEOUT_MS: '2000',
        LDM_STATUS_TOTAL_BUDGET_MS: '10000',
      },
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let stdout = '';
    let stderr = '';
    child.stdout.setEncoding('utf8');
    child.stderr.setEncoding('utf8');
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('close', status => resolve({ status, stdout, stderr }));
  });
}

async function runFixture({ concurrency, delayMs }) {
  const home = join(tempRoot, `home-${concurrency}-${delayMs}`);
  writeFixture(home);
  const registry = createRegistryServer(delayMs);
  const address = await listen(registry.server);
  const startedAt = Date.now();
  const result = await runStatus({
    concurrency,
    home,
    registryUrl: `http://${address.address}:${address.port}`,
  });
  const elapsedMs = Date.now() - startedAt;
  registry.server.closeAllConnections();
  registry.server.close();
  return { result, elapsedMs, maxActive: registry.getMaxActive() };
}

try {
  const concurrent = await runFixture({ concurrency: 4, delayMs: 500 });
  assert(concurrent.result.status === 0, `concurrent ldm status exited ${concurrent.result.status}\nstdout:\n${concurrent.result.stdout}\nstderr:\n${concurrent.result.stderr}`);
  assert(concurrent.elapsedMs < 3000, `concurrent ldm status should finish well before serial runtime; elapsed ${concurrent.elapsedMs}ms`);
  assert(concurrent.maxActive >= 4, `registry server should see concurrent probes; max active ${concurrent.maxActive}`);
  assert(concurrent.result.stdout.includes(`LDM OS v${sourceVersion}`), `status should print installed LDM OS version\n${concurrent.result.stdout}`);
  assert(concurrent.result.stdout.includes('Extensions: 8'), `status should print extension count\n${concurrent.result.stdout}`);
  assert(concurrent.result.stdout.includes('ext-8: checking npm'), `status should check every staged extension\n${concurrent.result.stdout}`);
  assert(!concurrent.result.stdout.includes('Update checks skipped:'), `concurrent status should not skip checks in this fixture\n${concurrent.result.stdout}`);

  const serialFallback = await runFixture({ concurrency: 1, delayMs: 10 });
  assert(serialFallback.result.status === 0, `serial fallback ldm status exited ${serialFallback.result.status}\nstdout:\n${serialFallback.result.stdout}\nstderr:\n${serialFallback.result.stderr}`);
  assert(serialFallback.maxActive === 1, `serial fallback should only run one probe at a time; max active ${serialFallback.maxActive}`);
  assert(serialFallback.result.stdout.includes('ext-8: checking npm'), `serial fallback should still check every staged extension\n${serialFallback.result.stdout}`);
  assert(!serialFallback.result.stdout.includes('Update checks skipped:'), `serial fallback should not skip checks in this fixture\n${serialFallback.result.stdout}`);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}

console.log('ldm status concurrency regression passed');
