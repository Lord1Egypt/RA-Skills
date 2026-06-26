#!/usr/bin/env node
/**
 * @zouroboros/autoloop — Autonomous single-metric optimization loop
 *
 * Reads a program.md, creates a git branch, and loops:
 *   propose change → commit → run experiment → measure metric → keep or revert
 *
 * Inspired by karpathy/autoresearch. Generalized for any single-metric task.
 *
 * @license MIT
 */

import { execSync, spawn } from "child_process";
import { existsSync, readFileSync, writeFileSync, appendFileSync, mkdirSync } from "fs";
import { resolve, dirname, basename, join } from "path";
import { parseArgs } from "util";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ProgramConfig {
  name: string;
  objective: string;
  metric: {
    name: string;
    direction: "lower_is_better" | "higher_is_better";
    extract: string;
  };
  setup: string;
  targetFile: string;
  runCommand: string;
  readOnlyFiles: string[];
  constraints: {
    timeBudgetSeconds: number;
    maxExperiments: number;
    maxDurationHours: number;
    maxCostUSD: number;
  };
  stagnation: {
    threshold: number;
    doubleThreshold: number;
    tripleThreshold: number;
  };
  notes: string;
}

export interface ExperimentRecord {
  commit: string;
  metric: number;
  status: "keep" | "discard" | "crash";
  description: string;
  timestamp: string;
  durationMs: number;
}

interface LoopState {
  bestMetric: number;
  bestCommit: string;
  experimentCount: number;
  stagnationCount: number;
  totalCostUSD: number;
  startTime: number;
  results: ExperimentRecord[];
  branch: string;
}

// ---------------------------------------------------------------------------
// Shell helper (replaces Bun.$)
// ---------------------------------------------------------------------------

function sh(cmd: string, opts?: { cwd?: string; env?: Record<string, string>; timeout?: number }): { stdout: string; stderr: string; exitCode: number } {
  try {
    const stdout = execSync(cmd, {
      cwd: opts?.cwd,
      env: { ...process.env, ...opts?.env },
      timeout: opts?.timeout,
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
      maxBuffer: 10 * 1024 * 1024,
    });
    return { stdout: stdout || "", stderr: "", exitCode: 0 };
  } catch (err: any) {
    return {
      stdout: err.stdout?.toString() || "",
      stderr: err.stderr?.toString() || "",
      exitCode: err.status ?? 1,
    };
  }
}

// ---------------------------------------------------------------------------
// Parse program.md
// ---------------------------------------------------------------------------

export function parseProgram(path: string): ProgramConfig {
  const raw = readFileSync(path, "utf-8");

  const getSection = (heading: string): string => {
    const re = new RegExp(`^##\\s+${heading}\\s*$`, "im");
    const match = raw.match(re);
    if (!match || match.index === undefined) return "";
    const start = match.index + match[0].length;
    const nextHeading = raw.slice(start).search(/^##\s+/m);
    const end = nextHeading === -1 ? raw.length : start + nextHeading;
    return raw.slice(start, end).trim();
  };

  const getField = (section: string, field: string): string => {
    const re = new RegExp(`^-\\s+\\*\\*${field}\\*\\*:\\s*(.+)$`, "im");
    const match = section.match(re);
    return match ? match[1].trim() : "";
  };

  const nameMatch = raw.match(/^#\s+Program:\s*(.+)$/m);
  const name = nameMatch ? nameMatch[1].trim() : "unnamed";

  const metricSection = getSection("Metric");
  const metricName = getField(metricSection, "name");
  const direction = getField(metricSection, "direction") as "lower_is_better" | "higher_is_better";
  const extract = getField(metricSection, "extract").replace(/^`|`$/g, "");

  const constraintsSection = getSection("Constraints");
  const parseConstraint = (label: string, fallback: number): number => {
    const re = new RegExp(`\\*\\*${label}\\*\\*:\\s*([\\d.]+)`, "i");
    const m = constraintsSection.match(re);
    return m ? parseFloat(m[1]) : fallback;
  };

  const stagnationSection = getSection("Stagnation");
  const parseStagnation = (label: string, fallback: number): number => {
    const re = new RegExp(`\\*\\*${label}\\*\\*:\\s*(\\d+)`, "i");
    const m = stagnationSection.match(re);
    return m ? parseInt(m[1]) : fallback;
  };

  const readOnlySection = getSection("Read-Only Files");
  const readOnlyFiles = readOnlySection
    .split("\n")
    .map((l) => l.replace(/^-\s*/, "").trim())
    .filter(Boolean);

  const setupSection = getSection("Setup");
  const setupCode = setupSection.match(/```(?:bash)?\n([\s\S]*?)```/);

  const runSection = getSection("Run Command");
  const runCode = runSection.match(/```(?:bash)?\n([\s\S]*?)```/);

  const targetFile = getSection("Target File").split("\n")[0].replace(/^`|`$/g, "").trim();

  return {
    name,
    objective: getSection("Objective"),
    metric: {
      name: metricName,
      direction: direction || "lower_is_better",
      extract,
    },
    setup: setupCode ? setupCode[1].trim() : setupSection,
    targetFile,
    runCommand: runCode ? runCode[1].trim() : runSection.split("\n")[0],
    readOnlyFiles,
    constraints: {
      timeBudgetSeconds: parseConstraint("Time budget per run", 300),
      maxExperiments: parseConstraint("Max experiments", 100),
      maxDurationHours: parseConstraint("Max duration", 8),
      maxCostUSD: parseConstraint("Max cost", 10),
    },
    stagnation: {
      threshold: parseStagnation("Threshold", 10),
      doubleThreshold: parseStagnation("Double threshold", 20),
      tripleThreshold: parseStagnation("Triple threshold", 30),
    },
    notes: getSection("Notes"),
  };
}

// ---------------------------------------------------------------------------
// Git helpers
// ---------------------------------------------------------------------------

function gitShortHash(cwd?: string): string {
  return sh("git rev-parse --short HEAD", { cwd }).stdout.trim();
}

function gitResetLast(cwd?: string): void {
  sh("git reset --hard HEAD~1", { cwd });
}

function gitCommit(file: string, message: string, cwd?: string): string {
  sh(`git add ${file}`, { cwd });
  sh(`git commit -m "${message.replace(/"/g, '\\"')}"`, { cwd });
  return gitShortHash(cwd);
}

function gitBranchExists(branch: string, cwd?: string): boolean {
  return sh(`git rev-parse --verify ${branch}`, { cwd }).exitCode === 0;
}

// ---------------------------------------------------------------------------
// Experiment execution
// ---------------------------------------------------------------------------

function runExperiment(
  config: ProgramConfig,
  workDir: string
): { metric: number; crashed: boolean; error?: string; durationMs: number } {
  const timeoutSec = config.constraints.timeBudgetSeconds * 2;
  const start = Date.now();

  const result = sh(`timeout ${timeoutSec} bash -c '${config.runCommand.replace(/'/g, "'\\''")}'`, {
    cwd: workDir,
    timeout: timeoutSec * 1000 + 5000,
  });

  const durationMs = Date.now() - start;

  if (result.exitCode !== 0) {
    return { metric: 0, crashed: true, error: result.stderr.slice(0, 2000), durationMs };
  }

  const metricResult = sh(`bash -c '${config.metric.extract.replace(/'/g, "'\\''")}'`, { cwd: workDir });
  if (metricResult.exitCode !== 0) {
    return { metric: 0, crashed: true, error: `Metric extraction failed: ${metricResult.stderr.slice(0, 500)}`, durationMs };
  }

  const metricValue = parseFloat(metricResult.stdout.trim());
  if (isNaN(metricValue)) {
    return { metric: 0, crashed: true, error: `Metric not a number: "${metricResult.stdout.trim()}"`, durationMs };
  }

  return { metric: metricValue, crashed: false, durationMs };
}

function isBetter(current: number, best: number, direction: "lower_is_better" | "higher_is_better"): boolean {
  return direction === "lower_is_better" ? current < best : current > best;
}

// ---------------------------------------------------------------------------
// Agent interaction (proposal generation)
// ---------------------------------------------------------------------------

function proposeChange(
  config: ProgramConfig,
  state: LoopState,
  workDir: string,
  executor: string
): string {
  const targetContent = readFileSync(resolve(workDir, config.targetFile), "utf-8");

  const recentResults = state.results.slice(-20);
  const historyBlock = recentResults.length > 0
    ? recentResults.map((r) => `${r.status}\t${r.metric.toFixed(6)}\t${r.description}`).join("\n")
    : "(no experiments yet)";

  const stagnationMode =
    state.stagnationCount >= config.stagnation.doubleThreshold
      ? "RADICAL: Try combining the two best past approaches or fundamentally different strategies."
      : state.stagnationCount >= config.stagnation.threshold
        ? "EXPLORATORY: Standard tweaks aren't working. Try bigger structural changes."
        : "NORMAL: Propose a focused, incremental improvement.";

  const prompt = `You are an autonomous research agent optimizing: ${config.objective}

METRIC: ${config.metric.name} (${config.metric.direction.replace("_", " ")})
BEST SO FAR: ${state.bestMetric} (commit ${state.bestCommit})
EXPERIMENTS WITHOUT IMPROVEMENT: ${state.stagnationCount}
MODE: ${stagnationMode}

RECENT EXPERIMENT HISTORY (status, metric, description):
${historyBlock}

TARGET FILE (${config.targetFile}):
\`\`\`
${targetContent.slice(0, 8000)}
\`\`\`

READ-ONLY FILES (do NOT modify): ${config.readOnlyFiles.join(", ") || "none"}

SIMPLICITY CRITERION: All else being equal, simpler is better. A small improvement that adds
ugly complexity is not worth it. Removing something and getting equal or better results is a win.

${config.notes ? `NOTES: ${config.notes}` : ""}

YOUR TASK:
1. Analyze the history to avoid repeating failed approaches
2. Propose ONE focused change to ${config.targetFile}

MANDATORY RESPONSE FORMAT — your response will be DISCARDED if you deviate from this:
Line 1: HYPOTHESIS: <one sentence explaining the change and why it should improve the metric>
Line 2: blank line
Line 3+: The COMPLETE new file contents wrapped in triple backticks, like this:
\`\`\`
{ ...complete file contents here... }
\`\`\`

Do NOT add any explanation after the code block. Do NOT output partial file contents.
Do NOT modify any read-only files. Do NOT install new packages.`;

  // Write prompt to temp file to avoid shell escaping issues
  const promptFile = join(workDir, ".autoloop-prompt.tmp");
  writeFileSync(promptFile, prompt);

  // Call executor — supports any CLI that reads from file or stdin
  const result = sh(`${executor} < "${promptFile}"`, { cwd: workDir, timeout: 120000 });
  const output = result.stdout;

  // Clean up temp file
  try { require("fs").unlinkSync(promptFile); } catch {}

  if (result.exitCode !== 0 || !output.trim()) {
    throw new Error(`Executor failed: ${result.stderr.slice(0, 1000)}`);
  }

  const hypothesisMatch = output.match(/HYPOTHESIS:\s*(.+)/i);
  const hypothesis = hypothesisMatch ? hypothesisMatch[1].trim().slice(0, 200) : "unknown change";

  const codeMatch = output.match(/```[\w]*\n([\s\S]*?)```/);
  if (!codeMatch) {
    throw new Error("Agent did not output file content in code blocks");
  }

  const newContent = codeMatch[1];
  writeFileSync(resolve(workDir, config.targetFile), newContent);

  return hypothesis;
}

// ---------------------------------------------------------------------------
// Results TSV
// ---------------------------------------------------------------------------

function initResultsTSV(path: string): void {
  if (!existsSync(path)) {
    writeFileSync(path, "commit\tmetric\tstatus\tdescription\ttimestamp\tduration_ms\n");
  }
}

function appendResult(path: string, record: ExperimentRecord): void {
  const line = `${record.commit}\t${record.metric.toFixed(6)}\t${record.status}\t${record.description}\t${record.timestamp}\t${record.durationMs}\n`;
  appendFileSync(path, line);
}

// ---------------------------------------------------------------------------
// Summary report
// ---------------------------------------------------------------------------

function writeSummary(config: ProgramConfig, state: LoopState, workDir: string, reason: string): void {
  const keeps = state.results.filter((r) => r.status === "keep");
  const discards = state.results.filter((r) => r.status === "discard");
  const crashes = state.results.filter((r) => r.status === "crash");
  const elapsed = ((Date.now() - state.startTime) / 3600000).toFixed(1);

  const summary = `# Autoloop Summary: ${config.name}

**Stopped**: ${reason}
**Branch**: ${state.branch}
**Duration**: ${elapsed} hours
**Experiments**: ${state.experimentCount} total (${keeps.length} kept, ${discards.length} discarded, ${crashes.length} crashed)
**Best ${config.metric.name}**: ${state.bestMetric} (commit ${state.bestCommit})
**Improvement rate**: ${((keeps.length / Math.max(1, state.experimentCount)) * 100).toFixed(1)}%

## Top Improvements
${keeps
  .sort((a, b) =>
    config.metric.direction === "lower_is_better" ? a.metric - b.metric : b.metric - a.metric
  )
  .slice(0, 5)
  .map((r) => `- ${r.commit}: ${r.metric.toFixed(6)} — ${r.description}`)
  .join("\n")}

## Crash Log
${crashes.length === 0 ? "No crashes." : crashes.map((r) => `- ${r.commit}: ${r.description}`).join("\n")}
`;

  const summaryPath = join(workDir, `autoloop-summary-${config.name}.md`);
  writeFileSync(summaryPath, summary);
  console.log(`\nSummary written to ${summaryPath}`);
}

// ---------------------------------------------------------------------------
// Main loop
// ---------------------------------------------------------------------------

async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      program: { type: "string" },
      executor: { type: "string", default: "cat" },
      resume: { type: "boolean", default: false },
      "dry-run": { type: "boolean", default: false },
      help: { type: "boolean", default: false },
    },
    strict: true,
  });

  if (values.help) {
    console.log(`@zouroboros/autoloop — Autonomous single-metric optimization loop

Usage:
  autoloop --program <path/to/program.md> [--executor <command>] [--resume] [--dry-run]

Options:
  --program   Path to program.md specification (required)
  --executor  Shell command that reads a prompt from stdin and outputs a response.
              Examples:
                "openclaw ask"           (OpenClaw CLI)
                "claude --print"         (Claude Code CLI)
                "cat prompt.txt | llm"   (any LLM CLI)
              Default: "cat" (echo mode for testing)
  --resume    Resume from existing autoloop branch
  --dry-run   Parse program.md and show config without running

Part of the Zouroboros ecosystem. https://github.com/AlariqHQ/zouroboros`);
    process.exit(0);
  }

  if (!values.program) {
    console.error("Usage: autoloop --program <path/to/program.md> [--executor <command>] [--resume] [--dry-run]");
    process.exit(1);
  }

  const programPath = resolve(values.program);
  if (!existsSync(programPath)) {
    console.error(`Program file not found: ${programPath}`);
    process.exit(1);
  }

  const config = parseProgram(programPath);
  const workDir = dirname(programPath);
  const executor = values.executor || "cat";

  console.log(`\n=== Autoloop: ${config.name} ===`);
  console.log(`Objective: ${config.objective}`);
  console.log(`Metric: ${config.metric.name} (${config.metric.direction})`);
  console.log(`Target: ${config.targetFile}`);
  console.log(`Run: ${config.runCommand}`);
  console.log(`Executor: ${executor}`);
  console.log(`Limits: ${config.constraints.maxExperiments} experiments, ${config.constraints.maxDurationHours}h, $${config.constraints.maxCostUSD}`);

  if (values["dry-run"]) {
    console.log("\n[DRY RUN] Config parsed successfully. Exiting.");
    process.exit(0);
  }

  const dateTag = new Date().toISOString().slice(0, 10).replace(/-/g, "");
  const branchName = `autoloop/${config.name}-${dateTag}`;

  if (values.resume) {
    if (!gitBranchExists(branchName, workDir)) {
      console.error(`Branch ${branchName} not found. Cannot resume.`);
      process.exit(1);
    }
    sh(`git checkout ${branchName}`, { cwd: workDir });
    console.log(`Resumed branch: ${branchName}`);
  } else {
    if (gitBranchExists(branchName, workDir)) {
      let counter = 2;
      while (gitBranchExists(`${branchName}-${counter}`, workDir)) counter++;
      const uniqueBranch = `${branchName}-${counter}`;
      sh(`git checkout -b ${uniqueBranch}`, { cwd: workDir });
      console.log(`Created branch: ${uniqueBranch}`);
    } else {
      sh(`git checkout -b ${branchName}`, { cwd: workDir });
      console.log(`Created branch: ${branchName}`);
    }
  }

  if (config.setup) {
    console.log("\nRunning setup...");
    const setupResult = sh(`bash -c '${config.setup.replace(/'/g, "'\\''")}'`, { cwd: workDir });
    if (setupResult.exitCode !== 0) {
      console.error(`Setup failed: ${setupResult.stderr.slice(0, 1000)}`);
      process.exit(1);
    }
    console.log("Setup complete.");
  }

  const tsvPath = join(workDir, "results.tsv");
  initResultsTSV(tsvPath);

  console.log("\nRunning baseline...");
  const baseline = runExperiment(config, workDir);
  if (baseline.crashed) {
    console.error(`Baseline crashed: ${baseline.error}`);
    process.exit(1);
  }

  const baselineCommit = gitShortHash(workDir);
  console.log(`Baseline: ${config.metric.name} = ${baseline.metric} (commit ${baselineCommit})`);

  const state: LoopState = {
    bestMetric: baseline.metric,
    bestCommit: baselineCommit,
    experimentCount: 1,
    stagnationCount: 0,
    totalCostUSD: 0,
    startTime: Date.now(),
    results: [{
      commit: baselineCommit,
      metric: baseline.metric,
      status: "keep",
      description: "baseline",
      timestamp: new Date().toISOString(),
      durationMs: baseline.durationMs,
    }],
    branch: branchName,
  };

  appendResult(tsvPath, state.results[0]);

  console.log("\n--- Entering experiment loop (Ctrl+C to stop) ---\n");

  while (true) {
    const elapsedHours = (Date.now() - state.startTime) / 3600000;
    if (state.experimentCount >= config.constraints.maxExperiments) {
      writeSummary(config, state, workDir, `Max experiments reached (${config.constraints.maxExperiments})`);
      break;
    }
    if (elapsedHours >= config.constraints.maxDurationHours) {
      writeSummary(config, state, workDir, `Max duration reached (${config.constraints.maxDurationHours}h)`);
      break;
    }
    if (state.stagnationCount >= config.stagnation.tripleThreshold) {
      writeSummary(config, state, workDir, `Triple stagnation threshold (${config.stagnation.tripleThreshold} experiments with no improvement)`);
      break;
    }

    state.experimentCount++;
    const expNum = state.experimentCount;

    let hypothesis: string;
    try {
      hypothesis = proposeChange(config, state, workDir, executor);
    } catch (err: any) {
      console.log(`[${expNum}] SKIP — Agent failed: ${err.message?.slice(0, 200)}`);
      state.stagnationCount++;
      continue;
    }

    let commit: string;
    try {
      commit = gitCommit(
        config.targetFile,
        `experiment ${expNum}: ${hypothesis.slice(0, 100)}`,
        workDir
      );
    } catch {
      console.log(`[${expNum}] SKIP — Nothing to commit`);
      state.stagnationCount++;
      continue;
    }

    const result = runExperiment(config, workDir);

    if (result.crashed) {
      gitResetLast(workDir);
      state.stagnationCount++;
      const record: ExperimentRecord = { commit, metric: 0, status: "crash", description: `${hypothesis} — ${result.error?.slice(0, 100)}`, timestamp: new Date().toISOString(), durationMs: result.durationMs };
      state.results.push(record);
      appendResult(tsvPath, record);
      console.log(`[${expNum}] CRASH — ${hypothesis.slice(0, 80)}`);
    } else if (isBetter(result.metric, state.bestMetric, config.metric.direction)) {
      state.bestMetric = result.metric;
      state.bestCommit = commit;
      state.stagnationCount = 0;
      const record: ExperimentRecord = { commit, metric: result.metric, status: "keep", description: hypothesis, timestamp: new Date().toISOString(), durationMs: result.durationMs };
      state.results.push(record);
      appendResult(tsvPath, record);
      console.log(`[${expNum}] KEEP — ${config.metric.name} = ${result.metric} (best!) — ${hypothesis}`);
    } else {
      gitResetLast(workDir);
      state.stagnationCount++;
      const record: ExperimentRecord = { commit, metric: result.metric, status: "discard", description: hypothesis, timestamp: new Date().toISOString(), durationMs: result.durationMs };
      state.results.push(record);
      appendResult(tsvPath, record);
      console.log(`[${expNum}] DISCARD — ${config.metric.name} = ${result.metric} — ${hypothesis}`);
    }

    if (state.stagnationCount === config.stagnation.threshold) {
      console.log(`\nStagnation threshold reached (${config.stagnation.threshold}). Switching to exploratory mode.\n`);
    } else if (state.stagnationCount === config.stagnation.doubleThreshold) {
      console.log(`\nDouble stagnation (${config.stagnation.doubleThreshold}). Switching to radical mode.\n`);
    }
  }

  console.log(`\n=== Autoloop complete: ${state.experimentCount} experiments, best ${config.metric.name} = ${state.bestMetric} ===`);
}

process.on("SIGINT", () => {
  console.log("\n\nInterrupted by user. Progress saved via git commits and results.tsv.");
  process.exit(0);
});

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
