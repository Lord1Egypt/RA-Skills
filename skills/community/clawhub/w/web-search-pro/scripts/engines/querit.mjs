import { requestText } from "../lib/http-client.mjs";
import { assertSafeRemoteUrl } from "../lib/url-safety.mjs";

const DEFAULT_BASE_URL = "https://api.querit.ai";
const DEFAULT_BASE_PATH = "/v1/search";

function normalizeCount(value, max = 20) {
  const n = Number.parseInt(String(value ?? 5), 10);
  if (!Number.isFinite(n)) return 5;
  return Math.max(1, Math.min(n, max));
}

function normalizeBaseUrl() {
  return String(process.env.QUERIT_BASE_URL ?? DEFAULT_BASE_URL).trim() || DEFAULT_BASE_URL;
}

function normalizeBasePath() {
  const raw = String(process.env.QUERIT_BASE_PATH ?? DEFAULT_BASE_PATH).trim() || DEFAULT_BASE_PATH;
  return raw.startsWith("/") ? raw : `/${raw}`;
}

function mapTimeRange(timeRange) {
  if (!timeRange) {
    return null;
  }
  return (
    {
      day: "d1",
      week: "w1",
      month: "m1",
      year: "y1",
    }[timeRange] ?? null
  );
}

function buildFilters(opts = {}) {
  const filters = {};

  if (opts.lang) {
    filters.languages = { include: [String(opts.lang).toLowerCase()] };
  }
  if (opts.country) {
    filters.geo = { countries: { include: [String(opts.country).toUpperCase()] } };
  }
  if (opts.includeDomains?.length || opts.excludeDomains?.length) {
    filters.sites = {};
    if (opts.includeDomains?.length) {
      filters.sites.include = [...opts.includeDomains];
    }
    if (opts.excludeDomains?.length) {
      filters.sites.exclude = [...opts.excludeDomains];
    }
  }

  const timeRange = mapTimeRange(opts.timeRange);
  if (timeRange) {
    filters.timeRange = { date: timeRange };
  }

  return Object.keys(filters).length > 0 ? filters : null;
}

function normalizeResult(item) {
  return {
    title: item.title ?? "",
    url: item.url ?? "",
    content: item.snippet ?? item.page_age ?? "",
    score: item.score ?? null,
    publishedDate: item.page_age ?? null,
    date: item.page_age ?? null,
  };
}

export function isAvailable() {
  return !!(process.env.QUERIT_API_KEY ?? "").trim();
}

export function name() {
  return "querit";
}

export async function search(query, opts = {}) {
  const apiKey = (process.env.QUERIT_API_KEY ?? "").trim();
  if (!apiKey) {
    throw new Error("Missing QUERIT_API_KEY");
  }

  const baseUrl = normalizeBaseUrl();
  const basePath = normalizeBasePath();
  await assertSafeRemoteUrl(baseUrl);
  const endpoint = new URL(basePath, `${baseUrl.replace(/\/$/, "")}/`);
  const filters = buildFilters(opts);
  const body = {
    query,
    count: normalizeCount(opts.count, 20),
    ...(filters ? { filters } : {}),
  };

  const response = await requestText(endpoint.toString(), {
    method: "POST",
    headers: {
      accept: "application/json",
      authorization: `Bearer ${apiKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
    timeoutMs: 20_000,
  });

  if (response.status !== 200) {
    throw new Error(`Querit search failed (${response.status}): ${response.body}`);
  }

  const data = JSON.parse(response.body);
  if (data.error_msg || ![undefined, null, 0, 200].includes(data.error_code)) {
    throw new Error(data.error_msg || `Querit search failed with error_code=${data.error_code}`);
  }

  const results = (((data.results ?? {}).result ?? []) || [])
    .slice(0, normalizeCount(opts.count, 20))
    .map(normalizeResult);

  return {
    engine: "querit",
    answer: results[0]?.content ?? null,
    results,
  };
}

export async function extract(_urls) {
  throw new Error("Querit does not support content extraction. Use Tavily, Exa, or fetch instead.");
}
