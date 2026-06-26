// x402-omnigraph subgraph client — server-side only.
//
// Replaces the 14 Dune queries previously used by the dashboard. Reads live
// from the published subgraph (Cb56epg3EvQ6JRpPfknbkM54QxpzTvLa7mwKNQQfUyoj)
// via The Graph Gateway and derives every dashboard panel from a single
// paginated fetch of `X402Payment` rows scoped to the gateway recipient.
//
// Auth: GRAPH_API_KEY env var (same key used by refresh_known_agents.py for
// the agent0 enrichment path). NEVER log the key value.

import { cache } from "react";

import type { ConcentrationRow } from "@/components/Concentration";
import type { CumulativePoint } from "@/components/CumulativeChart";
import type { DailyPoint } from "@/components/DailyChart";
import type { HeatPoint } from "@/components/ActivityHeatmap";
import type { NRPoint } from "@/components/NewVsReturning";
import type { PaymentRow } from "@/components/RecentActivity";

// ── Constants ────────────────────────────────────────────────────────────────

// The Graph's x402 gateway payTo address on Base. Lowercased to match the
// Bytes-comparison semantics of the subgraph's `to` field.
export const GATEWAY_RECIPIENT = "0x79dc34e41b2b591078d3de222c43ecaabd52fccb";

const SUBGRAPH_ID = "Cb56epg3EvQ6JRpPfknbkM54QxpzTvLa7mwKNQQfUyoj";

// 5-minute revalidate. Subgraph is live (indexes through current block) and
// the gateway gets a handful of payments per day at most, so 5-min staleness
// preserves the "real-time dashboard" feel that wasn't possible with the
// daily Dune cron without burning gateway query budget.
//
// IMPORTANT: app/page.tsx exports `revalidate = 300` as a literal because
// Next.js requires a static literal for route segment config. The two values
// must stay in sync; bumping one without the other will break the contract
// (the page caches for one window but fetches refresh at the other).
export const REVALIDATE_SECONDS = 300;

// Safety cap on the paginated payment fetch. Current dataset is ~143 rows;
// 5_000 = ~5y at current pace and ~5 pages of gateway queries worst case.
// A runaway loop is then bounded to single-digit gateway calls.
const MAX_ROWS = 5_000;
const PAGE_SIZE = 1000;

// ── Gateway client ────────────────────────────────────────────────────────────

function gatewayUrl(): string {
  const key = process.env.GRAPH_API_KEY;
  if (!key) {
    // Production should fail loudly — silent empty dashboards are a worse
    // signal for ops than a hard error. Local dev keeps the soft-warn path
    // so contributors without a key can still iterate on the UI shell.
    if (process.env.NODE_ENV === "production") {
      throw new Error(
        "[subgraph] GRAPH_API_KEY is required in production but not set",
      );
    }
    console.warn(
      "[subgraph] GRAPH_API_KEY not set; queries will return empty results",
    );
    return "";
  }
  return `https://gateway.thegraph.com/api/${key}/subgraphs/id/${SUBGRAPH_ID}`;
}

interface GraphQLResponse<T> {
  data?: T;
  errors?: { message: string }[];
}

/**
 * POST a GraphQL query to the gateway. Logs failures with a tag-able prefix
 * but returns null on any error so callers can fall back gracefully.
 *
 * Includes one transparent retry on transient gateway errors (the gateway
 * occasionally returns "bad indexers: Timeout" on the first hit and then
 * succeeds immediately on retry).
 */
export async function postGraphQL<T>(
  query: string,
  variables: Record<string, unknown> = {},
  opName = "query",
): Promise<T | null> {
  const url = gatewayUrl();
  if (!url) return null;
  const body = JSON.stringify({ query, variables });
  const attempts = 2;
  for (let attempt = 0; attempt < attempts; attempt++) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
        next: { revalidate: REVALIDATE_SECONDS, tags: ["subgraph:x402-omnigraph"] },
      });
      if (!res.ok) {
        console.warn(
          `[subgraph] HTTP ${res.status} from gateway (op=${opName}, attempt=${attempt + 1})`,
        );
        if (attempt + 1 < attempts) {
          await new Promise((r) => setTimeout(r, 500 * (attempt + 1)));
          continue;
        }
        return null;
      }
      const json = (await res.json()) as GraphQLResponse<T>;
      if (json.errors && json.errors.length) {
        console.warn(
          `[subgraph] GraphQL error (op=${opName}, attempt=${attempt + 1}): ${json.errors[0].message.slice(0, 200)}`,
        );
        if (attempt + 1 < attempts) {
          await new Promise((r) => setTimeout(r, 500 * (attempt + 1)));
          continue;
        }
        return null;
      }
      return json.data ?? null;
    } catch (e) {
      console.warn(
        `[subgraph] fetch failed (op=${opName}, attempt=${attempt + 1}):`,
        e,
      );
      if (attempt + 1 < attempts) {
        await new Promise((r) => setTimeout(r, 500 * (attempt + 1)));
        continue;
      }
      return null;
    }
  }
  return null;
}

// ── Raw entity types (subset of the schema we use) ───────────────────────────

interface RawPayment {
  id: string;
  blockNumber: string;
  blockTimestamp: string;
  transactionHash: string;
  from: string;
  to: string;
  amountDecimal: string;
}

interface RawSummary {
  id: string;
  address: string;
  role: string;
  totalPayments: string;
  totalVolumeDecimal: string;
  firstPaymentTimestamp: string | null;
  lastPaymentTimestamp: string | null;
}

interface PaymentsPage {
  x402Payments: RawPayment[];
}

interface SummariesQuery {
  x402AddressSummaries: RawSummary[];
}

// ── Workhorse: paginated payments to the gateway ──────────────────────────────

/**
 * Paginated id_gt cursor fetch of every X402Payment where to=gateway.
 * The dashboard derives DAILY, CUMULATIVE, CONCENTRATION, NEW_PAYERS,
 * ACTIVITY_HEATMAP, TRENDS, and TOP_PAYERS from this single dataset to
 * minimize gateway query cost.
 *
 * Wrapped in React's `cache()` for per-request memoization — the parallel
 * `Promise.all` in page.tsx hits this many times in one render but
 * dedupes to a single execution. NOT a cross-request cache: Next.js
 * `next: { revalidate }` on the underlying fetch handles cross-request
 * caching at the data layer.
 */
export const getGatewayPaymentsAll = cache(async (): Promise<RawPayment[]> => {
  // Use Bytes! cursor type — X402Payment.id is Bytes. "0x" is the
  // canonical empty-Bytes literal and lexicographically precedes every
  // real ID, so the first page returns from the start.
  const query = `
    query Payments($to: Bytes!, $cursor: Bytes!, $first: Int!) {
      x402Payments(
        where: { to: $to, id_gt: $cursor }
        first: $first
        orderBy: id
        orderDirection: asc
      ) {
        id
        blockNumber
        blockTimestamp
        transactionHash
        from
        to
        amountDecimal
      }
    }
  `;

  const all: RawPayment[] = [];
  let cursor = "0x";
  while (all.length < MAX_ROWS) {
    const data = await postGraphQL<PaymentsPage>(
      query,
      { to: GATEWAY_RECIPIENT, cursor, first: PAGE_SIZE },
      "getGatewayPaymentsAll",
    );
    // Distinguish "transient error → null" (postGraphQL already retried;
    // bail rather than treat as EOF and lose the whole dataset for 5min)
    // from "successful empty page → []" (true EOF).
    if (data === null) {
      console.warn(
        `[subgraph] getGatewayPaymentsAll: page fetch failed at cursor=${cursor.slice(0, 12)}…, returning partial (${all.length} rows)`,
      );
      break;
    }
    const rows = data.x402Payments ?? [];
    if (rows.length === 0) break;
    all.push(...rows);
    if (rows.length < PAGE_SIZE) break;
    cursor = rows[rows.length - 1].id;
  }
  return all;
});

// ── Individual fetchers (cards keyed by Dune query name) ─────────────────────

export interface LifetimeTotals {
  total_usdc: number;
  total_payments: number;
  first_payment_at: string;
  last_payment_at: string;
}

/** LIFETIME_TOTALS — Hero card top numbers.
 *
 *  Derives from the workhorse dataset as the single source of truth so
 *  Hero numbers exactly match the cumulative chart totals (no UI
 *  inconsistency between the summary entity lagging vs derived totals).
 *  The summary entity is still queried as a cheap sanity check, but
 *  derived values win.
 */
export async function fetchLifetimeTotals(): Promise<LifetimeTotals> {
  const payments = await getGatewayPaymentsAll();
  const total_usdc = payments.reduce((s, p) => s + Number(p.amountDecimal), 0);
  const sorted = [...payments].sort(
    (a, b) => Number(a.blockTimestamp) - Number(b.blockTimestamp),
  );
  return {
    total_usdc,
    total_payments: payments.length,
    first_payment_at: sorted.length ? tsToIso(sorted[0].blockTimestamp) : "",
    last_payment_at: sorted.length ? tsToIso(sorted[sorted.length - 1].blockTimestamp) : "",
  };
}

/** Sanity-check: read the X402AddressSummary entity directly for the gateway
 *  RECIPIENT. Schema note: the ID is role-prefixed ("0x01000000" + address),
 *  so the plural+where form is what works against the live subgraph. Returned
 *  for diagnostics / future use but NOT used as the Hero source of truth. */
export async function fetchGatewaySummary(): Promise<LifetimeTotals | null> {
  const query = `
    query Summaries($a: Bytes!) {
      x402AddressSummaries(
        where: { address: $a, role: RECIPIENT }
        first: 1
      ) {
        id
        address
        role
        totalPayments
        totalVolumeDecimal
        firstPaymentTimestamp
        lastPaymentTimestamp
      }
    }
  `;
  const data = await postGraphQL<SummariesQuery>(
    query,
    { a: GATEWAY_RECIPIENT },
    "fetchGatewaySummary",
  );
  const s = data?.x402AddressSummaries?.[0];
  if (!s) return null;
  return {
    total_usdc: Number(s.totalVolumeDecimal ?? 0),
    total_payments: Number(s.totalPayments ?? 0),
    first_payment_at: tsToIso(s.firstPaymentTimestamp),
    last_payment_at: tsToIso(s.lastPaymentTimestamp),
  };
}

/** DAILY — per-day payment counts for the gateway. */
export async function fetchDaily(): Promise<DailyPoint[]> {
  const payments = await getGatewayPaymentsAll();
  const byDay = new Map<string, number>();
  for (const p of payments) {
    const day = dayKey(p.blockTimestamp);
    byDay.set(day, (byDay.get(day) ?? 0) + 1);
  }
  return Array.from(byDay.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([day, payments]) => ({ day, payments }));
}

/** CUMULATIVE — running sum of USDC paid to the gateway. */
export async function fetchCumulative(): Promise<CumulativePoint[]> {
  const payments = await getGatewayPaymentsAll();
  const byDayUsdc = new Map<string, number>();
  for (const p of payments) {
    const day = dayKey(p.blockTimestamp);
    byDayUsdc.set(day, (byDayUsdc.get(day) ?? 0) + Number(p.amountDecimal));
  }
  let running = 0;
  return Array.from(byDayUsdc.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([day, amount]) => {
      running += amount;
      return { day, cumulative_usdc: running };
    });
}

/** TOP_PAYERS — payer wallets ranked by payment count to the gateway.
 *  Returned for identifyAgents() consumption — page.tsx no longer renders
 *  this directly, but the enrichment pass needs the wallet list. */
export interface TopPayer {
  wallet: string;
  payments: number;
  first_seen: string;
  last_seen: string;
}

export async function fetchTopPayers(): Promise<TopPayer[]> {
  const payments = await getGatewayPaymentsAll();
  const byPayer = new Map<string, { count: number; first: number; last: number }>();
  for (const p of payments) {
    const w = p.from.toLowerCase();
    const ts = Number(p.blockTimestamp);
    const prev = byPayer.get(w);
    if (prev) {
      prev.count += 1;
      if (ts > prev.last) prev.last = ts;
      if (ts < prev.first) prev.first = ts;
    } else {
      byPayer.set(w, { count: 1, first: ts, last: ts });
    }
  }
  return Array.from(byPayer.entries())
    .map(([wallet, v]) => ({
      wallet,
      payments: v.count,
      first_seen: tsToIso(v.first),
      last_seen: tsToIso(v.last),
    }))
    .sort((a, b) => b.payments - a.payments);
}

/** CONCENTRATION — payer cohort buckets (1, 2-5, 6-20, 21+). */
export async function fetchConcentration(): Promise<ConcentrationRow[]> {
  const payers = await fetchTopPayers();
  const buckets = [
    { bucket: "1 payment", min: 1, max: 1, payers: 0, payments: 0 },
    { bucket: "2–5 payments", min: 2, max: 5, payers: 0, payments: 0 },
    { bucket: "6–20 payments", min: 6, max: 20, payers: 0, payments: 0 },
    { bucket: "21+ payments", min: 21, max: Infinity, payers: 0, payments: 0 },
  ];
  for (const p of payers) {
    for (const b of buckets) {
      if (p.payments >= b.min && p.payments <= b.max) {
        b.payers += 1;
        b.payments += p.payments;
        break;
      }
    }
  }
  const total = buckets.reduce((s, b) => s + b.payments, 0);
  return buckets
    .filter((b) => b.payers > 0)
    .map((b) => ({
      bucket: b.bucket,
      payers: b.payers,
      payments: b.payments,
      share: total > 0 ? (b.payments / total) * 100 : 0,
    }));
}

/** NEW_PAYERS — per-day count of first-time payers to the gateway. */
export interface NewPayerRow {
  day: string;
  new_payers: number;
}

export async function fetchNewPayers(): Promise<NewPayerRow[]> {
  const payments = await getGatewayPaymentsAll();
  // first-seen day per payer
  const firstSeen = new Map<string, number>();
  for (const p of payments) {
    const w = p.from.toLowerCase();
    const ts = Number(p.blockTimestamp);
    const prev = firstSeen.get(w);
    if (prev === undefined || ts < prev) firstSeen.set(w, ts);
  }
  const byDay = new Map<string, number>();
  for (const ts of firstSeen.values()) {
    const day = dayKey(String(ts));
    byDay.set(day, (byDay.get(day) ?? 0) + 1);
  }
  return Array.from(byDay.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([day, new_payers]) => ({ day, new_payers }));
}

/** RECENT_PAYMENTS — last 50 payments to the gateway. Direct query (cheaper
 *  than scanning the whole dataset).
 *
 *  Secondary order on id desc to break ties when multiple payments share a
 *  blockTimestamp (very common: bursts of 5+ payments from the same payer
 *  within seconds in the same block). Without a tie-breaker the top-of-list
 *  flickers between renders. */
export async function fetchRecentPayments(limit = 50): Promise<PaymentRow[]> {
  const query = `
    query Recent($to: Bytes!, $first: Int!) {
      x402Payments(
        where: { to: $to }
        first: $first
        orderBy: blockTimestamp
        orderDirection: desc
      ) {
        id
        from
        amountDecimal
        blockTimestamp
        transactionHash
      }
    }
  `;
  const data = await postGraphQL<{
    x402Payments: {
      id: string;
      from: string;
      amountDecimal: string;
      blockTimestamp: string;
      transactionHash: string;
    }[];
  }>(query, { to: GATEWAY_RECIPIENT, first: limit }, "fetchRecentPayments");
  const rows = data?.x402Payments ?? [];
  // Stable secondary sort by id desc for tie-breaking (gateway has no
  // multi-key orderBy). Fetch a hair more than needed and slice if the
  // stable sort changes order around the boundary.
  const sorted = [...rows].sort((a, b) => {
    const t = Number(b.blockTimestamp) - Number(a.blockTimestamp);
    if (t !== 0) return t;
    return b.id.localeCompare(a.id);
  });
  return sorted.slice(0, limit).map((r) => ({
    wallet: r.from.toLowerCase(),
    amount_usdc: Number(r.amountDecimal),
    block_time: tsToIso(r.blockTimestamp),
    tx_hash: r.transactionHash,
  }));
}

/** ACTIVITY_HEATMAP — 7x24 matrix of payment counts by UTC day-of-week and hour. */
export async function fetchActivityHeatmap(): Promise<HeatPoint[]> {
  const payments = await getGatewayPaymentsAll();
  const matrix: number[][] = Array.from({ length: 7 }, () => Array(24).fill(0));
  for (const p of payments) {
    const d = new Date(Number(p.blockTimestamp) * 1000);
    const dow = d.getUTCDay();
    const hour = d.getUTCHours();
    matrix[dow][hour] += 1;
  }
  const out: HeatPoint[] = [];
  for (let dow = 0; dow < 7; dow++) {
    for (let hour = 0; hour < 24; hour++) {
      out.push({ day_of_week: dow, hour, count: matrix[dow][hour] });
    }
  }
  return out;
}

/** HOURS_SINCE — single-row hours-since-last-payment. Unused by page.tsx
 *  (last-paid timestamp is sourced from fetchRecentPayments), but kept as
 *  a typed helper for future use. */
export async function fetchHoursSinceLastPayment(): Promise<number> {
  const totals = await fetchLifetimeTotals();
  const t = Date.parse(totals.last_payment_at);
  if (!Number.isFinite(t)) return 0;
  return (Date.now() - t) / 3_600_000;
}

/** INTER_ARRIVAL — placeholder helper for the time-between-payments
 *  distribution (currently unused by page.tsx; left in for future cards). */
export async function fetchInterArrival(): Promise<{ wallet: string; gaps_seconds: number[] }[]> {
  const payments = await getGatewayPaymentsAll();
  const byPayer = new Map<string, number[]>();
  for (const p of payments) {
    const w = p.from.toLowerCase();
    const arr = byPayer.get(w) ?? [];
    arr.push(Number(p.blockTimestamp));
    byPayer.set(w, arr);
  }
  const out: { wallet: string; gaps_seconds: number[] }[] = [];
  for (const [wallet, ts] of byPayer.entries()) {
    if (ts.length < 2) continue;
    ts.sort((a, b) => a - b);
    const gaps: number[] = [];
    for (let i = 1; i < ts.length; i++) gaps.push(ts[i] - ts[i - 1]);
    out.push({ wallet, gaps_seconds: gaps });
  }
  return out;
}

/** ACTIVE_DAYS — distinct active days per payer (unused by page.tsx today). */
export async function fetchActiveDaysShare(): Promise<{ wallet: string; active_days: number }[]> {
  const payments = await getGatewayPaymentsAll();
  const byPayer = new Map<string, Set<string>>();
  for (const p of payments) {
    const w = p.from.toLowerCase();
    const day = dayKey(p.blockTimestamp);
    const set = byPayer.get(w) ?? new Set<string>();
    set.add(day);
    byPayer.set(w, set);
  }
  return Array.from(byPayer.entries())
    .map(([wallet, set]) => ({ wallet, active_days: set.size }))
    .sort((a, b) => b.active_days - a.active_days);
}

/** TRENDS — 24h / 7d / 30d payment & USDC totals for the gateway. */
export interface TrendsRow {
  payments_24h: number;
  payments_7d: number;
  payments_30d: number;
  usdc_24h: number;
  usdc_7d: number;
  usdc_30d: number;
}

export async function fetchTrends(): Promise<TrendsRow> {
  const payments = await getGatewayPaymentsAll();
  const nowSec = Date.now() / 1000;
  const w24 = nowSec - 86_400;
  const w7 = nowSec - 7 * 86_400;
  const w30 = nowSec - 30 * 86_400;
  const r: TrendsRow = {
    payments_24h: 0, payments_7d: 0, payments_30d: 0,
    usdc_24h: 0, usdc_7d: 0, usdc_30d: 0,
  };
  for (const p of payments) {
    const ts = Number(p.blockTimestamp);
    const amt = Number(p.amountDecimal);
    if (ts >= w30) { r.payments_30d += 1; r.usdc_30d += amt; }
    if (ts >= w7)  { r.payments_7d  += 1; r.usdc_7d  += amt; }
    if (ts >= w24) { r.payments_24h += 1; r.usdc_24h += amt; }
  }
  return r;
}

// ── Derivers used by page.tsx (kept exported for reuse in tests/scripts) ──

/**
 * Compute per-week new-vs-returning AGENT cohorts (not payment counts).
 *
 * For each week:
 *  - new_agents     = count of payers whose first-ever payment is in this week
 *  - returning_agents = count of payers active this week whose first-ever
 *                       payment was BEFORE this week
 *
 * Both sides are distinct-payer counts (units match), so the stacked bar
 * is semantically consistent. The previous implementation mixed payment
 * count (DailyPoint.payments) with payer count (NewPayerRow.new_payers),
 * which made the "returning" bar wrong.
 */
export async function fetchNewVsReturningByWeek(): Promise<NRPoint[]> {
  const payments = await getGatewayPaymentsAll();

  // Per-payer: first-seen timestamp + set of active weeks
  const firstSeenByPayer = new Map<string, number>();
  const activeWeeksByPayer = new Map<string, Set<string>>();
  for (const p of payments) {
    const w = p.from.toLowerCase();
    const ts = Number(p.blockTimestamp);
    const wkStart = isoWeekStart(dayKey(p.blockTimestamp));
    const prev = firstSeenByPayer.get(w);
    if (prev === undefined || ts < prev) firstSeenByPayer.set(w, ts);
    const set = activeWeeksByPayer.get(w) ?? new Set<string>();
    set.add(wkStart);
    activeWeeksByPayer.set(w, set);
  }

  // Invert: per-week set of active payers
  const activePayersByWeek = new Map<string, Set<string>>();
  for (const [payer, weeks] of activeWeeksByPayer.entries()) {
    for (const wk of weeks) {
      const s = activePayersByWeek.get(wk) ?? new Set<string>();
      s.add(payer);
      activePayersByWeek.set(wk, s);
    }
  }

  // Build NRPoint per week with distinct-payer counts on both sides.
  const weeks = Array.from(activePayersByWeek.keys()).sort();
  const out: NRPoint[] = [];
  for (const wk of weeks) {
    const wkStartSec = Date.parse(wk + "T00:00:00Z") / 1000;
    const wkEndSec = wkStartSec + 7 * 86_400;
    const active = activePayersByWeek.get(wk) ?? new Set<string>();
    let newAgents = 0;
    let returning = 0;
    for (const payer of active) {
      const first = firstSeenByPayer.get(payer) ?? Number.POSITIVE_INFINITY;
      if (first >= wkStartSec && first < wkEndSec) newAgents += 1;
      else returning += 1;
    }
    out.push({ week: wk, new_agents: newAgents, returning_agents: returning });
  }
  return out.slice(-8);
}

// ── Small helpers ────────────────────────────────────────────────────────────

function tsToIso(ts: string | number | null | undefined): string {
  if (ts === null || ts === undefined || ts === "") return "";
  const n = typeof ts === "string" ? Number(ts) : ts;
  if (!Number.isFinite(n) || n <= 0) return "";
  return new Date(n * 1000).toISOString();
}

function dayKey(ts: string | number): string {
  const n = typeof ts === "string" ? Number(ts) : ts;
  return new Date(n * 1000).toISOString().slice(0, 10);
}

function isoWeekStart(dayStr: string): string {
  const d = new Date(dayStr + "T00:00:00Z");
  if (Number.isNaN(d.getTime())) return dayStr;
  const dow = d.getUTCDay(); // 0=Sun
  const offset = (dow + 6) % 7; // make Monday=0
  d.setUTCDate(d.getUTCDate() - offset);
  return d.toISOString().slice(0, 10);
}
