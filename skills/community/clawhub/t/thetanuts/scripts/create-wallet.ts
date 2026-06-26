#!/usr/bin/env npx tsx
/**
 * Create a new wallet using WDK
 * Usage: npx tsx create-wallet.ts --chain <evm|solana> [--index <number>]
 *
 * Example:
 *   npx tsx create-wallet.ts --chain evm
 *   npx tsx create-wallet.ts --chain solana --index 0
 */

import { generateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';
import WalletManagerEvm from '@tetherto/wdk-wallet-evm';
import WalletManagerSolana from '@tetherto/wdk-wallet-solana';

const EVM_RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const SOLANA_RPC_URL = process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com';

interface CreateWalletParams {
  chain: 'evm' | 'solana';
  index: number;
}

function parseArgs(args: string[]): CreateWalletParams {
  const params: Partial<CreateWalletParams> = {
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

  if (!params.chain) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing required parameter: --chain',
      usage: 'npx tsx create-wallet.ts --chain <evm|solana> [--index <number>]',
      example: 'npx tsx create-wallet.ts --chain evm',
      supportedChains: ['evm', 'solana'],
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  return params as CreateWalletParams;
}

async function createEvmWallet(seedPhrase: string, index: number) {
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

async function createSolanaWallet(seedPhrase: string, index: number) {
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
  const params = parseArgs(args);

  // Generate new BIP-39 mnemonic (12 words)
  const seedPhrase = generateMnemonic(wordlist);

  try {
    let walletInfo;

    if (params.chain === 'evm') {
      walletInfo = await createEvmWallet(seedPhrase, params.index);
    } else {
      walletInfo = await createSolanaWallet(seedPhrase, params.index);
    }

    const result = {
      wallet: {
        chain: params.chain,
        address: walletInfo.address,
        seedPhrase: seedPhrase,
        derivationPath: walletInfo.derivationPath,
        index: params.index,
      },
      security: {
        warning: 'SAVE YOUR SEED PHRASE SECURELY. Anyone with this phrase can access your funds.',
        instructions: [
          'Write it down on paper and store in a secure location',
          'Never share your seed phrase with anyone',
          'Never enter your seed phrase on websites or apps you do not trust',
          'Consider using a hardware wallet for large amounts',
        ],
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
