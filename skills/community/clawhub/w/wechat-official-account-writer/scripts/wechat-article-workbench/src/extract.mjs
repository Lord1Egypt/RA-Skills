import * as cheerio from "cheerio";
import { Readability } from "@mozilla/readability";
import { JSDOM } from "jsdom";
import { fetchText, normalizeWhitespace } from "./http.mjs";

const X_HOSTS = new Set(["x.com", "twitter.com", "www.x.com", "www.twitter.com"]);

function hostnameOf(url) {
  try {
    return new URL(url).hostname.toLowerCase();
  } catch {
    return "";
  }
}

function fallbackFromHtml(html) {
  const $ = cheerio.load(html);
  $("script, style, noscript, svg").remove();
  const metaDescription =
    $("meta[name='description']").attr("content") ||
    $("meta[property='og:description']").attr("content") ||
    "";
  const title = $("meta[property='og:title']").attr("content") || $("title").text();
  const text = normalizeWhitespace($("article").text() || $("main").text() || $("body").text());
  return {
    title: normalizeWhitespace(title),
    excerpt: normalizeWhitespace(metaDescription),
    textContent: text
  };
}

export async function extractArticle(item, options = {}) {
  const maxChars = options.maxChars || 12000;
  const host = hostnameOf(item.url);

  if (X_HOSTS.has(host)) {
    const text = normalizeWhitespace([item.title, item.body, item.summary, item.quoted].filter(Boolean).join("\n\n"));
    return {
      extractionStatus: "used-curated-x-summary",
      extractedTitle: item.title,
      extractedExcerpt: item.reason || item.summary || "",
      extractedText: text.slice(0, maxChars)
    };
  }

  try {
    const html = await fetchText(item.url);
    const dom = new JSDOM(html, { url: item.url });
    const article = new Readability(dom.window.document).parse();
    const fallback = fallbackFromHtml(html);
    const text = normalizeWhitespace(article?.textContent || fallback.textContent);

    return {
      extractionStatus: text ? "readability" : "empty",
      extractedTitle: normalizeWhitespace(article?.title || fallback.title || item.title),
      extractedExcerpt: normalizeWhitespace(article?.excerpt || fallback.excerpt || item.summary || item.reason),
      extractedText: text.slice(0, maxChars)
    };
  } catch (error) {
    const text = normalizeWhitespace([item.summary, item.body, item.reason].filter(Boolean).join("\n\n"));
    return {
      extractionStatus: "fallback-curated-summary",
      extractionError: error.message,
      extractedTitle: item.title,
      extractedExcerpt: item.summary || item.reason || "",
      extractedText: text.slice(0, maxChars)
    };
  }
}
