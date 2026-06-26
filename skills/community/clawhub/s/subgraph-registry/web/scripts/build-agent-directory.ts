/**
 * Build-time agent directory generator.
 *
 * Runs once during `npm run build` (via the `prebuild` script). Queries the
 * x402-omnigraph subgraph directly for the current top payers to the gateway
 * recipient, enriches each wallet via the operator seed + bazaar + 8004scan
 * + agent0, and writes the result to `data/known-agents.json` — which
 * `app/page.tsx` then imports as a static module.
 *
 * Self-contained: does NOT import from `lib/` because those modules use
 * Next.js server-only APIs (`React.cache`, `unstable_cache`) that aren't
 * available in a plain Node script.
 *
 * Requires: GRAPH_API_KEY in env. Without it the script writes an empty
 * directory so the build doesn't break — page renders with no identified
 * agents (degraded-but-up) rather than failing.
 */

import { writeFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_PATH = resolve(__dirname, "..", "data", "known-agents.json");

const GATEWAY_RECIPIENT = "0x79dc34e41b2b591078d3de222c43ecaabd52fccb";
const SUBGRAPH_ID = "Cb56epg3EvQ6JRpPfknbkM54QxpzTvLa7mwKNQQfUyoj";
const AGENT0_BASE_SUBGRAPH_ID = "43s9hQRurMGjuYnC1r2ZwS6xSQktbFyXMPMqGKUFJojb";

const ENRICH_CONCURRENCY = 5;
const PAGE_SIZE = 1000;
const MAX_ROWS = 5_000;

// ── Types ────────────────────────────────────────────────────────────────────

interface TopPayer {
  wallet: string;
  payments: number;
  first_seen: string;
  last_seen: string;
}

interface AgentRow {
  agent: string;
  wallet: string;
  payments: number;
  first_seen: string;
  last_seen: string;
  registry: string;
  agent_link: string;
}

interface RawPayment {
  id: string;
  from: string;
  amountDecimal: string;
  blockTimestamp: string;
}

interface DirectoryFile {
  generated_at: string;
  source: "build-time";
  payer_count: number;
  agent_count: number;
  agents: AgentRow[];
}

// ── HTTP helpers ─────────────────────────────────────────────────────────────

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, { ...init, signal: AbortSignal.timeout(20_000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${url}`);
  return (await res.json()) as T;
}

async function postGraphQL<T>(url: string, query: string, variables: Record<string, unknown>): Promise<T> {
  const r = await fetchJSON<{ data?: T; errors?: Array<{ message: string }> }>(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables }),
  });
  if (r.errors?.length) throw new Error(`GraphQL: ${r.errors[0].message}`);
  if (!r.data) throw new Error("GraphQL: no data");
  return r.data;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function mapConcurrent<T, R>(
  items: T[],
  concurrency: number,
  fn: (item: T, index: number) => Promise<R>,
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let cursor = 0;
  const workers: Promise<void>[] = [];
  for (let w = 0; w < concurrency; w++) {
    workers.push(
      (async () => {
        while (true) {
          const i = cursor++;
          if (i >= items.length) return;
          results[i] = await fn(items[i], i);
        }
      })(),
    );
  }
  await Promise.all(workers);
  return results;
}

// ── Subgraph: top payers to the gateway ──────────────────────────────────────

async function fetchTopPayers(): Promise<TopPayer[]> {
  const key = process.env.GRAPH_API_KEY!;
  const url = `https://gateway.thegraph.com/api/${key}/subgraphs/id/${SUBGRAPH_ID}`;

  const payments: RawPayment[] = [];
  let cursor = "0x";
  while (payments.length < MAX_ROWS) {
    const data = await postGraphQL<{ x402Payments: RawPayment[] }>(
      url,
      `query Q($to: Bytes!, $cursor: Bytes!, $first: Int!) {
        x402Payments(
          first: $first
          where: { to: $to, id_gt: $cursor }
          orderBy: id
          orderDirection: asc
        ) {
          id from amountDecimal blockTimestamp
        }
      }`,
      { to: GATEWAY_RECIPIENT, cursor, first: PAGE_SIZE },
    );
    const rows = data.x402Payments ?? [];
    if (rows.length === 0) break;
    payments.push(...rows);
    cursor = rows[rows.length - 1].id;
    if (rows.length < PAGE_SIZE) break;
  }

  const byPayer = new Map<string, { count: number; first: number; last: number }>();
  for (const p of payments) {
    const w = p.from.toLowerCase();
    const ts = Number(p.blockTimestamp);
    const prev = byPayer.get(w);
    if (prev) {
      prev.count += 1;
      prev.first = Math.min(prev.first, ts);
      prev.last = Math.max(prev.last, ts);
    } else {
      byPayer.set(w, { count: 1, first: ts, last: ts });
    }
  }
  return Array.from(byPayer, ([wallet, { count, first, last }]) => ({
    wallet,
    payments: count,
    first_seen: new Date(first * 1000).toISOString(),
    last_seen: new Date(last * 1000).toISOString(),
  }));
}

// ── Operator seed (mirrors lib/identifyAgents.ts OPERATOR_SEED) ──────────────

const OPERATOR_SEED: Array<{ wallet: string; agent: string; registry: string; agent_link: string }> = [
  {
    wallet: "0x575267eed09c338fae5716a486a7b58a5749a292",
    agent: "[Graph Advocate](https://8004scan.io/agents/base/41034)",
    registry: "operator",
    agent_link: "https://8004scan.io/agents/base/41034",
  },
  {
    wallet: "0xe121e3a8611e1f44f7cc52892ee1117fddc8f734",
    agent: "[Graph Advocate](https://8004scan.io/agents/base/41034)",
    registry: "operator",
    agent_link: "https://8004scan.io/agents/base/41034",
  },
  {
    wallet: "0x0ff5a6ecef783bba35463ec2f8403b9b5e9e7c86",
    agent: "[Graph Advocate](https://8004scan.io/agents/base/41034)",
    registry: "operator",
    agent_link: "https://8004scan.io/agents/base/41034",
  },
];

// ── Bazaar enrichment ────────────────────────────────────────────────────────

async function fromBazaar(): Promise<
  Array<{ wallet: string; agent: string; registry: string; agent_link: string }>
> {
  try {
    const d = await fetchJSON<{
      results?: Array<{ resource: string; metadata?: { name?: string; identity?: { walletAddress?: string } } }>;
    }>("https://api.x402.org/v1/discovery/active?limit=200");
    const out: Array<{ wallet: string; agent: string; registry: string; agent_link: string }> = [];
    for (const it of d.results ?? []) {
      const wallet = it.metadata?.identity?.walletAddress?.toLowerCase();
      const name = it.metadata?.name;
      if (!wallet || !name) continue;
      out.push({
        wallet,
        agent: `[${name}](${it.resource})`,
        registry: "bazaar",
        agent_link: it.resource,
      });
    }
    return out;
  } catch (e) {
    console.warn("[bazaar] failed:", e instanceof Error ? e.message : e);
    return [];
  }
}

// ── 8004scan enrichment (with 1s/2s/4s backoff on 429) ───────────────────────

interface Scan8004Agent {
  agent_id?: string; // composite "chain:contract:tokenId"
  owner_address?: string;
  owner_ens?: string | null;
  name?: string;
  chain_id?: number;
}

function scan8004Link(agentIdFull: string | null): string {
  // Composite is "chainId:contract:tokenId" — translate to the /agents/<slug>/<id> URL
  if (!agentIdFull) return "https://8004scan.io";
  const parts = agentIdFull.split(":");
  const tokenId = parts[2] ?? parts[parts.length - 1];
  const chainId = Number(parts[0] ?? "8453");
  const slug =
    chainId === 8453
      ? "base"
      : chainId === 42161
        ? "arbitrum"
        : chainId === 137
          ? "polygon"
          : chainId === 1
            ? "ethereum"
            : String(chainId);
  return `https://8004scan.io/agents/${slug}/${tokenId}`;
}

async function from8004scan(wallet: string): Promise<AgentRow | null> {
  // 8004scan's `?search=` returns fuzzy matches — we MUST post-filter on
  // owner_address. Earlier draft of this script used `?owner_address=` which
  // isn't a real query parameter; the API silently ignored it and returned
  // the first agent in the global list (everything got tagged as "Liquios").
  const delays = [0, 1000, 2000, 4000];
  for (const delay of delays) {
    if (delay) await sleep(delay);
    try {
      const d = await fetchJSON<{ data?: Scan8004Agent[] }>(
        `https://8004scan.io/api/v1/public/agents?search=${wallet}`,
      );
      for (const a of d.data ?? []) {
        if ((a.owner_address ?? "").toLowerCase() !== wallet.toLowerCase()) continue;
        let name = a.name ?? "";
        if (!name || name.startsWith("Agent #")) {
          name = a.owner_ens ?? "";
          if (!name) continue;
        }
        const link = scan8004Link(a.agent_id ?? null);
        const label = a.chain_id === 8453 ? name : `${name} (chain ${a.chain_id})`;
        return {
          agent: `[${label}](${link})`,
          wallet,
          payments: 0,
          first_seen: "",
          last_seen: "",
          registry: "8004scan",
          agent_link: link,
        };
      }
      return null;
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      if (!msg.includes("429")) throw e;
      // 429 → keep retrying
    }
  }
  return null;
}

// ── agent0 enrichment ────────────────────────────────────────────────────────

async function fromAgent0(wallet: string): Promise<AgentRow | null> {
  // Agent0 schema has no top-level `name` field on Agent — it's only available
  // by decoding the agentURI which is typically a `data:application/json;base64,`
  // payload (matches the behaviour of scripts/refresh_known_agents.py in
  // subgraph-registry, fixed in commit a964d7b).
  const key = process.env.GRAPH_API_KEY!;
  const url = `https://gateway.thegraph.com/api/${key}/subgraphs/id/${AGENT0_BASE_SUBGRAPH_ID}`;
  const query = `query Q($w: Bytes!) {
    agents(first: 1, where: { or: [{ owner: $w }, { agentWallet: $w }, { operators_contains: [$w] }] }) {
      agentId owner agentWallet agentURI
    }
  }`;
  const delays = [0, 1000, 2000];
  for (const delay of delays) {
    if (delay) await sleep(delay);
    try {
      const d = await postGraphQL<{
        agents: Array<{ agentId: string; owner: string; agentWallet?: string; agentURI?: string }>;
      }>(url, query, { w: wallet });
      const a = d.agents?.[0];
      if (!a) return null;
      let name = `ERC-8004 #${a.agentId}`;
      const uri = a.agentURI ?? "";
      if (uri.startsWith("data:application/json;base64,")) {
        try {
          const json = JSON.parse(Buffer.from(uri.split(",", 2)[1], "base64").toString("utf8"));
          if (typeof json?.name === "string" && json.name.length) name = json.name;
        } catch {
          // ignore malformed metadata
        }
      }
      const link = `https://8004scan.io/agents/base/${a.agentId}`;
      return {
        agent: `[${name}](${link})`,
        wallet,
        payments: 0,
        first_seen: "",
        last_seen: "",
        registry: "agent0",
        agent_link: link,
      };
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      if (!msg.includes("429")) {
        console.warn(`[agent0] ${wallet.slice(0, 10)}…:`, msg);
        return null;
      }
    }
  }
  return null;
}

// ── Main enrichment ──────────────────────────────────────────────────────────

async function identifyAgents(payers: TopPayer[]): Promise<AgentRow[]> {
  const knownByWallet = new Map<string, AgentRow>();

  // 1. Operator seed + bazaar — fast, do first
  const bazaarRows = await fromBazaar();
  for (const row of [...OPERATOR_SEED, ...bazaarRows]) {
    knownByWallet.set(row.wallet.toLowerCase(), {
      agent: row.agent,
      wallet: row.wallet.toLowerCase(),
      payments: 0,
      first_seen: "",
      last_seen: "",
      registry: row.registry,
      agent_link: row.agent_link,
    });
  }

  // 2. Enrich unknown payers via 8004scan, fall back to agent0
  const unknown = payers.filter((p) => !knownByWallet.has(p.wallet));
  console.log(`[enrich] ${unknown.length} unknown wallets to check`);
  const enriched = await mapConcurrent(unknown, ENRICH_CONCURRENCY, async (p) => {
    let row = await from8004scan(p.wallet);
    if (!row) row = await fromAgent0(p.wallet);
    return row;
  });
  for (const row of enriched) {
    if (row) knownByWallet.set(row.wallet, row);
  }

  // 3. Stitch payments / first_seen / last_seen back onto the rows that
  // appear in the payers list. Drop seed/bazaar agents that haven't paid.
  const out: AgentRow[] = [];
  for (const p of payers) {
    const row = knownByWallet.get(p.wallet);
    if (!row) continue;
    out.push({ ...row, payments: p.payments, first_seen: p.first_seen, last_seen: p.last_seen });
  }
  return out.sort((a, b) => b.payments - a.payments);
}

// ── Driver ───────────────────────────────────────────────────────────────────

async function writeDirectory(file: DirectoryFile): Promise<void> {
  await mkdir(dirname(OUT_PATH), { recursive: true });
  await writeFile(OUT_PATH, JSON.stringify(file, null, 2) + "\n", "utf8");
}

async function main(): Promise<void> {
  const startedAt = Date.now();
  console.log("[build-agent-directory] starting");

  if (!process.env.GRAPH_API_KEY) {
    console.warn("[build-agent-directory] GRAPH_API_KEY not set — writing empty directory");
    await writeDirectory({
      generated_at: new Date().toISOString(),
      source: "build-time",
      payer_count: 0,
      agent_count: 0,
      agents: [],
    });
    return;
  }

  let payers: TopPayer[] = [];
  try {
    payers = await fetchTopPayers();
    console.log(`[build-agent-directory] fetched ${payers.length} top payers`);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    console.error(`[build-agent-directory] fetchTopPayers failed: ${msg}`);
    await writeDirectory({
      generated_at: new Date().toISOString(),
      source: "build-time",
      payer_count: 0,
      agent_count: 0,
      agents: [],
    });
    return;
  }

  let agents: AgentRow[] = [];
  try {
    agents = await identifyAgents(payers);
    console.log(`[build-agent-directory] enriched ${agents.length} agents`);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    console.error(`[build-agent-directory] identifyAgents failed: ${msg}`);
    agents = [];
  }

  await writeDirectory({
    generated_at: new Date().toISOString(),
    source: "build-time",
    payer_count: payers.length,
    agent_count: agents.length,
    agents,
  });

  const elapsed = ((Date.now() - startedAt) / 1000).toFixed(1);
  console.log(`[build-agent-directory] wrote ${OUT_PATH} (${agents.length} agents, ${elapsed}s)`);
}

main().catch((e) => {
  console.error("[build-agent-directory] fatal:", e);
  process.exit(1);
});
