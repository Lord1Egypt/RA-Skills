import { ApifyClient } from "apify-client";
import type { ScrapeResult } from "./types.js";

export async function scrapeWebsite(
  url: string,
  apifyToken: string,
  maxPages = 3
): Promise<ScrapeResult> {
  const client = new ApifyClient({ token: apifyToken });

  const run = await client.actor("apify/website-content-crawler").call({
    startUrls: [{ url }],
    maxCrawlPages: maxPages,
    crawlerType: "cheerio",
    maxConcurrency: 5,
    maxRequestRetries: 2,
  });

  const { items } = await client.dataset(run.defaultDatasetId).listItems();

  const pages = items.map((item: Record<string, unknown>) => {
    const pageUrl = String(item.url || "");
    const text = String(item.text || "");
    return `--- PAGE: ${pageUrl} ---\n${text}`;
  });

  return {
    url,
    pages_crawled: items.length,
    content: pages.join("\n\n"),
  };
}
