// Serper - Google SERP API with full Google search parameters
// API docs: https://serper.dev

const SEARCH_URL = "https://google.serper.dev/search";
const NEWS_URL = "https://google.serper.dev/news";

export function isAvailable() {
  return !!(process.env.SERPER_API_KEY ?? "").trim();
}

export function name() {
  return "serper";
}

export async function search(query, opts = {}) {
  const apiKey = (process.env.SERPER_API_KEY ?? "").trim();
  if (!apiKey) throw new Error("Missing SERPER_API_KEY");

  // Build query with site: filter if needed
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

  const body = {
    q,
    num: normalizeCount(opts.count, 100),
  };

  // Date range via tbs parameter
  if (opts.timeRange) {
    const tbsMap = { day: "qdr:d", week: "qdr:w", month: "qdr:m", year: "qdr:y" };
    if (tbsMap[opts.timeRange]) body.tbs = tbsMap[opts.timeRange];
  }
  if (opts.fromDate || opts.toDate) {
    const min = opts.fromDate ? fmtSerperDate(opts.fromDate) : "1/1/1970";
    const max = opts.toDate ? fmtSerperDate(opts.toDate) : "";
    body.tbs = `cdr:1,cd_min:${min},cd_max:${max}`;
  }

  if (opts.country) body.gl = opts.country.toLowerCase();
  if (opts.lang) body.hl = opts.lang;

  const url = opts.news ? NEWS_URL : SEARCH_URL;

  const resp = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-KEY": apiKey,
    },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Serper search failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  const items = opts.news ? data.news ?? [] : data.organic ?? [];

  return {
    engine: "serper",
    answer: data.answerBox?.answer ?? data.answerBox?.snippet ?? data.knowledgeGraph?.description ?? null,
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

function fmtSerperDate(dateStr) {
  // YYYY-MM-DD -> M/D/YYYY
  const [y, m, d] = dateStr.split("-");
  return `${parseInt(m)}/${parseInt(d)}/${y}`;
}

export async function extract(_urls) {
  throw new Error("Serper does not support content extraction. Use Tavily or Exa instead.");
}
