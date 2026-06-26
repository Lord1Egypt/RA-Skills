"use client";

import { useGameState } from "@/lib/hooks/use-game-state";

interface StatItemProps {
  value: string;
  label: string;
}

function StatItem({ value, label }: StatItemProps) {
  return (
    <div className="text-center">
      <div className="text-xl md:text-2xl font-bold text-foreground tabular-nums">
        {value}
      </div>
      <div className="text-[10px] text-muted-foreground uppercase tracking-wider mt-1">
        {label}
      </div>
    </div>
  );
}

function Divider() {
  return <div className="w-px h-6 bg-border" />;
}

export function StatsDisplay() {
  const { data, isLoading, isError } = useGameState();

  const entries = data?.totalEntries ?? 0;
  const currentRound = data?.currentRound ?? 0;
  const totalWins = data?.totalWins ?? 0;

  // Simple status: either we have data or we're loading
  const isLive = !isLoading && !isError && data?.phase === "active";

  return (
    <div className="mt-10 flex flex-col items-center gap-4">
      <div className="flex items-center gap-5 md:gap-8">
        <StatItem value="$1" label="Entry" />
        <Divider />
        <StatItem value={currentRound.toLocaleString()} label="Rounds" />
        <Divider />
        <StatItem value={entries.toLocaleString()} label="Entries" />
        {totalWins > 0 && (
          <>
            <Divider />
            <StatItem value={totalWins.toLocaleString()} label="Winners" />
          </>
        )}
      </div>
      <div className="flex items-center gap-2">
        <div
          className={`w-1.5 h-1.5 rounded-full ${
            isLive ? "bg-emerald-500" : "bg-amber-500"
          }`}
        />
        <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
          {isLoading ? "Loading..." : isLive ? "Live on Devnet" : "Offline"}
        </span>
      </div>
    </div>
  );
}
