#!/usr/bin/env node
/**
 * Query wallet balance with chain-specific context
 * Usage: node wallet-balance.js --chain base-mainnet [--index 0] [--tokens 0x...]
 *
 * Outputs JSON with address, native balance, and token balances
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';

const WDK_MCP_DIR = join(homedir(), '.openclaw', 'wdk-mcp');
const ENV_FILE = join(WDK_MCP_DIR, '.env');

// Chain registry
const CHAINS = {
  'ethereum-mainnet': { family: 'evm', rpc: 'https://eth.llamarpc.com', chainId: 1, symbol: 'ETH', decimals: 18 },
  'base-mainnet': { family: 'evm', rpc: 'https://mainnet.base.org', chainId: 8453, symbol: 'ETH', decimals: 18 },
  'bnb-smart-chain': { family: 'evm', rpc: 'https://bsc-dataseed.binance.org', chainId: 56, symbol: 'BNB', decimals: 18 },
  'solana-mainnet': { family: 'solana', rpc: 'https://api.mainnet-beta.solana.com', symbol: 'SOL', decimals: 9 },
};

// Known tokens
const KNOWN_TOKENS = {
  // Base Mainnet
  '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913': { symbol: 'USDC', decimals: 6, chains: ['base-mainnet'] },
  '0x4200000000000000000000000000000000000006': { symbol: 'WETH', decimals: 18, chains: ['base-mainnet'] },
  '0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf': { symbol: 'cbBTC', decimals: 8, chains: ['base-mainnet'] },
  // Ethereum Mainnet
  '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': { symbol: 'USDC', decimals: 6, chains: ['ethereum-mainnet'] },
  '0xdAC17F958D2ee523a2206206994597C13D831ec7': { symbol: 'USDT', decimals: 6, chains: ['ethereum-mainnet'] },
};

// Parse command line arguments
function parseArgs(args) {
  const params = {
    chain: null,
    index: 0,
    tokens: [],
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--chain':
        params.chain = args[++i]?.toLowerCase();
        break;
      case '--index':
        params.index = parseInt(args[++i]) || 0;
        break;
      case '--tokens':
        params.tokens = args[++i]?.split(',').map(t => t.trim()) || [];
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

// Format balance
function formatBalance(balanceWei, decimals) {
  const divisor = BigInt(10 ** decimals);
  const integerPart = balanceWei / divisor;
  const fractionalPart = balanceWei % divisor;

  const fractionalStr = fractionalPart.toString().padStart(decimals, '0');
  let trimmed = fractionalStr.replace(/0+$/, '');
  if (trimmed.length < 2) trimmed = fractionalStr.slice(0, Math.max(2, trimmed.length));

  return `${integerPart}.${trimmed || '00'}`;
}

async function queryBalance() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  // Show help if no chain
  if (!params.chain) {
    return {
      error: true,
      message: 'Missing required parameter: --chain',
      usage: 'node wallet-balance.js --chain <chain-slug> [--index <number>] [--tokens <address,address,...>]',
      example: 'node wallet-balance.js --chain base-mainnet --tokens 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
      supportedChains: Object.keys(CHAINS),
      timestamp: new Date().toISOString(),
    };
  }

  // Validate chain
  if (!CHAINS[params.chain]) {
    return {
      error: true,
      message: `Unknown chain: ${params.chain}`,
      supportedChains: Object.keys(CHAINS),
      timestamp: new Date().toISOString(),
    };
  }

  const chainInfo = CHAINS[params.chain];

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

  let address;
  let nativeBalance;
  const tokenBalances = [];

  if (chainInfo.family === 'evm') {
    const { default: WalletManagerEvm } = await import('@tetherto/wdk-wallet-evm');

    // Use custom RPC if set in env
    const rpcUrl = env.EVM_RPC_URL || chainInfo.rpc;

    const wallet = new WalletManagerEvm(env.WDK_SEED, {
      provider: rpcUrl,
    });

    try {
      const account = await wallet.getAccount(params.index);
      address = await account.getAddress();

      // Get native balance
      const balanceWei = await account.getBalance();
      nativeBalance = {
        symbol: chainInfo.symbol,
        balance: formatBalance(balanceWei, chainInfo.decimals),
        balanceWei: balanceWei.toString(),
        decimals: chainInfo.decimals,
      };

      // Get token balances
      for (const tokenAddress of params.tokens) {
        try {
          const tokenInfo = KNOWN_TOKENS[tokenAddress] || { symbol: 'UNKNOWN', decimals: 18 };
          const tokenBalanceRaw = await account.getTokenBalance(tokenAddress);

          tokenBalances.push({
            address: tokenAddress,
            symbol: tokenInfo.symbol,
            balance: formatBalance(tokenBalanceRaw, tokenInfo.decimals),
            balanceRaw: tokenBalanceRaw.toString(),
            decimals: tokenInfo.decimals,
          });
        } catch (err) {
          tokenBalances.push({
            address: tokenAddress,
            error: err.message,
          });
        }
      }
    } finally {
      wallet.dispose?.();
    }
  } else if (chainInfo.family === 'solana') {
    const { default: WalletManagerSolana } = await import('@tetherto/wdk-wallet-solana');

    const rpcUrl = env.SOLANA_RPC_URL || chainInfo.rpc;

    const wallet = new WalletManagerSolana(env.WDK_SEED, {
      rpcUrl,
    });

    try {
      const account = await wallet.getAccount(params.index);
      address = await account.getAddress();

      // Get native balance (lamports)
      const balanceLamports = await account.getBalance();
      nativeBalance = {
        symbol: chainInfo.symbol,
        balance: formatBalance(balanceLamports, chainInfo.decimals),
        balanceLamports: balanceLamports.toString(),
        decimals: chainInfo.decimals,
      };

      // Get SPL token balances
      for (const tokenAddress of params.tokens) {
        try {
          const tokenBalanceRaw = await account.getTokenBalance(tokenAddress);
          tokenBalances.push({
            address: tokenAddress,
            balance: formatBalance(tokenBalanceRaw, 9),
            balanceRaw: tokenBalanceRaw.toString(),
            decimals: 9,
          });
        } catch (err) {
          tokenBalances.push({
            address: tokenAddress,
            error: 'Token account not found',
          });
        }
      }
    } finally {
      wallet.dispose?.();
    }
  }

  const result = {
    chain: params.chain,
    chainId: chainInfo.chainId,
    index: params.index,
    address,
    native: nativeBalance,
  };

  if (tokenBalances.length > 0) {
    result.tokens = tokenBalances;
  }

  result.timestamp = new Date().toISOString();

  return result;
}

// Main
queryBalance()
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
