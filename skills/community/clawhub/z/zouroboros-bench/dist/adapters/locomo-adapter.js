#!/usr/bin/env node

// src/adapters/locomo-adapter.ts
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
var CONTEXT_CHAR_LIMIT = 6e3;
var CATEGORY_NAMES = {
  1: "single-hop",
  2: "multi-hop",
  3: "commonsense",
  4: "adversarial",
  5: "temporal"
};
function memoryCmd(subcommand, args, dbPath, stdin) {
  const cmd = `${MEMORY_CLI} ${subcommand} ${args.join(" ")}`;
  const env = { ...process.env, ZO_MEMORY_DB: dbPath };
  try {
    return execSync(cmd, {
      env,
      input: stdin,
      timeout: 3e5,
      maxBuffer: 50 * 1024 * 1024,
      encoding: "utf-8"
    });
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
function ftsSearch(dbPath, query, limit = 10, entity) {
  const args = [JSON.stringify(query), "--json", "--limit", String(limit)];
  if (entity) args.push("--entity", JSON.stringify(entity));
  const result = memoryCmd("search", args, dbPath);
  try {
    return JSON.parse(result);
  } catch {
    return [];
  }
}
async function generateAnswer(prompt) {
  if (ANSWER_MODEL.startsWith("gpt-") && OPENAI_API_KEY) {
    return openaiGenerate(prompt, ANSWER_MODEL);
  }
  return ollamaGenerate(prompt, ANSWER_MODEL);
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
async function ollamaGenerate(prompt, model = "qwen2.5:7b") {
  const resp = await fetch(`${OLLAMA_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model, prompt, stream: false, options: { temperature: 0.1, num_predict: 128 } })
  });
  if (!resp.ok) throw new Error(`Ollama error: ${resp.status}`);
  const data = await resp.json();
  return data.response.trim();
}
async function gpt4Judge(question, groundTruth, hypothesis) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return "no_key";
  const prompt = `You are evaluating a memory system's answer about a past conversation.

Question: ${question}
Ground Truth: ${groundTruth}
System Answer: ${hypothesis}

Is the system's answer correct? It doesn't need to match exactly \u2014 it should capture the key information.
Respond with exactly one word: CORRECT or INCORRECT`;
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
  const label = data.choices?.[0]?.message?.content?.trim()?.toUpperCase();
  return label === "CORRECT" ? "correct" : label === "INCORRECT" ? "incorrect" : "unknown";
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
function tokenF1(truth, hypothesis) {
  if (!truth || !hypothesis) return 0;
  const tTokens = truth.toLowerCase().split(/\s+/).filter(Boolean);
  const hTokens = hypothesis.toLowerCase().split(/\s+/).filter(Boolean);
  if (tTokens.length === 0 || hTokens.length === 0) return 0;
  const tSet = new Set(tTokens);
  const hSet = new Set(hTokens);
  let overlapCount = 0;
  for (const t of tSet) if (hSet.has(t)) overlapCount++;
  const precision = overlapCount / hSet.size;
  const recall = overlapCount / tSet.size;
  return precision + recall > 0 ? 2 * precision * recall / (precision + recall) : 0;
}
function avg(arr) {
  return arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
}
function extractSessions(conversation) {
  const sessions = [];
  const sessionKeys = Object.keys(conversation).filter((k) => /^session_\d+$/.test(k)).sort((a, b) => {
    const numA = parseInt(a.replace("session_", ""));
    const numB = parseInt(b.replace("session_", ""));
    return numA - numB;
  });
  for (const key of sessionKeys) {
    const sessionNum = parseInt(key.replace("session_", ""));
    const val = conversation[key];
    const dateKey = `${key}_date_time`;
    const date = conversation[dateKey] ?? void 0;
    let turns = [];
    if (Array.isArray(val)) {
      turns = val.map((turn) => {
        if (typeof turn === "object" && turn.speaker && turn.text) {
          return { speaker: turn.speaker, dia_id: turn.dia_id ?? "", text: turn.text };
        }
        if (Array.isArray(turn)) {
          return { speaker: turn[0] ?? "unknown", dia_id: turn[1] ?? "", text: turn[2] ?? turn[1] ?? "" };
        }
        return { speaker: "unknown", dia_id: "", text: JSON.stringify(turn) };
      });
    }
    sessions.push({ sessionKey: key, sessionNum, turns, date });
  }
  return sessions;
}
async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      dataset: { type: "string" },
      output: { type: "string", default: "data/runs" },
      limit: { type: "string", default: "0" },
      judge: { type: "boolean", default: false },
      "no-embed": { type: "boolean", default: false },
      help: { type: "boolean", default: false }
    }
  });
  if (values.help || !values.dataset) {
    console.log(`Usage: node adapters/locomo-adapter.js --dataset <path> [options]
  --output       Output directory (default: data/runs)
  --limit N      Limit total questions evaluated (0=all)
  --judge        Use GPT-4o judge for accuracy
  --no-embed     Skip embeddings, FTS-only (fast testing)`);
    process.exit(0);
  }
  const datasetPath = values.dataset;
  const outputDir = values.output;
  const limit = parseInt(values.limit) || 0;
  const useJudge = values.judge;
  const skipEmbed = values["no-embed"];
  console.log(`[locomo-v3] Loading dataset: ${datasetPath}`);
  console.log(`[locomo-v3] Mode: PRODUCTION CLI ONLY (no direct DB access)`);
  const raw = JSON.parse(readFileSync(datasetPath, "utf-8"));
  const conversations = Array.isArray(raw) ? raw : [raw];
  console.log(`[locomo-v3] ${conversations.length} conversations loaded`);
  console.log(`[locomo-v3] Embeddings: ${skipEmbed ? "DISABLED (FTS-only)" : "enabled"}`);
  const tmpDir = mkdtempSync(join(tmpdir(), "zo-locomo-v3-"));
  const dbFile = join(tmpDir, "locomo.db");
  memoryCmd("init", [], dbFile);
  console.log(`[locomo-v3] DB initialized: ${dbFile}`);
  console.log(`[locomo-v3] Phase 1: Ingesting sessions via batch-store...`);
  const ingestStart = performance.now();
  const factItems = [];
  for (const conv of conversations) {
    const sessions = extractSessions(conv.conversation);
    for (const session of sessions) {
      const datePrefix = session.date ? `[${session.date}] ` : "";
      for (let t = 0; t < session.turns.length; t++) {
        const turn = session.turns[t];
        const nextTurn = t + 1 < session.turns.length ? session.turns[t + 1] : null;
        let chunkParts = [`[${turn.speaker}]: ${turn.text}`];
        if (nextTurn && nextTurn.speaker !== turn.speaker) {
          chunkParts.push(`[${nextTurn.speaker}]: ${nextTurn.text}`);
          t++;
        }
        const value = datePrefix ? `${datePrefix}${chunkParts.join("\n")}` : chunkParts.join("\n");
        if (value.length < 20) continue;
        const entity = `${conv.sample_id}.session_${session.sessionNum}`;
        const key = `turn-${turn.dia_id || t}`;
        factItems.push({
          entity,
          key,
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
      console.log(`[locomo-v3]   Batch ${Math.floor(i / BATCH_SIZE) + 1}: ${result.stored} stored, ${result.embedded} embedded`);
    }
  }
  const ingestMs = performance.now() - ingestStart;
  console.log(`[locomo-v3]   Ingested ${totalStored} facts (${totalEmbedded} embedded) in ${Math.round(ingestMs)}ms`);
  if (totalStored === 0) {
    console.error(`[locomo-v3] FATAL: No facts stored \u2014 aborting`);
    rmSync(tmpDir, { recursive: true, force: true });
    process.exit(1);
  }
  let indexMs = 0;
  if (skipEmbed) {
    console.log(`[locomo-v3] Phase 2: Skipped (--no-embed). FTS-only retrieval.`);
  } else if (totalEmbedded < totalStored) {
    console.log(`[locomo-v3] Phase 2: Backfilling ${totalStored - totalEmbedded} missing embeddings...`);
    const indexStart = performance.now();
    memoryCmd("index", ["--batch", "50"], dbFile);
    indexMs = performance.now() - indexStart;
    console.log(`[locomo-v3]   Indexing complete in ${Math.round(indexMs)}ms`);
  } else {
    console.log(`[locomo-v3] Phase 2: All ${totalEmbedded} embeddings generated during ingest.`);
  }
  console.log(`[locomo-v3] Phase 3: Querying and answering...`);
  const results = [];
  let totalQ = 0;
  for (const conv of conversations) {
    let questions = conv.qa ?? [];
    if (limit > 0 && totalQ + questions.length > limit) {
      questions = questions.slice(0, limit - totalQ);
    }
    for (const qa of questions) {
      if (qa.answer == null) continue;
      totalQ++;
      const groundTruth = String(qa.answer);
      const catName = CATEGORY_NAMES[qa.category] ?? `cat-${qa.category}`;
      process.stdout.write(`\r  [${totalQ}] ${catName} \u2014 ${qa.question.slice(0, 55)}...`);
      const t0 = performance.now();
      let context = [];
      try {
        if (skipEmbed) {
          const results2 = ftsSearch(dbFile, qa.question, 10);
          context = results2.map((r) => r.value);
        } else {
          const hybridResults = hybridSearch(dbFile, qa.question, 10);
          context = hybridResults.map((r) => r.value);
          if (context.length === 0) {
            const ftsResults = ftsSearch(dbFile, qa.question, 10);
            context = ftsResults.map((r) => r.value);
          }
          if (hybridResults.length > 0) {
            const topEntities = /* @__PURE__ */ new Set();
            for (const r of hybridResults.slice(0, 3)) {
              topEntities.add(r.entity);
            }
            const existingSet = new Set(context);
            for (const entity of topEntities) {
              const sessionResults = ftsSearch(dbFile, qa.question, 5, entity);
              for (const r of sessionResults) {
                if (!existingSet.has(r.value)) {
                  context.push(r.value);
                  existingSet.add(r.value);
                }
              }
            }
          }
        }
      } catch (err) {
        console.error(`
  -> Search error: ${err}`);
      }
      context = context.slice(0, MAX_CONTEXT_CHUNKS);
      const retrievalMs = performance.now() - t0;
      const t1 = performance.now();
      let hypothesis = "";
      try {
        const contextStr = context.join("\n---\n").slice(0, CONTEXT_CHAR_LIMIT);
        hypothesis = await generateAnswer(
          `Given these conversation memories, answer the question with ONLY the specific fact requested. Give a short, direct answer \u2014 just the name, number, date, or place. Do not explain or qualify.
When dates are asked, use the absolute date (e.g. "7 May 2023") from the session timestamps, not relative terms like "yesterday" or "last week".

Context:
${contextStr}

Question: ${qa.question}

Answer:`
        );
      } catch {
        hypothesis = "Error generating answer";
      }
      const answerMs = performance.now() - t1;
      const isCorrect = useJudge ? false : simpleMatch(groundTruth, hypothesis);
      let judgeLabel;
      if (useJudge) {
        judgeLabel = await gpt4Judge(qa.question, groundTruth, hypothesis);
      }
      results.push({
        sample_id: conv.sample_id,
        question: qa.question,
        ground_truth: groundTruth,
        hypothesis,
        category: qa.category,
        category_name: catName,
        retrieved_context: context.map((c) => c.slice(0, 500)),
        retrieval_ms: Math.round(retrievalMs),
        answer_ms: Math.round(answerMs),
        correct: useJudge ? judgeLabel === "correct" : isCorrect,
        judge_label: judgeLabel
      });
    }
    if (limit > 0 && totalQ >= limit) break;
  }
  console.log("");
  const byCategory = {};
  let totalCorrect = 0;
  for (const r of results) {
    const key = `${r.category}-${r.category_name}`;
    if (!byCategory[key]) byCategory[key] = { correct: 0, total: 0, f1_sum: 0 };
    byCategory[key].total++;
    byCategory[key].f1_sum += tokenF1(r.ground_truth, r.hypothesis);
    if (r.correct) {
      byCategory[key].correct++;
      totalCorrect++;
    }
  }
  const scoreSummary = {};
  for (const [cat, s] of Object.entries(byCategory)) {
    scoreSummary[cat] = {
      accuracy: Math.round(s.correct / s.total * 1e4) / 100,
      avg_f1: Math.round(s.f1_sum / s.total * 1e4) / 1e4,
      total: s.total
    };
  }
  const overallF1 = results.length > 0 ? Math.round(results.reduce((a, r) => a + tokenF1(r.ground_truth, r.hypothesis), 0) / results.length * 1e4) / 1e4 : 0;
  const overallAccuracy = results.length > 0 ? Math.round(totalCorrect / results.length * 1e4) / 100 : 0;
  const retrievalLatencies = results.map((r) => r.retrieval_ms).sort((a, b) => a - b);
  const answerLatencies = results.map((r) => r.answer_ms);
  const runResult = {
    benchmark: "LoCoMo",
    timestamp: (/* @__PURE__ */ new Date()).toISOString(),
    dataset: basename(datasetPath),
    adapter_version: "v3-production-parity",
    total_questions: results.length,
    scores: {
      overall_f1: overallF1,
      overall_accuracy: overallAccuracy,
      by_category: scoreSummary
    },
    latency: {
      avg_retrieval_ms: Math.round(avg(retrievalLatencies)),
      avg_answer_ms: Math.round(avg(answerLatencies)),
      p95_retrieval_ms: Math.round(retrievalLatencies[Math.floor(retrievalLatencies.length * 0.95)] ?? 0),
      total_ingest_ms: Math.round(ingestMs),
      total_index_ms: Math.round(indexMs)
    },
    questions: results
  };
  if (!existsSync(outputDir)) mkdirSync(outputDir, { recursive: true });
  const outFile = join(outputDir, `locomo-${Date.now()}.json`);
  writeFileSync(outFile, JSON.stringify(runResult, null, 2));
  console.log(`
[locomo-v3] Results written to ${outFile}`);
  console.log(`[locomo-v3] Adapter: PRODUCTION CLI ONLY (v3)`);
  console.log(`[locomo-v3] Overall: F1=${overallF1}, Accuracy=${overallAccuracy}%`);
  console.log(`[locomo-v3] Ingest: ${Math.round(ingestMs)}ms | Indexing: ${Math.round(indexMs)}ms`);
  console.log(`[locomo-v3] Avg retrieval: ${runResult.latency.avg_retrieval_ms}ms, P95: ${runResult.latency.p95_retrieval_ms}ms`);
  for (const [cat, s] of Object.entries(scoreSummary)) {
    console.log(`  ${cat}: Accuracy=${s.accuracy}%, F1=${s.avg_f1} (n=${s.total})`);
  }
  rmSync(tmpDir, { recursive: true, force: true });
}
main().catch((e) => {
  console.error("[locomo-v3] Fatal:", e);
  process.exit(1);
});
