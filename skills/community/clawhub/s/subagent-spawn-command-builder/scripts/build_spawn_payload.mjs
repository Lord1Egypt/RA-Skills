#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT = path.resolve(__dirname, "..");
const STATE_DIR = path.join(ROOT, "state");
const LOG_PATH = path.join(STATE_DIR, "build-log.jsonl");

function usage() {
  console.error(`Build sessions_spawn payload from CLI arguments (values from TOOLS.md)\n\n` +
`Usage:\n` +
`  node scripts/build_spawn_payload.mjs --profile <name> --task <text> [options]\n\n` +
`Options:\n` +
`  --profile <name>              profile label for logging (required)\n` +
`  --task <text>                 task text for subagent (required)\n` +
`  --label <text>                sessions_spawn.label\n` +
`  --agent-id <id>               sessions_spawn.agentId\n` +
`  --model <name>                sessions_spawn.model\n` +
`  --thinking <value>            sessions_spawn.thinking\n` +
`  --run-timeout-seconds <int>   sessions_spawn.runTimeoutSeconds\n` +
`  --cleanup <keep|delete>       sessions_spawn.cleanup\n` +
`  --cwd <path>                  sessions_spawn.cwd (working directory for subagent)\n` +
`  --mode <run|session>          sessions_spawn.mode\n` +
`  -h, --help                    show this help\n`);
}

function parseArgs(argv) {
  const out = {
    profile: "",
    task: "",
    label: "",
    agentId: "",
    model: "",
    thinking: "",
    runTimeoutSeconds: undefined,
    cleanup: "",
    cwd: "",
    mode: "",
  };

  const map = new Map([
    ["--profile", "profile"],
    ["--task", "task"],
    ["--label", "label"],
    ["--agent-id", "agentId"],
    ["--model", "model"],
    ["--thinking", "thinking"],
    ["--run-timeout-seconds", "runTimeoutSeconds"],
    ["--cleanup", "cleanup"],
    ["--cwd", "cwd"],
    ["--mode", "mode"],
  ]);

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "-h" || a === "--help") {
      usage();
      process.exit(0);
    }

    if (!map.has(a)) {
      throw new Error(`Unknown option: ${a}`);
    }

    const key = map.get(a);
    const val = argv[i + 1];
    if (val == null || val.startsWith("--")) {
      throw new Error(`Missing value for ${a}`);
    }
    i += 1;

    if (key === "runTimeoutSeconds") {
      const n = Number.parseInt(val, 10);
      if (!Number.isFinite(n)) throw new Error(`Invalid integer for ${a}: ${val}`);
      out[key] = n;
    } else {
      out[key] = val;
    }
  }

  if (!out.profile) throw new Error("--profile is required");
  if (!out.task) throw new Error("--task is required");
  if (out.cleanup && !["keep", "delete"].includes(out.cleanup)) {
    throw new Error(`--cleanup must be keep|delete, got: ${out.cleanup}`);
  }
  if (out.mode && !["run", "session"].includes(out.mode)) {
    throw new Error(`--mode must be run|session, got: ${out.mode}`);
  }

  return out;
}

function nonEmpty(v) {
  return v !== undefined && v !== null && v !== "";
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  const payload = { task: args.task };

  payload.label = nonEmpty(args.label)
    ? args.label
    : `${args.profile}-${Math.floor(Date.now() / 1000)}`;

  if (nonEmpty(args.agentId)) payload.agentId = args.agentId;
  if (nonEmpty(args.model)) payload.model = args.model;
  if (nonEmpty(args.thinking)) payload.thinking = args.thinking;
  if (args.runTimeoutSeconds !== undefined) payload.runTimeoutSeconds = args.runTimeoutSeconds;
  if (nonEmpty(args.cleanup)) payload.cleanup = args.cleanup;
  if (nonEmpty(args.cwd)) payload.cwd = args.cwd;
  if (nonEmpty(args.mode)) payload.mode = args.mode;

  fs.mkdirSync(STATE_DIR, { recursive: true });
  const logLine = JSON.stringify({ ts: Math.floor(Date.now() / 1000), profile: args.profile, payload }, null, 0) + "\n";
  fs.appendFileSync(LOG_PATH, logLine, "utf8");

  process.stdout.write(JSON.stringify(payload, null, 2) + "\n");
}

try {
  main();
} catch (err) {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
}
