import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

import { createStableError } from './redact.mjs';

const DEFAULT_STALE_MS = 10 * 60 * 1000;
const DEFAULT_RETRY_DELAY_MS = 100;
const DEFAULT_TIMEOUT_MS = 30 * 1000;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function readLockMetadata(lockDir) {
  try {
    const raw = await fs.readFile(path.join(lockDir, 'lock.json'), 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function isStale(metadata, now, staleMs) {
  if (!metadata?.createdAt) {
    return false;
  }
  const created = new Date(metadata.createdAt).getTime();
  if (!Number.isFinite(created)) {
    return false;
  }
  return now.getTime() - created > staleMs;
}

async function writeLockMetadata(lockDir, options) {
  const now = options.now();
  const metadata = {
    pid: typeof process.pid === 'number' ? process.pid : null,
    hostname: options.hostname(),
    createdAt: now.toISOString(),
  };
  await fs.writeFile(path.join(lockDir, 'lock.json'), JSON.stringify(metadata, null, 2), {
    mode: 0o600,
  });
}

export async function acquireDirectoryLock(lockDir, options = {}) {
  const resolvedOptions = {
    now: options.now ?? (() => new Date()),
    hostname: options.hostname ?? (() => os.hostname()),
    staleMs: options.staleMs ?? DEFAULT_STALE_MS,
    retryDelayMs: options.retryDelayMs ?? DEFAULT_RETRY_DELAY_MS,
    timeoutMs: options.timeoutMs ?? DEFAULT_TIMEOUT_MS,
  };
  const startedAt = resolvedOptions.now().getTime();

  while (true) {
    try {
      await fs.mkdir(lockDir, { mode: 0o700 });
      await writeLockMetadata(lockDir, resolvedOptions);
      let released = false;
      return {
        lockDir,
        async release() {
          if (released) {
            return;
          }
          released = true;
          await fs.rm(lockDir, { recursive: true, force: true });
        },
      };
    } catch (error) {
      if (error?.code !== 'EEXIST') {
        throw createStableError('figma_token_lock_failed', 'Could not acquire Figma token lock');
      }
    }

    const metadata = await readLockMetadata(lockDir);
    if (isStale(metadata, resolvedOptions.now(), resolvedOptions.staleMs)) {
      throw createStableError('figma_token_lock_stale', 'Figma token lock is stale; inspect and remove it manually');
    }

    if (resolvedOptions.now().getTime() - startedAt > resolvedOptions.timeoutMs) {
      throw createStableError('figma_token_lock_timeout', 'Timed out waiting for Figma token lock');
    }

    await sleep(resolvedOptions.retryDelayMs);
  }
}
