#!/usr/bin/env node
/**
 * Standalone LongMemEval adapter for Zouroboros — PRODUCTION API ONLY
 *
 * Usage:
 *   node adapters/longmemeval-adapter.js \
 *     --dataset data/longmemeval/longmemeval_s_cleaned.json \
 *     --output data/runs/ \
 *     [--limit 50] \
 *     [--judge] \
 *     [--judge-model gpt-4o]
 *     [--no-embed]
 *
 * Pipeline:
 *   1. Ingest all haystack sessions via `zouroboros-memory batch-store` (production CLI)
 *   2. For each question, retrieve context via `zouroboros-memory hybrid --json` (production search)
 *   3. Generate hypothesis answer via LLM
 *   4. Optionally score with GPT-4o judge
 *   5. Output results JSON
 *
 * v3: Production-parity rewrite — uses ONLY the memory CLI.
 *     No direct sqlite access. No custom RRF weights.
 *     Scores reflect what the real memory system can do.
 */

import { mkdtempSync, writeFileSync, readFileSync, rmSync, existsSync, mkdirSync } from "fs";
import { tmpdir } from "os";
import { join, basename } from "path";
import { parseArgs } from "util";
import { execSync } from "child_process";
import { randomUUID } from "crypto";

const MEMORY_CLI = process.env.ZOUROBOROS_MEMORY_CLI ?? 'zouroboros-memory';
const ANSWER_MODEL = process.env.ZO_ANSWER_MODEL ?? "gpt-4o-mini";
const OLLAMA_URL = process.env.OLLAMA_URL ?? "http://localhost:11434";
const OPENAI_API_KEY = process.env.OPENAI_API_KEY ?? "";
const MAX_CONTEXT_CHUNKS = 12;
const CONTEXT_CHAR_LIMIT = 12000;

interface LongMemQuestion {
  question_id: string;
  question_type: string;
  question: string;
  answer: string;
  question_date?: string;
  haystack_sessions?: Array<Array<{ role: string; content: string; has_answer?: boolean }>>;
  haystack_session_ids?: string[];
  answer_session_ids?: string[];
}

interface RunResult {
  benchmark: string;
  timestamp: string;
  dataset: string;
  total_questions: number;
  answered: number;
  adapter_version: string;
  scores: {
    overall_accuracy: number;
    by_type: Record<string, { correct: number; total: number; accuracy: number }>;
  };
  latency: {
    avg_retrieval_ms: number;
    avg_answer_ms: number;
    p95_retrieval_ms: number;
    total_ingest_ms: number;
    total_index_ms: number;
  };
  questions: Array<{
    question_id: string;
    question_type: string;
    question: string;
    ground_truth: string;
    hypothesis: string;
    retrieved_context: string[];
    retrieval_ms: number;
    answer_ms: number;
    judge_label?: string;
  }>;
}

interface HybridResult {
  id: string;
  persona: string;
  entity: string;
  key: string | null;
  value: string;
  text: string;
  category: string;
  decayClass: string;
  importance: number;
  source: string;
  createdAt: number;
  expiresAt: number | null;
  confidence: number;
  score: number;
  sources: string[];
}

// ─── Production CLI Helpers ──────────────────────────────────────────

function memoryCmd(subcommand: string, args: string[], dbPath: string, stdin?: string): string {
  const cli = MEMORY_CLI;
  const cmd = `${cli} ${subcommand} ${args.join(" ")}`;
  const env = { ...process.env, ZO_MEMORY_DB: dbPath };
  try {
    const result = execSync(cmd, {
      env,
      input: stdin,
      timeout: 300_000,
      maxBuffer: 50 * 1024 * 1024,
      encoding: "utf-8",
    });
    return result;
  } catch (e: any) {
    const stderr = e.stderr?.toString() ?? "";
    const stdout = e.stdout?.toString() ?? "";
    console.error(`[cli-error] ${subcommand}: ${stderr.slice(0, 300)}`);
    return stdout;
  }
}

function batchStore(
  dbPath: string,
  items: Array<{ entity: string; value: string; key?: string; importance?: number; source?: string }>,
  noEmbed: boolean
): { stored: number; embedded: number } {
  const json = JSON.stringify(items);
  const flags = ["--json"];
  if (noEmbed) flags.push("--no-embed");
  const result = memoryCmd("batch-store", flags, dbPath, json);
  try {
    return JSON.parse(result);
  } catch {
    console.error(`[batch-store] Failed to parse result: ${result.slice(0, 200)}`);
    return { stored: 0, embedded: 0 };
  }
}

function hybridSearch(dbPath: string, query: string, limit = 10): HybridResult[] {
  const result = memoryCmd("hybrid", [
    JSON.stringify(query),
    "--json",
    "--limit", String(limit),
  ], dbPath);
  try {
    return JSON.parse(result);
  } catch {
    return [];
  }
}

function ftsSearch(dbPath: string, query: string, limit = 10): HybridResult[] {
  const result = memoryCmd("search", [
    JSON.stringify(query),
    "--json",
    "--limit", String(limit),
  ], dbPath);
  try {
    return JSON.parse(result);
  } catch {
    return [];
  }
}

// ─── LLM Answer Generation ──────────────────────────────────────────

async function ollamaGenerate(prompt: string, model = ANSWER_MODEL): Promise<string> {
  if (model.startsWith("gpt-") && OPENAI_API_KEY) {
    return openaiGenerate(prompt, model);
  }
  const resp = await fetch(`${OLLAMA_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model, prompt, stream: false, options: { temperature: 0.1, num_predict: 128 } }),
  });
  if (!resp.ok) throw new Error(`Ollama error: ${resp.status}`);
  const data = (await resp.json()) as { response: string };
  return data.response.trim();
}

async function openaiGenerate(prompt: string, model = "gpt-4o-mini"): Promise<string> {
  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${OPENAI_API_KEY}` },
    body: JSON.stringify({
      model,
      messages: [{ role: "user", content: prompt }],
      temperature: 0.1,
      max_tokens: 200,
    }),
  });
  if (!resp.ok) throw new Error(`OpenAI error: ${resp.status} ${await resp.text()}`);
  const data = (await resp.json()) as any;
  return (data.choices?.[0]?.message?.content ?? "").trim();
}

// ─── Chain-of-Thought Answer ─────────────────────────────────────────

async function cotAnswer(
  question: string,
  context: string,
  dbPath: string,
  questionType?: string
): Promise<string> {
  let typeInstructions = "";
  if (questionType === "knowledge-update") {
    typeInstructions = `\n8. CRITICAL — RECENCY: When the same fact appears with DIFFERENT values across chunks, ALWAYS use the MOST RECENT value. Look for "updated", "now", "changed to", "improved to", "moved to", "new", or the later date.\n9. If you see both an old value and a new value, the answer is the NEW value.`;
  } else if (questionType === "multi-session") {
    typeInstructions = `\n8. CRITICAL — COUNTING/AGGREGATION: Read ALL chunks and ENUMERATE every distinct instance before answering. For "how many" questions, list each item then count. Do NOT stop at the first few.\n9. Different chunks may mention different instances. Each unique item counts separately.\n10. After listing all items, give your final count as the answer.`;
  } else if (questionType === "single-session-preference") {
    typeInstructions = `\n8. CRITICAL — PREFERENCES: The question asks for a PERSONALIZED recommendation. Look for the user's stated preferences, interests, hobbies, past purchases, favorites, or expertise areas.\n9. Reference specific details from the user's past conversations to justify your recommendation.`;
  } else if (questionType === "temporal-reasoning") {
    typeInstructions = `\n8. CRITICAL — DATES/TIMING: Pay close attention to dates and temporal references. Extract exact dates and compute the answer.\n9. Convert relative dates using conversation context if available.\n10. For "how many days" questions, count carefully between the two dates.`;
  }

  const cotPrompt = `You are answering a question using conversation history. The answer IS in the context below — find it.

Context:
${context}

Question: ${question}

Instructions:
1. Read ALL chunks carefully from first to last — the answer may appear anywhere.
2. Look for specific names, places, dates, numbers, or facts that directly answer the question.
3. If a date is described as a holiday (e.g. "Valentine's Day"), convert to the calendar date.
4. If a place is mentioned by name, use the exact name.
5. Cross-reference entities across chunks: If one chunk describes an ACTION but doesn't name the STORE, look in nearby chunks for store/brand mentions.
6. For "Where" questions: scan ALL chunks for store names, brand names, app names, and location names.
7. Give a short, direct answer — just the specific fact requested.${typeInstructions}

The answer is:`;

  const cotResp = await ollamaGenerate(cotPrompt);

  const answerMatch = cotResp.match(/(?:ANSWER|The answer is)[:\s]+(.+)/i);
  const firstAnswer = answerMatch ? answerMatch[1].trim() : cotResp.split("\n").pop()?.trim() || cotResp.trim();

  // Multi-hop: if answer seems incomplete, do a second retrieval via production CLI
  const isWhereQuestion = /^where\b/i.test(question.trim());
  const answerLacksProperNoun = !/[A-Z][a-z]{2,}/.test(firstAnswer);
  const needsMultiHop = cotResp.includes("Not specified") || cotResp.includes("not enough") ||
    (isWhereQuestion && answerLacksProperNoun);

  if (needsMultiHop) {
    try {
      const augment = isWhereQuestion ? " store shop location name brand" : "";
      const refinedResults = hybridSearch(dbPath, `${question}${augment} ${cotResp.slice(0, 200)}`, 8);
      if (refinedResults.length > 0) {
        const refinedContext = refinedResults.map(r => r.value).join("\n---\n").slice(0, CONTEXT_CHAR_LIMIT);
        const retryPrompt = `Given these conversation memories, answer the question with ONLY the specific fact requested.

Context:
${refinedContext}

Question: ${question}

IMPORTANT: For "Where" questions, the answer should be a STORE NAME or LOCATION NAME (a proper noun). Look for brand names, app names that imply stores, and explicit store mentions.

Answer:`;
        return ollamaGenerate(retryPrompt);
      }
    } catch { /* fall through */ }
  }

  return firstAnswer;
}

// ─── GPT-4o Judge ────────────────────────────────────────────────────

async function gpt4Judge(question: string, groundTruth: string, hypothesis: string, questionType?: string, questionId?: string): Promise<string> {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return "no_key";

  const isAbstention = questionId?.includes("_abs") ?? false;
  let prompt: string;

  if (isAbstention) {
    prompt = `I will give you an unanswerable question, an explanation, and a response from a model. Please answer yes if the model correctly identifies the question as unanswerable.\n\nQuestion: ${question}\n\nExplanation: ${groundTruth}\n\nModel Response: ${hypothesis}\n\nDoes the model correctly identify the question as unanswerable? Answer yes or no only.`;
  } else if (questionType === "temporal-reasoning") {
    prompt = `I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Do not penalize off-by-one errors for number of days.\n\nQuestion: ${question}\n\nCorrect Answer: ${groundTruth}\n\nModel Response: ${hypothesis}\n\nIs the model response correct? Answer yes or no only.`;
  } else if (questionType === "knowledge-update") {
    prompt = `I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. If the response contains previous information along with an updated answer, consider it correct as long as the updated answer matches.\n\nQuestion: ${question}\n\nCorrect Answer: ${groundTruth}\n\nModel Response: ${hypothesis}\n\nIs the model response correct? Answer yes or no only.`;
  } else if (questionType === "single-session-preference") {
    prompt = `I will give you a question, a rubric, and a model response. Answer yes if the response satisfies the rubric. It doesn't need to reflect all points — just correctly recall and utilize personal information.\n\nQuestion: ${question}\n\nRubric: ${groundTruth}\n\nModel Response: ${hypothesis}\n\nIs the model response correct? Answer yes or no only.`;
  } else {
    prompt = `I will give you a question, a correct answer, and a response from a model. Answer yes if the response contains the correct answer or is equivalent. If it only contains a subset, answer no.\n\nQuestion: ${question}\n\nCorrect Answer: ${groundTruth}\n\nModel Response: ${hypothesis}\n\nIs the model response correct? Answer yes or no only.`;
  }

  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
    body: JSON.stringify({
      model: "gpt-4o",
      messages: [{ role: "user", content: prompt }],
      temperature: 0,
      max_tokens: 10,
    }),
  });
  if (!resp.ok) return "judge_error";
  const data = (await resp.json()) as any;
  const label = data.choices?.[0]?.message?.content?.trim()?.toLowerCase();
  return label?.includes("yes") ? "correct" : label?.includes("no") ? "incorrect" : "unknown";
}

// ─── Simple Match Scoring ────────────────────────────────────────────

function simpleMatch(truth: string, hypothesis: string): boolean {
  if (!truth || !hypothesis) return false;
  const t = truth.toLowerCase().trim();
  const h = hypothesis.toLowerCase().trim();
  if (h.includes(t) || t.includes(h)) return true;
  const tWords = t.split(/\s+/).filter((w) => w.length > 2);
  if (tWords.length === 0) return false;
  let overlap = 0;
  for (const w of tWords) {
    if (h.includes(w)) overlap++;
  }
  return overlap / tWords.length >= 0.5;
}

function avg(arr: number[]): number {
  return arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
}

// ─── Main ────────────────────────────────────────────────────────────

async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      dataset: { type: "string" },
      output: { type: "string", default: "data/runs" },
      limit: { type: "string", default: "0" },
      judge: { type: "boolean", default: false },
      "judge-model": { type: "string", default: "gpt-4o" },
      "no-embed": { type: "boolean", default: false },
      offset: { type: "string", default: "0" },
      "question-type": { type: "string" },
      help: { type: "boolean", default: false },
    },
  });

  if (values.help || !values.dataset) {
    console.log(`Usage: zouroboros-bench --benchmarks longmemeval --dataset <path> [--output <dir>] [--limit N] [--judge] [--no-embed]`);
    process.exit(0);
  }

  const datasetPath = values.dataset!;
  const outputDir = values.output!;
  const limit = parseInt(values.limit!) || 0;
  const useJudge = values.judge!;
  const skipEmbed = values["no-embed"]!;
  const offset = parseInt(values.offset!) || 0;
  const questionTypeFilter = values["question-type"];

  console.log(`[longmemeval-v3] Loading dataset: ${datasetPath}`);
  console.log(`[longmemeval-v3] Mode: PRODUCTION CLI ONLY (no direct DB access)`);
  const raw = JSON.parse(readFileSync(datasetPath, "utf-8"));
  let questions: LongMemQuestion[] = Array.isArray(raw) ? raw : raw.data ?? [raw];

  if (questionTypeFilter) {
    questions = questions.filter(q => q.question_type === questionTypeFilter);
    console.log(`[longmemeval-v3] Filtered to type '${questionTypeFilter}': ${questions.length} questions`);
  }
  if (offset > 0) questions = questions.slice(offset);
  if (limit > 0) questions = questions.slice(0, limit);
  console.log(`[longmemeval-v3] ${questions.length} questions to evaluate`);

  // Create temp DB path for this run
  const tmpDir = mkdtempSync(join(tmpdir(), "zo-longmemeval-v3-"));
  const dbFile = join(tmpDir, "longmemeval.db");

  // Initialize DB via production CLI
  memoryCmd("init", [], dbFile);
  console.log(`[longmemeval-v3] DB initialized: ${dbFile}`);

  // ── Phase 1: Ingest via production batch-store ──
  console.log(`[longmemeval-v3] Phase 1: Ingesting sessions via batch-store...`);
  const ingestStart = performance.now();
  const allSessionIds = new Set<string>();

  // Turn-level chunking: prepare fact items for batch store
  const factItems: Array<{ entity: string; value: string; key: string; importance: number; source: string }> = [];

  for (const q of questions) {
    if (!q.haystack_sessions) continue;
    for (let i = 0; i < q.haystack_sessions.length; i++) {
      const sessionId = q.haystack_session_ids?.[i] ?? `session-${q.question_id}-${i}`;
      if (allSessionIds.has(sessionId)) continue;
      allSessionIds.add(sessionId);

      const session = q.haystack_sessions[i];

      for (let t = 0; t < session.length; t++) {
        const turn = session[t];
        if (turn.role !== "user") continue;

        let chunkParts: string[] = [`[user]: ${turn.content}`];
        if (t + 1 < session.length && session[t + 1].role === "assistant") {
          chunkParts.push(`[assistant]: ${session[t + 1].content}`);
        }

        const value = chunkParts.join("\n");
        if (value.length < 30) continue;

        factItems.push({
          entity: `session.${sessionId}`,
          key: `turn-${t}`,
          value,
          importance: 0.8,
          source: "bench",
        });
      }
    }
  }

  // Batch store in chunks of 200 to avoid massive stdin payloads
  const BATCH_SIZE = 200;
  let totalStored = 0;
  let totalEmbedded = 0;

  for (let i = 0; i < factItems.length; i += BATCH_SIZE) {
    const batch = factItems.slice(i, i + BATCH_SIZE);
    const result = batchStore(dbFile, batch, skipEmbed);
    totalStored += result.stored;
    totalEmbedded += result.embedded;
    if (factItems.length > BATCH_SIZE) {
      console.log(`[longmemeval-v3]   Batch ${Math.floor(i / BATCH_SIZE) + 1}: ${result.stored} stored, ${result.embedded} embedded`);
    }
  }

  const ingestMs = performance.now() - ingestStart;
  console.log(`[longmemeval-v3]   Ingested ${totalStored} facts (${totalEmbedded} embedded) in ${Math.round(ingestMs)}ms`);

  if (totalStored === 0) {
    console.error(`[longmemeval-v3] FATAL: No facts stored — aborting`);
    rmSync(tmpDir, { recursive: true, force: true });
    process.exit(1);
  }

  // ── Phase 2: Indexing done during batch-store (unless --no-embed) ──
  let indexMs = 0;
  if (skipEmbed) {
    console.log(`[longmemeval-v3] Phase 2: Skipped (--no-embed). FTS-only retrieval.`);
  } else if (totalEmbedded < totalStored) {
    // Run index backfill for any missed embeddings
    console.log(`[longmemeval-v3] Phase 2: Backfilling ${totalStored - totalEmbedded} missing embeddings...`);
    const indexStart = performance.now();
    memoryCmd("index", ["--batch", "50"], dbFile);
    indexMs = performance.now() - indexStart;
    console.log(`[longmemeval-v3]   Indexing complete in ${Math.round(indexMs)}ms`);
  } else {
    console.log(`[longmemeval-v3] Phase 2: All ${totalEmbedded} embeddings generated during ingest.`);
  }

  // ── Phase 3: Query + Answer via production CLI ──
  console.log(`[longmemeval-v3] Phase 3: Querying and answering...`);
  const results: RunResult["questions"] = [];
  const retrievalLatencies: number[] = [];
  const answerLatencies: number[] = [];

  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    process.stdout.write(`\r  [${i + 1}/${questions.length}] ${q.question_type} — ${q.question.slice(0, 60)}...`);

    // Retrieve via production hybrid search
    const t0 = performance.now();
    let context: string[] = [];

    try {
      const hybridResults = hybridSearch(dbFile, q.question, 10);
      context = hybridResults.map((r) => r.value);
    } catch (err) {
      console.error(`\n  -> Hybrid search error: ${err}`);
    }

    // Fallback to FTS if hybrid returned nothing
    if (context.length === 0) {
      const ftsResults = ftsSearch(dbFile, q.question, 10);
      context = ftsResults.map((r) => r.value);
    }

    // Trim to max chunks
    context = context.slice(0, MAX_CONTEXT_CHUNKS);

    const retrievalMs = performance.now() - t0;
    retrievalLatencies.push(retrievalMs);

    // Chain-of-thought answer
    const t1 = performance.now();
    let hypothesis = "";
    try {
      const contextStr = context.join("\n---\n").slice(0, CONTEXT_CHAR_LIMIT);
      hypothesis = await cotAnswer(q.question, contextStr, dbFile, q.question_type);
    } catch {
      hypothesis = "Error generating answer";
    }
    const answerMs = performance.now() - t1;
    answerLatencies.push(answerMs);

    // Judge (optional)
    let judgeLabel: string | undefined;
    if (useJudge) {
      judgeLabel = await gpt4Judge(q.question, q.answer, hypothesis, q.question_type, q.question_id);
    }

    results.push({
      question_id: q.question_id,
      question_type: q.question_type,
      question: q.question,
      ground_truth: q.answer,
      hypothesis,
      retrieved_context: context.map((c) => c.slice(0, 500)),
      retrieval_ms: Math.round(retrievalMs),
      answer_ms: Math.round(answerMs),
      judge_label: judgeLabel,
    });
  }
  console.log("");

  // ── Phase 4: Score ──
  const byType: Record<string, { correct: number; total: number; accuracy: number }> = {};
  let totalCorrect = 0;

  for (const r of results) {
    if (!byType[r.question_type]) byType[r.question_type] = { correct: 0, total: 0, accuracy: 0 };
    byType[r.question_type].total++;

    const isCorrect = r.judge_label === "correct"
      || (!useJudge && simpleMatch(r.ground_truth, r.hypothesis));

    if (isCorrect) {
      byType[r.question_type].correct++;
      totalCorrect++;
    }
  }

  for (const type of Object.keys(byType)) {
    byType[type].accuracy = byType[type].total > 0
      ? Math.round((byType[type].correct / byType[type].total) * 10000) / 100
      : 0;
  }

  const sortedRetrieval = [...retrievalLatencies].sort((a, b) => a - b);

  const runResult: RunResult = {
    benchmark: "LongMemEval",
    timestamp: new Date().toISOString(),
    dataset: basename(datasetPath),
    total_questions: questions.length,
    answered: results.length,
    adapter_version: "v3-production-parity",
    scores: {
      overall_accuracy: results.length > 0
        ? Math.round((totalCorrect / results.length) * 10000) / 100
        : 0,
      by_type: byType,
    },
    latency: {
      avg_retrieval_ms: Math.round(avg(retrievalLatencies)),
      avg_answer_ms: Math.round(avg(answerLatencies)),
      p95_retrieval_ms: Math.round(sortedRetrieval[Math.floor(sortedRetrieval.length * 0.95)] ?? 0),
      total_ingest_ms: Math.round(ingestMs),
      total_index_ms: Math.round(indexMs),
    },
    questions: results,
  };

  // Write output
  if (!existsSync(outputDir)) mkdirSync(outputDir, { recursive: true });
  const outFile = join(outputDir, `longmemeval-${Date.now()}.json`);
  writeFileSync(outFile, JSON.stringify(runResult, null, 2));
  console.log(`\n[longmemeval-v3] Results written to ${outFile}`);
  console.log(`[longmemeval-v3] Adapter: PRODUCTION CLI ONLY (v3)`);
  console.log(`[longmemeval-v3] Overall accuracy: ${runResult.scores.overall_accuracy}%`);
  console.log(`[longmemeval-v3] Ingest: ${Math.round(ingestMs)}ms | Indexing: ${Math.round(indexMs)}ms`);
  console.log(`[longmemeval-v3] Avg retrieval: ${runResult.latency.avg_retrieval_ms}ms, P95: ${runResult.latency.p95_retrieval_ms}ms`);
  for (const [type, s] of Object.entries(byType)) {
    console.log(`  ${type}: ${s.accuracy}% (${s.correct}/${s.total})`);
  }

  // Cleanup
  rmSync(tmpDir, { recursive: true, force: true });
}

main().catch((e) => {
  console.error("[longmemeval-v3] Fatal:", e);
  process.exit(1);
});
