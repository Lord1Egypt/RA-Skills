import { NextResponse } from "next/server";
import {
  fetchGameFromChain,
  formatJackpot,
  getRoundResults,
  flipToStr,
} from "@/lib/solana";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const game = await fetchGameFromChain();

    if (!game) {
      return NextResponse.json(
        {
          phase: "not_initialized",
          jackpot: 0,
          currentRound: 0,
          totalEntries: 0,
          totalWins: 0,
        },
        { status: 200 }
      );
    }

    // Get last round's results if available
    let lastRoundResults: string[] = [];
    if (game.currentRound > 0) {
      const results = getRoundResults(game, game.currentRound - 1);
      lastRoundResults = results.map(flipToStr);
    }

    // Cooldown calculation
    const now = Math.floor(Date.now() / 1000);
    const cooldownSeconds = 43_200; // 12 hours
    const elapsed = now - game.lastFlipAt;
    const flipReady = game.lastFlipAt === 0 || elapsed >= cooldownSeconds;
    const nextFlipAt = flipReady ? now : game.lastFlipAt + cooldownSeconds;

    return NextResponse.json({
      phase: "active",
      jackpot: formatJackpot(game.jackpotPool),
      operatorPool: formatJackpot(game.operatorPool),
      currentRound: game.currentRound,
      totalEntries: game.totalEntries,
      totalWins: game.totalWins,
      lastRoundResults,
      lastFlipAt: game.lastFlipAt,
      nextFlipAt,
      flipReady,
      authority: game.authority.toBase58(),
      vault: game.vault.toBase58(),
      usdcMint: game.usdcMint.toBase58(),
    });
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json(
      { error: "Failed to fetch game state", details: message },
      { status: 500 }
    );
  }
}
