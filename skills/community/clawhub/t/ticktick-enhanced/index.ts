#!/usr/bin/env bun

/**
 * TickTick Skill Handler for OpenClaw
 *
 * This script parses OpenClaw command arguments and invokes
 * the TickTick CLI with JSON output for structured parsing.
 *
 * Usage: This is invoked automatically by OpenClaw when
 * user types /tasks or /ticktick with arguments.
 */

import { $ } from "bun";

// Commands we support:
// - projects: list projects
// - tasks: list tasks
// - add: create task
// - done: complete task
// - abandon: mark won't do

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log("Usage: /tasks <command> [options]");
  console.log("Try: /tasks projects, /tasks add \"Task name\", /tasks done \"Task\"");
  process.exit(0);
}

const command = args[0];

// Build the ticktick CLI command
let cmd = "bun run scripts/ticktick.ts";

switch (command) {
  case "projects":
  case "lists":
    cmd += " lists --json";
    break;
  case "tasks":
    // Parse options: --project, --status, etc.
    cmd += " tasks --json";
    // Pass through any additional args (--list, --status, etc.)
    if (args.length > 1) {
      cmd += " " + args.slice(1).join(" ");
    }
    break;
  case "add":
    // Create task: /tasks add "title" [options]
    cmd += " task " + args.slice(1).join(" ");
    break;
  case "done":
  case "complete":
    cmd += " complete " + args.slice(1).join(" ");
    break;
  case "abandon":
    cmd += " abandon " + args.slice(1).join(" ");
    break;
  default:
    console.error(`Unknown command: ${command}`);
    process.exit(1);
}

// Execute and pass through output
const proc = Bun.spawnSync(cmd, {
  cwd: process.env.OPENCLAW_SKILL_DIR || __dirname,
  stdin: "inherit",
  stdout: "inherit",
  stderr: "inherit",
});

process.exit(proc.exitCode);
