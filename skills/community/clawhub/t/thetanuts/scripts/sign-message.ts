#!/usr/bin/env npx tsx
/**
 * Sign a message with wallet private key.
 * Seed is read from WDK_SEED env var (or --seed-file) — never from argv.
 *
 * Usage: WDK_SEED="..." npx tsx sign-message.ts --chain <evm|solana> --message "<message>" [--index <number>]
 */

import WalletManagerEvm from '@tetherto/wdk-wallet-evm';
import WalletManagerSolana from '@tetherto/wdk-wallet-solana';
import { loadSeed } from './lib/load-seed';

const EVM_RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const SOLANA_RPC_URL = process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com';

interface SignMessageParams {
  chain: 'evm' | 'solana';
  message: string;
  index: number;
}

function parseArgs(args: string[]): SignMessageParams {
  const params: Partial<SignMessageParams> = {
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
      case '--message':
        params.message = args[++i];
        break;
      case '--index':
        params.index = parseInt(args[++i]) || 0;
        break;
    }
  }

  const missing: string[] = [];
  if (!params.chain) missing.push('--chain (evm|solana)');
  if (!params.message) missing.push('--message "<message to sign>"');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing required parameters',
      missing,
      usage: 'WDK_SEED="..." npx tsx sign-message.ts --chain <evm|solana> --message "<message>" [--index <number>]',
      example: 'WDK_SEED="word1 word2 ... word12" npx tsx sign-message.ts --chain evm --message "Hello World"',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  return {
    chain: params.chain!,
    message: params.message!,
    index: params.index!,
  };
}

async function signEvmMessage(seedPhrase: string, index: number, message: string) {
  const wallet = new WalletManagerEvm(seedPhrase, {
    provider: EVM_RPC_URL,
  });

  try {
    const account = await wallet.getAccount(index);
    const address = await account.getAddress();
    const signature = await account.sign(message);

    return {
      address,
      signature,
    };
  } finally {
    wallet.dispose?.();
  }
}

async function signSolanaMessage(seedPhrase: string, index: number, message: string) {
  const wallet = new WalletManagerSolana(seedPhrase, {
    rpcUrl: SOLANA_RPC_URL,
  });

  try {
    const account = await wallet.getAccount(index);
    const address = await account.getAddress();
    const signature = await account.sign(message);

    return {
      address,
      signature,
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
    let signatureInfo;

    if (params.chain === 'evm') {
      signatureInfo = await signEvmMessage(seed, params.index, params.message);
    } else {
      signatureInfo = await signSolanaMessage(seed, params.index, params.message);
    }

    const result = {
      signature: {
        chain: params.chain,
        address: signatureInfo.address,
        message: params.message,
        signature: signatureInfo.signature,
      },
      warning: 'You have signed a message with your private key. This signature can be used to authenticate actions or approve operations. Only share this signature with trusted parties.',
      network: params.chain === 'evm' ? {
        name: 'Base Mainnet',
        chainId: 8453,
      } : {
        name: 'Solana Mainnet',
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
