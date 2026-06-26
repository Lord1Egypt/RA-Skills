#!/usr/bin/env node
/**
 * Run all benchmarks and produce a unified report.
 *
 * Usage:
 *   node scripts/run-all.js [--judge] [--limit 50] [--benchmarks longmemeval,locomo,convomem]
 */

import { execSync } from "child_process";
import { existsSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { parseArgs } from "util";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, "../..");
const DATA_DIR = join(PROJECT_ROOT, "data");
const RUNS_DIR = join(DATA_DIR, "runs");
const ADAPTERS_DIR = join(PROJECT_ROOT, "dist/adapters");

const BENCHMARKS: Record<string, { adapter: string; datasetFlag: string; datasetCheck: string }> = {
  longmemeval: {
    adapter: "longmemeval-adapter.js",
    datasetFlag: `--dataset ${join(DATA_DIR, "longmemeval/longmemeval_s_cleaned.json")}`,
    datasetCheck: join(DATA_DIR, "longmemeval/longmemeval_s_cleaned.json"),
  },
  locomo: {
    adapter: "locomo-adapter.js",
    datasetFlag: `--dataset ${join(DATA_DIR, "locomo/locomo10.json")}`,
    datasetCheck: join(DATA_DIR, "locomo/locomo10.json"),
  },
  convomem: {
    adapter: "convomem-adapter.js",
    datasetFlag: `--dataset ${join(DATA_DIR, "convomem/core_benchmark")}`,
    datasetCheck: join(DATA_DIR, "convomem/core_benchmark"),
  },
};

function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      judge: { type: "boolean", default: false },
      limit: { type: "string", default: "50" },
      benchmarks: { type: "string", default: Object.keys(BENCHMARKS).join(",") },
      help: { type: "boolean", default: false },
    },
  });

  if (values.help) {
    console.log(`Usage: zouroboros-bench [--judge] [--limit N] [--benchmarks longmemeval,locomo,convomem]`);
    process.exit(0);
  }

  const selected = values.benchmarks!.split(",").map((s) => s.trim());
  const limit = values.limit!;
  const judge = values.judge!;

  if (!existsSync(RUNS_DIR)) mkdirSync(RUNS_DIR, { recursive: true });

  console.log("╔══════════════════════════════════════════╗");
  console.log("║     Zouroboros-Bench: Full Evaluation     ║");
  console.log("╚══════════════════════════════════════════╝");
  console.log(`Benchmarks: ${selected.join(", ")}`);
  console.log(`Limit: ${limit} questions per benchmark`);
  console.log(`Judge: ${judge ? "GPT-4o" : "heuristic"}`);
  console.log("");

  // Check datasets exist — skip missing ones instead of aborting
  const runnable: string[] = [];
  const missing: string[] = [];
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
    console.log(`  To download: bash scripts/download-datasets.sh\n`);
  }

  if (runnable.length === 0) {
    console.log(`No datasets available. Run: bash scripts/download-datasets.sh`);
    process.exit(1);
  }

  // Run each benchmark
  const results: Array<{ name: string; exitCode: number; duration: number }> = [];

  for (const name of runnable) {
    const bench = BENCHMARKS[name];
    const cmd = `node ${join(ADAPTERS_DIR, bench.adapter)} ${bench.datasetFlag} --output ${RUNS_DIR} --limit ${limit}${judge ? " --judge" : ""}`;

    console.log(`\n${"━".repeat(60)}`);
    console.log(`Running ${name.toUpperCase()}`);
    console.log(`  ${cmd}`);
    console.log(`${"━".repeat(60)}`);

    const t0 = Date.now();
    try {
      execSync(cmd, {
        stdio: "inherit",
        timeout: 1_800_000, // 30 min per benchmark
        cwd: PROJECT_ROOT,
      });
      results.push({ name, exitCode: 0, duration: Date.now() - t0 });
    } catch (e: any) {
      results.push({ name, exitCode: e.status ?? 1, duration: Date.now() - t0 });
      console.error(`  FAIL: ${name} failed with exit code ${e.status}`);
    }
  }

  // Summary
  console.log(`\n${"═".repeat(60)}`);
  console.log("BENCHMARK RUN SUMMARY");
  console.log(`${"═".repeat(60)}`);
  for (const r of results) {
    const status = r.exitCode === 0 ? "PASS" : "FAIL";
    const mins = (r.duration / 60_000).toFixed(1);
    console.log(`  ${status}  ${r.name.padEnd(15)} ${mins} min`);
  }
  for (const name of missing) {
    console.log(`  SKIP  ${name.padEnd(15)} (dataset missing)`);
  }

  // Generate report
  console.log(`\nGenerating unified report...`);
  try {
    execSync(`node ${join(PROJECT_ROOT, "dist/scripts/report.js")} --runs ${RUNS_DIR}`, {
      stdio: "inherit",
      timeout: 60_000,
      cwd: PROJECT_ROOT,
    });
  } catch {
    console.error("Report generation failed — run manually: node dist/scripts/report.js --runs data/runs/");
  }

  const anyFailed = results.some((r) => r.exitCode !== 0);
  process.exit(anyFailed ? 1 : 0);
}

main();
