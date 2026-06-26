#!/usr/bin/env node
// Wallet management for superhero.com / æternity blockchain
// Generate new wallet, check balance, export address
import { AeSdk, Node, MemoryAccount } from '@aeternity/aepp-sdk';

const NODE_URL = 'https://mainnet.aeternity.io';

function loadAccount() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set.');
    console.error('Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  return new MemoryAccount(privateKey);
}

function generateWallet() {
  const account = MemoryAccount.generate();
  console.log(JSON.stringify({
    success: true,
    address: account.address,
    AE_PRIVATE_KEY: account.secretKey,
    next_step: `export AE_PRIVATE_KEY=${account.secretKey}`,
    warning: 'Save this private key securely. Back it up offline. Never commit it to git.',
  }));
}

async function getBalance() {
  const account = loadAccount();
  const node = new Node(NODE_URL);
  const sdk = new AeSdk({
    nodes: [{ name: 'mainnet', instance: node }],
  });
  try {
    const balanceAettos = await sdk.getBalance(account.address);
    const balanceAE = parseInt(balanceAettos) / 1e18;
    console.log(JSON.stringify({
      address: account.address,
      balance_ae: balanceAE,
      balance_aettos: balanceAettos,
    }));
  } catch (e) {
    console.log(JSON.stringify({ address: account.address, balance_ae: 0, balance_aettos: '0' }));
  }
}

function showAddress() {
  const account = loadAccount();
  console.log(JSON.stringify({ address: account.address }));
}

function importWallet(secretKey) {
  if (!secretKey) {
    console.error('Usage: node scripts/superhero-wallet.mjs import <secretKey>');
    process.exit(1);
  }
  const account = new MemoryAccount(secretKey);
  console.log(JSON.stringify({
    success: true,
    address: account.address,
    next_step: `export AE_PRIVATE_KEY=${secretKey}`,
    warning: 'Save this private key securely. Back it up offline. Never commit it to git.',
  }));
}

async function main() {
  const command = process.argv[2] || 'help';
  const arg = process.argv[3];

  switch (command) {
    case 'generate':
      generateWallet();
      break;
    case 'balance':
      await getBalance();
      break;
    case 'address':
      showAddress();
      break;
    case 'import':
      importWallet(arg);
      break;
    case 'exists':
      console.log(JSON.stringify({ exists: !!process.env.AE_PRIVATE_KEY }));
      break;
    case 'help':
    default:
      console.log(`
Wallet Commands:
  generate              Create a new wallet keypair (outputs key once — save it)
  import <secretKey>    Show setup instructions for an existing secret key
  balance               Check wallet AE balance  (requires AE_PRIVATE_KEY env var)
  address               Show wallet address      (requires AE_PRIVATE_KEY env var)
  exists                Check if AE_PRIVATE_KEY env var is set

Environment:
  export AE_PRIVATE_KEY=<your_secret_key>
`);
  }
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });
