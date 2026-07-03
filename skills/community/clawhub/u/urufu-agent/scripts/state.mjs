import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';

const EMPTY = {
  lastClaimAtMs: 0,
  lastMintAtMs: 0,
  lastSwapAtMs: 0,
  lastStatsAtMs: 0,
  lastClaimTxHash: null,
  lastMintTxHash: null,
  consecutiveErrors: 0,
};

export async function loadState(path) {
  try {
    const raw = await readFile(path, 'utf8');
    return { ...EMPTY, ...JSON.parse(raw) };
  } catch (error) {
    if (error && typeof error === 'object' && error.code === 'ENOENT') {
      return { ...EMPTY };
    }
    throw error;
  }
}

export async function saveState(path, state) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, `${JSON.stringify(state, null, 2)}\n`, 'utf8');
}
