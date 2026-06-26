import { collapseWhitespace, decodeHtmlEntities, stripHtmlTags } from "./html-text.mjs";

const TITLE_PATTERN = new RegExp(
  [
    '<h2 class="result__title">[\\s\\S]*?',
    '<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([\\s\\S]*?)<\\/a>',
    "[\\s\\S]*?<\\/h2>",
  ].join(""),
  "gi",
);

function extractSnippet(block) {
  const snippetMatch =
    block.match(/<a[^>]*class="result__snippet"[^>]*>([\s\S]*?)<\/a>/i) ??
    block.match(/<div[^>]*class="result__snippet"[^>]*>([\s\S]*?)<\/div>/i);
  return collapseWhitespace(stripHtmlTags(snippetMatch?.[1] ?? ""));
}

function normalizeResultUrl(rawUrl) {
  const decoded = decodeHtmlEntities(rawUrl);

  try {
    const url = new URL(decoded);
    if (url.hostname === "duckduckgo.com" && url.pathname === "/y.js") {
      return null;
    }
    if (url.hostname === "duckduckgo.com" && url.searchParams.has("uddg")) {
      return decodeURIComponent(url.searchParams.get("uddg"));
    }
  } catch {
    return decoded;
  }

  return decoded;
}

export function parseDuckDuckGoHtml(html, maxResults = 5) {
  const results = [];
  const matches = Array.from(html.matchAll(TITLE_PATTERN));

  for (let index = 0; index < matches.length && results.length < maxResults; index++) {
    const match = matches[index];
    const [, rawUrl, titleHtml] = match;
    const blockStart = match.index ?? 0;
    const blockEnd = matches[index + 1]?.index ?? html.length;
    const block = html.slice(blockStart, blockEnd);
    const title = collapseWhitespace(stripHtmlTags(titleHtml));
    const content = extractSnippet(block);
    const url = normalizeResultUrl(rawUrl);

    if (!title || !url) {
      continue;
    }

    results.push({
      title,
      url,
      content,
      score: null,
    });
  }

  return results;
}
