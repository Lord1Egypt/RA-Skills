import { requestText } from "../lib/http-client.mjs";

const API_URL = "https://api.search.brave.com/res/v1/web/search";

function normalizeCount(value, max = 20) {
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
  if (opts.fromDate) {
    return `${opts.fromDate}to${new Date().toISOString().slice(0, 10)}`;
  }
  if (opts.toDate) {
    return `1970-01-01to${opts.toDate}`;
  }
  if (opts.timeRange) {
    return (
      {
        day: "pd",
        week: "pw",
        month: "pm",
        year: "py",
      }[opts.timeRange] ?? null
    );
  }
  return null;
}

function normalizeResult(item) {
  const extraSnippets = Array.isArray(item.extra_snippets) ? item.extra_snippets : [];
  const snippets = [item.description ?? "", ...extraSnippets].filter(Boolean);
  return {
    title: item.title ?? "",
    url: item.url ?? "",
    content: snippets.join(" ").trim(),
    score: null,
    publishedDate: item.age ?? null,
    date: item.age ?? null,
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
  return !!(process.env.BRAVE_API_KEY ?? "").trim();
}

export function name() {
  return "brave";
}

export async function search(query, opts = {}) {
  const apiKey = (process.env.BRAVE_API_KEY ?? "").trim();
  if (!apiKey) {
    throw new Error("Missing BRAVE_API_KEY");
  }

  const url = new URL(API_URL);
  url.searchParams.set("q", buildQuery(query, opts));
  url.searchParams.set("count", String(normalizeCount(opts.count, 20)));
  url.searchParams.set("extra_snippets", "true");
  if (opts.country) {
    url.searchParams.set("country", String(opts.country).toUpperCase());
  }
  if (opts.lang) {
    url.searchParams.set("search_lang", String(opts.lang).toLowerCase());
  }
  const freshness = buildFreshness(opts);
  if (freshness) {
    url.searchParams.set("freshness", freshness);
  }

  const response = await requestText(url.toString(), {
    method: "GET",
    headers: {
      accept: "application/json",
      "x-subscription-token": apiKey,
    },
    timeoutMs: 20_000,
  });

  if (response.status !== 200) {
    throw new Error(`Brave search failed (${response.status}): ${response.body}`);
  }

  const data = JSON.parse(response.body);
  const results = (data.web?.results ?? [])
    .slice(0, normalizeCount(opts.count, 20))
    .map(normalizeResult);

  return {
    engine: "brave",
    answer: buildAnswer(results) || null,
    results,
  };
}

export async function extract(_urls) {
  throw new Error("Brave does not support content extraction. Use Tavily, Exa, or fetch instead.");
}
