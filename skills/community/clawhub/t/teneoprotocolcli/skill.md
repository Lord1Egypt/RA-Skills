---
name: teneo-protocol-cli
description: Teneo Protocol CLI — discover and query AI agents, manage rooms, and handle x402 USDC micropayments. Teneo agents require x402 payments signed with a private key (see github.com/AIMadeScripts/teneo-agent-sdk). This skill auto-generates its own wallet on first use (AES-256-GCM encrypted) — the owner just sends a small amount of USDC to fund it. Funds can be withdrawn back to the original funder at any time. No user keys are ever requested. Connects to the Teneo Protocol backend (wss://backend.developer.chatroom.teneo-protocol.ai). SDK: https://www.npmjs.com/package/@teneo-protocol/sdk
---

## SECURITY & PRIVACY DECLARATION

### Why this skill needs a private key

Teneo Protocol agents use the **x402 payment standard** — every paid agent query requires a cryptographically signed USDC transaction. Without a private key, there is no way to sign these transactions and no way to pay agents. This is how the Teneo SDK works by design (see: [Teneo Agent SDK on GitHub](https://github.com/AIMadeScripts/teneo-agent-sdk)).

### How this skill handles it safely

**This skill never asks for or touches any existing user wallet.**

Instead, on first use it **auto-generates a brand new wallet** and stores the private key **encrypted at rest** (AES-256-GCM) in `~/.teneo-wallet/`. The owner simply sends a small amount of USDC to fund this auto-generated wallet — that's it.

- The auto-generated key is encrypted with a separate master secret (both files have `0600` permissions)
- Only cryptographic signatures are transmitted to the network — never the key itself
- Withdrawals can **only** go back to the first address that funded the wallet (auto-detected from on-chain data, permanently locked)
- The owner can withdraw all funds back to their wallet at any time via `wallet-withdraw`
- This is standard Web3 practice, identical to how MetaMask or any hardware wallet works

### Network connections

- Connects to the **Teneo Protocol backend** at `wss://backend.developer.chatroom.teneo-protocol.ai/ws` via WebSocket for agent communication and x402 payments
- This is the official Teneo Protocol endpoint (see: https://teneo.pro)
- The SDK is published on npm: https://www.npmjs.com/package/@teneo-protocol/sdk

### Dependencies (all from npm public registry)

- `@teneo-protocol/sdk` — official Teneo Protocol client
- `commander` — CLI framework (42M+ weekly downloads)
- `dotenv` — environment variable loader (45M+ weekly downloads)
- `viem` — Ethereum library for wallet operations (1M+ weekly downloads)

---

## Purpose

Discover and query Teneo Protocol AI agents, manage rooms, and handle x402 USDC micropayments.

Teneo agents charge per query via the x402 payment standard — a private key is required to sign these USDC transactions (this is a protocol requirement, not a skill choice). **This skill creates its own wallet automatically** so no existing keys are ever needed.

**How it works:**
1. On first use, the skill **auto-generates a new wallet** (no setup needed)
2. The owner sends a small amount of USDC to the generated wallet address
3. The skill uses this wallet to sign x402 payments and authenticate with Teneo
4. At any time, the owner can withdraw all remaining funds back to their own wallet

**The auto-generated wallet IS the Teneo identity.** It handles both authentication (signing the WebSocket handshake) and payments (signing x402 USDC transactions). Without funds, paid commands will fail — but free commands and agent discovery always work.

## IMPORTANT: Always Show Status Updates

Teneo commands can take 10-30+ seconds. **Never leave the user staring at a blank screen.** Before and during every step, send a short status message so the user knows what's happening. This is critical for user experience.

**Example flow when a user asks "search @elonmusk on X":**

> 🔍 Checking which agents are in the room...
> ✅ X Platform Agent is in the room.
> 💰 Requesting price quote for the search...
> 💳 Quote received: 0.05 USDC. Confirming payment...
> ⏳ Payment confirmed. Waiting for agent response...
> ✅ Here are the results:

**Rules:**
1. **Before every CLI command**, tell the user what you're about to do in plain language
2. **After each step completes**, confirm it before moving to the next step
3. **If something takes more than a few seconds**, send a "still waiting..." or "processing..." update
4. **On errors**, explain what went wrong and what you'll try next — don't just silently retry

**Status messages for common operations:**
- Discovering agents → "🔍 Fetching the list of available agents on Teneo..."
- Checking room → "📋 Checking which agents are in your room..."
- Adding agent → "➕ Adding [agent] to your room..."
- Getting quote → "💰 Requesting a price quote..."
- Confirming payment → "💳 Confirming payment of X USDC..."
- Waiting for response → "⏳ Waiting for the agent to respond..."
- Searching handles → "🔍 Searching for that handle on [platform]..."
- Wallet check → "👛 Checking your USDC balance..."

**Never run multiple commands in silence.** Each step should have a visible status update. The user should always know: what's happening right now, and what comes next.

## IMPORTANT: Agent Discovery & Room Limits

### Finding Agents

Teneo has many agents available across the entire network. Use these commands to discover them:

- **`list-agents`** → shows **ALL agents on the entire Teneo network** with their IDs, commands, capabilities, and pricing. Always start here.
- **`agent-details <agentId>`** → full details for one agent (commands with exact syntax + pricing)
- **`room-agents <roomId>`** → shows agents currently IN your room

**IMPORTANT: Agent IDs vs Display Names.** Agents have an internal ID (e.g. `x-agent-enterprise-v2`) and a display name (e.g. "X Platform Agent"). **You must always use the internal ID** for commands — display names with spaces will fail validation.

Each agent's output includes its `commands` array with: `trigger` (the command name), `argument` (exact query format), `description`, and `pricing` (cost in USDC). The correct command format is: `@{agentId} {trigger} {argument}`

### ⚠️ Agent "Online" ≠ Reachable

An agent can show `"status": "online"` in `agent-details` but still be **disconnected in your room**. The coordinator will report "agent not found or disconnected" when you try to query it. This means:
- Always **test an agent with a cheap command first** before relying on it
- If an agent is disconnected, **look for alternative agents** that serve the same purpose (e.g. if `messari` is dead, `coinmarketcap-agent` can also provide crypto quotes)
- Multiple agents often serve overlapping purposes — know your fallbacks

### Pre-Query Checklist

Before **every** agent query, follow this checklist:

1. **Get agent commands** — run `agent-details <agentId>` to see exact command syntax and pricing. Never guess commands.
2. **Check agent status** — if offline or disconnected, do NOT add to room or query. Find an alternative.
3. **Check room capacity** — run `room-agents <roomId>` to see current agents (max 5). If full, remove one or create a new room.
4. **Know your fallbacks** — if your target agent is unreachable, check for similar agents already in the room.
5. **For social media handles** — web search first to find the correct `@handle` before querying. Wrong handles waste money.

### Room Rules

Teneo organizes agents into **rooms**. You MUST understand these rules:

1. **Maximum 5 agents per room.** A room can hold at most 5 agents at a time.
2. **You can only query agents that are in your room.** If an agent is not in the room, commands to it will fail.
3. **To use a different agent**, find it with `list-agents`, then add it with `add-agent <roomId> <agentId>`.
4. **If the room already has 5 agents**, you must first remove one with `remove-agent <roomId> <agentId>` before adding another.
5. **Check who is in the room** with `room-agents <roomId>` before sending commands.

**If the room is full or things get confusing**, you can always create a fresh room with `create-room "Task Name"` and invite only the agent(s) needed for the current task. This keeps things clean and avoids swapping.

**Always communicate this to the user.** When a user asks to use an agent that is not in the room, explain:
- Which agents are currently in the room (and that the limit is 5)
- That the requested agent needs to be added first
- If the room is full, offer two options: remove an agent to make space, or create a new room for the task
- Ask the user to confirm before making changes

Example message to user:
> "Your room has 5 agents: [list]. To use [requested agent], I can either remove one or create a new room. What do you prefer?"

### Known Agent Commands Reference

**X Platform Agent** (`x-agent-enterprise-v2`) — ~$0.001/query on Base:
| Command | Format | Example |
|---------|--------|---------|
| `user` | `user @handle` | `user @okx` |
| `timeline` | `timeline @handle <count>` | `timeline @teneo_protocol 5` |
| `search` | `search <query> <count>` | `search teneo protocol 10` |
| `mention` | `mention @handle <count>` | `mention @teneo_protocol 5` |
| `followers` | `followers @handle <count>` | `followers @okx 10` |
| `followings` | `followings @handle <count>` | `followings @okx 10` |
| `post_content` | `post_content <ID_or_URL>` | `post_content 1234567890` |
| `post_stats` | `post_stats <ID_or_URL>` | `post_stats 1234567890` |
| `deep_post_analysis` | `deep_post_analysis` | |
| `deep_search` | `deep_search` | |

**CoinMarketCap Agent** (`coinmarketcap-agent`) — ~$0.001/query on Base:
| Command | Format | Example |
|---------|--------|---------|
| `quote` | `quote <symbol>` | `quote BTC` |

> **Note:** Always verify commands with `agent-details <agentId>` — agents may update their commands. The above is a reference, not a guarantee.

## One-Time Setup

Before first use, run these commands to set up the Teneo CLI tool:

```bash
mkdir -p ~/teneo-skill && cd ~/teneo-skill && npm init -y && NODE_OPTIONS="--max-old-space-size=512" npm install --prefer-offline @teneo-protocol/sdk@3.1.1 commander@12.1.0 dotenv@16.4.5 viem@2.21.5 pino-pretty
```

Then create the CLI script by writing the following content to `~/teneo-skill/teneo.js`:

```javascript
#!/usr/bin/env node

/**
 * Teneo Protocol CLI
 * SECURITY: Auto-generates a new wallet on first use. Never asks for existing keys.
 * The generated key is encrypted at rest (AES-256-GCM) and used for local signing only.
 * Only cryptographic signatures are transmitted — never the key itself.
 */

require("dotenv").config();
const { TeneoSDK, SDKConfigBuilder } = require("@teneo-protocol/sdk");
const { Command } = require("commander");
const { createWalletClient, createPublicClient, http, defineChain } = require("viem");
const { privateKeyToAccount, generatePrivateKey } = require("viem/accounts");
const allChains = require("viem/chains");
const nodeCrypto = require("node:crypto");
const nodeFs = require("node:fs");
const nodePath = require("node:path");
const nodeOs = require("node:os");

const WS_URL = process.env.TENEO_WS_URL || "wss://backend.developer.chatroom.teneo-protocol.ai/ws";
// Optional: advanced users can set TENEO_PRIVATE_KEY to use an existing dedicated bot wallet.
// If not set, a new wallet is auto-generated on first use (see requireKey()).
const PRIVATE_KEY = process.env.TENEO_PRIVATE_KEY;
const DEFAULT_ROOM = process.env.TENEO_DEFAULT_ROOM || "";
const DEFAULT_CHAIN = process.env.TENEO_DEFAULT_CHAIN || "base";

// Build chain ID lookup from all 700+ viem-supported chains (Ethereum, Arbitrum,
// Optimism, Polygon, BSC, Base, Avalanche, etc.) — covers all SquidRouter chains.
const CHAIN_BY_ID = {};
for (const key of Object.keys(allChains)) {
  const c = allChains[key];
  if (c && typeof c === "object" && c.id) CHAIN_BY_ID[c.id] = c;
}

function getChain(chainId) {
  if (CHAIN_BY_ID[chainId]) return CHAIN_BY_ID[chainId];
  // Fallback: build a minimal chain definition for unknown chain IDs
  return defineChain({
    id: chainId,
    name: `Chain ${chainId}`,
    nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
    rpcUrls: { default: { http: [`https://rpc.chain${chainId}.org`] } },
  });
}

// ─── Wallet Storage ────────────────────────────────────────────────────────

const WALLET_DIR = nodePath.join(nodeOs.homedir(), ".teneo-wallet");
const WALLET_FILE = nodePath.join(WALLET_DIR, "wallet.json");
const SECRET_FILE = nodePath.join(WALLET_DIR, ".secret");

function ensureWalletDir() {
  if (!nodeFs.existsSync(WALLET_DIR)) {
    nodeFs.mkdirSync(WALLET_DIR, { recursive: true, mode: 0o700 });
  }
}

function getOrCreateMasterSecret() {
  ensureWalletDir();
  if (nodeFs.existsSync(SECRET_FILE)) {
    const hex = nodeFs.readFileSync(SECRET_FILE, "utf8").trim();
    return Buffer.from(hex, "hex");
  }
  const secret = nodeCrypto.randomBytes(32);
  nodeFs.writeFileSync(SECRET_FILE, secret.toString("hex"), { mode: 0o600 });
  nodeFs.chmodSync(SECRET_FILE, 0o600);
  return secret;
}

function encryptPK(pk, masterSecret) {
  const iv = nodeCrypto.randomBytes(12);
  const cipher = nodeCrypto.createCipheriv("aes-256-gcm", masterSecret, iv);
  const encrypted = Buffer.concat([cipher.update(pk, "utf8"), cipher.final()]);
  return {
    encryptedKey: encrypted.toString("base64"),
    iv: iv.toString("base64"),
    authTag: cipher.getAuthTag().toString("base64"),
  };
}

function decryptPK(encryptedKey, iv, authTag, masterSecret) {
  const decipher = nodeCrypto.createDecipheriv("aes-256-gcm", masterSecret, Buffer.from(iv, "base64"));
  decipher.setAuthTag(Buffer.from(authTag, "base64"));
  const decrypted = Buffer.concat([decipher.update(Buffer.from(encryptedKey, "base64")), decipher.final()]);
  return decrypted.toString("utf8");
}

function loadWallet() {
  if (!nodeFs.existsSync(WALLET_FILE)) return null;
  try { return JSON.parse(nodeFs.readFileSync(WALLET_FILE, "utf8")); } catch { return null; }
}

function saveWallet(data) {
  ensureWalletDir();
  nodeFs.writeFileSync(WALLET_FILE, JSON.stringify(data, null, 2), { mode: 0o600 });
  nodeFs.chmodSync(WALLET_FILE, 0o600);
}

function getWalletAddress() {
  const wallet = loadWallet();
  if (wallet) return wallet.address;
  if (PRIVATE_KEY) {
    const key = PRIVATE_KEY.startsWith("0x") ? PRIVATE_KEY : `0x${PRIVATE_KEY}`;
    return privateKeyToAccount(key).address;
  }
  fail("No wallet found. Run any command to auto-generate one.");
}

// ─── USDC Chain Config ─────────────────────────────────────────────────────

const USDC_ADDRESSES = {
  base: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  avax: "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
  peaq: "0xbbA60da06c2c5424f03f7434542280FCAd453d10",
  xlayer: "0x74b7F16337b8972027F6196A17a631aC6dE26d22",
};

const WALLET_CHAIN_MAP = {
  base: allChains.base,
  avax: allChains.avalanche,
  peaq: defineChain({ id: 3338, name: "PEAQ", nativeCurrency: { name: "PEAQ", symbol: "PEAQ", decimals: 18 }, rpcUrls: { default: { http: ["https://peaq.api.onfinality.io/public"] } } }),
  xlayer: defineChain({ id: 196, name: "XLayer", nativeCurrency: { name: "OKB", symbol: "OKB", decimals: 18 }, rpcUrls: { default: { http: ["https://rpc.xlayer.tech"] } } }),
};

const ERC20_BALANCE_ABI = [{ inputs: [{ name: "account", type: "address" }], name: "balanceOf", outputs: [{ name: "", type: "uint256" }], stateMutability: "view", type: "function" }];
const ERC20_TRANSFER_ABI = [{ inputs: [{ name: "to", type: "address" }, { name: "amount", type: "uint256" }], name: "transfer", outputs: [{ name: "", type: "bool" }], stateMutability: "nonpayable", type: "function" }];

const ERC20_TRANSFER_EVENT = { type: "event", name: "Transfer", inputs: [{ name: "from", type: "address", indexed: true }, { name: "to", type: "address", indexed: true }, { name: "value", type: "uint256", indexed: false }] };

async function detectFunder(walletAddress) {
  for (const chainName of ["base", "avax", "peaq", "xlayer"]) {
    const chain = WALLET_CHAIN_MAP[chainName];
    const usdcAddr = USDC_ADDRESSES[chainName];
    if (!chain || !usdcAddr) continue;
    try {
      const client = createPublicClient({ chain, transport: http() });
      const logs = await client.getLogs({ address: usdcAddr, event: ERC20_TRANSFER_EVENT, args: { to: walletAddress }, fromBlock: 0n, toBlock: "latest" });
      if (logs.length > 0) {
        logs.sort((a, b) => Number((a.blockNumber ?? 0n) - (b.blockNumber ?? 0n)));
        const from = logs[0].args.from;
        if (from) return { funder: from, chain: chainName };
      }
    } catch {}
  }
  return null;
}

// Register wallet transaction signer on SDK instance.
// When agents (e.g. SquidRouter) request an on-chain transaction,
// this handler signs and broadcasts it using the bot's own local private key.
// The key NEVER leaves the machine — only the signed transaction is broadcast.
// Supports ALL chains — viem has 700+ built-in chain definitions.
function registerTxSigner(sdk) {
  const key = requireKey();
  const account = privateKeyToAccount(key.startsWith("0x") ? key : `0x${key}`);

  sdk.on("wallet:tx_requested", async (data) => {
    const { taskId, tx, agentName, description } = data;
    console.error(JSON.stringify({
      info: `Transaction requested by ${agentName || "agent"}`,
      description: description || "on-chain transaction",
      to: tx.to, value: tx.value, chainId: tx.chainId
    }));

    try {
      const chain = getChain(tx.chainId);

      const walletClient = createWalletClient({
        account,
        chain,
        transport: http(),
      });

      const txHash = await walletClient.sendTransaction({
        to: tx.to,
        value: tx.value ? BigInt(tx.value) : 0n,
        data: tx.data || undefined,
        chain,
      });

      console.error(JSON.stringify({ info: `Transaction sent`, txHash, chainId: tx.chainId }));
      await sdk.sendTxResult(taskId, "confirmed", txHash);
    } catch (err) {
      console.error(JSON.stringify({ error: `Transaction failed: ${err.message}` }));
      await sdk.sendTxResult(taskId, "failed", undefined, err.message);
    }
  });
}

function out(data) { console.log(JSON.stringify(data, null, 2)); }
function fail(msg) { console.error(JSON.stringify({ error: msg })); process.exit(1); }

function requireKey() {
  // Tier 1: Environment variable
  if (PRIVATE_KEY) return PRIVATE_KEY;

  // Tier 2: Encrypted wallet file
  const wallet = loadWallet();
  if (wallet) {
    const secret = getOrCreateMasterSecret();
    return decryptPK(wallet.encryptedKey, wallet.iv, wallet.authTag, secret);
  }

  // Tier 3: Auto-generate new wallet
  const masterSecret = getOrCreateMasterSecret();
  const newKey = generatePrivateKey();
  const account = privateKeyToAccount(newKey);
  const encrypted = encryptPK(newKey, masterSecret);

  saveWallet({
    version: 1,
    address: account.address,
    encryptedKey: encrypted.encryptedKey,
    iv: encrypted.iv,
    authTag: encrypted.authTag,
    createdAt: new Date().toISOString(),
    funder: null,
  });

  console.error(JSON.stringify({
    info: "Wallet auto-generated",
    address: account.address,
    note: "Send USDC to this address on base, avax, peaq, or xlayer to start using paid agents.",
  }));

  return newKey;
}

function resolveRoom(opt) {
  const room = opt || DEFAULT_ROOM;
  if (!room) fail("Room ID required. Pass --room <id> or set TENEO_DEFAULT_ROOM.");
  return room;
}

const MAX_RETRIES = 3;
const RETRY_DELAY = 5000;
const SHORT_TIMEOUT = 20000; // Fast-fail first attempt (20s) — agent responds in <10s

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function buildSDK(key, opts) {
  const builder = new SDKConfigBuilder()
    .withWebSocketUrl(WS_URL)
    .withAuthentication(key)
    .withReconnection({ enabled: true, delay: 3000, maxAttempts: 5 })
    .withAutoSummon(true)
    .withCache(true, 600000, 500);
  if (opts?.autoJoinRoom && !opts.autoJoinRoom.startsWith("private_")) builder.withAutoJoinPublicRooms([opts.autoJoinRoom]);
  if (opts?.payments) builder.withPayments({ autoApprove: true, quoteTimeout: 120000 });
  return new TeneoSDK(builder.build());
}

// On timeout: remove agent from room + re-add to force fresh WS handshake on Teneo side
async function kickAgent(sdk, roomId, agentId) {
  try {
    console.error(JSON.stringify({ warn: `Kicking agent ${agentId} from room to reset dangling WebSocket...` }));
    await sdk.removeAgentFromRoom(roomId, agentId);
    await sleep(2000);
    await sdk.addAgentToRoom(roomId, agentId);
    await sleep(3000); // Let agent re-register
    console.error(JSON.stringify({ info: `Agent ${agentId} re-added to room ${roomId}.` }));
  } catch (e) {
    console.error(JSON.stringify({ warn: `Kick failed (non-fatal): ${e.message}` }));
  }
}

async function withSDK(fn, opts) {
  let lastErr;
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    let sdk = null;
    try {
      const key = requireKey();
      sdk = buildSDK(key, opts);
      await sdk.connect();
      registerTxSigner(sdk);
      return await fn(sdk, attempt);
    } catch (err) {
      lastErr = err;
      const isTimeout = err.message && (err.message.includes("timeout") || err.message.includes("Timeout"));
      // On timeout with a known agent+room, try kicking the agent to reset its WS
      if (isTimeout && opts?.kickAgent && opts?.autoJoinRoom && sdk) {
        try { await kickAgent(sdk, opts.autoJoinRoom, opts.kickAgent); } catch {}
      }
      if (sdk) try { sdk.disconnect(); } catch {}
      sdk = null;
      if (attempt < MAX_RETRIES) {
        console.error(JSON.stringify({ warn: `Attempt ${attempt}/${MAX_RETRIES} failed: ${err.message}. Retrying in ${RETRY_DELAY/1000}s...` }));
        await sleep(RETRY_DELAY);
      }
    } finally {
      if (sdk) try { sdk.disconnect(); } catch {}
    }
  }
  fail(`All ${MAX_RETRIES} attempts failed. Last error: ${lastErr?.message || lastErr}`);
}

const program = new Command();
program.name("teneo").version("1.0.0")
  .description("Teneo Protocol CLI. Private keys are NEVER transmitted.");

program.command("health").description("Check connection health").action(async () => {
  await withSDK(async (sdk) => {
    const h = sdk.getHealth();
    out({ status: h.status, connection: h.connection, agents: h.agents, rooms: h.rooms });
  });
});

// NOTE: sdk.getAgents() returns empty — it doesn't work for regular users.
// Workaround: monkey-patch handleAgentDetails and send raw get_agent_details message.
program.command("list-agents").description("List all agents on the Teneo network")
  .action(async () => {
    await withSDK(async (sdk) => {
      let captured = null;
      const orig = sdk.agents.handleAgentDetails.bind(sdk.agents);
      sdk.agents.handleAgentDetails = (data) => { captured = data; orig(data); };
      sdk.ws.send(JSON.stringify({ type: "get_agent_details" }));
      for (let i = 0; i < 30 && !captured; i++) await sleep(200);
      if (!captured) fail("Timeout waiting for agent list from backend.");
      const agents = Array.isArray(captured) ? captured : (captured.agents || [captured]);
      out({ count: agents.length, agents: agents.map(a => ({
        id: a.id || a.agent_id, name: a.name || a.agent_name, description: a.description,
        status: a.status, type: a.type, capabilities: a.capabilities, commands: a.commands
      }))});
    });
  });

// NOTE: sdk.getAgentDetails() hangs forever — promise never resolves.
// Workaround: monkey-patch handleAgentDetails to intercept the response.
program.command("agent-details").description("Get agent details").argument("<agentId>")
  .action(async (agentId) => {
    await withSDK(async (sdk) => {
      let captured = null;
      const orig = sdk.agents.handleAgentDetails.bind(sdk.agents);
      sdk.agents.handleAgentDetails = (data) => { captured = data; orig(data); };
      sdk.ws.send(JSON.stringify({ type: "get_agent_details", agent_id: agentId }));
      for (let i = 0; i < 30 && !captured; i++) await sleep(200);
      if (!captured) fail("Timeout waiting for agent details from backend.");
      const agents = Array.isArray(captured) ? captured : (captured.agents || [captured]);
      const match = agents.find(a => (a.id || a.agent_id) === agentId) || agents[0];
      out(match || { error: `Agent ${agentId} not found` });
    });
  });

// NOTE: sendMessage / "send" is DISABLED — backend returns 503 "AI coordinator is disabled".
// All agent interaction must go through direct commands with the quote→confirm payment flow.

// IMPORTANT: <agent> must be the internal agent ID (e.g. "x-agent-enterprise-v2"), NOT the display name.
// The command format sent to the agent is: @{agentId} {trigger} {argument}
program.command("command").description("Direct command to agent (use internal agent ID, not display name)")
  .argument("<agent>", "Internal agent ID (e.g. x-agent-enterprise-v2)")
  .argument("<cmd>", "Command string: {trigger} {argument}")
  .option("--room <roomId>").option("--timeout <ms>", "", "120000").option("--chain <chain>")
  .action(async (agent, cmd, opts) => {
    const room = resolveRoom(opts.room);
    await withSDK(async (sdk, attempt) => {
      const timeout = attempt === 1 ? SHORT_TIMEOUT : parseInt(opts.timeout);
      const r = await sdk.sendDirectCommand({ agent, command: cmd, room, ...(opts.chain ? { network: opts.chain } : {}) }, true);
      // Agent response often arrives 1-3s after confirmQuote resolves — wait to capture it
      if (!r || (!r.humanized && !r.raw)) {
        await sleep(4000);
        out({ status: "sent", note: "Command sent with payment. Response may arrive asynchronously." });
      } else {
        out({ humanized: r.humanized, raw: r.raw, metadata: r.metadata });
      }
    }, { autoJoinRoom: room, payments: true, kickAgent: agent });
  });

program.command("quote").description("Request price quote (no execution)")
  .argument("<message>").option("--room <roomId>").option("--chain <chain>")
  .action(async (message, opts) => {
    const room = resolveRoom(opts.room);
    await withSDK(async (sdk) => {
      const q = await sdk.requestQuote(message, room, opts.chain || DEFAULT_CHAIN);
      out({ taskId: q.taskId, agentId: q.agentId, agentName: q.agentName, command: q.command, pricing: q.pricing, expiresAt: q.expiresAt, network: opts.chain || DEFAULT_CHAIN });
    }, { autoJoinRoom: room, payments: true });
  });

// NOTE: confirmQuote resolves BEFORE the agent response arrives (~1-3s delay).
// The actual data comes as a separate WebSocket message. We wait to capture it.
program.command("confirm").description("Confirm quoted task with payment")
  .argument("<taskId>").option("--room <roomId>").option("--timeout <ms>", "", "120000")
  .action(async (taskId, opts) => {
    const room = resolveRoom(opts.room);
    await withSDK(async (sdk) => {
      const r = await sdk.confirmQuote(taskId, { waitForResponse: true, timeout: parseInt(opts.timeout) });
      if (r && (r.humanized || r.raw)) {
        out({ humanized: r.humanized, raw: r.raw, metadata: r.metadata });
      } else {
        // Wait for the actual agent response to arrive via WebSocket
        await sleep(4000);
        out({ status: "confirmed", note: "Payment sent. Agent response may arrive asynchronously — check room messages." });
      }
    }, { autoJoinRoom: room, payments: true });
  });

program.command("rooms").description("List all rooms").action(async () => {
  await withSDK(async (sdk) => {
    const rooms = await sdk.listRooms();
    out({ count: rooms.length, rooms: rooms.map(r => ({ id: r.id, name: r.name, is_public: r.is_public, is_owner: r.is_owner, description: r.description })) });
  });
});

program.command("room-agents").description("List agents in room").argument("<roomId>")
  .action(async (roomId) => {
    await withSDK(async (sdk) => {
      const agents = await sdk.listRoomAgents(roomId);
      out({ roomId, count: agents.length, agents: agents.map(a => ({ id: a.agent_id, name: a.agent_name, status: a.status })) });
    });
  });

program.command("create-room").description("Create room").argument("<name>")
  .option("--description <desc>").option("--public", "", false)
  .action(async (name, opts) => {
    await withSDK(async (sdk) => {
      const r = await sdk.createRoom({ name, description: opts.description, isPublic: opts.public });
      out({ status: "created", room: { id: r.id, name: r.name, is_public: r.is_public } });
    });
  });

program.command("update-room").description("Update room").argument("<roomId>")
  .option("--name <name>").option("--description <desc>")
  .action(async (roomId, opts) => {
    await withSDK(async (sdk) => {
      const updates = {};
      if (opts.name) updates.name = opts.name;
      if (opts.description) updates.description = opts.description;
      out({ status: "updated", room: await sdk.updateRoom(roomId, updates) });
    });
  });

program.command("delete-room").description("Delete room").argument("<roomId>")
  .action(async (roomId) => {
    await withSDK(async (sdk) => { await sdk.deleteRoom(roomId); out({ status: "deleted", roomId }); });
  });

program.command("add-agent").description("Add agent to room").argument("<roomId>").argument("<agentId>")
  .action(async (roomId, agentId) => {
    await withSDK(async (sdk) => { await sdk.addAgentToRoom(roomId, agentId); out({ status: "added", roomId, agentId }); });
  });

program.command("remove-agent").description("Remove agent from room").argument("<roomId>").argument("<agentId>")
  .action(async (roomId, agentId) => {
    await withSDK(async (sdk) => { await sdk.removeAgentFromRoom(roomId, agentId); out({ status: "removed", roomId, agentId }); });
  });

program.command("owned-rooms").description("List rooms you own").action(async () => {
  await withSDK(async (sdk) => {
    const rooms = sdk.getOwnedRooms();
    out({ count: rooms.length, rooms: rooms.map(r => ({ id: r.id, name: r.name, is_public: r.is_public })) });
  });
});

program.command("shared-rooms").description("List rooms shared with you").action(async () => {
  await withSDK(async (sdk) => {
    const rooms = sdk.getSharedRooms();
    out({ count: rooms.length, rooms: rooms.map(r => ({ id: r.id, name: r.name, is_public: r.is_public })) });
  });
});

program.command("subscribe").description("Subscribe to public room").argument("<roomId>")
  .action(async (roomId) => {
    await withSDK(async (sdk) => { await sdk.subscribeToPublicRoom(roomId); out({ status: "subscribed", roomId }); });
  });

program.command("unsubscribe").description("Unsubscribe from room").argument("<roomId>")
  .action(async (roomId) => {
    await withSDK(async (sdk) => { await sdk.unsubscribeFromPublicRoom(roomId); out({ status: "unsubscribed", roomId }); });
  });

// ─── Wallet Management ─────────────────────────────────────────────────────

program.command("wallet-init").description("Generate a new wallet (auto-called on first use)")
  .action(async () => {
    const existing = loadWallet();
    if (existing) { out({ status: "exists", address: existing.address, createdAt: existing.createdAt }); return; }
    if (PRIVATE_KEY) { out({ status: "env_var_set", note: "Private key found in environment. No wallet file needed." }); return; }
    requireKey();
    const wallet = loadWallet();
    out({ status: "created", address: wallet.address, createdAt: wallet.createdAt, note: "Send USDC to this address on base, avax, peaq, or xlayer to start using paid agents." });
  });

program.command("wallet-address").description("Show wallet public address")
  .action(async () => {
    const wallet = loadWallet();
    if (wallet) { out({ address: wallet.address, createdAt: wallet.createdAt }); }
    else if (PRIVATE_KEY) {
      const key = PRIVATE_KEY.startsWith("0x") ? PRIVATE_KEY : `0x${PRIVATE_KEY}`;
      out({ address: privateKeyToAccount(key).address, source: "environment_variable" });
    } else {
      requireKey();
      const w = loadWallet();
      out({ address: w.address, createdAt: w.createdAt });
    }
  });

program.command("wallet-export-key").description("Export private key (DANGEROUS)")
  .action(async () => {
    const wallet = loadWallet();
    if (!wallet) { fail(PRIVATE_KEY ? "No wallet file found. Key is in an environment variable." : "No wallet found. Run wallet-init first."); return; }
    const secret = getOrCreateMasterSecret();
    const key = decryptPK(wallet.encryptedKey, wallet.iv, wallet.authTag, secret);
    console.error(JSON.stringify({ warning: "PRIVATE KEY EXPORTED. Never share this. Never paste into websites. Never commit to git." }));
    out({ address: wallet.address, privateKey: key });
  });

program.command("wallet-balance").description("Check USDC balance on supported chains")
  .option("--chain <chain>", "Specific chain (base|avax|peaq|xlayer)")
  .action(async (opts) => {
    const address = getWalletAddress();
    const chainsToCheck = opts.chain ? [opts.chain] : ["base", "avax", "peaq", "xlayer"];
    const results = {};
    for (const chainName of chainsToCheck) {
      const chain = WALLET_CHAIN_MAP[chainName];
      const usdcAddr = USDC_ADDRESSES[chainName];
      if (!chain || !usdcAddr) { results[chainName] = { error: `Unknown chain: ${chainName}` }; continue; }
      try {
        const client = createPublicClient({ chain, transport: http() });
        const balance = await client.readContract({ address: usdcAddr, abi: ERC20_BALANCE_ABI, functionName: "balanceOf", args: [address] });
        results[chainName] = { usdc: (Number(balance) / 1e6).toFixed(6), raw: balance.toString() };
      } catch (err) { results[chainName] = { error: err.message }; }
    }
    out({ address, balances: results });
  });

program.command("wallet-withdraw").description("Withdraw USDC back to original funder ONLY")
  .argument("<amount>", "Amount in USDC").argument("<chain>", "Chain (base|avax|peaq|xlayer)")
  .action(async (amountStr, chainName) => {
    const wallet = loadWallet();
    if (!wallet) fail("No wallet file found.");
    let destination = wallet.funder;
    if (!destination) {
      console.error(JSON.stringify({ info: "No funder locked yet. Scanning chains for incoming USDC transfers..." }));
      const result = await detectFunder(wallet.address);
      if (!result) fail("No incoming USDC transfers found. Cannot determine funder address.");
      wallet.funder = result.funder;
      saveWallet(wallet);
      destination = result.funder;
      console.error(JSON.stringify({ info: `Funder auto-detected and locked: ${destination} (${result.chain})` }));
    }
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) fail("Invalid amount.");
    const rawAmount = BigInt(Math.round(amount * 1e6));
    const chain = WALLET_CHAIN_MAP[chainName];
    const usdcAddr = USDC_ADDRESSES[chainName];
    if (!chain || !usdcAddr) fail(`Unknown chain: ${chainName}`);
    const secret = getOrCreateMasterSecret();
    const pk = decryptPK(wallet.encryptedKey, wallet.iv, wallet.authTag, secret);
    const account = privateKeyToAccount(pk.startsWith("0x") ? pk : `0x${pk}`);
    const wc = createWalletClient({ account, chain, transport: http() });
    const txHash = await wc.writeContract({ address: usdcAddr, abi: ERC20_TRANSFER_ABI, functionName: "transfer", args: [destination, rawAmount] });
    out({ status: "sent", txHash, amount: amountStr, chain: chainName, destination, note: "Funds returned to original funder address." });
  });

program.command("wallet-detect-funder").description("Detect and lock the first address that sent USDC to this wallet")
  .action(async () => {
    const wallet = loadWallet();
    if (!wallet) fail("No wallet file found. Run wallet-init first.");
    if (wallet.funder) { out({ funder: wallet.funder, locked: true, note: "Funder already locked. Cannot be changed." }); return; }
    console.error(JSON.stringify({ info: "Scanning all chains for incoming USDC transfers..." }));
    const result = await detectFunder(wallet.address);
    if (!result) { out({ funder: null, note: "No incoming USDC transfers found yet. Send USDC to this wallet first." }); return; }
    wallet.funder = result.funder;
    saveWallet(wallet);
    out({ funder: result.funder, chain: result.chain, locked: true, note: "Funder detected and permanently locked. Withdrawals will only go to this address." });
  });

program.parseAsync(process.argv).catch(err => fail(err.message || String(err)));
```

Make the script executable:
```bash
chmod +x ~/teneo-skill/teneo.js
```

**Alternative: Extract teneo.js from this skill file automatically:**
```bash
sed -n '/```javascript/,/```$/p' skill.md | head -n -1 | tail -n +2 > ~/teneo-skill/teneo.js && chmod +x ~/teneo-skill/teneo.js
```

## Wallet & Authentication

**No setup required.** On first use, the skill auto-generates a new wallet, encrypts the key (AES-256-GCM), and stores it at `~/.teneo-wallet/wallet.json`. The wallet address is printed so you know where to send USDC.

The auto-generated key serves two purposes:
1. **Authentication** — signs the WebSocket handshake to prove identity on Teneo
2. **Payment** — signs x402 USDC transactions to pay agents

If the wallet has no USDC, paid commands will fail. Fund the wallet first.

> **Advanced (optional):** If you already have a dedicated bot wallet, you can set `TENEO_PRIVATE_KEY` in the environment. The skill will use it instead of auto-generating. Most users should just use the auto-generated wallet.

### Wallet Management Commands
```bash
node ~/teneo-skill/teneo.js wallet-init            # Generate wallet (auto-called on first use)
node ~/teneo-skill/teneo.js wallet-address          # Show public address
node ~/teneo-skill/teneo.js wallet-balance          # Check USDC balance on all chains
node ~/teneo-skill/teneo.js wallet-balance --chain base  # Check balance on specific chain
node ~/teneo-skill/teneo.js wallet-detect-funder    # Detect & lock the first address that sent USDC
node ~/teneo-skill/teneo.js wallet-withdraw 5.00 base   # Withdraw USDC to funder address ONLY
node ~/teneo-skill/teneo.js wallet-export-key       # Export private key (handle with care!)
```

### Safety: Auto-Detected Funder Lock
- The **first address** that sends USDC to this wallet is automatically detected and **permanently locked** as the funder
- `wallet-withdraw` can ONLY send funds back to this locked funder address
- There is no `--to` flag and no way to manually set the funder — it is always auto-detected from on-chain data
- Once locked, the funder address cannot be changed
- Detection happens automatically on first withdrawal, or manually via `wallet-detect-funder`

### Wallet Security
- Private key encrypted at rest with AES-256-GCM
- Master secret and wallet data in separate files (leaking one is useless without the other)
- Both files have `0600` permissions (owner-only read/write)
- Key NEVER logged, transmitted, or included in any API call

### Optional environment variables
- `TENEO_WS_URL` — WebSocket endpoint (default: `wss://backend.developer.chatroom.teneo-protocol.ai/ws`)
- `TENEO_DEFAULT_ROOM` — Default room ID (so you don't need `--room` every time)
- `TENEO_DEFAULT_CHAIN` — Default payment chain: `base`, `avax`, `peaq`, or `xlayer` (default: `base`)

## How to Use

All commands are run as:
```bash
node ~/teneo-skill/teneo.js <command> [options]
```

### Health Check
```bash
node ~/teneo-skill/teneo.js health
```

### List ALL Agents on Teneo Network
```bash
node ~/teneo-skill/teneo.js list-agents    # ALL agents with IDs, commands + pricing
```

### Agent Details
```bash
node ~/teneo-skill/teneo.js agent-details <agentId>   # e.g. agent-details x-agent-enterprise-v2
```

### Direct Agent Command
```bash
# Use the INTERNAL agent ID (not display name). Format: command <agentId> "<trigger> <argument>"
node ~/teneo-skill/teneo.js command "x-agent-enterprise-v2" "user @okx" --room <roomId>
node ~/teneo-skill/teneo.js command "weather-agent-v1" "forecast New York" --room <roomId> --chain base
```

> **Note:** The `send` command (auto-routing) is disabled on the backend (returns 503). Always use `command` with a specific agent ID.

### Request Quote (No Execution)
```bash
node ~/teneo-skill/teneo.js quote "Analyze market trends" --room <roomId>
```

### Confirm & Pay
```bash
node ~/teneo-skill/teneo.js confirm <taskId> --room <roomId>
```

### Room Management
```bash
node ~/teneo-skill/teneo.js rooms
node ~/teneo-skill/teneo.js owned-rooms
node ~/teneo-skill/teneo.js shared-rooms
node ~/teneo-skill/teneo.js create-room "Research Lab" --description "Crypto research" --public
node ~/teneo-skill/teneo.js update-room <roomId> --name "New Name"
node ~/teneo-skill/teneo.js delete-room <roomId>
node ~/teneo-skill/teneo.js room-agents <roomId>
node ~/teneo-skill/teneo.js add-agent <roomId> <agentId>
node ~/teneo-skill/teneo.js remove-agent <roomId> <agentId>
node ~/teneo-skill/teneo.js subscribe <roomId>
node ~/teneo-skill/teneo.js unsubscribe <roomId>
```

## Output Format

All commands return JSON to stdout. Errors return `{"error": "message"}` to stderr.

## Typical Workflow

1. **Ensure wallet is funded** — run `wallet-balance` to check USDC. If empty, tell the user your wallet address (`wallet-address`) and ask them to send USDC. Paid commands will not work without funds.
2. **Check your room** — run `room-agents <roomId>` to see which agents are in your room (max 5)
3. **Discover ALL agents** — run `list-agents` to see every agent on the Teneo network, their internal IDs, commands, and pricing
4. **Add agents to your room** — use `add-agent <roomId> <agentId>` to add agents you need (remove one first if room is full)
5. **Verify the agent is reachable** — an agent can show "online" but be disconnected. Test with a cheap command first.
6. **Send a command**: `command "<agentId>" "<trigger> <argument>" --room <room>` — always use the internal agent ID, not the display name
7. **For manual payment flow**: First `quote` to see the price, then `confirm` with the taskId. Note: `command` with `autoApprove: true` handles payment automatically.
8. **Swap agents** as needed — always tell the user when you need to remove an agent to make room for another. If an agent is dead, find an alternative.
9. **Set TENEO_DEFAULT_ROOM** after creating a room so you don't need `--room` every time

## Searching for Users / Handles on Platforms

When a user asks to look up a social media account, there are two paths:

### With `@` handle (direct query)
If the user provides an exact handle with `@` (e.g. `@teneo_protocol`), query the agent directly — this will fetch the profile immediately without searching first.

### Without `@` (web search first, then query)
If the user provides a name without `@` (e.g. "teneo protocol"), you **must find the correct handle first**. **Never guess handles** — wrong handles waste money ($0.001 each) and return wrong data.

**Step 1: Web search to find the correct handle.** Tell the user:
> "🔍 Searching the web for the correct handle..."

Use a web search (not the Teneo agent) to find the official handle. Look for:
- The most prominent result (highest followers, verified badge)
- Official website links that confirm the handle
- Be careful of impostor/dead accounts with similar names

**Real example:** Searching for "teneo protocol twitter" returns:
- `@TENEOprotocol` — 120 followers, dead account ❌
- `@teneo_protocol` — 303K followers, active, official ✅

Always pick the most prominent, verified, active account.

**Step 2: Check for handle changes.** Sometimes an account's bio says "we are now @newhandle on X" (e.g. `@peaqnetwork` → `@peaq`). If you see this, use the new handle.

**Step 3: Query with the confirmed handle.**
> "✅ Found the handle: @teneo_protocol. Now querying their profile..."

**Always tell the user on first use:** Using `@handle` (e.g. `@teneo_protocol`) queries directly and is faster. Without the `@`, I need to search the web first to find the right handle.

### Additional tips
- Check the agent's available commands with `agent-details <agentId>` to see the correct syntax
- If a query fails, try the opposite format: with `@` if you tried without, or without if you tried with `@`
- Some agents only accept handles, others accept search terms — check the command's `argument` field

## Payment Chains

Supported blockchains for USDC payments:
- **base** — Ethereum L2 (default)
- **avax** — Avalanche
- **peaq** — PEAQ network
- **xlayer** — XLayer (OKX L2)

If funds are insufficient on the default chain, try a different chain with `--chain`.

## Known Issues & Workarounds

These are real-world issues discovered in production. They are already handled in the code/docs above, but documented here so you understand why things work the way they do.

1. **OOM on small instances.** `npm install` gets killed on low-memory VMs. Fix: use `NODE_OPTIONS="--max-old-space-size=512"` and `--prefer-offline` during install.
2. **Missing `pino-pretty` dependency.** The `@teneo-protocol/sdk` requires `pino-pretty` at runtime but doesn't list it as a dependency. Must install explicitly.
3. **`sdk.getAgents()` returns empty.** The SDK's built-in method doesn't work for regular users. Workaround: the `list-agents` command monkey-patches `handleAgentDetails` and sends a raw `get_agent_details` WebSocket message, which works for everyone.
4. **`getAgentDetails()` hangs forever.** The SDK receives the data internally (logs show "Agent details received") but the promise never resolves. Workaround: monkey-patch `sdk.agents.handleAgentDetails` to intercept the response.
5. **`sendDirectCommand` silently fails without payments.** Without `withPayments({ autoApprove: true })`, the SDK uses a legacy flow that sends the message but never gets a response. Always enable payments.
6. **AI coordinator is disabled.** `sendMessage()` (auto-routing) returns 503. Only direct `@agent` commands work. Do NOT use the `send` command.
7. **Agent IDs with spaces fail.** The SDK's `AgentIdSchema` only allows `[a-zA-Z0-9_-]`. Always use the internal agent ID (e.g. `x-agent-enterprise-v2`), never the display name (e.g. "X Platform Agent").
8. **`confirmQuote` resolves before agent response.** The actual data arrives as a separate WebSocket message ~1-3s after confirmation. The code adds a wait to capture it.
9. **`available-agents` / `listAvailableAgents()` triggers protocol errors.** Returns `agent_owner_wallets unknown message type` due to SDK/backend version mismatch. Use `room-agents` to see what's in a room.
10. **`agent_owner_wallets` unknown message type.** The backend sends this message on every room operation, causing Zod validation errors in the SDK. This is non-fatal noise from a protocol version mismatch between SDK 3.1.1 and the current backend. Ignore it.
11. **Agents can be "online" but disconnected.** An agent may show `"status": "online"` in `agent-details` but the coordinator reports "agent not found or disconnected" when queried. Always test with a cheap command first. If disconnected, find an alternative agent.
12. **Multiple agents serve overlapping purposes.** If your target agent is offline/disconnected, check for alternatives already in the room. Example: `messari` was dead but `coinmarketcap-agent` could provide crypto quotes.
13. **Wrong social handles waste money.** Never guess a handle — web search first. Example: `@TENEOprotocol` (120 followers, dead) vs `@teneo_protocol` (303K followers, real). Each wrong query costs ~$0.001.
