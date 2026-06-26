#!/usr/bin/env node

import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import registerFastPath from '../extensions/walvis-fastpath/index.js';

const TESTNET_SEAL_PACKAGE_ID = '0x299d7d7592c84d08a25ec26c777933d6ab72e51b31a615027186a0a377fe75cb';

function writeJson(path, payload) {
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function setupHomeFixture() {
  const home = mkdtempSync(join(tmpdir(), 'walvis-fastpath-'));
  const walvisDir = join(home, '.walvis');
  const spacesDir = join(walvisDir, 'spaces');
  mkdirSync(spacesDir, { recursive: true });

  writeJson(join(walvisDir, 'manifest.json'), {
    agent: 'walvis',
    fastPathEnabled: true,
    network: 'testnet',
    activeSpace: 'default',
    walrusPublisher: 'https://publisher.walrus-testnet.walrus.space',
    walrusAggregator: 'https://aggregator.walrus-testnet.walrus.space',
    spaces: {
      default: { name: 'default', updatedAt: '2026-03-10T00:00:00.000Z' },
      research: { name: 'research', updatedAt: '2026-03-10T00:00:00.000Z' },
    },
    items: {},
  });

  writeJson(join(spacesDir, 'default.json'), {
    id: 'default',
    name: 'default',
    createdAt: '2026-03-10T00:00:00.000Z',
    updatedAt: '2026-03-10T00:00:00.000Z',
    items: [
      {
        id: 'a1',
        type: 'link',
        title: 'AI Article',
        summary: 'A practical guide to agent systems.',
        tags: ['ai', 'agent'],
        content: 'agent planning and execution',
        notes: '',
        screenshotBlobId: 'blob-screen-1',
        url: 'https://example.com/ai',
        createdAt: '2026-03-10T00:01:00.000Z',
        updatedAt: '2026-03-10T00:01:00.000Z',
      },
      {
        id: 'a2',
        type: 'link',
        title: 'Sui Notes',
        summary: 'Notes about Sui wallets and blobs.',
        tags: ['sui', 'wallet'],
        content: 'walrus publisher and manifest',
        notes: '',
        url: 'https://example.com/sui',
        createdAt: '2026-03-10T00:02:00.000Z',
        updatedAt: '2026-03-10T00:02:00.000Z',
      },
      {
        id: 'a3',
        type: 'text',
        title: 'Reading Queue',
        summary: 'Follow up on agent papers.',
        tags: ['reading'],
        content: 'agent papers',
        notes: '',
        createdAt: '2026-03-10T00:03:00.000Z',
        updatedAt: '2026-03-10T00:03:00.000Z',
      },
      {
        id: 'a4',
        type: 'text',
        title: 'Infra Checklist',
        summary: 'Container mount notes.',
        tags: ['infra'],
        content: 'mounts hooks plugins',
        notes: '',
        createdAt: '2026-03-10T00:04:00.000Z',
        updatedAt: '2026-03-10T00:04:00.000Z',
      },
      {
        id: 'a5',
        type: 'text',
        title: 'Inline Buttons',
        summary: 'Telegram callback experiments.',
        tags: ['telegram'],
        content: 'inline keyboard buttons',
        notes: '',
        createdAt: '2026-03-10T00:05:00.000Z',
        updatedAt: '2026-03-10T00:05:00.000Z',
      },
      {
        id: 'a6',
        type: 'text',
        title: 'Second Page Item',
        summary: 'Used for pagination checks.',
        tags: ['paging'],
        content: 'page two content',
        notes: '',
        createdAt: '2026-03-10T00:06:00.000Z',
        updatedAt: '2026-03-10T00:06:00.000Z',
      },
    ],
  });

  writeJson(join(spacesDir, 'research.json'), {
    id: 'research',
    name: 'research',
    createdAt: '2026-03-10T00:00:00.000Z',
    updatedAt: '2026-03-10T00:00:00.000Z',
    items: [],
  });

  return home;
}

function createRegistry() {
  const entries = new Map();
  return {
    api: {
      registerCommand(def) {
        entries.set(def.name, def);
      },
    },
    entries,
  };
}

async function invoke(entries, name, args = '', extraCtx = {}) {
  const def = entries.get(name);
  assert.ok(def, `command not registered: ${name}`);
  return def.handler({
    args,
    channelId: 'telegram',
    accountId: 'acct1',
    senderId: 'user1',
    from: 'user1',
    ...extraCtx,
  });
}

async function main() {
  const originalHome = process.env.HOME;
  const originalFetch = globalThis.fetch;
  const fixtureHome = setupHomeFixture();
  let uploadCount = 0;

  try {
    process.env.HOME = fixtureHome;
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url);
      if ((options.method ?? 'GET') === 'PUT' && target.includes('/v1/blobs?epochs=')) {
        uploadCount += 1;
        return {
          ok: true,
          async json() {
            return {
              newlyCreated: {
                blobObject: {
                  blobId: `blob-${uploadCount}`,
                },
              },
            };
          },
        };
      }
      if ((options.method ?? 'GET') === 'GET' && target === 'https://example.com/new-bookmark') {
        return {
          ok: true,
          async text() {
            return '<title>Example Bookmark</title><meta name="description" content="Saved without LLM for smoke testing.">';
          },
        };
      }
      throw new Error(`Unexpected fetch: ${target}`);
    };

    const { api, entries } = createRegistry();
    registerFastPath(api);

    const requiredCommands = [
      'walvis-fastpath',
      'walvis-list',
      'walvis-list-page',
      'walvis-search',
      'walvis-search-page',
      'walvis-run',
      'walvis-sync',
      'walvis-tags',
      'walvis-note',
      'walvis-pending',
      'walvis-delete',
      'walvis-encrypt',
    ];
    for (const name of requiredCommands) assert.ok(entries.has(name), `${name} should be registered`);

    const status = await invoke(entries, 'walvis-fastpath', 'status');
    assert.match(status.text, /Fast path status: ON/);
    const manifestAfterInit = readJson(join(fixtureHome, '.walvis', 'manifest.json'));
    assert.equal(manifestAfterInit.sealPackageId, TESTNET_SEAL_PACKAGE_ID);

    const list = await invoke(entries, 'walvis-list');
    assert.match(list.text, /WALVIS List — default/);
    assert.match(list.text, /Page 1\/2 • 6 item\(s\)/);
    assert.equal(Array.isArray(list.channelData.telegram.buttons), true);
    assert.equal(list.channelData.telegram.buttons[0][0].text, '🏷 Tags');
    assert.equal(list.channelData.telegram.buttons[0][1].text, '📝 Note');
    assert.equal(list.channelData.telegram.buttons[0][2].text, '🗑 Delete');
    assert.equal(list.channelData.telegram.buttons[0][0].callback_data, '/walvis-tags a6');
    assert.equal(list.channelData.telegram.buttons.at(-2)[0].callback_data, '/walvis-list-page 2');
    assert.equal(list.channelData.telegram.buttons.at(-1)[0].callback_data, '/walvis-sync');

    const page2 = await invoke(entries, 'walvis-list-page', '2');
    assert.match(page2.text, /Page 2\/2 • 6 item\(s\)/);
    assert.match(page2.text, /AI Article/);

    const search = await invoke(entries, 'walvis-search', 'agent');
    assert.match(search.text, /WALVIS Search — "agent"/);
    assert.match(search.channelData.telegram.buttons[0][0].callback_data, /^\/walvis-tags a[13]$/);

    const tagsPending = await invoke(entries, 'walvis-tags', 'a1');
    assert.match(tagsPending.text, /Send the new tags as your next message/);
    const pendingState1 = readJson(join(fixtureHome, '.walvis', 'fastpath-state.json'));
    assert.equal(Object.keys(pendingState1.pending).length, 1);

    const tagsApplied = await invoke(entries, 'walvis-pending', 'focus roadmap');
    assert.match(tagsApplied.text, /Updated tags for AI Article/);
    assert.match(tagsApplied.text, /#focus/);
    assert.match(tagsApplied.text, /#roadmap/);

    const notePending = await invoke(entries, 'walvis-note', 'a1');
    assert.match(notePending.text, /Send the new note as your next message/);
    const noteApplied = await invoke(entries, 'walvis-pending', 'check container-safe paths');
    assert.match(noteApplied.text, /Updated note for AI Article/);

    const synced = await invoke(entries, 'walvis-sync');
    assert.match(synced.text, /Synced to Walrus/);
    assert.match(synced.text, /manifest: blob-/);

    const web = await invoke(entries, 'walvis-web');
    assert.match(web.text, /Manifest blob: blob-/);
    assert.match(web.text, /paste the manifest blob ID/);

    const run = await invoke(entries, 'walvis-run');
    assert.match(run.text, /WALVIS Local Preview/);
    assert.match(run.text, /http:\/\/localhost:5173/);
    assert.match(run.text, /npm run dev:web/);

    console.log('fastpath plugin smoke tests passed.');
  } finally {
    globalThis.fetch = originalFetch;
    if (originalHome === undefined) {
      delete process.env.HOME;
    } else {
      process.env.HOME = originalHome;
    }
    rmSync(fixtureHome, { recursive: true, force: true });
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
