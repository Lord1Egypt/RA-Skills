"use client";

import { useGameState } from "@/lib/hooks/use-game-state";

export function LiveIndicator() {
  const { isLoading, isError, data } = useGameState();

  const isLive = !isLoading && !isError && data?.phase === "active";

  return (
    <div className="fixed top-6 right-6 flex items-center gap-2 z-50">
      <div className="relative">
        <div
          className={`w-2 h-2 rounded-full ${
            isLive ? "bg-emerald-500" : isLoading ? "bg-amber-500" : "bg-red-500"
          }`}
        />
        {isLive && (
          <div className="absolute inset-0 w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
        )}
      </div>
      <span className="text-xs font-mono text-muted-foreground uppercase tracking-wider">
        {isLoading ? "Loading" : isLive ? "Live" : "Offline"}
      </span>
    </div>
  );
}
