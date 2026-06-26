import type { TwitterSourceConfig } from "../../config/sources";
import type { TweetArticle } from "../types";
import { RateLimiter, type TwitterBackend, type TwitterSourceResult } from "./types";

const MAX_PAGES = 2;
const MAX_CONCURRENT = 3;
const RETRY_DELAYS = [250, 500];
const RATE_LIMIT_WAIT = 5000;

interface ApiTweet {
  id: string;
  text: string;
  created_at: string;
  retweetedTweet?: unknown;
  public_metrics?: {
    like_count?: number;
    retweet_count?: number;
    reply_count?: number;
    quote_count?: number;
    impression_count?: number;
  };
}

interface ApiResponse {
  tweets?: ApiTweet[];
  has_next_page?: boolean;
  next_cursor?: string;
}

async function sleep(ms: number): Promise<void> {
  await new Promise<void>((resolve) => setTimeout(resolve, ms));
}

async function fetchPage(
  handle: string,
  apiKey: string,
  cursor: string | undefined,
  fetcher: typeof fetch,
): Promise<ApiResponse> {
  const url = new URL("https://api.twitterapi.io/twitter/user/last_tweets");
  url.searchParams.set("userName", handle);
  url.searchParams.set("includeReplies", "false");
  if (cursor) {
    url.searchParams.set("cursor", cursor);
  }

  for (let attempt = 0; attempt <= RETRY_DELAYS.length; attempt++) {
    const response = await fetcher(url.toString(), {
      headers: { "X-API-Key": apiKey },
    });

    if (response.status === 429) {
      await sleep(RATE_LIMIT_WAIT);
      continue;
    }

    if (!response.ok) {
      if (attempt < RETRY_DELAYS.length) {
        await sleep(RETRY_DELAYS[attempt]!);
        continue;
      }
      throw new Error(`HTTP ${response.status}`);
    }

    return (await response.json()) as ApiResponse;
  }

  throw new Error("Max retries exceeded");
}

function buildTweetArticle(tweet: ApiTweet, source: TwitterSourceConfig): TweetArticle {
  const m = tweet.public_metrics ?? {};
  return {
    tweetId: tweet.id,
    handle: source.handle,
    displayName: source.name,
    title: tweet.text,
    link: `https://twitter.com/${source.handle}/status/${tweet.id}`,
    pubDate: new Date(tweet.created_at),
    description: tweet.text,
    sourceName: source.name,
    sourceUrl: `https://twitter.com/${source.handle}`,
    metrics: {
      like_count: m.like_count ?? 0,
      retweet_count: m.retweet_count ?? 0,
      reply_count: m.reply_count ?? 0,
      quote_count: m.quote_count ?? 0,
      impression_count: m.impression_count ?? 0,
    },
  };
}

async function fetchSourceTweets(
  source: TwitterSourceConfig,
  cutoff: Date,
  apiKey: string,
  limiter: RateLimiter,
  fetcher: typeof fetch,
): Promise<TwitterSourceResult> {
  try {
    const tweets: TweetArticle[] = [];
    let cursor: string | undefined;

    for (let page = 0; page < MAX_PAGES; page++) {
      await limiter.wait();
      const data = await fetchPage(source.handle, apiKey, cursor, fetcher);
      const rawTweets = data.tweets ?? [];

      for (const tweet of rawTweets) {
        if (tweet.retweetedTweet !== undefined) continue;
        if (tweet.text.startsWith("RT @")) continue;
        if (new Date(tweet.created_at) < cutoff) continue;
        tweets.push(buildTweetArticle(tweet, source));
      }

      if (!data.has_next_page || !data.next_cursor) break;
      cursor = data.next_cursor;
    }

    return {
      sourceId: source.id,
      handle: source.handle,
      status: "ok",
      count: tweets.length,
      tweets,
    };
  } catch (error) {
    return {
      sourceId: source.id,
      handle: source.handle,
      status: "error",
      count: 0,
      tweets: [],
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

export function createTwitterApiIoBackend(apiKey: string, fetcher: typeof fetch = fetch): TwitterBackend {
  return {
    async fetch(sources: TwitterSourceConfig[], cutoff: Date): Promise<TwitterSourceResult[]> {
      const limiter = new RateLimiter(5);
      const results: TwitterSourceResult[] = [];

      for (let i = 0; i < sources.length; i += MAX_CONCURRENT) {
        const batch = sources.slice(i, i + MAX_CONCURRENT);
        const batchResults = await Promise.all(
          batch.map((source) => fetchSourceTweets(source, cutoff, apiKey, limiter, fetcher)),
        );
        results.push(...batchResults);
      }

      return results;
    },
  };
}
