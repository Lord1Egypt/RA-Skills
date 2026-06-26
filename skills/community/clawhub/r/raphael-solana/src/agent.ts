import { startPumpListener, getBufferStats } from "./screener.ts"
import { getPortfolioSummary } from "./balance.ts"
import { threeXStrategy } from "./strategy.ts"
import { raydiumSwap, solToLamports, SOL_MINT } from "./swap.ts"
import type { AgentConfig, AgentState, ScoredToken, Trade } from "./types.ts"

const sleep = (ms: number) => new Promise<void>(r => setTimeout(r, ms))
const log = (msg: string) => console.log(`[${new Date().toISOString()}] ${msg}`)

// ── Tick — one iteration of the pumpfun strategy ──────────────────────────────

export const runPumpfunTick = async (
  config: AgentConfig,
  state: AgentState,
): Promise<AgentState> => {
  const nextState: AgentState = {
    ...state,
    lastRunAt: new Date().toISOString(),
  }

  try {
    // 1. Check portfolio
    const portfolio = await getPortfolioSummary(config.walletName)
    log(`Portfolio: ${portfolio.solBalance.toFixed(6)} SOL + ${portfolio.tokens.length} token(s)`)

    // 2. Run strategy
    if (config.strategy === "3x") {
      const decision = await threeXStrategy(portfolio.solBalance, config.maxRiskPercent)
      log(`Decision: ${decision.action.toUpperCase()} — ${decision.reason}`)

      if (decision.action === "buy" && decision.token) {
        if (config.dryRun) {
          log(
            `[dry-run] Would swap ${decision.suggestedAmountSol} SOL → ` +
            `${decision.token.symbol} (${decision.token.mint})`
          )
        } else {
          log(`Executing swap: ${decision.suggestedAmountSol} SOL → ${decision.token.symbol}`)
          const result = await raydiumSwap(
            config.walletName,
            SOL_MINT,
            decision.token.mint,
            solToLamports(decision.suggestedAmountSol)
          )

          const trade: Trade = {
            walletName: config.walletName,
            mint: decision.token.mint,
            symbol: decision.token.symbol,
            action: "buy",
            amountSol: decision.suggestedAmountSol,
            signature: result.signature,
            timestamp: new Date().toISOString(),
            score: decision.token.score,
          }

          nextState.tradeHistory = [...state.tradeHistory, trade]
          log(`✅ Executed! ${result.explorerUrl}`)
          log(`   ${result.inputAmountSol} SOL → ${result.outputAmount} ${decision.token.symbol}`)
        }
      }
    }

    // 3. Log buffer health every cycle
    const bufStats = getBufferStats()
    log(`Buffer: ${bufStats.totalEvents} events | ${bufStats.trackedTokens} tokens tracked`)

  } catch (err) {
    log(`Error: ${err instanceof Error ? err.message : String(err)}`)
  }

  return nextState
}

// ── Agent loop — kept for backward-compat CLI (`solana-wallet agent <wallet>`) ─

export const runAgentLoop = async (config: AgentConfig): Promise<void> => {
  let state: AgentState = {
    openPositions: [],
    tradeHistory: [],
    lastRunAt: null,
  }

  log(`Agent starting — wallet: ${config.walletName}`)
  log(`Strategy: ${config.strategy} | Interval: ${config.intervalSeconds}s | Dry run: ${config.dryRun}`)

  if (config.dryRun) {
    log("[dry-run] No real trades will be executed")
  }

  const onGraduation = (token: ScoredToken) => {
    log(`[graduation] 🎓 ${token.symbol} (${token.mint.slice(0, 8)}...) — score ${token.score}/100`)
    log(`  ${token.reason}`)
  }

  startPumpListener(onGraduation)

  log("[pump.fun] Waiting for WebSocket connection...")
  await sleep(5_000)

  const stats = getBufferStats()
  log(`[pump.fun] Connected: ${stats.connected} | Buffer: ${stats.totalEvents} events | Tokens tracked: ${stats.trackedTokens}`)

  while (true) {
    state = await runPumpfunTick(config, state)
    log(`Sleeping ${config.intervalSeconds}s until next cycle...\n`)
    await sleep(config.intervalSeconds * 1_000)
  }
}
