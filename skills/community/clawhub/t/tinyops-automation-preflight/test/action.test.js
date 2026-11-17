'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');
const test = require('node:test');
const { requestPreflight } = require('../index.js');

const ROOT = path.resolve(__dirname, '..');

function execute(env) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['index.js'], {
      cwd: ROOT,
      env: { ...process.env, ...env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += String(chunk); });
    child.stderr.on('data', (chunk) => { stderr += String(chunk); });
    child.on('error', reject);
    child.on('close', (code) => resolve({ code, stdout, stderr }));
  });
}

function executeCli(args, env) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['bin/automation-preflight.js', ...args], {
      cwd: ROOT,
      env: { ...process.env, ...env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += String(chunk); });
    child.stderr.on('data', (chunk) => { stderr += String(chunk); });
    child.on('error', reject);
    child.on('close', (code) => resolve({ code, stdout, stderr }));
  });
}

test('calls the bounded endpoint, masks the key, and writes outputs', async (t) => {
  let received;
  const server = http.createServer((request, response) => {
    let body = '';
    request.on('data', (chunk) => { body += String(chunk); });
    request.on('end', () => {
      received = { url: request.url, headers: request.headers, body: JSON.parse(body) };
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ readiness: { status: 'ready' }, service: 'TinyOps Automation Integration Preflight' }));
    });
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  const address = server.address();
  const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'tinyops-action-test-'));
  const output = path.join(workspace, 'outputs.txt');
  const summary = path.join(workspace, 'summary.md');
  const result = await execute({
    'INPUT_URL': 'https://example.com/public-form',
    'INPUT_RAPIDAPI-KEY': 'test-key-that-must-not-leak',
    'INPUT_MODE': 'analyze',
    'INPUT_OUTPUT-FILE': 'report.json',
    GITHUB_WORKSPACE: workspace,
    GITHUB_OUTPUT: output,
    GITHUB_STEP_SUMMARY: summary,
    AUTOMATION_PREFLIGHT_API_BASE_URL: `http://127.0.0.1:${address.port}`,
  });

  assert.equal(result.code, 0, result.stderr);
  assert.equal(received.url, '/rapidapi/analyze');
  assert.equal(received.body.url, 'https://example.com/public-form');
  assert.equal(received.headers['x-rapidapi-key'], 'test-key-that-must-not-leak');
  assert.match(result.stdout, /::add-mask::test-key-that-must-not-leak/);
  assert.doesNotMatch(result.stderr, /test-key-that-must-not-leak/);
  assert.equal(JSON.parse(fs.readFileSync(path.join(workspace, 'report.json'), 'utf8')).readiness.status, 'ready');
  assert.match(fs.readFileSync(output, 'utf8'), /readiness=ready/);
  assert.match(fs.readFileSync(summary, 'utf8'), /Automation integration preflight/);
});

test('rejects output paths outside the workspace before calling the API', async () => {
  const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'tinyops-action-test-'));
  const result = await execute({
    'INPUT_URL': 'https://example.com',
    'INPUT_RAPIDAPI-KEY': 'another-test-key',
    'INPUT_OUTPUT-FILE': '../outside.json',
    GITHUB_WORKSPACE: workspace,
  });
  assert.equal(result.code, 1);
  assert.match(result.stderr, /output-file must stay inside/);
  assert.doesNotMatch(result.stderr, /another-test-key/);
});

test('requests an acceptance pack through the published RapidAPI operation', async (t) => {
  let received;
  const server = http.createServer((request, response) => {
    let body = '';
    request.on('data', (chunk) => { body += String(chunk); });
    request.on('end', () => {
      received = { url: request.url, body: JSON.parse(body) };
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end(JSON.stringify({
        service: 'TinyOps Website Automation Acceptance Pack',
        acceptance_pack: { objective: received.body.objective },
      }));
    });
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  const address = server.address();
  const result = await requestPreflight({
    rapidApiKey: 'acceptance-test-key',
    url: 'https://example.com/launch',
    mode: 'acceptance-pack',
    objective: 'Verify the launch workflow.',
    apiBase: `http://127.0.0.1:${address.port}`,
  });

  assert.equal(received.url, '/rapidapi/analyze');
  assert.equal(received.body.mode, 'acceptance-pack');
  assert.equal(received.body.objective, 'Verify the launch workflow.');
  assert.equal(result.payload.acceptance_pack.objective, 'Verify the launch workflow.');
});

test('CLI writes a structured report without exposing the key', async (t) => {
  let received;
  const server = http.createServer((request, response) => {
    let body = '';
    request.on('data', (chunk) => { body += String(chunk); });
    request.on('end', () => {
      received = { url: request.url, headers: request.headers, body: JSON.parse(body) };
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ readiness: 'ready', source: 'cli-test' }));
    });
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  const address = server.address();
  const key = 'cli-test-key-that-must-not-leak';
  const result = await executeCli(['--url', 'https://example.com/form'], {
    RAPIDAPI_KEY: key,
    AUTOMATION_PREFLIGHT_API_BASE_URL: `http://127.0.0.1:${address.port}`,
  });

  assert.equal(result.code, 0, result.stderr);
  assert.equal(received.url, '/rapidapi/analyze');
  assert.equal(received.headers['x-rapidapi-key'], key);
  assert.equal(JSON.parse(result.stdout).source, 'cli-test');
  assert.doesNotMatch(result.stdout, new RegExp(key));
  assert.doesNotMatch(result.stderr, new RegExp(key));
});
