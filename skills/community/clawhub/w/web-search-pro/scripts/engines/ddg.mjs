import { parseDuckDuckGoHtml } from "../lib/ddg-parser.mjs";
import { requestText } from "../lib/http-client.mjs";

const SEARCH_URL = "https://html.duckduckgo.com/html/";
const BROWSER_HEADERS = {
  "user-agent":
    [
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
      "AppleWebKit/537.36 (KHTML, like Gecko)",
      "Chrome/122.0.0.0 Safari/537.36",
    ].join(" "),
  accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "accept-language": "en-US,en;q=0.9",
};

function buildQuery(query, opts = {}) {
  let searchQuery = query;

  if (opts.includeDomains?.length === 1) {
    searchQuery = `site:${opts.includeDomains[0]} ${searchQuery}`;
  } else if (opts.includeDomains?.length > 1) {
    const sites = opts.includeDomains.map((domain) => `site:${domain}`).join(" OR ");
    searchQuery = `(${sites}) ${searchQuery}`;
  }

  if (opts.excludeDomains?.length) {
    searchQuery += ` ${opts.excludeDomains.map((domain) => `-site:${domain}`).join(" ")}`;
  }

  return searchQuery.trim();
}

export function isAvailable() {
  return true;
}

export function name() {
  return "ddg";
}

export async function search(query, opts = {}) {
  const searchQuery = buildQuery(query, opts);

  let response;
  try {
    response = await requestText(SEARCH_URL, {
      method: "POST",
      headers: {
        ...BROWSER_HEADERS,
        "content-type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ q: searchQuery }).toString(),
      transport: "curl",
    });
  } catch {
    const searchUrl = new URL(SEARCH_URL);
    searchUrl.searchParams.set("q", searchQuery);
    response = await requestText(searchUrl.toString(), {
      method: "GET",
      headers: BROWSER_HEADERS,
      transport: "fetch",
    });
  }

  if (response.status !== 200) {
    throw new Error(`DuckDuckGo search failed (${response.status})`);
  }

  return {
    engine: "ddg",
    answer: null,
    results: parseDuckDuckGoHtml(
      response.body,
      Math.max(1, Math.min(opts.count ?? 5, 20)),
    ),
  };
}

export async function extract(_urls) {
  throw new Error("DuckDuckGo search does not support extraction. Use fetch, Tavily, or Exa.");
}
