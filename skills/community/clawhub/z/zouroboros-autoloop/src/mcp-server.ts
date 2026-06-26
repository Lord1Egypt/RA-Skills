#!/usr/bin/env node
/**
 * @zouroboros/autoloop MCP Server (stdio transport)
 *
 * Exposes autonomous optimization loop as MCP tools.
 * Works with any MCP-compatible client (Claude Desktop, OpenClaw, etc.)
 *
 * @license MIT
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { execSync } from "child_process";
import { existsSync, readFileSync, readdirSync, unlinkSync, statSync } from "fs";
import { join, basename, dirname } from "path";
import { parseArgs } from "util";

// --- Config (from CLI args or env) ---
const { values: cliArgs } = parseArgs({
  args: process.argv.slice(2),
  options: {
    "script-dir": { type: "string", default: dirname(new URL(import.meta.url).pathname) },
    "results-dir": { type: "string", default: process.cwd() },
  },
  strict: false,
});

const SCRIPT_DIR = cliArgs["script-dir"] as string;
const RESULTS_DIR = cliArgs["results-dir"] as string;

function getAutoloopScript(): string {
  const candidates = [
    join(SCRIPT_DIR, "autoloop.js"),
    join(SCRIPT_DIR, "autoloop.ts"),
  ];
  for (const c of candidates) {
    if (existsSync(c)) return c;
  }
  return "autoloop";
}

// --- Helpers ---
function findResultsTsv(programPath: string): string | null {
  const dir = dirname(programPath);
  const tsvPath = join(dir, "results.tsv");
  return existsSync(tsvPath) ? tsvPath : null;
}

function findGitBranch(projectDir: string): string | null {
  const headPath = join(projectDir, ".git", "HEAD");
  if (!existsSync(headPath)) return null;
  try {
    const head = readFileSync(headPath, "utf-8").trim();
    return head.startsWith("ref: ") ? head.replace("ref: refs/heads/", "") : head.substring(0, 8);
  } catch { return null; }
}

function listRecentLoops(limit = 10): Array<{
  program: string;
  branch: string | null;
  dir: string;
  hasResults: boolean;
}> {
  const loops: Array<{ program: string; branch: string | null; dir: string; hasResults: boolean; mtime: number }> = [];

  const scanDir = (dir: string, depth = 0) => {
    if (depth > 3) return;
    try {
      const entries = readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory() && !entry.name.startsWith(".") && !entry.name.startsWith("node_modules")) {
          const fullPath = join(dir, entry.name);
          const tsvPath = join(fullPath, "results.tsv");
          if (existsSync(tsvPath)) {
            const mtime = statSync(tsvPath).mtimeMs;
            loops.push({
              program: existsSync(join(fullPath, "program.md")) ? basename(fullPath) : "unknown",
              branch: findGitBranch(fullPath),
              dir: fullPath,
              hasResults: true,
              mtime,
            });
          }
          scanDir(fullPath, depth + 1);
        }
      }
    } catch {}
  };

  scanDir(RESULTS_DIR);

  return loops
    .sort((a, b) => b.mtime - a.mtime)
    .slice(0, limit)
    .map(({ mtime, ...rest }) => rest);
}

function isLoopRunning(programPath: string): boolean {
  const lockFile = join(dirname(programPath), ".autoloop.lock");
  return existsSync(lockFile);
}

// --- Tool implementations ---

function toolAutoloopStart(args: { program: string; executor?: string; resume?: boolean; dryRun?: boolean }): string {
  const programPath = args.program.startsWith("/") ? args.program : join(RESULTS_DIR, args.program);
  if (!existsSync(programPath)) return `Program not found: ${programPath}`;

  const script = getAutoloopScript();
  const cmd = [`node`, script, "--program", programPath];
  if (args.executor) cmd.push("--executor", args.executor);
  if (args.resume) cmd.push("--resume");
  if (args.dryRun) cmd.push("--dry-run");

  if (args.dryRun) {
    try {
      const output = execSync(cmd.join(" "), { cwd: dirname(programPath), encoding: "utf-8" });
      return `Dry run:\n${output}`;
    } catch (err: any) {
      return `Error: ${err.stderr || err.message}`;
    }
  }

  try {
    const { spawn } = require("child_process");
    const proc = spawn(cmd[0], cmd.slice(1), {
      cwd: dirname(programPath),
      detached: true,
      stdio: "ignore",
    });
    proc.unref();
    return `Autoloop started for ${basename(dirname(programPath))}\nProgram: ${programPath}`;
  } catch (err: any) {
    return `Error: ${err.message}`;
  }
}

function toolAutoloopStatus(args: { program: string }): string {
  const programPath = args.program.startsWith("/") ? args.program : join(RESULTS_DIR, args.program);
  if (!existsSync(programPath)) return `Program not found`;

  const dir = dirname(programPath);
  let output = `Status: ${isLoopRunning(programPath) ? "running" : "stopped"}\n`;
  const branch = findGitBranch(dir);
  if (branch) output += `Branch: ${branch}\n`;

  const resultsPath = findResultsTsv(programPath);
  if (resultsPath && existsSync(resultsPath)) {
    const content = readFileSync(resultsPath, "utf-8");
    const lines = content.trim().split("\n");
    if (lines.length > 1) {
      output += `Experiments: ${lines.length - 1}\n`;
      output += `\nRecent:\n`;
      lines.slice(-5).forEach(line => { output += `  ${line}\n`; });
    }
  } else {
    output += `No results yet.\n`;
  }

  return output;
}

function toolAutoloopResults(args: { program: string; limit?: number }): string {
  const programPath = args.program.startsWith("/") ? args.program : join(RESULTS_DIR, args.program);
  const resultsPath = findResultsTsv(programPath);
  if (!resultsPath || !existsSync(resultsPath)) return "No results found.";

  const content = readFileSync(resultsPath, "utf-8");
  const lines = content.trim().split("\n");
  if (lines.length <= 1) return "No data.";

  const limit = args.limit || lines.length;
  return lines.slice(0, 1).concat(lines.slice(-(limit))).join("\n") + `\n\n(${lines.length - 1} total experiments)`;
}

function toolAutoloopStop(args: { program: string }): string {
  const programPath = args.program.startsWith("/") ? args.program : join(RESULTS_DIR, args.program);
  const lockFile = join(dirname(programPath), ".autoloop.lock");

  if (!existsSync(lockFile)) return "Not running.";

  try {
    const pid = readFileSync(lockFile, "utf-8").trim();
    try { process.kill(parseInt(pid), "SIGTERM"); } catch {}
    unlinkSync(lockFile);
    return "Stopped.";
  } catch (err: any) {
    return `Error: ${err.message}`;
  }
}

function toolAutoloopList(args: { limit?: number }): string {
  const loops = listRecentLoops(args.limit || 10);
  if (loops.length === 0) return "No recent loops found.";

  let output = `Recent autoloop runs (${loops.length}):\n\n`;
  loops.forEach(loop => {
    output += `${loop.program}${loop.branch ? ` — ${loop.branch}` : ""} — ${loop.hasResults ? "has results" : "no results"}\n`;
  });
  return output;
}

// --- MCP Server ---

const TOOLS = [
  { name: "autoloop_start", description: "Start an autoloop optimization campaign.", inputSchema: { type: "object" as const, properties: { program: { type: "string", description: "Path to program.md" }, executor: { type: "string", description: "Shell command for LLM proposals (reads stdin)" }, resume: { type: "boolean" }, dryRun: { type: "boolean" } }, required: ["program"] } },
  { name: "autoloop_status", description: "Check autoloop status.", inputSchema: { type: "object" as const, properties: { program: { type: "string" } }, required: ["program"] } },
  { name: "autoloop_results", description: "Get experiment results.", inputSchema: { type: "object" as const, properties: { program: { type: "string" }, limit: { type: "number" } }, required: ["program"] } },
  { name: "autoloop_stop", description: "Stop a running autoloop.", inputSchema: { type: "object" as const, properties: { program: { type: "string" } }, required: ["program"] } },
  { name: "autoloop_list", description: "List recent autoloop campaigns.", inputSchema: { type: "object" as const, properties: { limit: { type: "number" } } } },
];

const server = new Server(
  { name: "autoloop", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    let result: string;
    switch (name) {
      case "autoloop_start": result = toolAutoloopStart(args as any); break;
      case "autoloop_status": result = toolAutoloopStatus(args as any); break;
      case "autoloop_results": result = toolAutoloopResults(args as any); break;
      case "autoloop_stop": result = toolAutoloopStop(args as any); break;
      case "autoloop_list": result = toolAutoloopList(args as any); break;
      default: result = `Unknown: ${name}`;
    }
    return { content: [{ type: "text", text: result }] };
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("@zouroboros/autoloop MCP server running on stdio");
}

main().catch(console.error);
