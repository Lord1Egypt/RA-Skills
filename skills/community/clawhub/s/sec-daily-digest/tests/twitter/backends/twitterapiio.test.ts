import { describe, expect, test } from "bun:test";
import { createTwitterApiIoBackend } from "../../../src/twitter/backends/twitterapiio";
import type { TwitterSourceConfig } from "../../../src/config/sources";

const sources: TwitterSourceConfig[] = [
  { id: "taviso", type: "twitter", name: "Tavis Ormandy", handle: "taviso", enabled: true, priority: true, topics: ["security"] },
];

const cutoff = new Date("2024-01-01T00:00:00Z");
const recentDate = "Tue Dec 10 07:00:30 +0000 2024";
const oldDate = "Tue Jan 01 00:00:00 +0000 2023";

function makeFetcher(responses: Array<{ status: number; body: unknown }>) {
  let callIndex = 0;
  return async (_url: string, _opts: unknown): Promise<Response> => {
    const resp = responses[callIndex] ?? responses[responses.length - 1]!;
    callIndex++;
    return new Response(JSON.stringify(resp.body), { status: resp.status });
  };
}

describe("createTwitterApiIoBackend", () => {
  test("filters retweets (retweetedTweet field)", async () => {
    const fetcher = makeFetcher([{
      status: 200,
      body: {
        tweets: [
          { id: "1", text: "Normal tweet", created_at: recentDate, retweetedTweet: {} },
          { id: "2", text: "Regular post", created_at: recentDate },
        ],
        has_next_page: false,
      },
    }]);

    const backend = createTwitterApiIoBackend("test-key", fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(results[0]?.tweets).toHaveLength(1);
    expect(results[0]?.tweets[0]?.tweetId).toBe("2");
  });

  test("filters RT @ prefix tweets", async () => {
    const fetcher = makeFetcher([{
      status: 200,
      body: {
        tweets: [
          { id: "1", text: "RT @someone: Some retweet", created_at: recentDate },
          { id: "2", text: "My own post", created_at: recentDate },
        ],
        has_next_page: false,
      },
    }]);

    const backend = createTwitterApiIoBackend("test-key", fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(results[0]?.tweets).toHaveLength(1);
    expect(results[0]?.tweets[0]?.tweetId).toBe("2");
  });

  test("filters tweets older than cutoff", async () => {
    const fetcher = makeFetcher([{
      status: 200,
      body: {
        tweets: [
          { id: "1", text: "Old tweet", created_at: oldDate },
          { id: "2", text: "Recent tweet", created_at: recentDate },
        ],
        has_next_page: false,
      },
    }]);

    const backend = createTwitterApiIoBackend("test-key", fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(results[0]?.tweets).toHaveLength(1);
    expect(results[0]?.tweets[0]?.tweetId).toBe("2");
  });

  test("handles pagination (fetches 2 pages max)", async () => {
    let callCount = 0;
    const fetcher = async (_url: string): Promise<Response> => {
      callCount++;
      if (callCount === 1) {
        return new Response(JSON.stringify({
          tweets: [{ id: "1", text: "Page 1 tweet", created_at: recentDate }],
          has_next_page: true,
          next_cursor: "cursor123",
        }), { status: 200 });
      }
      return new Response(JSON.stringify({
        tweets: [{ id: "2", text: "Page 2 tweet", created_at: recentDate }],
        has_next_page: true,
        next_cursor: "cursor456",
      }), { status: 200 });
    };

    const backend = createTwitterApiIoBackend("test-key", fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(callCount).toBe(2); // max 2 pages
    expect(results[0]?.tweets).toHaveLength(2);
  });

  test("handles 429 retry", async () => {
    let callCount = 0;
    const fetcher = async (): Promise<Response> => {
      callCount++;
      if (callCount === 1) {
        return new Response("rate limited", { status: 429 });
      }
      return new Response(JSON.stringify({
        tweets: [{ id: "1", text: "tweet", created_at: recentDate }],
        has_next_page: false,
      }), { status: 200 });
    };

    const backend = createTwitterApiIoBackend("test-key", fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(results[0]?.status).toBe("ok");
    expect(callCount).toBeGreaterThanOrEqual(2);
  }, 10_000);

  test("returns error status on consistent failure", async () => {
    const fetcher = makeFetcher([{ status: 500, body: "error" }]);

    const backend = createTwitterApiIoBackend("test-key", fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(results[0]?.status).toBe("error");
    expect(results[0]?.count).toBe(0);
  });
});
