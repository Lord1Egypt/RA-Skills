#!/usr/bin/env node
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const tempRoot = mkdtempSync(join(tmpdir(), 'ldm-status-timeout-'));
const sourceVersion = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function runStatus({ home, registryUrl }) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [join(root, 'bin', 'ldm.js'), 'status'], {
      cwd: root,
      env: {
        ...process.env,
        HOME: home,
        LDM_STATUS_NPM_REGISTRY_URL: registryUrl,
        LDM_STATUS_NPM_TIMEOUT_MS: '75',
        LDM_STATUS_TOTAL_BUDGET_MS: '250',
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

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address()));
  });
}

try {
  const home = join(tempRoot, 'home');
  const extensions = join(home, '.ldm', 'extensions');

  mkdirSync(extensions, { recursive: true });
  writeFileSync(join(home, '.ldm', 'version.json'), JSON.stringify({
    version: '0.0.0-test',
    installed: '2026-05-12T00:00:00.000Z',
    updated: '2026-05-12T00:00:00.000Z',
  }, null, 2) + '\n');
  writeFileSync(join(extensions, 'registry.json'), JSON.stringify({
    extensions: {
      'hung-extension': {
        source: { npm: 'hung-extension' },
        installed: { version: '1.0.0' },
      },
      'second-extension': {
        source: { npm: 'second-extension' },
        installed: { version: '1.0.0' },
      },
    },
  }, null, 2) + '\n');

  const server = createServer((_req, res) => {
    setTimeout(() => {
      res.setHeader('content-type', 'application/json');
      res.end(JSON.stringify({ 'dist-tags': { latest: '9.9.9' } }));
    }, 2000);
  });
  const address = await listen(server);

  const startedAt = Date.now();
  const result = await runStatus({ home, registryUrl: `http://${address.address}:${address.port}` });
  const elapsedMs = Date.now() - startedAt;
  server.closeAllConnections();
  server.close();

  assert(result.status === 0, `ldm status exited ${result.status}\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`);
  assert(elapsedMs < 2500, `ldm status should return before the process timeout; elapsed ${elapsedMs}ms`);
  assert(result.stdout.includes(`LDM OS v${sourceVersion}`), `status should print installed LDM OS version\n${result.stdout}`);
  assert(result.stdout.includes('Extensions: 2'), `status should print extension count\n${result.stdout}`);
  assert(result.stdout.includes('Checking updates:'), `status should show progress before update checks\n${result.stdout}`);
  assert(result.stdout.includes('hung-extension: checking npm'), `status should print the extension name before probing it\n${result.stdout}`);
  assert(result.stdout.includes('Update checks skipped:'), `status should report skipped checks instead of hanging\n${result.stdout}`);
  assert(/hung-extension: \[timeout \d+(ms|\.\d+s)\] hung-extension/.test(result.stdout), `hung extension should be reported as a timeout with elapsed time\n${result.stdout}`);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}

console.log('ldm status timeout regression passed');
