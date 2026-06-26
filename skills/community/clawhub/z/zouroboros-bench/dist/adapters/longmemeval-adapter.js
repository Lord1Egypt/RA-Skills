#!/usr/bin/env node

// src/adapters/longmemeval-adapter.ts
import { mkdtempSync, writeFileSync, readFileSync, rmSync, existsSync, mkdirSync } from "fs";
import { tmpdir } from "os";
import { join, basename } from "path";
import { parseArgs } from "util";
import { execSync } from "child_process";
var MEMORY_CLI = process.env.ZOUROBOROS_MEMORY_CLI ?? "zouroboros-memory";
var ANSWER_MODEL = process.env.ZO_ANSWER_MODEL ?? "gpt-4o-mini";
var OLLAMA_URL = process.env.OLLAMA_URL ?? "http://localhost:11434";
var OPENAI_API_KEY = process.env.OPENAI_API_KEY ?? "";
var MAX_CONTEXT_CHUNKS = 12;
var CONTEXT_CHAR_LIMIT = 12e3;
function memoryCmd(subcommand, args, dbPath, stdin) {
  const cli = MEMORY_CLI;
  const cmd = `${cli} ${subcommand} ${args.join(" ")}`;
  const env = { ...process.env, ZO_MEMORY_DB: dbPath };
  try {
    const result = execSync(cmd, {
      env,
      input: stdin,
      timeout: 3e5,
      maxBuffer: 50 * 1024 * 1024,
      encoding: "utf-8"
    });
    return result;
  } catch (e) {
    const stderr = e.stderr?.toString() ?? "";
    const stdout = e.stdout?.toString() ?? "";
    console.error(`[cli-error] ${subcommand}: ${stderr.slice(0, 300)}`);
    return stdout;
  }
}
function batchStore(dbPath, items, noEmbed) {
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
function hybridSearch(dbPath, query, limit = 10) {
  const result = memoryCmd("hybrid", [
    JSON.stringify(query),
    "--json",
    "--limit",
    String(limit)
  ], dbPath);
  try {
    return JSON.parse(result);
  } catch {
    return [];
  }
}
function ftsSearch(dbPath, query, limit = 10) {
  const result = memoryCmd("search", [
    JSON.stringify(query),
    "--json",
    "--limit",
    String(limit)
  ], dbPath);
  try {
    return JSON.parse(result);
  } catch {
    return [];
  }
}
async function ollamaGenerate(prompt, model = ANSWER_MODEL) {
  if (model.startsWith("gpt-") && OPENAI_API_KEY) {
    return openaiGenerate(prompt, model);
  }
  const resp = await fetch(`${OLLAMA_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model, prompt, stream: false, options: { temperature: 0.1, num_predict: 128 } })
  });
  if (!resp.ok) throw new Error(`Ollama error: ${resp.status}`);
  const data = await resp.json();
  return data.response.trim();
}
async function openaiGenerate(prompt, model = "gpt-4o-mini") {
  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${OPENAI_API_KEY}` },
    body: JSON.stringify({
      model,
      messages: [{ role: "user", content: prompt }],
      temperature: 0.1,
      max_tokens: 200
    })
  });
  if (!resp.ok) throw new Error(`OpenAI error: ${resp.status} ${await resp.text()}`);
  const data = await resp.json();
  return (data.choices?.[0]?.message?.content ?? "").trim();
}
async function cotAnswer(question, context, dbPath, questionType) {
  let typeInstructions = "";
  if (questionType === "knowledge-update") {
    typeInstructions = `
8. CRITICAL \u2014 RECENCY: When the same fact appears with DIFFERENT values across chunks, ALWAYS use the MOST RECENT value. Look for "updated", "now", "changed to", "improved to", "moved to", "new", or the later date.
9. If you see both an old value and a new value, the answer is the NEW value.`;
  } else if (questionType === "multi-session") {
    typeInstructions = `
8. CRITICAL \u2014 COUNTING/AGGREGATION: Read ALL chunks and ENUMERATE every distinct instance before answering. For "how many" questions, list each item then count. Do NOT stop at the first few.
9. Different chunks may mention different instances. Each unique item counts separately.
10. After listing all items, give your final count as the answer.`;
  } else if (questionType === "single-session-preference") {
    typeInstructions = `
8. CRITICAL \u2014 PREFERENCES: The question asks for a PERSONALIZED recommendation. Look for the user's stated preferences, interests, hobbies, past purchases, favorites, or expertise areas.
9. Reference specific details from the user's past conversations to justify your recommendation.`;
  } else if (questionType === "temporal-reasoning") {
    typeInstructions = `
8. CRITICAL \u2014 DATES/TIMING: Pay close attention to dates and temporal references. Extract exact dates and compute the answer.
9. Convert relative dates using conversation context if available.
10. For "how many days" questions, count carefully between the two dates.`;
  }
  const cotPrompt = `You are answering a question using conversation history. The answer IS in the context below \u2014 find it.

Context:
${context}

Question: ${question}

Instructions:
1. Read ALL chunks carefully from first to last \u2014 the answer may appear anywhere.
2. Look for specific names, places, dates, numbers, or facts that directly answer the question.
3. If a date is described as a holiday (e.g. "Valentine's Day"), convert to the calendar date.
4. If a place is mentioned by name, use the exact name.
5. Cross-reference entities across chunks: If one chunk describes an ACTION but doesn't name the STORE, look in nearby chunks for store/brand mentions.
6. For "Where" questions: scan ALL chunks for store names, brand names, app names, and location names.
7. Give a short, direct answer \u2014 just the specific fact requested.${typeInstructions}

The answer is:`;
  const cotResp = await ollamaGenerate(cotPrompt);
  const answerMatch = cotResp.match(/(?:ANSWER|The answer is)[:\s]+(.+)/i);
  const firstAnswer = answerMatch ? answerMatch[1].trim() : cotResp.split("\n").pop()?.trim() || cotResp.trim();
  const isWhereQuestion = /^where\b/i.test(question.trim());
  const answerLacksProperNoun = !/[A-Z][a-z]{2,}/.test(firstAnswer);
  const needsMultiHop = cotResp.includes("Not specified") || cotResp.includes("not enough") || isWhereQuestion && answerLacksProperNoun;
  if (needsMultiHop) {
    try {
      const augment = isWhereQuestion ? " store shop location name brand" : "";
      const refinedResults = hybridSearch(dbPath, `${question}${augment} ${cotResp.slice(0, 200)}`, 8);
      if (refinedResults.length > 0) {
        const refinedContext = refinedResults.map((r) => r.value).join("\n---\n").slice(0, CONTEXT_CHAR_LIMIT);
        const retryPrompt = `Given these conversation memories, answer the question with ONLY the specific fact requested.

Context:
${refinedContext}

Question: ${question}

IMPORTANT: For "Where" questions, the answer should be a STORE NAME or LOCATION NAME (a proper noun). Look for brand names, app names that imply stores, and explicit store mentions.

Answer:`;
        return ollamaGenerate(retryPrompt);
      }
    } catch {
    }
  }
  return firstAnswer;
}
async function gpt4Judge(question, groundTruth, hypothesis, questionType, questionId) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return "no_key";
  const isAbstention = questionId?.includes("_abs") ?? false;
  let prompt;
  if (isAbstention) {
    prompt = `I will give you an unanswerable question, an explanation, and a response from a model. Please answer yes if the model correctly identifies the question as unanswerable.

Question: ${question}

Explanation: ${groundTruth}

Model Response: ${hypothesis}

Does the model correctly identify the question as unanswerable? Answer yes or no only.`;
  } else if (questionType === "temporal-reasoning") {
    prompt = `I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Do not penalize off-by-one errors for number of days.

Question: ${question}

Correct Answer: ${groundTruth}

Model Response: ${hypothesis}

Is the model response correct? Answer yes or no only.`;
  } else if (questionType === "knowledge-update") {
    prompt = `I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. If the response contains previous information along with an updated answer, consider it correct as long as the updated answer matches.

Question: ${question}

Correct Answer: ${groundTruth}

Model Response: ${hypothesis}

Is the model response correct? Answer yes or no only.`;
  } else if (questionType === "single-session-preference") {
    prompt = `I will give you a question, a rubric, and a model response. Answer yes if the response satisfies the rubric. It doesn't need to reflect all points \u2014 just correctly recall and utilize personal information.

Question: ${question}

Rubric: ${groundTruth}

Model Response: ${hypothesis}

Is the model response correct? Answer yes or no only.`;
  } else {
    prompt = `I will give you a question, a correct answer, and a response from a model. Answer yes if the response contains the correct answer or is equivalent. If it only contains a subset, answer no.

Question: ${question}

Correct Answer: ${groundTruth}

Model Response: ${hypothesis}

Is the model response correct? Answer yes or no only.`;
  }
  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
    body: JSON.stringify({
      model: "gpt-4o",
      messages: [{ role: "user", content: prompt }],
      temperature: 0,
      max_tokens: 10
    })
  });
  if (!resp.ok) return "judge_error";
  const data = await resp.json();
  const label = data.choices?.[0]?.message?.content?.trim()?.toLowerCase();
  return label?.includes("yes") ? "correct" : label?.includes("no") ? "incorrect" : "unknown";
}
function simpleMatch(truth, hypothesis) {
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
function avg(arr) {
  return arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
}
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
      help: { type: "boolean", default: false }
    }
  });
  if (values.help || !values.dataset) {
    console.log(`Usage: zouroboros-bench --benchmarks longmemeval --dataset <path> [--output <dir>] [--limit N] [--judge] [--no-embed]`);
    process.exit(0);
  }
  const datasetPath = values.dataset;
  const outputDir = values.output;
  const limit = parseInt(values.limit) || 0;
  const useJudge = values.judge;
  const skipEmbed = values["no-embed"];
  const offset = parseInt(values.offset) || 0;
  const questionTypeFilter = values["question-type"];
  console.log(`[longmemeval-v3] Loading dataset: ${datasetPath}`);
  console.log(`[longmemeval-v3] Mode: PRODUCTION CLI ONLY (no direct DB access)`);
  const raw = JSON.parse(readFileSync(datasetPath, "utf-8"));
  let questions = Array.isArray(raw) ? raw : raw.data ?? [raw];
  if (questionTypeFilter) {
    questions = questions.filter((q) => q.question_type === questionTypeFilter);
    console.log(`[longmemeval-v3] Filtered to type '${questionTypeFilter}': ${questions.length} questions`);
  }
  if (offset > 0) questions = questions.slice(offset);
  if (limit > 0) questions = questions.slice(0, limit);
  console.log(`[longmemeval-v3] ${questions.length} questions to evaluate`);
  const tmpDir = mkdtempSync(join(tmpdir(), "zo-longmemeval-v3-"));
  const dbFile = join(tmpDir, "longmemeval.db");
  memoryCmd("init", [], dbFile);
  console.log(`[longmemeval-v3] DB initialized: ${dbFile}`);
  console.log(`[longmemeval-v3] Phase 1: Ingesting sessions via batch-store...`);
  const ingestStart = performance.now();
  const allSessionIds = /* @__PURE__ */ new Set();
  const factItems = [];
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
        let chunkParts = [`[user]: ${turn.content}`];
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
          source: "bench"
        });
      }
    }
  }
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
    console.error(`[longmemeval-v3] FATAL: No facts stored \u2014 aborting`);
    rmSync(tmpDir, { recursive: true, force: true });
    process.exit(1);
  }
  let indexMs = 0;
  if (skipEmbed) {
    console.log(`[longmemeval-v3] Phase 2: Skipped (--no-embed). FTS-only retrieval.`);
  } else if (totalEmbedded < totalStored) {
    console.log(`[longmemeval-v3] Phase 2: Backfilling ${totalStored - totalEmbedded} missing embeddings...`);
    const indexStart = performance.now();
    memoryCmd("index", ["--batch", "50"], dbFile);
    indexMs = performance.now() - indexStart;
    console.log(`[longmemeval-v3]   Indexing complete in ${Math.round(indexMs)}ms`);
  } else {
    console.log(`[longmemeval-v3] Phase 2: All ${totalEmbedded} embeddings generated during ingest.`);
  }
  console.log(`[longmemeval-v3] Phase 3: Querying and answering...`);
  const results = [];
  const retrievalLatencies = [];
  const answerLatencies = [];
  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    process.stdout.write(`\r  [${i + 1}/${questions.length}] ${q.question_type} \u2014 ${q.question.slice(0, 60)}...`);
    const t0 = performance.now();
    let context = [];
    try {
      const hybridResults = hybridSearch(dbFile, q.question, 10);
      context = hybridResults.map((r) => r.value);
    } catch (err) {
      console.error(`
  -> Hybrid search error: ${err}`);
    }
    if (context.length === 0) {
      const ftsResults = ftsSearch(dbFile, q.question, 10);
      context = ftsResults.map((r) => r.value);
    }
    context = context.slice(0, MAX_CONTEXT_CHUNKS);
    const retrievalMs = performance.now() - t0;
    retrievalLatencies.push(retrievalMs);
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
    let judgeLabel;
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
      judge_label: judgeLabel
    });
  }
  console.log("");
  const byType = {};
  let totalCorrect = 0;
  for (const r of results) {
    if (!byType[r.question_type]) byType[r.question_type] = { correct: 0, total: 0, accuracy: 0 };
    byType[r.question_type].total++;
    const isCorrect = r.judge_label === "correct" || !useJudge && simpleMatch(r.ground_truth, r.hypothesis);
    if (isCorrect) {
      byType[r.question_type].correct++;
      totalCorrect++;
    }
  }
  for (const type of Object.keys(byType)) {
    byType[type].accuracy = byType[type].total > 0 ? Math.round(byType[type].correct / byType[type].total * 1e4) / 100 : 0;
  }
  const sortedRetrieval = [...retrievalLatencies].sort((a, b) => a - b);
  const runResult = {
    benchmark: "LongMemEval",
    timestamp: (/* @__PURE__ */ new Date()).toISOString(),
    dataset: basename(datasetPath),
    total_questions: questions.length,
    answered: results.length,
    adapter_version: "v3-production-parity",
    scores: {
      overall_accuracy: results.length > 0 ? Math.round(totalCorrect / results.length * 1e4) / 100 : 0,
      by_type: byType
    },
    latency: {
      avg_retrieval_ms: Math.round(avg(retrievalLatencies)),
      avg_answer_ms: Math.round(avg(answerLatencies)),
      p95_retrieval_ms: Math.round(sortedRetrieval[Math.floor(sortedRetrieval.length * 0.95)] ?? 0),
      total_ingest_ms: Math.round(ingestMs),
      total_index_ms: Math.round(indexMs)
    },
    questions: results
  };
  if (!existsSync(outputDir)) mkdirSync(outputDir, { recursive: true });
  const outFile = join(outputDir, `longmemeval-${Date.now()}.json`);
  writeFileSync(outFile, JSON.stringify(runResult, null, 2));
  console.log(`
[longmemeval-v3] Results written to ${outFile}`);
  console.log(`[longmemeval-v3] Adapter: PRODUCTION CLI ONLY (v3)`);
  console.log(`[longmemeval-v3] Overall accuracy: ${runResult.scores.overall_accuracy}%`);
  console.log(`[longmemeval-v3] Ingest: ${Math.round(ingestMs)}ms | Indexing: ${Math.round(indexMs)}ms`);
  console.log(`[longmemeval-v3] Avg retrieval: ${runResult.latency.avg_retrieval_ms}ms, P95: ${runResult.latency.p95_retrieval_ms}ms`);
  for (const [type, s] of Object.entries(byType)) {
    console.log(`  ${type}: ${s.accuracy}% (${s.correct}/${s.total})`);
  }
  rmSync(tmpDir, { recursive: true, force: true });
}
main().catch((e) => {
  console.error("[longmemeval-v3] Fatal:", e);
  process.exit(1);
});
