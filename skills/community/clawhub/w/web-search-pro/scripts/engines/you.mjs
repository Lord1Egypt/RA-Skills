const API_URL = "https://ydc-index.io/v1/search";

function normalizeCount(value, max = 100) {
  const n = Number.parseInt(String(value ?? 5), 10);
  if (!Number.isFinite(n)) return 5;
  return Math.max(1, Math.min(n, max));
}

function buildQuery(query, opts = {}) {
  let q = query;
  if (opts.includeDomains?.length === 1) {
    q = `site:${opts.includeDomains[0]} ${query}`;
  } else if (opts.includeDomains?.length > 1) {
    const sites = opts.includeDomains.map((domain) => `site:${domain}`).join(" OR ");
    q = `(${sites}) ${query}`;
  }
  if (opts.excludeDomains?.length) {
    q += ` ${opts.excludeDomains.map((domain) => `-site:${domain}`).join(" ")}`;
  }
  return q.trim();
}

function buildFreshness(opts = {}) {
  if (opts.fromDate && opts.toDate) {
    return `${opts.fromDate}to${opts.toDate}`;
  }
  if (opts.timeRange) {
    return opts.timeRange;
  }
  return null;
}

function normalizeWebResult(item) {
  const snippets = Array.isArray(item.snippets) ? item.snippets : [];
  return {
    title: item.title ?? "",
    url: item.url ?? "",
    content: snippets[0] ?? item.description ?? "",
    score: null,
    publishedDate: item.page_age ?? null,
  };
}

function normalizeNewsResult(item) {
  return {
    title: item.title ?? "",
    url: item.url ?? "",
    content: item.description ?? "",
    score: null,
    publishedDate: item.page_age ?? null,
  };
}

function buildAnswer(results = []) {
  return results
    .map((item) => item.content ?? "")
    .filter(Boolean)
    .slice(0, 3)
    .join(" ")
    .slice(0, 1000);
}

export function isAvailable() {
  return !!(process.env.YOU_API_KEY ?? "").trim();
}

export function name() {
  return "you";
}

export async function search(query, opts = {}) {
  const apiKey = (process.env.YOU_API_KEY ?? "").trim();
  if (!apiKey) {
    throw new Error("Missing YOU_API_KEY");
  }

  const url = new URL(API_URL);
  url.searchParams.set("query", buildQuery(query, opts));
  url.searchParams.set("count", String(normalizeCount(opts.count, 100)));
  url.searchParams.set("safesearch", "moderate");
  if (opts.country) url.searchParams.set("country", String(opts.country).toUpperCase());
  if (opts.lang) url.searchParams.set("language", String(opts.lang));
  const freshness = buildFreshness(opts);
  if (freshness) {
    url.searchParams.set("freshness", freshness);
  }

  const resp = await fetch(url, {
    method: "GET",
    headers: {
      Accept: "application/json",
      "X-API-Key": apiKey,
    },
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`You.com search failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  const resultGroups = data.results ?? {};
  const webResults = Array.isArray(resultGroups.web) ? resultGroups.web : [];
  const newsResults = Array.isArray(resultGroups.news) ? resultGroups.news : [];
  const items = opts.news
    ? [...newsResults.map(normalizeNewsResult), ...webResults.map(normalizeWebResult)]
    : webResults.length > 0
      ? webResults.map(normalizeWebResult)
      : newsResults.map(normalizeNewsResult);
  const results = items.slice(0, normalizeCount(opts.count, 100));

  return {
    engine: "you",
    answer: buildAnswer(results) || null,
    results,
  };
}

export async function extract(_urls) {
  throw new Error("You.com does not support content extraction. Use Tavily, Exa, or fetch instead.");
}
