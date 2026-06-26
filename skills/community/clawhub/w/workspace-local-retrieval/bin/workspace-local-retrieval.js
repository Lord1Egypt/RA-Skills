#!/usr/bin/env node
const { spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const ROOT = path.resolve(__dirname, "..");
const SCRIPTS_DIR = path.join(ROOT, "scripts");
const PYTHON = process.env.PYTHON || "python3";
const DEFAULT_DEST = path.resolve(process.cwd(), "retrieval");
const DEFAULT_WORKSPACE_ROOT = process.cwd();

function resolveScript(name) {
  return path.join(SCRIPTS_DIR, name);
}

function safeParseJSON(text) {
  try {
    return JSON.parse(text);
  } catch (error) {
    console.error("Failed to parse JSON output from prerequisite check:", error.message);
    console.error(text);
    process.exit(1);
  }
}

function summarizePayload(payload) {
  if (!payload?.results) {
    console.warn("Prerequisite check produced no results.");
    return [];
  }
  console.log("\nPrerequisite summary:");
  payload.results.forEach((entry) => {
    const version = entry.version ? ` [${entry.version}]` : "";
    const status = entry.ok ? "✓" : "✗";
    const detail = typeof entry.details === "object" ? JSON.stringify(entry.details) : entry.details;
    console.log(`- ${status} ${entry.name}${version} (${entry.required}) · ${detail}`);
  });
  if (Array.isArray(payload.recommendations) && payload.recommendations.length) {
    console.log("Recommendations:");
    payload.recommendations.forEach((rec) => console.log(`- ${rec}`));
  }
  const blocking = payload.results.filter(
    (entry) => entry.ok === false && !/optional/i.test(entry.required || "")
  );
  return blocking;
}

function runPrereqCheck() {
  const result = spawnSync(PYTHON, [resolveScript("check_retrieval_prereqs.py"), "--json"], {
    encoding: "utf-8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  if (result.error) {
    console.error("Failed to run prerequisite check:", result.error.message);
    process.exit(1);
  }
  if (result.status !== 0) {
    console.error("Prerequisite check exited with non-zero status.");
    console.error(result.stderr);
    process.exit(result.status);
  }
  const payload = safeParseJSON(result.stdout);
  const blocking = summarizePayload(payload);
  return { payload, blocking };
}

function parseFlags(argv) {
  const options = { dest: null, workspaceRoot: null, force: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dest") {
      i += 1;
      options.dest = argv[i];
    } else if (arg === "--workspace-root") {
      i += 1;
      options.workspaceRoot = argv[i];
    } else if (arg === "--force") {
      options.force = true;
    } else if (arg === "--help") {
      showHelp();
      process.exit(0);
    } else {
      console.error(`Unknown flag: ${arg}`);
      showHelp();
      process.exit(1);
    }
  }
  return options;
}

function ensureDirectory(dirPath) {
  try {
    fs.mkdirSync(dirPath, { recursive: true });
  } catch (error) {
    console.error(`Unable to create directory ${dirPath}:`, error.message);
    process.exit(1);
  }
}

function installCommand(argv) {
  const options = parseFlags(argv);
  const { blocking } = runPrereqCheck();
  if (blocking.length) {
    console.warn("\nWarning: Missing required prerequisites detected. Review the summary above before proceeding.");
  }
  const dest = path.resolve(options.dest || DEFAULT_DEST);
  const workspaceRoot = path.resolve(options.workspaceRoot || DEFAULT_WORKSPACE_ROOT);
  ensureDirectory(dest);
  const bootstrapArgs = [
    resolveScript("bootstrap_workspace_retrieval.py"),
    "--dest",
    dest,
    "--workspace-root",
    workspaceRoot,
  ];
  if (options.force) {
    bootstrapArgs.push("--force");
  }
  const bootstrap = spawnSync(PYTHON, bootstrapArgs, { stdio: "inherit" });
  if (bootstrap.error) {
    console.error("Failed to run bootstrap script:", bootstrap.error.message);
    process.exit(1);
  }
  if (bootstrap.status !== 0) {
    console.error("Bootstrap script exited with non-zero status.");
    process.exit(bootstrap.status);
  }
  console.log("\nDone: retrieval templates written.");
  console.log(`- config directory: ${path.join(dest, "config")}`);
  console.log(`- workspace root: ${workspaceRoot}`);
  console.log("Next: run your chosen indexing/embedding workflow or a refresh script.");
}

function checkCommand() {
  const { blocking } = runPrereqCheck();
  if (blocking.length) {
    process.exitCode = 1;
  }
}

function showHelp() {
  console.log(`workspace-local-retrieval CLI

Usage:
  workspace-local-retrieval install [--dest <path>] [--workspace-root <root>] [--force]
  workspace-local-retrieval check

Commands:
  install          Run prereq checks and bootstrap retrieval/ config (default command when no subcommand is provided).
  check            Run the prerequisite assessment only and show status.

Options:
  --dest           Destination directory for generated config (default: ./retrieval)
  --workspace-root Workspace root to embed into templates (default: current working dir)
  --force          Overwrite existing templates even if files already exist
`);
}

(function main() {
  const argv = process.argv.slice(2);
  const command = argv[0]?.toLowerCase();
  if (!command || command === "install") {
    installCommand(command ? argv.slice(1) : []);
  } else if (command === "check") {
    checkCommand();
  } else if (command === "help" || command === "-h" || command === "--help") {
    showHelp();
  } else {
    console.error(`Unknown command: ${command}`);
    showHelp();
    process.exit(1);
  }
})();
