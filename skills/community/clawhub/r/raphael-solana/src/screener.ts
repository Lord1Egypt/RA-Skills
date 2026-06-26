import WebSocket from "ws"
import { PUMPPORTAL_WS, DEXSCREENER_API } from "./environment.ts"
import type { PumpEvent, RawPumpEvent, ScoredToken, DexScreenerConfirmation } from "./types.ts"

// ── In-memory state ───────────────────────────────────────────────────────────

const MAX_BUFFER = 2_000
const eventBuffer: PumpEvent[] = []

// Per-token trade stats accumulated from live trade events
const tokenStats: Map<string, { buys: number; sells: number; solVolume: number; marketCapSol: number }> = new Map()

// Graduated tokens (mint → scored token)
const graduatedTokens: Map<string, ScoredToken> = new Map()

let _connected = false
let _ws: WebSocket | null = null

const pushEvent = (event: PumpEvent): void => {
  eventBuffer.push(event)
  if (eventBuffer.length > MAX_BUFFER) eventBuffer.shift()

  if (event.txType === "buy" || event.txType === "sell") {
    const stats = tokenStats.get(event.mint) ?? { buys: 0, sells: 0, solVolume: 0, marketCapSol: 0 }
    if (event.txType === "buy") stats.buys++
    else stats.sells++
    stats.solVolume += event.solAmount
    if ("marketCapSol" in event) stats.marketCapSol = Number((event as RawPumpEvent).marketCapSol ?? 0)
    tokenStats.set(event.mint, stats)
  }

  // Track initial bonding curve data from create events
  if (event.txType === "create") {
    const raw = event as unknown as RawPumpEvent
    const stats = tokenStats.get(event.mint) ?? { buys: 0, sells: 0, solVolume: Number(raw.solAmount ?? 0), marketCapSol: Number(raw.marketCapSol ?? 0) }
    // initialBuy counts as a buy
    if (Number(raw.initialBuy ?? 0) > 0) stats.buys++
    tokenStats.set(event.mint, stats)
  }
}

// ── Event normalization (field names confirmed from live pumpportal.fun data) ─

const normalizeEvent = (raw: RawPumpEvent): PumpEvent | null => {
  const { txType, mint } = raw
  if (!mint || typeof mint !== "string") return null
  const now = Date.now()

  if (txType === "create") {
    return {
      txType: "create",
      mint,
      name: String(raw.name ?? ""),
      symbol: String(raw.symbol ?? ""),
      traderPublicKey: String(raw.traderPublicKey ?? ""),
      initialBuy: Number(raw.initialBuy ?? 0),
      bondingCurveKey: raw.bondingCurveKey as string | undefined,
      receivedAt: now,
    }
  }

  if (txType === "buy" || txType === "sell") {
    return {
      txType,
      mint,
      solAmount: Number(raw.solAmount ?? 0),
      tokenAmount: Number(raw.tokenAmount ?? 0),
      traderPublicKey: String(raw.traderPublicKey ?? ""),
      newTokenBalance: raw.newTokenBalance as number | undefined,
      bondingCurveKey: raw.bondingCurveKey as string | undefined,
      receivedAt: now,
    }
  }

  // Graduation: txType "migrate" when bonding curve completes → moves to Raydium
  if (txType === "migrate" || (raw.raydiumPool && typeof raw.raydiumPool === "string")) {
    return {
      txType: "migrate",
      mint,
      name: String(raw.name ?? ""),
      symbol: String(raw.symbol ?? ""),
      raydiumPool: raw.raydiumPool as string | undefined,
      bondingCurveKey: raw.bondingCurveKey as string | undefined,
      receivedAt: now,
    }
  }

  return null
}

const isGraduation = (event: PumpEvent): boolean =>
  event.txType === "migrate" || event.txType === "graduation"

// ── WebSocket listener ────────────────────────────────────────────────────────

export const startPumpListener = (
  onGraduation?: (token: ScoredToken) => void,
  verbose = false
): WebSocket => {
  const ws = new WebSocket(PUMPPORTAL_WS)
  _ws = ws

  ws.on("open", () => {
    _connected = true
    console.log("[pump.fun] Connected to pumpportal.fun WebSocket")

    // Subscribe to new token creations
    ws.send(JSON.stringify({ method: "subscribeNewToken" }))
  })

  ws.on("message", (raw) => {
    try {
      const data = JSON.parse(raw.toString()) as RawPumpEvent
      if (verbose) console.log("[pump.fun] raw:", JSON.stringify(data))

      // When a new token is created, subscribe to its trades immediately
      // This is the correct pattern — pump.fun doesn't support wildcard trade subs
      if (data.txType === "create" && data.mint && _ws?.readyState === WebSocket.OPEN) {
        _ws.send(JSON.stringify({
          method: "subscribeTokenTrade",
          keys: [data.mint],
        }))
      }

      const event = normalizeEvent(data)
      if (!event) return

      pushEvent(event)

      if (isGraduation(event)) {
        const scored = scoreGraduatedToken(data)
        graduatedTokens.set(event.mint, scored)
        console.log(`[pump.fun] 🎓 GRADUATED: ${scored.symbol} — score ${scored.score}/100`)
        onGraduation?.(scored)
      }
    } catch {
      // ignore malformed messages
    }
  })

  ws.on("error", (err) => console.error("[pump.fun] WS error:", err.message))

  ws.on("close", () => {
    _connected = false
    _ws = null
    console.log("[pump.fun] Connection closed — reconnecting in 3s...")
    setTimeout(() => startPumpListener(onGraduation, verbose), 3_000)
  })

  return ws
}

export const isPumpListenerConnected = (): boolean => _connected

// ── Scoring ──────────────────────────────────────────────────────────────────

export const scoreGraduatedToken = (raw: RawPumpEvent): ScoredToken => {
  const mint = String(raw.mint ?? "")
  const stats = tokenStats.get(mint) ?? { buys: 0, sells: 0, solVolume: 0, marketCapSol: 0 }
  const totalTrades = stats.buys + stats.sells
  const buyPressure = totalTrades > 0 ? stats.buys / totalTrades : 0.5

  let score = 50 // base: graduation itself is a proven-demand signal

  // Buy pressure (−15 to +25)
  score += buyPressure > 0.7 ? 25 : buyPressure > 0.55 ? 12 : buyPressure < 0.4 ? -15 : 0

  // SOL volume on bonding curve (0 to +15)
  score += stats.solVolume > 100 ? 15 : stats.solVolume > 50 ? 8 : stats.solVolume > 20 ? 3 : 0

  // Trade count = community interest (0 to +10)
  score += totalTrades > 300 ? 10 : totalTrades > 100 ? 5 : totalTrades > 30 ? 2 : 0

  score = Math.max(0, Math.min(100, score))

  const reason = [
    `Graduated → Raydium`,
    `${stats.buys}/${totalTrades} buys (${Math.round(buyPressure * 100)}% buy pressure)`,
    `${stats.solVolume.toFixed(1)} SOL bonding curve volume`,
  ].join(" · ")

  return {
    mint,
    symbol: String(raw.symbol ?? "UNKNOWN"),
    name: String(raw.name ?? "UNKNOWN"),
    score,
    reason,
    raydiumPool: raw.raydiumPool as string | undefined,
    graduatedAt: Date.now(),
    source: "graduation",
  }
}

// ── DexScreener confirmation ──────────────────────────────────────────────────

export const confirmOnDexScreener = async (mint: string): Promise<DexScreenerConfirmation> => {
  try {
    const res = await fetch(`${DEXSCREENER_API}/tokens/${mint}`)
    if (!res.ok) return null

    const data = await res.json() as {
      pairs?: Array<{
        liquidity?: { usd?: number }
        volume?: { h1?: number }
        priceChange?: { h1?: number }
      }>
    }

    const pair = data.pairs?.[0]
    if (!pair) return null

    return {
      liquidityUsd: pair.liquidity?.usd ?? 0,
      volume1h: pair.volume?.h1 ?? 0,
      priceChange1h: pair.priceChange?.h1 ?? 0,
    }
  } catch {
    return null
  }
}

// ── One-shot snapshot for CLI `find-pairs` ────────────────────────────────────

export const findHighPotentialPairs = async (minScore = 60): Promise<ScoredToken[]> => {
  // Return from graduated tokens map (populated by live WebSocket events)
  const cutoff = Date.now() - 30 * 60 * 1_000
  const recent = Array.from(graduatedTokens.values())
    .filter(t => (t.graduatedAt ?? 0) > cutoff)
    .filter(t => t.score >= minScore)
    .sort((a, b) => b.score - a.score)
    .slice(0, 10)

  return recent
}

export const getBufferStats = () => ({
  totalEvents: eventBuffer.length,
  trackedTokens: tokenStats.size,
  graduatedTokens: graduatedTokens.size,
  connected: _connected,
})
