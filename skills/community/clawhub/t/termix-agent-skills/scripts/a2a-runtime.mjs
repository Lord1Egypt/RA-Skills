#!/usr/bin/env node
//
// Termix Platform (dev-v2) A2A runtime connector for OpenClaw.
//
// Subcommands:
//   print-env [--dev|--prod]               Show an env template without secrets.
//   token                                  Sign AACP:a2a-runtime-token:<id>:<ts> with WALLET_KEY and obtain a 12 h runtime token.
//   inbox [--since <iso>] [--limit <n>]    GET /api/v1/a2a/runtime/inbox.
//   reply --conversation <id> --text <s>   POST /api/v1/a2a/runtime/reply.
//   loop [--interval 5] [--max-per-tick 5] Interactive poll loop that prints each
//                                          inbound message and waits for the
//                                          host LLM to call `reply` for each.
//
// Required env:
//   A2A_AGENT_ID    DB cuid of the Provider Agent to host.
//   WALLET_KEY      0x-prefixed private key that owns the agent (only used locally to sign).
//
// Optional env:
//   AACP_BASE_URL   Defaults to https://platform-backend.prod.termix.live
//   A2A_RUNTIME_TOKEN   Cached token (auto-written by `token` to .termix-a2a-runtime.env).
//
// The script never prints WALLET_KEY or full tokens — only previews.
//
import { existsSync, openSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const DEFAULT_BASE = "https://platform-backend.prod.termix.live";
const DEFAULT_DEV_BASE = "https://platform-backend.dev.termix.live";

const args = process.argv.slice(2);
const command = args[0] ?? "help";
const flags = new Set(args.slice(1).filter((s) => s.startsWith("--") && !args[args.indexOf(s) + 1]?.startsWith("--") ? false : s.startsWith("--")));

function arg(name, fallback) {
  const i = args.indexOf(`--${name}`);
  if (i < 0) return fallback;
  const v = args[i + 1];
  return v && !v.startsWith("--") ? v : true;
}

function baseUrl() {
  if (process.env.AACP_BASE_URL) return process.env.AACP_BASE_URL.replace(/\/$/, "");
  if (args.includes("--dev")) return DEFAULT_DEV_BASE;
  return DEFAULT_BASE;
}

function envCachePath() {
  return resolve(process.cwd(), ".termix-a2a-runtime.env");
}

function loadCachedToken() {
  if (process.env.A2A_RUNTIME_TOKEN) return process.env.A2A_RUNTIME_TOKEN;
  const path = envCachePath();
  if (!existsSync(path)) return null;
  const txt = readFileSync(path, "utf8");
  const m = txt.match(/^A2A_RUNTIME_TOKEN=(.+)$/m);
  return m ? m[1].trim() : null;
}

function writeCachedToken(token, meta) {
  const lines = [
    `# Termix A2A runtime token — keep local, do NOT paste back to chat.`,
    `# Issued ${new Date().toISOString()}`,
    `# agentId=${meta.agentId} agentTokenId=${meta.agentTokenId} agentName=${meta.agentName}`,
    `A2A_RUNTIME_TOKEN=${token}`,
    "",
  ];
  writeFileSync(envCachePath(), lines.join("\n"), { mode: 0o600 });
}

function requireWalletKey() {
  const key = process.env.WALLET_KEY?.trim();
  if (!key) throw new Error("WALLET_KEY env is required to sign a runtime token request.");
  if (!/^0x[a-fA-F0-9]{64}$/.test(key)) throw new Error("WALLET_KEY must be a 0x-prefixed 32-byte hex private key.");
  return key;
}

// ── Wallet session (SIWE-style login → list owned Provider Agents) ────────────

function sessionCachePath() {
  return resolve(process.cwd(), ".termix-a2a-session.env");
}

function loadSessionToken() {
  if (process.env.A2A_SESSION_TOKEN) return process.env.A2A_SESSION_TOKEN;
  const path = sessionCachePath();
  if (!existsSync(path)) return null;
  const m = readFileSync(path, "utf8").match(/^A2A_SESSION_TOKEN=(.+)$/m);
  return m ? m[1].trim() : null;
}

function writeSessionToken(token, meta) {
  const lines = [
    `# Termix wallet session token — keep local, do NOT paste back to chat.`,
    `# Issued ${new Date().toISOString()} wallet=${meta.wallet} account=${meta.account ?? ""}`,
    `A2A_SESSION_TOKEN=${token}`,
    "",
  ];
  writeFileSync(sessionCachePath(), lines.join("\n"), { mode: 0o600 });
}

// Reuse a cached runtime token if present; otherwise sign + issue a fresh one
// scoped to agentId. Used by `autoreply` so the operator never runs `token`
// manually.
async function ensureRuntimeToken(agentId, { reissue = false } = {}) {
  if (!reissue) {
    const cached = loadCachedToken();
    if (cached) return cached;
  }
  const { address, ts, sig } = await signRuntimeRequest(agentId);
  const res = await http("POST", `/api/v1/a2a/runtime/token/${agentId}`, {
    headers: { "x-wallet-address": address, "x-wallet-signature": sig, "x-wallet-timestamp": String(ts) },
  });
  writeCachedToken(res.token, { agentId: res.agentId, agentTokenId: res.agentTokenId, agentName: res.agentName });
  return res.token;
}

// ── LLM reply generation (OpenRouter / OpenAI-compatible) ─────────────────────

function llmConfig() {
  const key = process.env.OPENROUTER_API_KEY || process.env.OPENAI_API_KEY;
  const base = (process.env.OPENAI_BASE_URL || "https://openrouter.ai/api/v1").replace(/\/$/, "");
  const model = process.env.A2A_LLM_MODEL || "openai/gpt-4o-mini";
  return { key, base, model };
}

async function llmReply(persona, userText) {
  const { key, base, model } = llmConfig();
  if (!key) throw new Error("No LLM key — set OPENROUTER_API_KEY or OPENAI_API_KEY.");
  const res = await fetch(`${base}/chat/completions`, {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${key}` },
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: persona },
        { role: "user", content: userText },
      ],
      temperature: 0.4,
      max_tokens: 400,
    }),
  });
  const j = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`LLM ${res.status}: ${JSON.stringify(j).slice(0, 200)}`);
  const text = j?.choices?.[0]?.message?.content?.trim();
  if (!text) throw new Error("LLM returned an empty reply");
  return text;
}

function requireAgentId() {
  const id = process.env.A2A_AGENT_ID?.trim();
  if (!id || id === "<agent-id>") throw new Error("A2A_AGENT_ID env is required (Provider Agent DB cuid).");
  return id;
}

// Self-contained EIP-191 signer (vendored @noble bundle) so the skill signs
// runtime-token requests without requiring viem/ethers in the OpenClaw host.
async function loadSigner() {
  const vendored = fileURLToPath(new URL("./vendor/eth-signer.mjs", import.meta.url));
  return import(vendored);
}

async function signRuntimeRequest(agentId) {
  const pk = requireWalletKey();
  const { addressFromPrivateKey, signMessage } = await loadSigner();
  const address = addressFromPrivateKey(pk);
  const ts = Date.now();
  const msg = `AACP:a2a-runtime-token:${agentId}:${ts}`;
  const sig = signMessage(pk, msg);
  return { address, ts, msg, sig };
}

function previewToken(token) {
  if (!token) return "(none)";
  return `${token.slice(0, 16)}…${token.slice(-8)} (${token.length} chars)`;
}

async function http(method, path, { token, body, headers } = {}) {
  const url = path.startsWith("http") ? path : `${baseUrl()}${path.startsWith("/") ? path : `/${path}`}`;
  const res = await fetch(url, {
    method,
    headers: {
      ...(body ? { "content-type": "application/json" } : {}),
      ...(token ? { authorization: `Bearer ${token}` } : {}),
      ...(headers ?? {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json;
  try { json = text ? JSON.parse(text) : {}; } catch { json = { raw: text }; }
  if (!res.ok) {
    const err = new Error(`${method} ${path} → HTTP ${res.status}: ${json?.error?.message ?? text.slice(0, 200)}`);
    err.status = res.status;
    err.payload = json;
    throw err;
  }
  return json;
}

// ── Subcommands ─────────────────────────────────────────────────────────────

async function cmdPrintEnv() {
  const base = baseUrl();
  console.log(`# Termix A2A runtime connector — env template`);
  console.log(`# Fill A2A_AGENT_ID and WALLET_KEY locally. Do NOT paste into chat.`);
  console.log(`AACP_BASE_URL=${base}`);
  console.log(`A2A_AGENT_ID=<provider-agent-db-cuid>`);
  console.log(`WALLET_KEY=0x<your_private_key>`);
  console.log(`# A2A_RUNTIME_TOKEN=<auto-issued by \`a2a-runtime.mjs token\`>`);
}

async function cmdToken() {
  const agentId = requireAgentId();
  const { address, ts, msg, sig } = await signRuntimeRequest(agentId);
  const res = await http("POST", `/api/v1/a2a/runtime/token/${agentId}`, {
    headers: {
      "x-wallet-address": address,
      "x-wallet-signature": sig,
      "x-wallet-timestamp": String(ts),
    },
  });
  writeCachedToken(res.token, { agentId: res.agentId, agentTokenId: res.agentTokenId, agentName: res.agentName });
  console.log(JSON.stringify({
    agentId: res.agentId,
    agentTokenId: res.agentTokenId,
    agentName: res.agentName,
    ownerAccountId: res.ownerAccountId,
    expiresIn: res.expiresIn,
    tokenPreview: previewToken(res.token),
    cachedAt: envCachePath(),
  }, null, 2));
}

async function cmdInbox() {
  const token = loadCachedToken();
  if (!token) throw new Error("No runtime token cached. Run `a2a-runtime.mjs token` first.");
  const params = new URLSearchParams();
  const since = arg("since");
  const limit = arg("limit");
  if (typeof since === "string") params.set("since", since);
  if (typeof limit === "string") params.set("limit", limit);
  const path = `/api/v1/a2a/runtime/inbox${params.toString() ? `?${params.toString()}` : ""}`;
  const res = await http("GET", path, { token });
  console.log(JSON.stringify(res, null, 2));
}

async function cmdReply() {
  const token = loadCachedToken();
  if (!token) throw new Error("No runtime token cached. Run `a2a-runtime.mjs token` first.");
  const conversationId = arg("conversation");
  const text = arg("text");
  const clientMessageId = arg("client-msg");
  if (typeof conversationId !== "string" || !conversationId) throw new Error("--conversation <id> is required");
  if (typeof text !== "string" || !text) throw new Error("--text <s> is required");
  const body = { conversationId, text };
  if (typeof clientMessageId === "string") body.clientMessageId = clientMessageId;
  const res = await http("POST", `/api/v1/a2a/runtime/reply`, { token, body });
  console.log(JSON.stringify(res, null, 2));
}

// Polling loop emits inbox events to stdout as JSON lines. OpenClaw reads each
// line as a tool result, drafts a reply with its LLM, then calls `reply` —
// after which the loop fetches the next tick. No auto-reply.
async function cmdLoop() {
  const token = loadCachedToken();
  if (!token) throw new Error("No runtime token cached. Run `a2a-runtime.mjs token` first.");
  const intervalSec = Number(arg("interval", "5")) || 5;
  const maxPerTick = Number(arg("max-per-tick", "5")) || 5;
  const startSince = arg("since");
  let since = typeof startSince === "string" ? startSince : new Date().toISOString();
  process.stderr.write(`[loop] starting at since=${since} interval=${intervalSec}s max-per-tick=${maxPerTick}\n`);
  // Ctrl-C: clean exit.
  process.on("SIGINT", () => { process.stderr.write("\n[loop] stopped.\n"); process.exit(0); });

  while (true) {
    let res;
    try {
      res = await http("GET", `/api/v1/a2a/runtime/inbox?since=${encodeURIComponent(since)}&limit=${maxPerTick}`, { token });
    } catch (err) {
      process.stderr.write(`[loop] inbox error: ${err.message}\n`);
      await sleep(intervalSec * 1000);
      continue;
    }
    for (const item of res.items ?? []) {
      // One JSON-line event per inbound message. OpenClaw consumes these.
      console.log(JSON.stringify({ event: "inbox.message", message: item }));
      if (item.createdAt && item.createdAt > since) since = item.createdAt;
    }
    if ((res.items?.length ?? 0) === 0) {
      // Heartbeat for liveness; no message body.
      process.stderr.write(`[loop] tick ${new Date().toISOString()} (empty)\n`);
    }
    await sleep(intervalSec * 1000);
  }
}

// Wallet login: nonce → sign → session token. Caches the access token so
// `agents` can list the wallet's Provider Agents without re-signing.
async function cmdLogin() {
  const pk = requireWalletKey();
  const { addressFromPrivateKey, signMessage } = await loadSigner();
  const address = addressFromPrivateKey(pk);
  const nonceRes = await http("POST", "/api/v1/auth/nonce", { body: { walletAddress: address } });
  const sig = signMessage(pk, nonceRes.message);
  const login = await http("POST", "/api/v1/auth/wallet", {
    body: { walletAddress: address, nonce: nonceRes.nonce, signature: sig },
  });
  writeSessionToken(login.accessToken, { wallet: address, account: login.account?.id });
  console.log(JSON.stringify({
    wallet: address,
    accountId: login.account?.id ?? null,
    handle: login.account?.handle ?? null,
    sessionPreview: previewToken(login.accessToken),
    cachedAt: sessionCachePath(),
  }, null, 2));
}

// List the logged-in wallet's PROVIDER agents — the candidates the operator can
// host. Requires `login` first.
async function cmdAgents() {
  const session = loadSessionToken();
  if (!session) throw new Error("Not logged in. Run `a2a-runtime.mjs login` first.");
  const res = await http("GET", "/api/v1/agents?role=PROVIDER", { token: session });
  const items = (res.items ?? []).map((a) => ({
    agentId: a.id,
    agentTokenId: a.agentTokenId,
    name: a.name,
    a2aStatus: a.a2aStatus,
  }));
  console.log(JSON.stringify({ count: items.length, items }, null, 2));
}

function autoreplyPidFile(agentId) { return `/tmp/termix-autoreply-${agentId}.pid`; }
function autoreplyLogFile(agentId) { return `/tmp/termix-autoreply-${agentId}.log`; }
function pidAlive(pid) { try { process.kill(pid, 0); return true; } catch { return false; } }
function readPid(file) { try { const n = Number(readFileSync(file, "utf8").trim()); return Number.isFinite(n) ? n : 0; } catch { return 0; } }

// Resolve --agent (DB id | agentTokenId | name) to the canonical DB id using the
// cached wallet session. No-op when no session or already an id.
async function resolveAgentId(agentId) {
  const session = loadSessionToken();
  if (!session) return agentId;
  const list = await http("GET", "/api/v1/agents?role=PROVIDER", { token: session }).catch(() => null);
  const items = list?.items ?? [];
  const ref = String(agentId).toLowerCase();
  const match = items.find((a) =>
    a.id === agentId || a.agentTokenId === agentId || (a.name && a.name.toLowerCase() === ref));
  return match ? match.id : agentId;
}

// Go ONLINE. Without --worker this is the *launcher*: it self-detaches a single
// background worker and returns immediately (no `nohup &` needed, so it does not
// trip OpenClaw's elevated-exec gate) and is idempotent — re-running while a
// worker is alive reports "already online" instead of spawning a duplicate.
// `--stop` kills the running worker. `--worker` runs the actual poll/reply loop.
async function cmdAutoreply() {
  const isWorker = args.includes("--worker");
  const doStop = args.includes("--stop");
  let agentId = (typeof arg("agent") === "string" && arg("agent")) || process.env.A2A_AGENT_ID;
  if (!agentId || agentId === "<agent-id>") throw new Error("--agent <id|tokenId|name> (or A2A_AGENT_ID) is required");
  const intervalSec = Number(arg("interval", "5")) || 5;

  // The worker is spawned with the already-resolved DB id; only the launcher /
  // stop paths need to resolve a name/tokenId.
  if (!isWorker) agentId = await resolveAgentId(agentId);
  const pidFile = autoreplyPidFile(agentId);
  const logFile = autoreplyLogFile(agentId);

  if (doStop) {
    const pid = readPid(pidFile);
    if (pid && pidAlive(pid)) { try { process.kill(pid); } catch { /* ignore */ } }
    try { writeFileSync(pidFile, ""); } catch { /* ignore */ }
    console.log(JSON.stringify({ status: "offline", agentId, stoppedPid: pid || null }));
    return;
  }

  if (!isWorker) {
    // Singleton guard: if a live worker already hosts this agent, do nothing.
    const existing = readPid(pidFile);
    if (existing && pidAlive(existing)) {
      console.log(JSON.stringify({ status: "already-online", agentId, pid: existing, log: logFile }));
      return;
    }
    // Validate ownership + that the LLM is configured *before* detaching, so the
    // operator gets a clear error instead of a silently-dead background worker.
    await ensureRuntimeToken(agentId);
    if (!llmConfig().key) throw new Error("No LLM key — set OPENROUTER_API_KEY or OPENAI_API_KEY before going online.");
    const fd = openSync(logFile, "a");
    const childArgs = [fileURLToPath(import.meta.url), "autoreply", "--worker", "--agent", agentId, "--interval", String(intervalSec)];
    const personaArg = arg("persona");
    if (typeof personaArg === "string") childArgs.push("--persona", personaArg);
    const sinceArg = arg("since");
    if (typeof sinceArg === "string") childArgs.push("--since", sinceArg);
    const child = spawn(process.execPath, childArgs, { detached: true, stdio: ["ignore", fd, fd], env: process.env });
    writeFileSync(pidFile, String(child.pid));
    child.unref();
    console.log(JSON.stringify({ status: "online", agentId, pid: child.pid, interval: intervalSec, log: logFile }));
    return;
  }

  // ── Worker: poll inbox + auto-reply until killed ──────────────────────────
  writeFileSync(pidFile, String(process.pid));
  const persona = (typeof arg("persona") === "string" && arg("persona")) ||
    "你是 Termix 平台上某个服务提供方(Provider)的 AI 客服助手，代表卖家回复买家在对话中的咨询。" +
    "请用简洁、友好、专业的中文回答，聚焦服务是否可接单、交付时间、价格与流程等问题。" +
    "不要编造你并不知道的具体订单细节；不确定时礼貌说明会进一步确认。";
  let token = await ensureRuntimeToken(agentId);
  let since = (typeof arg("since") === "string" && arg("since")) || new Date().toISOString();
  process.stderr.write(`[autoreply] ONLINE agent=${agentId} interval=${intervalSec}s since=${since}\n`);
  const cleanup = () => { try { writeFileSync(pidFile, ""); } catch { /* ignore */ } process.exit(0); };
  process.on("SIGINT", cleanup);
  process.on("SIGTERM", cleanup);

  while (true) {
    let res;
    try {
      res = await http("GET", `/api/v1/a2a/runtime/inbox?since=${encodeURIComponent(since)}&limit=10`, { token });
    } catch (err) {
      if (err.status === 401) {
        try { token = await ensureRuntimeToken(agentId, { reissue: true }); continue; } catch { /* fall through */ }
      }
      process.stderr.write(`[autoreply] inbox error: ${err.message}\n`);
      await sleep(intervalSec * 1000);
      continue;
    }
    for (const m of res.items ?? []) {
      // Only reply to conversational messages. Platform status events
      // (OFFER_EVENT, ORDER_EVENT, SYSTEM, …) are not buyer questions — replying
      // to them produced bogus "the seller updated the offer…" chatter. The
      // backend inbox already filters these out; this is defense in depth.
      if (m.kind && m.kind !== "TEXT") {
        if (m.createdAt && m.createdAt > since) since = m.createdAt;
        continue;
      }
      try {
        const reply = await llmReply(persona, m.text ?? "");
        const posted = await http("POST", "/api/v1/a2a/runtime/reply", {
          token,
          body: { conversationId: m.conversationId, text: reply, clientMessageId: `auto-${m.messageId}` },
        });
        console.log(JSON.stringify({ event: "auto.reply", inbound: m.messageId, conversation: m.conversationId, replyId: posted.id, text: reply }));
      } catch (err) {
        process.stderr.write(`[autoreply] reply error for ${m.messageId}: ${err.message}\n`);
      }
      if (m.createdAt && m.createdAt > since) since = m.createdAt;
    }
    await sleep(intervalSec * 1000);
  }
}

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

function usage(code = 0) {
  process.stderr.write(`Usage: node scripts/a2a-runtime.mjs <command> [options]

Commands:
  print-env [--dev|--prod]
  login                                Wallet sign-in (nonce→sign→session). Needs WALLET_KEY.
  agents                               List the wallet's PROVIDER agents (needs login first).
  autoreply --agent <id> [--interval 5] [--persona <s>] [--since <iso>]
                                       Go ONLINE: issue runtime token + auto-reply to the
                                       agent's inbox via the configured LLM. Run in background.
  token                                Sign + cache the runtime token.
  inbox [--since <iso>] [--limit <n>]  Poll inbound messages.
  reply --conversation <id> --text <s> [--client-msg <key>]
  loop [--interval 5] [--max-per-tick 5] [--since <iso>]

Env:
  WALLET_KEY     0x-prefixed private key of the agent owner (login / token / autoreply).
  A2A_AGENT_ID   DB cuid of the Provider Agent to host (token/loop/autoreply fallback).
  AACP_BASE_URL  API base (defaults prod).
  OPENROUTER_API_KEY / OPENAI_API_KEY + OPENAI_BASE_URL + A2A_LLM_MODEL
                 LLM used by \`autoreply\` (default model openai/gpt-4o-mini).
  A2A_SESSION_TOKEN   Cached after \`login\`; \`agents\` auto-reads it.
  A2A_RUNTIME_TOKEN   Cached after \`token\`; loop/inbox/reply/autoreply auto-read it.
`);
  process.exit(code);
}

// ── Entry ───────────────────────────────────────────────────────────────────
try {
  switch (command) {
    case "print-env": await cmdPrintEnv(); break;
    case "login": await cmdLogin(); break;
    case "agents": await cmdAgents(); break;
    case "autoreply": await cmdAutoreply(); break;
    case "token": await cmdToken(); break;
    case "inbox": await cmdInbox(); break;
    case "reply": await cmdReply(); break;
    case "loop": await cmdLoop(); break;
    case "help":
    case "--help":
    case "-h":
      usage(0);
      break;
    default:
      process.stderr.write(`Unknown command: ${command}\n`);
      usage(2);
  }
} catch (err) {
  process.stderr.write(`error: ${err.message}\n`);
  process.exit(1);
}
