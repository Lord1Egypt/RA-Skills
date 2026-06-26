import { strategyManager } from "./strategyManager.ts"
import { createEvmWallet, listEvmWallets, getEvmAddress } from "./evmWallet.ts"
import { getUsdcBalance } from "./polymarketClob.ts"
import { createXClients, postTweet, replyToTweet, searchTweets, getMentions, likeTweet, retweetTweet, resolveUser } from "./xClient.ts"
import {
  X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET, X_BEARER_TOKEN,
} from "./environment.ts"
import type { XConfig, XStrategyConfig } from "./types.ts"

type OpenClawTool = {
  name: string
  description: string
  parameters: object
  execute: (
    id: string,
    params: Record<string, unknown>,
  ) => Promise<{ content: Array<{ type: "text"; text: string }> }>
}

type OpenClawAPI = {
  registerTool(tool: OpenClawTool, opts?: { optional?: boolean }): void
}

export default function register(api: OpenClawAPI): void {
  // ── create_evm_wallet ──────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "create_evm_wallet",
      description:
        "Create a new EVM (Polygon/secp256k1) wallet for Polymarket trading. Returns the wallet name and Polygon address. The user must bridge USDC to this address before live trading.",
      parameters: {
        type: "object",
        properties: {
          name: { type: "string", description: "Wallet name, e.g. \"polymarket1\"" },
        },
        required: ["name"],
      },
      execute: async (_id, params) => {
        try {
          const { name } = params as { name: string }
          const info = await createEvmWallet(name)
          return {
            content: [
              {
                type: "text" as const,
                text: [
                  `EVM wallet "${info.name}" created.`,
                  `  Polygon address: ${info.address}`,
                  `  Created at:      ${info.createdAt}`,
                  ``,
                  `Send USDC (Polygon PoS) to: ${info.address}`,
                  `Then call check_usdc_balance to verify arrival before starting the scanner.`,
                ].join("\n"),
              },
            ],
          }
        } catch (err) {
          return {
            content: [{ type: "text" as const, text: `Error creating EVM wallet: ${err instanceof Error ? err.message : String(err)}` }],
          }
        }
      },
    },
    { optional: true },
  )

  // ── list_evm_wallets ───────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "list_evm_wallets",
      description: "List all EVM (Polygon) wallets. Shows names and Polygon addresses.",
      parameters: { type: "object", properties: {} },
      execute: async () => {
        try {
          const wallets = await listEvmWallets()
          if (wallets.length === 0) {
            return { content: [{ type: "text" as const, text: "No EVM wallets found. Use create_evm_wallet to create one." }] }
          }
          const lines = wallets.map(w => `  ${w.name.padEnd(16)}: ${w.address}  (created ${w.createdAt})`)
          return { content: [{ type: "text" as const, text: `EVM wallets:\n${lines.join("\n")}` }] }
        } catch (err) {
          return {
            content: [{ type: "text" as const, text: `Error listing EVM wallets: ${err instanceof Error ? err.message : String(err)}` }],
          }
        }
      },
    },
    { optional: true },
  )

  // ── check_usdc_balance ─────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "check_usdc_balance",
      description:
        "Check the USDC.e balance on Polygon for a named EVM wallet. Use this to confirm funds have arrived before starting the live scanner.",
      parameters: {
        type: "object",
        properties: {
          wallet_name: { type: "string", description: "EVM wallet name" },
        },
        required: ["wallet_name"],
      },
      execute: async (_id, params) => {
        try {
          const { wallet_name } = params as { wallet_name: string }
          const address = await getEvmAddress(wallet_name)
          const balance = await getUsdcBalance(address)
          return {
            content: [
              {
                type: "text" as const,
                text: [
                  `USDC balance for "${wallet_name}":`,
                  `  Address: ${address}`,
                  `  Balance: $${balance.toFixed(2)} USDC`,
                  balance < 5
                    ? `  ⚠ Balance is below the $5 minimum trade amount.`
                    : `  ✅ Ready to trade.`,
                ].join("\n"),
              },
            ],
          }
        } catch (err) {
          return {
            content: [{ type: "text" as const, text: `Error checking USDC balance: ${err instanceof Error ? err.message : String(err)}` }],
          }
        }
      },
    },
    { optional: true },
  )

  // ── start_weather_arb ──────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "start_weather_arb",
      description:
        "Start the Polymarket weather arbitrage scanner. Polls Open-Meteo forecasts and buys underpriced YES brackets on Polymarket weather markets using an EVM (Polygon) wallet.",
      parameters: {
        type: "object",
        properties: {
          wallet_name: { type: "string", description: "EVM wallet name (Polygon/secp256k1)" },
          cities: {
            type: "array",
            items: { type: "string" },
            description: "City keys to scan, e.g. [\"nyc\",\"london\",\"seoul\"]",
          },
          trade_amount_usdc: {
            type: "number",
            description: "USDC to spend per trade (min $5, e.g. 5)",
          },
          max_position_usdc: {
            type: "number",
            description: "Hard cap USDC per bracket (default 10)",
          },
          min_edge: {
            type: "number",
            description: "Minimum edge (fairValue − askPrice) to trigger trade (default 0.20)",
          },
          min_fair_value: {
            type: "number",
            description: "Minimum fair probability to consider trading (default 0.40)",
          },
          interval_seconds: {
            type: "number",
            description: "Poll interval in seconds (default 120)",
          },
          dry_run: { type: "boolean", default: true },
        },
        required: ["wallet_name", "trade_amount_usdc"],
      },
      execute: async (_id, params) => {
        try {
          const p = params as {
            wallet_name: string
            cities?: string[]
            trade_amount_usdc: number
            max_position_usdc?: number
            min_edge?: number
            min_fair_value?: number
            interval_seconds?: number
            dry_run?: boolean
          }

          if (strategyManager.getStatus().weather_arb.running) {
            return {
              content: [
                {
                  type: "text" as const,
                  text: "Weather arb scanner is already running. Use stop_weather_arb first.",
                },
              ],
            }
          }

          const config = {
            walletName:       p.wallet_name,
            cities:           p.cities ?? ["nyc","london","seoul","chicago","dallas","miami","paris","toronto","seattle"],
            tradeAmountUsdc:  p.trade_amount_usdc,
            maxPositionUsdc:  p.max_position_usdc  ?? 10,
            minEdge:          p.min_edge            ?? 0.20,
            minFairValue:     p.min_fair_value      ?? 0.40,
            intervalSeconds:  p.interval_seconds    ?? 120,
            dryRun:           p.dry_run             ?? true,
          }

          strategyManager.startWeatherArb(config)

          return {
            content: [
              {
                type: "text" as const,
                text: [
                  "Polymarket weather arb scanner started.",
                  `  Wallet:       ${config.walletName}`,
                  `  Cities:       ${config.cities.join(", ")}`,
                  `  Amount:       $${config.tradeAmountUsdc} USDC`,
                  `  Max pos:      $${config.maxPositionUsdc} USDC`,
                  `  Min edge:     ${Math.round(config.minEdge * 100)}%`,
                  `  Min fair val: ${Math.round(config.minFairValue * 100)}%`,
                  `  Interval:     ${config.intervalSeconds}s`,
                  `  Dry run:      ${config.dryRun}`,
                ].join("\n"),
              },
            ],
          }
        } catch (err) {
          return {
            content: [
              {
                type: "text" as const,
                text: `Error starting weather arb: ${err instanceof Error ? err.message : String(err)}`,
              },
            ],
          }
        }
      },
    },
    { optional: true },
  )

  // ── stop_weather_arb ───────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "stop_weather_arb",
      description: "Stop the Polymarket weather arbitrage scanner.",
      parameters: { type: "object", properties: {} },
      execute: async () => {
        try {
          strategyManager.stopWeatherArb()
          return { content: [{ type: "text" as const, text: "Weather arb scanner stopped." }] }
        } catch (err) {
          return {
            content: [
              {
                type: "text" as const,
                text: `Error stopping weather arb: ${err instanceof Error ? err.message : String(err)}`,
              },
            ],
          }
        }
      },
    },
    { optional: true },
  )

  // ── get_strategy_status ────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "get_strategy_status",
      description:
        "Returns formatted status of both the pumpfun and Polymarket weather_arb scanners including latest per-city readings.",
      parameters: { type: "object", properties: {} },
      execute: async () => {
        const s = strategyManager.getStatus()

        const sourceLine =
          s._source
            ? `  Source:           ${s._source}${s._stale ? " ⚠ stale" : ""}`
            : null

        const cityLines = s.weather_arb.lastReadings.map((r) => {
          const edgeStr   = r.bestEdge   != null ? ` edge=${Math.round(r.bestEdge * 100)}%` : ""
          const bracketStr = r.targetBracket ? ` bracket="${r.targetBracket}"` : ""
          const skipStr   = r.skippedReason ? ` (${r.skippedReason})` : ""
          return `    ${r.city.padEnd(8)}: ${r.forecastHighF}°F${bracketStr}${edgeStr}${skipStr}`
        })

        const lines = [
          `── Pumpfun Scanner ─────────────────────`,
          `  Running:          ${s.pumpfun.running}`,
          `  Graduations seen: ${s.pumpfun.lastGraduations}`,
          `  Last check:       ${s.pumpfun.lastCheckAt ?? "never"}`,
          ``,
          `── Weather Arb Scanner ──────────────────`,
          ...(sourceLine ? [sourceLine] : []),
          `  Running:          ${s.weather_arb.running}`,
          `  Cities:           ${s.weather_arb.cities.join(", ") || "not configured"}`,
          `  Last check:       ${s.weather_arb.lastCheckAt ?? "never"}`,
          ...cityLines,
          ``,
          `── X Strategy ────────────────────────────`,
          `  Running:          ${s.x_strategy.running}`,
          `  Tweets this hour: ${s.x_strategy.tweetsThisHour}`,
          `  Last check:       ${s.x_strategy.lastCheckAt ?? "never"}`,
          `  Last tweet ID:    ${s.x_strategy.lastTweetId ?? "none"}`,
        ]
        return { content: [{ type: "text" as const, text: lines.join("\n") }] }
      },
    },
    { optional: true },
  )

  // ── Helper: build XConfig from env ────────────────────────────────────────
  const getXConfig = (): XConfig => ({
    apiKey:             X_API_KEY,
    apiSecret:          X_API_SECRET,
    accessToken:        X_ACCESS_TOKEN,
    accessTokenSecret:  X_ACCESS_TOKEN_SECRET,
    bearerToken:        X_BEARER_TOKEN,
  })

  // ── x_post_tweet ──────────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "x_post_tweet",
      description: "Post a tweet from the configured X/Twitter account.",
      parameters: {
        type: "object",
        properties: {
          text: { type: "string", description: "Tweet text (max 280 chars)" },
        },
        required: ["text"],
      },
      execute: async (_id, params) => {
        try {
          const { text } = params as { text: string }
          const { rw } = createXClients(getXConfig())
          const tweet = await postTweet(rw, text.slice(0, 280))
          return { content: [{ type: "text" as const, text: `Tweet posted: https://x.com/i/web/status/${tweet.id}` }] }
        } catch (err) {
          return { content: [{ type: "text" as const, text: `Error posting tweet: ${err instanceof Error ? err.message : String(err)}` }] }
        }
      },
    },
    { optional: true },
  )

  // ── x_reply ───────────────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "x_reply",
      description: "Reply to a specific tweet by ID.",
      parameters: {
        type: "object",
        properties: {
          tweet_id: { type: "string", description: "ID of the tweet to reply to" },
          text: { type: "string", description: "Reply text (max 280 chars)" },
        },
        required: ["tweet_id", "text"],
      },
      execute: async (_id, params) => {
        try {
          const { tweet_id, text } = params as { tweet_id: string; text: string }
          const { rw } = createXClients(getXConfig())
          const tweet = await replyToTweet(rw, tweet_id, text.slice(0, 280))
          return { content: [{ type: "text" as const, text: `Reply posted: https://x.com/i/web/status/${tweet.id}` }] }
        } catch (err) {
          return { content: [{ type: "text" as const, text: `Error replying: ${err instanceof Error ? err.message : String(err)}` }] }
        }
      },
    },
    { optional: true },
  )

  // ── x_search ──────────────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "x_search",
      description: "Search recent tweets (last 7 days). Requires Basic+ tier on X API.",
      parameters: {
        type: "object",
        properties: {
          query:       { type: "string", description: "Search query, e.g. \"pump.fun graduation -is:retweet\"" },
          max_results: { type: "number", description: "Max tweets to return (default 10, max 100)" },
        },
        required: ["query"],
      },
      execute: async (_id, params) => {
        try {
          const { query, max_results } = params as { query: string; max_results?: number }
          const { ro } = createXClients(getXConfig())
          const tweets = await searchTweets(ro, query, max_results ?? 10)
          if (tweets.length === 0) return { content: [{ type: "text" as const, text: "No tweets found." }] }
          const lines = tweets.map(t => `[${t.id}] @${t.authorId ?? "?"}: ${t.text.slice(0, 120)}`)
          return { content: [{ type: "text" as const, text: lines.join("\n") }] }
        } catch (err) {
          return { content: [{ type: "text" as const, text: `Error searching: ${err instanceof Error ? err.message : String(err)}` }] }
        }
      },
    },
    { optional: true },
  )

  // ── x_get_mentions ────────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "x_get_mentions",
      description: "Fetch recent mentions of the authenticated bot account.",
      parameters: {
        type: "object",
        properties: {
          since_id: { type: "string", description: "Only return tweets newer than this tweet ID" },
        },
      },
      execute: async (_id, params) => {
        try {
          const { since_id } = params as { since_id?: string }
          const clients = createXClients(getXConfig())
          const userId = await clients.userId()
          const mentions = await getMentions(clients.rw, userId, since_id)
          if (mentions.length === 0) return { content: [{ type: "text" as const, text: "No new mentions." }] }
          const lines = mentions.map(t => `[${t.id}] @${t.authorId ?? "?"}: ${t.text.slice(0, 120)}`)
          return { content: [{ type: "text" as const, text: lines.join("\n") }] }
        } catch (err) {
          return { content: [{ type: "text" as const, text: `Error fetching mentions: ${err instanceof Error ? err.message : String(err)}` }] }
        }
      },
    },
    { optional: true },
  )

  // ── x_resolve_user ────────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "x_resolve_user",
      description: "Look up a Twitter/X user by @handle and return their user ID.",
      parameters: {
        type: "object",
        properties: {
          handle: { type: "string", description: "Twitter handle with or without @, e.g. \"elonmusk\"" },
        },
        required: ["handle"],
      },
      execute: async (_id, params) => {
        try {
          const { handle } = params as { handle: string }
          const { ro } = createXClients(getXConfig())
          const user = await resolveUser(ro, handle)
          return { content: [{ type: "text" as const, text: `@${user.username} (${user.name})\n  User ID: ${user.id}` }] }
        } catch (err) {
          return { content: [{ type: "text" as const, text: `Error resolving user: ${err instanceof Error ? err.message : String(err)}` }] }
        }
      },
    },
    { optional: true },
  )

  // ── start_x_strategy ──────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "start_x_strategy",
      description:
        "Start the X/Twitter strategy: polls mentions, monitors keywords, and optionally posts trade updates automatically.",
      parameters: {
        type: "object",
        properties: {
          handle:                 { type: "string",  description: "Bot's X handle (without @)" },
          monitor_keywords:       { type: "array", items: { type: "string" }, description: "Keywords to watch, e.g. [\"pump.fun\",\"graduation\"]" },
          auto_reply_to_mentions: { type: "boolean", description: "Auto-reply to mentions (default false)" },
          post_trade_updates:     { type: "boolean", description: "Tweet when a trade fires (default true)" },
          max_tweets_per_hour:    { type: "number",  description: "Hard cap on outbound tweets per hour (default 2)" },
          interval_seconds:       { type: "number",  description: "Poll interval in seconds (default 60)" },
          dry_run:                { type: "boolean", description: "Log tweets without sending (default true)" },
        },
        required: ["handle"],
      },
      execute: async (_id, params) => {
        try {
          const p = params as {
            handle: string
            monitor_keywords?: string[]
            auto_reply_to_mentions?: boolean
            post_trade_updates?: boolean
            max_tweets_per_hour?: number
            interval_seconds?: number
            dry_run?: boolean
          }

          if (strategyManager.getStatus().x_strategy.running) {
            return { content: [{ type: "text" as const, text: "X strategy is already running. Use stop_x_strategy first." }] }
          }

          const config: XStrategyConfig = {
            handle:                 p.handle,
            monitorKeywords:        p.monitor_keywords       ?? [],
            autoReplyToMentions:    p.auto_reply_to_mentions ?? false,
            postTradeUpdates:       p.post_trade_updates     ?? true,
            maxTweetsPerHour:       p.max_tweets_per_hour    ?? 2,
            intervalSeconds:        p.interval_seconds       ?? 60,
            dryRun:                 p.dry_run                ?? true,
          }

          strategyManager.startXStrategy(getXConfig(), config)

          return {
            content: [{
              type: "text" as const,
              text: [
                "X strategy started.",
                `  Handle:        @${config.handle}`,
                `  Keywords:      ${config.monitorKeywords.join(", ") || "none"}`,
                `  Auto-reply:    ${config.autoReplyToMentions}`,
                `  Trade updates: ${config.postTradeUpdates}`,
                `  Max tweets/hr: ${config.maxTweetsPerHour}`,
                `  Interval:      ${config.intervalSeconds}s`,
                `  Dry run:       ${config.dryRun}`,
              ].join("\n"),
            }],
          }
        } catch (err) {
          return { content: [{ type: "text" as const, text: `Error starting X strategy: ${err instanceof Error ? err.message : String(err)}` }] }
        }
      },
    },
    { optional: true },
  )

  // ── stop_x_strategy ───────────────────────────────────────────────────────
  api.registerTool(
    {
      name: "stop_x_strategy",
      description: "Stop the X/Twitter strategy.",
      parameters: { type: "object", properties: {} },
      execute: async () => {
        try {
          strategyManager.stopXStrategy()
          return { content: [{ type: "text" as const, text: "X strategy stopped." }] }
        } catch (err) {
          return { content: [{ type: "text" as const, text: `Error stopping X strategy: ${err instanceof Error ? err.message : String(err)}` }] }
        }
      },
    },
    { optional: true },
  )
}
