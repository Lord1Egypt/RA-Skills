import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import type { TwitterSourceConfig } from "../../config/sources";
import { getStateRoot } from "../../config/paths";
import type { TweetArticle } from "../types";
import type { TwitterBackend, TwitterSourceResult } from "./types";

const MAX_CONCURRENT = 5;
const RETRY_DELAYS = [1000, 2000];
const RATE_LIMIT_WAIT = 60_000;
const ID_CACHE_TTL = 7 * 24 * 3600_000;

interface IdCache {
  [handle: string]: { id: string; cachedAt: number };
}

interface V2Tweet {
  id: string;
  text: string;
  created_at?: string;
  public_metrics?: {
    like_count?: number;
    retweet_count?: number;
    reply_count?: number;
    quote_count?: number;
    impression_count?: number;
  };
  referenced_tweets?: Array<{ type: string; id: string }>;
}

interface V2UserLookupData {
  id: string;
  name: string;
  username: string;
}

async function sleep(ms: number): Promise<void> {
  await new Promise<void>((resolve) => setTimeout(resolve, ms));
}

async function apiFetch<T>(url: string, bearerToken: string, fetcher: typeof fetch): Promise<T> {
  for (let attempt = 0; attempt <= RETRY_DELAYS.length; attempt++) {
    const response = await fetcher(url, {
      headers: { Authorization: `Bearer ${bearerToken}` },
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

    return (await response.json()) as T;
  }

  throw new Error("Max retries exceeded");
}

async function loadIdCache(env: NodeJS.ProcessEnv): Promise<IdCache> {
  try {
    const cachePath = path.join(getStateRoot(env), "twitter-id-cache.json");
    const content = await readFile(cachePath, "utf8");
    return JSON.parse(content) as IdCache;
  } catch {
    return {};
  }
}

async function saveIdCache(cache: IdCache, env: NodeJS.ProcessEnv): Promise<void> {
  const root = getStateRoot(env);
  await mkdir(root, { recursive: true });
  const cachePath = path.join(root, "twitter-id-cache.json");
  await writeFile(cachePath, JSON.stringify(cache, null, 2), "utf8");
}

async function resolveHandleIds(
  handles: string[],
  bearerToken: string,
  cache: IdCache,
  fetcher: typeof fetch,
): Promise<Map<string, string>> {
  const now = Date.now();
  const idMap = new Map<string, string>();
  const needFetch: string[] = [];

  for (const handle of handles) {
    const key = handle.toLowerCase();
    const cached = cache[key];
    if (cached && now - cached.cachedAt < ID_CACHE_TTL) {
      idMap.set(handle.toLowerCase(), cached.id);
    } else {
      needFetch.push(handle);
    }
  }

  for (let i = 0; i < needFetch.length; i += 100) {
    const batch = needFetch.slice(i, i + 100);
    const url = `https://api.x.com/2/users/by?usernames=${batch.join(",")}`;
    try {
      const data = await apiFetch<{ data?: V2UserLookupData[] }>(url, bearerToken, fetcher);
      for (const user of data.data ?? []) {
        const key = user.username.toLowerCase();
        idMap.set(key, user.id);
        cache[key] = { id: user.id, cachedAt: now };
      }
    } catch (error) {
      console.warn(`[twitter/official] user lookup failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  return idMap;
}

async function fetchUserTweets(
  source: TwitterSourceConfig,
  userId: string,
  cutoff: Date,
  bearerToken: string,
  fetcher: typeof fetch,
): Promise<TwitterSourceResult> {
  try {
    const url = `https://api.x.com/2/users/${userId}/tweets?max_results=20&tweet.fields=created_at,public_metrics,referenced_tweets`;
    const data = await apiFetch<{ data?: V2Tweet[] }>(url, bearerToken, fetcher);
    const tweets: TweetArticle[] = [];

    for (const tweet of data.data ?? []) {
      if (tweet.text.startsWith("RT @")) continue;
      if (tweet.referenced_tweets?.some((r) => r.type === "replied_to")) continue;
      const pubDate = tweet.created_at ? new Date(tweet.created_at) : new Date(0);
      if (pubDate < cutoff) continue;

      const m = tweet.public_metrics ?? {};
      tweets.push({
        tweetId: tweet.id,
        handle: source.handle,
        displayName: source.name,
        title: tweet.text,
        link: `https://twitter.com/${source.handle}/status/${tweet.id}`,
        pubDate,
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
      });
    }

    return { sourceId: source.id, handle: source.handle, status: "ok", count: tweets.length, tweets };
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

export function createOfficialBackend(bearerToken: string, env: NodeJS.ProcessEnv, fetcher: typeof fetch = fetch): TwitterBackend {
  return {
    async fetch(sources: TwitterSourceConfig[], cutoff: Date): Promise<TwitterSourceResult[]> {
      const cache = await loadIdCache(env);
      const handles = sources.map((s) => s.handle);
      const idMap = await resolveHandleIds(handles, bearerToken, cache, fetcher);
      await saveIdCache(cache, env);

      const results: TwitterSourceResult[] = [];

      for (let i = 0; i < sources.length; i += MAX_CONCURRENT) {
        const batch = sources.slice(i, i + MAX_CONCURRENT);
        const batchResults = await Promise.all(
          batch.map((source) => {
            const userId = idMap.get(source.handle.toLowerCase());
            if (!userId) {
              return Promise.resolve<TwitterSourceResult>({
                sourceId: source.id,
                handle: source.handle,
                status: "error",
                count: 0,
                tweets: [],
                error: "User ID not found",
              });
            }
            return fetchUserTweets(source, userId, cutoff, bearerToken, fetcher);
          }),
        );
        results.push(...batchResults);
      }

      return results;
    },
  };
}
