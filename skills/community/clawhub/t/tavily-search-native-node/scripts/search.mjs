#!/usr/bin/env node
// tavily-search-native-node/scripts/search.mjs
// Cost-effective Tavily web search for OpenClaw - minimal reference implementation.
// Usage: node search.mjs [flags] "query"
// Requires Node 18+ (uses native fetch). Reads TAVILY_API_KEY from the process environment only.

const ENDPOINT = "https://api.tavily.com/search";
const DEFAULT_TIMEOUT_MS = 30000;

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
  warn("using TAVILY_API_KEY from process environment");
  return value;
}

function parseArgs(argv) {
  const out = {
    topic: "general",
    depth: "basic",
    max: 5,
    days: 7,
    include: [],
    exclude: [],
    json: false,
    query: "",
  };
  const stringFlags = new Set(["--topic", "--depth", "--max", "--days", "--include", "--exclude"]);
  const leftovers = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") { out.json = true; continue; }
    if (a === "-h" || a === "--help") {
      process.stdout.write(
        "Usage: search.mjs [flags] \"query\"\n" +
        "\n" +
        "Flags:\n" +
        "  --topic general|news     (default general)\n" +
        "  --depth basic|advanced   (default basic; advanced = 2 credits)\n" +
        "  --max N                  (1-20, default 5)\n" +
        "  --days N                 (1-365, news only, default 7)\n" +
        "  --include a,b,c          domains to include\n" +
        "  --exclude a,b,c          domains to exclude\n" +
        "  --json                   redacted JSON output\n" +
        "\n" +
        "Env: TAVILY_TEST_ENDPOINT is local-test-only; use dummy keys because it receives Authorization.\n" +
        "\n" +
        "For caching, raw-content, extract, and stats, use a separately reviewed Pro Tavily skill/package when available.\n"
      );
      process.exit(0);
    }
    if (stringFlags.has(a)) {
      const v = argv[++i];
      if (v === undefined) die(`flag ${a} needs a value`);
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
          if (!Number.isInteger(n) || n < 1 || n > 365) die(`--days must be 1-365`);
          out.days = n; break;
        }
        case "--include":
          out.include = v.split(",").map(s => s.trim()).filter(Boolean); break;
        case "--exclude":
          out.exclude = v.split(",").map(s => s.trim()).filter(Boolean); break;
      }
      continue;
    }
    if (a.startsWith("--")) die(`unknown flag ${a}`);
    leftovers.push(a);
  }
  out.query = leftovers.join(" ").trim();
  if (!out.query) die("missing query. Example: search.mjs \"latest AI news\"");
  return out;
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

function redactSecret(text, secret) {
  const value = String(text || "");
  if (!secret) return value;
  return value.split(secret).join("[redacted]");
}

function redactValue(value, secret) {
  if (!secret) return value;
  if (typeof value === "string") return redactSecret(value, secret);
  if (Array.isArray(value)) return value.map((item) => redactValue(item, secret));
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [redactSecret(key, secret), redactValue(item, secret)]));
  }
  return value;
}

function isDummyLocalTestKey(value) {
  const key = String(value || "").trim().toLowerCase();
  return /^(test|dummy|fake|local|example)[-_]/.test(key)
    || /(^|[-_])(test|dummy|fake|local|example|not[-_]?real|do[-_]?not[-_]?(?:print|use))([-_]|$)/.test(key);
}

function formatHuman(resp, args, elapsedMs, secret) {
  const lines = [];
  lines.push(`Query: ${redactSecret(args.query, secret)}`);
  lines.push(`Topic: ${args.topic} - Depth: ${args.depth} - Results: ${(resp.results || []).length}/${args.max}`);
  if (resp.answer) {
    lines.push("");
    lines.push("Answer:");
    lines.push(truncate(redactSecret(String(resp.answer).trim(), secret), 1200));
  }
  lines.push("");
  lines.push("Results:");
  (resp.results || []).forEach((r, i) => {
    lines.push(`${i + 1}. ${redactSecret(r.title || "(no title)", secret)}`);
    lines.push(`   ${redactSecret(r.url || "", secret)}`);
    if (r.published_date) lines.push(`   published: ${redactSecret(r.published_date, secret)}`);
    if (r.content) lines.push(`   ${truncate(redactSecret(String(r.content).replace(/\s+/g, " ").trim(), secret), 280)}`);
  });
  lines.push("");
  const parts = [`elapsed ${elapsedMs}ms`];
  if (resp.response_time) parts.push(`api ${redactSecret(resp.response_time, secret)}s`);
  lines.push(`- ${parts.join(" - ")}`);
  return asciiSafe(lines.join("\n"));
}

function timeoutMs() {
  const raw = (process.env.TAVILY_TIMEOUT_MS || "").trim();
  if (!raw) return DEFAULT_TIMEOUT_MS;
  const n = Number(raw);
  if (!Number.isInteger(n) || n < 1000 || n > 120000) die("TAVILY_TIMEOUT_MS must be an integer from 1000 to 120000");
  return n;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const apiKey = loadApiKey();
  const timeout = timeoutMs();

  const endpoint = process.env.TAVILY_TEST_ENDPOINT || ENDPOINT;
  if (endpoint !== ENDPOINT) {
    let parsed;
    try { parsed = new URL(endpoint); }
    catch { die("TAVILY_TEST_ENDPOINT must be a valid local test URL"); }
    if (parsed.protocol !== "http:" || parsed.hostname !== "127.0.0.1" || parsed.username || parsed.password || !parsed.port) {
      die("TAVILY_TEST_ENDPOINT is only allowed for local 127.0.0.1 tests");
    }
    if (!isDummyLocalTestKey(apiKey)) {
      die("TAVILY_TEST_ENDPOINT requires a clearly dummy/local/test TAVILY_API_KEY; refusing to send a possible real credential to a test endpoint");
    }
  }
  const body = {
    query: args.query,
    topic: args.topic,
    search_depth: args.depth,
    max_results: args.max,
    include_answer: true,
    include_raw_content: false,
    include_images: false,
  };
  if (args.topic === "news") body.days = args.days;
  if (args.include.length) body.include_domains = args.include;
  if (args.exclude.length) body.exclude_domains = args.exclude;

  const started = Date.now();
  let resp;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    resp = await fetch(endpoint, {
      method: "POST",
      redirect: "manual",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
  } catch (e) {
    if (e?.name === "AbortError") die(`network timeout after ${timeout}ms`);
    die(`network error: ${e.message || e}`);
  }

  const elapsed = Date.now() - started;
  if (resp.status >= 300 && resp.status < 400) {
    clearTimeout(timer);
    die(`HTTP ${resp.status}: redirect refused; not following provider/test endpoint redirects to preserve outbound destination boundary`);
  }
  let text;
  try {
    text = await resp.text();
  } catch (e) {
    if (e?.name === "AbortError") die(`network timeout after ${timeout}ms`);
    die(`response read error: ${e.message || e}`);
  } finally {
    clearTimeout(timer);
  }

  if (!resp.ok) {
    let detail = text;
    try { const j = JSON.parse(text); detail = j.detail || j.error || text; } catch {}
    const retry = resp.headers.get("retry-after");
    const safeRetry = retry ? redactSecret(retry, apiKey).slice(0, 120) : "";
    const retryHint = safeRetry ? ` (retry-after: ${safeRetry})` : "";
    die(`HTTP ${resp.status}${retryHint}: ${redactSecret(String(detail), apiKey).slice(0, 500)}`);
  }

  let data;
  try { data = JSON.parse(text); }
  catch { die(`invalid JSON response: ${redactSecret(text, apiKey).slice(0, 300)}`); }

  const safeData = redactValue(data, apiKey);
  if (args.json) {
    process.stdout.write(JSON.stringify(safeData, null, 2) + "\n");
    return;
  }
  process.stdout.write(formatHuman(safeData, args, elapsed, apiKey) + "\n");
}

main().catch((e) => die(e?.message || String(e)));
