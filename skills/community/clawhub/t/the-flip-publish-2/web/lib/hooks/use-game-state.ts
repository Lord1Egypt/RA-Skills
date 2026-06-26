"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchGameFromChain, formatJackpot } from "@/lib/solana";
import type { GameState } from "@/lib/types";
import { EMPTY_GAME_STATE } from "@/lib/types";

const REFETCH_INTERVAL = 10_000; // 10 seconds

async function fetchGameState(): Promise<GameState> {
  try {
    const onChain = await fetchGameFromChain();

    if (!onChain) {
      return { ...EMPTY_GAME_STATE, phase: "not_initialized" };
    }

    return {
      phase: "active",
      jackpot: formatJackpot(onChain.jackpotPool),
      currentRound: onChain.currentRound,
      totalEntries: onChain.totalEntries,
      totalWins: onChain.totalWins,
      operatorPool: formatJackpot(onChain.operatorPool),
    };
  } catch (error) {
    console.error("Failed to fetch game state:", error);
    return { ...EMPTY_GAME_STATE, phase: "offline" };
  }
}

export function useGameState() {
  return useQuery({
    queryKey: ["gameState"],
    queryFn: fetchGameState,
    refetchInterval: REFETCH_INTERVAL,
    staleTime: REFETCH_INTERVAL - 2000,
    refetchOnWindowFocus: true,
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 10000),
  });
}
