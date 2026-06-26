#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const os = require("os");
const crypto = require("crypto");
const vm = require("vm");

const DEFAULT_KEYSTORE = process.env.TOKENMAIL_KEYSTORE || path.join(os.homedir(), ".tokenmail");
const DEFAULT_API_URL = process.env.TOKENMAIL_API_URL || "https://tokenforge.fit/api";
const ETHERS_UMD_URL = process.env.TOKENMAIL_ETHERS_URL || "https://cdn.jsdelivr.net/npm/ethers@6.13.5/dist/ethers.umd.min.js";
const MAX_POW_ATTEMPTS = 10_000_000;

let ethersLib = null;

function usage() {
  console.log(`TokenMail JS CLI (sandbox-friendly, no password mode)

Commands:
  create <name> [--alias <alias>] [--mnemonic "..."] [--private-key 0x...] [--keystore <dir>] [--api-url <url>]
  ensure <name> [--alias <alias>] [--mnemonic "..."] [--private-key 0x...] [--keystore <dir>] [--api-url <url>]
  list [--keystore <dir>]
  send [agent] --to <recipient> [--subject <s>] [--body <b>] [--json '{...}'] [--from-private-key 0x...] [--from-mnemonic "..."] [--api-url <url>] [--keystore <dir>]
  send-external [agent] --to <email> --subject <s> --body <b> [--html <html>] [--no-sign] [--from-private-key 0x...] [--from-mnemonic "..."] [--api-url <url>] [--keystore <dir>]
  inbox [agent] [--limit <n>] [--offset <n>] [--from-private-key 0x...] [--from-mnemonic "..."] [--api-url <url>] [--keystore <dir>]

  alias [agent] <alias> [--from-private-key 0x...] [--from-mnemonic "..."] [--api-url <url>] [--keystore <dir>]
  export <agent> [--output <file>] [--keystore <dir>]
  import <name> --mnemonic "..." [--alias <alias>] [--keystore <dir>]
  delete <agent> --force [--keystore <dir>]

No password required. Keep mnemonic/private key secure yourself.

Sandbox mode tips:
  - No local file writes: use --from-private-key (or TOKENMAIL_PRIVATE_KEY)
  - No npm install: CLI auto-loads ethers from CDN in memory when local module is missing`);
}

function parseCli(argv) {
  const command = argv[2];
  const args = { _: [] };
  for (let i = 3; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith("--")) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
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

async function getEthers() {
  if (ethersLib) return ethersLib;

  try {
    ethersLib = require("ethers");
    return ethersLib;
  } catch {
    // fallback to CDN UMD
  }

  const res = await fetch(ETHERS_UMD_URL, { method: "GET" });
  if (!res.ok) throw new Error(`Failed to load ethers from CDN (${res.status})`);
  const code = await res.text();

  const sandbox = {
    console,
    setTimeout,
    clearTimeout,
    setInterval,
    clearInterval,
    TextEncoder,
    TextDecoder,
    Uint8Array,
    ArrayBuffer,
    DataView,
    Buffer,
    globalThis: null,
    self: null,
    window: null,
    global: null
  };
  sandbox.globalThis = sandbox;
  sandbox.self = sandbox;
  sandbox.window = sandbox;
  sandbox.global = sandbox;

  vm.runInNewContext(code, sandbox, { filename: "ethers.umd.min.js" });
  ethersLib = sandbox.ethers;
  if (!ethersLib) throw new Error("Loaded ethers script but module was not exposed");
  return ethersLib;
}

function safeName(name) {
  return name.toLowerCase().replace(/\s+/g, "-").replace(/_/g, "-");
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function canonicalJson(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map((x) => canonicalJson(x)).join(",")}]`;
  const keys = Object.keys(value).sort();
  return `{${keys.map((k) => `${JSON.stringify(k)}:${canonicalJson(value[k])}`).join(",")}}`;
}

async function signCanonical(wallet, messageObj) {
  return wallet.signMessage(canonicalJson(messageObj));
}

function sha256Hex(data) {
  const hasher = crypto.createHash("sha256");
  hasher.update(data);
  return hasher.digest("hex");
}

function calculatePowNonce(fromAddr, toAddr, timestamp, payloadHash, difficulty) {
  const target = "0".repeat(difficulty);
  for (let i = 0; i < MAX_POW_ATTEMPTS; i += 1) {
    const nonce = String(i);
    const digest = sha256Hex(`${nonce}:${fromAddr}:${toAddr}:${timestamp}:${payloadHash}`);
    if (digest.startsWith(target)) return nonce;
  }
  throw new Error("Failed to compute PoW nonce");
}

function normalizeBaseUrl(apiUrl) {
  return String(apiUrl || DEFAULT_API_URL).replace(/\/+$/, "");
}

async function apiGet(apiUrl, route, query = undefined) {
  const base = normalizeBaseUrl(apiUrl);
  const url = new URL(`${base}/${route.replace(/^\/+/, "")}`);
  if (query) {
    for (const [k, v] of Object.entries(query)) {
      url.searchParams.set(k, String(v));
    }
  }
  const res = await fetch(url, { method: "GET" });
  if (!res.ok) throw new Error(`GET ${route} failed (${res.status}): ${await res.text()}`);
  return res.json();
}

async function apiPost(apiUrl, route, payload) {
  const base = normalizeBaseUrl(apiUrl);
  const res = await fetch(`${base}/${route.replace(/^\/+/, "")}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`POST ${route} failed (${res.status}): ${await res.text()}`);
  return res.json();
}

class PlainKeystore {
  constructor(keystoreDir) {
    this.keystoreDir = keystoreDir;
    this.keysDir = path.join(keystoreDir, "keys");
  }

  getAgentPath(name) {
    return path.join(this.keysDir, `${safeName(name)}.json`);
  }

  saveAgent(agent) {
    ensureDir(this.keysDir);
    const file = this.getAgentPath(agent.name);
    fs.writeFileSync(file, JSON.stringify(agent, null, 2), "utf8");
    return agent;
  }

  loadAgent(name) {
    const file = this.getAgentPath(name);
    if (!fs.existsSync(file)) return null;
    return JSON.parse(fs.readFileSync(file, "utf8"));
  }

  listAgentNames() {
    if (!fs.existsSync(this.keysDir)) return [];
    return fs.readdirSync(this.keysDir).filter((n) => n.endsWith(".json")).map((n) => n.replace(/\.json$/, "")).sort();
  }

  listAgents() {
    return this.listAgentNames().map((name) => {
      try {
        return this.loadAgent(name);
      } catch {
        return null;
      }
    }).filter(Boolean);
  }

  deleteAgent(name) {
    const file = this.getAgentPath(name);
    if (!fs.existsSync(file)) return false;
    fs.unlinkSync(file);
    return true;
  }
}

function getCommon(args) {
  return {
    apiUrl: args["api-url"] || DEFAULT_API_URL,
    keystoreDir: args.keystore || DEFAULT_KEYSTORE
  };
}

async function walletFromRecord(record) {
  const { Wallet } = await getEthers();
  if (record.private_key) return new Wallet(record.private_key);
  if (record.mnemonic) return Wallet.fromPhrase(record.mnemonic);
  throw new Error("Agent record missing mnemonic/private_key");
}

function buildAgentRecord(name, wallet, opts = {}) {
  return {
    name,
    address: wallet.address,
    alias: opts.alias || null,
    mnemonic: opts.mnemonic || null,
    private_key: opts.private_key || null,
    created: new Date().toISOString(),
    warning: "THIS FILE CONTAINS SECRET KEY MATERIAL. BACK UP SECURELY."
  };
}

async function getPublicKeyForUpload(wallet) {
  const { SigningKey } = await getEthers();
  const uncompressed = SigningKey.computePublicKey(wallet.privateKey, false);
  if (uncompressed.startsWith("0x04")) return `0x${uncompressed.slice(4)}`;
  return uncompressed;
}

async function resolveForPowIfNeeded(apiUrl, toAddr) {
  if (toAddr.startsWith("0x") || toAddr.includes("@")) return toAddr;
  const resolved = await apiGet(apiUrl, `resolve/${encodeURIComponent(toAddr)}`);
  return resolved.address;
}

async function uploadPubkey(apiUrl, wallet) {
  const timestamp = Math.floor(Date.now() / 1000);
  const publicKey = await getPublicKeyForUpload(wallet);
  const signObj = { action: "upload_pubkey", address: wallet.address, public_key: publicKey, timestamp };
  const signature = await signCanonical(wallet, signObj);
  await apiPost(apiUrl, "pubkey/upload", { address: wallet.address, public_key: publicKey, timestamp, signature });
}

async function registerAlias(apiUrl, wallet, alias) {
  const timestamp = Math.floor(Date.now() / 1000);
  const signObj = { action: "register_alias", alias, address: wallet.address, timestamp };
  const signature = await signCanonical(wallet, signObj);
  await apiPost(apiUrl, "alias/register", { alias, address: wallet.address, timestamp, signature });
}

function requireAgent(ks, name) {
  const data = ks.loadAgent(name);
  if (!data) throw new Error(`Agent '${name}' not found`);
  return data;
}

async function walletFromDirectArgs(args) {
  const privateKey = args["from-private-key"] || process.env.TOKENMAIL_PRIVATE_KEY;
  if (privateKey) {
    const { Wallet } = await getEthers();
    return new Wallet(String(privateKey));
  }

  const mnemonic = args["from-mnemonic"] || process.env.TOKENMAIL_MNEMONIC;
  if (mnemonic) {
    const { Wallet } = await getEthers();
    return Wallet.fromPhrase(String(mnemonic));
  }

  return null;
}

async function resolveSender(args, agentName, keystoreDir) {
  const directWallet = await walletFromDirectArgs(args);
  if (directWallet) {
    return {
      wallet: directWallet,
      agentName: agentName || "inline-key",
      record: null,
      ks: null,
      fromKeystore: false
    };
  }

  if (!agentName) {
    throw new Error("Missing agent name (or pass --from-private-key / --from-mnemonic)");
  }

  const ks = new PlainKeystore(keystoreDir);
  const record = requireAgent(ks, agentName);
  const wallet = await walletFromRecord(record);

  return {
    wallet,
    agentName,
    record,
    ks,
    fromKeystore: true
  };
}

async function cmdCreate(args) {
  const name = args._[0];
  if (!name) throw new Error("Missing agent name");

  const { apiUrl, keystoreDir } = getCommon(args);
  const ks = new PlainKeystore(keystoreDir);
  const { Wallet } = await getEthers();

  let wallet;
  const recordOpts = { alias: args.alias || null, mnemonic: null, private_key: null };

  if (args["private-key"]) {
    wallet = new Wallet(String(args["private-key"]));
    recordOpts.private_key = wallet.privateKey;
  } else if (args.mnemonic) {
    wallet = Wallet.fromPhrase(String(args.mnemonic));
    recordOpts.mnemonic = String(args.mnemonic);
  } else {
    wallet = Wallet.createRandom();
    recordOpts.mnemonic = wallet.mnemonic.phrase;
  }

  const record = buildAgentRecord(name, wallet, recordOpts);
  ks.saveAgent(record);

  try {
    await uploadPubkey(apiUrl, wallet);
    console.log("Public key uploaded");
  } catch (err) {
    console.log(`Warning: upload_pubkey failed: ${err.message}`);
  }

  if (record.alias) {
    try {
      await registerAlias(apiUrl, wallet, record.alias);
      console.log(`Alias registered: ${record.alias}`);
    } catch (err) {
      console.log(`Warning: alias registration failed: ${err.message}`);
    }
  }

  console.log("=".repeat(60));
  console.log(`Agent: ${record.name}`);
  console.log(`Address: ${record.address}`);
  if (record.alias) console.log(`Email: ${record.alias}@mail.tokenforge.fit`);
  if (record.mnemonic) {
    console.log("Mnemonic (SAVE OFFLINE):");
    console.log(record.mnemonic);
  }
  if (record.private_key) {
    console.log("Private Key (SAVE OFFLINE):");
    console.log(record.private_key);
  }
  console.log("=".repeat(60));
}

async function cmdImport(args) {
  const name = args._[0];
  if (!name) throw new Error("Missing agent name");
  if (!args.mnemonic && !args["private-key"]) throw new Error("Provide --mnemonic or --private-key");

  const { keystoreDir } = getCommon(args);
  const ks = new PlainKeystore(keystoreDir);
  const { Wallet } = await getEthers();

  let wallet;
  const opts = { alias: args.alias || null, mnemonic: null, private_key: null };

  if (args["private-key"]) {
    wallet = new Wallet(String(args["private-key"]));
    opts.private_key = wallet.privateKey;
  } else {
    wallet = Wallet.fromPhrase(String(args.mnemonic));
    opts.mnemonic = String(args.mnemonic);
  }

  ks.saveAgent(buildAgentRecord(name, wallet, opts));
  console.log(`Imported agent '${name}' (${wallet.address})`);
}

async function cmdEnsure(args) {
  const name = args._[0];
  if (!name) throw new Error("Missing agent name");

  const { apiUrl, keystoreDir } = getCommon(args);
  const ks = new PlainKeystore(keystoreDir);

  let record = ks.loadAgent(name);
  let created = false;
  let wallet;

  if (!record) {
    const { Wallet } = await getEthers();
    const recordOpts = { alias: args.alias || null, mnemonic: null, private_key: null };

    if (args["private-key"]) {
      wallet = new Wallet(String(args["private-key"]));
      recordOpts.private_key = wallet.privateKey;
    } else if (args.mnemonic) {
      wallet = Wallet.fromPhrase(String(args.mnemonic));
      recordOpts.mnemonic = String(args.mnemonic);
    } else {
      wallet = Wallet.createRandom();
      recordOpts.mnemonic = wallet.mnemonic.phrase;
    }

    record = buildAgentRecord(name, wallet, recordOpts);
    ks.saveAgent(record);
    created = true;

    try {
      await uploadPubkey(apiUrl, wallet);
    } catch (err) {
      console.log(`Warning: upload_pubkey failed: ${err.message}`);
    }

    if (record.alias) {
      try {
        await registerAlias(apiUrl, wallet, record.alias);
      } catch (err) {
        console.log(`Warning: alias registration failed: ${err.message}`);
      }
    }
  } else {
    wallet = await walletFromRecord(record);

    if (args.alias && args.alias !== record.alias) {
      try {
        await registerAlias(apiUrl, wallet, String(args.alias));
        record = { ...record, alias: String(args.alias) };
        ks.saveAgent(record);
      } catch (err) {
        console.log(`Warning: alias registration failed: ${err.message}`);
      }
    }
  }

  console.log(JSON.stringify({
    name: record.name,
    address: record.address,
    alias: record.alias,
    created
  }, null, 2));
}

async function cmdList(args) {
  const { keystoreDir } = getCommon(args);
  const ks = new PlainKeystore(keystoreDir);
  const agents = ks.listAgents();
  if (agents.length === 0) {
    console.log("No agents found");
    return;
  }

  console.log("Name                 Address                                     Alias");
  console.log("--------------------------------------------------------------------------------");
  for (const a of agents) {
    console.log(`${String(a.name || "-").padEnd(20)} ${String(a.address || "-").padEnd(42)} ${String(a.alias || "-")}`);
  }
}

async function cmdSend(args) {
  const agentName = args._[0] || null;
  if (!args.to) throw new Error("Missing --to");

  const { apiUrl, keystoreDir } = getCommon(args);
  const sender = await resolveSender(args, agentName, keystoreDir);
  const wallet = sender.wallet;

  const content = args.json
    ? JSON.parse(args.json)
    : { type: "email", subject: args.subject || "(No Subject)", body: args.body || "" };

  const payloadBytes = Buffer.from(JSON.stringify(content), "utf8");
  const payload = payloadBytes.toString("base64");
  const payloadHash = sha256Hex(payloadBytes);
  const timestamp = Math.floor(Date.now() / 1000);

  const config = await apiGet(apiUrl, "config");
  const toForPow = await resolveForPowIfNeeded(apiUrl, String(args.to));
  const nonce = calculatePowNonce(wallet.address, toForPow, timestamp, payloadHash, Number(config.difficulty || 4));

  const signObj = { from: wallet.address, to: String(args.to), timestamp, payload, encrypted: false, nonce };
  const signature = await signCanonical(wallet, signObj);

  const result = await apiPost(apiUrl, "send", {
    from: wallet.address,
    to: String(args.to),
    timestamp,
    payload,
    encrypted: false,
    nonce,
    signature
  });

  console.log(`Email sent. message_id=${result.message_id}`);
}

async function cmdSendExternal(args) {
  const agentName = args._[0] || null;
  if (!args.to) throw new Error("Missing --to");
  if (!args.subject) throw new Error("Missing --subject");
  if (!args.body) throw new Error("Missing --body");

  const { apiUrl, keystoreDir } = getCommon(args);
  const sender = await resolveSender(args, agentName, keystoreDir);
  const wallet = sender.wallet;

  const timestamp = Math.floor(Date.now() / 1000);
  const signObj = { action: "send_external", from: wallet.address, to: String(args.to), subject: String(args.subject), timestamp };
  const signature = await signCanonical(wallet, signObj);

  const result = await apiPost(apiUrl, "send-external", {
    from: wallet.address,
    to: String(args.to),
    subject: String(args.subject),
    body: String(args.body),
    html: args.html ? String(args.html) : undefined,
    sign: !args["no-sign"],
    timestamp,
    signature
  });

  console.log(`${result.status}: sent to ${result.to}`);
}

function tryDecodePayload(payload) {
  try {
    const raw = Buffer.from(payload, "base64").toString("utf8");
    try {
      return JSON.parse(raw);
    } catch {
      return raw;
    }
  } catch {
    return payload;
  }
}

async function cmdInbox(args) {
  const agentName = args._[0] || null;

  const { apiUrl, keystoreDir } = getCommon(args);
  const sender = await resolveSender(args, agentName, keystoreDir);
  const wallet = sender.wallet;

  const timestamp = Math.floor(Date.now() / 1000);
  const limit = Number(args.limit || 10);
  const offset = Number(args.offset || 0);

  const config = await apiGet(apiUrl, "config");
  const inboxPowPayloadHash = sha256Hex(Buffer.from(`inbox:${wallet.address}:${limit}:${offset}`, "utf8"));
  const nonce = calculatePowNonce(
    wallet.address,
    wallet.address,
    timestamp,
    inboxPowPayloadHash,
    Number(config.difficulty || 4)
  );

  const signObj = { action: "get_inbox", address: wallet.address, timestamp, limit, offset, nonce };
  const sig = await signCanonical(wallet, signObj);

  const result = await apiGet(apiUrl, `inbox/${wallet.address}`, { sig, timestamp, nonce, limit, offset });

  const messages = result.messages || [];
  console.log(`Inbox for ${sender.agentName} (${messages.length} messages)`);

  for (const msg of messages) {
    const decoded = tryDecodePayload(msg.payload);
    console.log("---");
    console.log(`ID: ${msg.message_id}`);
    console.log(`From: ${msg.from}`);
    console.log(`Encrypted: ${msg.encrypted}`);
    if (typeof decoded === "object") {
      const subject = decoded.subject || "(No Subject)";
      const body = decoded.body || "";
      console.log(`Subject: ${subject}`);
      if (body) console.log(`Body: ${body.length > 120 ? `${body.slice(0, 120)}...` : body}`);
    } else {
      const text = String(decoded);
      console.log(`Content: ${text.length > 120 ? `${text.slice(0, 120)}...` : text}`);
    }
  }
}

async function cmdAlias(args) {
  let agentName = null;
  let alias = null;

  if (args._.length >= 2) {
    agentName = args._[0];
    alias = args._[1];
  } else if (args._.length === 1 && (args["from-private-key"] || args["from-mnemonic"] || process.env.TOKENMAIL_PRIVATE_KEY || process.env.TOKENMAIL_MNEMONIC)) {
    alias = args._[0];
  }

  if (!alias) throw new Error("Usage: alias [agent] <alias> [--from-private-key 0x...]");

  const { apiUrl, keystoreDir } = getCommon(args);
  const sender = await resolveSender(args, agentName, keystoreDir);
  await registerAlias(apiUrl, sender.wallet, alias);

  if (sender.fromKeystore && sender.ks && sender.record) {
    sender.ks.saveAgent({ ...sender.record, alias });
    console.log(`Alias '${alias}' registered and saved for ${sender.wallet.address}`);
  } else {
    console.log(`Alias '${alias}' registered for ${sender.wallet.address}`);
    console.log("Note: sender key came from argument/env, no local agent file updated.");
  }
}

async function cmdExport(args) {
  const agentName = args._[0];
  if (!agentName) throw new Error("Missing agent name");

  const { keystoreDir } = getCommon(args);
  const ks = new PlainKeystore(keystoreDir);
  const data = requireAgent(ks, agentName);

  const out = JSON.stringify(data, null, 2);
  if (args.output) {
    fs.writeFileSync(String(args.output), out, "utf8");
    console.log(`Exported to: ${args.output}`);
    return;
  }
  console.log(out);
}

async function cmdDelete(args) {
  const agentName = args._[0];
  if (!agentName) throw new Error("Missing agent name");
  if (!args.force) throw new Error("Deletion requires --force");

  const { keystoreDir } = getCommon(args);
  const ks = new PlainKeystore(keystoreDir);
  if (!ks.deleteAgent(agentName)) throw new Error("Agent not found");
  console.log(`Agent '${agentName}' deleted`);
}

async function main() {
  const { command, args } = parseCli(process.argv);
  if (!command || command === "help" || command === "--help") {
    usage();
    process.exit(0);
  }

  const handlers = {
    create: cmdCreate,
    ensure: cmdEnsure,
    import: cmdImport,
    list: cmdList,
    send: cmdSend,
    "send-external": cmdSendExternal,
    inbox: cmdInbox,
    alias: cmdAlias,
    export: cmdExport,
    delete: cmdDelete
  };

  const handler = handlers[command];
  if (!handler) {
    usage();
    throw new Error(`Unknown command: ${command}`);
  }

  await handler(args);
}

main().catch((err) => {
  const msg = String(err && err.message ? err.message : err);
  console.error(`Error: ${msg}`);
  if (/EACCES|EPERM|EROFS|read-only|permission/i.test(msg)) {
    console.error("Hint: sandbox read-only mode can use --from-private-key for send/inbox/alias (no local keystore writes).");
  }
  if (/load ethers|Cannot find module 'ethers'|CDN/i.test(msg)) {
    console.error("Hint: if outbound network is blocked, preload ethers in scripts/node_modules or provide a reachable TOKENMAIL_ETHERS_URL.");
  }
  process.exit(1);
});
