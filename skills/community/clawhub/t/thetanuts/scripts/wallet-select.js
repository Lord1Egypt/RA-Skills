#!/usr/bin/env node
/**
 * Select active wallet context (family, chain, index)
 * Usage: node wallet-select.js --family evm --chain base-mainnet --index 0
 *
 * Sets the active wallet context for subsequent operations
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';

const WDK_MCP_DIR = join(homedir(), '.openclaw', 'wdk-mcp');
const ENV_FILE = join(WDK_MCP_DIR, '.env');

// Chain registry
const CHAINS = {
  'ethereum-mainnet': { family: 'evm', rpc: 'https://eth.llamarpc.com', chainId: 1, symbol: 'ETH' },
  'base-mainnet': { family: 'evm', rpc: 'https://mainnet.base.org', chainId: 8453, symbol: 'ETH' },
  'bnb-smart-chain': { family: 'evm', rpc: 'https://bsc-dataseed.binance.org', chainId: 56, symbol: 'BNB' },
  'solana-mainnet': { family: 'solana', rpc: 'https://api.mainnet-beta.solana.com', symbol: 'SOL' },
};

// Parse command line arguments
function parseArgs(args) {
  const params = {
    family: null,
    chain: null,
    index: 0,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--family':
        params.family = args[++i]?.toLowerCase();
        break;
      case '--chain':
        params.chain = args[++i]?.toLowerCase();
        break;
      case '--index':
        params.index = parseInt(args[++i]) || 0;
        break;
    }
  }

  return params;
}

// Parse .env file
function parseEnv(filePath) {
  if (!existsSync(filePath)) return {};

  const content = readFileSync(filePath, 'utf-8');
  const env = {};

  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    const match = trimmed.match(/^([^=]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      let value = match[2].trim();
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      env[key] = value;
    }
  }

  return env;
}

// Write .env file
function writeEnv(filePath, updates) {
  let content = '';

  if (existsSync(filePath)) {
    content = readFileSync(filePath, 'utf-8');
  }

  for (const [key, value] of Object.entries(updates)) {
    const regex = new RegExp(`^(#\\s*)?${key}=.*$`, 'm');
    const newLine = `${key}=${value}`;

    if (regex.test(content)) {
      content = content.replace(regex, newLine);
    } else {
      content = content.trimEnd() + '\n' + newLine + '\n';
    }
  }

  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(filePath, content);
}

async function selectWallet() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  // Show help if no arguments
  if (!params.family && !params.chain) {
    return {
      error: true,
      message: 'Missing required parameters',
      usage: 'node wallet-select.js --family <evm|solana> --chain <chain-slug> [--index <number>]',
      example: 'node wallet-select.js --family evm --chain base-mainnet --index 0',
      supportedChains: Object.keys(CHAINS).reduce((acc, key) => {
        acc[key] = CHAINS[key].family;
        return acc;
      }, {}),
      timestamp: new Date().toISOString(),
    };
  }

  // Validate family
  if (params.family && !['evm', 'solana'].includes(params.family)) {
    return {
      error: true,
      message: `Invalid family: ${params.family}. Must be 'evm' or 'solana'.`,
      timestamp: new Date().toISOString(),
    };
  }

  // Validate chain
  if (params.chain && !CHAINS[params.chain]) {
    return {
      error: true,
      message: `Unknown chain: ${params.chain}`,
      supportedChains: Object.keys(CHAINS),
      timestamp: new Date().toISOString(),
    };
  }

  // Validate chain matches family
  if (params.family && params.chain) {
    const chainInfo = CHAINS[params.chain];
    if (chainInfo.family !== params.family) {
      return {
        error: true,
        message: `Chain ${params.chain} is ${chainInfo.family}, not ${params.family}`,
        timestamp: new Date().toISOString(),
      };
    }
  }

  // Infer family from chain if not provided
  if (!params.family && params.chain) {
    params.family = CHAINS[params.chain].family;
  }

  // Check if wallet is configured
  const env = parseEnv(ENV_FILE);
  if (!env.WDK_SEED) {
    return {
      error: true,
      message: 'No wallet configured. Run wallet-create.js or wallet-import.js first.',
      timestamp: new Date().toISOString(),
    };
  }

  // Validate seed
  if (!validateMnemonic(env.WDK_SEED, wordlist)) {
    return {
      error: true,
      message: 'Invalid WDK_SEED in .env.',
      timestamp: new Date().toISOString(),
    };
  }

  // Write new context to .env
  writeEnv(ENV_FILE, {
    WDK_ACTIVE_FAMILY: params.family,
    WDK_ACTIVE_CHAIN: params.chain || (params.family === 'evm' ? 'base-mainnet' : 'solana-mainnet'),
    WDK_ACTIVE_INDEX: params.index.toString(),
  });

  // Derive address for selected context
  const selectedChain = params.chain || (params.family === 'evm' ? 'base-mainnet' : 'solana-mainnet');
  const chainInfo = CHAINS[selectedChain];
  let address;

  if (params.family === 'evm') {
    const { default: WalletManagerEvm } = await import('@tetherto/wdk-wallet-evm');
    const wallet = new WalletManagerEvm(env.WDK_SEED, {
      provider: chainInfo.rpc,
    });
    const account = await wallet.getAccount(params.index);
    address = await account.getAddress();
    wallet.dispose?.();
  } else {
    const { default: WalletManagerSolana } = await import('@tetherto/wdk-wallet-solana');
    const wallet = new WalletManagerSolana(env.WDK_SEED, {
      rpcUrl: chainInfo.rpc,
    });
    const account = await wallet.getAccount(params.index);
    address = await account.getAddress();
    wallet.dispose?.();
  }

  return {
    selected: true,
    context: {
      family: params.family,
      chain: selectedChain,
      chainId: chainInfo.chainId,
      symbol: chainInfo.symbol,
      index: params.index,
      address,
    },
    envFile: ENV_FILE,
    timestamp: new Date().toISOString(),
  };
}

// Main
selectWallet()
  .then(result => {
    console.log(JSON.stringify(result, null, 2));
    if (result.error) process.exit(1);
  })
  .catch(err => {
    console.error(JSON.stringify({
      error: true,
      message: err.message,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  });
