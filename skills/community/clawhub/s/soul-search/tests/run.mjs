#!/usr/bin/env node

import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const script = path.resolve(here, '..', 'scripts', 'soul.mjs');
const moduleUrl = pathToFileURL(script).href;
const soul = await import(moduleUrl);

async function mktemp() {
  return await fs.mkdtemp(path.join(os.tmpdir(), 'openclaw-soul-test-'));
}

async function writeJson(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, JSON.stringify(value, null, 2) + '\n', 'utf8');
}

async function writeText(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, value, 'utf8');
}

async function setupWorkspace({ state, cache, soulContent } = {}) {
  const dir = await mktemp();
  if (state) await writeJson(path.join(dir, 'soul-data', 'state.json'), state);
  if (cache) await writeJson(path.join(dir, 'soul-data', 'cache', 'agents.json'), cache);
  if (typeof soulContent === 'string') await writeText(path.join(dir, 'SOUL.md'), soulContent);
  return dir;
}

async function test(name, fn) {
  try {
    await fn();
    console.log(`PASS ${name}`);
  } catch (err) {
    console.error(`FAIL ${name}`);
    console.error(err?.stack || String(err));
    process.exitCode = 1;
  }
}

async function runInWorkspace(cwd, fn) {
  const prev = process.cwd();
  process.chdir(cwd);
  try {
    return await fn();
  } finally {
    process.chdir(prev);
  }
}

const validCatalog = {
  agents: [
    {
      id: 'pirate',
      category: 'fun',
      name: 'Pirate',
      role: 'Talks like a pirate',
      path: 'agents/pirate/SOUL.md'
    }
  ]
};

await test('help output includes refresh', async () => {
  const cwd = await setupWorkspace();
  const result = await runInWorkspace(cwd, async () => {
    const lines = [];
    const orig = console.log;
    console.log = (msg) => lines.push(String(msg));
    try {
      await soul.showHelp();
    } finally {
      console.log = orig;
    }
    return { code: 0, stdout: lines.join('\n') };
  });
  assert.equal(result.code, 0);
  assert.match(result.stdout, /soul refresh/);
});

await test('refresh fails on invalid cached catalog shape', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    cache: { agents: 'broken' }
  });
  await runInWorkspace(cwd, async () => {
    assert.throws(() => soul.validateCatalog({ agents: 'broken' }), /Catalog must contain an agents array/);
  });
});

await test('categories works from valid cache', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    cache: validCatalog
  });
  await runInWorkspace(cwd, async () => {
    const catalog = soul.validateCatalog(validCatalog);
    const categories = soul.byCategory(catalog);
    assert.deepEqual(categories[0][0], 'fun');
  });
});

await test('show prints useful metadata', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    cache: validCatalog
  });
  await runInWorkspace(cwd, async () => {
    const agent = soul.findAgent(soul.validateCatalog(validCatalog), 'pirate');
    assert.equal(agent?.id, 'pirate');
    const url = soul.buildRawSoulUrl({ catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json' }, agent);
    assert.match(url, /raw\.githubusercontent\.com/);
  });
});

await test('current defaults to builtin soul', async () => {
  const cwd = await setupWorkspace();
  await runInWorkspace(cwd, async () => {
    const current = await soul.currentSoul({ current: null, catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json', lastFetchedAt: null });
    assert.equal(current.id, 'openclaw-default');
    assert.equal(current.category, 'builtin');
  });
});

await test('restore fails cleanly when no backup exists', async () => {
  const cwd = await setupWorkspace();
  await runInWorkspace(cwd, async () => {
    const backups = await soul.listBackups();
    assert.deepEqual(backups, []);
  });
});

await test('restore stores checksum-capable current state', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    soulContent: '# Current\n\nOld soul\n'
  });
  const backupPath = path.join(cwd, 'soul-data', 'backups', 'SOUL-1.md');
  await writeText(backupPath, '# Restored\n\nBacked up soul\n');
  await runInWorkspace(cwd, async () => {
    const content = await fs.readFile(backupPath, 'utf8');
    const checksum = crypto.createHash('sha1').update(content, 'utf8').digest('hex');
    const state = await soul.loadState();
    state.current = { id: 'custom', category: 'local', sourceUrl: backupPath, appliedAt: new Date().toISOString(), checksum, custom: true };
    await soul.saveState(state);
  });
  const state = JSON.parse(await fs.readFile(path.join(cwd, 'soul-data', 'state.json'), 'utf8'));
  state.current = { id: 'custom', category: 'local', sourceUrl: backupPath, appliedAt: new Date().toISOString(), checksum: crypto.createHash('sha1').update(await fs.readFile(backupPath, 'utf8'), 'utf8').digest('hex'), custom: true };
  await writeJson(path.join(cwd, 'soul-data', 'state.json'), state);
  const updated = JSON.parse(await fs.readFile(path.join(cwd, 'soul-data', 'state.json'), 'utf8'));
  assert.equal(updated.current.id, 'custom');
  assert.match(updated.current.checksum, /^[a-f0-9]{40}$/);
});

await test('show returns a simple not-found message for unknown id', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    cache: validCatalog
  });
  await runInWorkspace(cwd, async () => {
    const agent = soul.findAgent(soul.validateCatalog(validCatalog), 'pirat');
    assert.equal(agent, undefined);
  });
});

await test('list returns a simple not-found message for unknown category', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    cache: validCatalog
  });
  await runInWorkspace(cwd, async () => {
    const matches = soul.searchAgents(soul.validateCatalog(validCatalog), 'fuun');
    assert.equal(matches.length, 0);
  });
});

await test('apply accepts a relative path entry', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    cache: { agents: [{ id: 'oops', category: 'fun', path: './local/SOUL.md' }] },
    soulContent: '# Existing\n'
  });
  await writeText(path.join(cwd, 'local', 'SOUL.md'), '# Local\n\nLocal soul\n');
  await runInWorkspace(cwd, async () => {
    const agent = soul.findAgent(soul.validateCatalog({ agents: [{ id: 'oops', category: 'fun', path: './local/SOUL.md' }] }), 'oops');
    const url = soul.buildRawSoulUrl({ catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json' }, agent);
    assert.match(url, /local\/SOUL\.md$/);
  });
});

await test('rejects local paths outside workspace', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    cache: { agents: [{ id: 'oops', category: 'fun', path: '../evil/SOUL.md' }] },
    soulContent: '# Existing\n'
  });
  await runInWorkspace(cwd, async () => {
    assert.throws(() => soul.buildRawSoulUrl({ catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json' }, { path: '../evil/SOUL.md' }), /escapes workspace/);
  });
});

await test('manual edit is detected as custom', async () => {
  const cwd = await setupWorkspace({
    state: {
      catalogUrl: 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json'
    },
    soulContent: '# Existing\n'
  });
  const state = JSON.parse(await fs.readFile(path.join(cwd, 'soul-data', 'state.json'), 'utf8'));
  state.current = {
    id: 'orion',
    category: 'curated',
    sourceUrl: 'https://example.invalid/orion/SOUL.md',
    appliedAt: '2026-03-29T00:00:00.000Z',
    checksum: crypto.createHash('sha1').update('# Original\n', 'utf8').digest('hex'),
    custom: false
  };
  await writeJson(path.join(cwd, 'soul-data', 'state.json'), state);
  await writeText(path.join(cwd, 'SOUL.md'), '# Edited\n');
  await runInWorkspace(cwd, async () => {
    const current = await soul.currentSoul(state);
    assert.equal(current.id, 'custom');
    assert.match(current.note, /custom, from https:\/\/example\.invalid\/orion\/SOUL\.md \(modified\)/);
  });
});

if (process.exitCode) {
  process.exit(process.exitCode);
}
