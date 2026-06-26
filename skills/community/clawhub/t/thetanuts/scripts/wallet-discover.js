#!/usr/bin/env node
/**
 * Discover configured wallet and derive addresses
 * Usage: node wallet-discover.js
 *
 * Outputs JSON with wallet configuration status and addresses
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';

// Dynamic imports for WDK (ESM)
const WDK_MCP_DIR = join(homedir(), '.openclaw', 'wdk-mcp');
const ENV_FILE = join(WDK_MCP_DIR, '.env');

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
      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      env[key] = value;
    }
  }

  return env;
}

async function discoverWallet() {
  // Check if .env exists
  if (!existsSync(ENV_FILE)) {
    return {
      configured: false,
      message: 'No wallet configured. Run wallet-create.js or wallet-import.js first.',
      envFile: ENV_FILE,
      timestamp: new Date().toISOString(),
    };
  }

  // Parse environment
  const env = parseEnv(ENV_FILE);
  const seed = env.WDK_SEED;

  if (!seed) {
    return {
      configured: false,
      message: 'WDK_SEED not set in .env. Run wallet-create.js or wallet-import.js.',
      envFile: ENV_FILE,
      timestamp: new Date().toISOString(),
    };
  }

  // Validate seed
  if (!validateMnemonic(seed, wordlist)) {
    return {
      configured: false,
      error: 'Invalid WDK_SEED in .env. Must be a valid BIP-39 mnemonic.',
      envFile: ENV_FILE,
      timestamp: new Date().toISOString(),
    };
  }

  // Import WDK modules dynamically
  const { default: WalletManagerEvm } = await import('@tetherto/wdk-wallet-evm');
  const { default: WalletManagerSolana } = await import('@tetherto/wdk-wallet-solana');

  const wallets = {};

  // Derive EVM address
  try {
    const evmWallet = new WalletManagerEvm(seed, {
      provider: env.EVM_RPC_URL || 'https://mainnet.base.org',
    });
    const evmAccount = await evmWallet.getAccount(0);
    const evmAddress = await evmAccount.getAddress();

    wallets.evm = {
      family: 'evm',
      address: evmAddress,
      derivationPath: "m/44'/60'/0'/0/0",
    };

    evmWallet.dispose?.();
  } catch (err) {
    wallets.evm = { error: err.message };
  }

  // Derive Solana address
  try {
    const solWallet = new WalletManagerSolana(seed, {
      rpcUrl: env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
    });
    const solAccount = await solWallet.getAccount(0);
    const solAddress = await solAccount.getAddress();

    wallets.solana = {
      family: 'solana',
      address: solAddress,
      derivationPath: "m/44'/501'/0'/0'",
    };

    solWallet.dispose?.();
  } catch (err) {
    wallets.solana = { error: err.message };
  }

  // Get active context
  const activeContext = {
    family: env.WDK_ACTIVE_FAMILY || 'evm',
    chain: env.WDK_ACTIVE_CHAIN || 'base-mainnet',
    index: parseInt(env.WDK_ACTIVE_INDEX || '0'),
  };

  return {
    configured: true,
    wallets,
    activeContext,
    envFile: ENV_FILE,
    timestamp: new Date().toISOString(),
  };
}

// Main
discoverWallet()
  .then(result => {
    console.log(JSON.stringify(result, null, 2));
  })
  .catch(err => {
    console.error(JSON.stringify({
      error: true,
      message: err.message,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  });
