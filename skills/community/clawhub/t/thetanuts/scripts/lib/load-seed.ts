/**
 * Secure seed loader.
 *
 * Seeds are loaded from WDK_SEED (env var) or a --seed-file path.
 * The phrase-on-argv variant is rejected because argv is visible to other
 * processes (ps, top, shell history, agent logs).
 */

import { readFileSync } from 'fs';
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';

export interface LoadedSeed {
  seed: string;
  source: 'env' | 'file';
}

function fail(message: string, extra: Record<string, unknown> = {}): never {
  console.error(JSON.stringify({
    error: true,
    message,
    ...extra,
    timestamp: new Date().toISOString(),
  }, null, 2));
  process.exit(1);
}

export function loadSeed(args: string[]): LoadedSeed {
  // Hard-reject the phrase-on-argv variant. argv contents leak via ps,
  // shell history, and agent logs, so a seed flag on the command line is
  // categorically unsafe even if "private" from the user's perspective.
  if (args.includes('--seed')) {
    fail(
      'Passing --seed on the command line is not allowed. Seed phrases on argv leak via ps, shell history, and agent logs. Set the WDK_SEED environment variable (e.g., from .env) or pass --seed-file <path> instead.',
      {
        howToFix: [
          'Option 1 (preferred): export WDK_SEED="word1 word2 ... word12" then re-run',
          'Option 2: write the seed to a chmod 600 file and pass --seed-file <path>',
        ],
      },
    );
  }

  let raw: string | undefined;
  let source: 'env' | 'file' | undefined;

  const fileIdx = args.indexOf('--seed-file');
  if (fileIdx !== -1) {
    const path = args[fileIdx + 1];
    if (!path) fail('--seed-file requires a path argument');
    try {
      raw = readFileSync(path, 'utf8');
      source = 'file';
    } catch (e) {
      fail(`Could not read seed file at ${path}: ${(e as Error).message}`);
    }
  } else if (process.env.WDK_SEED) {
    raw = process.env.WDK_SEED;
    source = 'env';
  } else {
    fail(
      'No seed available. Set WDK_SEED in the environment (or in .env) before running this script.',
      {
        howToFix: 'echo \'WDK_SEED="word1 word2 ... word12"\' >> .env  (then re-run)',
      },
    );
  }

  const seed = raw!.trim().replace(/\s+/g, ' ');
  if (!validateMnemonic(seed, wordlist)) {
    fail('Loaded seed is not a valid BIP-39 mnemonic (12 or 24 words).');
  }

  return { seed, source: source! };
}
