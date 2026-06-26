#!/usr/bin/env node
var __require = /* @__PURE__ */ ((x) => typeof require !== "undefined" ? require : typeof Proxy !== "undefined" ? new Proxy(x, {
  get: (a, b) => (typeof require !== "undefined" ? require : a)[b]
}) : x)(function(x) {
  if (typeof require !== "undefined") return require.apply(this, arguments);
  throw Error('Dynamic require of "' + x + '" is not supported');
});

// src/autoloop.ts
import { execSync } from "child_process";
import { existsSync, readFileSync, writeFileSync, appendFileSync } from "fs";
import { resolve, dirname, join } from "path";
import { parseArgs } from "util";
function sh(cmd, opts) {
  try {
    const stdout = execSync(cmd, {
      cwd: opts?.cwd,
      env: { ...process.env, ...opts?.env },
      timeout: opts?.timeout,
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
      maxBuffer: 10 * 1024 * 1024
    });
    return { stdout: stdout || "", stderr: "", exitCode: 0 };
  } catch (err) {
    return {
      stdout: err.stdout?.toString() || "",
      stderr: err.stderr?.toString() || "",
      exitCode: err.status ?? 1
    };
  }
}
function parseProgram(path) {
  const raw = readFileSync(path, "utf-8");
  const getSection = (heading) => {
    const re = new RegExp(`^##\\s+${heading}\\s*$`, "im");
    const match = raw.match(re);
    if (!match || match.index === void 0) return "";
    const start = match.index + match[0].length;
    const nextHeading = raw.slice(start).search(/^##\s+/m);
    const end = nextHeading === -1 ? raw.length : start + nextHeading;
    return raw.slice(start, end).trim();
  };
  const getField = (section, field) => {
    const re = new RegExp(`^-\\s+\\*\\*${field}\\*\\*:\\s*(.+)$`, "im");
    const match = section.match(re);
    return match ? match[1].trim() : "";
  };
  const nameMatch = raw.match(/^#\s+Program:\s*(.+)$/m);
  const name = nameMatch ? nameMatch[1].trim() : "unnamed";
  const metricSection = getSection("Metric");
  const metricName = getField(metricSection, "name");
  const direction = getField(metricSection, "direction");
  const extract = getField(metricSection, "extract").replace(/^`|`$/g, "");
  const constraintsSection = getSection("Constraints");
  const parseConstraint = (label, fallback) => {
    const re = new RegExp(`\\*\\*${label}\\*\\*:\\s*([\\d.]+)`, "i");
    const m = constraintsSection.match(re);
    return m ? parseFloat(m[1]) : fallback;
  };
  const stagnationSection = getSection("Stagnation");
  const parseStagnation = (label, fallback) => {
    const re = new RegExp(`\\*\\*${label}\\*\\*:\\s*(\\d+)`, "i");
    const m = stagnationSection.match(re);
    return m ? parseInt(m[1]) : fallback;
  };
  const readOnlySection = getSection("Read-Only Files");
  const readOnlyFiles = readOnlySection.split("\n").map((l) => l.replace(/^-\s*/, "").trim()).filter(Boolean);
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
      extract
    },
    setup: setupCode ? setupCode[1].trim() : setupSection,
    targetFile,
    runCommand: runCode ? runCode[1].trim() : runSection.split("\n")[0],
    readOnlyFiles,
    constraints: {
      timeBudgetSeconds: parseConstraint("Time budget per run", 300),
      maxExperiments: parseConstraint("Max experiments", 100),
      maxDurationHours: parseConstraint("Max duration", 8),
      maxCostUSD: parseConstraint("Max cost", 10)
    },
    stagnation: {
      threshold: parseStagnation("Threshold", 10),
      doubleThreshold: parseStagnation("Double threshold", 20),
      tripleThreshold: parseStagnation("Triple threshold", 30)
    },
    notes: getSection("Notes")
  };
}
function gitShortHash(cwd) {
  return sh("git rev-parse --short HEAD", { cwd }).stdout.trim();
}
function gitResetLast(cwd) {
  sh("git reset --hard HEAD~1", { cwd });
}
function gitCommit(file, message, cwd) {
  sh(`git add ${file}`, { cwd });
  sh(`git commit -m "${message.replace(/"/g, '\\"')}"`, { cwd });
  return gitShortHash(cwd);
}
function gitBranchExists(branch, cwd) {
  return sh(`git rev-parse --verify ${branch}`, { cwd }).exitCode === 0;
}
function runExperiment(config, workDir) {
  const timeoutSec = config.constraints.timeBudgetSeconds * 2;
  const start = Date.now();
  const result = sh(`timeout ${timeoutSec} bash -c '${config.runCommand.replace(/'/g, "'\\''")}'`, {
    cwd: workDir,
    timeout: timeoutSec * 1e3 + 5e3
  });
  const durationMs = Date.now() - start;
  if (result.exitCode !== 0) {
    return { metric: 0, crashed: true, error: result.stderr.slice(0, 2e3), durationMs };
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
function isBetter(current, best, direction) {
  return direction === "lower_is_better" ? current < best : current > best;
}
function proposeChange(config, state, workDir, executor) {
  const targetContent = readFileSync(resolve(workDir, config.targetFile), "utf-8");
  const recentResults = state.results.slice(-20);
  const historyBlock = recentResults.length > 0 ? recentResults.map((r) => `${r.status}	${r.metric.toFixed(6)}	${r.description}`).join("\n") : "(no experiments yet)";
  const stagnationMode = state.stagnationCount >= config.stagnation.doubleThreshold ? "RADICAL: Try combining the two best past approaches or fundamentally different strategies." : state.stagnationCount >= config.stagnation.threshold ? "EXPLORATORY: Standard tweaks aren't working. Try bigger structural changes." : "NORMAL: Propose a focused, incremental improvement.";
  const prompt = `You are an autonomous research agent optimizing: ${config.objective}

METRIC: ${config.metric.name} (${config.metric.direction.replace("_", " ")})
BEST SO FAR: ${state.bestMetric} (commit ${state.bestCommit})
EXPERIMENTS WITHOUT IMPROVEMENT: ${state.stagnationCount}
MODE: ${stagnationMode}

RECENT EXPERIMENT HISTORY (status, metric, description):
${historyBlock}

TARGET FILE (${config.targetFile}):
\`\`\`
${targetContent.slice(0, 8e3)}
\`\`\`

READ-ONLY FILES (do NOT modify): ${config.readOnlyFiles.join(", ") || "none"}

SIMPLICITY CRITERION: All else being equal, simpler is better. A small improvement that adds
ugly complexity is not worth it. Removing something and getting equal or better results is a win.

${config.notes ? `NOTES: ${config.notes}` : ""}

YOUR TASK:
1. Analyze the history to avoid repeating failed approaches
2. Propose ONE focused change to ${config.targetFile}

MANDATORY RESPONSE FORMAT \u2014 your response will be DISCARDED if you deviate from this:
Line 1: HYPOTHESIS: <one sentence explaining the change and why it should improve the metric>
Line 2: blank line
Line 3+: The COMPLETE new file contents wrapped in triple backticks, like this:
\`\`\`
{ ...complete file contents here... }
\`\`\`

Do NOT add any explanation after the code block. Do NOT output partial file contents.
Do NOT modify any read-only files. Do NOT install new packages.`;
  const promptFile = join(workDir, ".autoloop-prompt.tmp");
  writeFileSync(promptFile, prompt);
  const result = sh(`${executor} < "${promptFile}"`, { cwd: workDir, timeout: 12e4 });
  const output = result.stdout;
  try {
    __require("fs").unlinkSync(promptFile);
  } catch {
  }
  if (result.exitCode !== 0 || !output.trim()) {
    throw new Error(`Executor failed: ${result.stderr.slice(0, 1e3)}`);
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
function initResultsTSV(path) {
  if (!existsSync(path)) {
    writeFileSync(path, "commit	metric	status	description	timestamp	duration_ms\n");
  }
}
function appendResult(path, record) {
  const line = `${record.commit}	${record.metric.toFixed(6)}	${record.status}	${record.description}	${record.timestamp}	${record.durationMs}
`;
  appendFileSync(path, line);
}
function writeSummary(config, state, workDir, reason) {
  const keeps = state.results.filter((r) => r.status === "keep");
  const discards = state.results.filter((r) => r.status === "discard");
  const crashes = state.results.filter((r) => r.status === "crash");
  const elapsed = ((Date.now() - state.startTime) / 36e5).toFixed(1);
  const summary = `# Autoloop Summary: ${config.name}

**Stopped**: ${reason}
**Branch**: ${state.branch}
**Duration**: ${elapsed} hours
**Experiments**: ${state.experimentCount} total (${keeps.length} kept, ${discards.length} discarded, ${crashes.length} crashed)
**Best ${config.metric.name}**: ${state.bestMetric} (commit ${state.bestCommit})
**Improvement rate**: ${(keeps.length / Math.max(1, state.experimentCount) * 100).toFixed(1)}%

## Top Improvements
${keeps.sort(
    (a, b) => config.metric.direction === "lower_is_better" ? a.metric - b.metric : b.metric - a.metric
  ).slice(0, 5).map((r) => `- ${r.commit}: ${r.metric.toFixed(6)} \u2014 ${r.description}`).join("\n")}

## Crash Log
${crashes.length === 0 ? "No crashes." : crashes.map((r) => `- ${r.commit}: ${r.description}`).join("\n")}
`;
  const summaryPath = join(workDir, `autoloop-summary-${config.name}.md`);
  writeFileSync(summaryPath, summary);
  console.log(`
Summary written to ${summaryPath}`);
}
async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      program: { type: "string" },
      executor: { type: "string", default: "cat" },
      resume: { type: "boolean", default: false },
      "dry-run": { type: "boolean", default: false },
      help: { type: "boolean", default: false }
    },
    strict: true
  });
  if (values.help) {
    console.log(`@zouroboros/autoloop \u2014 Autonomous single-metric optimization loop

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
  console.log(`
=== Autoloop: ${config.name} ===`);
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
  const dateTag = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10).replace(/-/g, "");
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
      console.error(`Setup failed: ${setupResult.stderr.slice(0, 1e3)}`);
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
  const state = {
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
      timestamp: (/* @__PURE__ */ new Date()).toISOString(),
      durationMs: baseline.durationMs
    }],
    branch: branchName
  };
  appendResult(tsvPath, state.results[0]);
  console.log("\n--- Entering experiment loop (Ctrl+C to stop) ---\n");
  while (true) {
    const elapsedHours = (Date.now() - state.startTime) / 36e5;
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
    let hypothesis;
    try {
      hypothesis = proposeChange(config, state, workDir, executor);
    } catch (err) {
      console.log(`[${expNum}] SKIP \u2014 Agent failed: ${err.message?.slice(0, 200)}`);
      state.stagnationCount++;
      continue;
    }
    let commit;
    try {
      commit = gitCommit(
        config.targetFile,
        `experiment ${expNum}: ${hypothesis.slice(0, 100)}`,
        workDir
      );
    } catch {
      console.log(`[${expNum}] SKIP \u2014 Nothing to commit`);
      state.stagnationCount++;
      continue;
    }
    const result = runExperiment(config, workDir);
    if (result.crashed) {
      gitResetLast(workDir);
      state.stagnationCount++;
      const record = { commit, metric: 0, status: "crash", description: `${hypothesis} \u2014 ${result.error?.slice(0, 100)}`, timestamp: (/* @__PURE__ */ new Date()).toISOString(), durationMs: result.durationMs };
      state.results.push(record);
      appendResult(tsvPath, record);
      console.log(`[${expNum}] CRASH \u2014 ${hypothesis.slice(0, 80)}`);
    } else if (isBetter(result.metric, state.bestMetric, config.metric.direction)) {
      state.bestMetric = result.metric;
      state.bestCommit = commit;
      state.stagnationCount = 0;
      const record = { commit, metric: result.metric, status: "keep", description: hypothesis, timestamp: (/* @__PURE__ */ new Date()).toISOString(), durationMs: result.durationMs };
      state.results.push(record);
      appendResult(tsvPath, record);
      console.log(`[${expNum}] KEEP \u2014 ${config.metric.name} = ${result.metric} (best!) \u2014 ${hypothesis}`);
    } else {
      gitResetLast(workDir);
      state.stagnationCount++;
      const record = { commit, metric: result.metric, status: "discard", description: hypothesis, timestamp: (/* @__PURE__ */ new Date()).toISOString(), durationMs: result.durationMs };
      state.results.push(record);
      appendResult(tsvPath, record);
      console.log(`[${expNum}] DISCARD \u2014 ${config.metric.name} = ${result.metric} \u2014 ${hypothesis}`);
    }
    if (state.stagnationCount === config.stagnation.threshold) {
      console.log(`
Stagnation threshold reached (${config.stagnation.threshold}). Switching to exploratory mode.
`);
    } else if (state.stagnationCount === config.stagnation.doubleThreshold) {
      console.log(`
Double stagnation (${config.stagnation.doubleThreshold}). Switching to radical mode.
`);
    }
  }
  console.log(`
=== Autoloop complete: ${state.experimentCount} experiments, best ${config.metric.name} = ${state.bestMetric} ===`);
}
process.on("SIGINT", () => {
  console.log("\n\nInterrupted by user. Progress saved via git commits and results.tsv.");
  process.exit(0);
});
main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
export {
  parseProgram
};
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
