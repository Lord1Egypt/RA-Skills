// SerpAPI - Multi-engine SERP API (Google, Bing, DuckDuckGo, Baidu, Yandex)
// API docs: https://serpapi.com/search-api

const API_URL = "https://serpapi.com/search.json";

export function isAvailable() {
  return !!(process.env.SERPAPI_API_KEY ?? "").trim();
}

export function name() {
  return "serpapi";
}

const ENGINE_MAP = {
  google: "google",
  bing: "bing",
  duckduckgo: "duckduckgo",
  baidu: "baidu",
  yandex: "yandex",
};

export async function search(query, opts = {}) {
  const apiKey = (process.env.SERPAPI_API_KEY ?? "").trim();
  if (!apiKey) throw new Error("Missing SERPAPI_API_KEY");

  const engine = ENGINE_MAP[opts.searchEngine ?? "google"] ?? "google";

  // Build query with site: filter
  let q = query;
  if (opts.includeDomains?.length === 1) {
    q = `site:${opts.includeDomains[0]} ${query}`;
  } else if (opts.includeDomains?.length > 1) {
    const sites = opts.includeDomains.map((d) => `site:${d}`).join(" OR ");
    q = `(${sites}) ${query}`;
  }
  if (opts.excludeDomains?.length) {
    q += " " + opts.excludeDomains.map((d) => `-site:${d}`).join(" ");
  }

  const params = new URLSearchParams({
    api_key: apiKey,
    engine,
    q,
    num: String(normalizeCount(opts.count, 100)),
  });

  // Date range (Google tbs)
  if (engine === "google") {
    if (opts.timeRange) {
      const tbsMap = { day: "qdr:d", week: "qdr:w", month: "qdr:m", year: "qdr:y" };
      if (tbsMap[opts.timeRange]) params.set("tbs", tbsMap[opts.timeRange]);
    }
    if (opts.fromDate || opts.toDate) {
      const min = opts.fromDate ? fmtGoogleDate(opts.fromDate) : "1/1/1970";
      const max = opts.toDate ? fmtGoogleDate(opts.toDate) : "";
      params.set("tbs", `cdr:1,cd_min:${min},cd_max:${max}`);
    }
    if (opts.news) params.set("tbm", "nws");
  }

  if (opts.country) params.set("gl", opts.country.toLowerCase());
  if (opts.lang) params.set("hl", opts.lang);

  const resp = await fetch(`${API_URL}?${params.toString()}`);

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`SerpAPI search failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  const items = opts.news
    ? (data.news_results ?? data.organic_results ?? [])
    : (data.organic_results ?? data.news_results ?? []);

  return {
    engine: `serpapi:${engine}`,
    answer: data.answer_box?.answer ?? data.answer_box?.snippet ?? data.knowledge_graph?.description ?? null,
    results: items.map((r) => ({
      title: r.title ?? "",
      url: r.link ?? "",
      content: r.snippet ?? r.description ?? "",
      score: null,
      date: r.date ?? null,
    })),
  };
}

function normalizeCount(value, max) {
  const n = Number.parseInt(String(value ?? 5), 10);
  if (!Number.isFinite(n)) return 5;
  return Math.max(1, Math.min(n, max));
}

function fmtGoogleDate(dateStr) {
  // YYYY-MM-DD -> M/D/YYYY
  const [y, m, d] = dateStr.split("-");
  return `${parseInt(m, 10)}/${parseInt(d, 10)}/${y}`;
}

export async function extract(_urls) {
  throw new Error("SerpAPI does not support content extraction. Use Tavily or Exa instead.");
}
