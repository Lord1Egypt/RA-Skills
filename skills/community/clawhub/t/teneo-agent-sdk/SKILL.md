---
name: teneo-protocol-cli
version: 2.0.0
description: "Teneo Protocol CLI — discover and query 400+ AI agents on the Teneo Protocol network. Manage rooms, handle x402 USDC micropayments, and auto-generate encrypted wallets. Use this skill when the user needs real-time data from specialized agents (social media profiles, hotel search, crypto prices, gas fees, Amazon products, news) or when composing multi-agent workflows."
homepage: https://teneo-protocol.ai
metadata: {"teneo":{"backend":"wss://backend.developer.chatroom.teneo-protocol.ai/ws","sdk":"https://www.npmjs.com/package/@teneo-protocol/sdk","chains":["base:8453","peaq:3338","avalanche:43114","xlayer:196"],"payment":"x402-usdc"}}
---

# teneo-protocol-cli — CLI Gateway for the Teneo Agent Network

## What This Skill Teaches You

This skill enables you to **consume** AI agents on the Teneo Protocol network. You will learn to:

1. **Discover** every available agent, their commands, pricing, and capabilities
2. **Inspect** any agent's full command interface, parameters, and billing model
3. **Query** agents directly — free agents auto-confirm, paid agents auto-pay via x402 USDC micropayments
4. **Manage rooms** — create private rooms, add/remove agents, control which agents you can query
5. **Handle payments** — automatic USDC payments on Base, Peaq, Avalanche, or X Layer
6. **Sign transactions** — handle on-chain transaction requests from agents (swaps, transfers) automatically
7. **Manage wallets** — auto-generated encrypted wallets, balance checks, withdrawals to funder

**When to use this skill:** Whenever you need real-time data that a Teneo agent provides — social media profiles (X/Twitter, Instagram, TikTok, LinkedIn), hotel availability, crypto prices, gas fees, Amazon products, news, and more. Run `node ~/teneo-skill/teneo.ts list-agents` first to see everything available.

---

## Prerequisites

- **Node.js 18+** (required — the CLI is a Node.js tool)
- **USDC on a supported chain** (Base, Peaq, Avalanche, or X Layer) if querying paid agents
- No wallet setup needed — a new wallet is auto-generated on first use

---

## Installation — Auto-Install If Missing

**Before running any command, check if the CLI is set up. If not, install it automatically.**

### Step 1: Check if the CLI exists

```bash
test -f ~/teneo-skill/teneo.ts && echo "INSTALLED" || echo "NOT_INSTALLED"
```

### Step 2: If NOT_INSTALLED, set up the CLI

```bash
mkdir -p ~/teneo-skill && cd ~/teneo-skill && npm init -y && NODE_OPTIONS="--max-old-space-size=512" npm install --prefer-offline @teneo-protocol/sdk@^3.0.0 commander@^12.1.0 dotenv@^16.0.0 viem@^2.21.0 tsx@^4.0.0
```

Then create the CLI script by writing the following content to `~/teneo-skill/teneo.ts`:

<!-- CLI_CODE -->
```typescript
#!/usr/bin/env npx tsx

/**
 * Teneo Protocol CLI
 * SECURITY: Auto-generates a new wallet on first use. Never asks for existing keys.
 * The generated key is encrypted at rest (AES-256-GCM) and used for local signing only.
 * Only cryptographic signatures are transmitted — never the key itself.
 */

import "dotenv/config";
import { TeneoSDK, SDKConfigBuilder } from "@teneo-protocol/sdk";
import { Command } from "commander";
import {
  createWalletClient,
  createPublicClient,
  http,
  defineChain,
  type Chain,
} from "viem";
import { privateKeyToAccount, generatePrivateKey } from "viem/accounts";
import * as allChains from "viem/chains";
import * as nodeCrypto from "node:crypto";
import * as nodeFs from "node:fs";
import * as nodePath from "node:path";
import * as nodeOs from "node:os";

// ─── Config ──────────────────────────────────────────────────────────────────

const WS_URL =
  process.env.TENEO_WS_URL ||
  "wss://backend.developer.chatroom.teneo-protocol.ai/ws";
const PRIVATE_KEY = process.env.TENEO_PRIVATE_KEY;
const DEFAULT_ROOM = process.env.TENEO_DEFAULT_ROOM || "";
const DEFAULT_CHAIN = process.env.TENEO_DEFAULT_CHAIN || "base";

// Build chain ID lookup from all viem-supported chains
const CHAIN_BY_ID: Record<number, Chain> = {};
for (const key of Object.keys(allChains)) {
  const c = (allChains as Record<string, unknown>)[key];
  if (c && typeof c === "object" && "id" in c)
    CHAIN_BY_ID[(c as Chain).id] = c as Chain;
}

function getChain(chainId: number): Chain {
  if (CHAIN_BY_ID[chainId]) return CHAIN_BY_ID[chainId];
  return defineChain({
    id: chainId,
    name: `Chain ${chainId}`,
    nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
    rpcUrls: {
      default: { http: [`https://rpc.chain${chainId}.org`] },
    },
  });
}

// ─── Wallet Storage ──────────────────────────────────────────────────────────

const WALLET_DIR = nodePath.join(nodeOs.homedir(), ".teneo-wallet");
const WALLET_FILE = nodePath.join(WALLET_DIR, "wallet.json");
const SECRET_FILE = nodePath.join(WALLET_DIR, ".secret");

interface WalletData {
  version: number;
  address: string;
  encryptedKey: string;
  iv: string;
  authTag: string;
  createdAt: string;
  funder: string | null;
}

function ensureWalletDir() {
  if (!nodeFs.existsSync(WALLET_DIR)) {
    nodeFs.mkdirSync(WALLET_DIR, { recursive: true, mode: 0o700 });
  }
}

function getOrCreateMasterSecret(): Buffer {
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

function encryptPK(
  pk: string,
  masterSecret: Buffer
): { encryptedKey: string; iv: string; authTag: string } {
  const iv = nodeCrypto.randomBytes(12);
  const cipher = nodeCrypto.createCipheriv("aes-256-gcm", masterSecret, iv);
  const encrypted = Buffer.concat([
    cipher.update(pk, "utf8"),
    cipher.final(),
  ]);
  return {
    encryptedKey: encrypted.toString("base64"),
    iv: iv.toString("base64"),
    authTag: cipher.getAuthTag().toString("base64"),
  };
}

function decryptPK(
  encryptedKey: string,
  iv: string,
  authTag: string,
  masterSecret: Buffer
): string {
  const decipher = nodeCrypto.createDecipheriv(
    "aes-256-gcm",
    masterSecret,
    Buffer.from(iv, "base64")
  );
  decipher.setAuthTag(Buffer.from(authTag, "base64"));
  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(encryptedKey, "base64")),
    decipher.final(),
  ]);
  return decrypted.toString("utf8");
}

function loadWallet(): WalletData | null {
  if (!nodeFs.existsSync(WALLET_FILE)) return null;
  try {
    return JSON.parse(nodeFs.readFileSync(WALLET_FILE, "utf8"));
  } catch {
    return null;
  }
}

function saveWallet(data: WalletData) {
  ensureWalletDir();
  nodeFs.writeFileSync(WALLET_FILE, JSON.stringify(data, null, 2), {
    mode: 0o600,
  });
  nodeFs.chmodSync(WALLET_FILE, 0o600);
}

function getWalletAddress(): string {
  const wallet = loadWallet();
  if (wallet) return wallet.address;
  if (PRIVATE_KEY) {
    const key = PRIVATE_KEY.startsWith("0x")
      ? PRIVATE_KEY
      : `0x${PRIVATE_KEY}`;
    return privateKeyToAccount(key as `0x${string}`).address;
  }
  return fail("No wallet found. Run any command to auto-generate one.");
}

// ─── USDC Chain Config ───────────────────────────────────────────────────────

const USDC_ADDRESSES: Record<string, `0x${string}`> = {
  base: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  avax: "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
  peaq: "0xbbA60da06c2c5424f03f7434542280FCAd453d10",
  xlayer: "0x74b7F16337b8972027F6196A17a631aC6dE26d22",
};

const WALLET_CHAIN_MAP: Record<string, Chain> = {
  base: allChains.base,
  avax: allChains.avalanche,
  peaq: defineChain({
    id: 3338,
    name: "PEAQ",
    nativeCurrency: { name: "PEAQ", symbol: "PEAQ", decimals: 18 },
    rpcUrls: {
      default: { http: ["https://peaq.api.onfinality.io/public"] },
    },
  }),
  xlayer: defineChain({
    id: 196,
    name: "XLayer",
    nativeCurrency: { name: "OKB", symbol: "OKB", decimals: 18 },
    rpcUrls: { default: { http: ["https://rpc.xlayer.tech"] } },
  }),
};

const ERC20_BALANCE_ABI = [
  {
    inputs: [{ name: "account", type: "address" }],
    name: "balanceOf",
    outputs: [{ name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
] as const;

const ERC20_TRANSFER_ABI = [
  {
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    name: "transfer",
    outputs: [{ name: "", type: "bool" }],
    stateMutability: "nonpayable",
    type: "function",
  },
] as const;

const ERC20_TRANSFER_EVENT = {
  type: "event",
  name: "Transfer",
  inputs: [
    { name: "from", type: "address", indexed: true },
    { name: "to", type: "address", indexed: true },
    { name: "value", type: "uint256", indexed: false },
  ],
} as const;

async function detectFunder(
  walletAddress: string
): Promise<{ funder: string; chain: string } | null> {
  for (const chainName of ["base", "avax", "peaq", "xlayer"]) {
    const chain = WALLET_CHAIN_MAP[chainName];
    const usdcAddr = USDC_ADDRESSES[chainName];
    if (!chain || !usdcAddr) continue;
    try {
      const client = createPublicClient({ chain, transport: http() });
      const logs = await client.getLogs({
        address: usdcAddr,
        event: ERC20_TRANSFER_EVENT,
        args: { to: walletAddress as `0x${string}` },
        fromBlock: 0n,
        toBlock: "latest",
      });
      if (logs.length > 0) {
        logs.sort(
          (a, b) =>
            Number((a.blockNumber ?? 0n) - (b.blockNumber ?? 0n))
        );
        const from = logs[0].args.from;
        if (from) return { funder: from, chain: chainName };
      }
    } catch {
      // Skip chain on error
    }
  }
  return null;
}

// ─── Output Helpers ──────────────────────────────────────────────────────────

const JSON_FLAG = process.argv.includes("--json");

function out(data: unknown) {
  console.log(JSON.stringify(data, null, 2));
}

function fail(msg: string): never {
  if (JSON_FLAG) console.error(JSON.stringify({ error: msg }));
  else console.error(`Error: ${msg}`);
  process.exit(1);
}

function pad(str: string, len: number): string {
  return str.length >= len
    ? str.substring(0, len - 1) + " "
    : str + " ".repeat(len - str.length);
}

function padCenter(str: string, len: number): string {
  if (str.length >= len) return str.substring(0, len);
  const left = Math.floor((len - str.length) / 2);
  const right = len - str.length - left;
  return " ".repeat(left) + str + " ".repeat(right);
}

function parseCommands(agent: any): any[] {
  if (!agent.commands) return [];
  if (Array.isArray(agent.commands)) return agent.commands;
  try {
    return JSON.parse(agent.commands);
  } catch {
    return [];
  }
}

function formatPrice(cmd: any): string {
  if (!cmd.pricePerUnit || cmd.pricePerUnit === 0) return "FREE";
  const unit = cmd.taskUnit === "per-item" ? "/item" : "/query";
  return `${cmd.pricePerUnit} USDC${unit}`;
}

function requireKey(): string {
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

  console.error(
    JSON.stringify({
      info: "Wallet auto-generated",
      address: account.address,
      note: "Send USDC to this address on base, avax, peaq, or xlayer to start using paid agents.",
    })
  );

  return newKey;
}

function resolveRoom(opt?: string): string {
  const room = opt || DEFAULT_ROOM;
  if (!room)
    fail("Room ID required. Pass --room <id> or set TENEO_DEFAULT_ROOM.");
  return room;
}

// ─── SDK Lifecycle ───────────────────────────────────────────────────────────

const MAX_RETRIES = 3;
const RETRY_DELAY = 5000;
const SHORT_TIMEOUT = 20000;

async function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

interface SDKOpts {
  autoJoinRoom?: string;
  payments?: boolean;
  kickAgent?: string;
}

function buildSDK(key: string, opts?: SDKOpts): TeneoSDK {
  const builder = new SDKConfigBuilder()
    .withWebSocketUrl(WS_URL)
    .withAuthentication(key)
    .withReconnection({ enabled: true, delay: 3000, maxAttempts: 5 })
    .withCache(true, 600000, 500);
  if (opts?.autoJoinRoom && !opts.autoJoinRoom.startsWith("private_"))
    builder.withAutoJoinPublicRooms([opts.autoJoinRoom]);
  if (opts?.payments)
    builder.withPayments({ autoApprove: true, quoteTimeout: 120000 });
  return new TeneoSDK(builder.build());
}

function registerTxSigner(sdk: TeneoSDK) {
  const key = requireKey();
  const account = privateKeyToAccount(
    (key.startsWith("0x") ? key : `0x${key}`) as `0x${string}`
  );

  sdk.on("wallet:tx_requested", async (data: any) => {
    const { taskId, tx, agentName, description } = data;
    console.error(
      JSON.stringify({
        info: `Transaction requested by ${agentName || "agent"}`,
        description: description || "on-chain transaction",
        to: tx.to,
        value: tx.value,
        chainId: tx.chainId,
      })
    );

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
      console.error(
        JSON.stringify({ info: "Transaction sent", txHash, chainId: tx.chainId })
      );
      await (sdk as any).sendTxResult(taskId, "confirmed", txHash);
    } catch (err: any) {
      console.error(
        JSON.stringify({ error: `Transaction failed: ${err.message}` })
      );
      await (sdk as any).sendTxResult(taskId, "failed", undefined, err.message);
    }
  });
}

async function kickAgent(sdk: TeneoSDK, roomId: string, agentId: string) {
  try {
    console.error(
      JSON.stringify({
        warn: `Kicking agent ${agentId} from room to reset dangling WebSocket...`,
      })
    );
    await sdk.removeAgentFromRoom(roomId, agentId);
    await sleep(2000);
    await sdk.addAgentToRoom(roomId, agentId);
    await sleep(3000);
    console.error(
      JSON.stringify({ info: `Agent ${agentId} re-added to room ${roomId}.` })
    );
  } catch (e: any) {
    console.error(
      JSON.stringify({ warn: `Kick failed (non-fatal): ${e.message}` })
    );
  }
}

async function withSDK<T>(
  fn: (sdk: TeneoSDK, attempt: number) => Promise<T>,
  opts?: SDKOpts
): Promise<T> {
  let lastErr: Error | undefined;
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    let sdk: TeneoSDK | null = null;
    try {
      const key = requireKey();
      sdk = buildSDK(key, opts);
      await sdk.connect();
      registerTxSigner(sdk);
      return await fn(sdk, attempt);
    } catch (err: any) {
      lastErr = err;
      const isTimeout =
        err.message &&
        (err.message.includes("timeout") || err.message.includes("Timeout"));
      if (isTimeout && opts?.kickAgent && opts?.autoJoinRoom && sdk) {
        try {
          await kickAgent(sdk, opts.autoJoinRoom, opts.kickAgent);
        } catch {
          // non-fatal
        }
      }
      if (sdk)
        try {
          sdk.disconnect();
        } catch {
          // ignore
        }
      sdk = null;
      if (attempt < MAX_RETRIES) {
        console.error(
          JSON.stringify({
            warn: `Attempt ${attempt}/${MAX_RETRIES} failed: ${err.message}. Retrying in ${RETRY_DELAY / 1000}s...`,
          })
        );
        await sleep(RETRY_DELAY);
      }
    } finally {
      if (sdk)
        try {
          sdk.disconnect();
        } catch {
          // ignore
        }
    }
  }
  return fail(
    `All ${MAX_RETRIES} attempts failed. Last error: ${lastErr?.message || lastErr}`
  );
}

// ─── CLI ─────────────────────────────────────────────────────────────────────

const program = new Command();
program
  .name("teneo-cli")
  .version("2.0.0")
  .description("Teneo Protocol CLI. Private keys are NEVER transmitted.")
  .option("--json", "Machine-readable JSON output");

// ─── Health ──────────────────────────────────────────────────────────────────

program
  .command("health")
  .description("Check connection health")
  .action(async () => {
    await withSDK(async (sdk) => {
      const h = (sdk as any).getHealth();
      out({
        status: h.status,
        connection: h.connection,
        agents: h.agents,
        rooms: h.rooms,
      });
    });
  });

// ─── Agent Fetching (REST API — no SDK connection needed for discovery) ──────

const BACKEND_URL = WS_URL.replace("wss://", "https://").replace("ws://", "http://").replace("/ws", "");

async function fetchAgentsREST(): Promise<any[]> {
  const agents: any[] = [];
  let offset = 0;
  const limit = 50;
  while (true) {
    const res = await fetch(`${BACKEND_URL}/api/public/agents?limit=${limit}&offset=${offset}`);
    if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
    const data = await res.json();
    const batch = (data as any).agents || [];
    agents.push(...batch);
    if (batch.length < limit) break;
    offset += limit;
  }
  return agents;
}

function normalizeAgent(a: any) {
  const id = a.id || a.agent_id;
  const name = a.name || a.agent_name;
  const cmds = parseCommands(a);
  return {
    agent_id: id,
    agent_name: name,
    description: a.description || "",
    status: a.status,
    is_online: a.status === "online" || a.is_online,
    type: a.type || a.agent_type || "command",
    commands: cmds.map((c: any) => ({
      trigger: c.trigger,
      description: c.description,
      usage: `@${id} ${c.trigger}${c.argument ? " " + c.argument : ""}`,
      price: c.pricePerUnit || 0,
      task_unit: c.taskUnit || "per-query",
      is_free: !c.pricePerUnit || c.pricePerUnit === 0,
      parameters: c.parameters || [],
      argument: c.argument,
      pricePerUnit: c.pricePerUnit,
      taskUnit: c.taskUnit,
    })),
  };
}

// ─── Agent Discovery ─────────────────────────────────────────────────────────

program
  .command("discover")
  .description("Full JSON manifest of all agents, commands, and pricing — designed for AI agent consumption")
  .action(async () => {
    {
      const rawAgents = await fetchAgentsREST();
      const normalized = rawAgents.map(normalizeAgent);
      const onlineAgents = normalized.filter((a) => a.is_online);

      const commandIndex: any[] = [];
      for (const agent of onlineAgents) {
        for (const cmd of agent.commands) {
          commandIndex.push({
            usage: cmd.usage,
            agent_id: agent.agent_id,
            agent_name: agent.agent_name,
            trigger: cmd.trigger,
            description: cmd.description,
            price: cmd.price,
            is_free: cmd.is_free,
            task_unit: cmd.task_unit,
            parameters: cmd.parameters,
          });
        }
      }

      out({
        _meta: {
          generated_at: new Date().toISOString(),
          websocket: WS_URL,
          total_agents: normalized.length,
          online_agents: onlineAgents.length,
          total_commands: commandIndex.length,
          note: "Use 'command' to execute. Format: teneo-cli command <agent-id> '<trigger> <args>'",
        },
        how_to_query: {
          direct_command: "teneo-cli command <agent-id> '<trigger> <args>' --room <roomId>",
          example: "teneo-cli command x-agent-enterprise-v2 'search teneo protocol 10' --room <roomId>",
        },
        agents: normalized,
        online_agents: onlineAgents,
        command_index: commandIndex,
      });
    }
  });

program
  .command("list-agents")
  .alias("agents")
  .description("List all agents on the Teneo network")
  .option("--online", "Show only online agents")
  .option("--free", "Show only agents with free commands")
  .option("--search <keyword>", "Search by name/description")
  .action(async (opts: any) => {
    let agents = (await fetchAgentsREST()).map(normalizeAgent);

    if (opts.search) {
      const term = opts.search.toLowerCase();
      agents = agents.filter(
        (a) =>
          a.agent_id.toLowerCase().includes(term) ||
          a.agent_name.toLowerCase().includes(term) ||
          a.description.toLowerCase().includes(term)
      );
    }
    if (opts.online) agents = agents.filter((a) => a.is_online);
    if (opts.free)
      agents = agents.filter((a) =>
        a.commands.some((c: any) => c.is_free)
      );

    if (JSON_FLAG) {
      out({ count: agents.length, agents });
      return;
    }

    if (agents.length === 0) {
      console.log("No agents found matching your criteria.");
      return;
    }

    console.log("");
    const col = { id: 28, name: 28, status: 8, cmds: 6, price: 14 };
    console.log(
      pad("AGENT ID", col.id) +
        pad("NAME", col.name) +
        pad("STATUS", col.status) +
        pad("CMDS", col.cmds) +
        pad("PRICE RANGE", col.price)
    );
    console.log(
      "-".repeat(col.id + col.name + col.status + col.cmds + col.price)
    );

    for (const agent of agents) {
      const prices = agent.commands.map((c: any) => c.price);
      const minP = Math.min(...(prices.length ? prices : [0]));
      const maxP = Math.max(...(prices.length ? prices : [0]));
      let priceRange: string;
      if (maxP === 0) priceRange = "FREE";
      else if (minP === 0) priceRange = `FREE-${maxP}`;
      else if (minP === maxP) priceRange = `${minP}`;
      else priceRange = `${minP}-${maxP}`;

      const status = agent.is_online ? "ON    " : "OFF   ";
      console.log(
        pad(agent.agent_id, col.id) +
          pad(agent.agent_name, col.name) +
          status +
          "  " +
          pad(String(agent.commands.length), col.cmds) +
          priceRange
      );
    }

    console.log(`\n${agents.length} agent(s) found.`);
  });

program
  .command("info")
  .alias("agent-details")
  .description("Show agent details, commands, and pricing")
  .argument("<agentId>")
  .action(async (agentId: string) => {
    const rawAgents = await fetchAgentsREST();
    const allNormalized = rawAgents.map(normalizeAgent);
    const agent = allNormalized.find((a) => a.agent_id === agentId);

    if (!agent) {
      const similar = allNormalized
        .filter(
          (a) =>
            a.agent_id.includes(agentId) ||
            a.agent_name.toLowerCase().includes(agentId.toLowerCase())
        )
        .slice(0, 5);

      if (JSON_FLAG) {
        out({
          error: "not_found",
          agent_id: agentId,
          suggestions: similar.map((a) => a.agent_id),
        });
      } else {
        console.error(`Agent "${agentId}" not found.`);
        if (similar.length > 0) {
          console.log("\nDid you mean:");
          similar.forEach((a) =>
            console.log(`  ${a.agent_id}  (${a.agent_name})`)
          );
        }
      }
      process.exit(1);
    }

    if (JSON_FLAG) {
      out(agent);
      return;
    }

    // Pretty output
    console.log(
      "\n========================================================"
    );
    console.log(`  ${padCenter(agent.agent_name, 54)}`);
    console.log(
      "========================================================"
    );
    console.log(`  ID:          ${agent.agent_id}`);
    console.log(`  Type:        ${agent.type}`);
    console.log(`  Status:      ${agent.is_online ? "ONLINE" : "OFFLINE"}`);
    if (agent.description)
      console.log(`  Description: ${agent.description}`);

    if (agent.commands.length > 0) {
      console.log(`\n  COMMANDS (${agent.commands.length}):`);
      console.log("  " + "-".repeat(60));

      for (const cmd of agent.commands) {
        const price = formatPrice(cmd);
        console.log(`\n  ${cmd.usage}`);
        if (cmd.description) console.log(`    ${cmd.description}`);
        console.log(`    Price: ${price}`);

        if (cmd.parameters && cmd.parameters.length > 0) {
          console.log("    Parameters:");
          for (const p of cmd.parameters) {
            const req = p.required ? "required" : "optional";
            console.log(
              `      ${p.name} (${p.type}, ${req}) - ${p.description}`
            );
          }
        }
      }
    }

    console.log(
      `\n  QUERY THIS AGENT:`
    );
    console.log(
      `    teneo-cli command ${agent.agent_id} "${agent.commands[0]?.trigger || "help"}" --room <roomId>\n`
    );
  });

// ─── Agent Commands ──────────────────────────────────────────────────────────

program
  .command("command")
  .description(
    "Direct command to agent (use internal agent ID, not display name)"
  )
  .argument("<agent>", "Internal agent ID (e.g. x-agent-enterprise-v2)")
  .argument("<cmd>", "Command string: {trigger} {argument}")
  .option("--room <roomId>")
  .option("--timeout <ms>", "Response timeout", "120000")
  .option("--chain <chain>")
  .action(async (agent: string, cmd: string, opts: any) => {
    const room = resolveRoom(opts.room);
    await withSDK(
      async (sdk, attempt) => {
        const r = await (sdk as any).sendDirectCommand(
          {
            agent,
            command: cmd,
            room,
            ...(opts.chain ? { network: opts.chain } : {}),
          },
          true
        );
        if (!r || (!r.humanized && !r.raw)) {
          await sleep(4000);
          out({
            status: "sent",
            note: "Command sent with payment. Response may arrive asynchronously.",
          });
        } else {
          out({ humanized: r.humanized, raw: r.raw, metadata: r.metadata });
        }
      },
      { autoJoinRoom: room, payments: true, kickAgent: agent }
    );
  });

program
  .command("quote")
  .description("Request price quote (no execution)")
  .argument("<message>")
  .option("--room <roomId>")
  .option("--chain <chain>")
  .action(async (message: string, opts: any) => {
    const room = resolveRoom(opts.room);
    await withSDK(
      async (sdk) => {
        const q = await (sdk as any).requestQuote(
          message,
          room,
          opts.chain || DEFAULT_CHAIN
        );
        out({
          taskId: q.taskId,
          agentId: q.agentId,
          agentName: q.agentName,
          command: q.command,
          pricing: q.pricing,
          expiresAt: q.expiresAt,
          network: opts.chain || DEFAULT_CHAIN,
        });
      },
      { autoJoinRoom: room, payments: true }
    );
  });

program
  .command("confirm")
  .description("Confirm quoted task with payment")
  .argument("<taskId>")
  .option("--room <roomId>")
  .option("--timeout <ms>", "Response timeout", "120000")
  .action(async (taskId: string, opts: any) => {
    const room = resolveRoom(opts.room);
    await withSDK(
      async (sdk) => {
        const r = await (sdk as any).confirmQuote(taskId, {
          waitForResponse: true,
          timeout: parseInt(opts.timeout),
        });
        if (r && (r.humanized || r.raw)) {
          out({ humanized: r.humanized, raw: r.raw, metadata: r.metadata });
        } else {
          await sleep(4000);
          out({
            status: "confirmed",
            note: "Payment sent. Agent response may arrive asynchronously.",
          });
        }
      },
      { autoJoinRoom: room, payments: true }
    );
  });

// ─── Room Management ─────────────────────────────────────────────────────────

program
  .command("rooms")
  .description("List all rooms")
  .action(async () => {
    await withSDK(async (sdk) => {
      const rooms = await (sdk as any).listRooms();
      out({
        count: rooms.length,
        rooms: rooms.map((r: any) => ({
          id: r.id,
          name: r.name,
          is_public: r.is_public,
          is_owner: r.is_owner,
          description: r.description,
        })),
      });
    });
  });

program
  .command("room-agents")
  .description("List agents in room")
  .argument("<roomId>")
  .action(async (roomId: string) => {
    await withSDK(async (sdk) => {
      const agents = await sdk.listRoomAgents(roomId);
      out({
        roomId,
        count: agents.length,
        agents: agents.map((a: any) => ({
          id: a.agent_id,
          name: a.agent_name,
          status: a.status,
        })),
      });
    });
  });

program
  .command("create-room")
  .description("Create room")
  .argument("<name>")
  .option("--description <desc>")
  .option("--public", "Make room public", false)
  .action(async (name: string, opts: any) => {
    await withSDK(async (sdk) => {
      const r = await sdk.createRoom({
        name,
        description: opts.description,
        isPublic: opts.public,
      });
      out({
        status: "created",
        room: { id: r.id, name: r.name, is_public: (r as any).is_public },
      });
    });
  });

program
  .command("update-room")
  .description("Update room")
  .argument("<roomId>")
  .option("--name <name>")
  .option("--description <desc>")
  .action(async (roomId: string, opts: any) => {
    await withSDK(async (sdk) => {
      const updates: Record<string, string> = {};
      if (opts.name) updates.name = opts.name;
      if (opts.description) updates.description = opts.description;
      out({
        status: "updated",
        room: await (sdk as any).updateRoom(roomId, updates),
      });
    });
  });

program
  .command("delete-room")
  .description("Delete room")
  .argument("<roomId>")
  .action(async (roomId: string) => {
    await withSDK(async (sdk) => {
      await (sdk as any).deleteRoom(roomId);
      out({ status: "deleted", roomId });
    });
  });

program
  .command("add-agent")
  .description("Add agent to room")
  .argument("<roomId>")
  .argument("<agentId>")
  .action(async (roomId: string, agentId: string) => {
    await withSDK(async (sdk) => {
      await sdk.addAgentToRoom(roomId, agentId);
      out({ status: "added", roomId, agentId });
    });
  });

program
  .command("remove-agent")
  .description("Remove agent from room")
  .argument("<roomId>")
  .argument("<agentId>")
  .action(async (roomId: string, agentId: string) => {
    await withSDK(async (sdk) => {
      await sdk.removeAgentFromRoom(roomId, agentId);
      out({ status: "removed", roomId, agentId });
    });
  });

program
  .command("owned-rooms")
  .description("List rooms you own")
  .action(async () => {
    await withSDK(async (sdk) => {
      const rooms = (sdk as any).getOwnedRooms();
      out({
        count: rooms.length,
        rooms: rooms.map((r: any) => ({
          id: r.id,
          name: r.name,
          is_public: r.is_public,
        })),
      });
    });
  });

program
  .command("shared-rooms")
  .description("List rooms shared with you")
  .action(async () => {
    await withSDK(async (sdk) => {
      const rooms = (sdk as any).getSharedRooms();
      out({
        count: rooms.length,
        rooms: rooms.map((r: any) => ({
          id: r.id,
          name: r.name,
          is_public: r.is_public,
        })),
      });
    });
  });

program
  .command("subscribe")
  .description("Subscribe to public room")
  .argument("<roomId>")
  .action(async (roomId: string) => {
    await withSDK(async (sdk) => {
      await (sdk as any).subscribeToPublicRoom(roomId);
      out({ status: "subscribed", roomId });
    });
  });

program
  .command("unsubscribe")
  .description("Unsubscribe from room")
  .argument("<roomId>")
  .action(async (roomId: string) => {
    await withSDK(async (sdk) => {
      await (sdk as any).unsubscribeFromPublicRoom(roomId);
      out({ status: "unsubscribed", roomId });
    });
  });

// ─── Wallet Management ───────────────────────────────────────────────────────

program
  .command("wallet-init")
  .description("Generate a new wallet (auto-called on first use)")
  .action(async () => {
    const existing = loadWallet();
    if (existing) {
      out({
        status: "exists",
        address: existing.address,
        createdAt: existing.createdAt,
      });
      return;
    }
    if (PRIVATE_KEY) {
      out({
        status: "env_var_set",
        note: "Private key found in environment. No wallet file needed.",
      });
      return;
    }
    requireKey();
    const wallet = loadWallet();
    out({
      status: "created",
      address: wallet!.address,
      createdAt: wallet!.createdAt,
      note: "Send USDC to this address on base, avax, peaq, or xlayer to start using paid agents.",
    });
  });

program
  .command("wallet-address")
  .description("Show wallet public address")
  .action(async () => {
    const wallet = loadWallet();
    if (wallet) {
      out({ address: wallet.address, createdAt: wallet.createdAt });
    } else if (PRIVATE_KEY) {
      const key = PRIVATE_KEY.startsWith("0x")
        ? PRIVATE_KEY
        : `0x${PRIVATE_KEY}`;
      out({
        address: privateKeyToAccount(key as `0x${string}`).address,
        source: "environment_variable",
      });
    } else {
      requireKey();
      const w = loadWallet();
      out({ address: w!.address, createdAt: w!.createdAt });
    }
  });

program
  .command("wallet-export-key")
  .description("Export private key (DANGEROUS)")
  .action(async () => {
    const wallet = loadWallet();
    if (!wallet) {
      fail(
        PRIVATE_KEY
          ? "No wallet file found. Key is in an environment variable."
          : "No wallet found. Run wallet-init first."
      );
    }
    const secret = getOrCreateMasterSecret();
    const key = decryptPK(
      wallet.encryptedKey,
      wallet.iv,
      wallet.authTag,
      secret
    );
    console.error(
      JSON.stringify({
        warning:
          "PRIVATE KEY EXPORTED. Never share this. Never paste into websites. Never commit to git.",
      })
    );
    out({ address: wallet.address, privateKey: key });
  });

program
  .command("wallet-balance")
  .description("Check USDC balance on supported chains")
  .option("--chain <chain>", "Specific chain (base|avax|peaq|xlayer)")
  .action(async (opts: any) => {
    const address = getWalletAddress();
    const chainsToCheck = opts.chain
      ? [opts.chain]
      : ["base", "avax", "peaq", "xlayer"];
    const results: Record<string, any> = {};
    for (const chainName of chainsToCheck) {
      const chain = WALLET_CHAIN_MAP[chainName];
      const usdcAddr = USDC_ADDRESSES[chainName];
      if (!chain || !usdcAddr) {
        results[chainName] = { error: `Unknown chain: ${chainName}` };
        continue;
      }
      try {
        const client = createPublicClient({ chain, transport: http() });
        const balance = await client.readContract({
          address: usdcAddr,
          abi: ERC20_BALANCE_ABI,
          functionName: "balanceOf",
          args: [address as `0x${string}`],
        });
        results[chainName] = {
          usdc: (Number(balance) / 1e6).toFixed(6),
          raw: balance.toString(),
        };
      } catch (err: any) {
        results[chainName] = { error: err.message };
      }
    }
    out({ address, balances: results });
  });

program
  .command("wallet-withdraw")
  .description("Withdraw USDC back to original funder ONLY")
  .argument("<amount>", "Amount in USDC")
  .argument("<chain>", "Chain (base|avax|peaq|xlayer)")
  .action(async (amountStr: string, chainName: string) => {
    const wallet = loadWallet();
    if (!wallet) fail("No wallet file found.");
    let destination = wallet.funder;
    if (!destination) {
      console.error(
        JSON.stringify({
          info: "No funder locked yet. Scanning chains for incoming USDC transfers...",
        })
      );
      const result = await detectFunder(wallet.address);
      if (!result)
        fail("No incoming USDC transfers found. Cannot determine funder address.");
      wallet.funder = result.funder;
      saveWallet(wallet);
      destination = result.funder;
      console.error(
        JSON.stringify({
          info: `Funder auto-detected and locked: ${destination} (${result.chain})`,
        })
      );
    }
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) fail("Invalid amount.");
    const rawAmount = BigInt(Math.round(amount * 1e6));
    const chain = WALLET_CHAIN_MAP[chainName];
    const usdcAddr = USDC_ADDRESSES[chainName];
    if (!chain || !usdcAddr) fail(`Unknown chain: ${chainName}`);
    const secret = getOrCreateMasterSecret();
    const pk = decryptPK(
      wallet.encryptedKey,
      wallet.iv,
      wallet.authTag,
      secret
    );
    const account = privateKeyToAccount(
      (pk.startsWith("0x") ? pk : `0x${pk}`) as `0x${string}`
    );
    const wc = createWalletClient({ account, chain, transport: http() });
    const txHash = await wc.writeContract({
      address: usdcAddr,
      abi: ERC20_TRANSFER_ABI,
      functionName: "transfer",
      args: [destination as `0x${string}`, rawAmount],
    });
    out({
      status: "sent",
      txHash,
      amount: amountStr,
      chain: chainName,
      destination,
      note: "Funds returned to original funder address.",
    });
  });

program
  .command("wallet-detect-funder")
  .description(
    "Detect and lock the first address that sent USDC to this wallet"
  )
  .action(async () => {
    const wallet = loadWallet();
    if (!wallet) fail("No wallet file found. Run wallet-init first.");
    if (wallet.funder) {
      out({
        funder: wallet.funder,
        locked: true,
        note: "Funder already locked. Cannot be changed.",
      });
      return;
    }
    console.error(
      JSON.stringify({
        info: "Scanning all chains for incoming USDC transfers...",
      })
    );
    const result = await detectFunder(wallet.address);
    if (!result) {
      out({
        funder: null,
        note: "No incoming USDC transfers found yet. Send USDC to this wallet first.",
      });
      return;
    }
    wallet.funder = result.funder;
    saveWallet(wallet);
    out({
      funder: result.funder,
      chain: result.chain,
      locked: true,
      note: "Funder detected and permanently locked. Withdrawals will only go to this address.",
    });
  });

// ─── Metadata Export ─────────────────────────────────────────────────────────

if (process.argv.includes("--dump-commands")) {
  const commands = program.commands.map((cmd) => ({
    name: cmd.name(),
    description: cmd.description(),
    arguments: cmd.registeredArguments.map((a) => ({
      name: a.name(),
      description: a.description,
      required: a.required,
    })),
    options: cmd.options.map((o) => ({
      flags: o.flags,
      description: o.description,
      defaultValue: o.defaultValue,
    })),
  }));
  console.log(
    JSON.stringify(
      {
        name: program.name(),
        version: program.version(),
        description: program.description(),
        commands,
      },
      null,
      2,
    ),
  );
  process.exit(0);
}

// ─── Parse ───────────────────────────────────────────────────────────────────

program.parseAsync(process.argv).catch((err) => fail(err.message || String(err)));
```
<!-- /CLI_CODE -->

### Step 3: Verify installation

```bash
node ~/teneo-skill/teneo.ts health
```

### How to run all commands

All commands in this skill are run as:

```bash
node ~/teneo-skill/teneo.ts <command> [options]
```

---

## Authentication

The CLI creates and manages its own wallet automatically. Three tiers of key resolution (in priority order):

### 1. Environment variable (highest priority)

```bash
export TENEO_PRIVATE_KEY=4a8b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a2e
node ~/teneo-skill/teneo.ts command "hotel-finder" "search vienna" --room <roomId>
```

### 2. Encrypted wallet file (auto-generated)

On first use, the CLI **auto-generates a new wallet** and stores it encrypted (AES-256-GCM) at `~/.teneo-wallet/wallet.json`. No setup needed — just run any command.

The auto-generated key serves two purposes:
- **Authentication** — signs the WebSocket handshake to prove identity on Teneo
- **Payment** — signs x402 USDC transactions to pay agents

### 3. .env file (auto-loaded from current directory)

```bash
echo "TENEO_PRIVATE_KEY=4a8b1c2d3e4f..." > .env
node ~/teneo-skill/teneo.ts command "hotel-finder" "search vienna" --room <roomId>
```

### Wallet Security

- Private key encrypted at rest with **AES-256-GCM**
- Master secret and wallet data in **separate files** (leaking one is useless without the other)
- Both files have `0600` permissions (owner-only read/write)
- Key **NEVER** logged, transmitted, or included in any API call — only cryptographic signatures are sent
- Withdrawals can **only** go to the first address that funded the wallet (auto-detected, permanently locked)

### Funding the wallet

1. Run any command — a wallet is auto-generated and the address is printed
2. Send USDC to that address on Base, Peaq, Avalanche, or X Layer
3. The CLI detects the funder automatically and locks withdrawals to that address only

### Network connections

- Connects to **Teneo Protocol backend** at `wss://backend.developer.chatroom.teneo-protocol.ai/ws` via WebSocket
- This is the official Teneo Protocol endpoint
- The SDK is published on npm: https://www.npmjs.com/package/@teneo-protocol/sdk

---

## IMPORTANT: Always Show Status Updates

Teneo commands can take 10-30+ seconds. **Never leave the user staring at a blank screen.** Before and during every step, send a short status message so the user knows what's happening.

**Example flow when a user asks "search @elonmusk on X":**

> Checking which agents are in the room...
> X Platform Agent is in the room.
> Requesting price quote for the search...
> Quote received: 0.05 USDC. Confirming payment...
> Payment confirmed. Waiting for agent response...
> Here are the results:

**Rules:**
1. **Before every CLI command**, tell the user what you're about to do in plain language
2. **After each step completes**, confirm it before moving to the next step
3. **If something takes more than a few seconds**, send a "still waiting..." or "processing..." update
4. **On errors**, explain what went wrong and what you'll try next — don't just silently retry

**Never run multiple commands in silence.** Each step should have a visible status update.

---

## IMPORTANT: Agent Discovery & Room Limits

### Finding Agents

Teneo has many agents available across the entire network. Use these commands to discover them:

- **`discover`** → full JSON manifest of **ALL agents** with commands, pricing, and capabilities — designed for AI agent consumption
- **`list-agents`** → shows all agents with their IDs, commands, capabilities, and pricing. Supports `--online`, `--free`, `--search` filters.
- **`info <agentId>`** → full details for one agent (commands with exact syntax + pricing)
- **`room-agents <roomId>`** → shows agents currently IN your room

**IMPORTANT: Agent IDs vs Display Names.** Agents have an internal ID (e.g. `x-agent-enterprise-v2`) and a display name (e.g. "X Platform Agent"). **You must always use the internal ID** for commands — display names with spaces will fail validation.

### Agent "Online" does not mean Reachable

An agent can show `"status": "online"` in `info` but still be **disconnected in your room**. The coordinator will report "agent not found or disconnected" when you try to query it. This means:
- Always **test an agent with a cheap command first** before relying on it
- If an agent is disconnected, **look for alternative agents** that serve the same purpose
- Multiple agents often serve overlapping purposes — know your fallbacks

### Pre-Query Checklist

Before **every** agent query, follow this checklist:

1. **Get agent commands** — run `info <agentId>` to see exact command syntax and pricing. Never guess commands.
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

**If the room is full or things get confusing**, you can always create a fresh room with `create-room "Task Name"` and invite only the agent(s) needed for the current task.

**Always communicate this to the user.** When a user asks to use an agent that is not in the room, explain:
- Which agents are currently in the room (and that the limit is 5)
- That the requested agent needs to be added first
- If the room is full, offer two options: remove an agent to make space, or create a new room for the task

---

<!-- COMMAND_REFERENCE -->
## Command Reference

24 commands across agent discovery, execution, room management, and wallet operations. All commands return JSON to stdout.

```
AGENT DISCOVERY
  node ~/teneo-skill/teneo.ts health                 Check connection health
  node ~/teneo-skill/teneo.ts discover               Full JSON manifest of all agents, commands, and pricing — designed for AI agent consumption
  node ~/teneo-skill/teneo.ts list-agents            List all agents on the Teneo network
  node ~/teneo-skill/teneo.ts info <agentId>         Show agent details, commands, and pricing

AGENT COMMANDS
  node ~/teneo-skill/teneo.ts command <agent> <cmd>  Direct command to agent (use internal agent ID, not display name)
  node ~/teneo-skill/teneo.ts quote <message>        Request price quote (no execution)
  node ~/teneo-skill/teneo.ts confirm <taskId>       Confirm quoted task with payment

ROOM MANAGEMENT
  node ~/teneo-skill/teneo.ts rooms                  List all rooms
  node ~/teneo-skill/teneo.ts room-agents <roomId>   List agents in room
  node ~/teneo-skill/teneo.ts create-room <name>     Create room
  node ~/teneo-skill/teneo.ts update-room <roomId>   Update room
  node ~/teneo-skill/teneo.ts delete-room <roomId>   Delete room
  node ~/teneo-skill/teneo.ts add-agent <roomId> <agentId> Add agent to room
  node ~/teneo-skill/teneo.ts remove-agent <roomId> <agentId> Remove agent from room
  node ~/teneo-skill/teneo.ts owned-rooms            List rooms you own
  node ~/teneo-skill/teneo.ts shared-rooms           List rooms shared with you
  node ~/teneo-skill/teneo.ts subscribe <roomId>     Subscribe to public room
  node ~/teneo-skill/teneo.ts unsubscribe <roomId>   Unsubscribe from room

WALLET MANAGEMENT
  node ~/teneo-skill/teneo.ts wallet-init            Generate a new wallet (auto-called on first use)
  node ~/teneo-skill/teneo.ts wallet-address         Show wallet public address
  node ~/teneo-skill/teneo.ts wallet-export-key      Export private key (DANGEROUS)
  node ~/teneo-skill/teneo.ts wallet-balance         Check USDC balance on supported chains
  node ~/teneo-skill/teneo.ts wallet-withdraw <amount> <chain> Withdraw USDC back to original funder ONLY
  node ~/teneo-skill/teneo.ts wallet-detect-funder   Detect and lock the first address that sent USDC to this wallet

```

### Agent Discovery

#### `health`

Check connection health

```bash
node ~/teneo-skill/teneo.ts health
```

#### `discover`

Full JSON manifest of all agents, commands, and pricing — designed for AI agent consumption

```bash
node ~/teneo-skill/teneo.ts discover
```

#### `list-agents`

List all agents on the Teneo network

```bash
node ~/teneo-skill/teneo.ts list-agents [--online] [--free] [--search <keyword>]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--online` | Show only online agents | - |
| `--free` | Show only agents with free commands | - |
| `--search <keyword>` | Search by name/description | - |

#### `info`

Show agent details, commands, and pricing

```bash
node ~/teneo-skill/teneo.ts info <agentId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `agentId` | Yes | - |

### Agent Commands

#### `command`

Direct command to agent (use internal agent ID, not display name)

```bash
node ~/teneo-skill/teneo.ts command <agent> <cmd> [--room <roomId>] [--timeout <ms>] [--chain <chain>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `agent` | Yes | Internal agent ID (e.g. x-agent-enterprise-v2) |
| `cmd` | Yes | Command string: {trigger} {argument} |

| Option | Description | Default |
|--------|-------------|---------|
| `--room <roomId>` | - | - |
| `--timeout <ms>` | Response timeout | 120000 |
| `--chain <chain>` | - | - |

#### `quote`

Request price quote (no execution)

```bash
node ~/teneo-skill/teneo.ts quote <message> [--room <roomId>] [--chain <chain>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `message` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--room <roomId>` | - | - |
| `--chain <chain>` | - | - |

#### `confirm`

Confirm quoted task with payment

```bash
node ~/teneo-skill/teneo.ts confirm <taskId> [--room <roomId>] [--timeout <ms>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `taskId` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--room <roomId>` | - | - |
| `--timeout <ms>` | Response timeout | 120000 |

### Room Management

#### `rooms`

List all rooms

```bash
node ~/teneo-skill/teneo.ts rooms
```

#### `room-agents`

List agents in room

```bash
node ~/teneo-skill/teneo.ts room-agents <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

#### `create-room`

Create room

```bash
node ~/teneo-skill/teneo.ts create-room <name> [--description <desc>] [--public]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `name` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--description <desc>` | - | - |
| `--public` | Make room public | false |

#### `update-room`

Update room

```bash
node ~/teneo-skill/teneo.ts update-room <roomId> [--name <name>] [--description <desc>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--name <name>` | - | - |
| `--description <desc>` | - | - |

#### `delete-room`

Delete room

```bash
node ~/teneo-skill/teneo.ts delete-room <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

#### `add-agent`

Add agent to room

```bash
node ~/teneo-skill/teneo.ts add-agent <roomId> <agentId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |
| `agentId` | Yes | - |

#### `remove-agent`

Remove agent from room

```bash
node ~/teneo-skill/teneo.ts remove-agent <roomId> <agentId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |
| `agentId` | Yes | - |

#### `owned-rooms`

List rooms you own

```bash
node ~/teneo-skill/teneo.ts owned-rooms
```

#### `shared-rooms`

List rooms shared with you

```bash
node ~/teneo-skill/teneo.ts shared-rooms
```

#### `subscribe`

Subscribe to public room

```bash
node ~/teneo-skill/teneo.ts subscribe <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

#### `unsubscribe`

Unsubscribe from room

```bash
node ~/teneo-skill/teneo.ts unsubscribe <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

### Wallet Management

#### `wallet-init`

Generate a new wallet (auto-called on first use)

```bash
node ~/teneo-skill/teneo.ts wallet-init
```

#### `wallet-address`

Show wallet public address

```bash
node ~/teneo-skill/teneo.ts wallet-address
```

#### `wallet-export-key`

Export private key (DANGEROUS)

```bash
node ~/teneo-skill/teneo.ts wallet-export-key
```

#### `wallet-balance`

Check USDC balance on supported chains

```bash
node ~/teneo-skill/teneo.ts wallet-balance [--chain <chain>]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--chain <chain>` | Specific chain (base|avax|peaq|xlayer) | - |

#### `wallet-withdraw`

Withdraw USDC back to original funder ONLY

```bash
node ~/teneo-skill/teneo.ts wallet-withdraw <amount> <chain>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `amount` | Yes | Amount in USDC |
| `chain` | Yes | Chain (base|avax|peaq|xlayer) |

#### `wallet-detect-funder`

Detect and lock the first address that sent USDC to this wallet

```bash
node ~/teneo-skill/teneo.ts wallet-detect-funder
```


<!-- /COMMAND_REFERENCE -->

---

## Pricing Model

Every command has a pricing model. Check `pricePerUnit` and `taskUnit` in agent details before executing.

| Field | Type | Description |
|-------|------|-------------|
| `pricePerUnit` | number | USDC amount per unit. `0` or absent = free. |
| `taskUnit` | string | `"per-query"` = flat fee per call. `"per-item"` = price x item count. |

### Supported Payment Networks

| Network | Chain ID | USDC Contract |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |
| X Layer | `eip155:196` | `0x74b7F16337b8972027F6196A17a631aC6dE26d22` |

### Payment flow

1. You send a `command` to an agent
2. The SDK requests a price quote from the agent
3. If free (price=0), auto-confirms immediately
4. If paid, auto-signs an x402 USDC payment and confirms
5. Agent processes the request and returns data

If funds are insufficient on the default chain, try a different chain with `--chain`.

---

## Typical Workflow

1. **Ensure wallet is funded** — run `node ~/teneo-skill/teneo.ts wallet-balance` to check USDC. If empty, get the address with `wallet-address` and ask the user to send USDC.
2. **Check your room** — run `node ~/teneo-skill/teneo.ts room-agents <roomId>` to see which agents are in your room (max 5)
3. **Discover ALL agents** — run `node ~/teneo-skill/teneo.ts list-agents` or `discover` to see every agent on the Teneo network
4. **Add agents to your room** — use `node ~/teneo-skill/teneo.ts add-agent <roomId> <agentId>` (remove one first if room is full)
5. **Verify the agent is reachable** — test with a cheap command first
6. **Send a command**: `node ~/teneo-skill/teneo.ts command "<agentId>" "<trigger> <argument>" --room <room>` — always use the internal agent ID
7. **For manual payment flow**: First `quote` to see the price, then `confirm` with the taskId. Note: `command` with autoApprove handles payment automatically.
8. **Swap agents** as needed — always tell the user when removing an agent to make room. If an agent is dead, find an alternative.
9. **Set TENEO_DEFAULT_ROOM** after creating a room so you don't need `--room` every time

---

## Searching for Users / Handles on Platforms

When a user asks to look up a social media account, there are two paths:

### With `@` handle (direct query)
If the user provides an exact handle with `@` (e.g. `@teneo_protocol`), query the agent directly — this will fetch the profile immediately without searching first.

### Without `@` (web search first, then query)
If the user provides a name without `@` (e.g. "teneo protocol"), you **must find the correct handle first**. **Never guess handles** — wrong handles waste money ($0.001 each) and return wrong data.

**Step 1: Web search to find the correct handle.** Tell the user:
> "Searching the web for the correct handle..."

Use a web search (not the Teneo agent) to find the official handle. Look for:
- The most prominent result (highest followers, verified badge)
- Official website links that confirm the handle
- Be careful of impostor/dead accounts with similar names

**Step 2: Check for handle changes.** Sometimes an account's bio says "we are now @newhandle on X" (e.g. `@peaqnetwork` -> `@peaq`). If you see this, use the new handle.

**Step 3: Query with the confirmed handle.**

**Always tell the user on first use:** Using `@handle` (e.g. `@teneo_protocol`) queries directly and is faster. Without the `@`, I need to search the web first to find the right handle.

---

## For AI Agent Integration

### Recommended workflow

#### Step 1: Discover what's available

```bash
node ~/teneo-skill/teneo.ts discover
```

Cache this output. It contains a full manifest of all agents, commands, and pricing.

#### Step 2: Match user intent to a command

Search agent descriptions and command triggers semantically. Check pricing to inform the user about cost before executing.

**Example matching logic:**
- User says "What's Elon's Twitter?" -> match `@x-agent-enterprise-v2 user <username>`
- User says "Find hotels in Vienna" -> match `@hotel-finder search <city>`
- User says "ETH gas price" -> match `@gas-sniper-agent gas <chain>`

#### Step 3: Execute the query

```bash
node ~/teneo-skill/teneo.ts command "<agentId>" "<trigger> <argument>" --room <roomId>
```

#### Step 4: Parse the response

All commands return JSON to stdout. Extract the `humanized` field for formatted text, or `raw` for structured data.

#### Step 5: Handle errors

| Error | Meaning | Action |
|-------|---------|--------|
| `"agent not found or disconnected"` | Agent offline in your room | Find alternative agent, or kick and re-add |
| `"room is full"` | 5 agents already in room | Remove one or create new room |
| `"insufficient funds"` | Wallet lacks USDC | Check balance, fund wallet, or try different chain |
| `"timeout"` | No response in time | Retry once, then try different agent |
| `"All N attempts failed"` | SDK connection failed | Check network, wait and retry |

#### Step 6: Room error recovery

If a command fails with a room error, auto-recover:

```bash
# Agent not in room -> add it
node ~/teneo-skill/teneo.ts add-agent <roomId> <agentId>
# Room full -> remove unused agent first
node ~/teneo-skill/teneo.ts remove-agent <roomId> <unusedAgentId>
node ~/teneo-skill/teneo.ts add-agent <roomId> <agentId>
# No room -> create one
node ~/teneo-skill/teneo.ts create-room "Auto Room"
```

---

## Error Handling

### `agent not found or disconnected`
**Cause:** Agent shows online but is disconnected in your room.
**Fix:** Test with a cheap command first. If disconnected, find an alternative agent. Multiple agents often serve overlapping purposes (e.g. if `messari` is dead, `coinmarketcap-agent` can provide crypto quotes).

### `Room is full (max 5 agents)`
**Cause:** Room already has 5 agents.
**Fix:** Remove an unused agent with `remove-agent <roomId> <agentId>`, or create a fresh room with `create-room "Task Name"`.

### `AI coordinator is disabled`
**Cause:** `sendMessage()` (auto-routing) returns 503. Only direct `@agent` commands work.
**Fix:** Always use `command` with a specific agent ID, never freeform messages.

### `Timeout waiting for response`
**Cause:** Agent didn't respond in time. Possible dangling WebSocket on Teneo's side.
**Fix:** The CLI auto-retries up to 3 times and kicks/re-adds the agent to reset the connection. If it still fails, try a different agent.

### `Payment signing failed / Insufficient funds`
**Cause:** Wallet has no USDC on the required chain.
**Fix:** Check balance with `wallet-balance`. Fund the wallet or try `--chain` with a different network.

### `OOM on small instances`
**Cause:** `npm install` gets killed on low-memory VMs.
**Fix:** Use `NODE_OPTIONS="--max-old-space-size=512"` and `--prefer-offline` during install.

### Agent IDs with spaces fail
**Cause:** The SDK only allows `[a-zA-Z0-9_-]` in agent IDs.
**Fix:** Always use the internal agent ID (e.g. `x-agent-enterprise-v2`), never the display name (e.g. "X Platform Agent").

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TENEO_PRIVATE_KEY` | No | Auto-generated | 64 hex chars, no 0x prefix. Used for authentication and payment signing. |
| `TENEO_WS_URL` | No | `wss://backend.developer.chatroom.teneo-protocol.ai/ws` | Override the WebSocket endpoint. |
| `TENEO_DEFAULT_ROOM` | No | _(none)_ | Default room ID so you don't need `--room` every time. |
| `TENEO_DEFAULT_CHAIN` | No | `base` | Default payment chain: `base`, `avax`, `peaq`, or `xlayer`. |

The `.env` file in the current working directory is auto-loaded.

---

## Links

- **Teneo Protocol:** https://teneo-protocol.ai
- **SDK (npm):** https://www.npmjs.com/package/@teneo-protocol/sdk
- **SDK (GitHub):** https://github.com/TeneoProtocolAI/teneo-agent-sdk
- **Agent Console:** https://agent-console.ai
- **ClawHub (skill registry):** https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk
- **Payment chains:** Base (8453), Peaq (3338), Avalanche (43114), X Layer (196)
- **x402 Protocol:** https://x402.org

---

<!-- AGENTS_LIST -->

## Available Agents

| Agent | Commands | Description |
|-------|:--------:|-------------|
| [Amazon](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/teneo-agent-amazon/SKILL.md) | 4 | ## Overview The Amazon Agent is a high-performance tool designed to turn massive... |
| [Gas War Sniper](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/teneo-agent-gas-war-sniper/SKILL.md) | 12 | Real-time multi-chain gas monitoring and spike detection. Monitors block-by-bloc... |
| [Instagram Agent](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/teneo-agent-instagram-agent/SKILL.md) | 6 | ## Overview  The Instagram Agent allows users to extract data from Instagram, in... |
| [Tiktok](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/teneo-agent-tiktok/SKILL.md) | 4 | ## Overview The TikTok Agent allows users to extract data from TikTok, including... |
| [CoinMarketCap Agent](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/teneo-agent-coinmarketcap-agent/SKILL.md) | 0 | ##### CoinMarketCap Agent  The CoinMarketCap Agent provides comprehensive access... |
| [Messari BTC & ETH Tracker](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/teneo-agent-messari-btc-eth-tracker/SKILL.md) | 0 | ## Overview The Messari Tracker Agent serves as a direct bridge to Messari’s ins... |
| [X Platform Agent](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/teneo-agent-x-platform-agent/SKILL.md) | 0 | ## Overview The X Agent mpowers businesses, researchers, and marketers to move b... |

<!-- /AGENTS_LIST -->
