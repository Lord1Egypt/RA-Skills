import Anthropic from "@anthropic-ai/sdk";
import { getAmpParquetGlob, getDailyStatsPath, runSql } from "@/lib/duck";
import { SYSTEM_PROMPT } from "@/lib/ampSchema";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
// Vercel hobby tier caps at 10s; Pro at 60s. Setting maxDuration=60 unlocks
// Pro's headroom and is a no-op on hobby (silently clamped to 10s).
export const maxDuration = 60;

// Sonnet is fast enough that interactive chat feels responsive; Opus is overkill
// for SQL translation. Override via AMP_MODEL env if you want to A/B.
const MODEL = process.env.AMP_MODEL || "claude-sonnet-4-6";

// Wall-clock budget for the whole request. Cold parquet scans across ~1k
// files in R2 need ~5-10s just for footer fetches; allow ~50s for the full
// model-loop + scan, leaving 10s of platform headroom.
const TOTAL_BUDGET_MS = 50_000;
const MAX_TURNS = 6;

interface AskRequest {
  question: string;
}

interface ToolUse {
  type: "tool_use";
  id: string;
  name: string;
  input: Record<string, unknown>;
}

interface TraceStep {
  sql: string;
  ms: number;
  rows?: number;
  error?: string;
}

// The model writes "FROM settlements" or "FROM daily_stats"; we rewrite each
// to a read_parquet call pointing at the configured path. Case-insensitive,
// also handles "from   settlements".
//
// A naive regex replace would also munge those names appearing inside SQL
// comments or string literals. Walk the SQL with a tiny state machine that
// skips line-comments (-- … \n), block-comments (/* … */), and single/double
// quoted strings (respecting SQL '' / "" escapes). Only substitute occurrences
// found in code state. Whitespace and case in the original SQL are preserved.
function rewriteVirtualTables(
  sql: string,
  tables: Array<{ name: string; path: string }>,
): string {
  // Build per-table regex + replacement up front so we don't recompile per-char.
  const replacements = tables.map((t) => ({
    pattern: new RegExp(`^FROM\\s+${t.name}\\b`, "i"),
    replacement: `FROM read_parquet('${t.path.replace(/'/g, "''")}')`,
  }));
  let out = "";
  let i = 0;
  while (i < sql.length) {
    const c = sql[i];
    const n = sql[i + 1];
    // Block comment /* ... */
    if (c === "/" && n === "*") {
      const end = sql.indexOf("*/", i + 2);
      const stop = end === -1 ? sql.length : end + 2;
      out += sql.slice(i, stop);
      i = stop;
      continue;
    }
    // Line comment -- ... \n
    if (c === "-" && n === "-") {
      const nl = sql.indexOf("\n", i + 2);
      const stop = nl === -1 ? sql.length : nl;
      out += sql.slice(i, stop);
      i = stop;
      continue;
    }
    // Quoted string ' ... ' or " ... " (with doubled-quote escape)
    if (c === "'" || c === '"') {
      const q = c;
      out += c;
      i++;
      while (i < sql.length) {
        if (sql[i] === q && sql[i + 1] === q) {
          out += q + q;
          i += 2;
          continue;
        }
        out += sql[i];
        if (sql[i] === q) {
          i++;
          break;
        }
        i++;
      }
      continue;
    }
    // Code state: only substitute at word boundaries.
    const isBoundary = i === 0 || !/[A-Za-z0-9_]/.test(sql[i - 1]);
    if (isBoundary) {
      let matched = false;
      for (const { pattern, replacement } of replacements) {
        const m = pattern.exec(sql.slice(i));
        if (m) {
          out += replacement;
          i += m[0].length;
          matched = true;
          break;
        }
      }
      if (matched) continue;
    }
    out += c;
    i++;
  }
  return out;
}

export async function POST(req: Request) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return Response.json(
      { error: "ANTHROPIC_API_KEY missing on the server. Set it in .env.local for `npm run dev`." },
      { status: 500 },
    );
  }

  let body: AskRequest;
  try {
    body = (await req.json()) as AskRequest;
  } catch {
    return Response.json({ error: "Body must be JSON: { question: string }" }, { status: 400 });
  }
  const question = (body.question || "").trim();
  if (!question) {
    return Response.json({ error: "question is required" }, { status: 400 });
  }

  // Resolve the parquet glob once up front. Surfaces missing/invalid
  // AMP_PARQUET_GLOB as a clean 503 instead of a generic 500 from inside the
  // tool loop, and gives the operator a precise message to fix in Project
  // Settings.
  let parquetGlob: string;
  try {
    parquetGlob = getAmpParquetGlob();
  } catch (e) {
    return Response.json(
      {
        error: e instanceof Error ? e.message : "AMP_PARQUET_GLOB is not configured.",
      },
      { status: 503 },
    );
  }
  // Daily-stats path is optional. When absent, the daily_stats virtual table
  // is simply not rewritten and any query against it will fail at DuckDB
  // (which the model handles via its retry loop).
  const dailyStatsPath = getDailyStatsPath();
  const tableMap: Array<{ name: string; path: string }> = [
    { name: "settlements", path: parquetGlob },
  ];
  if (dailyStatsPath) tableMap.push({ name: "daily_stats", path: dailyStatsPath });

  const client = new Anthropic({ apiKey });

  const tools: Anthropic.Tool[] = [
    {
      name: "run_sql",
      description:
        "Execute a single read-only SQL statement via DuckDB. Two virtual tables are available:\n" +
        "  • settlements — row-level data, 132M rows. Use for top-N, lookups, narrow windows.\n" +
        "  • daily_stats — pre-aggregated, 388 rows (one per day). Use for panoramic " +
        "daily/weekly/monthly views, time-series plots, or any question spanning > 90 days.\n" +
        "One statement per call. Include LIMIT 500 unless aggregate or user explicitly asks more.",
      input_schema: {
        type: "object",
        properties: {
          sql: {
            type: "string",
            description:
              "A single SELECT / WITH / EXPLAIN statement, no trailing semicolon. " +
              "Use 'FROM settlements' as the table.",
          },
        },
        required: ["sql"],
      },
    },
  ];

  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: question },
  ];

  const trace: TraceStep[] = [];
  let answerText = "";
  const t0 = Date.now();
  const budgetLeft = () => TOTAL_BUDGET_MS - (Date.now() - t0);

  for (let i = 0; i < MAX_TURNS; i++) {
    if (budgetLeft() <= 500) break;

    let resp: Anthropic.Message;
    try {
      resp = await client.messages.create({
        model: MODEL,
        max_tokens: 1500,
        system: SYSTEM_PROMPT,
        tools,
        messages,
      });
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      return Response.json({ error: `Anthropic error: ${msg}` }, { status: 502 });
    }

    if (resp.stop_reason !== "tool_use") {
      answerText = resp.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("\n")
        .trim();
      break;
    }

    // Tool turn: run every tool_use block in this assistant message.
    messages.push({ role: "assistant", content: resp.content });
    const toolResults: Anthropic.ToolResultBlockParam[] = [];

    for (const block of resp.content) {
      if (block.type !== "tool_use") continue;
      const use = block as ToolUse;
      if (use.name !== "run_sql") {
        toolResults.push({
          type: "tool_result",
          tool_use_id: use.id,
          is_error: true,
          content: `Unknown tool: ${use.name}`,
        });
        continue;
      }
      const sql = String((use.input as { sql?: unknown }).sql || "").trim();
      const rewritten = rewriteVirtualTables(sql, tableMap);
      // Tight per-call timeout so a single bad query can't eat the whole budget.
      const perCallTimeout = Math.max(1500, Math.min(40_000, budgetLeft() - 500));
      const result = await runSql(rewritten, { timeoutMs: perCallTimeout });

      const step: TraceStep = { sql, ms: result.ms };
      if (result.error) step.error = result.error;
      else step.rows = result.rows.length;
      trace.push(step);

      toolResults.push({
        type: "tool_result",
        tool_use_id: use.id,
        is_error: !!result.error,
        content: result.error
          ? `ERROR: ${result.error}`
          : JSON.stringify(result.rows),
      });
    }
    messages.push({ role: "user", content: toolResults });
  }

  // Synthesis fallback: if the loop exited without an assistant text turn,
  // do one final tool-less call summarizing the trace into an answer.
  if (!answerText && budgetLeft() > 500) {
    try {
      const summary = await client.messages.create({
        model: MODEL,
        max_tokens: 600,
        system:
          "You're being asked to answer a user's question given a partial " +
          "transcript of SQL calls and their results. Even if no single " +
          "call gave the full answer, write the best plain-English answer " +
          "you can from what's known, and clearly state what's unknown.",
        messages: [
          {
            role: "user",
            content:
              `Original question: ${question}\n\n` +
              `SQL trace so far:\n` +
              trace
                .map(
                  (t, i) =>
                    `[${i + 1}] ${t.sql}\n  → ${
                      t.error ? "ERROR: " + t.error : `${t.rows} rows`
                    }`,
                )
                .join("\n") +
              `\n\nAnswer the question concisely.`,
          },
        ],
      });
      answerText = summary.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("\n")
        .trim();
    } catch {
      // fall through with empty answer
    }
  }

  // Log the configured glob server-side for debugging — never echo it to clients.
  console.info("[amp/ask]", {
    question_chars: question.length,
    trace_steps: trace.length,
    total_ms: Date.now() - t0,
    parquet_path: parquetGlob,
  });

  return Response.json({
    answer: answerText || "(no answer produced)",
    trace,
    model: MODEL,
    total_ms: Date.now() - t0,
  });
}
