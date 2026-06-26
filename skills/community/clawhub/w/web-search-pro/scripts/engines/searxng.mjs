import { requestText } from "../lib/http-client.mjs";
import { assertSafeRemoteUrl } from "../lib/url-safety.mjs";

function normalizeCount(value, max = 20) {
  const n = Number.parseInt(String(value ?? 5), 10);
  if (!Number.isFinite(n)) return 5;
  return Math.max(1, Math.min(n, max));
}

function parseCsvEnv(name) {
  return String(process.env[name] ?? "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
}

function normalizeSafeSearch(value) {
  const parsed = Number.parseInt(String(value ?? 1), 10);
  if (!Number.isInteger(parsed)) {
    return 1;
  }
  return Math.max(0, Math.min(parsed, 2));
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

function buildSearchUrl(instanceUrl, opts, query) {
  const base = instanceUrl.replace(/\/$/, "");
  const url = new URL(`${base}/search`);
  url.searchParams.set("q", buildQuery(query, opts));
  url.searchParams.set("format", "json");
  url.searchParams.set("safesearch", String(normalizeSafeSearch(process.env.SEARXNG_SAFESEARCH)));
  if (opts.news) {
    url.searchParams.set("categories", "news");
  }
  if (opts.timeRange) {
    url.searchParams.set("time_range", opts.timeRange);
  }
  const configuredLanguage = String(process.env.SEARXNG_LANGUAGE ?? "").trim();
  if (configuredLanguage) {
    url.searchParams.set("language", configuredLanguage);
  }
  const engines = parseCsvEnv("SEARXNG_ENGINES");
  if (engines.length > 0) {
    url.searchParams.set("engines", engines.join(","));
  }
  return url;
}

function normalizeResult(item) {
  return {
    title: item.title ?? "",
    url: item.url ?? "",
    content: item.content ?? "",
    score: item.score ?? null,
    publishedDate: item.publishedDate ?? null,
    date: item.publishedDate ?? null,
  };
}

function buildAnswer(data, results) {
  if (Array.isArray(data.answers) && data.answers.length > 0) {
    return typeof data.answers[0] === "string" ? data.answers[0] : String(data.answers[0]);
  }
  if (Array.isArray(data.infoboxes) && data.infoboxes.length > 0) {
    const infobox = data.infoboxes[0];
    return infobox.content ?? infobox.infobox ?? "";
  }
  return results[0]?.content ?? null;
}

export function isAvailable() {
  return !!(process.env.SEARXNG_INSTANCE_URL ?? "").trim();
}

export function name() {
  return "searxng";
}

export async function search(query, opts = {}) {
  const instanceUrl = String(process.env.SEARXNG_INSTANCE_URL ?? "").trim();
  if (!instanceUrl) {
    throw new Error("Missing SEARXNG_INSTANCE_URL");
  }

  await assertSafeRemoteUrl(instanceUrl);
  const url = buildSearchUrl(instanceUrl, opts, query);
  const response = await requestText(url.toString(), {
    method: "GET",
    headers: {
      accept: "application/json",
      "user-agent": "web-search-pro/1.1",
    },
    timeoutMs: 20_000,
  });

  if (response.status !== 200) {
    throw new Error(`SearXNG search failed (${response.status}): ${response.body}`);
  }

  const data = JSON.parse(response.body);
  const results = (data.results ?? []).slice(0, normalizeCount(opts.count, 20)).map(normalizeResult);

  return {
    engine: "searxng",
    answer: buildAnswer(data, results),
    results,
  };
}

export async function extract(_urls) {
  throw new Error("SearXNG does not support content extraction. Use Tavily, Exa, or fetch instead.");
}
