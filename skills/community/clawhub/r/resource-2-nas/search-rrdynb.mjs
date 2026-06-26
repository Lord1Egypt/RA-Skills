#!/usr/bin/env node

import path from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_API_BASE = "https://so.252035.xyz/api";
const DEFAULT_MAX_CANDIDATES = 50;
const DEFAULT_RESULT_TYPE = "all";
const DEFAULT_SOURCE_TYPE = "all";
const DEFAULT_TIMEOUT_MS = 60_000;
const DEFAULT_CLOUD_TYPES = ["baidu", "quark"];

const PROVIDER_LABELS = {
  baidu: "百度网盘",
  aliyun: "阿里云盘",
  quark: "夸克网盘",
  guangya: "光鸭云盘",
  tianyi: "天翼云盘",
  uc: "UC网盘",
  mobile: "移动云盘",
  "115": "115网盘",
  pikpak: "PikPak",
  xunlei: "迅雷网盘",
  "123": "123网盘",
  magnet: "磁力链接",
  ed2k: "电驴链接",
  others: "其他"
};

const CHECKABLE_TYPES = new Set(["baidu", "aliyun", "quark", "tianyi", "uc", "mobile", "115", "xunlei", "123"]);

if (isCliEntryPoint()) {
  main().catch((error) => {
    const message = error && error.message ? error.message : String(error);
    console.error(JSON.stringify({ ok: false, error: message }, null, 2));
    process.exit(1);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.title) {
    printUsage();
    process.exit(2);
  }

  const searchResult = await searchPanSou(args);
  if (args.checkLinks) {
    searchResult.linkChecks = await checkSearchResultLinks(args, searchResult.downloadLinks);
  }

  console.log(formatSearchResult(searchResult, args.format));
}

function parseArgs(argv) {
  const parsed = {
    title: "",
    apiBase: DEFAULT_API_BASE,
    maxCandidates: DEFAULT_MAX_CANDIDATES,
    resultType: DEFAULT_RESULT_TYPE,
    sourceType: DEFAULT_SOURCE_TYPE,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    channels: [],
    plugins: [],
    cloudTypes: [...DEFAULT_CLOUD_TYPES],
    include: [],
    exclude: [],
    ext: null,
    filter: null,
    concurrency: null,
    refresh: false,
    checkLinks: false,
    viewToken: "",
    proxyUrl: "",
    format: "markdown"
  };
  const positionals = [];

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--api-base") {
      parsed.apiBase = argv[++index] || DEFAULT_API_BASE;
    } else if (arg === "--max-candidates") {
      parsed.maxCandidates = Number(argv[++index] || DEFAULT_MAX_CANDIDATES);
    } else if (arg === "--res") {
      parsed.resultType = argv[++index] || DEFAULT_RESULT_TYPE;
    } else if (arg === "--src") {
      parsed.sourceType = argv[++index] || DEFAULT_SOURCE_TYPE;
    } else if (arg === "--channels") {
      parsed.channels = parseList(argv[++index]);
    } else if (arg === "--plugins") {
      parsed.plugins = parseList(argv[++index]);
    } else if (arg === "--cloud-types") {
      parsed.cloudTypes = parseList(argv[++index]);
    } else if (arg === "--include") {
      parsed.include = parseList(argv[++index]);
    } else if (arg === "--exclude") {
      parsed.exclude = parseList(argv[++index]);
    } else if (arg === "--ext-json") {
      parsed.ext = parseJson(argv[++index], "--ext-json");
    } else if (arg === "--filter-json") {
      parsed.filter = parseJson(argv[++index], "--filter-json");
    } else if (arg === "--conc") {
      parsed.concurrency = Number(argv[++index] || 0);
    } else if (arg === "--timeout-ms") {
      parsed.timeoutMs = Number(argv[++index] || DEFAULT_TIMEOUT_MS);
    } else if (arg === "--refresh") {
      parsed.refresh = true;
    } else if (arg === "--check-links") {
      parsed.checkLinks = true;
    } else if (arg === "--view-token") {
      parsed.viewToken = argv[++index] || "";
    } else if (arg === "--proxy-url" || arg === "--proxy") {
      parsed.proxyUrl = argv[++index] || "";
    } else if (arg === "--format") {
      parsed.format = argv[++index] || "markdown";
    } else if (arg === "--json") {
      parsed.format = "json";
    } else if (arg === "--markdown") {
      parsed.format = "markdown";
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else {
      positionals.push(arg);
    }
  }

  parsed.title = positionals.join(" ").trim();
  return parsed;
}

function printUsage() {
  console.error("Usage: node scripts/search-rrdynb.mjs <title> [options]");
  console.error("Options:");
  console.error("  --api-base https://so.252035.xyz/api");
  console.error("  --max-candidates 50");
  console.error("  --res all|merge|results");
  console.error("  --src all|tg|plugin");
  console.error("  --channels tgsearchers4,Aliyun_4K_Movies");
  console.error("  --plugins wanou,zhizhen");
  console.error("  --cloud-types baidu,quark");
  console.error("  --include 4K,合集 --exclude 预告");
  console.error("  --refresh");
  console.error("  --check-links [--proxy-url socks5://127.0.0.1:1080]");
  console.error("  --format markdown|json");
}

function formatSearchResult(searchResult, format = "markdown") {
  if (format === "json") return JSON.stringify(searchResult, null, 2);
  if (format === "markdown") return renderMarkdownTable(searchResult);
  throw new Error(`Unsupported format: ${format}`);
}

async function searchPanSou(args) {
  const apiBase = normalizeApiBase(args.apiBase);
  const params = buildSearchQueryParams(args);
  const searchUrl = `${apiBase}/search?${params.toString()}`;
  const response = await fetchJson(searchUrl, { timeoutMs: args.timeoutMs });
  const normalized = normalizePanSouSearchResponse(response, {
    title: args.title,
    selectedQuery: args.title,
    maxCandidates: args.maxCandidates,
    cloudTypes: args.cloudTypes
  });

  return {
    ...normalized,
    apiBase,
    selectedQuery: args.title,
    searchAttempts: [
      {
        query: args.title,
        searchUrl,
        availableTotal: normalized.availableTotal,
        returnedCount: normalized.returnedCount,
        candidateCount: normalized.candidates.length
      }
    ],
    output: {
      directResourceLinks: "included_when_detected",
      extractionCodes: "included_when_detected",
      linkChecks: args.checkLinks ? "included_when_requested" : "not_requested"
    }
  };
}

function buildSearchQueryParams(args) {
  const params = new URLSearchParams();
  params.set("kw", args.title);
  if (args.channels && args.channels.length > 0) params.set("channels", args.channels.join(","));
  if (args.plugins && args.plugins.length > 0) params.set("plugins", args.plugins.join(","));
  if (args.concurrency) params.set("conc", String(args.concurrency));
  if (args.refresh) params.set("refresh", "true");
  if (args.resultType) params.set("res", args.resultType);
  if (args.sourceType) params.set("src", args.sourceType);
  if (args.cloudTypes && args.cloudTypes.length > 0) params.set("cloud_types", args.cloudTypes.join(","));
  if (args.ext) params.set("ext", JSON.stringify(args.ext));

  const filter = args.filter || buildFilter(args.include, args.exclude);
  if (filter) params.set("filter", JSON.stringify(filter));

  return params;
}

function normalizePanSouSearchResponse(response, options = {}) {
  const data = unwrapData(response);
  const rankedLinks = data.results && data.results.length > 0 ? flattenResultsLinks(data.results) : [];
  const mergedByType = data.merged_by_type || groupResultsByType(data.results || []);
  const rawLinks = rankedLinks.length > 0 ? rankedLinks : flattenMergedLinks(mergedByType);
  const cloudTypes = Array.isArray(options.cloudTypes) ? options.cloudTypes : DEFAULT_CLOUD_TYPES;
  const allLinks = filterLinksByCloudTypes(rawLinks, cloudTypes);
  const limit = Number.isFinite(options.maxCandidates) ? options.maxCandidates : DEFAULT_MAX_CANDIDATES;
  const downloadLinks = allLinks.slice(0, limit).map((link, index) => normalizeDownloadLink(link, index + 1));
  const candidates = downloadLinks.map((link) => ({
    rank: link.rank,
    name: link.note || link.label || options.title || "未命名资源",
    provider: link.provider,
    diskType: link.diskType,
    datetime: link.datetime,
    source: link.source,
    matchReason: link.note ? "PanSou 结果说明包含资源标题" : "PanSou 搜索结果",
    resourceProviders: [
      {
        provider: link.provider,
        diskType: link.diskType,
        available: true,
        links: [
          {
            label: link.label,
            url: link.url,
            extractionCode: link.extractionCode,
            extractionCodes: link.extractionCodes
          }
        ],
        extractionCodes: link.extractionCodes,
        note: link.source || "PanSou API"
      }
    ],
    downloadLinks: [stripRank(link)]
  }));

  return {
    ok: true,
    inputTitle: options.title || "",
    selectedQuery: options.selectedQuery || options.title || "",
    availableTotal: Number(data.total || allLinks.length || 0),
    returnedCount: downloadLinks.length,
    total: downloadLinks.length,
    providerCounts: countBy(downloadLinks, "diskType"),
    candidates,
    downloadLinks: downloadLinks.map(stripRank)
  };
}

function normalizeCheckLinksResponse(response) {
  const data = unwrapData(response);
  return {
    ok: true,
    results: (data.results || []).map((item) => ({
      provider: providerLabel(item.disk_type),
      diskType: item.disk_type,
      url: item.url,
      normalizedUrl: item.normalized_url || "",
      state: item.state,
      cacheHit: Boolean(item.cache_hit),
      checkedAt: item.checked_at || null,
      expiresAt: item.expires_at || null,
      summary: item.summary || ""
    }))
  };
}

function renderMarkdownTable(searchResult) {
  const title = searchResult.inputTitle || searchResult.selectedQuery || "搜索结果";
  const availableTotal = Number(searchResult.availableTotal || 0);
  const returnedCount = Number(searchResult.returnedCount || searchResult.candidates?.length || 0);
  const lines = [
    `### ${escapeMarkdownText(title)} 搜索结果`,
    "",
    `按 PanSou 相关度排序，返回前 ${returnedCount} 条。上游可用结果约 ${availableTotal} 条。`,
    "",
    "| # | 资源 | 网盘 | 链接 | 提取码 | 来源 | 时间 |",
    "|---:|---|---|---|---|---|---|"
  ];

  for (const candidate of searchResult.candidates || []) {
    const link = candidate.downloadLinks?.[0] || {};
    lines.push(
      [
        candidate.rank,
        escapeMarkdownCell(candidate.name || link.note || link.label || "未命名资源"),
        escapeMarkdownCell(candidate.provider || link.provider || providerLabel(link.diskType)),
        link.url ? `[打开](${escapeMarkdownUrl(link.url)})` : "-",
        escapeMarkdownCell(link.extractionCode || "-"),
        escapeMarkdownCell(candidate.source || link.source || "-"),
        escapeMarkdownCell(formatDate(candidate.datetime || link.datetime))
      ].join(" | ").replace(/^/, "| ").replace(/$/, " |")
    );
  }

  if (searchResult.linkChecks) {
    lines.push("", renderLinkCheckNote(searchResult.linkChecks));
  }

  return lines.join("\n");
}

function renderLinkCheckNote(linkChecks) {
  if (linkChecks.ok) {
    const checked = linkChecks.results?.length || 0;
    return `链接检测：已检测 ${checked} 条。`;
  }
  return `链接检测：当前不可用（${escapeMarkdownText(linkChecks.error || "检测失败")}）。`;
}

function formatDate(value) {
  if (!value || value === "0001-01-01T00:00:00Z") return "-";
  return String(value).slice(0, 10);
}

function escapeMarkdownCell(value) {
  return escapeMarkdownText(value).replace(/\|/g, "\\|");
}

function escapeMarkdownText(value) {
  return String(value ?? "")
    .replace(/\r?\n+/g, " ")
    .trim();
}

function escapeMarkdownUrl(value) {
  return String(value ?? "").replace(/\)/g, "%29");
}

function filterLinksByCloudTypes(links, cloudTypes = []) {
  if (!cloudTypes || cloudTypes.length === 0) return links;
  const allowed = new Set(cloudTypes);
  return links.filter((link) => allowed.has(link.diskType));
}

async function checkSearchResultLinks(args, downloadLinks) {
  const items = downloadLinks
    .filter((link) => CHECKABLE_TYPES.has(link.diskType))
    .map((link) => ({
      disk_type: link.diskType,
      url: link.url,
      ...(link.extractionCode ? { password: link.extractionCode } : {})
    }));

  if (items.length === 0) {
    return { ok: true, results: [], skipped: "no_checkable_links" };
  }

  const apiBase = normalizeApiBase(args.apiBase);
  const body = {
    items,
    ...(args.viewToken ? { view_token: args.viewToken } : {}),
    ...(args.proxyUrl ? { proxy_url: args.proxyUrl } : {})
  };
  const checkUrl = `${apiBase}/check/links`;
  try {
    const response = await fetchJson(checkUrl, {
      method: "POST",
      timeoutMs: args.timeoutMs,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    return normalizeCheckLinksResponse(response);
  } catch (error) {
    return {
      ok: false,
      error: error && error.message ? error.message : String(error),
      checkUrl,
      checkedItemCount: items.length
    };
  }
}

async function fetchJson(url, options = {}) {
  const retries = Number.isFinite(options.retries) ? options.retries : 2;
  let lastError = null;
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      return await fetchJsonOnce(url, options);
    } catch (error) {
      lastError = error;
      if (attempt === retries) break;
      await delay(500 * (attempt + 1));
    }
  }
  throw lastError;
}

async function fetchJsonOnce(url, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs || DEFAULT_TIMEOUT_MS);
  try {
    const response = await fetch(url, {
      method: options.method || "GET",
      headers: {
        Accept: "application/json",
        ...(options.headers || {})
      },
      body: options.body,
      signal: controller.signal
    });
    const text = await response.text();
    let json;
    try {
      json = text ? JSON.parse(text) : {};
    } catch {
      throw new Error(`Expected JSON from ${url}, got: ${text.slice(0, 200)}`);
    }
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} from ${url}: ${JSON.stringify(json).slice(0, 300)}`);
    }
    if (json && typeof json === "object" && "code" in json && json.code !== 0) {
      throw new Error(`PanSou API error: ${json.message || json.error || json.code}`);
    }
    return json;
  } finally {
    clearTimeout(timeout);
  }
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function unwrapData(response) {
  if (response && typeof response === "object" && response.data && typeof response.data === "object") {
    return response.data;
  }
  return response || {};
}

function flattenMergedLinks(mergedByType) {
  const flattened = [];
  for (const [diskType, links] of Object.entries(mergedByType || {})) {
    for (const link of links || []) {
      flattened.push({ diskType, ...link });
    }
  }
  return flattened;
}

function flattenResultsLinks(results) {
  const flattened = [];
  for (const result of results || []) {
    for (const link of result.links || []) {
      flattened.push({
        diskType: link.type || "others",
        url: link.url,
        password: link.password,
        note: link.work_title || result.title,
        datetime: link.datetime || result.datetime,
        source: result.channel ? `tg:${result.channel}` : "unknown",
        images: result.images || []
      });
    }
  }
  return flattened;
}

function groupResultsByType(results) {
  const grouped = {};
  for (const result of results || []) {
    for (const link of result.links || []) {
      const diskType = link.type || "others";
      if (!grouped[diskType]) grouped[diskType] = [];
      grouped[diskType].push({
        url: link.url,
        password: link.password,
        note: link.work_title || result.title,
        datetime: link.datetime || result.datetime,
        source: result.channel ? `tg:${result.channel}` : "unknown",
        images: result.images || []
      });
    }
  }
  return grouped;
}

function normalizeDownloadLink(link, rank) {
  const extractionCode = link.password || extractCodeFromUrl(link.url) || null;
  const provider = providerLabel(link.diskType);
  const label = link.note || provider;
  return {
    rank,
    provider,
    diskType: link.diskType,
    label,
    note: link.note || "",
    url: link.url,
    extractionCode,
    extractionCodes: extractionCode ? [extractionCode] : [],
    datetime: link.datetime || "",
    source: link.source || "",
    images: link.images || []
  };
}

function stripRank(link) {
  const { rank, ...rest } = link;
  return rest;
}

function providerLabel(diskType) {
  return PROVIDER_LABELS[diskType] || diskType || "未知来源";
}

function extractCodeFromUrl(url) {
  try {
    const parsed = new URL(url);
    return ["pwd", "password", "passcode", "extract_code", "extraction_code"]
      .map((name) => parsed.searchParams.get(name))
      .find(Boolean) || null;
  } catch {
    return null;
  }
}

function buildFilter(include, exclude) {
  const filter = {};
  if (include && include.length > 0) filter.include = include;
  if (exclude && exclude.length > 0) filter.exclude = exclude;
  return Object.keys(filter).length > 0 ? filter : null;
}

function countBy(items, key) {
  const counts = {};
  for (const item of items) {
    const value = item[key] || "unknown";
    counts[value] = (counts[value] || 0) + 1;
  }
  return counts;
}

function normalizeApiBase(value) {
  const trimmed = (value || DEFAULT_API_BASE).replace(/\/+$/g, "");
  if (trimmed.endsWith("/api")) return trimmed;
  return `${trimmed}/api`;
}

function parseList(value = "") {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function parseJson(value, label) {
  try {
    return JSON.parse(value || "{}");
  } catch (error) {
    throw new Error(`${label} must be valid JSON: ${error.message}`);
  }
}

function isCliEntryPoint() {
  return Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export {
  buildSearchQueryParams,
  formatSearchResult,
  normalizeCheckLinksResponse,
  normalizePanSouSearchResponse,
  parseArgs,
  renderMarkdownTable
};
