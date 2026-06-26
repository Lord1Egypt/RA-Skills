"use client";

import { useGameState } from "@/lib/hooks/use-game-state";
import { AnimatedNumber } from "./animated-number";

export function JackpotDisplay() {
  const { data, isLoading } = useGameState();

  const jackpot = data?.jackpot ?? 0;

  return (
    <div className="relative flex flex-col items-center">
      {/* Glow effect */}
      <div className="absolute -inset-20 bg-foreground/5 blur-[100px] rounded-full" />

      <h1 className="relative text-[clamp(3rem,18vw,12rem)] font-bold leading-none tracking-tighter text-foreground">
        <span className="text-muted-foreground text-[0.6em] mr-2">$</span>
        <AnimatedNumber value={jackpot} className="tabular-nums" />
      </h1>

      <span className="relative mt-2 text-xs font-mono text-muted-foreground/70 uppercase tracking-widest">
        {isLoading ? "Loading..." : "Enter Anytime"}
      </span>
    </div>
  );
}
