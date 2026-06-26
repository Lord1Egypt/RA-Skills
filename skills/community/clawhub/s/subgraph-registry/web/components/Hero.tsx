import { LiveDot } from "./LiveDot";
import { StatCard } from "./StatCard";
import { fmtInt, fmtUSD, fmtPct, timeAgo } from "@/lib/format";

export interface HeroStats {
  totalUSDC: number;
  totalPayments: number;
  agentsKnown: number;
  agentsRepeat: number;
  weekDeltaUSDC?: number;        // percent
  weekDeltaPayments?: number;    // percent
  agentsThisWeek?: number;       // count of new agents this week
  repeatsThisWeek?: number;      // count of agents who paid again this week
  lastPaymentAt?: string;        // ISO
  paymentsToday?: number;
}

export function Hero({ stats }: { stats: HeroStats }) {
  return (
    <section className="mb-8">
      <header className="mb-6 flex flex-col items-start justify-between gap-2 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            <span className="text-accent">x402</span> Watch
          </h1>
          <p className="mt-1 text-sm text-muted">
            Live agent payments to The Graph on Base, with ERC-8004 identity attribution.
          </p>
        </div>
        <div className="flex items-center gap-3 text-xs text-dim">
          <LiveDot label="live" />
          <span>last paid {timeAgo(stats.lastPaymentAt)}</span>
          {stats.paymentsToday != null && (
            <>
              <span aria-hidden>·</span>
              <span>{fmtInt(stats.paymentsToday)} today</span>
            </>
          )}
          <span aria-hidden>·</span>
          <a
            href="/ask"
            className="rounded-full border border-accent/40 px-2 py-0.5 text-[11px] font-medium text-accent transition hover:bg-accent/15"
          >
            Ask x402 →
          </a>
        </div>
      </header>

      <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
        <StatCard
          value={fmtUSD(stats.totalUSDC)}
          label="total USDC"
          delta={
            stats.weekDeltaUSDC != null
              ? { value: fmtPct(stats.weekDeltaUSDC, true), positive: stats.weekDeltaUSDC >= 0 }
              : null
          }
          hint="all-time"
        />
        <StatCard
          value={fmtInt(stats.totalPayments)}
          label="payments"
          delta={
            stats.weekDeltaPayments != null
              ? { value: fmtPct(stats.weekDeltaPayments, true), positive: stats.weekDeltaPayments >= 0 }
              : null
          }
          hint="all-time"
        />
        <StatCard
          value={fmtInt(stats.agentsKnown)}
          label="agents"
          delta={
            stats.agentsThisWeek != null && stats.agentsThisWeek > 0
              ? { value: `+${stats.agentsThisWeek} this wk`, positive: true }
              : null
          }
          hint="identified"
        />
        <StatCard
          value={fmtInt(stats.agentsRepeat)}
          label="repeats"
          delta={
            stats.repeatsThisWeek != null && stats.repeatsThisWeek > 0
              ? { value: `+${stats.repeatsThisWeek} this wk`, positive: true }
              : null
          }
          hint=">1 payment"
        />
      </div>
    </section>
  );
}
