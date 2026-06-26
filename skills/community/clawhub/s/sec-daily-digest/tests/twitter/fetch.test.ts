import { describe, expect, test } from "bun:test";
import { fetchTwitterKols } from "../../src/twitter/fetch";
import type { TwitterSourceConfig } from "../../src/config/sources";
import type { TwitterBackend, TwitterSourceResult } from "../../src/twitter/backends/types";
import type { TweetArticle } from "../../src/twitter/types";

const sources: TwitterSourceConfig[] = [
  { id: "taviso", type: "twitter", name: "Tavis Ormandy", handle: "taviso", enabled: true, priority: true, topics: ["security"] },
];

function makeMockTweet(override?: Partial<TweetArticle>): TweetArticle {
  return {
    tweetId: "12345",
    handle: "taviso",
    displayName: "Tavis Ormandy",
    title: "Security research post",
    link: "https://twitter.com/taviso/status/12345",
    pubDate: new Date("2024-12-10T07:00:00Z"),
    description: "Security research post",
    sourceName: "Tavis Ormandy",
    sourceUrl: "https://twitter.com/taviso",
    metrics: { like_count: 100, retweet_count: 50, reply_count: 10, quote_count: 5, impression_count: 5000 },
    ...override,
  };
}

function makeMockBackend(tweets: TweetArticle[]): TwitterBackend {
  return {
    async fetch(): Promise<TwitterSourceResult[]> {
      return [{
        sourceId: "taviso",
        handle: "taviso",
        status: "ok",
        count: tweets.length,
        tweets,
      }];
    },
  };
}

describe("fetchTwitterKols", () => {
  test("returns articles with Article-compatible fields", async () => {
    const tweet = makeMockTweet();
    const backend = makeMockBackend([tweet]);
    const { articles, results } = await fetchTwitterKols(sources, {
      hours: 48,
      env: {} as NodeJS.ProcessEnv,
      backend,
    });

    expect(articles).toHaveLength(1);
    expect(results).toHaveLength(1);

    const article = articles[0]!;
    expect(typeof article.title).toBe("string");
    expect(typeof article.link).toBe("string");
    expect(article.pubDate).toBeInstanceOf(Date);
    expect(typeof article.description).toBe("string");
    expect(typeof article.sourceName).toBe("string");
    expect(typeof article.sourceUrl).toBe("string");
    expect(typeof article.tweetId).toBe("string");
    expect(typeof article.handle).toBe("string");
  });

  test("returns empty when null backend (no credentials)", async () => {
    const { articles, results } = await fetchTwitterKols(sources, {
      hours: 48,
      env: {} as NodeJS.ProcessEnv, // no credentials → null backend
    });
    expect(articles).toHaveLength(0);
    expect(results).toHaveLength(0);
  });

  test("returns empty when sources list is empty", async () => {
    const backend = makeMockBackend([makeMockTweet()]);
    const { articles } = await fetchTwitterKols([], {
      hours: 48,
      env: {} as NodeJS.ProcessEnv,
      backend,
    });
    expect(articles).toHaveLength(0);
  });
});
