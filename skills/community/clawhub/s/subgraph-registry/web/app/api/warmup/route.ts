import { runSql, getAmpParquetGlob } from "@/lib/duck";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

// Cron-friendly keep-warm endpoint. A scheduled GitHub Action pings this
// every 5 minutes so the Vercel lambda's DuckDB instance + httpfs extension
// + parquet footer cache stay resident — eliminating the ~30s cold-start
// users would otherwise see on the first /api/ask request after idle time.
//
// The query intentionally touches the parquet glob (not just SELECT 1) so
// DuckDB re-reads at least one file's footer; with enable_object_cache=true
// that primes the cache for the real queries that follow.
//
// Returns 200 with timing JSON on success; 503 if the glob isn't configured;
// anything else is the underlying DuckDB error surfaced verbatim. Designed
// to be cheap (<1s warm, <10s cold) and harmless to call repeatedly.
export async function GET() {
  const t0 = Date.now();

  let glob: string;
  try {
    glob = getAmpParquetGlob();
  } catch (e) {
    return Response.json(
      { ok: false, error: e instanceof Error ? e.message : "glob not configured" },
      { status: 503 },
    );
  }

  const sql = `SELECT 1 AS ping FROM read_parquet('${glob.replace(/'/g, "''")}') LIMIT 1`;
  const result = await runSql(sql, { timeoutMs: 20_000 });

  return Response.json({
    ok: !result.error,
    sql_ms: result.ms,
    total_ms: Date.now() - t0,
    error: result.error,
  });
}
