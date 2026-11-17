#!/usr/bin/env node
// update-page.mjs — update a Stacktree page the wallet paid for, without paying again.
//
// The wallet that paid the x402 publish is the page's update credential:
// a single-use challenge signed with personal_sign (EIP-191). No transaction,
// no fees, nothing on-chain — the signature only proves you hold the wallet.
//   1. POST {api}/wallet-auth/challenge { wallet }   -> { challenge, message }
//   2. personal_sign the exact `message` text
//   3. PUT {api}/sites/{id} with {"html": "..."} and Authorization: Wallet ...
//
// Usage:
//   node update-page.mjs --site <id-or-token> --file <new.html>
// Options:
//   --key-file <path>  wallet to sign with; default ~/.agentcash/wallet.json
//   --api <base>       default https://api.stacktr.ee
//
// The key is read from disk here, on purpose. Never pass it on the command
// line and never read it into your own context: it is a funded wallet AND the
// standing update credential for every page it paid for, so anything that
// logs your transcript ends up holding both.
//
// Setup once, in this scripts directory: npm install   (pulls `viem`)
import { readFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { privateKeyToAccount } from 'viem/accounts';

const arg = (name, fallback) => {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
};
const site = arg('site');
const file = arg('file');
const api = arg('api', 'https://api.stacktr.ee').replace(/\/+$/, '');
const keyFile = arg('key-file', join(homedir(), '.agentcash', 'wallet.json'));
if (!site || !file) {
  console.error('usage: node update-page.mjs --site <id-or-token> --file <new.html> [--key-file ~/.agentcash/wallet.json] [--api https://api.stacktr.ee]');
  process.exit(2);
}

// Env var still works for wallets that live somewhere else entirely, but the
// file is the default so the common path never puts a key in a command.
let pk = process.env.WALLET_PRIVATE_KEY;
if (!pk) {
  try {
    const raw = await readFile(keyFile, 'utf8');
    pk = keyFile.endsWith('.json') ? JSON.parse(raw).privateKey : raw.trim();
  } catch {
    console.error(`no wallet key: ${keyFile} is unreadable. Pass --key-file, or set WALLET_PRIVATE_KEY in the environment (not on the command line).`);
    process.exit(2);
  }
}
if (!pk) {
  console.error(`no privateKey field in ${keyFile}`);
  process.exit(2);
}

const account = privateKeyToAccount(pk.startsWith('0x') ? pk : `0x${pk}`);

const challengeRes = await fetch(`${api}/wallet-auth/challenge`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ wallet: account.address }),
});
const challenge = await challengeRes.json();
if (!challengeRes.ok) {
  // 404 unknown_wallet: this wallet never paid for a page here. 403: blocked.
  console.error(JSON.stringify(challenge, null, 2));
  process.exit(1);
}

// Sign the server's exact `message` text — it embeds the challenge id, and the
// server verifies against that exact string. Never reconstruct it locally.
const sig = await account.signMessage({ message: challenge.message });

// JSON, not multipart: PUT takes the same body shape POST /publish takes, so a
// revision is the same document at a different verb. (Multipart still works and
// is the only shape that carries a zip, a PDF, or e2e ciphertext.)
const putRes = await fetch(`${api}/sites/${encodeURIComponent(site)}`, {
  method: 'PUT',
  headers: {
    authorization: `Wallet challenge=${challenge.challenge},sig=${sig}`,
    'content-type': 'application/json',
  },
  body: JSON.stringify({ html: await readFile(file, 'utf8') }),
});
const out = await putRes.json();
console.log(JSON.stringify(out, null, 2));
process.exit(putRes.ok ? 0 : 1);
