// DuckDB-over-parquet backend for the /amp chat.
//
// AMP_PARQUET_GLOB is REQUIRED — the lazy getParquetGlob() throws on first
// runtime use (not module init) if the env var is unset. Throwing at runtime
// rather than at import keeps Vercel's static "Collecting page data" pass
// from blowing up the whole build when the env var hasn't been configured
// in the Project Settings yet. The route surfaces the missing-config error
// as a normal trace[].error entry, which AmpChat renders cleanly.
//
// Future Regime B (R2/S3): a second env-driven mode where the glob is
// "s3://bucket/path/[0-9]*.parquet" plus AWS_* / S3_ENDPOINT env vars would
// just work via httpfs. Intentionally NOT wired up yet — Phase 2 is local only.
//
// The instance is cached at module scope so warm Vercel invocations re-use
// the in-memory DuckDB plus its loaded httpfs extension and object cache.

import { DuckDBInstance, type DuckDBConnection } from "@duckdb/node-api";

// Allowlist of glob-path prefixes. Rejects file://, /etc/, ../, etc.
const ALLOWED_GLOB_PREFIXES = [
  "/Volumes/",
  "/Users/",
  "s3://",
  "https://",
  "r2://",
];

function resolveParquetGlob(): string {
  const raw = process.env.AMP_PARQUET_GLOB;
  if (!raw || !raw.trim()) {
    throw new Error(
      "AMP_PARQUET_GLOB is required but not set. " +
        "Configure it to a parquet glob starting with one of: " +
        ALLOWED_GLOB_PREFIXES.join(", "),
    );
  }
  const glob = raw.trim();
  if (!ALLOWED_GLOB_PREFIXES.some((p) => glob.startsWith(p))) {
    throw new Error(
      `AMP_PARQUET_GLOB has disallowed prefix. Must start with one of: ${ALLOWED_GLOB_PREFIXES.join(", ")}`,
    );
  }
  return glob;
}

// Lazy cache. Resolves + validates on first runtime call (request time on
// Vercel, not build time). Subsequent calls reuse the resolved value.
let _cachedGlob: string | null = null;
export function getAmpParquetGlob(): string {
  if (_cachedGlob === null) _cachedGlob = resolveParquetGlob();
  return _cachedGlob;
}

// Pre-aggregated daily-stats parquet — one row per day, ~390 rows total.
// Panoramic dashboard questions ("daily count from May 2025 to June 2026")
// hit this instead of scanning all 132M settlement rows. Optional: if
// AMP_DAILY_STATS_PATH is unset, the daily_stats virtual table is
// effectively unavailable and the model will fall back to settlements.
function resolveDailyStatsPath(): string | null {
  const raw = process.env.AMP_DAILY_STATS_PATH;
  if (!raw || !raw.trim()) return null;
  const path = raw.trim();
  if (!ALLOWED_GLOB_PREFIXES.some((p) => path.startsWith(p))) {
    throw new Error(
      `AMP_DAILY_STATS_PATH has disallowed prefix. Must start with one of: ${ALLOWED_GLOB_PREFIXES.join(", ")}`,
    );
  }
  return path;
}

let _cachedDailyStats: string | null | undefined = undefined;
export function getDailyStatsPath(): string | null {
  if (_cachedDailyStats === undefined) _cachedDailyStats = resolveDailyStatsPath();
  return _cachedDailyStats;
}

const DEFAULT_ROW_LIMIT = 500;
const DEFAULT_TIMEOUT_MS = 9_000;

// SQL statements that mutate state or touch the filesystem are rejected up
// front. Only read-only analytics queries are allowed. Match on whole words to
// avoid blocking innocent column names like "created_at".
const FORBIDDEN_KEYWORDS = [
  "DROP",
  "DELETE",
  "INSERT",
  "UPDATE",
  "CREATE",
  "ALTER",
  "ATTACH",
  "DETACH",
  "COPY",
  "EXPORT",
  "IMPORT",
  "PRAGMA",
  "INSTALL",
  "LOAD",
  "SET",
  "TRUNCATE",
  "GRANT",
  "REVOKE",
  "CALL",
  "VACUUM",
];

function isUnsafe(sql: string): string | null {
  const trimmed = sql.trim().replace(/;+\s*$/, "");
  if (!trimmed) return "empty SQL";
  // Only allow statements that *start* with SELECT, WITH, or EXPLAIN.
  if (!/^\s*(SELECT|WITH|EXPLAIN)\b/i.test(trimmed)) {
    return "Only SELECT / WITH / EXPLAIN statements are allowed.";
  }
  // No semicolons allowed mid-string — prevents stacking a second statement.
  if (trimmed.includes(";")) {
    return "Multiple statements are not allowed.";
  }
  // Word-boundary check against forbidden keywords.
  const upper = trimmed.toUpperCase();
  for (const kw of FORBIDDEN_KEYWORDS) {
    const re = new RegExp(`\\b${kw}\\b`, "i");
    if (re.test(upper)) {
      return `Disallowed keyword: ${kw}`;
    }
  }
  return null;
}

let instancePromise: Promise<DuckDBInstance> | null = null;
let initPromise: Promise<DuckDBConnection> | null = null;

async function getInstance(): Promise<DuckDBInstance> {
  if (!instancePromise) {
    instancePromise = DuckDBInstance.create(":memory:", {
      // Keep the default thread count; Vercel's small footprint means
      // DuckDB picks something reasonable. Override here if needed.
    });
  }
  return instancePromise;
}

async function getConnection(): Promise<DuckDBConnection> {
  if (!initPromise) {
    initPromise = (async () => {
      const instance = await getInstance();
      const conn = await instance.connect();
      // Vercel's serverless FS is read-only except /tmp. DuckDB needs a writable
      // home + extension dir to install httpfs at runtime.
      try {
        await conn.run("SET home_directory='/tmp'");
        await conn.run("SET extension_directory='/tmp/duckdb_extensions'");
      } catch {
        // ignore — local dev doesn't need /tmp
      }
      try {
        await conn.run("INSTALL httpfs");
      } catch {
        // ignore — extension may already be installed
      }
      try {
        await conn.run("LOAD httpfs");
      } catch {
        // ignore — extension may already be loaded
      }
      try {
        await conn.run("SET enable_object_cache=true");
      } catch {
        // ignore — older DuckDB versions might not have this knob
      }
      // DuckDB's httpfs does NOT honor AWS_* env vars — they're for the AWS
      // SDK. We have to push the S3 config into DuckDB's own settings. R2
      // requires path-style URLs (vhost style fails for bucket-scoped tokens).
      const accessKey = process.env.AWS_ACCESS_KEY_ID;
      const secretKey = process.env.AWS_SECRET_ACCESS_KEY;
      const endpoint = process.env.AWS_ENDPOINT_URL;
      const region = process.env.AWS_REGION || "auto";
      if (accessKey && secretKey && endpoint) {
        const host = endpoint.replace(/^https?:\/\//, "");
        const esc = (s: string) => s.replace(/'/g, "''");
        try {
          await conn.run(`SET s3_endpoint='${esc(host)}'`);
          await conn.run(`SET s3_access_key_id='${esc(accessKey)}'`);
          await conn.run(`SET s3_secret_access_key='${esc(secretKey)}'`);
          await conn.run(`SET s3_region='${esc(region)}'`);
          await conn.run("SET s3_url_style='path'");
          await conn.run("SET s3_use_ssl=true");
        } catch (e) {
          // Loud — without this, every query 500s with an opaque parquet error.
          console.error("[duck] S3 config failed:", e instanceof Error ? e.message : String(e));
        }
      }
      return conn;
    })();
  }
  return initPromise;
}

// Convert BigInt / decimal-ish values inside row objects to strings so the
// result survives JSON.stringify. DuckDB returns BigInts for UBIGINT, and
// Decimal-shaped objects for DECIMAL(38,0). Dates are returned as Date
// instances — turn those into ISO strings for stable wire format.
function jsonSafe(value: unknown): unknown {
  if (value === null || value === undefined) return value;
  if (typeof value === "bigint") return value.toString();
  if (value instanceof Date) return value.toISOString();
  if (Array.isArray(value)) return value.map(jsonSafe);
  if (typeof value === "object") {
    // DuckDB Decimal128 / similar shape: { value: bigint, scale: number, width: number }
    const v = value as Record<string, unknown>;
    if (typeof v.value === "bigint" && typeof v.scale === "number") {
      const raw = v.value as bigint;
      const scale = v.scale as number;
      if (scale === 0) return raw.toString();
      const s = raw.toString();
      const neg = s.startsWith("-");
      const digits = neg ? s.slice(1) : s;
      const padded = digits.padStart(scale + 1, "0");
      const cut = padded.length - scale;
      const out = padded.slice(0, cut) + "." + padded.slice(cut);
      return (neg ? "-" : "") + out;
    }
    const out: Record<string, unknown> = {};
    for (const k of Object.keys(v)) out[k] = jsonSafe(v[k]);
    return out;
  }
  return value;
}

export interface RunSqlResult {
  rows: Record<string, unknown>[];
  error?: string;
  ms: number;
  truncated?: boolean;
}

// Map a raw DuckDB error message to a short generic category for client display.
// The full error is logged to server console.error in the caller. We classify on
// known DuckDB prefixes (Binder, Catalog, Parser, IO, Conversion, Out of Memory)
// and fall back to "query rejected: error" for anything else.
function sanitizeDuckError(raw: string): string {
  const m = /^([A-Z][A-Za-z ]+? Error)\b/.exec(raw);
  if (m) {
    return `query rejected: ${m[1].toLowerCase()}`;
  }
  return "query rejected: error";
}

export interface RunSqlOptions {
  rowLimit?: number;
  timeoutMs?: number;
}

export async function runSql(
  sql: string,
  options: RunSqlOptions = {},
): Promise<RunSqlResult> {
  const t0 = Date.now();
  const rowLimit = options.rowLimit ?? DEFAULT_ROW_LIMIT;
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  const unsafe = isUnsafe(sql);
  if (unsafe) {
    return { rows: [], error: unsafe, ms: Date.now() - t0 };
  }

  let conn: DuckDBConnection;
  try {
    conn = await getConnection();
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    console.error("[duck] init failed:", msg);
    return { rows: [], error: "query rejected: init failed", ms: Date.now() - t0 };
  }

  const cleanedSql = sql.trim().replace(/;+\s*$/, "");

  let timer: ReturnType<typeof setTimeout> | undefined;
  const timeout = new Promise<RunSqlResult>((resolve) => {
    timer = setTimeout(() => {
      resolve({
        rows: [],
        error: `Query timed out after ${timeoutMs}ms`,
        ms: Date.now() - t0,
      });
    }, timeoutMs);
  });

  const query: Promise<RunSqlResult> = (async () => {
    try {
      const reader = await conn.runAndReadAll(cleanedSql);
      const rawRows = reader.getRowObjects() as Record<string, unknown>[];
      const truncated = rawRows.length > rowLimit;
      const limited = truncated ? rawRows.slice(0, rowLimit) : rawRows;
      const safe = limited.map((r) => jsonSafe(r) as Record<string, unknown>);
      return {
        rows: safe,
        ms: Date.now() - t0,
        truncated: truncated || undefined,
      };
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      console.error("[duck] query failed:", msg, "\nSQL:", cleanedSql);
      return { rows: [], error: sanitizeDuckError(msg), ms: Date.now() - t0 };
    }
  })();

  try {
    return await Promise.race([query, timeout]);
  } finally {
    if (timer) clearTimeout(timer);
  }
}
