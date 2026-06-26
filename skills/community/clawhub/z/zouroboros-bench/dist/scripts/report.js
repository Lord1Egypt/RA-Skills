#!/usr/bin/env node

// src/scripts/report.ts
import { readdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { parseArgs } from "util";
function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      runs: { type: "string", default: "data/runs" },
      output: { type: "string" },
      help: { type: "boolean", default: false }
    }
  });
  if (values.help) {
    console.log(`Usage: node scripts/report.js --runs <dir> [--output <file>]`);
    process.exit(0);
  }
  const runsDir = values.runs;
  const files = readdirSync(runsDir).filter((f) => f.endsWith(".json")).sort();
  if (files.length === 0) {
    console.log("No run files found in", runsDir);
    process.exit(1);
  }
  const latestRuns = /* @__PURE__ */ new Map();
  for (const file of files) {
    try {
      const data = JSON.parse(readFileSync(join(runsDir, file), "utf-8"));
      const existing = latestRuns.get(data.benchmark);
      if (!existing || data.timestamp > existing.timestamp) {
        latestRuns.set(data.benchmark, data);
      }
    } catch {
    }
  }
  const supermemoryBaselines = {
    LongMemEval: {
      "overall": 81.6,
      "single-session-user": 97.14,
      "single-session-assistant": 96.43,
      "single-session-preference": 70,
      "knowledge-update": 88.46,
      "temporal-reasoning": 76.69,
      "multi-session": 71.43
    },
    LoCoMo: {},
    ConvoMem: {}
  };
  const lines = [];
  const ts = (/* @__PURE__ */ new Date()).toISOString().split("T")[0];
  lines.push(`# Zouroboros Benchmark Report`);
  lines.push(`> Generated: ${ts}`);
  lines.push(`> Engine: Zouroboros Memory System v4.0`);
  lines.push(`> Search: Hybrid (BM25 + Vector + Graph-Boost RRF)`);
  lines.push(``);
  lines.push(`## Summary`);
  lines.push(``);
  lines.push(`| Benchmark | Questions | Accuracy | Avg Retrieval | P95 Retrieval | Avg Answer |`);
  lines.push(`|-----------|-----------|----------|---------------|---------------|------------|`);
  for (const [name, run] of latestRuns) {
    const accuracy = run.scores.overall_accuracy ?? run.scores.overall_f1 ?? "\u2014";
    lines.push(
      `| ${name} | ${run.total_questions} | ${accuracy}% | ${run.latency.avg_retrieval_ms}ms | ${run.latency.p95_retrieval_ms}ms | ${run.latency.avg_answer_ms}ms |`
    );
  }
  lines.push(``);
  for (const [name, run] of latestRuns) {
    lines.push(`## ${name}`);
    lines.push(``);
    lines.push(`- **Dataset:** ${run.dataset}`);
    lines.push(`- **Questions:** ${run.total_questions}`);
    lines.push(`- **Run:** ${run.timestamp}`);
    lines.push(``);
    if (name === "LongMemEval" && run.scores.by_type) {
      lines.push(`### Accuracy by Question Type`);
      lines.push(``);
      lines.push(`| Type | Zouroboros | Supermemory | \u0394 |`);
      lines.push(`|------|-----------|-------------|---|`);
      const smBaseline = supermemoryBaselines.LongMemEval ?? {};
      for (const [type, data] of Object.entries(run.scores.by_type)) {
        const sm = smBaseline[type];
        const delta = sm != null ? `${(data.accuracy - sm).toFixed(1)}` : "\u2014";
        const smStr = sm != null ? `${sm}%` : "\u2014";
        lines.push(`| ${type} | ${data.accuracy}% (${data.correct}/${data.total}) | ${smStr} | ${delta} |`);
      }
      const overallSm = smBaseline.overall;
      if (overallSm != null) {
        const delta = (run.scores.overall_accuracy - overallSm).toFixed(1);
        lines.push(`| **Overall** | **${run.scores.overall_accuracy}%** | **${overallSm}%** | **${delta}** |`);
      }
      lines.push(``);
    }
    if (name === "LoCoMo" && run.scores.by_category) {
      lines.push(`### Scores by Category`);
      lines.push(``);
      lines.push(`| Category | Avg F1 | Accuracy | Count |`);
      lines.push(`|----------|--------|----------|-------|`);
      for (const [cat, data] of Object.entries(run.scores.by_category)) {
        lines.push(`| ${cat} | ${data.avg_f1} | ${data.accuracy}% | ${data.total} |`);
      }
      lines.push(``);
    }
    if (name === "ConvoMem" && run.scores.accuracy_matrix) {
      lines.push(`### Accuracy Matrix (Category \xD7 Context Size)`);
      lines.push(``);
      const allSizes = /* @__PURE__ */ new Set();
      for (const sizes of Object.values(run.scores.accuracy_matrix)) {
        for (const s of Object.keys(sizes)) allSizes.add(Number(s));
      }
      const sortedSizes = [...allSizes].sort((a, b) => a - b);
      lines.push(`| Category | ${sortedSizes.map((s) => `${s}`).join(" | ")} |`);
      lines.push(`|----------|${sortedSizes.map(() => "------").join("|")}|`);
      for (const [cat, sizes] of Object.entries(run.scores.accuracy_matrix)) {
        const vals = sortedSizes.map((s) => sizes[s] != null ? `${sizes[s]}%` : "\u2014");
        lines.push(`| ${cat} | ${vals.join(" | ")} |`);
      }
      lines.push(``);
    }
    if (name === "ZouroBench" && run.scores.by_category) {
      lines.push(`### Accuracy by Category`);
      lines.push(``);
      lines.push(`| Category | Accuracy | Correct | Total |`);
      lines.push(`|----------|----------|---------|-------|`);
      for (const [cat, data] of Object.entries(run.scores.by_category)) {
        lines.push(`| ${cat} | ${data.accuracy}% | ${data.correct} | ${data.total} |`);
      }
      if (run.scores.overall_accuracy != null) {
        const totalCorrect = Object.values(run.scores.by_category).reduce((s, c) => s + c.correct, 0);
        const totalQ = Object.values(run.scores.by_category).reduce((s, c) => s + c.total, 0);
        lines.push(`| **Overall** | **${run.scores.overall_accuracy}%** | **${totalCorrect}** | **${totalQ}** |`);
      }
      lines.push(``);
      if (run.scores.by_type) {
        lines.push(`### Accuracy by Question Type`);
        lines.push(``);
        lines.push(`| Category : Type | Accuracy | Correct | Total |`);
        lines.push(`|-----------------|----------|---------|-------|`);
        for (const [type, data] of Object.entries(run.scores.by_type)) {
          lines.push(`| ${type} | ${data.accuracy}% | ${data.correct} | ${data.total} |`);
        }
        lines.push(``);
      }
    }
    lines.push(`### Latency`);
    lines.push(``);
    lines.push(`| Metric | Value |`);
    lines.push(`|--------|-------|`);
    lines.push(`| Avg Retrieval | ${run.latency.avg_retrieval_ms}ms |`);
    lines.push(`| P95 Retrieval | ${run.latency.p95_retrieval_ms}ms |`);
    lines.push(`| Avg Answer Gen | ${run.latency.avg_answer_ms}ms |`);
    lines.push(``);
  }
  lines.push(`## Methodology`);
  lines.push(``);
  lines.push(`### Search Pipeline`);
  lines.push(`1. **Ingest:** Benchmark conversations stored as facts in temporary SQLite DB`);
  lines.push(`2. **Index:** nomic-embed-text (768-dim) embeddings generated for all facts`);
  lines.push(`3. **Retrieve:** Hybrid search (BM25 FTS5 + vector cosine + graph-boost RRF fusion)`);
  lines.push(`4. **Answer:** qwen2.5:7b generates answer from top-5 retrieved contexts`);
  lines.push(`5. **Judge:** GPT-4o binary judge (when --judge enabled) or heuristic F1 match`);
  lines.push(``);
  lines.push(`### System Under Test`);
  lines.push(`- **Engine:** Zouroboros Memory System v4.0`);
  lines.push(`- **Database:** SQLite (better-sqlite3) with FTS5 + WAL mode`);
  lines.push(`- **Embeddings:** nomic-embed-text (768-dim, Ollama)`);
  lines.push(`- **Search:** RRF fusion (BM25: 0.60, Graph: 0.15, Freshness: 0.15, Confidence: 0.10)`);
  lines.push(`- **Answer Model:** qwen2.5:7b (local Ollama)`);
  lines.push(`- **No cloud dependencies** for retrieval (Ollama-only pipeline)`);
  lines.push(``);
  lines.push(`### Comparison Notes`);
  lines.push(`- Supermemory uses cloud-hosted infrastructure with proprietary indexing`);
  lines.push(`- Zouroboros runs entirely on local hardware (single-node Ollama)`);
  lines.push(`- Supermemory's LongMemEval scores are from their published research page`);
  lines.push(`- Direct comparison is informative but not apples-to-apples (different compute budgets)`);
  lines.push(``);
  const report = lines.join("\n");
  const outFile = values.output ?? join(runsDir, `REPORT-${ts}.md`);
  writeFileSync(outFile, report);
  console.log(`[report] Written to ${outFile}`);
  console.log(`[report] ${latestRuns.size} benchmarks included`);
}
main();
