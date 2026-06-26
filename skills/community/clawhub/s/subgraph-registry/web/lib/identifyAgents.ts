// Agent enrichment for the dashboard's payer leaderboard.
//
// Resolves a list of payer wallets into AgentRow entries by querying:
//   1. OPERATOR_SEED (inline; mirrors scripts/refresh_known_agents.py)
//   2. graphadvocate.com/bazaar/active (active x402 services)
//   3. 8004scan ?search=<wallet> exact-owner-match (with backoff on 429)
//   4. agent0-base-mainnet subgraph (catches operator-paid agents that
//      8004scan misses)
//
// Runs on ISR revalidate (not build time): page.tsx is a server component
// that calls identifyAgents() during rendering. To prevent the page render
// from blowing the Vercel function timeout on 8004scan rate-limit storms,
// the top-level `identifyAgents` is wrapped in `unstable_cache` with a 6h
// TTL — identity changes slowly compared to payments, and decoupling the
// cache TTL from the payments revalidate keeps the dashboard responsive
// even when the directory build is slow.
//
// Returns rows in the same shape page.tsx expects: { agent, wallet,
// payments, last_seen, registry, agent_link }. The `agent` field is
// markdown-wrapped `[name](link)` so the AgentLeaderboard component's
// existing extractName() keeps working unchanged.

import { unstable_cache } from "next/cache";

import type { TopPayer } from "./subgraph";

const AGENT0_BASE_SUBGRAPH_ID = "43s9hQRurMGjuYnC1r2ZwS6xSQktbFyXMPMqGKUFJojb";
const GA_8004_BASE_AGENT_ID = "8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:41034";

// Bounded concurrency for the per-payer enrichment pass. Keeps 8004scan
// happy (single-digit RPS) but parallelises enough that 30-50 wallets
// finish in seconds rather than ~1 min sequential.
const ENRICH_CONCURRENCY = 5;

// Directory cache TTL — identity changes much more slowly than payment
// flow, so we decouple this from REVALIDATE_SECONDS. 6h is a reasonable
// trade-off between staleness and load.
const DIRECTORY_TTL_SECONDS = 6 * 60 * 60;

const CHAIN_SLUG: Record<number, string> = {
  1: "ethereum", 8453: "base", 42161: "arbitrum", 10: "optimism",
  56: "bsc", 137: "polygon", 42220: "celo", 130: "unichain",
  1923: "swellchain", 2741: "abstract", 5042002: "ronin",
  84532: "base-sepolia", 11155111: "sepolia",
};

function scan8004(agentId: string | null | undefined): string {
  if (!agentId) return "https://8004scan.io";
  const parts = agentId.split(":");
  if (parts.length === 3 && /^\d+$/.test(parts[0]) && /^\d+$/.test(parts[2])) {
    const slug = CHAIN_SLUG[Number(parts[0])];
    if (slug) return `https://8004scan.io/agents/${slug}/${parts[2]}`;
  }
  return "https://8004scan.io";
}

function basescan(wallet: string): string {
  return `https://basescan.org/address/${wallet}`;
}

// Mirror of OPERATOR_SEED in scripts/refresh_known_agents.py.
// Format: [wallet, name, source, link]. All three GA-controlled wallets
// surface as the same agent identity to match the single-name format the
// other identified agents use.
const OPERATOR_SEED: [string, string, string, string][] = [
  ["0x575267eed09c338fae5716a486a7b58a5749a292", "graphadvocate", "operator", scan8004(GA_8004_BASE_AGENT_ID)],
  ["0xe121e3a8611e1f44f7cc52892ee1117fddc8f734", "graphadvocate", "operator", scan8004(GA_8004_BASE_AGENT_ID)],
  ["0x0ff5a6ecef783bba35463ec2f8403b9b5e9e7c86", "graphadvocate", "operator", scan8004(GA_8004_BASE_AGENT_ID)],
];

// ── HTTP helpers ─────────────────────────────────────────────────────────────

interface FetchOpts {
  timeoutMs?: number;
}

async function fetchJSON<T>(url: string, opts: FetchOpts = {}): Promise<T | null> {
  const { timeoutMs = 8000 } = opts;
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      headers: { "User-Agent": "x402-watch-build/1.0", Accept: "application/json" },
      signal: controller.signal,
      // No revalidate — this runs inside unstable_cache with its own TTL.
      cache: "no-store",
    });
    if (!res.ok) {
      if (res.status === 429) throw new RateLimitError();
      return null;
    }
    return (await res.json()) as T;
  } catch (e) {
    if (e instanceof RateLimitError) throw e;
    return null;
  } finally {
    clearTimeout(t);
  }
}

async function postJSON<T>(url: string, body: unknown, opts: FetchOpts = {}): Promise<T | null> {
  const { timeoutMs = 15_000 } = opts;
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "User-Agent": "x402-watch-build/1.0",
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      signal: controller.signal,
      cache: "no-store",
    });
    if (!res.ok) {
      if (res.status === 429) throw new RateLimitError();
      return null;
    }
    return (await res.json()) as T;
  } catch (e) {
    if (e instanceof RateLimitError) throw e;
    return null;
  } finally {
    clearTimeout(t);
  }
}

class RateLimitError extends Error {
  constructor() { super("rate limit"); this.name = "RateLimitError"; }
}

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

/** Run `fn` against each item in `items` with bounded concurrency.
 *  Preserves input order in the output array. */
async function mapConcurrent<T, R>(
  items: T[],
  limit: number,
  fn: (item: T, idx: number) => Promise<R>,
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let nextIdx = 0;
  async function worker(): Promise<void> {
    while (true) {
      const i = nextIdx++;
      if (i >= items.length) return;
      results[i] = await fn(items[i], i);
    }
  }
  const workers = Array.from({ length: Math.min(limit, items.length) }, () => worker());
  await Promise.all(workers);
  return results;
}

// ── Bazaar fetch ─────────────────────────────────────────────────────────────

interface BazaarItem {
  pay_to?: string;
  resource?: string;
  erc8004_agent?: {
    name?: string;
    ens?: string;
    owner?: string;
    agent_id?: string;
  };
}

async function fromBazaar(): Promise<[string, string, string, string][]> {
  // One retry on 429 — bazaar is graphadvocate.com which can throttle. If
  // it's still 429 on retry we proceed without bazaar rows rather than
  // throwing into identifyAgents and crashing the page render.
  const delays = [0, 1500];
  let d: { results?: BazaarItem[] } | null = null;
  for (let i = 0; i < delays.length; i++) {
    if (delays[i] > 0) await sleep(delays[i]);
    try {
      d = await fetchJSON<{ results?: BazaarItem[] }>(
        "https://graphadvocate.com/bazaar/active",
        { timeoutMs: 10_000 },
      );
      break;
    } catch (e) {
      if (e instanceof RateLimitError && i + 1 < delays.length) continue;
      d = null;
      break;
    }
  }
  if (!d || !d.results) return [];
  const rows: [string, string, string, string][] = [];
  for (const it of d.results) {
    const payTo = (it.pay_to ?? "").toLowerCase();
    const e8 = it.erc8004_agent ?? {};
    const name = e8.name ?? e8.ens ?? hostname(it.resource ?? "") ?? "?";
    const agentIdFull = e8.agent_id ?? null;
    const link = agentIdFull ? scan8004(agentIdFull) : basescan(payTo);
    if (payTo.startsWith("0x")) rows.push([payTo, String(name), "bazaar", link]);
    const owner = (e8.owner ?? "").toLowerCase();
    if (owner.startsWith("0x") && owner !== payTo) {
      rows.push([
        owner,
        agentIdFull ? `ERC-8004 #${agentIdFull}` : String(name),
        "erc8004",
        scan8004(agentIdFull),
      ]);
    }
  }
  return rows;
}

function hostname(url: string): string | null {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return null;
  }
}

// ── 8004scan exact-wallet enrichment ─────────────────────────────────────────

interface Scan8004Agent {
  owner_address?: string;
  owner_ens?: string;
  name?: string;
  chain_id?: number;
  agent_id?: string;
}

async function enrichFrom8004scan(
  wallet: string,
): Promise<[string, string, string, string] | null> {
  // Exponential backoff, max 3 retries. Skip-on-final-failure so the build
  // doesn't fail if 8004scan is degraded.
  const delays = [1000, 2000, 4000];
  for (let attempt = 0; attempt < delays.length; attempt++) {
    try {
      const d = await fetchJSON<{ data?: Scan8004Agent[] }>(
        `https://8004scan.io/api/v1/public/agents?search=${wallet}`,
        { timeoutMs: 8000 },
      );
      if (!d || !d.data) return null;
      for (const a of d.data) {
        if ((a.owner_address ?? "").toLowerCase() !== wallet.toLowerCase()) continue;
        let name = a.name ?? "";
        if (!name || name.startsWith("Agent #")) {
          name = a.owner_ens ?? "";
          if (!name) continue;
        }
        const chain = a.chain_id;
        const agentIdFull = a.agent_id ?? null;
        const label = chain === 8453 ? name : `${name} (chain ${chain})`;
        return [wallet.toLowerCase(), label, "8004scan", scan8004(agentIdFull)];
      }
      return null;
    } catch (e) {
      if (e instanceof RateLimitError && attempt < delays.length - 1) {
        await sleep(delays[attempt]);
        continue;
      }
      // Any other error: skip this wallet, don't block the build.
      return null;
    }
  }
  return null;
}

// ── agent0 subgraph enrichment ───────────────────────────────────────────────

interface Agent0Result {
  data?: {
    agents?: {
      agentId?: string;
      owner?: string;
      agentWallet?: string;
      agentURI?: string;
      operators?: string[];
    }[];
  };
  errors?: { message: string }[];
}

async function enrichFromAgent0(
  wallet: string,
): Promise<[string, string, string, string] | null> {
  const key = process.env.GRAPH_API_KEY;
  if (!key) return null;
  const url = `https://gateway.thegraph.com/api/${key}/subgraphs/id/${AGENT0_BASE_SUBGRAPH_ID}`;
  // Match the exact query shape refresh_known_agents.py uses — verified
  // working against the live agent0 subgraph (returns matches for known
  // owner/agentWallet/operators wallets, empty array for unknowns).
  const query = `
    query($w: Bytes!) {
      agents(first: 5, where: {or: [
        {owner: $w},
        {agentWallet: $w},
        {operators_contains: [$w]}
      ]}) {
        agentId owner agentWallet agentURI operators
      }
    }
  `;
  const w = wallet.toLowerCase();
  // Same backoff envelope as 8004scan: catch 429 storms instead of
  // crashing the page render via RateLimitError bubbling up.
  const delays = [1000, 2000, 4000];
  let d: Agent0Result | null = null;
  for (let attempt = 0; attempt < delays.length; attempt++) {
    try {
      d = await postJSON<Agent0Result>(url, { query, variables: { w } });
      break;
    } catch (e) {
      if (e instanceof RateLimitError && attempt < delays.length - 1) {
        await sleep(delays[attempt]);
        continue;
      }
      return null;
    }
  }
  if (!d || d.errors || !d.data?.agents) return null;
  for (const a of d.data.agents) {
    if (!a) continue;
    // Defense-in-depth: explicit post-filter. The where:{or:[...]} should
    // already scope by wallet, but if a future schema shift degrades the
    // filter we won't accidentally attribute an unrelated agent to this
    // payer wallet.
    const isOwner = (a.owner ?? "").toLowerCase() === w;
    const isAgentWallet = (a.agentWallet ?? "").toLowerCase() === w;
    const isOperator = (a.operators ?? []).some((op) => (op ?? "").toLowerCase() === w);
    if (!isOwner && !isAgentWallet && !isOperator) continue;

    const agentId = a.agentId ?? "";
    let name = `ERC-8004 #${agentId}`;
    const uri = a.agentURI ?? "";
    if (uri.startsWith("data:application/json;base64,")) {
      try {
        const meta = JSON.parse(
          Buffer.from(uri.split(",", 2)[1] ?? "", "base64").toString("utf8"),
        ) as { name?: string };
        if (meta.name) name = meta.name;
      } catch {
        // ignore parse errors
      }
    }
    if (!(isOwner || isAgentWallet)) name = `${name} (operator)`;
    const agentIdFull = agentId
      ? `8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:${agentId}`
      : null;
    return [w, name, "agent0", scan8004(agentIdFull)];
  }
  return null;
}

// ── Top-level identify ───────────────────────────────────────────────────────

export interface AgentRow {
  agent: string;
  wallet: string;
  payments: number;
  first_seen: string;
  last_seen: string;
  registry: string;
  agent_link: string;
}

/**
 * Resolve a list of payers (from fetchTopPayers) into AgentRow entries.
 * Only rows that resolve to a registered identity are returned — unknown
 * wallets fall through and are excluded from the leaderboard but still
 * appear in the Recent Activity feed as a shortened address.
 *
 * Wrapped in `unstable_cache` with a 6h TTL — agent identity changes
 * slowly so we don't need to rebuild this on every 5-minute page
 * revalidation. Cache key includes the set of unknown wallets so it
 * invalidates automatically when new payers show up.
 */
async function identifyAgentsImpl(payers: TopPayer[]): Promise<AgentRow[]> {
  // Source 1+2: operator seed and bazaar (one network call total)
  const bazaarRows = await fromBazaar();
  const directory = new Map<string, [string, string, string, string]>();
  for (const row of [...OPERATOR_SEED, ...bazaarRows]) {
    const w = row[0].toLowerCase();
    if (!directory.has(w)) directory.set(w, row);
  }

  // Source 3+4: per-payer 8004scan + agent0 fallback with bounded
  // concurrency. With ENRICH_CONCURRENCY=5, 50 unknown wallets resolve
  // in ~ceil(50/5) * avg-call-time ≈ 1-2s under healthy conditions, and
  // bounded ~30s under 8004scan rate-limit storms (vs 60s+ sequential).
  const unknown = payers.filter((p) => !directory.has(p.wallet.toLowerCase()));
  const enriched = await mapConcurrent(unknown, ENRICH_CONCURRENCY, async (p) => {
    const w = p.wallet.toLowerCase();
    const fromScan = await enrichFrom8004scan(w);
    if (fromScan) return { wallet: w, row: fromScan };
    const fromAgent0 = await enrichFromAgent0(w);
    if (fromAgent0) return { wallet: w, row: fromAgent0 };
    return null;
  });
  for (const r of enriched) {
    if (!r) continue;
    if (!directory.has(r.wallet)) directory.set(r.wallet, r.row);
  }

  // Join directory with payer counts. Drop directory entries that have no
  // payments to the gateway (they're seeded operators that haven't paid yet).
  const statsByWallet = new Map(payers.map((p) => [p.wallet.toLowerCase(), p]));
  const rows: AgentRow[] = [];
  for (const [wallet, [, name, source, link]] of directory.entries()) {
    const stats = statsByWallet.get(wallet);
    if (!stats) continue;
    rows.push({
      // Markdown-wrapped to match the format AgentLeaderboard.extractName() expects.
      agent: `[${name}](${link})`,
      wallet,
      payments: stats.payments,
      first_seen: stats.first_seen,
      last_seen: stats.last_seen,
      registry: source,
      agent_link: link,
    });
  }
  rows.sort((a, b) => b.payments - a.payments);
  return rows;
}

/**
 * Public entrypoint. Caches the directory build for 6h so the expensive
 * 8004scan + agent0 fan-out doesn't run on every ISR revalidation. The
 * cache key includes the sorted set of payer wallets, so it invalidates
 * automatically when a new payer hits the gateway.
 */
export async function identifyAgents(payers: TopPayer[]): Promise<AgentRow[]> {
  // Stable cache key: sort wallets so order-changes don't bust the cache.
  const sortedWallets = payers.map((p) => p.wallet.toLowerCase()).sort();
  // Hash via a simple FNV-1a so the key stays short even at 100s of payers.
  const walletHash = fnv1a(sortedWallets.join(","));

  const cached = unstable_cache(
    async () => identifyAgentsImpl(payers),
    ["identifyAgents", walletHash],
    { revalidate: DIRECTORY_TTL_SECONDS, tags: ["agent-directory"] },
  );
  return cached();
}

function fnv1a(s: string): string {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
  }
  return h.toString(16);
}
