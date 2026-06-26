"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchGameFromChain, getRoundResults, flipToStr } from "@/lib/solana";
import { PREDICTIONS_SIZE, SURVIVAL_FLIPS } from "@/lib/types";
import { cn } from "@/lib/utils";

export function FlipProgress() {
  const { data: game } = useQuery({
    queryKey: ["gameRaw"],
    queryFn: fetchGameFromChain,
    refetchInterval: 10_000,
    staleTime: 8_000,
  });

  if (!game || game.currentRound === 0) {
    return null;
  }

  // Show the most recent round's results
  const lastRound = game.currentRound - 1;
  const results = getRoundResults(game, lastRound);

  if (results.length === 0) {
    return null;
  }

  return (
    <div className="mt-8 w-full max-w-xl mx-auto px-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">
          Round #{lastRound} Results
        </span>
        <span className="text-[10px] font-mono text-muted-foreground tabular-nums">
          {game.currentRound.toLocaleString()} rounds completed
        </span>
      </div>

      <div className="flex gap-0.5">
        {results.map((r, i) => {
          const label = flipToStr(r);
          return (
            <div key={i} className="flex-1 flex flex-col items-center">
              <div
                className={cn(
                  "w-full h-7 rounded-sm flex items-center justify-center text-[10px] font-bold transition-all duration-300",
                  i < SURVIVAL_FLIPS
                    ? r === 1
                      ? "bg-foreground text-background"
                      : "bg-muted-foreground/70 text-background"
                    : r === 1
                      ? "bg-foreground/40 text-background/60"
                      : "bg-muted-foreground/30 text-background/60"
                )}
              >
                {label}
              </div>
              <span className="text-[8px] font-mono text-muted-foreground/50 mt-0.5 tabular-nums">
                {i + 1}
              </span>
            </div>
          );
        })}
      </div>

      <p className="text-[10px] text-muted-foreground/60 text-center mt-2">
        All {PREDICTIONS_SIZE} coins flipped at once. First {SURVIVAL_FLIPS} must match your predictions to win.
      </p>
    </div>
  );
}
