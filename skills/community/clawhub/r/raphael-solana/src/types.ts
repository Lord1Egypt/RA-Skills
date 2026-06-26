export type Network = "devnet" | "mainnet-beta"

// ── Wallet Store ────────────────────────────────────────────────────────────

export type EncryptedWalletRecord = {
  name: string
  publicKey: string
  encryptedPrivateKey: string
  salt: string
  createdAt: string
  network: Network
  tags: string[]
}

export type WalletStore = {
  version: number
  wallets: Record<string, EncryptedWalletRecord>
}

export type WalletInfo = {
  name: string
  publicKey: string
  network: Network
  createdAt: string
  tags: string[]
}

// ── Balances ─────────────────────────────────────────────────────────────────

export type TokenBalance = {
  mint: string
  symbol: string
  decimals: number
  amount: bigint
  uiAmount: number
}

export type BalanceResult = {
  walletName: string
  publicKey: string
  solBalance: number
  lamports: number
  tokens: TokenBalance[]
}

// ── Transfers + Swaps ────────────────────────────────────────────────────────

export type TransferResult = {
  signature: string
  explorerUrl: string
  from: string
  to: string
  amount: number
  mint?: string
}

export type SwapResult = {
  signature: string
  explorerUrl: string
  inputMint: string
  outputMint: string
  inputAmountSol: number
  outputAmount: number
}

// ── pump.fun events ──────────────────────────────────────────────────────────

// Raw events from pumpportal.fun WebSocket (field names match their live API)
export type RawPumpEvent = Record<string, unknown> & {
  txType?: string
  mint?: string
}

export type PumpCreateEvent = {
  txType: "create"
  mint: string
  name: string
  symbol: string
  traderPublicKey: string
  initialBuy?: number
  bondingCurveKey?: string
}

export type PumpTradeEvent = {
  txType: "buy" | "sell"
  mint: string
  solAmount: number
  tokenAmount: number
  traderPublicKey: string
  newTokenBalance?: number
  bondingCurveKey?: string
}

// Graduation = token completed bonding curve, migrated to Raydium
// pump.fun may send this as txType "migrate" or a top-level "type" field
export type PumpGraduationEvent = {
  txType: "migrate" | "graduation"
  mint: string
  name: string
  symbol: string
  raydiumPool?: string
  bondingCurveKey?: string
}

export type PumpEvent = (PumpCreateEvent | PumpTradeEvent | PumpGraduationEvent) & {
  receivedAt: number   // added by us on receipt
}

// ── Screener ─────────────────────────────────────────────────────────────────

export type ScoredToken = {
  mint: string
  symbol: string
  name: string
  score: number
  reason: string
  raydiumPool?: string
  graduatedAt?: number
  source: "graduation" | "momentum"
}

export type DexScreenerConfirmation = {
  liquidityUsd: number
  volume1h: number
  priceChange1h: number
} | null

// ── Strategy ─────────────────────────────────────────────────────────────────

export type TradeDecision = {
  action: "buy" | "hold" | "skip"
  token: ScoredToken | null
  reason: string
  suggestedAmountSol: number
  targetMultiple: number
  stopLossPercent: number
}

// ── Agent ────────────────────────────────────────────────────────────────────

export type Position = {
  walletName: string
  mint: string
  symbol: string
  entryAmountSol: number
  tokensHeld: number
  openedAt: string
  targetMultiple: number
  stopLossPercent: number
  score: number
}

export type Trade = {
  walletName: string
  mint: string
  symbol: string
  action: "buy" | "sell"
  amountSol: number
  signature: string
  timestamp: string
  score: number
}

export type AgentConfig = {
  walletName: string
  intervalSeconds: number
  strategy: "3x" | "manual"
  maxRiskPercent: number
  dryRun: boolean
}

export type AgentState = {
  openPositions: Position[]
  tradeHistory: Trade[]
  lastRunAt: string | null
}

// ── Polymarket Weather Arb ────────────────────────────────────────────────────

export type PolymarketWeatherConfig = {
  walletName: string          // EVM wallet name (secp256k1, Polygon)
  cities: string[]            // e.g. ["nyc", "london", "seoul"]
  tradeAmountUsdc: number     // per trade (min $5, default $5)
  maxPositionUsdc: number     // hard cap per bracket (default $10)
  minEdge: number             // fairValue − askPrice threshold (default 0.20)
  minFairValue: number        // minimum fair probability to trade (default 0.40)
  intervalSeconds: number
  dryRun: boolean
}

export type PolymarketWeatherReading = {
  city: string
  forecastHighF: number
  sigmaF: number              // forecast uncertainty used (°F)
  targetBracket: string | null   // e.g. "40-41°F"
  bestEdge: number | null
  orderId: string | null
  skippedReason: string | null   // "no_market" | "market_closing_soon" | "no_edge" | "already_positioned" | "insufficient_usdc" | "error"
  scannedAt: number
}

// ── X / Twitter ──────────────────────────────────────────────────────────────

export type XConfig = {
  apiKey: string
  apiSecret: string
  accessToken: string
  accessTokenSecret: string
  bearerToken: string
}

export type Tweet = {
  id: string
  text: string
  authorId?: string
  createdAt: string
  conversationId?: string
}

export type XUser = {
  id: string
  name: string
  username: string
}

export type XStrategyConfig = {
  /** X handle of this bot account (without @) */
  handle: string
  /** Keywords to search and monitor (Basic+ tier only) */
  monitorKeywords: string[]
  /** Auto-reply to mentions with a canned response (dry_run ignores this) */
  autoReplyToMentions: boolean
  /** Automatically post a tweet when any strategy fires a trade */
  postTradeUpdates: boolean
  /** Hard cap on tweets sent per hour (default 2) */
  maxTweetsPerHour: number
  /** If true, no tweets are actually sent */
  dryRun: boolean
  /** Poll interval for mentions + keyword feed (seconds, default 60) */
  intervalSeconds: number
}

// ── Strategy Manager ─────────────────────────────────────────────────────────
export type StrategyStatus = {
  pumpfun: {
    running: boolean
    lastGraduations: number
    lastCheckAt: string | null
  }
  weather_arb: {
    running: boolean
    lastCheckAt: string | null
    cities: string[]
    lastReadings: PolymarketWeatherReading[]
  }
  x_strategy: {
    running: boolean
    lastCheckAt: string | null
    tweetsThisHour: number
    lastTweetId: string | null
  }
  _source?: "live" | "file" | "default" | "dead_daemon_cleanup"
  _stale?: boolean
}
