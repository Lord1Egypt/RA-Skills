#!/usr/bin/env node
// tavily-search-pro-native-node/scripts/tavily-pro.mjs
// Research-grade Tavily web search for OpenClaw.
// Subcommands: search, extract, stats, cache
// Requires Node 18+ (uses native fetch). Reads TAVILY_API_KEY from the process environment only.

import { createHash } from "node:crypto";
import { existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, rmSync, statSync, writeFileSync, appendFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, relative, resolve } from "node:path";

const SEARCH_ENDPOINT = "https://api.tavily.com/search";
const EXTRACT_ENDPOINT = "https://api.tavily.com/extract";
const SKILL_DIR_NAME = "tavily-search-pro-native-node";
const BASE_DIR = join(homedir(), ".openclaw", "cache", SKILL_DIR_NAME);
const CACHE_DIR = join(BASE_DIR, "cache");
const USAGE_LOG = join(BASE_DIR, "usage.log");

// Default TTLs (seconds).
const DEFAULT_TTL = {
  search_general: 24 * 60 * 60,  // 24 hours
  search_news: 60 * 60,          // 1 hour
  extract: 7 * 24 * 60 * 60,     // 7 days - extracted content is pretty stable
};

// Rate-limit backoff config
const RETRY_MAX = 3;
const RETRY_BASE_MS = 1000;
const DEFAULT_TIMEOUT_MS = 30000;

// -------- utilities --------

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function warn(msg) {
  process.stderr.write(`warn: ${msg}\n`);
}

function loadApiKey() {
  const value = (process.env.TAVILY_API_KEY || "").trim();
  if (!value) die("TAVILY_API_KEY not set. Export it in the process environment.");
  warn("using TAVILY_API_KEY from env:TAVILY_API_KEY");
  return value;
}

function asciiSafe(s) {
  return String(s)
    .replace(/[\u00a0]/g, " ")
    .replace(/[\u00b7]/g, "-")
    .replace(/[\u2010-\u2015]/g, "-")
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u201c\u201d]/g, '"')
    .replace(/[\u2026]/g, "...")
    .replace(/[\u2192]/g, "->")
    .replace(/[^\x09\x0a\x0d\x20-\x7e]/g, "?");
}

function truncate(s, n) {
  if (!s) return "";
  return s.length > n ? s.slice(0, n - 3) + "..." : s;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function isPrivateIpv4Literal(host) {
  const m = String(host).match(/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/);
  if (!m) return false;
  const octets = m.slice(1).map(Number);
  if (octets.some(n => !Number.isInteger(n) || n < 0 || n > 255)) return false;
  const [a, b] = octets;
  if (a === 0) return true;
  if (a === 10) return true;
  if (a === 127) return true;
  if (a === 169 && b === 254) return true;
  if (a === 172 && b >= 16 && b <= 31) return true;
  if (a === 192 && b === 168) return true;
  return false;
}

function ipv4FromMappedIpv6Host(host) {
  const value = String(host).toLowerCase();
  if (!value.startsWith("::ffff:")) return null;
  const tail = value.slice("::ffff:".length);
  if (/^\d+\.\d+\.\d+\.\d+$/.test(tail)) return tail;
  const m = tail.match(/^([0-9a-f]{1,4}):([0-9a-f]{1,4})$/i);
  if (!m) return null;
  const hi = Number.parseInt(m[1], 16);
  const lo = Number.parseInt(m[2], 16);
  if (hi > 0xffff || lo > 0xffff) return null;
  return `${(hi >> 8) & 255}.${hi & 255}.${(lo >> 8) & 255}.${lo & 255}`;
}

function isLocalOrPrivateUrl(raw) {
  let parsed;
  try { parsed = new URL(raw); } catch { return false; }
  const host = parsed.hostname.toLowerCase().replace(/^\[|\]$/g, "");
  if (host === "localhost" || host.endsWith(".localhost")) return true;
  if (host === "::" || host === "0:0:0:0:0:0:0:0") return true;
  if (host === "::1" || host === "0:0:0:0:0:0:0:1") return true;
  const mappedIpv4 = ipv4FromMappedIpv6Host(host);
  if (mappedIpv4 && isPrivateIpv4Literal(mappedIpv4)) return true;
  const ipv6Head = host.match(/^([0-9a-f]{1,4})(?::|$)/i)?.[1];
  if (ipv6Head) {
    const firstHextet = Number.parseInt(ipv6Head, 16);
    if (firstHextet >= 0xfc00 && firstHextet <= 0xfdff) return true;
    if (firstHextet >= 0xfe80 && firstHextet <= 0xfebf) return true;
  }
  if (isPrivateIpv4Literal(host)) return true;
  return false;
}

function parseHttpUrlArg(raw) {
  const value = String(raw);
  if (value.includes("\\")) return { ok: false, reason: "invalid" };
  if (!/^https?:\/\/(?!\/)/i.test(value)) return { ok: false, reason: "invalid" };
  try {
    const parsed = new URL(value);
    if (parsed.username || parsed.password) return { ok: false, reason: "userinfo" };
    const ok = (parsed.protocol === "http:" || parsed.protocol === "https:") && parsed.hostname !== "";
    return ok ? { ok: true, parsed } : { ok: false, reason: "invalid" };
  } catch {
    return { ok: false, reason: "invalid" };
  }
}

function isHttpUrl(raw) {
  return parseHttpUrlArg(raw).ok;
}

// -------- cache --------

function cacheKey(kind, body) {
  const h = createHash("sha256");
  h.update(kind + "\n" + JSON.stringify(body));
  return h.digest("hex").slice(0, 32);
}

function cachePath(key) {
  return join(CACHE_DIR, key + ".json");
}

function pathWithin(root, candidate) {
  const rel = relative(resolve(root), resolve(candidate));
  return rel === "" || (rel && !rel.startsWith("..") && !/^[A-Za-z]:[\\/]/.test(rel) && !rel.startsWith("\\") && !rel.startsWith("/"));
}

function samePath(a, b) {
  const ar = resolve(a);
  const br = resolve(b);
  return process.platform === "win32" ? ar.toLowerCase() === br.toLowerCase() : ar === br;
}

function expectedCacheFileName(name) {
  return /^[a-f0-9]{32}\.json$/.test(String(name));
}

function assertContainedDirSafe(dir, label) {
  const homeRoot = resolve(homedir());
  const intendedBase = resolve(homeRoot, ".openclaw", "cache", SKILL_DIR_NAME);
  const intendedCache = resolve(intendedBase, "cache");
  const resolvedDir = resolve(dir);
  if (label === "usage log directory" && !samePath(BASE_DIR, intendedBase)) {
    throw new Error("refusing usage log access: base path is not the intended skill cache path");
  }
  if (label === "cache directory" && !samePath(CACHE_DIR, intendedCache)) {
    throw new Error("refusing cache access: cache path is not the intended skill cache path");
  }
  if (!pathWithin(homeRoot, resolvedDir)) throw new Error(`refusing persistent-state access: ${label} escapes home directory`);
  const relParts = relative(homeRoot, resolvedDir).split(/[\\/]+/).filter(Boolean);
  let cursor = homeRoot;
  for (const part of relParts) {
    cursor = join(cursor, part);
    if (!existsSync(cursor)) continue;
    const st = lstatSync(cursor);
    if (st.isSymbolicLink()) throw new Error(`refusing persistent-state access: ${label} contains symlink indirection`);
  }
  if (!existsSync(resolvedDir)) mkdirSync(resolvedDir, { recursive: true });
  const dirSt = lstatSync(resolvedDir);
  if (!dirSt.isDirectory() || dirSt.isSymbolicLink()) throw new Error(`refusing persistent-state access: ${label} is not a normal directory`);
  return true;
}

function assertCacheDirSafe() {
  return assertContainedDirSafe(CACHE_DIR, "cache directory");
}

function assertUsageLogDirSafe() {
  return assertContainedDirSafe(BASE_DIR, "usage log directory");
}

function assertContainedFileSafe(filePath, rootDir, expectedName, label) {
  const resolvedFile = resolve(filePath);
  const resolvedRoot = resolve(rootDir);
  if (!pathWithin(resolvedRoot, resolvedFile)) throw new Error(`refusing ${label}: path escapes intended directory`);
  if (expectedName && resolvedFile.split(/[\\/]+/).pop() !== expectedName) throw new Error(`refusing ${label}: unexpected filename`);
  if (existsSync(resolvedFile)) {
    const st = lstatSync(resolvedFile);
    if (!st.isFile() || st.isSymbolicLink()) throw new Error(`refusing ${label}: target is not a normal file`);
    const rootReal = realpathSync(resolvedRoot);
    const fileReal = realpathSync(resolvedFile);
    if (!pathWithin(rootReal, fileReal)) throw new Error(`refusing ${label}: target resolves outside intended directory`);
  }
  return true;
}

function cacheRead(key, ttlSec) {
  try {
    if (!expectedCacheFileName(key + ".json")) return null;
    assertCacheDirSafe();
    const p = cachePath(key);
    assertContainedFileSafe(p, CACHE_DIR, key + ".json", "cache read");
    const st = statSync(p);
    const ageMs = Date.now() - st.mtimeMs;
    if (ageMs > ttlSec * 1000) return null;
    return JSON.parse(readFileSync(p, "utf8"));
  } catch (e) {
    if (e instanceof SyntaxError) warn(`cache read failed: ${e.message}`);
    else if (e?.message?.startsWith?.("refusing ")) warn(e.message);
    return null;
  }
}

function cacheWrite(key, data) {
  try {
    if (!expectedCacheFileName(key + ".json")) throw new Error("refusing cache write: unexpected cache key");
    assertCacheDirSafe();
    const p = cachePath(key);
    assertContainedFileSafe(p, CACHE_DIR, key + ".json", "cache write");
    writeFileSync(p, JSON.stringify(data), "utf8");
  } catch (e) {
    warn(`cache write failed: ${e.message}`);
  }
}

function assertCacheClearRootSafe() {
  if (!existsSync(CACHE_DIR)) return false;
  const homeRoot = resolve(homedir());
  const intendedBase = resolve(homeRoot, ".openclaw", "cache", SKILL_DIR_NAME);
  const intendedCache = resolve(intendedBase, "cache");
  if (!samePath(BASE_DIR, intendedBase) || !samePath(CACHE_DIR, intendedCache)) {
    die("refusing cache clear: cache path is not the intended skill cache path");
  }
  if (!pathWithin(homeRoot, intendedCache)) die("refusing cache clear: cache path escapes home directory");
  const relParts = relative(homeRoot, intendedCache).split(/[\\/]+/).filter(Boolean);
  let cursor = homeRoot;
  for (const part of relParts) {
    cursor = join(cursor, part);
    if (!existsSync(cursor)) return false;
    const st = lstatSync(cursor);
    if (st.isSymbolicLink()) die("refusing cache clear: cache path contains symlink indirection");
  }
  const cacheSt = lstatSync(CACHE_DIR);
  if (!cacheSt.isDirectory() || cacheSt.isSymbolicLink()) die("refusing cache clear: cache path is not a normal directory");
  return true;
}

function cacheClear() {
  if (!assertCacheClearRootSafe()) return { deleted: 0, skipped: 0 };
  const cacheReal = realpathSync(CACHE_DIR);
  const entries = readdirSync(CACHE_DIR, { withFileTypes: true });
  const deletions = [];
  let skipped = 0;
  for (const ent of entries) {
    if (!expectedCacheFileName(ent.name)) { skipped++; continue; }
    const target = join(CACHE_DIR, ent.name);
    const st = lstatSync(target);
    if (!ent.isFile() || st.isSymbolicLink()) die(`refusing cache clear: unexpected cache entry type for ${ent.name}`);
    const targetReal = realpathSync(target);
    if (!pathWithin(cacheReal, targetReal)) die(`refusing cache clear: cache entry resolves outside cache directory: ${ent.name}`);
    deletions.push({ name: ent.name, target });
  }
  let deleted = 0;
  for (const item of deletions) {
    try {
      rmSync(item.target);
      deleted++;
    } catch (e) {
      die(`cache clear failed after deleting ${deleted} of ${deletions.length} cache entries: ${e.message}`);
    }
  }
  return { deleted, skipped };
}

function cacheInfo() {
  try {
    assertCacheDirSafe();
    const entries = readdirSync(CACHE_DIR).filter(f => f.endsWith(".json"));
    let totalBytes = 0;
    let oldest = Infinity;
    let newest = 0;
    let count = 0;
    for (const f of entries) {
      const p = join(CACHE_DIR, f);
      try { assertContainedFileSafe(p, CACHE_DIR, f, "cache info read"); }
      catch { continue; }
      const st = statSync(p);
      count++;
      totalBytes += st.size;
      if (st.mtimeMs < oldest) oldest = st.mtimeMs;
      if (st.mtimeMs > newest) newest = st.mtimeMs;
    }
    return {
      dir: CACHE_DIR,
      count,
      bytes: totalBytes,
      oldestAgeMin: oldest === Infinity ? null : Math.floor((Date.now() - oldest) / 60000),
      newestAgeMin: newest === 0 ? null : Math.floor((Date.now() - newest) / 60000),
    };
  } catch (e) {
    if (e?.message?.startsWith?.("refusing ")) warn(e.message);
    return { dir: CACHE_DIR, count: 0, bytes: 0, oldestAgeMin: null, newestAgeMin: null };
  }
}

// -------- usage log --------

function logUsage(entry) {
  try {
    assertUsageLogDirSafe();
    assertContainedFileSafe(USAGE_LOG, BASE_DIR, "usage.log", "usage log write");
    appendFileSync(USAGE_LOG, JSON.stringify(entry) + "\n", "utf8");
  } catch (e) {
    warn(`usage log write failed: ${e.message}`);
  }
}

function readUsage(sinceMs) {
  try {
    assertUsageLogDirSafe();
    if (!existsSync(USAGE_LOG)) return [];
    assertContainedFileSafe(USAGE_LOG, BASE_DIR, "usage.log", "usage log read");
    const txt = readFileSync(USAGE_LOG, "utf8");
    const out = [];
    for (const line of txt.split(/\r?\n/)) {
      if (!line.trim()) continue;
      try {
        const e = JSON.parse(line);
        if (sinceMs && e.ts && e.ts < sinceMs) continue;
        out.push(e);
      } catch { /* skip bad lines */ }
    }
    return out;
  } catch (e) {
    if (e?.message?.startsWith?.("refusing ")) warn(e.message);
    return [];
  }
}

// -------- HTTP with backoff --------

async function callWithBackoff(url, body, apiKey, { noRetry = false, timeoutMs = DEFAULT_TIMEOUT_MS } = {}) {
  let lastErr;
  const attempts = noRetry ? 1 : RETRY_MAX;
  for (let i = 0; i < attempts; i++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });
      clearTimeout(timer);
      const text = await resp.text();
      if (resp.ok) {
        try { return { ok: true, data: JSON.parse(text), status: resp.status }; }
        catch { return { ok: false, status: resp.status, detail: "invalid JSON from server" }; }
      }
      // Non-OK. Check if retryable.
      if (resp.status === 429 && i < attempts - 1) {
        const retryAfter = parseInt(resp.headers.get("retry-after") || "", 10);
        const waitMs = !isNaN(retryAfter) ? retryAfter * 1000 : RETRY_BASE_MS * Math.pow(2, i);
        await sleep(waitMs);
        continue;
      }
      let detail = text;
      try { const j = JSON.parse(text); detail = j.detail || j.error || text; } catch { /* plain text */ }
      return { ok: false, status: resp.status, detail: String(detail).slice(0, 500), retryAfter: resp.headers.get("retry-after") };
    } catch (e) {
      clearTimeout(timer);
      lastErr = e;
      if (i < attempts - 1) {
        await sleep(RETRY_BASE_MS * Math.pow(2, i));
        continue;
      }
    }
  }
  return { ok: false, status: 0, detail: `network error: ${lastErr?.message || "unknown"}` };
}

async function callTavily(url, body, apiKey, options = {}) {
  if (process.env.TAVILY_PRO_SELFTEST === "1" && process.env.TAVILY_PRO_MOCK_JSON) {
    try { return { ok: true, data: JSON.parse(process.env.TAVILY_PRO_MOCK_JSON), status: 200 }; }
    catch { return { ok: false, status: 0, detail: "invalid TAVILY_PRO_MOCK_JSON" }; }
  }
  return callWithBackoff(url, body, apiKey, options);
}

// -------- arg helpers --------

function isLikelyFlag(value) {
  return typeof value === "string" && /^--[A-Za-z]/.test(value);
}

function flagValue(argv, index, name) {
  const value = argv[index + 1];
  if (value === undefined || isLikelyFlag(value)) die(`flag ${name} needs a value`);
  return value;
}

function consumeFlag(argv, name, hasValue) {
  // Non-mutating: returns {value, rest}
  const rest = [];
  let value = hasValue ? null : false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === name) {
      if (hasValue) {
        value = flagValue(argv, i, name);
        i++;
      } else {
        value = true;
      }
    } else {
      rest.push(argv[i]);
    }
  }
  return { value, rest };
}

function parsePositiveInt(value, label) {
  const n = Number(value);
  if (!Number.isInteger(n) || n < 1) die(`${label} must be a positive int`);
  return n;
}

function rejectLeftovers(argv, context) {
  if (argv.length) die(`unknown argument for ${context}: ${argv[0]}`);
}

function parseCommonSearchArgs(argv) {
  const out = {
    topic: "general",
    depth: "basic",
    max: 5,
    days: 7,
    include: [],
    exclude: [],
    json: false,
    rawContent: false,
    noCache: false,
    noLog: false,
    noRetry: false,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    ttl: null,
    query: "",
  };
  const stringFlags = new Set(["--topic", "--depth", "--max", "--days", "--include", "--exclude", "--ttl", "--timeout-ms"]);
  const leftovers = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") { out.json = true; continue; }
    if (a === "--raw-content") { out.rawContent = true; continue; }
    if (a === "--no-cache") { out.noCache = true; continue; }
    if (a === "--no-log") { out.noLog = true; continue; }
    if (a === "--no-retry") { out.noRetry = true; continue; }
    if (stringFlags.has(a)) {
      const v = flagValue(argv, i, a);
      i++;
      switch (a) {
        case "--topic":
          if (!["general", "news"].includes(v)) die(`--topic must be general|news`);
          out.topic = v; break;
        case "--depth":
          if (!["basic", "advanced"].includes(v)) die(`--depth must be basic|advanced`);
          out.depth = v; break;
        case "--max": {
          const n = Number(v);
          if (!Number.isInteger(n) || n < 1 || n > 20) die(`--max must be 1-20`);
          out.max = n; break;
        }
        case "--days": {
          const n = Number(v);
          if (!Number.isInteger(n) || n < 1) die(`--days must be positive int`);
          out.days = n; break;
        }
        case "--include":
          out.include = v.split(",").map(s => s.trim()).filter(Boolean); break;
        case "--exclude":
          out.exclude = v.split(",").map(s => s.trim()).filter(Boolean); break;
        case "--ttl": {
          const n = Number(v);
          if (!Number.isInteger(n) || n < 0) die(`--ttl must be non-negative int`);
          out.ttl = n; break;
        }
        case "--timeout-ms":
          out.timeoutMs = parsePositiveInt(v, "--timeout-ms"); break;
      }
      continue;
    }
    if (isLikelyFlag(a)) die(`unknown flag for search: ${a}`);
    leftovers.push(a);
  }
  out.query = leftovers.join(" ").trim();
  return out;
}

// -------- subcommand: search --------

function formatSearchHuman(resp, args, elapsedMs, fromCache) {
  const lines = [];
  lines.push(`Query: ${args.query}`);
  const meta = [`Topic: ${args.topic}`, `Depth: ${args.depth}`, `Results: ${(resp.results || []).length}/${args.max}`];
  if (fromCache) meta.push("cache: hit");
  lines.push(meta.join(" - "));
  if (resp.answer) {
    lines.push("");
    lines.push("Answer:");
    lines.push(truncate(String(resp.answer).trim(), 1200));
  }
  lines.push("");
  lines.push("Results:");
  (resp.results || []).forEach((r, i) => {
    lines.push(`${i + 1}. ${r.title || "(no title)"}`);
    lines.push(`   ${r.url || ""}`);
    if (r.published_date) lines.push(`   published: ${r.published_date}`);
    if (r.content) lines.push(`   ${truncate(String(r.content).replace(/\s+/g, " ").trim(), 280)}`);
    if (args.rawContent && r.raw_content) {
      const clean = String(r.raw_content).replace(/\s+/g, " ").trim();
      lines.push(`   --- raw content (${clean.length} chars) ---`);
      lines.push(`   ${truncate(clean, 2000)}`);
    }
  });
  lines.push("");
  const parts = [`elapsed ${elapsedMs}ms`];
  if (fromCache) parts.push("cached (0 credits)");
  else if (resp.response_time) parts.push(`api ${resp.response_time}s`);
  lines.push(`- ${parts.join(" - ")}`);
  return asciiSafe(lines.join("\n"));
}

async function cmdSearch(argv) {
  const args = parseCommonSearchArgs(argv);
  if (!args.query) die(`search needs a query. Example: tavily-pro.mjs search "latest AI news"`);
  const apiKey = loadApiKey();

  const body = {
    query: args.query,
    topic: args.topic,
    search_depth: args.depth,
    max_results: args.max,
    include_answer: true,
    include_raw_content: args.rawContent,
    include_images: false,
  };
  if (args.topic === "news") body.days = args.days;
  if (args.include.length) body.include_domains = args.include;
  if (args.exclude.length) body.exclude_domains = args.exclude;

  const ttl = args.ttl !== null ? args.ttl : DEFAULT_TTL["search_" + args.topic];
  const key = cacheKey("search", body);

  if (!args.noCache) {
    const cached = cacheRead(key, ttl);
    if (cached) {
      if (!args.noLog) {
        logUsage({ ts: Date.now(), kind: "search", query: args.query, depth: args.depth, topic: args.topic, cached: true, credits: 0 });
      }
      if (args.json) { process.stdout.write(JSON.stringify(cached, null, 2) + "\n"); return; }
      process.stdout.write(formatSearchHuman(cached, args, 0, true) + "\n");
      return;
    }
  }

  const started = Date.now();
  const result = await callTavily(SEARCH_ENDPOINT, body, apiKey, { noRetry: args.noRetry, timeoutMs: args.timeoutMs });
  const elapsed = Date.now() - started;

  if (!result.ok) {
    if (!args.noLog) {
      logUsage({ ts: Date.now(), kind: "search", query: args.query, depth: args.depth, topic: args.topic, cached: false, credits: 0, error: result.status });
    }
    const retryHint = result.retryAfter ? ` (retry-after: ${result.retryAfter}s)` : "";
    die(`HTTP ${result.status}${retryHint}: ${result.detail}`);
  }

  if (!args.noCache) cacheWrite(key, result.data);

  const credits = args.depth === "advanced" ? 2 : 1;
  if (!args.noLog) {
    logUsage({ ts: Date.now(), kind: "search", query: args.query, depth: args.depth, topic: args.topic, cached: false, credits });
  }

  if (args.json) { process.stdout.write(JSON.stringify(result.data, null, 2) + "\n"); return; }
  process.stdout.write(formatSearchHuman(result.data, args, elapsed, false) + "\n");
}

// -------- subcommand: extract --------

function formatExtractHuman(resp, urls, elapsedMs, fromCache) {
  const lines = [];
  lines.push(`Extract: ${urls.length} URL${urls.length !== 1 ? "s" : ""}`);
  if (fromCache) lines.push("cache: hit");
  lines.push("");
  const results = resp.results || [];
  const failed = resp.failed_results || [];
  results.forEach((r, i) => {
    const content = String(r.raw_content || "").replace(/\s+/g, " ").trim();
    lines.push(`[${i + 1}] ${r.url || "(no url)"}`);
    lines.push(`    ${content.length} chars extracted`);
    lines.push(`    ${truncate(content, 1500)}`);
    lines.push("");
  });
  if (failed.length) {
    lines.push("Failed:");
    failed.forEach((f) => lines.push(`  - ${f.url || "(unknown)"} :: ${f.error || "unknown error"}`));
    lines.push("");
  }
  const parts = [`elapsed ${elapsedMs}ms`];
  if (fromCache) parts.push("cached (0 credits)");
  lines.push(`- ${parts.join(" - ")}`);
  return asciiSafe(lines.join("\n"));
}

function parseExtractArgs(argv) {
  const out = {
    json: false,
    noCache: false,
    noLog: false,
    noRetry: false,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    ttl: DEFAULT_TTL.extract,
    depth: "basic",
    urls: [],
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") { out.json = true; continue; }
    if (a === "--no-cache") { out.noCache = true; continue; }
    if (a === "--no-log") { out.noLog = true; continue; }
    if (a === "--no-retry") { out.noRetry = true; continue; }
    if (a === "--ttl") {
      const v = flagValue(argv, i, a);
      const n = Number(v);
      if (!Number.isInteger(n) || n < 0) die(`--ttl must be non-negative int`);
      out.ttl = n;
      i++;
      continue;
    }
    if (a === "--timeout-ms") {
      out.timeoutMs = parsePositiveInt(flagValue(argv, i, a), "--timeout-ms");
      i++;
      continue;
    }
    if (a === "--depth") {
      const v = flagValue(argv, i, a);
      if (!["basic", "advanced"].includes(v)) die(`--depth must be basic|advanced`);
      out.depth = v;
      i++;
      continue;
    }
    if (isLikelyFlag(a)) die(`unknown flag for extract: ${a}`);
    out.urls.push(a);
  }
  return out;
}

async function cmdExtract(argv) {
  const { json, noCache, noLog, noRetry, timeoutMs, ttl, depth: extractDepth, urls } = parseExtractArgs(argv);

  if (urls.length === 0) die(`extract needs at least one URL. Example: tavily-pro.mjs extract https://example.com`);
  for (const u of urls) {
    const parsedUrl = parseHttpUrlArg(u);
    if (!parsedUrl.ok) {
      if (parsedUrl.reason === "userinfo") die("credential-bearing URLs are not allowed for Tavily extract");
      die("invalid URL");
    }
    if (isLocalOrPrivateUrl(u)) die("refusing local/private URL for Tavily extract");
  }

  const apiKey = loadApiKey();
  const body = { urls, extract_depth: extractDepth, include_images: false };
  const key = cacheKey("extract", body);

  if (!noCache) {
    const cached = cacheRead(key, ttl);
    if (cached) {
      if (!noLog) logUsage({ ts: Date.now(), kind: "extract", urls, depth: extractDepth, cached: true, credits: 0 });
      if (json) { process.stdout.write(JSON.stringify(cached, null, 2) + "\n"); return; }
      process.stdout.write(formatExtractHuman(cached, urls, 0, true) + "\n");
      return;
    }
  }

  const started = Date.now();
  const result = await callTavily(EXTRACT_ENDPOINT, body, apiKey, { noRetry, timeoutMs });
  const elapsed = Date.now() - started;

  if (!result.ok) {
    if (!noLog) logUsage({ ts: Date.now(), kind: "extract", urls, depth: extractDepth, cached: false, credits: 0, error: result.status });
    const retryHint = result.retryAfter ? ` (retry-after: ${result.retryAfter}s)` : "";
    die(`HTTP ${result.status}${retryHint}: ${result.detail}`);
  }

  if (!noCache) cacheWrite(key, result.data);

  // Tavily extract: 1 credit per 5 URLs (basic), 2 per 5 (advanced).
  const rawCredits = extractDepth === "advanced" ? 2 : 1;
  const credits = Math.ceil(urls.length / 5) * rawCredits;
  if (!noLog) logUsage({ ts: Date.now(), kind: "extract", urls, depth: extractDepth, cached: false, credits });

  if (json) { process.stdout.write(JSON.stringify(result.data, null, 2) + "\n"); return; }
  process.stdout.write(formatExtractHuman(result.data, urls, elapsed, false) + "\n");
}

// -------- subcommand: stats --------

function cmdStats(argv) {
  const { value: daysStr, rest: rest1 } = consumeFlag(argv, "--days", true);
  const { value: jsonOut, rest: rest2 } = consumeFlag(rest1, "--json", false);
  rejectLeftovers(rest2, "stats");

  const daysBack = daysStr !== null ? Number(daysStr) : 30;
  if (!Number.isInteger(daysBack) || daysBack < 1) die(`--days must be positive int`);
  const sinceMs = Date.now() - daysBack * 24 * 60 * 60 * 1000;

  const entries = readUsage(sinceMs);
  const summary = {
    days_back: daysBack,
    total_calls: entries.length,
    searches: entries.filter(e => e.kind === "search").length,
    extracts: entries.filter(e => e.kind === "extract").length,
    cache_hits: entries.filter(e => e.cached).length,
    cache_misses: entries.filter(e => e.cached === false).length,
    errors: entries.filter(e => e.error).length,
    credits_used: entries.reduce((s, e) => s + (e.credits || 0), 0),
    estimated_credits_avoided_by_cache: entries.filter(e => e.cached).reduce((s, e) => {
      const unit = e.depth === "advanced" ? 2 : 1;
      if (e.kind === "extract") {
        const urlCount = Array.isArray(e.urls) ? e.urls.length : 1;
        return s + Math.ceil(urlCount / 5) * unit;
      }
      return s + unit;
    }, 0),
  };

  if (jsonOut) { process.stdout.write(JSON.stringify(summary, null, 2) + "\n"); return; }

  const hitRate = summary.total_calls ? Math.round(100 * summary.cache_hits / summary.total_calls) : 0;
  const lines = [];
  lines.push(`Tavily usage - last ${daysBack} day${daysBack !== 1 ? "s" : ""}`);
  lines.push("");
  lines.push(`Total calls:        ${summary.total_calls}`);
  lines.push(`  Searches:         ${summary.searches}`);
  lines.push(`  Extracts:         ${summary.extracts}`);
  lines.push(`Cache hits:         ${summary.cache_hits} (${hitRate}%)`);
  lines.push(`Cache misses:       ${summary.cache_misses}`);
  lines.push(`Errors:             ${summary.errors}`);
  lines.push(`Estimated credits used: ${summary.credits_used}`);
  lines.push(`Est. credits avoided by cache: ${summary.estimated_credits_avoided_by_cache}`);
  process.stdout.write(lines.join("\n") + "\n");
}

// -------- subcommand: cache --------

function cmdCache(argv) {
  const sub = argv[0] || "info";
  if (sub === "clear") {
    rejectLeftovers(argv.slice(1), "cache clear");
    const result = cacheClear();
    const skipped = result.skipped ? ` (skipped ${result.skipped} non-cache entries)` : "";
    process.stdout.write(`cleared ${result.deleted} cache entries from ${CACHE_DIR}${skipped}\n`);
    return;
  }
  if (sub === "info") {
    const info = cacheInfo();
    const { value: jsonOut, rest } = consumeFlag(argv.slice(1), "--json", false);
    rejectLeftovers(rest, "cache info");
    if (jsonOut) { process.stdout.write(JSON.stringify(info, null, 2) + "\n"); return; }
    process.stdout.write(
      `Cache dir:   ${info.dir}\n` +
      `Entries:     ${info.count}\n` +
      `Total size:  ${(info.bytes / 1024).toFixed(1)} KB\n` +
      `Oldest:      ${info.oldestAgeMin === null ? "-" : info.oldestAgeMin + " min ago"}\n` +
      `Newest:      ${info.newestAgeMin === null ? "-" : info.newestAgeMin + " min ago"}\n`
    );
    return;
  }
  die(`unknown cache subcommand: ${sub}. Use 'clear' or 'info'.`);
}

// -------- help --------

function showHelp() {
  process.stdout.write(
    "Tavily Pro - research-grade web search\n" +
    "\n" +
    "Usage: tavily-pro.mjs <subcommand> [flags] [args...]\n" +
    "Note: search/extract require TAVILY_API_KEY and send queries/URLs to Tavily.\n" +
    "\n" +
    "Subcommands:\n" +
    "  search \"query\"       Search the web via Tavily\n" +
    "  extract <url> ...    Extract clean content from one or more URLs\n" +
    "  stats                Show usage stats from the log\n" +
    "  cache [info]|clear   Inspect or wipe the response cache; clear is local deletion\n" +
    "  help                 Show this message\n" +
    "\n" +
    "Search flags:\n" +
    "  --topic general|news     (default general)\n" +
    "  --depth basic|advanced   (default basic; advanced = 2 credits)\n" +
    "  --max N                  (1-20, default 5)\n" +
    "  --days N                 (news only, default 7)\n" +
    "  --include a,b,c          domains to include\n" +
    "  --exclude a,b,c          domains to exclude\n" +
    "  --raw-content            include full page text per result\n" +
    "\n" +
    "Extract flags:\n" +
    "  --depth basic|advanced   (default basic)\n" +
    "\n" +
    "Shared flags:\n" +
    "  --json                   raw JSON output\n" +
    "  --no-cache               skip cache lookup and don't write cache\n" +
    "  --no-log                 skip writing usage log\n" +
    "  --no-retry               don't retry on 429/network error\n" +
    "  --ttl SECONDS            override cache TTL; 0 disables cache reads but still writes fresh responses\n" +
    "  --timeout-ms N           per-attempt network timeout (default 30000)\n" +
    "\n" +
    "Stats flags:\n" +
    "  --days N                 look back N days (default 30)\n" +
    "\n" +
    `Data dir:  ${BASE_DIR}\n`
  );
}

// -------- main --------

async function main() {
  const [sub, ...rest] = process.argv.slice(2);
  if (!sub || sub === "help" || sub === "-h" || sub === "--help") {
    showHelp();
    return;
  }
  switch (sub) {
    case "search":  await cmdSearch(rest);  break;
    case "extract": await cmdExtract(rest); break;
    case "stats":   cmdStats(rest);         break;
    case "cache":   cmdCache(rest);         break;
    default:
      die(`unknown subcommand: ${sub}. Try 'help'.`);
  }
}

main();
