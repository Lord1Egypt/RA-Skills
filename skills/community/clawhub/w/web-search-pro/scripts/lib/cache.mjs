import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

import { resolveCacheDir } from "./config.mjs";

function sortObject(value) {
  if (Array.isArray(value)) {
    return value.map(sortObject);
  }
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, sortObject(value[key])]),
    );
  }
  return value;
}

function stableStringify(value) {
  return JSON.stringify(sortObject(value));
}

function getNow(options = {}) {
  return typeof options.now === "number" ? options.now : Date.now();
}

function normalizeTtlSeconds(value) {
  const ttlSeconds = Number.isFinite(value) ? Math.max(0, Math.trunc(value)) : 0;
  return ttlSeconds;
}

function getKindDirectory(kind, options = {}) {
  const cwd = options.cwd ?? process.cwd();
  return path.join(resolveCacheDir(options.config, cwd), kind);
}

function getEntryPath(kind, key, options = {}) {
  return path.join(getKindDirectory(kind, options), `${key}.json`);
}

async function ensureKindDir(kind, options = {}) {
  await fs.mkdir(getKindDirectory(kind, options), { recursive: true });
}

async function listJsonFiles(dirPath) {
  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });
    return entries
      .filter((entry) => entry.isFile() && entry.name.endsWith(".json"))
      .map((entry) => path.join(dirPath, entry.name));
  } catch (error) {
    if (error.code === "ENOENT") {
      return [];
    }
    throw error;
  }
}

function createHash(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function normalizeSearchFilters(request = {}) {
  return {
    count: request.count ?? 5,
    deep: Boolean(request.deep),
    news: Boolean(request.news),
    days: request.days ?? null,
    includeDomains: [...(request.includeDomains ?? [])].sort(),
    excludeDomains: [...(request.excludeDomains ?? [])].sort(),
    timeRange: request.timeRange ?? null,
    fromDate: request.fromDate ?? null,
    toDate: request.toDate ?? null,
    searchEngine: request.searchEngine ?? null,
    country: request.country ?? null,
    lang: request.lang ?? null,
  };
}

function normalizeUrlList(urls = []) {
  return [...urls].map((url) => String(url)).sort();
}

export function buildSearchCacheKey({ providerId, request, federation = null }) {
  return createHash(
    stableStringify({
      providerId,
      query: String(request.query ?? "").trim(),
      filters: normalizeSearchFilters(request),
      federation:
        federation && federation.triggered
          ? {
              mergePolicy: federation.mergePolicy,
              providersPlanned: [...(federation.providersPlanned ?? [])].sort(),
              maxPerProvider: federation.maxPerProvider,
              triggerReasons: [...(federation.triggerReasons ?? [])].sort(),
              fanoutPolicy: federation.fanoutPolicy ?? null,
            }
          : null,
    }),
  );
}

export function buildExtractCacheKey({
  command = "extract",
  providerId,
  urls,
  maxChars,
  render = null,
}) {
  return createHash(
    stableStringify({
      strategyVersion: 3,
      command: String(command),
      providerId,
      urls: normalizeUrlList(urls),
      maxChars,
      render:
        render && render.policy
          ? {
              policy: render.policy,
              budgetMs: render.budgetMs ?? null,
              waitUntil: render.waitUntil ?? null,
              blockTypes: [...(render.blockTypes ?? [])].sort(),
              sameOriginOnly: render.sameOriginOnly ?? null,
            }
          : null,
    }),
  );
}

export function buildCrawlCacheKey({
  entryUrls,
  depth,
  maxPages,
  sameOrigin,
  includePathPrefixes,
  excludePathPrefixes,
}) {
  return createHash(
    stableStringify({
      entryUrls: normalizeUrlList(entryUrls),
      depth,
      maxPages,
      sameOrigin: Boolean(sameOrigin),
      includePathPrefixes: [...(includePathPrefixes ?? [])].sort(),
      excludePathPrefixes: [...(excludePathPrefixes ?? [])].sort(),
    }),
  );
}

export function buildMapCacheKey(input) {
  return buildCrawlCacheKey(input);
}

export async function readCacheRecord(kind, key, options = {}) {
  if (!options.config.cache.enabled) {
    return null;
  }

  const entryPath = getEntryPath(kind, key, options);

  let raw;
  try {
    raw = await fs.readFile(entryPath, "utf8");
  } catch (error) {
    if (error.code === "ENOENT") {
      return null;
    }
    throw error;
  }

  const entry = JSON.parse(raw);
  if (entry.expiresAt <= getNow(options)) {
    await fs.rm(entryPath, { force: true });
    return null;
  }

  return entry;
}

export async function readCacheEntry(kind, key, options = {}) {
  const entry = await readCacheRecord(kind, key, options);
  return entry?.value ?? null;
}

export async function writeCacheEntry(kind, key, value, options = {}) {
  if (!options.config.cache.enabled) {
    return null;
  }

  await ensureKindDir(kind, options);

  const now = getNow(options);
  const ttlSeconds = normalizeTtlSeconds(options.ttlSeconds);
  const entry = {
    key,
    createdAt: now,
    expiresAt: now + ttlSeconds * 1000,
    value,
  };

  const entryPath = getEntryPath(kind, key, options);
  await fs.writeFile(entryPath, JSON.stringify(entry, null, 2));
  return entry;
}

export function buildCacheTelemetry(kind, options = {}) {
  const enabled = options.enabled ?? options.config?.cache?.enabled ?? true;
  const now = getNow(options);
  const ttlSeconds = normalizeTtlSeconds(options.ttlSeconds);
  const record = options.record ?? null;

  if (!enabled) {
    return {
      enabled: false,
      hit: false,
      kind,
      createdAt: null,
      expiresAt: null,
      ageSeconds: null,
      ttlRemainingSeconds: null,
      ttlSeconds,
    };
  }

  const createdAt = record?.createdAt ?? now;
  const expiresAt = record?.expiresAt ?? createdAt + ttlSeconds * 1000;
  const ageSeconds = Math.max(0, Math.floor((now - createdAt) / 1000));
  const ttlRemainingSeconds = Math.max(0, Math.ceil((expiresAt - now) / 1000));

  return {
    enabled: true,
    hit: Boolean(record),
    kind,
    createdAt,
    expiresAt,
    ageSeconds,
    ttlRemainingSeconds,
    ttlSeconds: Math.max(ttlSeconds, Math.round((expiresAt - createdAt) / 1000)),
  };
}

export async function getCacheStats(options = {}) {
  const enabled = options.config.cache.enabled;
  const cacheDir = resolveCacheDir(options.config, options.cwd ?? process.cwd());

  if (!enabled) {
    return {
      enabled,
      dir: cacheDir,
      entries: 0,
      bytes: 0,
    };
  }

  let entries = 0;
  let bytes = 0;
  for (const kind of ["search", "extract", "crawl", "map"]) {
    const files = await listJsonFiles(path.join(cacheDir, kind));
    entries += files.length;
    for (const filePath of files) {
      const stat = await fs.stat(filePath);
      bytes += stat.size;
    }
  }

  return {
    enabled,
    dir: cacheDir,
    entries,
    bytes,
  };
}

export async function clearCache(options = {}) {
  const cacheDir = resolveCacheDir(options.config, options.cwd ?? process.cwd());
  let removedEntries = 0;

  for (const kind of ["search", "extract", "crawl", "map"]) {
    const files = await listJsonFiles(path.join(cacheDir, kind));
    removedEntries += files.length;
    for (const filePath of files) {
      await fs.rm(filePath, { force: true });
    }
  }

  return {
    dir: cacheDir,
    removedEntries,
  };
}
