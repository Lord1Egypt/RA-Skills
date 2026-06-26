import { findHighPotentialPairs, confirmOnDexScreener } from "./screener.ts"
import type { TradeDecision } from "./types.ts"

export const threeXStrategy = async (
  currentPortfolioSol: number,
  maxRiskPercent = 5
): Promise<TradeDecision> => {
  const topTokens = await findHighPotentialPairs(65)

  if (topTokens.length === 0) {
    return {
      action: "skip",
      token: null,
      reason:
        "No qualifying pump.fun graduations in buffer. " +
        "Start the agent loop to collect live signals: solana-wallet agent <wallet> --dry-run",
      suggestedAmountSol: 0,
      targetMultiple: 3.0,
      stopLossPercent: 30,
    }
  }

  // Optional DexScreener confirmation on the top candidate
  const best = topTokens[0]
  const dex = await confirmOnDexScreener(best.mint)

  // If DexScreener shows the token but liquidity is dangerously low, skip
  if (dex !== null && dex.liquidityUsd < 10_000) {
    return {
      action: "skip",
      token: best,
      reason: `Low Raydium liquidity ($${dex.liquidityUsd.toFixed(0)}) — rug risk too high`,
      suggestedAmountSol: 0,
      targetMultiple: 3.0,
      stopLossPercent: 30,
    }
  }

  // Risk sizing: % of portfolio, min 0.01 SOL, max 0.5 SOL
  const amountSol = Math.max(
    0.01,
    Math.min(currentPortfolioSol * (maxRiskPercent / 100), 0.5)
  )

  if (currentPortfolioSol < amountSol + 0.005) {
    return {
      action: "skip",
      token: best,
      reason: `Insufficient SOL (${currentPortfolioSol.toFixed(4)}) — need ${(amountSol + 0.005).toFixed(4)} SOL including fees`,
      suggestedAmountSol: 0,
      targetMultiple: 3.0,
      stopLossPercent: 30,
    }
  }

  const dexNote = dex
    ? ` | Raydium liq: $${dex.liquidityUsd.toFixed(0)}`
    : " | Raydium liq: pending"

  return {
    action: "buy",
    token: best,
    reason: `Score ${best.score}/100 — ${best.symbol} · ${best.reason}${dexNote}`,
    suggestedAmountSol: amountSol,
    targetMultiple: 3.0,
    stopLossPercent: 30,
  }
}
