/**
 * X (Twitter) strategy — polls mentions + keyword feed, posts trade updates.
 *
 * Safety rules enforced here:
 *  - Hard cap: maxTweetsPerHour (default 2) — rolling window
 *  - Never auto-likes or auto-retweets (TOS violation)
 *  - dryRun mode logs all outbound tweets without sending
 */
import { createXClients, getMentions, searchTweets, postTweet, replyToTweet } from "./xClient.ts"
import type { XConfig, XStrategyConfig, Tweet } from "./types.ts"

// ── State ─────────────────────────────────────────────────────────────────────

export type XStrategyState = {
  running: boolean
  lastCheckAt: string | null
  tweetsThisHour: number
  lastTweetId: string | null
  /** id of the last seen mention — used as since_id for incremental polling */
  lastMentionId: string | null
}

const initialState = (): XStrategyState => ({
  running: false,
  lastCheckAt: null,
  tweetsThisHour: 0,
  lastTweetId: null,
  lastMentionId: null,
})

// ── Rate-limit guard ──────────────────────────────────────────────────────────

type TweetTimestamp = number  // epoch ms

const recentTweets: TweetTimestamp[] = []

const canTweet = (maxPerHour: number): boolean => {
  const now = Date.now()
  const hourAgo = now - 60 * 60 * 1_000
  // purge old entries
  while (recentTweets.length && recentTweets[0]! < hourAgo) recentTweets.shift()
  return recentTweets.length < maxPerHour
}

const recordTweet = (): void => { recentTweets.push(Date.now()) }

// ── Jitter helper — avoids mechanical posting intervals ──────────────────────

const jitter = (ms: number, pct = 0.2): number =>
  ms + Math.floor((Math.random() * 2 - 1) * ms * pct)

// ── Main strategy tick ────────────────────────────────────────────────────────

export const runXStrategyTick = async (
  xConfig: XConfig,
  strategyConfig: XStrategyConfig,
  state: XStrategyState,
  onStateUpdate: (s: XStrategyState) => void,
): Promise<void> => {
  const { rw, ro, userId } = createXClients(xConfig)
  const next: XStrategyState = { ...state, lastCheckAt: new Date().toISOString() }

  try {
    const uid = await userId()

    // ── 1. Poll mentions ────────────────────────────────────────────────────
    let newMentions: Tweet[] = []
    try {
      newMentions = await getMentions(rw, uid, state.lastMentionId ?? undefined)
    } catch (err) {
      console.warn("[x-strategy] mentions fetch failed (rate limit or auth):", String(err))
    }

    if (newMentions.length > 0) {
      next.lastMentionId = newMentions[0]!.id
      console.log(`[x-strategy] ${newMentions.length} new mention(s)`)

      if (strategyConfig.autoReplyToMentions) {
        for (const mention of newMentions.slice(0, 2)) {  // cap at 2 replies per tick
          await safeTweet(rw, strategyConfig, next, async () => {
            const reply = buildMentionReply(mention.text)
            return replyToTweet(rw, mention.id, reply)
          })
        }
      }
    }

    // ── 2. Keyword monitoring ───────────────────────────────────────────────
    // Requires Basic+ tier — silently skip if we get a 403
    if (strategyConfig.monitorKeywords.length > 0) {
      const query = strategyConfig.monitorKeywords
        .map(k => (k.includes(" ") ? `"${k}"` : k))
        .join(" OR ")
        + " -is:retweet lang:en"

      try {
        const found = await searchTweets(ro, query, 10)
        if (found.length > 0) {
          console.log(`[x-strategy] keyword feed: ${found.length} tweet(s) matching [${strategyConfig.monitorKeywords.join(", ")}]`)
          // Log them; agent (via plugin) decides whether to act
          for (const t of found.slice(0, 3)) {
            console.log(`  @${t.authorId ?? "?"}: ${t.text.slice(0, 80)}…`)
          }
        }
      } catch (err: unknown) {
        const status = (err as { code?: number })?.code
        if (status === 403 || status === 401) {
          console.warn("[x-strategy] Keyword search requires Basic+ tier — skipping")
        } else {
          console.warn("[x-strategy] search failed:", String(err))
        }
      }
    }

  } catch (err) {
    console.error("[x-strategy] tick error:", err instanceof Error ? err.message : String(err))
  }

  // rolling tweet count
  next.tweetsThisHour = recentTweets.length
  onStateUpdate(next)
}

// ── Trade-triggered posting ───────────────────────────────────────────────────

/**
 * Called by strategyManager when any strategy fires a trade.
 * Builds a summary tweet and posts it (respects rate cap + dryRun).
 */
export const postTradeUpdate = async (
  xConfig: XConfig,
  strategyConfig: XStrategyConfig,
  state: XStrategyState,
  onStateUpdate: (s: XStrategyState) => void,
  summary: string,
): Promise<void> => {
  if (!strategyConfig.postTradeUpdates) return
  const { rw } = createXClients(xConfig)

  await safeTweet(rw, strategyConfig, state, async () => {
    const tweet = await postTweet(rw, summary)
    console.log(`[x-strategy] trade update posted: ${tweet.id}`)
    onStateUpdate({ ...state, lastTweetId: tweet.id, tweetsThisHour: recentTweets.length })
    return tweet
  })
}

// ── Helpers ───────────────────────────────────────────────────────────────────

/** Posts a tweet only if within rate cap; dry-run logs instead of sending */
const safeTweet = async (
  rw: ReturnType<typeof createXClients>["rw"],
  config: XStrategyConfig,
  state: XStrategyState,
  fn: () => Promise<Tweet>,
): Promise<Tweet | null> => {
  if (!canTweet(config.maxTweetsPerHour)) {
    console.log(`[x-strategy] rate cap hit (${config.maxTweetsPerHour}/hr) — skipping tweet`)
    return null
  }

  if (config.dryRun) {
    console.log("[x-strategy] [dry-run] would send tweet")
    return null
  }

  try {
    const tweet = await fn()
    recordTweet()
    return tweet
  } catch (err) {
    console.error("[x-strategy] tweet failed:", err instanceof Error ? err.message : String(err))
    return null
  }
}

/**
 * Builds a concise reply for a mention.
 * Keep it simple and varied to avoid template-detection.
 */
const buildMentionReply = (mentionText: string): string => {
  const templates = [
    "On it. Scanning now.",
    "Noted — checking the feed.",
    "Got it. Running analysis.",
    "Acknowledged.",
    "Reading the market. Stand by.",
  ]
  return templates[Math.floor(Math.random() * templates.length)]!
}

// ── Strategy closure (used by strategyManager) ────────────────────────────────

export const createXStrategy = () => {
  let intervalId: NodeJS.Timeout | null = null
  let currentState: XStrategyState = initialState()

  const onStateUpdate = (s: XStrategyState) => { currentState = s }

  const start = (xConfig: XConfig, strategyConfig: XStrategyConfig): void => {
    if (intervalId) return

    currentState = { ...initialState(), running: true }

    const tick = () =>
      runXStrategyTick(xConfig, strategyConfig, currentState, onStateUpdate).catch(console.error)

    tick()  // immediate first tick
    const ms = jitter(strategyConfig.intervalSeconds * 1_000)
    intervalId = setInterval(tick, ms)

    console.log(`[x-strategy] started (interval ~${Math.round(ms / 1000)}s, dryRun=${strategyConfig.dryRun})`)
  }

  const stop = (): void => {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
      currentState = { ...currentState, running: false }
      console.log("[x-strategy] stopped")
    }
  }

  const getState = (): XStrategyState => ({ ...currentState, running: intervalId !== null })

  const onTrade = (xConfig: XConfig, strategyConfig: XStrategyConfig, summary: string): void => {
    postTradeUpdate(xConfig, strategyConfig, currentState, onStateUpdate, summary).catch(console.error)
  }

  return { start, stop, getState, onTrade }
}
