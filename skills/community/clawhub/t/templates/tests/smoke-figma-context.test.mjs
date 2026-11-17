import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import { runSmoke } from '../scripts/smoke-figma-context.mjs';

async function makeTempDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-smoke-test-'));
}

describe('runSmoke', () => {
  it('prints help without requiring credentials or network', async () => {
    const result = await runSmoke(['node', 'script', '--help']);

    assert.equal(result.exitCode, 0);
    assert.equal(result.code, 'smoke_succeeded');
    assert.match(result.output, /read-figma-design/);
  });

  it('adds require screenshot behavior for non-help runs', async () => {
    const result = await runSmoke(['node', 'script']);

    assert.equal(result.exitCode, 1);
    assert.equal(result.code, 'figma_input_required');
  });

  it('verifies /v1/me before reading Figma nodes in smoke runs', async () => {
    const tempDir = await makeTempDir();
    const repo = path.join(tempDir, 'repo');
    const out = path.join(repo, '.multica', 'figma-context');
    await fs.mkdir(path.join(repo, '.git', 'info'), { recursive: true });
    const calls = [];
    const node = {
      id: '1:2',
      name: 'Target',
      type: 'FRAME',
      absoluteBoundingBox: { x: 0, y: 0, width: 100, height: 40 },
      children: [],
    };
    const client = {
      async getMe() {
        calls.push('getMe');
        return { id: 'user-1' };
      },
      async getNode() {
        calls.push('getNode');
        return { fileVersion: '123', document: node };
      },
      async getFile() {
        calls.push('getFile');
        return {
          fileVersion: '123',
          document: {
            id: '0:0',
            name: 'Doc',
            type: 'DOCUMENT',
            children: [{ id: '0:1', name: 'Page', type: 'CANVAS', children: [node] }],
          },
        };
      },
      async exportNodeImage({ outPath }) {
        calls.push('exportNodeImage');
        await fs.mkdir(path.dirname(outPath), { recursive: true });
        await fs.writeFile(outPath, Buffer.from([1, 2, 3]));
        return { path: outPath, byteLength: 3 };
      },
    };

    const result = await runSmoke(
      [
        'node',
        'script',
        '--url',
        'https://www.figma.com/design/fileKey123/File?node-id=1-2',
        '--out',
        out,
        '--repo',
        repo,
      ],
      {
        cwd: tempDir,
        env: {},
        createClient: () => client,
      },
    );

    assert.equal(result.exitCode, 0);
    assert.equal(result.runDirRelative.startsWith('.multica/figma-context/'), true);
    assert.equal(path.isAbsolute(result.runDirRelative), false);
    assert.equal(calls[0], 'getMe');
    assert.equal(calls.filter((call) => call === 'getMe').length, 1);
    assert.ok(calls.indexOf('getMe') < calls.indexOf('getNode'));
  });
});
