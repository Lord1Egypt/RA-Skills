import { ActivityHeatmap } from "@/components/ActivityHeatmap";
import { AgentLeaderboard } from "@/components/AgentLeaderboard";
import { Concentration } from "@/components/Concentration";
import { CumulativeChart } from "@/components/CumulativeChart";
import { DailyChart } from "@/components/DailyChart";
import { Hero, type HeroStats } from "@/components/Hero";
import { NewVsReturning } from "@/components/NewVsReturning";
import { RecentActivity } from "@/components/RecentActivity";
import type { AgentRow } from "@/lib/identifyAgents";
import {
  fetchActivityHeatmap,
  fetchConcentration,
  fetchCumulative,
  fetchDaily,
  fetchLifetimeTotals,
  fetchNewVsReturningByWeek,
  fetchRecentPayments,
  fetchTrends,
} from "@/lib/subgraph";
// Static directory of identified agents, baked at build time by
// scripts/build-agent-directory.ts. Bypasses the per-request 8004scan +
// agent0 enrichment that was costing ~10s on every Vercel cold lambda
// (`unstable_cache` is per-lambda, so cold starts re-pay the full cost).
// The directory refreshes whenever Vercel rebuilds, which currently
// happens on every commit to main plus the daily registry crawl.
import knownAgentsDirectory from "../data/known-agents.json";

// Dynamic rendering: the page is rendered on demand and the underlying
// gateway fetches are cached via `next.revalidate` (300s) and React's
// per-request `cache()`. Avoiding static prerender at build time means
// builds don't require GRAPH_API_KEY to be set in the build environment
// (only runtime). Previous architecture relied on a daily Dune cron
// (revalidate=86400); migrating to the x402-omnigraph subgraph lets the
// dashboard feel real-time without burning gateway query budget.
export const dynamic = "force-dynamic";

// Note on caching: `dynamic = "force-dynamic"` makes Next render the route
// at every request, so a page-level `revalidate` export here would conflict
// (Next 15 rejects the route segment config on build with "can't recognize
// the exported `config` field"). Per-fetch caching still happens via the
// `next.revalidate` option passed inside lib/subgraph.ts (REVALIDATE_SECONDS),
// which feeds Next's Data Cache for the GraphQL responses — that's where the
// 5-min staleness window actually lives. Don't add `export const revalidate`
// here without also changing dynamic to "auto".

// Hard wall-clock budget for the page render. Vercel functions default to
// 10s on Hobby and 60s on Pro; 60s is plenty for the workhorse subgraph
// fetch (single-digit pages) + cached identifyAgents directory build.
export const maxDuration = 60;

function extractAgentName(agent: string): string {
  const m = /^\[([^\]]+)\]/.exec(agent);
  return m ? m[1] : agent;
}
function extractAgentLink(agent: string, fallback: string): string {
  const m = /\(([^)]+)\)$/.exec(agent);
  return m ? m[1] : fallback;
}

export default async function Page() {
  // All gateway-scoped panels derive from a single paginated payment fetch
  // memoized inside subgraph.ts via React's cache(); the parallel Promise.all
  // here is mostly about keeping the call graph readable.
  const [
    lifetime,
    daily,
    cumulative,
    nrPoints,
    paymentRows,
    heatPoints,
    concRows,
    trends,
  ] = await Promise.all([
    fetchLifetimeTotals(),
    fetchDaily(),
    fetchCumulative(),
    fetchNewVsReturningByWeek(),
    fetchRecentPayments(50),
    fetchActivityHeatmap(),
    fetchConcentration(),
    fetchTrends(),
  ]);

  // Agent identity is pre-baked at build time (see import above + the
  // scripts/build-agent-directory.ts generator). No per-request enrichment,
  // no 8004scan rate-limit waits on cold lambdas. If the JSON is the bootstrap
  // placeholder (count=0), the AgentLeaderboard panel just renders the
  // "no matches yet" empty state, which is the same graceful degradation
  // the previous 6h-unstable_cache path had.
  const agentRows = knownAgentsDirectory.agents as AgentRow[];

  const identityByWallet = new Map<string, { name: string; link: string }>();
  for (const a of agentRows) {
    const name = extractAgentName(a.agent);
    const link = extractAgentLink(a.agent, a.agent_link);
    identityByWallet.set(a.wallet, { name, link });
  }

  const agentsRepeat = agentRows.filter((a) => a.payments > 1).length;

  // Hero numbers
  const totalUSDC = lifetime.total_usdc;
  const totalPayments = lifetime.total_payments;

  // WoW delta = 7d vs (30d-7d)/3 (prior-3-week average) for stability on
  // early data. Identical formula to the previous Dune-backed version.
  const paymentsToday = trends.payments_24h;
  const payments7d = trends.payments_7d;
  const usdc7d = trends.usdc_7d;
  const payments30d = trends.payments_30d;
  const usdc30d = trends.usdc_30d;
  const priorWeeklyAvg_payments = Math.max(0, (payments30d - payments7d) / 3);
  const priorWeeklyAvg_usdc = Math.max(0, (usdc30d - usdc7d) / 3);
  const weekDeltaPayments = priorWeeklyAvg_payments > 0
    ? ((payments7d - priorWeeklyAvg_payments) / priorWeeklyAvg_payments) * 100
    : 0;
  const weekDeltaUSDC = priorWeeklyAvg_usdc > 0
    ? ((usdc7d - priorWeeklyAvg_usdc) / priorWeeklyAvg_usdc) * 100
    : 0;

  const lastPaymentAt = paymentRows[0]?.block_time ?? lifetime.last_payment_at ?? "";

  // "Agents this week" — distinct NEW agents whose first-ever payment to the
  // gateway is in the last 7 days. Uses first_seen (set by fetchTopPayers
  // and propagated through identifyAgents) so a long-time repeat payer
  // doesn't get re-counted every week.
  const weekAgo = Date.now() - 7 * 86_400_000;
  const agentsThisWeek = agentRows.filter((a) => {
    const t = Date.parse(a.first_seen);
    return Number.isFinite(t) && t >= weekAgo;
  }).length;

  const heroStats: HeroStats = {
    totalUSDC,
    totalPayments,
    agentsKnown: agentRows.length,
    agentsRepeat,
    // 0% delta is meaningful (= "exactly on prior-week pace"); coerce to
    // undefined so the StatCard hides the chip rather than rendering "+0%"
    // for a quiet week. Matches the Dune-era visual behaviour.
    weekDeltaUSDC: weekDeltaUSDC || undefined,
    weekDeltaPayments: weekDeltaPayments || undefined,
    agentsThisWeek,
    repeatsThisWeek: undefined,
    lastPaymentAt,
    // Preserve 0 — "0 payments today" is different from "no data". Hero
    // hides the chip when undefined and renders "0 today" when zero.
    paymentsToday: paymentsToday ?? undefined,
  };

  return (
    <>
      <Hero stats={heroStats} />

      <a
        href="https://payql-playground-production.up.railway.app"
        target="_blank"
        rel="noopener noreferrer"
        className="mb-6 flex items-center justify-between gap-3 rounded-xl border border-accent/20 bg-accent/5 px-4 py-3 text-sm text-muted transition hover:border-accent/40 hover:bg-accent/10"
      >
        <span>
          <span className="font-medium text-accent">▶ Try it yourself</span> — ask a question, pay $0.01, and query The Graph live in the PayQL playground
        </span>
        <span className="text-accent">↗</span>
      </a>

      <div className="mb-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <CumulativeChart data={cumulative} />
        <DailyChart data={daily} />
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <AgentLeaderboard rows={agentRows} />
        </div>
        <RecentActivity rows={paymentRows} identityByWallet={identityByWallet} />
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <NewVsReturning data={nrPoints} />
        <Concentration rows={concRows} />
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4">
        <ActivityHeatmap data={heatPoints} />
      </div>

      <footer className="mt-10 flex items-center justify-between text-xs text-dim">
        <span>
          Onchain data via the{" "}
          <a
            className="text-muted hover:text-accent"
            href="https://thegraph.com/explorer/subgraphs/Cb56epg3EvQ6JRpPfknbkM54QxpzTvLa7mwKNQQfUyoj"
            target="_blank"
            rel="noopener noreferrer"
          >
            x402-omnigraph subgraph
          </a>
          {" · "}
          gateway contract on{" "}
          <a
            className="text-muted hover:text-accent"
            href="https://basescan.org/address/0x79DC34E41B2b591078d3dE222C43EcaaBD52FcCB"
            target="_blank"
            rel="noopener noreferrer"
          >
            BaseScan
          </a>
          {" · "}
          agent identity via{" "}
          <a className="text-muted hover:text-accent" href="https://8004scan.io" target="_blank" rel="noopener noreferrer">
            8004scan
          </a>{" "}
          +{" "}
          <a className="text-muted hover:text-accent" href="https://thegraph.com" target="_blank" rel="noopener noreferrer">
            The Graph
          </a>{" "}
          agent0 subgraph
        </span>
        <span>live · 5-min revalidate</span>
      </footer>
    </>
  );
}
