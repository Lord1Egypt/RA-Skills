import { describe, expect, test } from "bun:test";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { runPipeline } from "../../src/pipeline/run";
import type { TwitterSourceResult } from "../../src/twitter/backends/types";
import type { TweetArticle } from "../../src/twitter/types";

const TEST_NOW = new Date("2026-02-27T12:00:00Z");

const seedArticles = [
  {
    title: "Critical CVE in AI gateway",
    link: "https://example.com/a",
    pubDate: new Date("2026-02-27T10:00:00Z"),
    description: "CVE-2026-11111 affects model serving layer",
    sourceName: "source-a",
    sourceUrl: "https://example.com",
  },
  {
    title: "New agent evaluation benchmark",
    link: "https://example.com/b",
    pubDate: new Date("2026-02-27T09:00:00Z"),
    description: "LLM agent evaluation and reproducibility notes",
    sourceName: "source-b",
    sourceUrl: "https://example.com",
  },
];

function makeSeedTwitterResult(tweets: TweetArticle[]): TwitterSourceResult {
  return {
    sourceId: "taviso",
    handle: "taviso",
    status: "ok",
    count: tweets.length,
    tweets,
  };
}

function makeTweetArticle(id: string): TweetArticle {
  return {
    tweetId: id,
    handle: "taviso",
    displayName: "Tavis Ormandy",
    title: `Security tweet ${id}`,
    link: `https://twitter.com/taviso/status/${id}`,
    pubDate: new Date("2026-02-27T08:00:00Z"), // within 48h of TEST_NOW
    description: `Security tweet ${id}`,
    sourceName: "Tavis Ormandy",
    sourceUrl: "https://twitter.com/taviso",
    metrics: { like_count: 100, retweet_count: 50, reply_count: 10, quote_count: 5, impression_count: 5000 },
  };
}

describe("runPipeline", () => {
  test("returns output path and summary counters", async () => {
    const tempRoot = await mkdtemp(path.join(os.tmpdir(), "sec-pipeline-"));
    const outputPath = path.join(tempRoot, "digest.md");

    const result = await runPipeline({
      dryRun: true,
      outputPath,
      now: TEST_NOW,
      env: {
        SEC_DAILY_DIGEST_HOME: tempRoot,
      } as NodeJS.ProcessEnv,
      seedArticles,
    });

    expect(result.outputPath).toBe(outputPath);
    expect(result.counters.articles).toBe(2);
    expect(result.counters.selected).toBeGreaterThan(0);
    expect(result.counters.twitter_kols).toBe(0);

    const report = await readFile(outputPath, "utf8");
    expect(report).toContain("## AI发展");
    expect(report).toContain("## 安全动态");
    expect(report).toContain("## 📝 今日趋势");
    expect(report).toContain("## 漏洞专报");

    await rm(tempRoot, { recursive: true, force: true });
  });

  test("twitter_kols counter reflects injected twitter results", async () => {
    const tempRoot = await mkdtemp(path.join(os.tmpdir(), "sec-pipeline-"));
    const outputPath = path.join(tempRoot, "digest.md");

    const tweetArticles = [makeTweetArticle("tweet1"), makeTweetArticle("tweet2")];
    const seedTwitterResults = [makeSeedTwitterResult(tweetArticles)];

    const result = await runPipeline({
      dryRun: true,
      outputPath,
      now: TEST_NOW,
      env: {
        SEC_DAILY_DIGEST_HOME: tempRoot,
      } as NodeJS.ProcessEnv,
      seedArticles,
      seedTwitterResults,
    });

    expect(result.counters.twitter_kols).toBe(2);

    const report = await readFile(outputPath, "utf8");
    expect(report).toContain("## 🔐 Security KOL Updates");

    await rm(tempRoot, { recursive: true, force: true });
  });

  test("no credentials → twitter_kols: 0 (no crash)", async () => {
    const tempRoot = await mkdtemp(path.join(os.tmpdir(), "sec-pipeline-"));
    const outputPath = path.join(tempRoot, "digest.md");

    const result = await runPipeline({
      dryRun: true,
      outputPath,
      now: TEST_NOW,
      env: {
        SEC_DAILY_DIGEST_HOME: tempRoot,
        // No TWITTERAPI_IO_KEY or X_BEARER_TOKEN
      } as NodeJS.ProcessEnv,
      seedArticles,
    });

    expect(result.counters.twitter_kols).toBe(0);
    await rm(tempRoot, { recursive: true, force: true });
  });

  test("--no-twitter flag disables twitter fetch", async () => {
    const tempRoot = await mkdtemp(path.join(os.tmpdir(), "sec-pipeline-"));
    const outputPath = path.join(tempRoot, "digest.md");

    const result = await runPipeline({
      dryRun: true,
      outputPath,
      now: TEST_NOW,
      twitterEnabled: false,
      env: {
        SEC_DAILY_DIGEST_HOME: tempRoot,
        TWITTERAPI_IO_KEY: "fake-key", // has credential but twitter disabled
      } as NodeJS.ProcessEnv,
      seedArticles,
    });

    expect(result.counters.twitter_kols).toBe(0);
    await rm(tempRoot, { recursive: true, force: true });
  });
});
