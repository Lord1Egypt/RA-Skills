#!/usr/bin/env node
/**
 * Browser search for sites that Tavily/Brave can't reach.
 * Uses Xvfb + Chromium + Puppeteer (三件套).
 * 
 * Outputs JSON array of results to stdout.
 */

const puppeteer = require("puppeteer");

async function searchXiaohongshu(page, query) {
  const results = [];
  try {
    await page.goto(`https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(query)}`, {
      waitUntil: "networkidle2",
      timeout: 30000,
    });
    await new Promise((r) => setTimeout(r, 3000));

    const items = await page.evaluate(() => {
      const cards = document.querySelectorAll('[class*="note-item"], [class*="search-result"]');
      return Array.from(cards)
        .slice(0, 5)
        .map((card) => {
          const title = card.querySelector('[class*="title"], h2, h3');
          const desc = card.querySelector('[class*="desc"], p');
          const link = card.querySelector("a");
          return {
            title: title ? title.innerText.trim() : "",
            content: desc ? desc.innerText.trim() : "",
            url: link ? link.href : "",
          };
        })
        .filter((item) => item.title);
    });

    for (const item of items) {
      results.push({ ...item, source: "xiaohongshu" });
    }
  } catch (e) {
    console.error(`Xiaohongshu search failed: ${e.message}`);
  }
  return results;
}

async function searchTwitter(page, query) {
  const results = [];
  try {
    await page.goto(`https://x.com/search?q=${encodeURIComponent(query)}&f=top`, {
      waitUntil: "networkidle2",
      timeout: 30000,
    });
    await new Promise((r) => setTimeout(r, 5000));

    const tweets = await page.evaluate(() => {
      const articles = document.querySelectorAll("article");
      return Array.from(articles)
        .slice(0, 5)
        .map((article) => {
          const text = article.querySelector('[data-testid="tweetText"]');
          const user = article.querySelector('[data-testid="User-Name"]');
          return {
            title: user ? user.innerText.split("\n")[0] : "Tweet",
            content: text ? text.innerText.trim() : "",
            url: "",
          };
        })
        .filter((item) => item.content);
    });

    for (const item of tweets) {
      results.push({ ...item, source: "x_twitter" });
    }
  } catch (e) {
    console.error(`X/Twitter search failed: ${e.message}`);
  }
  return results;
}

async function main() {
  const args = process.argv.slice(2);
  const queryIdx = args.indexOf("--query");
  const query = queryIdx >= 0 ? args[queryIdx + 1] : "";

  if (!query) {
    console.error("Usage: node browser_search.js --query <query>");
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
  });

  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  );

  const allResults = [];

  // Search Xiaohongshu
  const xhsResults = await searchXiaohongshu(page, query);
  allResults.push(...xhsResults);

  // Search X/Twitter
  const twitterResults = await searchTwitter(page, query);
  allResults.push(...twitterResults);

  await browser.close();

  // Output JSON to stdout
  console.log(JSON.stringify(allResults, null, 2));
}

main().catch((e) => {
  console.error(`Browser search error: ${e.message}`);
  process.exit(1);
});
