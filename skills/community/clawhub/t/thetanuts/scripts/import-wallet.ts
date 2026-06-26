#!/usr/bin/env npx tsx
/**
 * Import an existing wallet using seed phrase.
 * Seed is read from WDK_SEED env var (or --seed-file) — never from argv.
 *
 * Usage: WDK_SEED="..." npx tsx import-wallet.ts --chain <evm|solana> [--index <n>]
 */

import WalletManagerEvm from '@tetherto/wdk-wallet-evm';
import WalletManagerSolana from '@tetherto/wdk-wallet-solana';
import { loadSeed } from './lib/load-seed';

const EVM_RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const SOLANA_RPC_URL = process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com';

interface ImportWalletParams {
  chain: 'evm' | 'solana';
  index: number;
}

function parseArgs(args: string[]): ImportWalletParams {
  const params: Partial<ImportWalletParams> = {
    index: 0,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--chain':
        const chain = args[++i]?.toLowerCase();
        if (chain === 'evm' || chain === 'solana') {
          params.chain = chain;
        }
        break;
      case '--index':
        params.index = parseInt(args[++i]) || 0;
        break;
    }
  }

  const missing: string[] = [];
  if (!params.chain) missing.push('--chain (evm|solana)');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing required parameters',
      missing,
      usage: 'WDK_SEED="..." npx tsx import-wallet.ts --chain <evm|solana> [--index <number>]',
      example: 'WDK_SEED="word1 word2 ... word12" npx tsx import-wallet.ts --chain evm',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  return {
    chain: params.chain!,
    index: params.index!,
  };
}

async function importEvmWallet(seedPhrase: string, index: number) {
  const wallet = new WalletManagerEvm(seedPhrase, {
    provider: EVM_RPC_URL,
  });

  try {
    const account = await wallet.getAccount(index);
    const address = await account.getAddress();
    const path = `m/44'/60'/0'/0/${index}`;

    return {
      address,
      derivationPath: path,
    };
  } finally {
    wallet.dispose?.();
  }
}

async function importSolanaWallet(seedPhrase: string, index: number) {
  const wallet = new WalletManagerSolana(seedPhrase, {
    rpcUrl: SOLANA_RPC_URL,
  });

  try {
    const account = await wallet.getAccount(index);
    const address = await account.getAddress();
    const path = `m/44'/501'/${index}'/0'`;

    return {
      address,
      derivationPath: path,
    };
  } finally {
    wallet.dispose?.();
  }
}

async function main() {
  const args = process.argv.slice(2);
  const { seed } = loadSeed(args);
  const params = parseArgs(args);

  try {
    let walletInfo;

    if (params.chain === 'evm') {
      walletInfo = await importEvmWallet(seed, params.index);
    } else {
      walletInfo = await importSolanaWallet(seed, params.index);
    }

    // NOTE: We do NOT include the seed phrase in the output for import
    const result = {
      wallet: {
        chain: params.chain,
        address: walletInfo.address,
        derivationPath: walletInfo.derivationPath,
        index: params.index,
      },
      network: params.chain === 'evm' ? {
        name: 'Base Mainnet',
        chainId: 8453,
        rpcUrl: EVM_RPC_URL,
      } : {
        name: 'Solana Mainnet',
        rpcUrl: SOLANA_RPC_URL,
      },
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      chain: params.chain,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
