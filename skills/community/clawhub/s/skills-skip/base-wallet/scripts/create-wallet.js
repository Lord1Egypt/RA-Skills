#!/usr/bin/env node
/**
 * Create Base Wallet
 * Usage: node create-wallet.js --env
 */

const { ethers } = require('ethers');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const mode = args[0]; // --env, --managed, --json

function createWallet() {
    const wallet = ethers.Wallet.createRandom();
    return wallet;
}

function outputEnv(wallet) {
    console.log('# === BASE WALLET (Environment Format) ===');
    console.log(`export WALLET_ADDRESS="${wallet.address}"`);
    console.log(`export PRIVATE_KEY="${wallet.privateKey}"`);
    console.log('# =========================================');
    console.log('# Mnemonic (BACKUP!):');
    console.log(`# ${wallet.mnemonic.phrase}`);
}

function outputManaged(wallet, name) {
    const dir = path.join(process.env.HOME, '.openclaw', 'wallets');
    fs.mkdirSync(dir, { recursive: true });
    
    const filepath = path.join(dir, `${name}.json`);
    fs.writeFileSync(filepath, JSON.stringify({
        address: wallet.address,
        privateKey: wallet.privateKey,
        mnemonic: wallet.mnemonic.phrase,
        created: new Date().toISOString()
    }, null, 2));
    
    fs.chmodSync(filepath, 0o600);
    console.log(`Wallet saved to: ${filepath}`);
}

function outputJson(wallet) {
    console.log(JSON.stringify({
        address: wallet.address,
        privateKey: wallet.privateKey,
        mnemonic: wallet.mnemonic.phrase
    }, null, 2));
}

// Main
const wallet = createWallet();

if (mode === '--env') {
    outputEnv(wallet);
} else if (mode === '--managed') {
    const name = process.argv[3] || 'wallet';
    outputManaged(wallet, name);
} else if (mode === '--json') {
    outputJson(wallet);
} else {
    console.log('Usage: node create-wallet.js [--env|--managed name|--json]');
    console.log('  --env      Output as environment variables (recommended)');
    console.log('  --managed  Save to file (opt-in)');
    console.log('  --json     Output as JSON');
}
