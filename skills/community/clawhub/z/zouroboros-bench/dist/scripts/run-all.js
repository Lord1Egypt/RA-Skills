#!/usr/bin/env node

// src/scripts/run-all.ts
import { execSync } from "child_process";
import { existsSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { parseArgs } from "util";
import { fileURLToPath } from "url";
var __dirname = dirname(fileURLToPath(import.meta.url));
var PROJECT_ROOT = join(__dirname, "../..");
var DATA_DIR = join(PROJECT_ROOT, "data");
var RUNS_DIR = join(DATA_DIR, "runs");
var ADAPTERS_DIR = join(PROJECT_ROOT, "dist/adapters");
var BENCHMARKS = {
  longmemeval: {
    adapter: "longmemeval-adapter.js",
    datasetFlag: `--dataset ${join(DATA_DIR, "longmemeval/longmemeval_s_cleaned.json")}`,
    datasetCheck: join(DATA_DIR, "longmemeval/longmemeval_s_cleaned.json")
  },
  locomo: {
    adapter: "locomo-adapter.js",
    datasetFlag: `--dataset ${join(DATA_DIR, "locomo/locomo10.json")}`,
    datasetCheck: join(DATA_DIR, "locomo/locomo10.json")
  },
  convomem: {
    adapter: "convomem-adapter.js",
    datasetFlag: `--dataset ${join(DATA_DIR, "convomem/core_benchmark")}`,
    datasetCheck: join(DATA_DIR, "convomem/core_benchmark")
  }
};
function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      judge: { type: "boolean", default: false },
      limit: { type: "string", default: "50" },
      benchmarks: { type: "string", default: Object.keys(BENCHMARKS).join(",") },
      help: { type: "boolean", default: false }
    }
  });
  if (values.help) {
    console.log(`Usage: zouroboros-bench [--judge] [--limit N] [--benchmarks longmemeval,locomo,convomem]`);
    process.exit(0);
  }
  const selected = values.benchmarks.split(",").map((s) => s.trim());
  const limit = values.limit;
  const judge = values.judge;
  if (!existsSync(RUNS_DIR)) mkdirSync(RUNS_DIR, { recursive: true });
  console.log("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557");
  console.log("\u2551     Zouroboros-Bench: Full Evaluation     \u2551");
  console.log("\u255A\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255D");
  console.log(`Benchmarks: ${selected.join(", ")}`);
  console.log(`Limit: ${limit} questions per benchmark`);
  console.log(`Judge: ${judge ? "GPT-4o" : "heuristic"}`);
  console.log("");
  const runnable = [];
  const missing = [];
  for (const name of selected) {
    const bench = BENCHMARKS[name];
    if (!bench) {
      console.error(`Unknown benchmark: ${name}`);
      process.exit(1);
    }
    if (existsSync(bench.datasetCheck)) {
      runnable.push(name);
    } else {
      missing.push(name);
    }
  }
  if (missing.length > 0) {
    console.log(`Skipping missing datasets: ${missing.join(", ")}`);
    console.log(`  To download: bash scripts/download-datasets.sh
`);
  }
  if (runnable.length === 0) {
    console.log(`No datasets available. Run: bash scripts/download-datasets.sh`);
    process.exit(1);
  }
  const results = [];
  for (const name of runnable) {
    const bench = BENCHMARKS[name];
    const cmd = `node ${join(ADAPTERS_DIR, bench.adapter)} ${bench.datasetFlag} --output ${RUNS_DIR} --limit ${limit}${judge ? " --judge" : ""}`;
    console.log(`
${"\u2501".repeat(60)}`);
    console.log(`Running ${name.toUpperCase()}`);
    console.log(`  ${cmd}`);
    console.log(`${"\u2501".repeat(60)}`);
    const t0 = Date.now();
    try {
      execSync(cmd, {
        stdio: "inherit",
        timeout: 18e5,
        // 30 min per benchmark
        cwd: PROJECT_ROOT
      });
      results.push({ name, exitCode: 0, duration: Date.now() - t0 });
    } catch (e) {
      results.push({ name, exitCode: e.status ?? 1, duration: Date.now() - t0 });
      console.error(`  FAIL: ${name} failed with exit code ${e.status}`);
    }
  }
  console.log(`
${"\u2550".repeat(60)}`);
  console.log("BENCHMARK RUN SUMMARY");
  console.log(`${"\u2550".repeat(60)}`);
  for (const r of results) {
    const status = r.exitCode === 0 ? "PASS" : "FAIL";
    const mins = (r.duration / 6e4).toFixed(1);
    console.log(`  ${status}  ${r.name.padEnd(15)} ${mins} min`);
  }
  for (const name of missing) {
    console.log(`  SKIP  ${name.padEnd(15)} (dataset missing)`);
  }
  console.log(`
Generating unified report...`);
  try {
    execSync(`node ${join(PROJECT_ROOT, "dist/scripts/report.js")} --runs ${RUNS_DIR}`, {
      stdio: "inherit",
      timeout: 6e4,
      cwd: PROJECT_ROOT
    });
  } catch {
    console.error("Report generation failed \u2014 run manually: node dist/scripts/report.js --runs data/runs/");
  }
  const anyFailed = results.some((r) => r.exitCode !== 0);
  process.exit(anyFailed ? 1 : 0);
}
main();
