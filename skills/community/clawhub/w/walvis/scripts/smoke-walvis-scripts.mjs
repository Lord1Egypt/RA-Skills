#!/usr/bin/env node

import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');

function runNode(args, home) {
  return spawnSync('node', args, {
    cwd: repoRoot,
    env: { ...process.env, HOME: home },
    encoding: 'utf8',
  });
}

function parseSingleJson(stdout, label) {
  const text = stdout.trim();
  assert.ok(text.length > 0, `${label}: expected JSON output`);
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`${label}: output is not a single valid JSON value:\n${stdout}`);
  }
}

function writeJson(path, payload) {
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function createFixtureHome() {
  const home = mkdtempSync(join(tmpdir(), 'walvis-smoke-'));
  const walvisDir = join(home, '.walvis');
  const spacesDir = join(walvisDir, 'spaces');
  mkdirSync(spacesDir, { recursive: true });

  writeJson(join(walvisDir, 'manifest.json'), {
    agent: 'walvis',
    network: 'testnet',
    activeSpace: 'default',
    spaces: {
      default: { name: 'default', updatedAt: '2026-03-10T10:00:00.000Z' },
      research: { name: 'research', updatedAt: '2026-03-10T10:00:00.000Z' },
    },
  });

  writeJson(join(spacesDir, 'default.json'), {
    id: 'default',
    name: 'default',
    createdAt: '2026-03-10T09:00:00.000Z',
    updatedAt: '2026-03-10T10:00:00.000Z',
    items: [
      {
        id: 'i1',
        title: 'AI Article',
        summary: 'A deep dive into AI agents and practical use.',
        type: 'link',
        url: 'https://example.com/ai',
        tags: ['ai', 'agents'],
        notes: 'reference',
        content: 'agent architecture and planning',
        createdAt: '2026-03-10T09:59:00.000Z',
        updatedAt: '2026-03-10T09:59:00.000Z',
      },
      {
        id: 'i2',
        title: 'Sui Note',
        summary: 'Quick note about Sui testnet setup.',
        type: 'text',
        url: '',
        tags: ['sui', 'testnet'],
        notes: '',
        content: 'configure rpc endpoint',
        createdAt: '2026-03-10T09:58:00.000Z',
        updatedAt: '2026-03-10T09:58:00.000Z',
      },
    ],
  });

  writeJson(join(spacesDir, 'research.json'), {
    id: 'research',
    name: 'research',
    createdAt: '2026-03-10T09:00:00.000Z',
    updatedAt: '2026-03-10T10:00:00.000Z',
    items: [],
  });

  return home;
}

function expect(label, fn) {
  try {
    fn();
    console.log(`PASS ${label}`);
  } catch (err) {
    console.error(`FAIL ${label}`);
    throw err;
  }
}

function main() {
  const fixtureHome = createFixtureHome();
  const emptyHome = mkdtempSync(join(tmpdir(), 'walvis-smoke-empty-'));

  try {
    expect('list page 1 returns message payload', () => {
      const res = runNode(['scripts/list.mjs', '1'], fixtureHome);
      assert.equal(res.status, 0, res.stderr);
      const json = parseSingleJson(res.stdout, 'list page 1');
      assert.equal(json.action, 'send');
      assert.equal(json.channel, 'telegram');
      assert.match(json.message, /WALVIS List — default/);
      assert.ok(Array.isArray(json.buttons));
    });

    expect('list missing space returns single error object', () => {
      const res = runNode(['scripts/list.mjs', '1', 'does-not-exist'], fixtureHome);
      assert.equal(res.status, 0, res.stderr);
      const json = parseSingleJson(res.stdout, 'list missing space');
      assert.equal(typeof json.error, 'string');
      assert.match(json.error, /not found/i);
    });

    expect('search query returns message payload', () => {
      const res = runNode(['scripts/search.mjs', 'ai', '1'], fixtureHome);
      assert.equal(res.status, 0, res.stderr);
      const json = parseSingleJson(res.stdout, 'search query');
      assert.equal(json.action, 'send');
      assert.equal(json.channel, 'telegram');
      assert.match(json.message, /WALVIS Search — "ai"/);
      assert.ok(Array.isArray(json.buttons));
    });

    expect('search no-result returns empty object', () => {
      const res = runNode(['scripts/search.mjs', 'nonexistent', '1'], fixtureHome);
      assert.equal(res.status, 0, res.stderr);
      const json = parseSingleJson(res.stdout, 'search no-result');
      assert.equal(json.empty, true);
      assert.equal(json.query, 'nonexistent');
    });

    expect('msg wrapper returns payload', () => {
      const res = runNode(['scripts/msg.mjs', 'reminder', 'hello'], fixtureHome);
      assert.equal(res.status, 0, res.stderr);
      const json = parseSingleJson(res.stdout, 'msg reminder');
      assert.equal(json.action, 'send');
      assert.equal(json.channel, 'telegram');
      assert.ok(Array.isArray(json.buttons));
    });

    expect('list on uninitialized home returns JSON error', () => {
      const res = runNode(['scripts/list.mjs', '1'], emptyHome);
      assert.equal(res.status, 0, res.stderr);
      const json = parseSingleJson(res.stdout, 'list uninitialized');
      assert.equal(typeof json.error, 'string');
      assert.match(json.error, /not initialized/i);
    });

    expect('search on uninitialized home returns JSON error', () => {
      const res = runNode(['scripts/search.mjs', 'ai', '1'], emptyHome);
      assert.equal(res.status, 0, res.stderr);
      const json = parseSingleJson(res.stdout, 'search uninitialized');
      assert.equal(typeof json.error, 'string');
      assert.match(json.error, /not initialized/i);
    });

    expect('search without query exits with usage error', () => {
      const res = runNode(['scripts/search.mjs'], fixtureHome);
      assert.equal(res.status, 1);
      assert.match(res.stderr, /Usage:/i);
    });

    console.log('\nAll WALVIS script smoke tests passed.');
  } finally {
    rmSync(fixtureHome, { recursive: true, force: true });
    rmSync(emptyHome, { recursive: true, force: true });
  }
}

main();
