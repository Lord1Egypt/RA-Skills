// The rfind crawler, shared by the CLI (rfind.mjs) and the MCP server
// (mcp.mjs). Headless port of grtwrn/recursive-find (worker.js + kmp.js):
// fetch a page, strip it to text, search it, follow its links breadth-first
// to `depth`, and return only the pages that match. Never writes to stdout.

import { Worker } from "node:worker_threads";
import { decodeBody, normalizeUrl } from "./page.mjs";

export {
  decodeBody, decodeEntities, extractLinks, findMatches, foldCase, htmlToText, mainContent,
  normalizeUrl, pageTitle, processPage, searchText, sniffEncoding,
} from "./page.mjs";

export const MAX_BODY_BYTES = 32 * 1024 * 1024;
export const DEFAULTS = {
  depth: 1, maxPages: 100, mode: "text", caseSensitive: false, anySite: false,
  within: null, mainOnly: false, first: false, limit: 20, snippets: 3, concurrency: 4,
  timeout: 10, maxSeconds: 120, robots: true, maxBodyBytes: MAX_BODY_BYTES,
};

const MAX_ERRORS_SHOWN = 20;
const MAX_RETRY_AFTER_MS = 10_000;
const DEFAULT_RETRY_MS = 1000;
const ROBOTS_MAX_BYTES = 512 * 1024;
const UA = "rfind/1.0 (+https://github.com/grtwrn/recursive-find)";

// --- options ---

// Fill in defaults, clamp numbers to their caps, and validate url/mode/query.
// Throws an Error with a user-facing message on bad input. Idempotent.
export function resolveOptions(input) {
  const opts = { ...DEFAULTS };
  for (const [k, v] of Object.entries(input)) if (v !== undefined && v !== null) opts[k] = v;
  const num = (name) => {
    const n = Number(opts[name]);
    if (!Number.isFinite(n) || n < 0) throw new Error(`bad value for ${name}: ${opts[name]}`);
    return Math.floor(n);
  };
  const clamp = (name, lo, hi) => Math.max(lo, Math.min(hi, num(name)));
  opts.depth = clamp("depth", 0, 3);
  opts.maxPages = clamp("maxPages", 1, 1000);
  opts.limit = clamp("limit", 1, Infinity);
  opts.snippets = num("snippets");
  opts.concurrency = clamp("concurrency", 1, 8);
  opts.timeout = clamp("timeout", 1, Infinity);
  opts.maxSeconds = clamp("maxSeconds", 1, Infinity);
  opts.maxBodyBytes = clamp("maxBodyBytes", 1, Infinity);
  // A path prefix as URL.pathname spells it: leading "/", non-ASCII
  // percent-encoded (so "/café/" matches); a full URL means its path.
  opts.within = opts.within ? new URL(String(opts.within), "http://x/").pathname : null;

  let url = String(opts.url ?? "").trim();
  if (!/^https?:\/\//i.test(url)) url = "https://" + url;
  let parsed;
  try { parsed = new URL(url); } catch { throw new Error(`bad url: ${url}`); }
  if (parsed.username || parsed.password) throw new Error("URLs with a username or password aren't supported");
  opts.url = parsed.href;
  if (!["text", "word", "regex"].includes(opts.mode)) throw new Error("mode must be text, word or regex");
  if (!opts.query) throw new Error("empty query");
  opts.query = String(opts.query);
  if (opts.mode === "regex") {
    try { new RegExp(opts.query); } catch (e) { throw new Error(`invalid regex: ${e.message}`); }
  }
  return opts;
}

// --- fetching ---

// Resolves after `ms`, or rejects as soon as `signal` aborts.
function sleep(ms, signal) {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) return reject(new Error("deadline"));
    const onAbort = () => {
      clearTimeout(timer);
      reject(new Error("deadline"));
    };
    const timer = setTimeout(() => {
      signal?.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    signal?.addEventListener("abort", onAbort, { once: true });
  });
}

// Retry-After in ms (delay-seconds or an HTTP date), or null.
export function retryAfterMs(value, now = Date.now()) {
  if (!value) return null;
  if (/^\s*\d+\s*$/.test(value)) return Number(value) * 1000;
  const t = Date.parse(value);
  return Number.isNaN(t) ? null : Math.max(0, t - now);
}

// "fetch failed" says nothing; undici puts the reason (DNS, TLS, refused,
// redirect loop…) in `cause`.
function describeFetchError(e) {
  const cause = e?.cause;
  if (e?.message === "fetch failed" && cause) {
    const why = cause.code && cause.code !== "UND_ERR" ? cause.code : cause.message;
    return `fetch failed: ${why || "network error"}`;
  }
  return (e?.message || String(e)).replace(/\/\/[^/@\s]*@/g, "//"); // never echo credentials
}

// Fetches a page's body as bytes (decoded later, by its declared charset).
// `signal` aborts from outside (the crawl deadline); the error is then
// "deadline" instead of "timeout". A 429 or 503 is retried once after its
// Retry-After (at most 10 s; 1 s if absent); `pauses` (origin -> time) makes
// the other fetches to that origin wait too. The timeout covers each attempt.
export async function fetchPage(url, timeoutMs, { signal, maxBodyBytes = MAX_BODY_BYTES, pauses } = {}) {
  const origin = new URL(url).origin;
  for (let attempt = 0; ; attempt++) {
    const wait = (pauses?.get(origin) ?? 0) - Date.now();
    if (wait > 0) await sleep(wait, signal);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    const onAbort = () => controller.abort();
    if (signal?.aborted) controller.abort();
    else signal?.addEventListener("abort", onAbort, { once: true });
    try {
      const res = await fetch(url, {
        signal: controller.signal,
        redirect: "follow",
        headers: { "user-agent": UA, accept: "text/html,application/xhtml+xml,text/plain;q=0.9" },
      });
      if (!res.ok) {
        res.body?.cancel().catch(() => {});
        let msg = `HTTP ${res.status}`;
        if (res.status === 429 || res.status === 503) {
          const after = retryAfterMs(res.headers.get("retry-after"));
          if (attempt === 0 && (after === null || after <= MAX_RETRY_AFTER_MS)) {
            const ms = after ?? DEFAULT_RETRY_MS;
            pauses?.set(origin, Math.max(pauses.get(origin) ?? 0, Date.now() + ms));
            clearTimeout(timer);
            await sleep(ms, signal);
            continue;
          }
          msg += attempt ? " (also after a retry)" : `, Retry-After ${Math.round(after / 1000)}s (not retried)`;
        }
        throw new Error(msg);
      }
      const type = res.headers.get("content-type") || "";
      if (type && !/text\/html|text\/plain|application\/xhtml/i.test(type)) {
        res.body?.cancel().catch(() => {});
        throw Object.assign(new Error(`skipped ${type.split(";")[0]}`), { skipped: true });
      }
      const chunks = [];
      let size = 0;
      let truncated = false;
      if (res.body) {
        const reader = res.body.getReader();
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          size += value.length;
          chunks.push(value);
          if (size > maxBodyBytes) {
            truncated = true;
            reader.cancel().catch(() => {});
            break;
          }
        }
      }
      // One exact-size buffer of our own, so it can be transferred to a worker.
      const bytes = new Uint8Array(size);
      let at = 0;
      for (const c of chunks) {
        bytes.set(c, at);
        at += c.length;
      }
      return { bytes, contentType: type, finalUrl: res.url || url, truncated };
    } catch (e) {
      if (e?.name === "AbortError" || controller.signal.aborted) {
        throw new Error(signal?.aborted ? "deadline" : "timeout");
      }
      if (e?.skipped || /^HTTP /.test(e?.message)) throw e;
      throw new Error(describeFetchError(e));
    } finally {
      clearTimeout(timer);
      signal?.removeEventListener("abort", onAbort);
    }
  }
}

// Fetches a page and decodes it as text (for robots.txt and callers that
// want the old string API).
export async function fetchHtml(url, timeoutMs, opts) {
  const { bytes, contentType, finalUrl, truncated } = await fetchPage(url, timeoutMs, opts);
  return { html: decodeBody(bytes, contentType), finalUrl, truncated };
}

// Minimal robots.txt: Disallow/Allow rules in the "User-agent: *" (or rfind)
// groups, longest match wins. Unreachable robots.txt = allow everything.
export function parseRobots(txt) {
  const rules = [];
  let agents = [];
  let inRules = false;
  for (let line of txt.split(/\r\n?|\n/)) {
    const hash = line.indexOf("#");
    if (hash !== -1) line = line.slice(0, hash);
    const colon = line.indexOf(":");
    if (colon === -1) continue;
    const key = line.slice(0, colon).trim().toLowerCase();
    if (!/^[a-z-]+$/.test(key)) continue;
    const val = line.slice(colon + 1).trim();
    if (key === "user-agent") {
      if (inRules) { agents = []; inRules = false; }
      agents.push(val.toLowerCase());
    } else if (key === "allow" || key === "disallow") {
      inRules = true;
      if (val && agents.some((a) => a === "*" || a.includes("rfind"))) {
        rules.push({ allow: key === "allow", path: val });
      }
    }
  }
  return rules;
}

// Does a robots.txt path pattern match? "*" is any run of characters and a
// final "$" anchors the end. Matched piece by piece (no RegExp), so a
// hostile pattern like "/*a*a*a*a*a*b" can't backtrack for minutes.
function robotsMatch(pattern, path) {
  const anchored = pattern.endsWith("$");
  const pieces = (anchored ? pattern.slice(0, -1) : pattern).split("*");
  if (!path.startsWith(pieces[0])) return false;
  if (pieces.length === 1) return !anchored || path.length === pieces[0].length;
  let at = pieces[0].length;
  const last = pieces.length - 1;
  for (let i = 1; i < last; i++) {
    const found = path.indexOf(pieces[i], at);
    if (found === -1) return false;
    at = found + pieces[i].length;
  }
  if (!anchored) return path.indexOf(pieces[last], at) !== -1;
  return path.length - pieces[last].length >= at && path.endsWith(pieces[last]);
}

export function robotsAllows(rules, url) {
  const u = new URL(url);
  const path = u.pathname + u.search;
  let best = null;
  for (const r of rules) {
    if (robotsMatch(r.path, path) && (!best || r.path.length > best.path.length)) best = r;
  }
  return !best || best.allow;
}

// --- page processing in worker threads ---

const WORKER_URL = new URL("./page-worker.mjs", import.meta.url);
// Caps a worker's heap so one page can't take the whole process down.
const WORKER_LIMITS = { maxOldGenerationSizeMb: 1024 };

// Runs processPage (page.mjs) in worker threads, at most one page per worker,
// started as needed. A page that takes longer than `timeoutMs` has its worker
// terminated, which stops even a regex stuck in catastrophic backtracking.
class PagePool {
  idle = [];
  busy = new Set();
  closed = false;

  process(job, timeoutMs, timeoutMessage) {
    if (this.closed) return Promise.reject(new Error("deadline"));
    const worker = this.idle.pop() || new Worker(WORKER_URL, { resourceLimits: WORKER_LIMITS });
    return new Promise((resolve, reject) => {
      const entry = {};
      const settle = (reuse, fn, value) => {
        clearTimeout(timer);
        worker.off("message", onMessage).off("error", onError).off("exit", onExit);
        this.busy.delete(entry);
        if (reuse && !this.closed) this.idle.push(worker);
        else worker.terminate().catch(() => {});
        fn(value);
      };
      const onMessage = (m) => (m.ok ? settle(true, resolve, m.result) : settle(true, reject, new Error(m.error)));
      const onError = (e) =>
        settle(false, reject, new Error(e?.code === "ERR_WORKER_OUT_OF_MEMORY" ? "page too large to search (out of memory)" : e?.message || String(e)));
      const onExit = () => settle(false, reject, new Error("page worker exited"));
      const timer = setTimeout(() => settle(false, reject, new Error(timeoutMessage)), timeoutMs);
      entry.kill = () => settle(false, reject, new Error("deadline"));
      this.busy.add(entry);
      worker.on("message", onMessage).on("error", onError).on("exit", onExit);
      worker.postMessage(job, [job.bytes.buffer]);
    });
  }

  close() {
    this.closed = true;
    for (const entry of [...this.busy]) entry.kill();
    for (const w of this.idle.splice(0)) w.terminate().catch(() => {});
  }
}

// --- crawl ---

// Crawl and search. Returns { summary, hits, errors } with every hit and error
// (use toJSON / formatText to apply `limit`). Throws only on bad options.
export async function crawl(input) {
  const opts = resolveOptions(input);
  const timeoutMs = opts.timeout * 1000;
  // Same site = the start URL's origin, plus the origin it redirects to
  // (example.com -> www.example.com), whose links are all on the new origin.
  const origins = new Set([new URL(opts.url).origin]);
  const deadline = new AbortController();
  const fetchOpts = { signal: deadline.signal, maxBodyBytes: opts.maxBodyBytes, pauses: new Map() };
  const pool = new PagePool();
  const searchTimeout = opts.mode === "regex"
    ? `regex search took over ${opts.timeout}s on this page (catastrophic backtracking?), page skipped`
    : `searching the page took over ${opts.timeout}s, page skipped`;
  const t0 = Date.now();

  const robotsCache = new Map();
  const robotsFor = (origin) => {
    if (!robotsCache.has(origin)) {
      robotsCache.set(origin, (async () => {
        try {
          const robotsOpts = { ...fetchOpts, maxBodyBytes: ROBOTS_MAX_BYTES };
          const { html } = await fetchHtml(origin + "/robots.txt", Math.min(timeoutMs, 5000), robotsOpts);
          return parseRobots(html);
        } catch {
          return [];
        }
      })());
    }
    return robotsCache.get(origin);
  };

  const allowed = (href) => {
    try {
      const u = new URL(href);
      if (!opts.anySite && !origins.has(u.origin)) return false;
      if (opts.within && !u.pathname.startsWith(opts.within)) return false;
      return true;
    } catch {
      return false;
    }
  };

  const visited = new Set([normalizeUrl(opts.url)]);
  const fetched = new Set(); // final URLs, after redirects
  const queue = [{ url: opts.url, depth: 0 }];
  const hits = [];
  const errors = [];
  const truncatedPages = [];
  let start = null; // what the start page looked like, for the JS-rendering hint
  let scanned = 0;
  let blocked = 0;
  let skipped = 0;
  let capped = false;
  let timedOut = false;
  let stopped = false;
  let firstHit = false;
  let active = 0;
  let queued = 1; // pages queued for fetching, start page included

  try {
    await new Promise((resolve) => {
      let graceTimer;
      const finish = () => {
        clearTimeout(deadlineTimer);
        clearTimeout(graceTimer);
        resolve();
      };
      // --max-seconds: stop queueing, abort in-flight fetches and searches, and
      // give them a moment to unwind; resolve regardless so the crawl can never hang.
      const deadlineTimer = setTimeout(() => {
        timedOut = true;
        stopped = true;
        queue.length = 0;
        deadline.abort();
        pool.close();
        graceTimer = setTimeout(finish, 1000);
      }, opts.maxSeconds * 1000);

      const pump = () => {
        if (stopped) queue.length = 0;
        while (active < opts.concurrency && queue.length) {
          const job = queue.shift();
          active++;
          visit(job).finally(() => {
            active--;
            pump();
          });
        }
        if (active === 0 && queue.length === 0) finish();
      };

      const visit = async ({ url, depth }) => {
        try {
          if (opts.robots) {
            const rules = await robotsFor(new URL(url).origin);
            if (!robotsAllows(rules, url)) {
              blocked++;
              return;
            }
          }
          const { bytes, contentType, finalUrl, truncated } = await fetchPage(url, timeoutMs, fetchOpts);
          if (truncated) truncatedPages.push(finalUrl);
          if (stopped) return;
          // Two links that redirect to the same page: search it once.
          const finalKey = normalizeUrl(finalUrl);
          if (fetched.has(finalKey)) return;
          fetched.add(finalKey);
          visited.add(finalKey);
          if (depth === 0) {
            try { origins.add(new URL(finalUrl).origin); } catch { /* keep the start origin */ }
          }
          const page = await pool.process({
            bytes, contentType, url: finalUrl, query: opts.query, mode: opts.mode,
            caseSensitive: opts.caseSensitive, snippets: opts.snippets, mainOnly: opts.mainOnly,
            links: depth < opts.depth && !stopped,
          }, timeoutMs, searchTimeout);
          if (firstHit) return; // another page already answered (--first)
          scanned++;
          if (depth === 0) start = { textLength: page.textLength, hasScripts: page.hasScripts };
          if (page.matchCount > 0) {
            hits.push({
              url: finalUrl, title: page.title, depth, matchCount: page.matchCount, snippets: page.snippets,
              ...(truncated && { truncated }),
            });
            if (opts.first) stopped = firstHit = true;
          }
          if (depth < opts.depth && !stopped) {
            for (const href of page.links) {
              if (timedOut) break;
              const n = normalizeUrl(href);
              if (visited.has(n) || !allowed(href)) continue;
              visited.add(n);
              // Check robots before queueing so blocked links don't use up --max-pages.
              if (opts.robots && !robotsAllows(await robotsFor(new URL(href).origin), href)) {
                blocked++;
                continue;
              }
              if (queued >= opts.maxPages) {
                capped = true;
                break;
              }
              queued++;
              queue.push({ url: href, depth: depth + 1 });
            }
          }
        } catch (e) {
          if (timedOut) {
            // Pages cut off by the deadline aren't errors, unless it's the start page.
            if (depth === 0) {
              scanned++;
              errors.push({ url, depth, error: `deadline: no response within ${opts.maxSeconds}s` });
            }
            return;
          }
          if (e?.skipped && depth > 0) {
            skipped++; // a non-HTML link (PDF, markdown, image…), not a failure
            return;
          }
          scanned++;
          errors.push({ url, depth, error: e?.message || String(e) });
        }
      };

      pump();
    });
  } finally {
    pool.close();
  }

  hits.sort((a, b) => b.matchCount - a.matchCount || a.depth - b.depth);
  const summary = {
    query: opts.query, start: opts.url, depth: opts.depth, mode: opts.mode,
    pagesScanned: scanned, pagesWithHits: hits.length,
    totalHits: hits.reduce((s, h) => s + h.matchCount, 0),
    errors: errors.length, skippedNonHtml: skipped, robotsBlocked: blocked, capped, timedOut,
    truncatedPages, stoppedAtFirst: firstHit,
    seconds: +((Date.now() - t0) / 1000).toFixed(1),
  };
  return { summary, hits, errors };
}

// The start page's error, if it failed (CLI exit code 1, MCP isError).
export function startError(result) {
  return result.errors.find((e) => e.depth === 0) || null;
}

export function toJSON({ summary, hits, errors }, opts) {
  return { summary, hits: hits.slice(0, opts.limit), errors: errors.slice(0, MAX_ERRORS_SHOWN) };
}

// Option names as they appear in the summary line ("hit --max-pages 100").
export const CLI_NAMES = { maxPages: "--max-pages", maxSeconds: "--max-seconds", limit: "--limit" };

// Compact text report: a summary line, then each matching page with snippets.
export function formatText(result, opts, names = CLI_NAMES) {
  const { summary, hits } = result;
  const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;
  const maxBodyBytes = opts.maxBodyBytes ?? MAX_BODY_BYTES;
  const size = maxBodyBytes % (1 << 20) === 0 ? `${maxBodyBytes >> 20} MB` : `${maxBodyBytes} bytes`;
  const lines = [];
  let line = `${plural(summary.totalHits, "hit")} on ${plural(summary.pagesWithHits, "page")} · ${plural(summary.pagesScanned, "page")} scanned, depth ${summary.depth}, ${summary.seconds}s`;
  if (summary.errors) line += ` · ${plural(summary.errors, "error")}`;
  if (summary.skippedNonHtml) line += ` · ${summary.skippedNonHtml} non-HTML links skipped`;
  if (summary.robotsBlocked) line += ` · ${summary.robotsBlocked} blocked by robots.txt`;
  if (summary.capped) line += ` · hit ${names.maxPages} ${opts.maxPages}, results may be incomplete`;
  if (summary.timedOut) line += ` · hit ${names.maxSeconds} ${opts.maxSeconds}, results may be incomplete`;
  if (summary.truncatedPages.length) {
    line += ` · ${plural(summary.truncatedPages.length, "page")} over ${size} only partly searched: ${summary.truncatedPages.join(", ")}`;
  }
  if (summary.stoppedAtFirst) line += " · stopped at first hit";
  lines.push(line);
  for (const h of hits.slice(0, opts.limit)) {
    lines.push(`\n${h.matchCount}× ${h.url}${h.title ? `  — ${h.title}` : ""}`);
    for (const s of h.snippets) lines.push(`   ${s}`);
  }
  if (hits.length > opts.limit) lines.push(`\n… ${hits.length - opts.limit} more matching pages (raise ${names.limit})`);
  const failed = startError(result);
  if (failed) lines.push(`\nstart page failed: ${failed.error}`);
  return lines.join("\n");
}
