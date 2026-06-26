#!/usr/bin/env node

// Unified Player Creation Tool for Structs AI Agents
//
// Handles the entire player creation flow:
//   1. Generate or recover a mnemonic
//   2. Derive address + pubkey
//   3. Check if player already exists (via REST)
//   4. Sign guild-join proxy message (hex-encoded, NOT base64)
//   5. POST to guild API signup endpoint
//   6. Poll until player ID is confirmed
//
// Outputs a single JSON object to stdout with mnemonic, address, pubkey, player_id.
//
// Usage:
//   node create-player.mjs --guild-id "0-1" --guild-api "http://crew.oh.energy/api/" --reactor-api "https://public.testnet.structs.network"
//   node create-player.mjs --mnemonic "word1 word2 ..." --guild-id "0-1" --guild-api "http://crew.oh.energy/api/" --reactor-api "https://public.testnet.structs.network" --username "my-agent" --pfp "ipfs://bafy..."
//
// As of structsd v0.16.0, the guild API forwards `username` and `pfp` to the
// chain via MsgGuildMembershipJoinProxy.playerName / playerPfp, so the chain
// rejects invalid values at signup time. This script preflights the same
// validators as `x/structs/types/ugc.go` so failures surface locally instead
// of as opaque "broadcast OK, player never appeared" timeouts.

import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";
import { Secp256k1, sha256 } from "@cosmjs/crypto";

// --- Encoding ---
// The guild API requires hex-encoded pubkey and signature, NOT base64.
// This is the #1 reason agents fail when attempting manual signing.
// - Pubkey: hex-encoded compressed secp256k1 (66 hex chars)
// - Signature: hex-encoded raw R||S (128 hex chars)
// - Message: plaintext GUILD<id>ADDRESS<addr>NONCE<n>, SHA256-hashed, Secp256k1-signed

function bytesToHex(byteArray) {
  return Array.from(byteArray, byte => ('0' + (byte & 0xFF).toString(16)).slice(-2)).join('');
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--mnemonic' && argv[i + 1]) args.mnemonic = argv[++i];
    else if (argv[i] === '--guild-id' && argv[i + 1]) args.guildId = argv[++i];
    else if (argv[i] === '--guild-api' && argv[i + 1]) args.guildApi = argv[++i];
    else if (argv[i] === '--reactor-api' && argv[i + 1]) args.reactorApi = argv[++i];
    else if (argv[i] === '--username' && argv[i + 1]) args.username = argv[++i];
    else if (argv[i] === '--pfp' && argv[i + 1]) args.pfp = argv[++i];
    else if (argv[i] === '--timeout' && argv[i + 1]) args.timeout = parseInt(argv[++i], 10);
  }
  return args;
}

// --- UGC validation (mirror of x/structs/types/ugc.go in structsd v0.16.0) ---
// These checks must agree with the chain validators or signup will appear to
// succeed and then silently fail. If you change one side, change the other.

const PLAYER_NAME_RE = /^[\p{L}0-9\-_]{3,20}$/u;
const OBJECT_ID_RE = /^[0-9]+-[0-9]+$/;
const OPAQUE_PFP_RE = /^[A-Za-z0-9._/\-]{1,256}$/;
const ALLOWED_PFP_SCHEMES = new Set(["https", "http", "ipfs", "ipns", "ar"]);
const INVISIBLE_RUNES = new Set([
  0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
  0x2066, 0x2067, 0x2068, 0x2069,
  0x200B, 0x200C, 0x200D, 0x2060,
  0x00AD, 0xFEFF,
]);
const COMBINING_RANGES = [
  // Mn (non-spacing marks)
  [0x0300, 0x036F], [0x0483, 0x0489], [0x0591, 0x05BD], [0x05BF, 0x05BF],
  [0x05C1, 0x05C2], [0x05C4, 0x05C5], [0x05C7, 0x05C7], [0x0610, 0x061A],
  [0x064B, 0x065F], [0x0670, 0x0670], [0x06D6, 0x06DC], [0x06DF, 0x06E4],
  [0x06E7, 0x06E8], [0x06EA, 0x06ED], [0x0711, 0x0711], [0x0730, 0x074A],
  [0x07A6, 0x07B0], [0x07EB, 0x07F3], [0x0816, 0x0819], [0x081B, 0x0823],
  [0x0825, 0x0827], [0x0829, 0x082D], [0x0859, 0x085B], [0x08D3, 0x08E1],
  [0x08E3, 0x0902], [0x093A, 0x093A], [0x093C, 0x093C], [0x0941, 0x0948],
  [0x094D, 0x094D], [0x0951, 0x0957], [0x0962, 0x0963], [0x0981, 0x0981],
  [0x09BC, 0x09BC], [0x09C1, 0x09C4], [0x09CD, 0x09CD], [0x09E2, 0x09E3],
  [0x09FE, 0x09FE], [0x0A01, 0x0A02], [0x0A3C, 0x0A3C], [0x0A41, 0x0A42],
  [0x0A47, 0x0A48], [0x0A4B, 0x0A4D], [0x0A51, 0x0A51], [0x0A70, 0x0A71],
  [0x1AB0, 0x1AFF], [0x1DC0, 0x1DFF], [0x20D0, 0x20FF], [0xFE00, 0xFE0F],
  [0xFE20, 0xFE2F],
  // Me (enclosing marks)
  [0x0488, 0x0489], [0x1ABE, 0x1ABE], [0x20DD, 0x20E0], [0x20E2, 0x20E4],
];

function isCombiningMark(cp) {
  for (const [lo, hi] of COMBINING_RANGES) {
    if (cp >= lo && cp <= hi) return true;
  }
  return false;
}

function isFormatOrSurrogate(cp) {
  // Basic Cf coverage. Adequate for common spoofing vectors but not
  // exhaustive — the chain uses Go's unicode.Is(unicode.Cf, ...) which is
  // exhaustive. If you need 100% parity, plug in a Unicode tables library.
  if (cp >= 0xD800 && cp <= 0xDFFF) return true; // surrogates
  if (cp === 0x00AD) return true;
  if (cp >= 0x0600 && cp <= 0x0605) return true;
  if (cp === 0x061C) return true;
  if (cp === 0x06DD) return true;
  if (cp === 0x070F) return true;
  if (cp === 0x180E) return true;
  if (cp >= 0x200B && cp <= 0x200F) return true;
  if (cp >= 0x202A && cp <= 0x202E) return true;
  if (cp >= 0x2060 && cp <= 0x2064) return true;
  if (cp >= 0x2066 && cp <= 0x206F) return true;
  if (cp === 0xFEFF) return true;
  if (cp >= 0xFFF9 && cp <= 0xFFFB) return true;
  return false;
}

function normalizeAndCheckRunes(s, label) {
  if (typeof s !== "string") {
    throw new Error(`${label} must be a string`);
  }
  let normalized;
  try {
    normalized = s.normalize("NFC");
  } catch {
    throw new Error(`${label} contains invalid UTF-8`);
  }
  for (const r of normalized) {
    const cp = r.codePointAt(0);
    if (isCombiningMark(cp)) {
      throw new Error(`${label} contains combining marks (Zalgo/stacked diacritics not allowed)`);
    }
    if (INVISIBLE_RUNES.has(cp) || isFormatOrSurrogate(cp)) {
      throw new Error(`${label} contains bidi-override, zero-width, or other invisible characters`);
    }
  }
  return normalized;
}

function validatePlayerName(name) {
  const normalized = normalizeAndCheckRunes(name, "player name");
  if (OBJECT_ID_RE.test(normalized)) {
    throw new Error("player name cannot resemble an object ID (e.g. '1-2')");
  }
  if (!PLAYER_NAME_RE.test(normalized)) {
    throw new Error("player name must be 3-20 characters of letters, digits, hyphens, or underscores (no spaces, no apostrophes)");
  }
  return normalized;
}

function validatePfp(pfp) {
  if (pfp === "" || pfp === null || pfp === undefined) {
    return "";
  }
  if (typeof pfp !== "string") {
    throw new Error("pfp must be a string");
  }
  const runeCount = [...pfp].length;
  if (runeCount > 256) {
    throw new Error(`pfp must be at most 256 characters (got ${runeCount})`);
  }
  for (const r of pfp) {
    const cp = r.codePointAt(0);
    if (cp < 0x20 || cp === 0x7F) {
      throw new Error(`pfp contains forbidden control character (0x${cp.toString(16).padStart(2, "0")})`);
    }
    if (INVISIBLE_RUNES.has(cp) || isFormatOrSurrogate(cp)) {
      throw new Error("pfp contains bidi-override, zero-width, or other invisible characters");
    }
  }
  if (/[<>`"\\\s]/.test(pfp)) {
    throw new Error("pfp must not contain <, >, backtick, quote, backslash, or any whitespace");
  }
  if (!pfp.includes(":")) {
    if (!OPAQUE_PFP_RE.test(pfp)) {
      throw new Error("pfp opaque identifier must be 1-256 characters of letters, digits, dot, slash, hyphen, or underscore");
    }
    return pfp;
  }
  const colonIdx = pfp.indexOf(":");
  const scheme = pfp.slice(0, colonIdx).toLowerCase();
  if (!scheme) {
    throw new Error("pfp URL must have a scheme");
  }
  if (!ALLOWED_PFP_SCHEMES.has(scheme)) {
    throw new Error(`pfp URL scheme '${scheme}' is not allowed (permitted: https, http, ipfs, ipns, ar)`);
  }
  let parsed;
  try {
    parsed = new URL(pfp);
  } catch (err) {
    throw new Error(`pfp URL is malformed: ${err.message}`);
  }
  if (scheme === "https" || scheme === "http") {
    if (!parsed.host) {
      throw new Error(`pfp ${scheme} URL must include a host`);
    }
  } else {
    // ipfs / ipns / ar may put the resource id in host or path or as opaque
    if (!parsed.host && !parsed.pathname && !parsed.search && !parsed.hash) {
      throw new Error(`pfp ${scheme} URL must include a content identifier`);
    }
  }
  return pfp;
}

function fail(obj) {
  console.log(JSON.stringify({ success: false, ...obj }));
  process.exit(1);
}

async function checkPlayerExists(reactorApi, address) {
  const url = `${reactorApi}/structs/address/${address}`;
  const res = await fetch(url);
  if (!res.ok) return null;
  const data = await res.json();
  const record = data.Address || data.address || data;
  const playerId = record.playerId || record.player_id || null;
  if (playerId && playerId !== "1-0") return playerId;
  return null;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const args = parseArgs(process.argv);

  if (!args.guildId || !args.guildApi || !args.reactorApi) {
    fail({
      error: "Missing required arguments: --guild-id, --guild-api, --reactor-api",
      usage: 'node create-player.mjs --guild-id "0-1" --guild-api "http://crew.oh.energy/api/" --reactor-api "https://public.testnet.structs.network" [--mnemonic "..."] [--username "name"] [--pfp "ipfs://..."] [--timeout 120]'
    });
  }

  // Preflight UGC values when explicitly provided. The chain rejects invalid
  // names/pfps at signup, so we validate locally first to return a clearer
  // error.
  if (args.username !== undefined) {
    try {
      args.username = validatePlayerName(args.username);
    } catch (err) {
      fail({ error: `Invalid --username: ${err.message}`, hint: "See knowledge/mechanics/ugc-moderation.md for the player name rules." });
    }
  }
  if (args.pfp !== undefined && args.pfp !== "") {
    try {
      args.pfp = validatePfp(args.pfp);
    } catch (err) {
      fail({ error: `Invalid --pfp: ${err.message}`, hint: "See knowledge/mechanics/ugc-moderation.md for the pfp rules." });
    }
  }

  const timeout = args.timeout || 120;
  const reactorApi = args.reactorApi.replace(/\/+$/, '');
  const guildApi = args.guildApi.replace(/\/+$/, '');

  // Step 1: Wallet — generate or recover
  let wallet;
  let mnemonic;
  let generated = false;

  if (args.mnemonic) {
    try {
      wallet = await DirectSecp256k1HdWallet.fromMnemonic(args.mnemonic, { prefix: "structs" });
      mnemonic = args.mnemonic;
    } catch (err) {
      fail({ error: `Invalid mnemonic: ${err.message}` });
    }
  } else {
    wallet = await DirectSecp256k1HdWallet.generate(24, { prefix: "structs" });
    mnemonic = wallet.mnemonic;
    generated = true;
  }

  const accounts = await wallet.getAccountsWithPrivkeys();
  const account = accounts[0];
  const address = account.address;
  const pubkeyHex = bytesToHex(account.pubkey);

  // Step 2: Check if player already exists
  try {
    const existingPlayerId = await checkPlayerExists(reactorApi, address);
    if (existingPlayerId) {
      console.log(JSON.stringify({
        success: true,
        mnemonic: generated ? mnemonic : undefined,
        address,
        pubkey: pubkeyHex,
        player_id: existingPlayerId,
        guild_id: args.guildId,
        created: false,
        message: "Player already exists for this address"
      }));
      process.exit(0);
    }
  } catch (err) {
    fail({
      error: `Failed to check player status: ${err.message}`,
      address,
      hint: "Verify --reactor-api URL is correct and reachable"
    });
  }

  // Step 3: Sign guild-join proxy message
  const nonce = "0";
  const proxyMessage = `GUILD${args.guildId}ADDRESS${address}NONCE${nonce}`;
  const digest = sha256(new TextEncoder().encode(proxyMessage));
  const signature = await Secp256k1.createSignature(digest, account.privkey);
  const signatureHex = bytesToHex(signature.toFixedLength());

  let username = args.username || `agent-${address.slice(-6)}`;
  // Re-validate the auto-generated default just in case address.slice(-6)
  // happens to produce something pathological.
  try {
    username = validatePlayerName(username);
  } catch (err) {
    fail({ error: `Default username failed validation: ${err.message}`, hint: "Pass --username with a value matching ^[\\p{L}0-9\\-_]{3,20}$" });
  }
  const pfp = args.pfp ?? null;

  const signupPayload = {
    primary_address: address,
    signature: signatureHex,
    pubkey: pubkeyHex,
    guild_id: args.guildId,
    username,
    pfp
  };

  // Step 4: POST to guild API
  let signupResponse;
  try {
    signupResponse = await fetch(`${guildApi}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(signupPayload)
    });
  } catch (err) {
    fail({
      error: `Failed to connect to guild API: ${err.message}`,
      mnemonic: generated ? mnemonic : undefined,
      address,
      pubkey: pubkeyHex,
      guild_id: args.guildId,
      hint: "Verify --guild-api URL is correct. The signup endpoint is POST-only."
    });
  }

  let signupBody;
  try {
    signupBody = await signupResponse.json();
  } catch {
    signupBody = await signupResponse.text();
  }

  if (!signupResponse.ok) {
    fail({
      error: `Guild API returned ${signupResponse.status}`,
      mnemonic: generated ? mnemonic : undefined,
      address,
      pubkey: pubkeyHex,
      guild_id: args.guildId,
      signup_response: signupBody,
      hint: "If you got HTML back, you may be hitting the wrong URL or the guild does not support programmatic signup"
    });
  }

  // Step 5: Poll for player creation
  const startTime = Date.now();
  const pollInterval = 10_000;
  let playerId = null;

  process.stderr.write(`Signup submitted. Polling for player creation (timeout: ${timeout}s)...\n`);

  while (Date.now() - startTime < timeout * 1000) {
    await sleep(pollInterval);

    try {
      playerId = await checkPlayerExists(reactorApi, address);
      if (playerId) break;
    } catch {
      // Network hiccup during poll — keep trying
    }

    const elapsed = Math.round((Date.now() - startTime) / 1000);
    process.stderr.write(`  ...${elapsed}s elapsed, still waiting\n`);
  }

  if (!playerId) {
    fail({
      error: `Player creation timed out after ${timeout}s. The signup was submitted but the player has not appeared yet. You can re-run with the same --mnemonic to resume polling.`,
      mnemonic: generated ? mnemonic : undefined,
      address,
      pubkey: pubkeyHex,
      guild_id: args.guildId,
      signup_response: signupBody
    });
  }

  // Step 6: Return complete package
  console.log(JSON.stringify({
    success: true,
    mnemonic: generated ? mnemonic : undefined,
    address,
    pubkey: pubkeyHex,
    player_id: playerId,
    guild_id: args.guildId,
    username,
    pfp,
    created: true,
    next_step: `structsd tx structs planet-explore --from [key-name] --gas auto --gas-adjustment 1.5 -- ${playerId}`
  }));

  process.exit(0);
}

main();
