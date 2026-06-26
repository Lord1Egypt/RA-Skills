#!/usr/bin/env node
// AENS (æternity Name System) — register, lookup, and manage .chain names
// Names are on-chain usernames (e.g. "myagent.chain") pointed to a wallet address.
// Names shorter than 13 characters (excluding ".chain") go through an auction process.
import { AeSdk, Node, MemoryAccount, Name } from '@aeternity/aepp-sdk';

const NODE_URL = 'https://mainnet.aeternity.io';
const MIDDLEWARE_URL = 'https://mainnet.aeternity.io/mdw/v3';
const AE_AENS_DOMAIN = '.chain';
const AUCTION_LENGTH_THRESHOLD = 12; // names with <= 12 chars (before .chain) go to auction

function getAeSdk() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set. Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  const account = new MemoryAccount(privateKey);
  const node = new Node(NODE_URL);
  return new AeSdk({
    nodes: [{ name: 'mainnet', instance: node }],
    accounts: [account],
  });
}

function loadWallet() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set. Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  return { address: new MemoryAccount(privateKey).address };
}

function normalizeName(input) {
  const name = input.endsWith(AE_AENS_DOMAIN) ? input : input + AE_AENS_DOMAIN;
  return name.toLowerCase();
}

function getNameLength(name) {
  return name.replace(AE_AENS_DOMAIN, '').length;
}

function isAuctionName(name) {
  return getNameLength(name) <= AUCTION_LENGTH_THRESHOLD;
}

// ── Check if a name is available ──────────────────────────────────────────────
async function checkAvailability(rawName) {
  const name = normalizeName(rawName);
  const nameLen = getNameLength(name);
  const needsAuction = isAuctionName(name);

  // Query the middleware for name state
  const url = `${MIDDLEWARE_URL}/names/${encodeURIComponent(name)}`;
  const res = await fetch(url);

  if (res.status === 404) {
    console.log(JSON.stringify({
      name,
      available: true,
      length: nameLen,
      needs_auction: needsAuction,
      note: needsAuction
        ? `Name is ${nameLen} chars — requires auction. Choose a name with 13+ characters for instant registration.`
        : 'Name is available for immediate registration.',
    }));
    return;
  }

  const data = await res.json();
  const status = data.status || (data.info?.expireHeight ? 'active' : 'unknown');

  console.log(JSON.stringify({
    name,
    available: false,
    status,
    owner: data.info?.ownership?.current || data.owner || null,
    expires_at_height: data.info?.expireHeight || null,
    pointers: data.info?.pointers || [],
    length: nameLen,
    needs_auction: needsAuction,
  }));
}

// ── Register a name (preclaim → claim → update pointer) ──────────────────────
async function registerName(rawName) {
  const name = normalizeName(rawName);

  if (isAuctionName(name)) {
    console.error(`Error: "${name}" is ${getNameLength(name)} characters — names with 12 or fewer characters require an auction.`);
    console.error('Choose a name with 13+ characters for instant registration.');
    console.log(JSON.stringify({
      success: false,
      error: 'name_too_short_auction_required',
      name,
      length: getNameLength(name),
      suggestion: 'Use a name with 13 or more characters (before .chain) to skip the auction process.',
    }));
    process.exit(1);
  }

  const aeSdk = getAeSdk();
  const nameObj = new Name(name, aeSdk.getContext());

  // Check if already registered
  const isRegistered = await nameObj.getState().then(() => true, () => false);
  if (isRegistered) {
    const state = await nameObj.getState();
    console.log(JSON.stringify({
      success: false,
      error: 'name_already_registered',
      name,
      owner: state.owner,
    }));
    process.exit(1);
  }

  console.error(`Step 1/3: Preclaiming "${name}"...`);
  await nameObj.preclaim();

  console.error(`Step 2/3: Claiming "${name}"...`);
  const claimResult = await nameObj.claim();
  const claimTxHash = claimResult.hash;

  console.error('Waiting for claim transaction to be mined...');
  await aeSdk.poll(claimTxHash);

  // Point the name to our wallet address
  const walletData = loadWallet();
  console.error(`Step 3/3: Pointing "${name}" → ${walletData.address}...`);
  await nameObj.update({ account_pubkey: walletData.address });

  console.log(JSON.stringify({
    success: true,
    name,
    address: walletData.address,
    tx_hash: claimTxHash,
  }));
}

// ── Update name pointer to a different address ───────────────────────────────
async function updatePointer(rawName, address) {
  const name = normalizeName(rawName);
  const aeSdk = getAeSdk();
  const nameObj = new Name(name, aeSdk.getContext());

  // Default to own wallet address if none provided
  const walletData = loadWallet();
  const targetAddress = address || walletData.address;

  console.error(`Updating pointer: "${name}" → ${targetAddress}...`);
  await nameObj.update({ account_pubkey: targetAddress }, { extendPointers: true });

  console.log(JSON.stringify({
    success: true,
    name,
    pointed_to: targetAddress,
  }));
}

// ── Extend name TTL ──────────────────────────────────────────────────────────
async function extendName(rawName) {
  const name = normalizeName(rawName);
  const aeSdk = getAeSdk();
  const nameObj = new Name(name, aeSdk.getContext());

  console.error(`Extending TTL for "${name}"...`);
  await nameObj.extendTtl();

  console.log(JSON.stringify({
    success: true,
    name,
    action: 'extended',
  }));
}

// ── Look up name by wallet address ───────────────────────────────────────────
async function getNameByAddress(address) {
  // Default to own wallet if no address given
  const targetAddress = address || loadWallet().address;

  const url = `${MIDDLEWARE_URL}/names?owned_by=${targetAddress}&state=active&limit=100`;
  const res = await fetch(url);
  const data = await res.json();

  const names = (data.data || []).map((entry) => ({
    name: entry.name,
    expires_at_height: entry.info?.expireHeight || null,
    pointers: entry.info?.pointers || [],
    hash: entry.hash || null,
  }));

  console.log(JSON.stringify({
    address: targetAddress,
    count: names.length,
    names,
  }));
}

// ── Resolve a .chain name to its pointed address ─────────────────────────────
async function resolveName(rawName) {
  const name = normalizeName(rawName);
  const url = `${MIDDLEWARE_URL}/names/${encodeURIComponent(name)}`;
  const res = await fetch(url);

  if (res.status === 404) {
    console.log(JSON.stringify({
      name,
      resolved: false,
      error: 'name_not_found',
    }));
    process.exit(1);
  }

  const data = await res.json();
  const pointers = data.info?.pointers || [];
  const accountPointer = pointers.find((p) => p.key === 'account_pubkey');

  console.log(JSON.stringify({
    name,
    resolved: true,
    address: accountPointer?.id || null,
    owner: data.info?.ownership?.current || null,
    expires_at_height: data.info?.expireHeight || null,
    pointers,
  }));
}

// ── List own names ───────────────────────────────────────────────────────────
async function listOwnNames() {
  const walletData = loadWallet();
  await getNameByAddress(walletData.address);
}

// ── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  const command = process.argv[2] || 'help';
  const arg1 = process.argv[3];
  const arg2 = process.argv[4];

  switch (command) {
    case 'available':
      if (!arg1) {
        console.error('Usage: node scripts/superhero-name.mjs available <name>');
        process.exit(1);
      }
      await checkAvailability(arg1);
      break;

    case 'register':
      if (!arg1) {
        console.error('Usage: node scripts/superhero-name.mjs register <name>');
        process.exit(1);
      }
      await registerName(arg1);
      break;

    case 'update':
      if (!arg1) {
        console.error('Usage: node scripts/superhero-name.mjs update <name> [address]');
        process.exit(1);
      }
      await updatePointer(arg1, arg2);
      break;

    case 'extend':
      if (!arg1) {
        console.error('Usage: node scripts/superhero-name.mjs extend <name>');
        process.exit(1);
      }
      await extendName(arg1);
      break;

    case 'resolve':
      if (!arg1) {
        console.error('Usage: node scripts/superhero-name.mjs resolve <name>');
        process.exit(1);
      }
      await resolveName(arg1);
      break;

    case 'lookup':
      if (!arg1) {
        console.error('Usage: node scripts/superhero-name.mjs lookup <address>');
        process.exit(1);
      }
      await getNameByAddress(arg1);
      break;

    case 'list':
      await listOwnNames();
      break;

    case 'help':
    default:
      console.log(`
AENS Name Commands (.chain usernames):

  available <name>          Check if a .chain name is available
  register <name>           Register a name (preclaim → claim → point to wallet)
  update <name> [address]   Update name pointer (defaults to own wallet)
  extend <name>             Extend name TTL before it expires
  resolve <name>            Resolve a .chain name to its pointed address
  lookup <address>          Get all names owned by an address
  list                      List your own .chain names

Name Rules:
  - Names must end in ".chain" (auto-appended if omitted)
  - Names with 13+ characters → instant registration
  - Names with 12 or fewer characters → auction (not supported here)
  - Recommended: choose a name with 13+ chars for quick purchase

Examples:
  node scripts/superhero-name.mjs available myagentname
  node scripts/superhero-name.mjs register myagentname
  node scripts/superhero-name.mjs resolve myagentname.chain
  node scripts/superhero-name.mjs lookup ak_...
  node scripts/superhero-name.mjs list
  node scripts/superhero-name.mjs update myagentname.chain ak_...
  node scripts/superhero-name.mjs extend myagentname.chain

Note: Registration costs AE for gas + name fee. Use "available" first to check.
`);
  }
}

main().catch((e) => { console.error('ERROR:', e.message || e); process.exit(1); });
