#!/usr/bin/env node
/**
 * TokenMail JS CLI (ethers) - Python crypto依赖不可用时的替代方案
 *
 * 依赖:
 *   npm i ethers
 *
 * 示例:
 *   node scripts/tokenmail_cli_js.mjs addr --mnemonic "..."
 *   node scripts/tokenmail_cli_js.mjs send --mnemonic "..." --to "will.1@foxmail.com" --subject "Hello" --body "Hi" --api-url "https://tokenforge.fit/api"
 *   node scripts/tokenmail_cli_js.mjs inbox --mnemonic "..." --limit 10 --api-url "https://tokenforge.fit/api"
 */

import crypto from 'node:crypto';
import { Wallet, SigningKey } from 'ethers';

const DEFAULT_API_URL = process.env.TOKENMAIL_API_URL || 'https://tokenforge.fit/api';

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const args = { _: [] };
  for (let i = 0; i < rest.length; i++) {
    const token = rest[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = rest[i + 1];
      if (!next || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    } else {
      args._.push(token);
    }
  }
  return { command, args };
}

function requireArg(args, key) {
  const v = args[key];
  if (v === undefined || v === null || v === '') {
    throw new Error(`Missing required argument --${key}`);
  }
  return String(v);
}

function normalizeBaseUrl(url) {
  return String(url || DEFAULT_API_URL).replace(/\/+$/, '') + '/';
}

function canonicalize(value) {
  if (value === null || typeof value !== 'object') return value;
  if (Array.isArray(value)) return value.map(canonicalize);
  const out = {};
  for (const k of Object.keys(value).sort()) {
    out[k] = canonicalize(value[k]);
  }
  return out;
}

function stableStringify(obj) {
  return JSON.stringify(canonicalize(obj));
}

function toBase64Utf8(str) {
  return Buffer.from(str, 'utf8').toString('base64');
}

function sha256HexBytes(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}

function sha256HexString(s) {
  return crypto.createHash('sha256').update(s, 'utf8').digest('hex');
}

function startsWithZeros(hex, difficulty) {
  return hex.startsWith('0'.repeat(Number(difficulty)));
}

async function getJson(url, init = {}) {
  const res = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init.headers || {}),
    },
  });
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}: ${typeof data === 'string' ? data : JSON.stringify(data)}`);
  }
  return data;
}

async function signMessage(wallet, messageObj) {
  const canonical = stableStringify(messageObj);
  return wallet.signMessage(canonical);
}

async function getConfig(baseUrl) {
  return getJson(`${baseUrl}config`);
}

async function resolveRecipientForPow(baseUrl, to) {
  if (to.startsWith('0x') || to.includes('@')) return to;
  const resolved = await getJson(`${baseUrl}resolve/${encodeURIComponent(to)}`);
  return resolved.address;
}

function calcNonce({ from, toPow, timestamp, payloadHash, difficulty }) {
  let nonce = 0;
  while (true) {
    const data = `${from}:${toPow}:${timestamp}:${nonce}:${payloadHash}`;
    const h = sha256HexString(data);
    if (startsWithZeros(h, difficulty)) return String(nonce);
    nonce += 1;
  }
}

function buildWalletFromMnemonic(mnemonic) {
  return Wallet.fromPhrase(mnemonic.trim());
}

function getPublicKeyFromWallet(wallet) {
  return SigningKey.computePublicKey(wallet.privateKey, false);
}

async function cmdAddr(args) {
  const mnemonic = requireArg(args, 'mnemonic');
  const wallet = buildWalletFromMnemonic(mnemonic);
  const pub = getPublicKeyFromWallet(wallet);
  console.log(JSON.stringify({
    address: wallet.address,
    public_key: pub,
  }, null, 2));
}

async function cmdUploadPubkey(args) {
  const mnemonic = requireArg(args, 'mnemonic');
  const baseUrl = normalizeBaseUrl(args['api-url']);
  const wallet = buildWalletFromMnemonic(mnemonic);
  const timestamp = Math.floor(Date.now() / 1000);
  const publicKey = getPublicKeyFromWallet(wallet);

  const messageForSigning = {
    action: 'upload_pubkey',
    address: wallet.address,
    public_key: publicKey,
    timestamp,
  };
  const signature = await signMessage(wallet, messageForSigning);

  const body = {
    address: wallet.address,
    public_key: publicKey,
    timestamp,
    signature,
  };

  const res = await getJson(`${baseUrl}pubkey/upload`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
  console.log(JSON.stringify(res, null, 2));
}

async function cmdAlias(args) {
  const mnemonic = requireArg(args, 'mnemonic');
  const alias = requireArg(args, 'alias');
  const baseUrl = normalizeBaseUrl(args['api-url']);
  const wallet = buildWalletFromMnemonic(mnemonic);
  const timestamp = Math.floor(Date.now() / 1000);

  const messageForSigning = {
    action: 'register_alias',
    alias,
    address: wallet.address,
    timestamp,
  };
  const signature = await signMessage(wallet, messageForSigning);

  const body = { alias, address: wallet.address, timestamp, signature };
  const res = await getJson(`${baseUrl}alias/register`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
  console.log(JSON.stringify(res, null, 2));
}

async function cmdSend(args) {
  const mnemonic = requireArg(args, 'mnemonic');
  const to = requireArg(args, 'to');
  const baseUrl = normalizeBaseUrl(args['api-url']);
  const wallet = buildWalletFromMnemonic(mnemonic);

  const config = await getConfig(baseUrl);
  const difficulty = Number(config.difficulty ?? 3);

  let content;
  if (args.json) {
    content = JSON.parse(String(args.json));
  } else {
    content = {
      type: 'email',
      subject: String(args.subject || '(No Subject)'),
      body: String(args.body || ''),
    };
  }

  const payloadRaw = JSON.stringify(content);
  const payloadB64 = toBase64Utf8(payloadRaw);
  const payloadBytes = Buffer.from(payloadB64, 'base64');
  const payloadHash = sha256HexBytes(payloadBytes);
  const timestamp = Math.floor(Date.now() / 1000);

  const toPow = await resolveRecipientForPow(baseUrl, to);
  const nonce = calcNonce({
    from: wallet.address,
    toPow,
    timestamp,
    payloadHash,
    difficulty,
  });

  const messageForSigning = {
    from: wallet.address,
    to,
    timestamp,
    payload: payloadB64,
    encrypted: false,
    nonce,
  };
  const signature = await signMessage(wallet, messageForSigning);

  const body = {
    from: wallet.address,
    to,
    timestamp,
    payload: payloadB64,
    encrypted: false,
    nonce,
    signature,
  };

  const res = await getJson(`${baseUrl}send`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
  console.log(JSON.stringify(res, null, 2));
}

async function cmdInbox(args) {
  const mnemonic = requireArg(args, 'mnemonic');
  const baseUrl = normalizeBaseUrl(args['api-url']);
  const limit = Number(args.limit || 10);
  const wallet = buildWalletFromMnemonic(mnemonic);
  const timestamp = Math.floor(Date.now() / 1000);

  const messageForSigning = {
    action: 'get_inbox',
    address: wallet.address,
    timestamp,
  };
  const sig = await signMessage(wallet, messageForSigning);

  const qs = new URLSearchParams({
    sig,
    timestamp: String(timestamp),
    limit: String(limit),
    offset: String(args.offset || 0),
  });

  const res = await getJson(`${baseUrl}inbox/${wallet.address}?${qs.toString()}`);
  console.log(JSON.stringify(res, null, 2));
}

function printHelp() {
  console.log(`
TokenMail JS CLI (ethers)


Commands:
  addr --mnemonic "..." [--api-url URL]
  upload-pubkey --mnemonic "..." [--api-url URL]
  alias --mnemonic "..." --alias my-bot [--api-url URL]
  send --mnemonic "..." --to recipient [--subject S --body B | --json '{...}'] [--api-url URL]
  inbox --mnemonic "..." [--limit 10 --offset 0 --api-url URL]

Notes:
  - 需要 Node.js >= 18
  - 依赖: npm i ethers
  - 外部邮箱可直接 --to user@gmail.com（服务端会自动按外发处理）
`);
}

async function main() {
  const { command, args } = parseArgs(process.argv.slice(2));
  try {
    switch (command) {
      case 'addr':
        await cmdAddr(args);
        break;
      case 'upload-pubkey':
        await cmdUploadPubkey(args);
        break;
      case 'alias':
        await cmdAlias(args);
        break;
      case 'send':
        await cmdSend(args);
        break;
      case 'inbox':
        await cmdInbox(args);
        break;
      case 'help':
      case '--help':
      case '-h':
      default:
        printHelp();
        break;
    }
  } catch (err) {
    console.error(`Error: ${err?.message || err}`);
    process.exit(1);
  }
}

main();
