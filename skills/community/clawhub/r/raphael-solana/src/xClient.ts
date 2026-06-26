import { TwitterApi } from "twitter-api-v2"
import type { TwitterApiReadWrite, TwitterApiReadOnly } from "twitter-api-v2"
import { TwitterApiRateLimitPlugin } from "@twitter-api-v2/plugin-rate-limit"
import type { XConfig, Tweet, XUser } from "./types.ts"

// ── Client factory ────────────────────────────────────────────────────────────

export type XClients = {
  /** OAuth 1.0a user context — required for writes (tweet, reply, like, retweet) */
  rw: TwitterApiReadWrite
  /** OAuth 2.0 app-only — efficient for searches and timeline reads */
  ro: TwitterApiReadOnly
  /** Resolved user ID for the authenticated account (lazy-populated) */
  userId: () => Promise<string>
}

let _userId: string | null = null

export const createXClients = (config: XConfig): XClients => {
  const rateLimitPlugin = new TwitterApiRateLimitPlugin()

  const userClient = new TwitterApi(
    {
      appKey:        config.apiKey,
      appSecret:     config.apiSecret,
      accessToken:   config.accessToken,
      accessSecret:  config.accessTokenSecret,
    },
    { plugins: [rateLimitPlugin] },
  )

  const appClient = new TwitterApi(config.bearerToken, { plugins: [rateLimitPlugin] })

  const rw = userClient.readWrite
  const ro = appClient.readOnly

  const userId = async (): Promise<string> => {
    if (_userId) return _userId
    const me = await rw.v2.me()
    _userId = me.data.id
    return _userId
  }

  return { rw, ro, userId }
}

// ── Write operations ──────────────────────────────────────────────────────────

export const postTweet = async (
  rw: TwitterApiReadWrite,
  text: string,
): Promise<Tweet> => {
  const res = await rw.v2.tweet(text)
  return { id: res.data.id, text: res.data.text ?? text, createdAt: new Date().toISOString() }
}

export const replyToTweet = async (
  rw: TwitterApiReadWrite,
  tweetId: string,
  text: string,
): Promise<Tweet> => {
  const res = await rw.v2.reply(text, tweetId)
  return { id: res.data.id, text: res.data.text ?? text, createdAt: new Date().toISOString() }
}

export const likeTweet = async (
  rw: TwitterApiReadWrite,
  userId: string,
  tweetId: string,
): Promise<void> => {
  await rw.v2.like(userId, tweetId)
}

export const retweetTweet = async (
  rw: TwitterApiReadWrite,
  userId: string,
  tweetId: string,
): Promise<void> => {
  await rw.v2.retweet(userId, tweetId)
}

export const deleteTweet = async (
  rw: TwitterApiReadWrite,
  tweetId: string,
): Promise<void> => {
  await rw.v2.deleteTweet(tweetId)
}

// ── Read operations ───────────────────────────────────────────────────────────

export const searchTweets = async (
  ro: TwitterApiReadOnly,
  query: string,
  maxResults = 10,
): Promise<Tweet[]> => {
  const res = await ro.v2.search(query, {
    max_results: Math.min(maxResults, 100) as 10,
    "tweet.fields": ["created_at", "author_id", "conversation_id", "in_reply_to_user_id"],
  })
  return (res.data.data ?? []).map(t => ({
    id: t.id,
    text: t.text,
    authorId: t.author_id,
    createdAt: t.created_at ?? "",
    conversationId: t.conversation_id,
  }))
}

export const getMentions = async (
  rw: TwitterApiReadWrite,
  userId: string,
  sinceId?: string,
): Promise<Tweet[]> => {
  const params: Record<string, unknown> = {
    max_results: 10,
    "tweet.fields": ["created_at", "author_id", "conversation_id"],
  }
  if (sinceId) params["since_id"] = sinceId

  const res = await rw.v2.userMentionTimeline(userId, params as any)
  return (res.data.data ?? []).map(t => ({
    id: t.id,
    text: t.text,
    authorId: t.author_id,
    createdAt: t.created_at ?? "",
    conversationId: t.conversation_id,
  }))
}

export const getUserTimeline = async (
  ro: TwitterApiReadOnly,
  userId: string,
  maxResults = 10,
): Promise<Tweet[]> => {
  const res = await ro.v2.userTimeline(userId, {
    max_results: Math.min(maxResults, 100) as 10,
    "tweet.fields": ["created_at", "author_id"],
    exclude: ["retweets", "replies"],
  })
  return (res.data.data ?? []).map(t => ({
    id: t.id,
    text: t.text,
    authorId: t.author_id,
    createdAt: t.created_at ?? "",
  }))
}

export const resolveUser = async (
  ro: TwitterApiReadOnly,
  handle: string,
): Promise<XUser> => {
  const username = handle.replace(/^@/, "")
  const res = await ro.v2.userByUsername(username, {
    "user.fields": ["name", "username", "public_metrics"],
  })
  if (!res.data) throw new Error(`User @${username} not found`)
  return {
    id: res.data.id,
    name: res.data.name,
    username: res.data.username,
  }
}
