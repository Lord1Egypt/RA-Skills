#!/usr/bin/env node
/**
 * Create a new wallet with fresh BIP-39 seed phrase
 * Usage: node wallet-create.js
 *
 * Generates a new seed phrase and configures the wallet runtime
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { generateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';

const WDK_MCP_DIR = join(homedir(), '.openclaw', 'wdk-mcp');
const ENV_FILE = join(WDK_MCP_DIR, '.env');

// Parse existing .env file
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

// Write .env file preserving comments and structure
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

  // Ensure directory exists
  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(filePath, content);
}

async function createWallet() {
  // Check if wallet already exists
  const existingEnv = parseEnv(ENV_FILE);
  if (existingEnv.WDK_SEED) {
    return {
      error: true,
      message: 'Wallet already exists. Use wallet-import.js to replace or manually delete WDK_SEED from .env.',
      envFile: ENV_FILE,
      timestamp: new Date().toISOString(),
    };
  }

  // Generate new seed phrase (128 bits = 12 words)
  const seedPhrase = generateMnemonic(wordlist, 128);

  // Write to .env
  writeEnv(ENV_FILE, {
    WDK_SEED: seedPhrase,
    WDK_ACTIVE_FAMILY: 'evm',
    WDK_ACTIVE_CHAIN: 'base-mainnet',
    WDK_ACTIVE_INDEX: '0',
  });

  // Import WDK modules and derive addresses
  const { default: WalletManagerEvm } = await import('@tetherto/wdk-wallet-evm');
  const { default: WalletManagerSolana } = await import('@tetherto/wdk-wallet-solana');

  const wallets = {};

  // Derive EVM address
  try {
    const evmWallet = new WalletManagerEvm(seedPhrase, {
      provider: 'https://mainnet.base.org',
    });
    const evmAccount = await evmWallet.getAccount(0);
    wallets.evm = {
      family: 'evm',
      address: await evmAccount.getAddress(),
      derivationPath: "m/44'/60'/0'/0/0",
    };
    evmWallet.dispose?.();
  } catch (err) {
    wallets.evm = { error: err.message };
  }

  // Derive Solana address
  try {
    const solWallet = new WalletManagerSolana(seedPhrase, {
      rpcUrl: 'https://api.mainnet-beta.solana.com',
    });
    const solAccount = await solWallet.getAccount(0);
    wallets.solana = {
      family: 'solana',
      address: await solAccount.getAddress(),
      derivationPath: "m/44'/501'/0'/0'",
    };
    solWallet.dispose?.();
  } catch (err) {
    wallets.solana = { error: err.message };
  }

  return {
    created: true,
    seedPhrase,
    wallets,
    envFile: ENV_FILE,
    warning: [
      '⚠️  SAVE THIS SEED PHRASE SECURELY!',
      '   - Write it down on paper and store in a safe place',
      '   - NEVER share this seed phrase with anyone',
      '   - NEVER enter this seed phrase on any website',
      '   - This seed phrase gives FULL ACCESS to your wallet',
      '',
      '⚠️  USE A DEDICATED WALLET!',
      '   - This should be a NEW wallet created specifically for this integration',
      '   - Do NOT reuse your primary, personal, or main wallet seed phrase',
    ].join('\n'),
    timestamp: new Date().toISOString(),
  };
}

// Main
createWallet()
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
