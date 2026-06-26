import { describe, expect, test } from "bun:test";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { createOfficialBackend } from "../../../src/twitter/backends/official";
import type { TwitterSourceConfig } from "../../../src/config/sources";

const sources: TwitterSourceConfig[] = [
  { id: "taviso", type: "twitter", name: "Tavis Ormandy", handle: "taviso", enabled: true, priority: true, topics: ["security"] },
];

const cutoff = new Date("2024-01-01T00:00:00Z");

describe("createOfficialBackend", () => {
  test("caches user IDs to disk", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "official-backend-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;
    let userLookupCalled = 0;

    const fetcher = async (url: string): Promise<Response> => {
      if (url.includes("/users/by")) {
        userLookupCalled++;
        return new Response(JSON.stringify({
          data: [{ id: "12345", name: "Tavis Ormandy", username: "taviso" }],
        }), { status: 200 });
      }
      // Tweets endpoint
      return new Response(JSON.stringify({
        data: [{
          id: "tweet1",
          text: "Security research post",
          created_at: "2024-12-10T07:00:00.000Z",
          public_metrics: { like_count: 100, retweet_count: 50, reply_count: 10, quote_count: 5, impression_count: 5000 },
        }],
      }), { status: 200 });
    };

    const backend1 = createOfficialBackend("bearer-token", env, fetcher as typeof fetch);
    await backend1.fetch(sources, cutoff);
    expect(userLookupCalled).toBe(1);

    // Second call should use cache
    const backend2 = createOfficialBackend("bearer-token", env, fetcher as typeof fetch);
    await backend2.fetch(sources, cutoff);
    expect(userLookupCalled).toBe(1); // still 1, used cache

    // Verify cache file exists
    const cacheContent = await readFile(path.join(tempDir, "twitter-id-cache.json"), "utf8");
    const cache = JSON.parse(cacheContent);
    expect(cache.taviso?.id).toBe("12345");

    await rm(tempDir, { recursive: true, force: true });
  });

  test("filters replied_to tweets", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "official-backend-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const fetcher = async (url: string): Promise<Response> => {
      if (url.includes("/users/by")) {
        return new Response(JSON.stringify({
          data: [{ id: "12345", name: "Tavis Ormandy", username: "taviso" }],
        }), { status: 200 });
      }
      return new Response(JSON.stringify({
        data: [
          {
            id: "tweet1",
            text: "A reply tweet",
            created_at: "2024-12-10T07:00:00.000Z",
            referenced_tweets: [{ type: "replied_to", id: "other123" }],
          },
          {
            id: "tweet2",
            text: "Original post",
            created_at: "2024-12-10T07:00:00.000Z",
          },
        ],
      }), { status: 200 });
    };

    const backend = createOfficialBackend("bearer-token", env, fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(results[0]?.tweets).toHaveLength(1);
    expect(results[0]?.tweets[0]?.tweetId).toBe("tweet2");

    await rm(tempDir, { recursive: true, force: true });
  });

  test("filters RT @ tweets", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "official-backend-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const fetcher = async (url: string): Promise<Response> => {
      if (url.includes("/users/by")) {
        return new Response(JSON.stringify({
          data: [{ id: "12345", name: "Tavis Ormandy", username: "taviso" }],
        }), { status: 200 });
      }
      return new Response(JSON.stringify({
        data: [
          { id: "tweet1", text: "RT @someone: some content", created_at: "2024-12-10T07:00:00.000Z" },
          { id: "tweet2", text: "My original thought", created_at: "2024-12-10T07:00:00.000Z" },
        ],
      }), { status: 200 });
    };

    const backend = createOfficialBackend("bearer-token", env, fetcher as typeof fetch);
    const results = await backend.fetch(sources, cutoff);
    expect(results[0]?.tweets).toHaveLength(1);
    expect(results[0]?.tweets[0]?.tweetId).toBe("tweet2");

    await rm(tempDir, { recursive: true, force: true });
  });
});
