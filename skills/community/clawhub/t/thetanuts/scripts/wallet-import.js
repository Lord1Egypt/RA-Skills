#!/usr/bin/env node
/**
 * Import existing wallet from seed phrase
 * Usage: node wallet-import.js --seed-file /path/to/seed.txt
 *        printf '%s' "$WDK_SEED" | node wallet-import.js --stdin
 *
 * Validates and imports an existing BIP-39 seed phrase
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';
import { createInterface } from 'readline';

const WDK_MCP_DIR = join(homedir(), '.openclaw', 'wdk-mcp');
const ENV_FILE = join(WDK_MCP_DIR, '.env');

// Parse command line arguments
function parseArgs(args) {
  const params = {
    seedFile: null,
    stdin: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--seed-file':
        params.seedFile = args[++i];
        break;
      case '--stdin':
        params.stdin = true;
        break;
    }
  }

  return params;
}

// Read seed from stdin
async function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    const rl = createInterface({
      input: process.stdin,
      terminal: false,
    });

    rl.on('line', (line) => {
      data += line;
    });

    rl.on('close', () => {
      resolve(data.trim());
    });

    rl.on('error', reject);

    // Timeout after 5 seconds
    setTimeout(() => {
      rl.close();
      if (!data) {
        reject(new Error('Timeout reading from stdin'));
      }
    }, 5000);
  });
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

async function importWallet() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  // Validate arguments
  if (!params.seedFile && !params.stdin) {
    return {
      error: true,
      message: 'Missing required parameter',
      usage: [
        'node wallet-import.js --seed-file /path/to/seed.txt',
        'printf \'%s\' "$WDK_SEED" | node wallet-import.js --stdin',
      ],
      timestamp: new Date().toISOString(),
    };
  }

  // Read seed phrase
  let seedPhrase;

  if (params.seedFile) {
    if (!existsSync(params.seedFile)) {
      return {
        error: true,
        message: `Seed file not found: ${params.seedFile}`,
        timestamp: new Date().toISOString(),
      };
    }
    seedPhrase = readFileSync(params.seedFile, 'utf-8').trim();
  } else if (params.stdin) {
    try {
      seedPhrase = await readStdin();
    } catch (err) {
      return {
        error: true,
        message: `Failed to read from stdin: ${err.message}`,
        timestamp: new Date().toISOString(),
      };
    }
  }

  // Validate seed phrase
  if (!seedPhrase) {
    return {
      error: true,
      message: 'Empty seed phrase provided',
      timestamp: new Date().toISOString(),
    };
  }

  if (!validateMnemonic(seedPhrase, wordlist)) {
    return {
      error: true,
      message: 'Invalid seed phrase. Must be a valid BIP-39 mnemonic (12 or 24 words).',
      timestamp: new Date().toISOString(),
    };
  }

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
    imported: true,
    wallets,
    envFile: ENV_FILE,
    warning: 'Wallet imported successfully. Use a DEDICATED wallet for this integration.',
    timestamp: new Date().toISOString(),
  };
}

// Main
importWallet()
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
