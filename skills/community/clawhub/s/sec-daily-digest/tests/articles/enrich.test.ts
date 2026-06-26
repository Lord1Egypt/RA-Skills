import { describe, expect, test } from "bun:test";
import { fetchFullText, enrichArticles, getDomain, SKIP_DOMAINS } from "../../src/articles/enrich";
import type { Article } from "../../src/rss/parse";

function makeArticle(link: string): Article {
  return {
    title: "Test Article",
    link,
    pubDate: new Date(),
    description: "test description",
    sourceName: "Test Source",
    sourceUrl: "https://example.com",
  };
}

describe("getDomain", () => {
  test("strips www prefix and lowercases", () => {
    expect(getDomain("https://www.Example.com/path")).toBe("example.com");
    expect(getDomain("https://TWITTER.COM/status/123")).toBe("twitter.com");
  });

  test("returns empty string on invalid URL", () => {
    expect(getDomain("not-a-url")).toBe("");
  });
});

describe("SKIP_DOMAINS", () => {
  test("contains expected domains", () => {
    expect(SKIP_DOMAINS.has("twitter.com")).toBe(true);
    expect(SKIP_DOMAINS.has("github.com")).toBe(true);
    expect(SKIP_DOMAINS.has("youtube.com")).toBe(true);
  });
});

describe("fetchFullText", () => {
  test("skip domains return immediately without HTTP call", async () => {
    let fetchCalled = false;
    const fakeFetcher = async (): Promise<Response> => {
      fetchCalled = true;
      return new Response("", { status: 200 });
    };

    const result = await fetchFullText("https://twitter.com/status/123", {
      fetcher: fakeFetcher as typeof fetch,
    });
    expect(result.method).toBe("skipped");
    expect(result.text).toBe("");
    expect(fetchCalled).toBe(false);
  });

  test("CF-markdown path: content-type text/markdown", async () => {
    const fakeFetcher = async (): Promise<Response> => {
      return new Response("# Heading\n\nSome markdown content.", {
        status: 200,
        headers: { "content-type": "text/markdown" },
      });
    };

    const result = await fetchFullText("https://example.com/article", {
      fetcher: fakeFetcher as typeof fetch,
      maxChars: 100,
    });
    expect(result.method).toBe("cf-markdown");
    expect(result.text).toContain("markdown content");
    expect(result.tokens).toBeGreaterThan(0);
  });

  test("HTML extract path: extracts text from article tag", async () => {
    const fakeFetcher = async (): Promise<Response> => {
      return new Response(
        "<html><body><nav>Nav</nav><article>Main article content here.</article><footer>Footer</footer></body></html>",
        { status: 200, headers: { "content-type": "text/html" } },
      );
    };

    const result = await fetchFullText("https://example.com/article", {
      fetcher: fakeFetcher as typeof fetch,
    });
    expect(result.method).toBe("html-extract");
    expect(result.text).toContain("Main article content");
    expect(result.text).not.toContain("<article>");
  });

  test("timeout/exception returns skipped with error", async () => {
    const fakeFetcher = async (): Promise<Response> => {
      throw new Error("Network error");
    };

    const result = await fetchFullText("https://example.com/article", {
      fetcher: fakeFetcher as typeof fetch,
    });
    expect(result.method).toBe("skipped");
    expect(result.error).toContain("Network error");
  });

  test("non-200 response returns skipped", async () => {
    const fakeFetcher = async (): Promise<Response> => {
      return new Response("Not Found", { status: 404 });
    };

    const result = await fetchFullText("https://example.com/article", {
      fetcher: fakeFetcher as typeof fetch,
    });
    expect(result.method).toBe("skipped");
    expect(result.error).toContain("404");
  });
});

describe("enrichArticles", () => {
  test("enriches articles with correct concurrency", async () => {
    let maxConcurrent = 0;
    let currentConcurrent = 0;
    let callCount = 0;

    const fakeFetcher = async (): Promise<Response> => {
      callCount++;
      currentConcurrent++;
      maxConcurrent = Math.max(maxConcurrent, currentConcurrent);
      await new Promise<void>((resolve) => setTimeout(resolve, 10));
      currentConcurrent--;
      return new Response("<article>Content</article>", {
        status: 200,
        headers: { "content-type": "text/html" },
      });
    };

    const articles = Array.from({ length: 10 }, (_, i) => makeArticle(`https://example.com/${i}`));
    const enriched = await enrichArticles(articles, { fetcher: fakeFetcher as typeof fetch, concurrency: 3 });

    expect(enriched).toHaveLength(10);
    expect(callCount).toBe(10);
    expect(maxConcurrent).toBeLessThanOrEqual(3);
    for (const a of enriched) {
      expect(a.fullText).toBeTruthy();
    }
  });
});
