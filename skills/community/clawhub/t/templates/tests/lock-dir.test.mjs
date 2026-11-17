import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import { acquireDirectoryLock } from '../scripts/lib/lock-dir.mjs';

async function makeTempDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-lock-test-'));
}

describe('acquireDirectoryLock', () => {
  it('creates an atomic lock directory with metadata and releases it', async () => {
    const tempDir = await makeTempDir();
    const lockDir = path.join(tempDir, 'figma-oauth.lock');

    const lock = await acquireDirectoryLock(lockDir, {
      now: () => new Date('2026-07-22T00:00:00Z'),
      hostname: () => 'test-host',
    });

    const stat = await fs.stat(lockDir);
    assert.equal(stat.isDirectory(), true);

    const metadata = JSON.parse(await fs.readFile(path.join(lockDir, 'lock.json'), 'utf8'));
    assert.equal(metadata.createdAt, '2026-07-22T00:00:00.000Z');
    assert.equal(metadata.hostname, 'test-host');
    assert.equal(typeof metadata.pid, 'number');

    await lock.release();
    await assert.rejects(fs.stat(lockDir), { code: 'ENOENT' });
  });

  it('waits for a fresh lock and acquires after another process releases it', async () => {
    const tempDir = await makeTempDir();
    const lockDir = path.join(tempDir, 'figma-oauth.lock');
    const first = await acquireDirectoryLock(lockDir, {
      retryDelayMs: 5,
      timeoutMs: 500,
    });

    const secondPromise = acquireDirectoryLock(lockDir, {
      retryDelayMs: 5,
      timeoutMs: 500,
    });

    await new Promise((resolve) => setTimeout(resolve, 25));
    await first.release();
    const second = await secondPromise;

    assert.equal(second.lockDir, lockDir);
    await second.release();
  });

  it('returns figma_token_lock_stale for stale locks and does not delete them', async () => {
    const tempDir = await makeTempDir();
    const lockDir = path.join(tempDir, 'figma-oauth.lock');
    await fs.mkdir(lockDir, { recursive: true });
    await fs.writeFile(
      path.join(lockDir, 'lock.json'),
      JSON.stringify({
        pid: 123,
        hostname: 'old-host',
        createdAt: '2026-07-22T00:00:00.000Z',
      }),
    );

    await assert.rejects(
      acquireDirectoryLock(lockDir, {
        now: () => new Date('2026-07-22T00:11:00Z'),
        retryDelayMs: 1,
        timeoutMs: 10,
      }),
      (error) => {
        assert.equal(error.code, 'figma_token_lock_stale');
        return true;
      },
    );

    const stat = await fs.stat(lockDir);
    assert.equal(stat.isDirectory(), true);
  });
});
