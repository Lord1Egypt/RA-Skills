import { homedir } from 'node:os';
import { join } from 'node:path';

import { DEFAULTS, MAINNET } from './addresses.mjs';
import { POLICY } from './policy.mjs';

function expandHome(path) {
  if (path.startsWith('~/')) return join(homedir(), path.slice(2));
  if (path === '~') return homedir();
  return path;
}

export function loadConfig() {
  const privateKey = (process.env.URUFU_PRIVATE_KEY || process.env.PRIVATE_KEY || '').trim();
  const wallet = (process.env.URUFU_WALLET || '').trim();

  return {
    chainId: Number(process.env.URUFU_CHAIN_ID || MAINNET.chainId),
    wallet,
    privateKey: privateKey.startsWith('0x') ? privateKey : privateKey ? `0x${privateKey}` : '',
    rpcUrl: (process.env.URUFU_RPC_URL || '').trim(),
    siteUrl: (process.env.URUFU_SITE_URL || DEFAULTS.siteUrl).replace(/\/$/, ''),
    indexerUrl: (process.env.URUFU_INDEXER || DEFAULTS.indexerUrl).replace(/\/$/, ''),
    vault: process.env.URUFU_VAULT || MAINNET.vault,
    minter: process.env.URUFU_MINTER || MAINNET.minter,
    uru: process.env.URUFU_URU || MAINNET.uru,
    statePath: expandHome(process.env.URUFU_AGENT_STATE || '~/.urufu-agent/state.json'),
    claimMinIntervalMs: Number(process.env.URUFU_CLAIM_INTERVAL_MS || POLICY.claimMinIntervalMs),
    mintMinIntervalMs: Number(process.env.URUFU_MINT_INTERVAL_MS || POLICY.mintMinIntervalMs),
    maxBatchSize: Number(process.env.URUFU_CLAIM_MAX_BATCH || POLICY.maxTokenIdsPerBatch),
    claimIntentTtlSeconds: 5 * 60,
    mintIntentTtlSeconds: 15 * 60,
  };
}

export function requireWallet(config) {
  if (!config.wallet) {
    throw new Error('URUFU_WALLET is required');
  }
  return config.wallet;
}

export function requireSigner(config) {
  if (!config.privateKey) {
    throw new Error('URUFU_PRIVATE_KEY is required for signing');
  }
  return config.privateKey;
}

export function requireRpc(config) {
  if (!config.rpcUrl) {
    throw new Error(
      'URUFU_RPC_URL is required. Use your own Base RPC (Alchemy, QuickNode, Infura, etc.) — urufu does not provide RPC for agents.',
    );
  }
  return config.rpcUrl;
}
